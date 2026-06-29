"""
Cognify core — the ECL orchestration (Extract -> Cognify -> Load), the shared
embedder, and the Backend protocol both backends implement.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, Protocol

import numpy as np

from . import config, extractor as _ex
from .loader import Document, load

log = logging.getLogger("cognify")
_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(config.EMBED_MODEL)
    return _model


def embed(texts: list[str]) -> np.ndarray:
    if not texts:
        return np.zeros((0, config.EMBED_DIM), dtype=np.float32)
    v = get_model().encode(texts, batch_size=64, normalize_embeddings=True, show_progress_bar=False)
    return np.asarray(v, dtype=np.float32)


def _embed_texts(backend, texts: list[str]) -> np.ndarray:
    """Use the backend's own embedder if it has one (client boxes use a torch-free
    ONNX MiniLM via ChromaDB), else the shared sentence-transformers model."""
    fn = getattr(backend, "embed_texts", None)
    return fn(texts) if callable(fn) else embed(texts)


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


class Backend(Protocol):
    def load_document(self, doc: Document, *, tenant: str, namespace: str, agent: str,
                      chunk_vecs: np.ndarray, extractions: dict) -> None: ...
    def search(self, qvec: np.ndarray, *, tenant: str, namespace: Optional[str], k: int) -> list[dict]: ...
    def expand(self, chunk_ids: list[str], *, tenant: str, hops: int) -> dict: ...
    def stats(self, *, tenant: Optional[str]) -> dict: ...


def ingest(backend, path_or_text: str, *, tenant: str = "default", namespace: str = "default",
           agent: str = "agent", is_path: Optional[bool] = None, title: Optional[str] = None,
           do_extract: bool = True) -> IngestResult:
    doc = load(path_or_text, is_path=is_path, title=title)
    if not doc.chunks:
        return IngestResult(doc.id, doc.title, tenant, namespace, 0, 0, 0, False)

    chunk_vecs = _embed_texts(backend, [c.text for c in doc.chunks])

    extractions, n_ent, n_rel, extracted = {}, 0, 0, False
    for c in doc.chunks:
        if do_extract:
            try:
                ex = _ex.extract(c.text)
            except Exception as e:
                log.warning("extraction failed for %s: %s", c.id, e)
                ex = _ex.Extraction()
        else:
            ex = _ex.Extraction()
        extractions[c.id] = ex
        n_ent += len(ex.entities)
        n_rel += len(ex.relations)
        extracted = extracted or bool(ex.entities or ex.relations)

    backend.load_document(doc, tenant=tenant, namespace=namespace, agent=agent,
                          chunk_vecs=chunk_vecs, extractions=extractions)
    return IngestResult(doc.id, doc.title, tenant, namespace, len(doc.chunks), n_ent, n_rel, extracted)


def recall(backend, query: str, *, tenant: str = "default", namespace: Optional[str] = None,
           k: int = 8, hops: int = 1) -> RecallResult:
    qvec = _embed_texts(backend, [query])
    chunks = backend.search(qvec, tenant=tenant, namespace=namespace, k=k)
    cids = [c["id"] for c in chunks]
    sub = backend.expand(cids, tenant=tenant, hops=hops) if cids else {"entities": [], "relations": []}
    return RecallResult(query, tenant, tuple(chunks),
                        tuple(sub.get("entities", [])), tuple(sub.get("relations", [])))
