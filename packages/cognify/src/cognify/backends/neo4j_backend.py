"""
Fleet/server backend: TurboVec (vectors) + Neo4j (typed graph).

Graph model (C-prefixed labels so Cognify never collides with other graphs in the
same Neo4j; every node carries tenant + namespace):

  (:CDocument)-[:PART_OF]<-(:CChunk)  (:CEntity)-[:MENTIONED_IN]->(:CChunk)
  (:CEntity)-[:REL {type}]->(:CEntity)
"""
from __future__ import annotations

import hashlib
import json
import re
import threading
import time
from pathlib import Path
from typing import Optional

import numpy as np

from .. import config

_DOC, _CHUNK, _ENT = "CDocument", "CChunk", "CEntity"


def _safe(t: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", t)


def _cid_int(s: str) -> int:
    return int.from_bytes(hashlib.sha256(s.encode()).digest()[:8], "little") & 0x7FFFFFFFFFFFFFFF


def _entity_id(tenant: str, name: str, etype: str) -> str:
    return f"{tenant}::{name.lower().strip()}::{etype}"


class Neo4jBackend:
    def __init__(self):
        import turbovec  # noqa: F401  (validate availability early)
        from neo4j import GraphDatabase
        c = config.neo4j_creds()
        if not c.get("uri") or not c.get("password"):
            raise RuntimeError("Set NEO4J_URI and NEO4J_PASSWORD (see .env.example)")
        self._driver = GraphDatabase.driver(c["uri"], auth=(c["user"], c["password"]))
        self._root = config.DATA_DIR / "neo4j"
        self._lock = threading.Lock()
        self._idx, self._meta = {}, {}
        self._ensure_schema()

    def _ensure_schema(self):
        with self._driver.session() as s:
            for lbl in (_DOC, _CHUNK, _ENT):
                s.run(f"CREATE INDEX {lbl.lower()}_id IF NOT EXISTS FOR (n:{lbl}) ON (n.id)")
            s.run(f"CREATE INDEX {_ENT.lower()}_tenant IF NOT EXISTS FOR (n:{_ENT}) ON (n.tenant)")

    # -- per-tenant TurboVec index ----------------------------------------
    def _tenant_dir(self, tenant: str) -> Path:
        d = self._root / _safe(tenant)
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _load_index(self, tenant: str):
        import turbovec
        if tenant in self._idx:
            return self._idx[tenant], self._meta[tenant]
        d = self._tenant_dir(tenant)
        ip, mp = d / "index.turbo", d / "meta.json"
        if ip.exists() and mp.exists():
            idx = turbovec.IdMapIndex.load(str(ip))
            meta = {int(k): v for k, v in json.loads(mp.read_text()).items()}
        else:
            idx, meta = turbovec.IdMapIndex(dim=config.EMBED_DIM), {}
        self._idx[tenant], self._meta[tenant] = idx, meta
        return idx, meta

    def _save_index(self, tenant: str):
        d = self._tenant_dir(tenant)
        self._idx[tenant].write(str(d / "index.turbo"))
        (d / "meta.json").write_text(json.dumps({str(k): v for k, v in self._meta[tenant].items()}))

    # -- load --------------------------------------------------------------
    def load_document(self, doc, *, tenant, namespace, agent, chunk_vecs, extractions):
        with self._lock:
            idx, meta = self._load_index(tenant)
            ids = []
            for c in doc.chunks:
                cint = _cid_int(c.id)
                try:
                    idx.remove(cint)
                except Exception:
                    pass
                ids.append(cint)
                meta[cint] = {"id": c.id, "doc_id": c.doc_id, "ord": c.ord, "heading": c.heading,
                              "text": c.text[:600], "tenant": tenant, "namespace": namespace,
                              "title": doc.title}
            if doc.chunks:
                idx.add_with_ids(np.asarray(chunk_vecs, dtype=np.float32),
                                 np.asarray(ids, dtype=np.uint64))
            self._save_index(tenant)
            self._write_graph(doc, tenant, namespace, agent, extractions)

    def _write_graph(self, doc, tenant, namespace, agent, extractions):
        ts = time.time()
        chunk_rows = [{"id": c.id, "doc_id": c.doc_id, "ord": c.ord, "heading": c.heading,
                       "text": c.text[:2000]} for c in doc.chunks]
        ent_rows, ment_rows, rel_rows = [], [], []
        for c in doc.chunks:
            ex = extractions.get(c.id)
            if not ex:
                continue
            n2i = {}
            for e in ex.entities:
                eid = _entity_id(tenant, e.name, e.type)
                n2i[e.name.lower()] = eid
                ent_rows.append({"id": eid, "name": e.name, "etype": e.type})
                ment_rows.append({"eid": eid, "cid": c.id})
            for r in ex.relations:
                sid, oid = n2i.get(r.subject.lower()), n2i.get(r.object.lower())
                if sid and oid and sid != oid:
                    rel_rows.append({"sid": sid, "oid": oid, "type": r.predicate, "doc_id": doc.id})
        with self._driver.session() as s:
            s.run(f"MERGE (d:{_DOC} {{id:$id}}) SET d.tenant=$t,d.namespace=$n,d.agent=$a,"
                  "d.title=$ti,d.source=$src,d.ts=$ts",
                  id=doc.id, t=tenant, n=namespace, a=agent, ti=doc.title, src=doc.source, ts=ts)
            s.run(f"UNWIND $rows AS r MERGE (c:{_CHUNK} {{id:r.id}}) "
                  "SET c.tenant=$t,c.namespace=$n,c.doc_id=r.doc_id,c.ord=r.ord,"
                  "c.heading=r.heading,c.text=r.text "
                  f"WITH c MATCH (d:{_DOC} {{id:$doc}}) MERGE (c)-[:PART_OF]->(d)",
                  rows=chunk_rows, t=tenant, n=namespace, doc=doc.id)
            if ent_rows:
                s.run(f"UNWIND $rows AS r MERGE (e:{_ENT} {{id:r.id}}) "
                      "SET e.tenant=$t,e.namespace=$n,e.name=r.name,e.etype=r.etype",
                      rows=ent_rows, t=tenant, n=namespace)
            if ment_rows:
                s.run(f"UNWIND $rows AS r MATCH (e:{_ENT} {{id:r.eid}}) "
                      f"MATCH (c:{_CHUNK} {{id:r.cid}}) MERGE (e)-[:MENTIONED_IN]->(c)", rows=ment_rows)
            if rel_rows:
                s.run(f"UNWIND $rows AS r MATCH (a:{_ENT} {{id:r.sid}}) MATCH (b:{_ENT} {{id:r.oid}}) "
                      "MERGE (a)-[rel:REL {type:r.type}]->(b) SET rel.doc_id=r.doc_id", rows=rel_rows)

    # -- search ------------------------------------------------------------
    def search(self, qvec, *, tenant, namespace, k):
        with self._lock:
            idx, meta = self._load_index(tenant)
            if not meta:
                return []
            scores, ids = idx.search(np.asarray(qvec, dtype=np.float32), min(k * 3, max(k, 30)))
        out, seen = [], set()
        for sc, uid in zip(scores[0].tolist(), ids[0].tolist()):
            row = meta.get(int(uid))
            if not row or (namespace and row.get("namespace") != namespace):
                continue
            tk = row.get("text", "")[:120]
            if tk in seen:
                continue
            seen.add(tk)
            out.append({**row, "score": round(float(sc), 4)})
            if len(out) >= k:
                break
        return out

    # -- expand ------------------------------------------------------------
    def expand(self, chunk_ids, *, tenant, hops):
        if not chunk_ids:
            return {"entities": [], "relations": []}
        with self._driver.session() as s:
            ent = s.run(f"MATCH (e:{_ENT})-[:MENTIONED_IN]->(c:{_CHUNK}) "
                        "WHERE c.id IN $cids AND e.tenant=$t "
                        "RETURN DISTINCT e.name AS name,e.etype AS etype,e.id AS id LIMIT 100",
                        cids=chunk_ids, t=tenant).data()
            eids = [e["id"] for e in ent]
            rel = s.run(f"MATCH (a:{_ENT})-[r:REL]->(b:{_ENT}) WHERE a.id IN $e AND a.tenant=$t "
                        "RETURN a.name AS subject,r.type AS predicate,b.name AS object LIMIT 200",
                        e=eids, t=tenant).data() if eids else []
        return {"entities": ent, "relations": rel}

    # -- stats -------------------------------------------------------------
    def stats(self, *, tenant):
        where = "WHERE n.tenant=$t" if tenant else ""
        p = {"t": tenant} if tenant else {}
        with self._driver.session() as s:
            d = s.run(f"MATCH (n:{_DOC}) {where} RETURN count(n) AS c", **p).single()["c"]
            c = s.run(f"MATCH (n:{_CHUNK}) {where} RETURN count(n) AS c", **p).single()["c"]
            e = s.run(f"MATCH (n:{_ENT}) {where} RETURN count(n) AS c", **p).single()["c"]
            r = s.run(f"MATCH (:{_ENT})-[rel:REL]->() "
                      + ("WHERE startNode(rel).tenant=$t " if tenant else "")
                      + "RETURN count(rel) AS c", **p).single()["c"]
        return {"documents": d, "chunks": c, "entities": e, "relations": r}

    def close(self):
        self._driver.close()
