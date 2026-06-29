"""Backend factory."""
from __future__ import annotations

import os


def get_backend(kind: str | None = None):
    """kind: 'local' (ChromaDB+networkx, default) or 'neo4j' (TurboVec+Neo4j).
    Defaults to env COGNIFY_BACKEND, else 'local' (zero external services)."""
    kind = kind or os.environ.get("COGNIFY_BACKEND", "local")
    if kind == "local":
        from .local_backend import LocalBackend
        return LocalBackend()
    if kind == "neo4j":
        from .neo4j_backend import Neo4jBackend
        return Neo4jBackend()
    raise ValueError(f"unknown backend: {kind}")
