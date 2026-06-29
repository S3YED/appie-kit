#!/usr/bin/env python3
"""
Client backend for Cognify: ChromaDB (vectors) + networkx (typed graph).

Runs fully self-contained on an isolated Orgo client box. No Neo4j, no torch:
embeddings come from ChromaDB's bundled ONNX all-MiniLM-L6-v2 (same 384d space
as the fleet), so a client agent gets the same document-ingestion + graph build
the fleet has, but physically isolated to its own box and its own tenant.

Storage (under COGNIFY_LOCAL_DIR, default ~/.clark/cognify):
  chroma/                 ChromaDB persistent store (one collection per tenant)
  graph-<tenant>.json     networkx node-link graph (entities, typed edges, mentions)
"""
from __future__ import annotations

import json
import os
import re
import threading
from pathlib import Path
from typing import Optional

import numpy as np

LOCAL_DIR = Path(os.environ.get("COGNIFY_LOCAL_DIR", os.path.expanduser("~/.clark/cognify")))


def _safe(tenant: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", tenant)


def _entity_id(tenant: str, name: str, etype: str) -> str:
    return f"{tenant}::{name.lower().strip()}::{etype}"


class CognifyLocal:
    """Client backend. One ChromaDB collection + one networkx graph per tenant."""

    def __init__(self, root: Optional[str] = None):
        import chromadb
        from chromadb.utils import embedding_functions

        self.root = Path(root) if root else LOCAL_DIR
        self.root.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(self.root / "chroma"))
        # Torch-free ONNX MiniLM, 384d — matches the fleet's all-MiniLM space.
        self._ef = embedding_functions.ONNXMiniLM_L6_V2()
        self._lock = threading.Lock()
        self._graphs: dict[str, object] = {}   # tenant -> networkx.DiGraph

    # -- embedder (consumed by core via duck-typing) -----------------------
    def embed_texts(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, 384), dtype=np.float32)
        return np.asarray(self._ef(texts), dtype=np.float32)

    # -- chroma collection per tenant --------------------------------------
    def _collection(self, tenant: str):
        return self._client.get_or_create_collection(
            name=f"cognify_{_safe(tenant)}", metadata={"hnsw:space": "cosine"}
        )

    # -- networkx graph per tenant -----------------------------------------
    def _graph_path(self, tenant: str) -> Path:
        return self.root / f"graph-{_safe(tenant)}.json"

    def _load_graph(self, tenant: str):
        import networkx as nx
        if tenant in self._graphs:
            return self._graphs[tenant]
        p = self._graph_path(tenant)
        if p.exists():
            g = nx.node_link_graph(json.loads(p.read_text()), directed=True, edges="links")
        else:
            g = nx.DiGraph()
        self._graphs[tenant] = g
        return g

    def _save_graph(self, tenant: str) -> None:
        import networkx as nx
        g = self._graphs[tenant]
        data = nx.node_link_data(g, edges="links")
        self._graph_path(tenant).write_text(json.dumps(data))

    # -- load (the L in ECL) -----------------------------------------------
    def load_document(self, doc, *, tenant, namespace, agent, chunk_vecs, extractions) -> None:
        with self._lock:
            col = self._collection(tenant)
            ids = [c.id for c in doc.chunks]
            # Idempotent re-ingest: drop any prior chunks for this doc.
            try:
                col.delete(where={"doc_id": doc.id})
            except Exception:
                pass
            col.add(
                ids=ids,
                embeddings=[v.tolist() for v in np.asarray(chunk_vecs, dtype=np.float32)],
                documents=[c.text[:2000] for c in doc.chunks],
                metadatas=[{
                    "doc_id": c.doc_id, "ord": c.ord, "heading": c.heading or "",
                    "tenant": tenant, "namespace": namespace, "title": doc.title,
                } for c in doc.chunks],
            )

            g = self._load_graph(tenant)
            g.add_node(f"doc::{doc.id}", kind="document", title=doc.title, source=doc.source)
            for c in doc.chunks:
                g.add_node(f"chunk::{c.id}", kind="chunk", doc_id=c.doc_id, namespace=namespace)
                ex = extractions.get(c.id)
                if not ex:
                    continue
                name_to_id: dict[str, str] = {}
                for e in ex.entities:
                    eid = _entity_id(tenant, e.name, e.type)
                    name_to_id[e.name.lower()] = eid
                    g.add_node(eid, kind="entity", name=e.name, etype=e.type, namespace=namespace)
                    g.add_edge(eid, f"chunk::{c.id}", rel="MENTIONED_IN")
                for r in ex.relations:
                    sid = name_to_id.get(r.subject.lower())
                    oid = name_to_id.get(r.object.lower())
                    if sid and oid and sid != oid:
                        g.add_edge(sid, oid, rel="REL", type=r.predicate, doc_id=doc.id)
            self._save_graph(tenant)

    # -- search (vector) ---------------------------------------------------
    def search(self, qvec, *, tenant, namespace, k) -> list[dict]:
        col = self._collection(tenant)
        where = {"namespace": namespace} if namespace else None
        try:
            res = col.query(
                query_embeddings=[np.asarray(qvec, dtype=np.float32)[0].tolist()],
                n_results=k, where=where,
            )
        except Exception:
            return []
        out: list[dict] = []
        ids = (res.get("ids") or [[]])[0]
        docs = (res.get("documents") or [[]])[0]
        metas = (res.get("metadatas") or [[]])[0]
        dists = (res.get("distances") or [[]])[0]
        for i, cid in enumerate(ids):
            m = metas[i] or {}
            out.append({
                "id": cid, "text": docs[i] if i < len(docs) else "",
                "heading": m.get("heading", ""), "doc_id": m.get("doc_id", ""),
                "title": m.get("title", ""), "namespace": m.get("namespace", ""),
                "score": round(1.0 - float(dists[i]), 4) if i < len(dists) else 0.0,
            })
        return out

    # -- expand (graph) ----------------------------------------------------
    def expand(self, chunk_ids, *, tenant, hops) -> dict:
        g = self._load_graph(tenant)
        ent_ids: set[str] = set()
        for cid in chunk_ids:
            cnode = f"chunk::{cid}"
            if not g.has_node(cnode):
                continue
            # entities mention chunks: edge entity -> chunk, so look at predecessors
            for pred in g.predecessors(cnode):
                if g.nodes[pred].get("kind") == "entity":
                    ent_ids.add(pred)
        entities = [
            {"id": e, "name": g.nodes[e].get("name"), "etype": g.nodes[e].get("etype")}
            for e in ent_ids
        ]
        relations = []
        for e in ent_ids:
            for _, tgt, data in g.out_edges(e, data=True):
                if data.get("rel") == "REL":
                    relations.append({
                        "subject": g.nodes[e].get("name"),
                        "predicate": data.get("type"),
                        "object": g.nodes[tgt].get("name"),
                    })
        return {"entities": entities, "relations": relations[:200]}

    # -- stats -------------------------------------------------------------
    def stats(self, *, tenant) -> dict:
        g = self._load_graph(tenant) if tenant else None
        col = self._collection(tenant) if tenant else None
        kinds = {"document": 0, "chunk": 0, "entity": 0}
        rels = 0
        if g is not None:
            for _, d in g.nodes(data=True):
                k = d.get("kind")
                if k in kinds:
                    kinds[k] += 1
            rels = sum(1 for *_e, d in g.edges(data=True) if d.get("rel") == "REL")
        return {
            "documents": kinds["document"], "chunks": kinds["chunk"],
            "entities": kinds["entity"], "relations": rels,
            "vectors": col.count() if col is not None else 0,
        }

    def close(self) -> None:
        pass
