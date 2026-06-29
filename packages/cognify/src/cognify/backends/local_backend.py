"""
Local/agent backend: ChromaDB (vectors) + networkx (typed graph).

Fully self-contained, no external DB, no torch — embeddings come from ChromaDB's
bundled ONNX all-MiniLM (same 384d space as the server backend). Ideal to drop
into an isolated agent box.
"""
from __future__ import annotations

import json
import re
import threading
from pathlib import Path
from typing import Optional

import numpy as np

from .. import config


def _safe(t: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", t)


def _entity_id(tenant: str, name: str, etype: str) -> str:
    return f"{tenant}::{name.lower().strip()}::{etype}"


class LocalBackend:
    def __init__(self):
        import chromadb
        from chromadb.utils import embedding_functions
        self.root = config.DATA_DIR / "local"
        self.root.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(self.root / "chroma"))
        self._ef = embedding_functions.ONNXMiniLM_L6_V2()
        self._lock = threading.Lock()
        self._graphs = {}

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, config.EMBED_DIM), dtype=np.float32)
        return np.asarray(self._ef(texts), dtype=np.float32)

    def _collection(self, tenant):
        return self._client.get_or_create_collection(
            name=f"cognify_{_safe(tenant)}", metadata={"hnsw:space": "cosine"})

    def _graph_path(self, tenant):
        return self.root / f"graph-{_safe(tenant)}.json"

    def _load_graph(self, tenant):
        import networkx as nx
        if tenant in self._graphs:
            return self._graphs[tenant]
        p = self._graph_path(tenant)
        g = (nx.node_link_graph(json.loads(p.read_text()), directed=True, edges="links")
             if p.exists() else nx.DiGraph())
        self._graphs[tenant] = g
        return g

    def _save_graph(self, tenant):
        import networkx as nx
        self._graph_path(tenant).write_text(
            json.dumps(nx.node_link_data(self._graphs[tenant], edges="links")))

    def load_document(self, doc, *, tenant, namespace, agent, chunk_vecs, extractions):
        with self._lock:
            col = self._collection(tenant)
            try:
                col.delete(where={"doc_id": doc.id})
            except Exception:
                pass
            col.add(
                ids=[c.id for c in doc.chunks],
                embeddings=[v.tolist() for v in np.asarray(chunk_vecs, dtype=np.float32)],
                documents=[c.text[:2000] for c in doc.chunks],
                metadatas=[{"doc_id": c.doc_id, "ord": c.ord, "heading": c.heading or "",
                            "tenant": tenant, "namespace": namespace, "title": doc.title}
                           for c in doc.chunks],
            )
            g = self._load_graph(tenant)
            g.add_node(f"doc::{doc.id}", kind="document", title=doc.title, source=doc.source)
            for c in doc.chunks:
                g.add_node(f"chunk::{c.id}", kind="chunk", doc_id=c.doc_id, namespace=namespace)
                ex = extractions.get(c.id)
                if not ex:
                    continue
                n2i = {}
                for e in ex.entities:
                    eid = _entity_id(tenant, e.name, e.type)
                    n2i[e.name.lower()] = eid
                    g.add_node(eid, kind="entity", name=e.name, etype=e.type, namespace=namespace)
                    g.add_edge(eid, f"chunk::{c.id}", rel="MENTIONED_IN")
                for r in ex.relations:
                    sid, oid = n2i.get(r.subject.lower()), n2i.get(r.object.lower())
                    if sid and oid and sid != oid:
                        g.add_edge(sid, oid, rel="REL", type=r.predicate, doc_id=doc.id)
            self._save_graph(tenant)

    def search(self, qvec, *, tenant, namespace, k):
        col = self._collection(tenant)
        try:
            res = col.query(query_embeddings=[np.asarray(qvec, dtype=np.float32)[0].tolist()],
                            n_results=k, where={"namespace": namespace} if namespace else None)
        except Exception:
            return []
        ids = (res.get("ids") or [[]])[0]
        docs = (res.get("documents") or [[]])[0]
        metas = (res.get("metadatas") or [[]])[0]
        dists = (res.get("distances") or [[]])[0]
        out = []
        for i, cid in enumerate(ids):
            m = metas[i] or {}
            out.append({"id": cid, "text": docs[i] if i < len(docs) else "",
                        "heading": m.get("heading", ""), "doc_id": m.get("doc_id", ""),
                        "title": m.get("title", ""), "namespace": m.get("namespace", ""),
                        "score": round(1.0 - float(dists[i]), 4) if i < len(dists) else 0.0})
        return out

    def expand(self, chunk_ids, *, tenant, hops):
        g = self._load_graph(tenant)
        ent_ids = set()
        for cid in chunk_ids:
            cn = f"chunk::{cid}"
            if g.has_node(cn):
                ent_ids.update(p for p in g.predecessors(cn) if g.nodes[p].get("kind") == "entity")
        entities = [{"id": e, "name": g.nodes[e].get("name"), "etype": g.nodes[e].get("etype")}
                    for e in ent_ids]
        relations = []
        for e in ent_ids:
            for _, tgt, d in g.out_edges(e, data=True):
                if d.get("rel") == "REL":
                    relations.append({"subject": g.nodes[e].get("name"), "predicate": d.get("type"),
                                      "object": g.nodes[tgt].get("name")})
        return {"entities": entities, "relations": relations[:200]}

    def stats(self, *, tenant):
        g = self._load_graph(tenant) if tenant else None
        col = self._collection(tenant) if tenant else None
        kinds = {"document": 0, "chunk": 0, "entity": 0}
        rels = 0
        if g is not None:
            for _, d in g.nodes(data=True):
                if d.get("kind") in kinds:
                    kinds[d["kind"]] += 1
            rels = sum(1 for *_e, d in g.edges(data=True) if d.get("rel") == "REL")
        return {"documents": kinds["document"], "chunks": kinds["chunk"], "entities": kinds["entity"],
                "relations": rels, "vectors": col.count() if col is not None else 0}

    def close(self):
        pass
