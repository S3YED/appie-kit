# Webflow CMS Skill

## Credentials
- **API Token**: `YOUR_WEBFLOW_API_TOKEN`
- **Site ID**: `68f612cac31a6f533ce5528d`
- **Site**: berendstrik.webflow.io

## Image Upload Workflow

### OPTION 1: Webflow Native (PREFERRED — but requires asset upload permission)

```javascript
const { WebflowClient } = require('webflow-api');
const fs = require('fs');

const client = new WebflowClient({ 
  token: 'YOUR_WEBFLOW_API_TOKEN' 
});

async function uploadAsset(filePath, fileName) {
  const fileBuffer = fs.readFileSync(filePath);
  const arrayBuffer = fileBuffer.buffer.slice(
    fileBuffer.byteOffset, 
    fileBuffer.byteOffset + fileBuffer.byteLength
  );
  
  return await client.assets.utilities.createAndUpload(
    '68f612cac31a6f533ce5528d',
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
- **Collection ID**: `69ce595b57060eb28a767604`
- **Fields**: name, slug, museum-description, cover (Image), article (RichText), url-naar-collectie (Link), city (PlainText), pic-1 (Image)
- **Item IDs**: See museums section below

### Events Collection
- **Collection ID**: `69bfd230ceecbebceff82be0`
- **Fields**: name, date-time, location, location-link, gallery, cover-image (Image), event-short-description, event-description, google-maps-embed (RichText), event-passed

### Arts Collection
- **Collection ID**: `69bfd1ac805e504d421e717e`
- **Fields**: title, slug, category, image (Image), description

### FAQs Collection
- **Collection ID**: `69bfcf6e010a4c52f2a48c84`

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
| `69da5015eae9663f6a1249a7` | Stedelijk Museum Amsterdam | Amsterdam |
| `69da502755f63a9020331500` | Collectie Gelderland | Arnhem |
| `69da5028589590c9f45f26f5` | Fries Museum | Leeuwarden |
| `69da50296e1e2ae5ac11da20` | Museum Boijmans Van Beuningen | Rotterdam |
| `69da502a33b6e39977b3878e` | Museum De Lakenhal | Leiden |
| `69da502c36537a51a7297f60` | SCHUNCK | Heerlen |
| `69da502fff42dc29f5e158e4` | Museum Het Valkhof | Nijmegen |
| `69da51907598dd35f8bb0196` | Rijksmuseum Twenthe | Enschede |
| `69da519179c7893028f9a61a` | Stedelijk Museum Schiedam | Schiedam |
| `69da5192c39688272b34cd9f` | TextielMuseum | Tilburg |
| `69da519333b6e39977b3c51b` | Museum Het Domein | Sittard |

## Events (5 items)
| ID | Naam | Gallery | Date |
|----|------|--------|------|
| `69c905c1c217479704f7a9d4` | Heem | Fries Museum | 28 Apr 2024 – 27 Apr 2025 |
| `69c905bf336bdaf15ece39a1` | 33 1/3 RPM | De Vishal | 7 Sep – 13 Oct 2024 |
| `69c905bdfecfd85d4f92cc0d` | Copilot, Voice and Vision | Galerie Fons Welters | 2 Nov – 21 Dec 2024 |
| `69c905acfecfd85d4f92ca7d` | Connecting Threads | GPS Gallery | 9 Jan – 17 Jan 2026 |
| `69bfda27313639e3d6279b81` | Art Rotterdam 2026 | Rotterdam Ahoy | 27 – 29 Mar 2026 |

## Error Codes
- **401**: Invalid token or no asset upload permission
- **404**: Collection/item not found
- **429**: Rate limited — wait 60s
- **validation_error**: Missing required field

## Notes
- Image fields use `{"url": "..."}` format, not plain URL string
- RichText fields need valid HTML
- Asset upload via native API may fail with 401 if token lacks permissions → use Zernio workaround
