#!/usr/bin/env python3
"""
Fleet backend for Cognify: TurboVec (vectors) + Neo4j (typed graph).

Graph model (all nodes carry a `tenant` and `namespace` property; Cognify uses
its own C-prefixed labels so it never collides with the legacy giga-graph
Memory/Document nodes living in the same Neo4j):

  (:CDocument {id, tenant, namespace, agent, title, source, ts})
  (:CChunk    {id, tenant, namespace, doc_id, ord, heading, text})
  (:CEntity   {id, tenant, namespace, name, etype})

  (:CChunk)-[:PART_OF]->(:CDocument)
  (:CEntity)-[:MENTIONED_IN]->(:CChunk)
  (:CEntity)-[:REL {type, doc_id}]->(:CEntity)

Vectors live in a per-tenant TurboVec IdMapIndex on disk; an id->meta map lets us
turn vector hits back into chunk rows for graph expansion.
"""
from __future__ import annotations

import os
os.environ.setdefault("DYLD_LIBRARY_PATH", "/opt/homebrew/opt/expat/lib:/opt/homebrew/lib")

import hashlib
import json
import logging
import re
import threading
import time
from pathlib import Path
from typing import Optional

import numpy as np

log = logging.getLogger("cognify.neo4j")

DATA_ROOT = Path("/Users/appie/clawd/.data/cognify")
EMBED_DIM = 384

_ENTITY_LABEL = "CEntity"
_CHUNK_LABEL = "CChunk"
_DOC_LABEL = "CDocument"


def _safe(tenant: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", tenant)


def _cid_int(chunk_id: str) -> int:
    h = hashlib.sha256(chunk_id.encode()).digest()
    return int.from_bytes(h[:8], "little") & 0x7FFFFFFFFFFFFFFF


def _entity_id(tenant: str, name: str, etype: str) -> str:
    return f"{tenant}::{name.lower().strip()}::{etype}"


def _read_neo4j_creds() -> dict:
    v: dict[str, str] = {}
    for f in [
        "/Users/appie/.hermes/mission-control/.env",
        "/Users/appie/.hermes/mission-control/.env.local",
    ]:
        try:
            txt = open(f).read()
        except FileNotFoundError:
            continue
        for k in ("NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD"):
            m = re.search(rf'^{k}=(.+)$', txt, re.M)
            if m and m.group(1).strip():
                v.setdefault(k, m.group(1).strip().strip('"').strip("'"))
    # Env fills gaps only (used on boxes without the MC .env). File creds win,
    # because a stale exported NEO4J_PASSWORD in the shell profile must not
    # silently override the canonical file value.
    for k in ("NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD"):
        if not v.get(k) and os.environ.get(k):
            v[k] = os.environ[k]
    return v


class CognifyNeo4j:
    """Fleet backend. Thread-safe for the single-writer server use."""

    def __init__(self, creds: Optional[dict] = None):
        from neo4j import GraphDatabase
        c = creds or _read_neo4j_creds()
        if not c.get("NEO4J_URI"):
            raise RuntimeError("Neo4j creds not found")
        self._driver = GraphDatabase.driver(c["NEO4J_URI"], auth=(c["NEO4J_USER"], c["NEO4J_PASSWORD"]))
        self._lock = threading.Lock()
        self._indexes: dict[str, object] = {}   # tenant -> IdMapIndex
        self._meta: dict[str, dict[int, dict]] = {}  # tenant -> {id_int: row}
        self._ensure_schema()

    # -- schema ------------------------------------------------------------
    def _ensure_schema(self) -> None:
        stmts = [
            f"CREATE INDEX cdoc_id IF NOT EXISTS FOR (n:{_DOC_LABEL}) ON (n.id)",
            f"CREATE INDEX cchunk_id IF NOT EXISTS FOR (n:{_CHUNK_LABEL}) ON (n.id)",
            f"CREATE INDEX centity_id IF NOT EXISTS FOR (n:{_ENTITY_LABEL}) ON (n.id)",
            f"CREATE INDEX centity_tenant IF NOT EXISTS FOR (n:{_ENTITY_LABEL}) ON (n.tenant)",
        ]
        with self._driver.session() as s:
            for st in stmts:
                try:
                    s.run(st)
                except Exception as e:
                    log.warning("schema stmt failed: %s", e)

    # -- per-tenant vector index ------------------------------------------
    def _tenant_dir(self, tenant: str) -> Path:
        d = DATA_ROOT / _safe(tenant)
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _load_index(self, tenant: str):
        import turbovec
        if tenant in self._indexes:
            return self._indexes[tenant], self._meta[tenant]
        d = self._tenant_dir(tenant)
        idx_path = d / "index.turbo"
        meta_path = d / "meta.json"
        if idx_path.exists() and meta_path.exists():
            idx = turbovec.IdMapIndex.load(str(idx_path))
            meta_raw = json.loads(meta_path.read_text())
            meta = {int(k): v for k, v in meta_raw.items()}
        else:
            idx = turbovec.IdMapIndex(dim=EMBED_DIM)
            meta = {}
        self._indexes[tenant] = idx
        self._meta[tenant] = meta
        return idx, meta

    def _save_index(self, tenant: str) -> None:
        d = self._tenant_dir(tenant)
        self._indexes[tenant].write(str(d / "index.turbo"))
        (d / "meta.json").write_text(json.dumps({str(k): v for k, v in self._meta[tenant].items()}))

    # -- load (the L in ECL) ----------------------------------------------
    def load_document(self, doc, *, tenant, namespace, agent, chunk_vecs, extractions) -> None:
        with self._lock:
            idx, meta = self._load_index(tenant)

            # 1. vectors -> TurboVec
            ids = []
            for i, c in enumerate(doc.chunks):
                cint = _cid_int(c.id)
                try:
                    idx.remove(cint)  # idempotent re-ingest
                except Exception:
                    pass
                ids.append(cint)
                meta[cint] = {
                    "id": c.id, "doc_id": c.doc_id, "ord": c.ord,
                    "heading": c.heading, "text": c.text[:600],
                    "tenant": tenant, "namespace": namespace, "title": doc.title,
                }
            if len(doc.chunks):
                idx.add_with_ids(np.asarray(chunk_vecs, dtype=np.float32),
                                 np.asarray(ids, dtype=np.uint64))
            self._save_index(tenant)

            # 2. graph -> Neo4j
            self._write_graph(doc, tenant, namespace, agent, extractions)

    def _write_graph(self, doc, tenant, namespace, agent, extractions) -> None:
        ts = time.time()
        chunk_rows = [
            {"id": c.id, "doc_id": c.doc_id, "ord": c.ord, "heading": c.heading,
             "text": c.text[:2000]}
            for c in doc.chunks
        ]
        # entities + relations flattened with provenance
        ent_rows: list[dict] = []
        ment_rows: list[dict] = []
        rel_rows: list[dict] = []
        for c in doc.chunks:
            ex = extractions.get(c.id)
            if not ex:
                continue
            name_to_id: dict[str, str] = {}
            for e in ex.entities:
                eid = _entity_id(tenant, e.name, e.type)
                name_to_id[e.name.lower()] = eid
                ent_rows.append({"id": eid, "name": e.name, "etype": e.type})
                ment_rows.append({"eid": eid, "cid": c.id})
            for r in ex.relations:
                sid = name_to_id.get(r.subject.lower())
                oid = name_to_id.get(r.object.lower())
                if sid and oid and sid != oid:
                    rel_rows.append({"sid": sid, "oid": oid, "type": r.predicate, "doc_id": doc.id})

        with self._driver.session() as s:
            s.run(
                f"MERGE (d:{_DOC_LABEL} {{id:$id}}) "
                "SET d.tenant=$tenant, d.namespace=$ns, d.agent=$agent, "
                "d.title=$title, d.source=$source, d.ts=$ts",
                id=doc.id, tenant=tenant, ns=namespace, agent=agent,
                title=doc.title, source=doc.source, ts=ts,
            )
            s.run(
                f"UNWIND $rows AS r MERGE (c:{_CHUNK_LABEL} {{id:r.id}}) "
                "SET c.tenant=$tenant, c.namespace=$ns, c.doc_id=r.doc_id, "
                "c.ord=r.ord, c.heading=r.heading, c.text=r.text "
                f"WITH c MATCH (d:{_DOC_LABEL} {{id:$doc}}) MERGE (c)-[:PART_OF]->(d)",
                rows=chunk_rows, tenant=tenant, ns=namespace, doc=doc.id,
            )
            if ent_rows:
                s.run(
                    f"UNWIND $rows AS r MERGE (e:{_ENTITY_LABEL} {{id:r.id}}) "
                    "SET e.tenant=$tenant, e.namespace=$ns, e.name=r.name, e.etype=r.etype",
                    rows=ent_rows, tenant=tenant, ns=namespace,
                )
            if ment_rows:
                s.run(
                    f"UNWIND $rows AS r MATCH (e:{_ENTITY_LABEL} {{id:r.eid}}) "
                    f"MATCH (c:{_CHUNK_LABEL} {{id:r.cid}}) MERGE (e)-[:MENTIONED_IN]->(c)",
                    rows=ment_rows,
                )
            if rel_rows:
                s.run(
                    f"UNWIND $rows AS r MATCH (a:{_ENTITY_LABEL} {{id:r.sid}}) "
                    f"MATCH (b:{_ENTITY_LABEL} {{id:r.oid}}) "
                    "MERGE (a)-[rel:REL {type:r.type}]->(b) SET rel.doc_id=r.doc_id",
                    rows=rel_rows,
                )

    # -- search (vector) ---------------------------------------------------
    def search(self, qvec, *, tenant, namespace, k) -> list[dict]:
        with self._lock:
            idx, meta = self._load_index(tenant)
            if not meta:
                return []
            scores, ids = idx.search(np.asarray(qvec, dtype=np.float32), min(k * 3, max(k, 30)))
        out: list[dict] = []
        seen_text: set[str] = set()
        for sc, uid in zip(scores[0].tolist(), ids[0].tolist()):
            row = meta.get(int(uid))
            if not row:
                continue
            if namespace and row.get("namespace") != namespace:
                continue
            tkey = row.get("text", "")[:120]
            if tkey in seen_text:
                continue
            seen_text.add(tkey)
            out.append({**row, "score": round(float(sc), 4)})
            if len(out) >= k:
                break
        return out

    # -- expand (graph) ----------------------------------------------------
    def expand(self, chunk_ids, *, tenant, hops) -> dict:
        if not chunk_ids:
            return {"entities": [], "relations": []}
        with self._driver.session() as s:
            ent = s.run(
                f"MATCH (e:{_ENTITY_LABEL})-[:MENTIONED_IN]->(c:{_CHUNK_LABEL}) "
                "WHERE c.id IN $cids AND e.tenant=$tenant "
                "RETURN DISTINCT e.name AS name, e.etype AS etype, e.id AS id LIMIT 100",
                cids=chunk_ids, tenant=tenant,
            ).data()
            eids = [e["id"] for e in ent]
            rel = []
            if eids:
                rel = s.run(
                    f"MATCH (a:{_ENTITY_LABEL})-[r:REL]->(b:{_ENTITY_LABEL}) "
                    "WHERE a.id IN $eids AND a.tenant=$tenant "
                    "RETURN a.name AS subject, r.type AS predicate, b.name AS object LIMIT 200",
                    eids=eids, tenant=tenant,
                ).data()
        return {"entities": ent, "relations": rel}

    # -- stats -------------------------------------------------------------
    def stats(self, *, tenant) -> dict:
        with self._driver.session() as s:
            where = "WHERE n.tenant=$tenant" if tenant else ""
            params = {"tenant": tenant} if tenant else {}
            docs = s.run(f"MATCH (n:{_DOC_LABEL}) {where} RETURN count(n) AS c", **params).single()["c"]
            chunks = s.run(f"MATCH (n:{_CHUNK_LABEL}) {where} RETURN count(n) AS c", **params).single()["c"]
            ents = s.run(f"MATCH (n:{_ENTITY_LABEL}) {where} RETURN count(n) AS c", **params).single()["c"]
            rels = s.run(
                f"MATCH (:{_ENTITY_LABEL})-[r:REL]->() "
                + ("WHERE startNode(r).tenant=$tenant " if tenant else "")
                + "RETURN count(r) AS c", **params
            ).single()["c"]
        return {"documents": docs, "chunks": chunks, "entities": ents, "relations": rels}

    def close(self) -> None:
        self._driver.close()
