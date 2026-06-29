---
name: cognify
description: Use when you need durable memory over documents — ingest files/notes into a typed knowledge graph and recall facts with their relationships. Build a knowledge base from PDFs, markdown, or pasted text, then ask grounded questions.
---

# Cognify (Hermes skill)

Give yourself a knowledge graph. `ingest` documents, `recall` facts plus how they
connect. Backed by ChromaDB + networkx locally (no external services), or
TurboVec + Neo4j for a shared graph.

## Setup (once per box)

```bash
pip install 'cognify-kg[local]'          # or [claude] to also use Claude as extractor
export ANTHROPIC_API_KEY=...             # Claude extractor (auto-detected)
# or: export OPENROUTER_API_KEY=...      # any OpenAI-compatible model
export COGNIFY_DATA_DIR="$HOME/.cognify" # where the graph lives
```

## Use it from the shell (simplest)

```bash
# ingest a file, a folder, or piped text — pick a tenant to isolate this agent's data
cognify ingest /path/to/handbook.pdf --tenant myagent --namespace docs
cognify ingest-dir ~/notes --glob '**/*.md' --tenant myagent --cache
echo "free text to remember" | cognify ingest - --tenant myagent

# recall: returns chunks + connected entities/relations as grounded context
cognify recall "who owns onboarding and what tool do they use?" --tenant myagent
cognify stats --tenant myagent
```

Parse the JSON from `recall` and use the `entities`/`relations`/`chunks` as
context for your answer.

## Use it over HTTP (for a shared graph or a long-running agent)

```bash
cognify-serve &      # 127.0.0.1:8799  (set COGNIFY_BACKEND=neo4j for a shared graph)
curl -s localhost:8799/ingest -d '{"path":"/docs/policy.md","tenant":"myagent"}' -H 'content-type: application/json'
curl -s localhost:8799/recall -d '{"query":"refund policy?","tenant":"myagent"}' -H 'content-type: application/json'
```

## Rules

- Always pass a stable `--tenant` for this agent so your memory stays isolated
  from other agents on the box.
- Ingesting calls the LLM once per chunk (cost). Use `--cache` on `ingest-dir` so
  re-runs skip unchanged files.
- For a fleet-shared graph use `COGNIFY_BACKEND=neo4j` with `NEO4J_*` set; for a
  private per-box graph use the default `local` backend.
