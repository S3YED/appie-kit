# Cognify — agent operating guide

You are working in **Cognify**, a document-ingestion + typed knowledge-graph
engine. Read this before changing anything.

## What it is

`ingest(document)` → chunks → cheap-LLM typed entity/relation extraction → embed +
write to a graph. `recall(query)` → vector search → expand the graph around the
hits. Two backends (`local` = ChromaDB+networkx, `neo4j` = TurboVec+Neo4j) behind
one API in `core.py`.

## Layout

```
src/cognify/
  config.py            env-driven paths/creds/model — the ONLY place machine
                       specifics live. No hardcoded paths or secrets anywhere else.
  loader.py            file/text -> heading-aware chunks (md/txt/pdf)
  extractor.py         LLM -> typed Extraction(entities, relations); OpenAI-compatible
  core.py              ECL orchestration + embedder + Backend protocol
  backends/
    local_backend.py   ChromaDB + networkx (torch-free, self-contained)
    neo4j_backend.py   TurboVec + Neo4j (shared/server)
    __init__.py        get_backend() factory
  cli.py               ingest / ingest-dir / recall / stats
  mcp_server.py        MCP tools for Claude Code/Desktop  (cognify-mcp)
  server.py            FastAPI HTTP server for Hermes/etc  (cognify-serve)
integrations/claude/   Claude extractor + MCP setup
integrations/hermes/   Hermes SKILL.md
examples/  tests/  setup.sh  pyproject.toml  .env.example
```

## Setup & run

```bash
./setup.sh local                      # or: neo4j / all
source .venv/bin/activate && set -a && . ./.env && set +a
cognify ingest <path|-> --tenant T    # ingest a file or stdin
cognify recall "<q>" --tenant T       # hybrid retrieval
pytest -q                             # smoke tests (e2e skips without an LLM key)
```

On Homebrew macOS, `config.py` auto-sets `DYLD_LIBRARY_PATH` to brew's expat so
`pypdf`/`chromadb` import. Elsewhere this is a no-op.

## Rules of the codebase

- **Immutable data**: dataclasses are `frozen=True`; functions return new values.
- **Backend symmetry**: any method added to one backend must exist on the other
  with identical semantics. `core.py` must never import a concrete backend.
- **All config through `config.py`** — never hardcode a path, model, or key.
- **Degrade, don't crash**: extraction failures fall back to chunks-only; log it.
- **Tenancy is non-negotiable**: every node carries `tenant`; every query filters
  by it. Never return another tenant's data.
- **Keep it lightweight**: the `local` backend must stay torch-free (ChromaDB ONNX
  embedder). Don't add heavy deps to the default path.

## Common extensions (and where)

- New file type → `loader.read_file()`.
- Different LLM/endpoint → env only (`COGNIFY_LLM_*`), no code change.
- New vector/graph store → new file in `backends/`, register in `backends/__init__.py`,
  implement the four `Backend` methods (+ optional `embed_texts`).
- Richer retrieval (multi-hop, rerank) → `core.recall()` and `backend.expand()`.

If you need to rebuild from scratch, follow `BLUEPRINT.md`.
