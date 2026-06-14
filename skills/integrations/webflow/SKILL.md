---
name: webflow
description: "Operate Webflow CMS for Weblyfe client sites, including collections, item updates, image fields, publishing, and asset-upload fallbacks."
version: 1.0.0
category: integrations
---

# Webflow CMS Skill

## Credentials
- **API Token**: `WEBFLOW_API_TOKEN` environment variable
- **Site ID**: `WEBFLOW_SITE_ID` environment variable
- **Site**: <webflow-site-domain>

## Image Upload Workflow

### OPTION 1: Webflow Native (PREFERRED — but requires asset upload permission)

```javascript
const { WebflowClient } = require('webflow-api');
const fs = require('fs');

const client = new WebflowClient({
  token: process.env.WEBFLOW_API_TOKEN
});

async function uploadAsset(filePath, fileName) {
  const fileBuffer = fs.readFileSync(filePath);
  const arrayBuffer = fileBuffer.buffer.slice(
    fileBuffer.byteOffset,
    fileBuffer.byteOffset + fileBuffer.byteLength
  );

  return await client.assets.utilities.createAndUpload(
    process.env.WEBFLOW_SITE_ID,
    { file: arrayBuffer, fileName }
  );
}
```

**⚠️ NOTE:** The Personal Access Token may not have asset upload permissions (401 Unauthorized). If this fails, use Zernio workaround below.

### OPTION 2: Zernio Workaround (RECOMMENDED when native fails)

```bash
# 1. Upload to Zernio
zernio media:upload /path/to/image.jpg
# Returns: {"url": "https://media.zernio.com/temp/..."}

# 2. Use the Zernio URL in Webflow PATCH
curl -X PATCH "https://api.webflow.com/v2/collections/<ID>/items/<ITEM_ID>" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"fieldData": {"cover": {"url": "https://media.zernio.com/temp/..."}}}'
```

## Collections

### Museums Collection
- **Collection ID**: `<COLLECTION_ID>`
- **Fields**: name, slug, museum-description, cover (Image), article (RichText), url-naar-collectie (Link), city (PlainText), pic-1 (Image)
- **Item IDs**: See museums section below

### Events Collection
- **Collection ID**: `<COLLECTION_ID>`
- **Fields**: name, date-time, location, location-link, gallery, cover-image (Image), event-short-description, event-description, google-maps-embed (RichText), event-passed

### Arts Collection
- **Collection ID**: `<COLLECTION_ID>`
- **Fields**: title, slug, category, image (Image), description

### FAQs Collection
- **Collection ID**: `<COLLECTION_ID>`

## Common Operations

```bash
# List collections
curl -s "https://api.webflow.com/v2/sites/<SITE_ID>/collections" \
  -H "Authorization: Bearer <TOKEN>"

# Get items
curl -s "https://api.webflow.com/v2/collections/<COLLECTION_ID>/items?limit=20" \
  -H "Authorization: Bearer <TOKEN>"

# Update item (PATCH)
curl -s -X PATCH "https://api.webflow.com/v2/collections/<COLLECTION_ID>/items/<ITEM_ID>" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"fieldData": {"field-slug": "value"}}'

# Update image field
curl -s -X PATCH "https://api.webflow.com/v2/collections/<COLLECTION_ID>/items/<ITEM_ID>" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"fieldData": {"cover": {"url": "https://..."}}}'

# Publish site
curl -s -X POST "https://api.webflow.com/v2/sites/<SITE_ID>/publish" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Museums (11 items)
| ID | Naam | City |
|----|------|------|
| `<ITEM_ID>` | Stedelijk Museum Amsterdam | Amsterdam |
| `<ITEM_ID>` | Collectie Gelderland | Arnhem |
| `<ITEM_ID>` | Fries Museum | Leeuwarden |
| `<ITEM_ID>` | Museum Boijmans Van Beuningen | Rotterdam |
| `<ITEM_ID>` | Museum De Lakenhal | Leiden |
| `<ITEM_ID>` | SCHUNCK | Heerlen |
| `<ITEM_ID>` | Museum Het Valkhof | Nijmegen |
| `<ITEM_ID>` | Rijksmuseum Twenthe | Enschede |
| `<ITEM_ID>` | Stedelijk Museum Schiedam | Schiedam |
| `<ITEM_ID>` | TextielMuseum | Tilburg |
| `<ITEM_ID>` | Museum Het Domein | Sittard |

## Events (5 items)
| ID | Naam | Gallery | Date |
|----|------|--------|------|
| `<ITEM_ID>` | Heem | Fries Museum | 28 Apr 2024 – 27 Apr 2025 |
| `<ITEM_ID>` | 33 1/3 RPM | De Vishal | 7 Sep – 13 Oct 2024 |
| `<ITEM_ID>` | Copilot, Voice and Vision | Galerie Fons Welters | 2 Nov – 21 Dec 2024 |
| `<ITEM_ID>` | Connecting Threads | GPS Gallery | 9 Jan – 17 Jan 2026 |
| `<ITEM_ID>` | Art Rotterdam 2026 | Rotterdam Ahoy | 27 – 29 Mar 2026 |

## Error Codes
- **401**: Invalid token or no asset upload permission
- **404**: Collection/item not found
- **429**: Rate limited — wait 60s
- **validation_error**: Missing required field

## Notes
- Image fields use `{"url": "..."}` format, not plain URL string
- RichText fields need valid HTML
- Asset upload via native API may fail with 401 if token lacks permissions → use Zernio workaround
