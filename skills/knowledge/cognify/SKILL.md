---
name: cognify
description: Interact with the Cognify shared-brain knowledge graph — recall contextual knowledge, ingest new content, and manage namespaces. Used by all fleet agents for cross-session memory sharing.
tags: [cognify, knowledge-graph, fleet, recall, ingest]
---

# Cognify — Fleet Shared Brain

Cognify is the fleet's shared knowledge graph (vector + entity store). It runs on Seyed's Mac Mini at `100.101.29.56:8765` (Tailscale-only, never exposed publicly). All Hermes agents (Appie-1, Appie-2, Spark Atlas) use it for cross-session and cross-agent memory.

## Endpoints

### Recall — Query Knowledge

```
POST http://100.101.29.56:8765/cognify/recall
Content-Type: application/json

{
  "query": "your search query",
  "tenant": "fleet",
  "k": 6           # number of chunks to return, default 3
}
```

Returns: `{ "chunks": [...], "entities": {...}, "relations": [...] }`

Always ground answers in returned chunks + entities + relations. Do not guess.

### Ingest — Add New Content

```
POST http://100.101.29.56:8765/cognify/ingest
Content-Type: application/json

{
  "source": "appie-1",               # REQUIRED — who is ingesting (field is "source" NOT "agent")
  "namespace": "workspace:appie-1",   # REQUIRED — namespace for organization
  "text": "...",                      # REQUIRED — the content (field is "text" NOT "content")
  "title": "optional title"           # OPTIONAL — overrides auto-title from first line
}
```

Response: `{ "doc_id": "...", "title": "...", "tenant": "fleet", "namespace": "...", "chunks": N, "entities": N, "relations": N, "extracted": true }`

**Critical details (verified by testing):**
- Field name is `"text"` — NOT `"content"` (older docs may be wrong)
- Field name is `"source"` — NOT `"agent"`
- Do NOT use `"path"` — that's for server-side file reading; our agents don't share a filesystem with the server
- Documents ~10KB need up to 120s timeout (entity extraction is compute-heavy)
- Returns chunk count, entity count, and relation count

## Python Patterns

### Ingest (preferred — handles long content)

```python
import json, urllib.request

with open(file_path) as f:
    text = f.read()

payload = {
    "source": "appie-1",
    "namespace": "workspace:appie-1",
    "text": text
}

data = json.dumps(payload).encode()
req = urllib.request.Request(
    "http://100.101.29.56:8765/cognify/ingest",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=120) as resp:
    result = json.loads(resp.read())
    print(f"Ingested: {result['chunks']} chunks, {result['entities']} entities, {result['relations']} relations")
```

### Recall

```python
import json, urllib.request

payload = {"query": "your search", "tenant": "fleet", "k": 6}
data = json.dumps(payload).encode()
req = urllib.request.Request(
    "http://100.101.29.56:8765/cognify/recall",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=30) as resp:
    results = json.loads(resp.read())
    # results["chunks"] — text chunks ranked by relevance
    # results["entities"] — named entities extracted
    # results["relations"] — relationships between entities
```

## Health Check

```
GET http://100.101.29.56:8765/health
```

Returns `{"status": "ok", "index_ready": true, "total_chunks": N, ...}`

## Key Differences From Earlier Documentation

| What old docs say | What actually works |
|-------------------|---------------------|
| `"agent"` field | `"source"` field |
| `"content"` field | `"text"` field |
| `"path"` field | Do not use (server can't read our local files) |
| Short timeout fine | 120s needed for 10KB+ documents |
| Shell curl escaping | Python avoids encoding issues |

## Notes

- Tailscale-only endpoint. Do not expose publicly.
- Namespace convention: `workspace:<agent-name>` (e.g. `workspace:appie-1`, `workspace:appie-2`).
- Tenant is always `"fleet"`.
- Entity extraction runs automatically on ingest — no separate call needed.