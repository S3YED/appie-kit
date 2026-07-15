---
name: cognify-memory
description: Durable client memory for KRATOS via Cognify (isolated local knowledge graph). Ingest documents and recall facts about Ibrahim Ramzy and his business with typed entities + relations. ALWAYS query this before answering recall questions about the client. Local backend only, tenant=ramzy, fully isolated (no shared/fleet endpoints).
---

# Cognify memory (isolated, client-only)

Cognify install: /root/cognify  (own .venv, local ChromaDB backend, data at /root/.cognify)
Tenant: **ramzy**  (canonical). Legacy tenant `ibrahim` holds earlier ingested data.
Isolation: COGNIFY_BACKEND=local, no Neo4j/TurboVec, no fleet endpoints. Client memory NEVER leaves this box.

## Recall (do this before answering client/business questions)
```bash
cd /root/cognify && set -a && . ./.env && set +a && export COGNIFY_DATA_DIR=/root/.cognify
./.venv/bin/cognify --tenant ramzy recall "<question>"
```

## Ingest a new fact/document
```bash
cd /root/cognify && set -a && . ./.env && set +a && export COGNIFY_DATA_DIR=/root/.cognify
./.venv/bin/cognify --tenant ramzy ingest /path/to/file.txt
```

## Stats
```bash
cd /root/cognify && ./.venv/bin/cognify --tenant ramzy stats
```