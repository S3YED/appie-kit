---
name: webflow-cms-access
description: Access Webflow CMS collections, find API tokens, and update CMS items for Weblyfe agency client sites.
version: 1.0.0
author: Appie
license: MIT
platforms: [macos, linux]
prerequisites:
  env_vars: []
metadata:
  hermes:
    tags: [webflow, cms, api, weblyfe, content]
---

# Webflow CMS Access

Access and manage Webflow CMS collections for Weblyfe client sites via the Webflow API v2.

## Finding the right API token

Weblyfe has multiple Webflow client sites, each with its own API token. Tokens live in `~/clawd/.env.secrets` but follow inconsistent naming.

### Token naming convention across sites

Sites and their known env var names (check .env.secrets for current values):

| Site | Env var | Notes |
|------|---------|-------|
| General / Workspace | `WEBFLOW_TOKEN`, `WEBFLOW_API_TOKEN` | Usually 401/unauthorized for specific sites |
| Weblyfe | `WEBFLOW_WEBLYFE_TOKEN` | site_id: `615bd59fd9d3edeb08fd3ea9` |
| Baliwithflow | `WEBFLOW_BALIWITHFLOW_TOKEN` | |
| Berend Strik | `WEBFLOW_BEREND_STRIK_TOKEN` | |
| Peakspring | `WEBFLOW_PEAKSPRING_API_KEY` | |
| Dubai Property | `WEBFLOW_DUBAI_PROPERTY_TOKEN` | |
| Mo Ecom | `WEBFLOW_MO_ECOM_TOKEN` | |
| Vrijheid Vastgoed | `WEBFLOW_VRIJHEID_VASTGOED_TOKEN` | site_id: `66df0e0a697bacd7438ba1a6` — Often NOT SET; ask user to share if missing |

### When a token is missing

1. First, check Notion for the project page — search "Vrijheid Vastgoed" or whatever the client name is
2. Check if there's a Notion page about Webflow token rotation (titled "Webflow: roteer dode tokens")
3. Ask the user to share the API key directly
4. Do NOT assume a generic/workspace token will work — Webflow API tokens are site-scoped

## Loading env secrets properly

The secrets file `~/clawd/.env.secrets` does NOT use `export` statements. To load into env:

```bash
# Wrong — vars won't be exported:
source ~/clawd/.env.secrets

# Right — auto-export:
set -a && source ~/clawd/.env.secrets && set +a
```

Or read values directly with grep/python.

## Finding a site ID

Every Webflow site publishes its site ID in a `data-wf-site` attribute on the live site's HTML:

```javascript
// In browser console:
document.querySelector('[data-wf-site]')?.getAttribute('data-wf-site')
```

## Webflow API v2 basics

Base URL: `https://api.webflow.com/v2`

Common endpoints:
- `GET /sites/{site_id}` — site info
- `GET /sites/{site_id}/collections` — list CMS collections (returns collection IDs)
- `GET /collections/{collection_id}/items` — list all CMS items in a collection
- `GET /collections/{collection_id}/items/{item_id}` — get single CMS item
- `PATCH /collections/{collection_id}/items/{item_id}` — update CMS item
- `POST /collections/{collection_id}/items` — create CMS item

All requests need header:
- `Authorization: Bearer {token}`
- `accept-version: 1.0.0`

## Webflow Designer access

The Webflow designer is at `https://webflow.com/design/{site-slug}`. The site slug is NOT the domain — you may need to:
1. Log into Webflow through the browser (subject to bot detection)
2. Find the slug from API metadata (not directly available via API v2 publicly)

**Note:** Webflow has aggressive bot detection on login/designer pages. Prefer API access over browser-based designer access.

## 1Password integration

The `op` CLI may be installed but not configured with accounts. Check:

```bash
op vault list  # returns 'No accounts configured' if not set up
```

If the 1Password desktop app is not running, service account needs to be configured. Ask the user if service account credentials are available.

## Pitfalls

- **Token naming is inconsistent** across the Weblyfe fleet — always search broadly in .env.secrets
- **The general WEBFLOW_TOKEN is a workspace-level token** that returns 401 for individual site operations
- **Bot detection on webflow.com** — avoid browser-based designer access if possible
- **env.secrets has no `export`** — use `set -a` trick or read with python/grep
- **API keys expire or can be rotated** — if a token returns 401, it may have been rotated since it was stored
- **Notion project pages** are the best source for project metadata (URLs, links, credentials), but don't always contain the actual API tokens