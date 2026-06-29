"""
Cognify — a lightweight document-ingestion + typed knowledge-graph engine.

Quickstart:
    import cognify
    be = cognify.get_backend("local")          # zero external services
    cognify.ingest(be, "notes.md", tenant="me")
    res = cognify.recall(be, "what uses Neo4j?", tenant="me")
    print(res.entities, res.relations)
"""
from .core import ingest, recall, embed, get_model, IngestResult, RecallResult  # noqa: F401
from .backends import get_backend  # noqa: F401

__version__ = "0.1.0"
