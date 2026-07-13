---
name: notion
description: "Notion API via curl: pages, databases, blocks, search."
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Notion, Productivity, Notes, Database, API]
    homepage: https://developers.notion.com
prerequisites:
  env_vars: [NOTION_API_KEY]
---

# Notion API

Use the Notion API via curl to create, read, update pages, databases (data sources), and blocks. No extra tools needed — just curl and a Notion API key.

## Prerequisites

1. Create an integration at https://notion.so/my-integrations
2. Copy the API key (starts with `ntn_` or `secret_`)
3. Store it in `~/.hermes/.env`:
   ```
   NOTION_API_KEY=ntn_your_key_here
   ```
4. **Important:** Share target pages/databases with your integration in Notion (click "..." → "Connect to" → your integration name)

## API Basics

All requests use this pattern:

```bash
curl -s -X GET "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

The `Notion-Version` header is required. This skill uses `2025-09-03` (latest). In this version, databases are called "data sources" in the API.

## Common Operations

### Search

```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

### Get Page

```bash
curl -s "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### Get Page Content (blocks)

```bash
curl -s "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### Create Page in a Database

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "xxx"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Item"}}]},
      "Status": {"select": {"name": "Todo"}}
    }
  }'
```

### Query a Database

```bash
curl -s -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "Active"}},
    "sorts": [{"property": "Date", "direction": "descending"}]
  }'
```

### Create a Database

```bash
curl -s -X POST "https://api.notion.com/v1/data_sources" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "xxx"},
    "title": [{"text": {"content": "My Database"}}],
    "properties": {
      "Name": {"title": {}},
      "Status": {"select": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
      "Date": {"date": {}}
    }
  }'
```

### Update Page Properties

```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

### Add Content to a Page

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello from Hermes!"}}]}}
    ]
  }'
```

## Property Types

Common property formats for database items:

- **Title:** `{"title": [{"text": {"content": "..."}}]}`
- **Rich text:** `{"rich_text": [{"text": {"content": "..."}}]}`
- **Select:** `{"select": {"name": "Option"}}`
- **Multi-select:** `{"multi_select": [{"name": "A"}, {"name": "B"}]}`
- **Date:** `{"date": {"start": "2026-01-15", "end": "2026-01-16"}}`
- **Checkbox:** `{"checkbox": true}`
- **Number:** `{"number": 42}`
- **URL:** `{"url": "https://..."}`
- **Email:** `{"email": "user@example.com"}`
- **Relation:** `{"relation": [{"id": "page_id"}]}`

## Key Differences in API Version 2025-09-03

- **Databases → Data Sources:** Use `/data_sources/` endpoints for queries and retrieval
- **Two IDs:** Each database has both a `database_id` and a `data_source_id`
  - Use `database_id` when creating pages (`parent: {"database_id": "..."}`)
  - Use `data_source_id` when querying (`POST /v1/data_sources/{id}/query`)
- **Search results:** Databases return as `"object": "data_source"` with their `data_source_id`

## Notes

- Page/database IDs are UUIDs (with or without dashes)
Rate limit: ~3 requests/second average.
- **File uploads via API are capped at ~5MB.** For larger files, upload to Google Drive and link from the Notion page instead. Update existing link paragraphs; don't try to replace file blocks.
- The API cannot set database view filters — that's UI-only
- Use `is_inline: true` when creating data sources to embed them in pages
- Add `-s` flag to curl to suppress progress bars (cleaner output for Hermes)
- Pipe output through `jq` for readable JSON: `... | jq '.results[0].properties'`

## Page Visibility & Parent Selection (CRITICAL)

Pages created via the API are **NOT automatically shared** with workspace members. `public_url` is `null` by default. If the user says "can't see it", the parent page you chose is either inaccessible to them or the page wasn't shared.

### DB creation pitfall: 404 "Could not find page"

Even when a page appears in search results, the integration may not have **write** access to it (only read at workspace level). To create a database when no accessible parent page exists:

1. Create a temporary placeholder page in any database you CAN write to (test first)
2. Create the target database under that page: `parent: {page_id: placeholder_id}`
3. Archive the placeholder afterward

The placeholder page appears in the writable database as a side effect — archive it to clean up.

### Token resolution pitfall

When `NOTION_TOKEN="$NOTION...Y"` — the value is a reference to another env var, not the actual token. Source the env file and resolve `$`-prefixed values before using.

When creating a page for a user, you MUST use a parent page they can already see. The API cannot share pages — that's UI-only.

1. **Search first:** `POST /v1/search` with `{"filter": {"property": "object", "value": "page"}}`
2. **Filter by accessible:** Only use pages that HAVE a `url` field — pages without URLs are database entries the user can't navigate to directly
3. **Pick a known parent:** Use a page the user explicitly references (e.g., an existing project page), or one with a recognizable title
4. **Create under that parent:** Use its ID as `parent.page_id`

### After creating

- Return the workspace URL format (e.g., `https://weblyfe.notion.site/Page-Title-{id_without_dashes}`), NOT `app.notion.com`
- Verify with `GET /v1/pages/{id}` — 200 means the integration can see it
- If the user still can't see it, they need to: Notion Settings → Connections → find the integration → ensure workspace access → share parent page via `...` → `Connect to`

## API Key Masking in Hermes

Hermes masks API keys (`ntn_...`, `sk-...`) in terminal commands and write_file content. This silently corrupts:
- Bash: `Bearer $NOTION_API_KEY` → `Bearer ***` → 401 Unauthorized
- Python f-strings: `f"Bearer ***` → syntax error on write

**Workaround:** Use Python scripts with string concatenation (`"Bearer " + key`), read keys from `~/.hermes/.env` with `os.path.expanduser()`, and strip quotes from values. See `references/hermes-masking.md`.

## Scripts

- `scripts/create_page.py` — Create a Notion page from a markdown file, auto-discovering an accessible parent. Usage: `python3 scripts/create_page.py "Title" content.md [parent_id]`
