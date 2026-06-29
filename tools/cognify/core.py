#!/usr/bin/env python3
"""
Cognify core: the ECL orchestration (Extract -> Cognify -> Load) plus the
shared embedder and the Backend protocol.

This is our own Cognee-equivalent, built on the stack we already run:
  - TurboVec + Neo4j   for the fleet  (backend_neo4j.CognifyNeo4j)
  - ChromaDB + networkx for client agents on isolated Orgo boxes (backend_local)

ingest():  document -> chunks -> LLM typed entities/relations -> embed -> load
recall():  query -> vector hint -> graph expansion -> hybrid result

Multi-tenant: every call carries (tenant, namespace). The fleet uses
tenant="fleet"; each client agent uses its own tenant (e.g. "client:roslan") so
client data is physically partitioned and never bleeds across boxes.
"""
from __future__ import annotations

import os
os.environ.setdefault("DYLD_LIBRARY_PATH", "/opt/homebrew/opt/expat/lib:/opt/homebrew/lib")

import logging
from dataclasses import dataclass, field
from typing import Optional, Protocol

import numpy as np

from . import extractor as _ex
from .loader import Document, load

log = logging.getLogger("cognify")

MODEL_NAME = "all-MiniLM-L6-v2"
EMBED_DIM = 384


# ---------------------------------------------------------------------------
# Shared embedder (lazy singleton)
# ---------------------------------------------------------------------------
_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        log.info("loading embedding model %s", MODEL_NAME)
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed(texts: list[str]) -> np.ndarray:
    if not texts:
        return np.zeros((0, EMBED_DIM), dtype=np.float32)
    vecs = get_model().encode(texts, batch_size=64, normalize_embeddings=True, show_progress_bar=False)
    return np.asarray(vecs, dtype=np.float32)


def _embed_texts(backend, texts: list[str]) -> np.ndarray:
    """Use the backend's own embedder when it has one (client boxes use a
    torch-free ONNX MiniLM via ChromaDB); otherwise fall back to the shared
    sentence-transformers model. Both produce 384d normalized vectors."""
    fn = getattr(backend, "embed_texts", None)
    if callable(fn):
        return fn(texts)
    return embed(texts)


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class IngestResult:
    doc_id: str
    title: str
    tenant: str
    namespace: str
    chunks: int
    entities: int
    relations: int
    extracted: bool


@dataclass(frozen=True)
class RecallResult:
    query: str
    tenant: str
    chunks: tuple[dict, ...]
    entities: tuple[dict, ...]
    relations: tuple[dict, ...]


# ---------------------------------------------------------------------------
# Backend protocol — both Neo4j and local backends implement this
# ---------------------------------------------------------------------------
class Backend(Protocol):
    def load_document(
        self, doc: Document, *, tenant: str, namespace: str, agent: str,
        chunk_vecs: np.ndarray, extractions: dict[str, "_ex.Extraction"],
    ) -> None: ...

    def search(self, qvec: np.ndarray, *, tenant: str, namespace: Optional[str], k: int) -> list[dict]: ...

    def expand(self, chunk_ids: list[str], *, tenant: str, hops: int) -> dict: ...

    def stats(self, *, tenant: Optional[str]) -> dict: ...


# ---------------------------------------------------------------------------
# ECL orchestration
# ---------------------------------------------------------------------------
def ingest(
    backend: Backend,
    path_or_text: str,
    *,
    tenant: str = "fleet",
    namespace: str = "default",
    agent: str = "appie-opus",
    is_path: Optional[bool] = None,
    title: Optional[str] = None,
    do_extract: bool = True,
) -> IngestResult:
    """Run the full ECL pipeline for one document."""
    doc = load(path_or_text, is_path=is_path, title=title)
    if not doc.chunks:
        return IngestResult(doc.id, doc.title, tenant, namespace, 0, 0, 0, False)

    # Embed all chunks in one batch (backend-pluggable embedder).
    chunk_vecs = _embed_texts(backend, [c.text for c in doc.chunks])

    # Extract typed entities/relations per chunk (the Cognee lesson).
    extractions: dict[str, _ex.Extraction] = {}
    n_ent = n_rel = 0
    extracted_any = False
    if do_extract:
        for c in doc.chunks:
            try:
                ex = _ex.extract(c.text)
            except Exception as e:  # degrade gracefully, but log loudly
                log.warning("extraction failed for chunk %s: %s", c.id, e)
                ex = _ex.Extraction()
            extractions[c.id] = ex
            n_ent += len(ex.entities)
            n_rel += len(ex.relations)
            if ex.entities or ex.relations:
                extracted_any = True
    else:
        extractions = {c.id: _ex.Extraction() for c in doc.chunks}

    backend.load_document(
        doc, tenant=tenant, namespace=namespace, agent=agent,
        chunk_vecs=chunk_vecs, extractions=extractions,
    )
    return IngestResult(
        doc_id=doc.id, title=doc.title, tenant=tenant, namespace=namespace,
        chunks=len(doc.chunks), entities=n_ent, relations=n_rel, extracted=extracted_any,
    )


def recall(
    backend: Backend,
    query: str,
    *,
    tenant: str = "fleet",
    namespace: Optional[str] = None,
    k: int = 8,
    hops: int = 1,
) -> RecallResult:
    """Hybrid retrieval: vector search for relevant chunks, then expand the
    graph around them for typed entities/relations."""
    qvec = _embed_texts(backend, [query])
    chunks = backend.search(qvec, tenant=tenant, namespace=namespace, k=k)
    chunk_ids = [c["id"] for c in chunks]
    sub = backend.expand(chunk_ids, tenant=tenant, hops=hops) if chunk_ids else {"entities": [], "relations": []}
    return RecallResult(
        query=query, tenant=tenant,
        chunks=tuple(chunks),
        entities=tuple(sub.get("entities", [])),
        relations=tuple(sub.get("relations", [])),
    )
