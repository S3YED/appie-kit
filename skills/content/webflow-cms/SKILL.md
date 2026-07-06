---
name: webflow-cms
description: "Access, read, and update Webflow CMS collections — FAQs, pages, posts, and other content collections. Covers site discovery, authentication, collection queries, item CRUD, and publishing."
version: 1.0.0
author: appie
license: MIT
platforms: [macos]
prerequisites:
  env_vars: [WEBFLOW_API_TOKEN]
metadata:
  hermes:
    tags: [webflow, cms, collections, faq, content]
---

# Webflow CMS Operations

Use when working with Webflow CMS collections: reading/updating FAQs, pages, blog posts, or any CMS-driven content. NOT for site structure/design changes (use the Webflow Designer for that).

## Setup

### Authentication

Webflow API v2 uses a **Site Access Token** (site-scoped) or a **Personal Access Token** (account-scoped).

```bash
export WEBFLOW_API_TOKEN="your_token_here"
```

Store tokens in `~/.hermes/.env` or `~/clawd/.env.secrets`:
```
WEBFLOW_SITENAME_TOKEN=xxx
```

Convention: `WEBFLOW_{PROJECT_NAME}_TOKEN` in all-caps with underscores.

### Finding the Site ID

Every Webflow site has a unique ID embedded in the live HTML:

```javascript
document.querySelector('[data-wf-site]')?.getAttribute('data-wf-site')
```

Run this in the browser console on the live site, or look for it in the page source (`<html data-wf-site="...">`).

## Discovery Flow

When you don't know the site ID or token:

1. **Open the live site** in a browser
2. **Extract site ID** from `<html data-wf-site="...">` via browser console
3. **Search credentials** in:
   - `~/.hermes/.env` — Hermes env vars
   - `~/clawd/.env.secrets` — project secrets
   - 1Password vault (via `op` CLI)
   - Notion project pages (search for "Webflow" or "token")
4. If no token found → ask the user or client

## Common Operations

All examples use the Webflow API v2 at `https://api.webflow.com/v2/`.

### List all collections for a site

```bash
curl -s "https://api.webflow.com/v2/sites/${SITE_ID}/collections" \
  -H "Authorization: Bearer ${WEBFLOW_API_TOKEN}"
```

### Get collection items

```bash
curl -s "https://api.webflow.com/v2/collections/${COLLECTION_ID}/items?limit=100" \
  -H "Authorization: Bearer ${WEBFLOW_API_TOKEN}"
```

### Get a specific item

```bash
curl -s "https://api.webflow.com/v2/collections/${COLLECTION_ID}/items/${ITEM_ID}" \
  -H "Authorization: Bearer ${WEBFLOW_API_TOKEN}"
```

### Update a CMS item (PATCH)

```bash
curl -s -X PATCH "https://api.webflow.com/v2/collections/${COLLECTION_ID}/items/${ITEM_ID}" \
  -H "Authorization: Bearer ${WEBFLOW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"fieldData": {"field-slug": "new value"}}'
```

### Update FAQ/Q&A items

FAQ collections typically have `question` and `answer` fields (or localised variants like `question-nl`, `answer-nl`).

```bash
curl -s -X PATCH "https://api.webflow.com/v2/collections/${COLLECTION_ID}/items/${ITEM_ID}" \
  -H "Authorization: Bearer ${WEBFLOW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"fieldData": {"question": "Updated question?", "answer": "Updated answer."}}'
```

### Publish the site

Changes to CMS items are NOT live until you publish:

```bash
curl -s -X POST "https://api.webflow.com/v2/sites/${SITE_ID}/publish" \
  -H "Authorization: Bearer ${WEBFLOW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{}'
```

To publish specific collections (optional, publishes all by default):

```bash
curl -s -X POST "https://api.webflow.com/v2/sites/${SITE_ID}/publish" \
  -H "Authorization: Bearer ${WEBFLOW_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"collectionIds": ["collection_id_1", "collection_id_2"]}'
```

## Pitfalls

- **Tokens are site-scoped.** A token for one site won't work for another. Each project needs its own env var.
- **Changes aren't live until you publish.** PATCH updates the CMS but the published site won't reflect them until you call the publish endpoint.
- **Field names in v2 use kebab-case** (e.g., `question-nl`, `cover-image`), not camelCase. Check the collection schema to see exact field keys.
- **Rate limit:** 60 requests per minute per token. If you get 429, wait and retry.
- **Image fields** use `{"url": "..."}` format, not plain URL strings.
- **RichText fields** need valid HTML — simple text strings may not render correctly.

## Related Skills

- `openclaw-imports/webflow` — legacy project-specific skill for Berendstrik site (contains specific site IDs and tokens for that project)

## References

- `references/vrijheid-vastgoed.md` — Vrijheid Vastgoed project-specific details