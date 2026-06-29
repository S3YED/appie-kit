"""Cognify: fleet ECL (Extract-Cognify-Load) knowledge pipeline on TurboVec + Neo4j.

Public API:
    from cognify import ingest, recall, get_backend
    be = get_backend()                       # fleet (Neo4j) by default
    ingest(be, "path/to/doc.pdf", tenant="fleet", namespace="research")
    res = recall(be, "what does Clark use for memory?", tenant="fleet")
"""
from .core import ingest, recall, IngestResult, RecallResult, embed, get_model  # noqa: F401


def get_backend(kind: str | None = None, **kwargs):
    """Factory. kind: 'neo4j' (fleet, default) or 'local' (client Orgo box).

    Defaults to env COGNIFY_BACKEND, else 'neo4j'."""
    import os
    kind = kind or os.environ.get("COGNIFY_BACKEND", "neo4j")
    if kind == "neo4j":
        from .backend_neo4j import CognifyNeo4j
        return CognifyNeo4j(**kwargs)
    if kind == "local":
        from .backend_local import CognifyLocal
        return CognifyLocal(**kwargs)
    raise ValueError(f"unknown backend kind: {kind}")
