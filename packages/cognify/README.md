# Cognify

A lightweight document-ingestion and **typed knowledge-graph** engine you can
hand to an agent. Drop in raw documents, get back a queryable graph of typed
entities and relations plus hybrid (vector + graph) retrieval.

Two interchangeable backends behind one API:

| backend | vectors | graph | needs | use |
|---|---|---|---|---|
| `local` (default) | ChromaDB (ONNX MiniLM) | networkx | nothing external, no torch | drop into an agent box |
| `neo4j` | TurboVec | Neo4j | a Neo4j instance | shared/server graph |

Same 384d embedding space on both, so retrieval behaves identically.

## Why not plain RAG

Plain RAG embeds chunks and does similarity search. Cognify also asks a cheap LLM
to extract **typed entities** (Person, Project, Technology, ...) and **typed
relations** (`USES`, `WORKS_AT`, `BUILT`, ...) from every chunk, builds a graph,
and expands that graph around your search hits. You get the facts *and* how they
connect, which is what makes multi-hop questions work.

## How it compares

| | Cognify | Cognee | Mem0 | Graphiti / Zep | LightRAG | plain RAG |
|---|---|---|---|---|---|---|
| Typed entity+relation graph | ✅ | ✅ | partial (dropped graph) | ✅ (temporal) | ✅ | ❌ |
| Runs with **zero external services** | ✅ (ChromaDB+networkx) | ❌ (Kuzu file-lock; Neo4j for multi-agent) | ❌ (hosted/Qdrant) | ❌ (Neo4j) | ⚠️ | ✅ |
| Torch-free local install | ✅ (ONNX embedder) | ❌ | ❌ | ❌ | ❌ | varies |
| Same API, swap local ↔ server | ✅ | ⚠️ | ❌ | ❌ | ❌ | n/a |
| Built-in multi-tenancy | ✅ (every node) | ⚠️ | ✅ | ✅ | ❌ | ❌ |
| MCP server for Claude | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Lines of core code | ~1k, readable | large | large | large | medium | tiny |
| Reconstruction spec for agents | ✅ `BLUEPRINT.md` | ❌ | ❌ | ❌ | ❌ | ❌ |

**Where each wins, honestly.** Graphiti/Zep is the choice if you need temporal
fact-tracking and SOC2/HIPAA compliance. Cognee has more managed connectors and a
cloud tier. Mem0 is simplest for pure conversational memory. **Cognify wins when
you want a real typed graph that an agent can run anywhere — a laptop, an
isolated box, or a shared server — with one dependency-light install, one API
across backends, and code small enough to read in a sitting.** It is the
embed-it-in-your-agent option, not the managed-platform option.

## Why it's so lightweight

- **Default backend needs nothing external** — ChromaDB (embedded) + a networkx
  graph in a JSON file. No database server, no Docker, no cloud.
- **No PyTorch** — embeddings come from ChromaDB's bundled ONNX MiniLM. The whole
  default install is small and CPU-only.
- **The LLM is the only heavy lift, and it's remote** — entity/relation extraction
  is one cheap API call per chunk; nothing large runs locally.
- **~1k lines of pure-function code**, src layout, one file per concern. The
  backend protocol is four methods; adding a store is one file.
- **Scales by swapping a backend, not rewriting** — move to TurboVec + Neo4j for a
  shared graph by changing one env var; the same embeddings and API carry over.

## Pipeline (ECL)

```
ingest(doc) ->  Extract: file/text -> heading-aware ~512-token chunks
                Cognify: per chunk, cheap LLM -> typed entities + relations
                Load:    embed chunks (384d) -> vectors ; write graph
recall(q)   ->  vector search (tenant-scoped) -> expand graph -> chunks + subgraph
```

## Quickstart

```bash
./setup.sh local            # venv + deps + .env
source .venv/bin/activate
echo 'OPENROUTER_API_KEY=sk-or-...' >> .env
set -a && . ./.env && set +a

cognify ingest examples/sample_docs/acme.md --tenant demo
cognify recall "what does Pathfinder run on and who owns it?" --tenant demo
cognify stats --tenant demo
```

Python:

```python
import cognify
be = cognify.get_backend("local")
cognify.ingest(be, "handbook.pdf", tenant="acme", namespace="hr")
res = cognify.recall(be, "who owns onboarding?", tenant="acme")
print(res.entities, res.relations)
```

## Use with Claude

**Claude as the extractor** — just set the key (auto-detected):
```bash
pip install 'cognify-kg[local]'
export ANTHROPIC_API_KEY=sk-ant-...
cognify ingest notes.md --tenant demo && cognify recall "what connects to X?" --tenant demo
```

**Cognify as MCP tools** in Claude Code / Desktop:
```bash
pip install 'cognify-kg[local,claude]'
claude mcp add cognify -- cognify-mcp
```
Claude then has `cognify_ingest`, `cognify_recall`, `cognify_stats`. Details in
`integrations/claude/`.

## Use with Hermes (and any agent runtime)

The `cognify` CLI works as-is — a Hermes agent shells out to it. Drop
`integrations/hermes/SKILL.md` into the agent's skills. Or run the HTTP server for
a shared/long-running graph:
```bash
pip install 'cognify-kg[serve]'
cognify-serve                      # 127.0.0.1:8799
curl -s localhost:8799/recall -d '{"query":"refund policy?","tenant":"acme"}' -H 'content-type: application/json'
```

## Multi-tenancy

Every node carries a `tenant` (and `namespace`). Pass a different `tenant` per
client/agent and their data stays isolated: the `local` backend is a separate
store, the `neo4j` backend filters every query by tenant. This is what makes it
safe to run one engine across many agents.

## Recommended models (extraction)

Extraction is one cheap LLM call per chunk; pick by cost vs throughput. Numbers
below are from a real single-chunk extraction test, not vendor specs.

| Model | Via | Cost (rough) | Notes |
|---|---|---|---|
| **`openai/gpt-4o-mini`** | OpenRouter / OpenAI | ~$0.15/$0.60 per M | **Recommended default.** Fast (~6s/chunk), reliable JSON. A 40-doc KB cost ~$0.20. |
| `google/gemini-2.0-flash` | OpenRouter / Google | ~$0.10/$0.40 per M | Cheapest solid cloud option; big context. Google free tier rate-limits (429) — use a paid key for bulk. |
| `deepseek/deepseek-chat` | OpenRouter | ~$0.14/$0.28 per M | Same quality as gpt-4o-mini but ~3× slower (~17s/chunk). Fine for small batches. |
| local **Qwen / Llama 3.3 / Gemma** | Ollama / vLLM | free | The real free path for bulk. Run on your own GPU; point `COGNIFY_LLM_BASE` at it. |
| Claude Haiku | Anthropic (native) | cheap | Set `ANTHROPIC_API_KEY`; auto-detected. Highest extraction quality of the cheap tier. |

Avoid OpenRouter's **`:free`** model variants for bulk — they are heavily
rate-limited (429) or very slow (one free model measured ~77s/chunk). Free is
only practical on local inference.

Switch model with one env var, e.g. local Ollama:
```bash
export COGNIFY_LLM_BASE=http://localhost:11434/v1
export COGNIFY_LLM_MODEL=qwen2.5:14b
export COGNIFY_LLM_KEY=ollama        # any non-empty string
```

## Configuration

All via env (see `.env.example`): `COGNIFY_BACKEND`, `COGNIFY_DATA_DIR`,
`COGNIFY_LLM_BASE/MODEL/KEY`, `COGNIFY_LLM_PROVIDER`, `NEO4J_URI/USER/PASSWORD`.
The LLM endpoint is OpenAI-compatible (OpenRouter, OpenAI, vLLM, Ollama) or native
Anthropic (Claude). See the model table above.

## For agents

`CLAUDE.md` is the operating guide. `ARCHITECTURE.md` explains the design.
`BLUEPRINT.md` is a from-scratch reconstruction spec: hand this repo to an agent
and it can rebuild or extend the whole thing.

MIT licensed.
