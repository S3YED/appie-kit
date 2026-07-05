---
name: drive-knowledge-ingestion
description: >-
  Drie-fase knowledge pipeline: Drive scanning → document text extraction
  → SQLite FTS5 knowledge base → entity extraction (heuristics) →
  knowledge graph → Neo4j export → realtime dashboard.
  Disk-safe: media wordt alleen metadata, documenten download naar temp en
  verwijderen direct. Ontworpen voor 8GB+ constraints.
---

# Knowledge Base Engineering — Full Pipeline

Class-level umbrella for ingesting, indexing, enriching, and visualizing
knowledge from Google Drive. Three stages: **Extract** → **Index** →
**Enrich & Visualize**.

## When to load

- User says "scan my entire Drive" or "build a knowledge base"
- User asks for a dashboard of Drive/business data
- You need to understand a client's full document landscape
- User says "build an entity graph" or "prepare for Neo4j"

## Triggers not to load

- Quick one-off file lookup (use google-workspace instead)
- Sending email or calendar ops (use google-workspace)

---

## Stage 1: Drive Scanning & Document Extraction

### Full recursive scan

Use `gog drive ls --all` with pagination to list every file in the Drive:

```bash
gog drive ls --json --all --max 1000 --client <client>
# Check nextPageToken, paginate if present
```

Rebuild folder hierarchy from the `parents` field:
```python
parent_map = {}
for f in all_files:
    for p in f.get('parents', []):
        parent_map.setdefault(p, []).append(f)
```

### Type breakdown

```python
from collections import Counter
types = Counter()
for f in all_files:
    mt = f['mimeType']
    if 'folder' in mt: types['folder'] += 1
    elif 'video' in mt or 'quicktime' in mt: types['video'] += 1
    elif any(x in mt for x in ['image','jpeg','png','heic','arw']): types['image'] += 1
    elif 'document' in mt or 'wordprocessing' in mt: types['document'] += 1
    elif 'pdf' in mt: types['pdf'] += 1
    elif 'presentation' in mt or 'slides' in mt: types['presentation'] += 1
    elif 'spreadsheet' in mt or 'sheet' in mt: types['spreadsheet'] += 1
    elif 'audio' in mt: types['audio'] += 1
    else: types['other'] += 1
```

### Document text extraction

Use `gog drive download --format <fmt>` to export Google-native docs:

| Google type | Export format | Tool |
|---|---|---|
| Google Doc | `txt` | `gog drive download --format txt` |
| Google Slides | `pptx` | `gog drive download --format pptx` |
| Google Sheets | `csv` | `gog drive download --format csv` |
| PDFs (native) | — | `gog drive download` → `pdftotext` |

**Disk management:** download to temp, extract text, delete temp immediately.
Never store media files (video/audio/images >500KB) locally.

---

## Stage 2: SQLite Knowledge Base

### Schema

```sql
CREATE TABLE files (
    id TEXT PRIMARY KEY,
    name TEXT, mime_type TEXT, size INTEGER,
    modified TEXT, parents TEXT, web_link TEXT, category TEXT,
    ingested INTEGER DEFAULT 0, ingested_at TEXT
);
CREATE TABLE documents (
    id TEXT PRIMARY KEY, file_id TEXT,
    content TEXT, word_count INTEGER, char_count INTEGER, summary TEXT
);
CREATE VIRTUAL TABLE docs_fts USING fts5(content, content='documents', content_rowid='rowid');
CREATE TABLE document_tags (id INTEGER PRIMARY KEY, file_id TEXT, tag TEXT);
```

### FTS5 Search

```sql
-- Full-text search across all document text
SELECT f.name, snippet(docs_fts, -1, '**', '**', '...', 32)
FROM docs_fts JOIN files f ON f.id = docs_fts.file_id
WHERE docs_fts MATCH 'search query';
```

### Scripts

- **`scripts/knowledge-ingest.py`** — `/root/.hermes/tools/knowledge-ingest.py`
  Runs Stage 1 + 2. Idempotent (skips already-processed files).
- **Cron job:** `drive-kennisbank-update` (weekly auto-refresh)

---

## Stage 3: Entity Extraction & Knowledge Graph

### Heuristics-based approach (no LLM needed)

Uses regex + known-person lists + keyword patterns instead of LLM calls.
This is **disk-safe, free, and fast** — suitable for 5,000+ file Drives.

**Entity types:** person, project, company, location

**Person matching:** regex for capitalized names + a KNOWN_PEOPLE list.
**Project matching:** regex for known brand/project names.
**Location matching:** known locations from the client's context.
**Topics:** keyword-based classification (coaching, finance, legal, marketing, etc.)

### Graph schema (SQLite)

```sql
CREATE TABLE entities (
    id INTEGER PRIMARY KEY, name TEXT, entity_type TEXT,
    mention_count INTEGER DEFAULT 1, first_seen TEXT
);
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    source_entity_id INTEGER, target_entity_id INTEGER,
    relationship_type TEXT, document_id TEXT, confidence REAL
);
```

### Neo4j export

Export entities + relationships as CSV + Cypher script:

```bash
# Produces in /root/.hermes/neo4j-export/:
#   entities.csv  — nodes
#   documents.csv — document nodes
#   relationships.csv — edges
#   import.cypher — run against Neo4j
```

### Scripts

- **`scripts/entity-pipeline.py`** — `/root/.hermes/tools/entity-pipeline.py`
  Runs Stage 3. Heuristics-only, no API calls.
- **Neo4j export:** auto-generated at `/root/.hermes/neo4j-export/`

---

## Stage 4: Dashboard

### Architecture

```
data collector (cron 30m) → dashboard-data.json → HTTP server → HTML + Chart.js
                                                         → Vercel (static deploy)
```

**Data collector:** `/root/.hermes/tools/dashboard-collector.py`
Gathers: Drive stats, system health, session activity, skills, GitHub PRs.

**Dashboard HTML:** `/root/.hermes/dashboard.html`
Single-page app, dark mode, Chart.js visualizations.

**Server:** `/root/.hermes/tools/dashboard-server.py [port]`
Serves HTML + JSON API endpoint at `/data`.

**Cron:** `dashboard-data-refresh` (every 30 min) — runs collector, copies data.json to
Vercel project dir, and auto-deploys via `vercel deploy --prod --yes`.

### Branding the dashboard

Every dashboard should carry the client's own visual identity. The workflow:

1. **Find brand assets** in Google Drive (search for logos, brand guidelines files)
2. **Extract brand colors** from SVG logos — download via gog, read `fill` attributes for exact hex
3. **Inline the logo SVG** directly in HTML (no external loads, no CORS)
4. **Build a CSS custom-property token system** (primary, secondary, accent, greys)
5. **Design deliberately** — use the client's existing visual language, not generic dark-mode
6. **Dual-mode fetch** so HTML works both locally and on Vercel:
   ```js
   let res = await fetch('/data').catch(() => fetch('data.json'));
   ```
7. **Auto-refresh pipeline**: cron → collector → copy → vercel deploy

See `references/dashboard-branding-guide.md` for the full step-by-step.

### Vercel deployment

The static dashboard + data.json can be deployed to Vercel:
`vercel deploy --prod --yes` from the project dir.
See `references/dashboard-vercel-deployment.md` for the full workflow.

Cron job `dashboard-data-refresh` should copy both the HTML and data.json to the Vercel
project directory before deploying, so branding changes propagate automatically.

---

## Disk-Safe Design Principles (8GB constraint)

| Rule | Why |
|---|---|
| Never store media locally | Video (2.5K files) + images (1.8K) = 500+ GB in Drive |
| Download docs to /tmp, extract, delete | Each doc is <1MB, temp footprint stays under 50MB |
| SQLite instead of heavy vector DB | FTS5 fits in 2MB vs ChromaDB+Torch = 2GB+ |
| Heuristics over LLM for entity extraction | 0 API cost, 0 disk, 0 latency per file |
| Single-page HTML dashboard | No build step, no node_modules, no framework |

## References

- `references/drive-research-workflow.md` — Systematic Drive exploration steps
  (in google-workspace skill, shared reference)
- `references/entity-extraction-methodology.md` — Known person lists,
  keyword maps, and extraction patterns for this client's ecosystem

## Related skills

- `google-workspace` — Raw Drive/Gmail/Calendar CLI ops (pre-pipeline)
- `srt-subtitles` — Parsing .srt subtitle files from Drive