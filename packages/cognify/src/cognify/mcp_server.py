"""
Cognify MCP server — exposes ingest/recall/stats as MCP tools so Claude Code,
Claude Desktop, or any MCP client can build and query a knowledge graph directly.

Run:  cognify-mcp                 (stdio transport)
Add to Claude Code:
      claude mcp add cognify -- cognify-mcp
Add to Claude Desktop (claude_desktop_config.json):
      {"mcpServers": {"cognify": {"command": "cognify-mcp"}}}

Backend + LLM are configured via env (COGNIFY_BACKEND, ANTHROPIC_API_KEY or
OPENROUTER_API_KEY, etc) — see .env.example.
"""
from __future__ import annotations

import os

import cognify

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:  # pragma: no cover
    raise SystemExit("MCP SDK not installed. Run: pip install 'cognify-kg[claude]'") from e

mcp = FastMCP("cognify")
_backend = None


def _be():
    global _backend
    if _backend is None:
        _backend = cognify.get_backend(os.environ.get("COGNIFY_BACKEND", "local"))
    return _backend


@mcp.tool()
def cognify_ingest(text: str, tenant: str = "default", namespace: str = "default") -> dict:
    """Ingest a document (raw text or a file path) into the knowledge graph:
    chunk it, extract typed entities + relations, embed, and store. Returns counts."""
    r = cognify.ingest(_be(), text, tenant=tenant, namespace=namespace,
                       is_path=os.path.exists(text) if "\n" not in text else False)
    return r.__dict__


@mcp.tool()
def cognify_recall(query: str, tenant: str = "default", k: int = 8) -> dict:
    """Hybrid retrieval: find the most relevant chunks for the query, then expand
    the graph around them. Returns matching chunks plus the connected typed
    entities and relations — use these as grounded context to answer."""
    res = cognify.recall(_be(), query, tenant=tenant, k=k)
    return {
        "chunks": [{"score": c["score"], "heading": c.get("heading", ""), "text": c["text"]}
                   for c in res.chunks],
        "entities": [f"{e['name']} ({e['etype']})" for e in res.entities],
        "relations": [f"{r['subject']} -{r['predicate']}-> {r['object']}" for r in res.relations],
    }


@mcp.tool()
def cognify_stats(tenant: str = "default") -> dict:
    """Counts of documents, chunks, entities and relations for a tenant."""
    return _be().stats(tenant=tenant)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
