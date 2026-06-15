# knowledge-pipeline Skill

## Purpose

Operate the local-first Weblyfe knowledge pipeline: ingest documents and Google Drive / Notion content, embed locally, search by meaning, and surface it as a 3D graph in Mission Control. Built 2026-06-03. Codifies the patterns so future sessions and fleet agents do not re-derive them.

## Where it lives

`~/clawd/projects/knowledge-pipeline/`. Store at `.data/knowledge.db` (SQLite, gitignored). Drive cache `.data/drive-cache/`, Notion cache `.data/notion-cache/`.

## Core principle (from the adversarial review)

Local-first is REAL: SQLite + local embeddings are canonical. Pinecone is a deferred optional sync target, never the critical path. No client data is embedded until per-tenant isolation is hard. `tenant` is fail-closed (NOT NULL, scoped search never returns another tenant or UNASSIGNED).

## Quick reference

| Task | Command |
|------|---------|
| Ingest a local folder | `python3 ingest.py <dir> --tenant weblyfe-internal` |
| Search | `python3 query.py "your question" --tenant weblyfe-internal -k 5` |
| Sync a Google Drive folder | `python3 sync_drive.py <driveFolderId>` then ingest `.data/drive-cache/<id>` |
| Export Notion (streaming) | `NOTION_API_KEY=... python3 -u sync_notion.py` then ingest `.data/notion-cache --tenant notion` |

## Stack

- Embeddings: local Ollama `bge-m3` (1024-dim). `ollama pull bge-m3`. Helper `kp/embed.py` hits `localhost:11434/api/embed`. Nothing leaves the machine.
- Store: SQLite + brute-force numpy cosine (`kp/store.py`). Corpus is small (tens of thousands of chunks) so this is fast and avoids fragile native installs on Python 3.14. sqlite-vec / Chroma is the upgrade path.
- Parse: PyMuPDF (fitz, preinstalled) for PDF, plain read for md/txt (`kp/parse.py`). `iter_files` skips node_modules/.git/.next/etc.
- Incremental: files are skipped by md5 on re-run.

## Gotchas

- Python 3.14 (`/opt/homebrew/bin/python3`) has a broken pyexpat for native builds; chromadb/sentence-transformers installs are fragile. Stick to ollama + SQLite + numpy.
- Notion `/v1/search` returns thousands of page objects for a large workspace. Stream (write per page) instead of collecting all first, or it appears to hang.
- Notion rate limit is ~3 req/s; keep a 0.34s pause per request.
- nohup buffers stdout; use `python3 -u` for live progress.

## Mission Control integration

The 3D graph lives at MC `Memory > Graph` (reagraph WebGL, already installed). `src/app/api/memory/graph/route.ts` surfaces the pipeline DB as a `knowledge` cluster (GROUP BY path, cap 350 nodes). The Graph tab was gated `!isLocal`; unlocked in local mode in `memory-browser-panel.tsx`. Override the DB path with env `KNOWLEDGE_DB_PATH`.

## Next phases (not built)

Per-tenant namespaces then client folders; FastAPI read-only for MC; audio (faster-whisper) + OCR ingest; entity/relation knowledge graph behind a flag; Pinecone remote sync; clustering/analysis; Obsidian export; voice "ask the KB".
