# Google Drive extraction for Cognify

## Auth issue
`gws drive files export` returns 401 even when `gws drive files list` succeeds.
The export subcommand appears to use a different auth path.

## Workaround
Use direct Google Drive API with access token:

```python
import json, urllib.request

with open("/root/.config/gws/tokens.json") as f:
    token = json.load(f)["access_token"]

url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=text/plain"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
with urllib.request.urlopen(req, timeout=15) as resp:
    text = resp.read().decode('utf-8')
```

## Token refresh
```bash
python3 /root/.hermes/scripts/refresh_google_token.py
```

## Key files for Ramzy
| Name | ID | Type |
|------|-----|------|
| GIVEAWAY NOTES | `1f-44ZGW-E0Z4wX9Mwa5sgF-pzNclZtn38Ftfln2kYao` | Google Doc |
| Giveaway Lead Command Center | `1DlRTlRelh_or_E5gUYIHiUgyUrY8hsGWnQ86YaxuFbY` | Google Sheet |
| Call transcripts | Multiple, named "Cali Creed ... Notes by Gemini" | Google Doc |

## Finding call transcripts
```bash
gws drive files list --params '{"q": "name contains \"Notes by Gemini\"", "orderBy": "modifiedTime desc", "pageSize": 20}'
```