# Cognify — fleet ECL knowledge pipeline (our Cognee, on TurboVec + Neo4j)

Document ingestion + typed knowledge-graph construction for every Appie and every
client agent. Built on the stack we already run, with the one thing the giga-graph
was missing: **LLM-extracted typed entities and relations**, not just semantic
similarity edges.

## Pipeline (ECL)

```
ingest(doc) ->
  Extract : load file (md/txt/pdf) or raw text -> heading-aware ~512-tok chunks
  Cognify : per chunk, cheap LLM pulls typed Entities + typed Relations
  Load    : embed chunks (384d) -> vector store ; write graph -> graph store
recall(query) ->
  vector search (tenant-scoped) -> expand graph around hits -> chunks + subgraph
```

## Two backends, one API

| | Fleet (`neo4j`) | Client (`local`) |
|---|---|---|
| Vectors | TurboVec (per-tenant `.turbo`) | ChromaDB (ONNX MiniLM, no torch) |
| Graph | shared Neo4j on appie-2 (C-prefixed labels) | networkx per-tenant JSON |
| Use | all fleet agents | isolated Orgo client boxes |
| Isolation | `tenant` property on every node | separate store + tenant |

Same `all-MiniLM-L6-v2` 384d space on both sides, so retrieval behaves identically.

## Multi-tenancy

Every node carries `tenant` + `namespace`. Fleet uses `tenant="fleet"`. Each client
agent uses its own (e.g. `client:roslan`) and physically cannot see another tenant's
data: the local backend is a separate store on a separate box; the Neo4j backend
filters every query by tenant.

## Graph model (Neo4j, C-prefixed to not collide with the legacy giga-graph)

```
(:CDocument {id,tenant,namespace,agent,title,source,ts})
(:CChunk    {id,tenant,namespace,doc_id,ord,heading,text})
(:CEntity   {id,tenant,namespace,name,etype})
(:CChunk)-[:PART_OF]->(:CDocument)
(:CEntity)-[:MENTIONED_IN]->(:CChunk)
(:CEntity)-[:REL {type,doc_id}]->(:CEntity)
```

## Use

```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib:/opt/homebrew/lib   # Mac mini only
PY=/Users/appie/clawd/external/.venv-turbovec/bin/python
cd /Users/appie/clawd/tools/knowledge-api

# ingest a folder into the fleet graph
$PY -m cognify.cli --backend neo4j --tenant fleet --namespace company-kb \
    ingest-dir /Users/appie/clawd/knowledge --glob '**/*.md'

# hybrid recall
$PY -m cognify.cli recall "how does Clark provision boxes?" --tenant fleet

# client box (self-contained, no torch, no Neo4j)
$PY -m cognify.cli --backend local --tenant client:roslan ingest-dir ./docs
```

HTTP (knowledge-api on :8765): `POST /cognify/ingest`, `POST /cognify/recall`,
`GET /cognify/stats?tenant=`.

Python:
```python
import cognify
be = cognify.get_backend("neo4j")     # or "local"
cognify.ingest(be, "doc.pdf", tenant="fleet", namespace="research")
res = cognify.recall(be, "question?", tenant="fleet")
```

## Config (env)

| var | default | purpose |
|---|---|---|
| `COGNIFY_BACKEND` | `neo4j` | which backend the factory builds |
| `COGNIFY_LLM_BASE` | `https://openrouter.ai/api/v1` | extractor endpoint |
| `COGNIFY_LLM_MODEL` | `openai/gpt-4o-mini` | extractor model (cheapest competent) |
| `COGNIFY_LLM_KEY` / `OPENROUTER_API_KEY` | — | extractor key |
| `COGNIFY_LOCAL_DIR` | `~/.clark/cognify` | client store path |

Point `COGNIFY_LLM_BASE` at Spark Atlas (`http://100.69.197.43:8000/v1`) to run
extraction on free local Qwen when it is up.

## Self-improvement

`tools/cognify-refresh.sh` re-ingests new/changed company-KB docs and is wired into
the fleet skill-sync + memory-sync so the graph keeps growing as fleet knowledge
grows. The client variant ships inside the golden Orgo box build.
