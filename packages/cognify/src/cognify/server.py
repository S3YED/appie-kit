"""
Cognify HTTP server — a tiny FastAPI app exposing the engine over HTTP, so any
agent runtime (Hermes, n8n, a shell, another service) can ingest and recall
without a Python import.

Run:  cognify-serve              (defaults to 127.0.0.1:8799)
Env:  COGNIFY_HOST, COGNIFY_PORT, COGNIFY_BACKEND, plus the usual LLM/Neo4j vars.

Endpoints:
  GET  /health
  POST /ingest   {text|path, tenant, namespace, agent, extract}
  POST /recall   {query, tenant, namespace, k}
  GET  /stats?tenant=
"""
from __future__ import annotations

import os

import cognify

try:
    from fastapi import FastAPI, HTTPException, Query
except ImportError as e:  # pragma: no cover
    raise SystemExit("FastAPI not installed. Run: pip install 'cognify-kg[serve]'") from e

app = FastAPI(title="Cognify", version=cognify.__version__)
_backend = None


def _be():
    global _backend
    if _backend is None:
        _backend = cognify.get_backend(os.environ.get("COGNIFY_BACKEND", "local"))
    return _backend


@app.get("/health")
def health():
    return {"status": "ok", "backend": os.environ.get("COGNIFY_BACKEND", "local"),
            "version": cognify.__version__}


@app.post("/ingest")
def ingest(body: dict):
    text = body.get("text") or body.get("path")
    if not text:
        raise HTTPException(400, "provide 'text' or 'path'")
    try:
        r = cognify.ingest(_be(), text, tenant=body.get("tenant", "default"),
                           namespace=body.get("namespace", "default"),
                           agent=body.get("agent", "agent"),
                           is_path=bool(body.get("path")),
                           do_extract=body.get("extract", True))
        return r.__dict__
    except Exception as e:
        raise HTTPException(500, f"ingest failed: {e}")


@app.post("/recall")
def recall(body: dict):
    q = body.get("query")
    if not q:
        raise HTTPException(400, "provide 'query'")
    try:
        res = cognify.recall(_be(), q, tenant=body.get("tenant", "default"),
                             namespace=body.get("namespace"), k=int(body.get("k", 8)))
        return {"query": res.query, "tenant": res.tenant, "chunks": list(res.chunks),
                "entities": list(res.entities), "relations": list(res.relations)}
    except Exception as e:
        raise HTTPException(500, f"recall failed: {e}")


@app.get("/stats")
def stats(tenant: str = Query(None)):
    return _be().stats(tenant=tenant)


def main():
    import uvicorn
    uvicorn.run(app, host=os.environ.get("COGNIFY_HOST", "127.0.0.1"),
                port=int(os.environ.get("COGNIFY_PORT", "8799")), log_level="info")


if __name__ == "__main__":
    main()
