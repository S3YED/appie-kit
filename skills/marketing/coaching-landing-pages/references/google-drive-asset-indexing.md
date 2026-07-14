# Google Drive Asset Indexing (OAuth)

Pattern for recursively listing and downloading all files from a shared Google Drive folder using Python + OAuth token refresh.

## Use Case

When a client shares a Google Drive folder with brand assets (logos, photos, fonts, styleguides). Index everything, download to local project, then use in the build.

## Pattern

```python
import json, urllib.request, urllib.parse, os

# 1. Refresh OAuth token
with open('~/.weblyfe-secrets/gmail-drive-token.json') as f:
    token_data = json.load(f)
with open('~/.config/gws/client_secret.json') as f:
    secret = json.load(f).get('installed', json.load(f))

body = urllib.parse.urlencode({
    'client_id': secret['client_id'],
    'client_secret': secret['client_secret'],
    'refresh_token': token_data['refresh_token'],
    'grant_type': 'refresh_token'
}).encode()
access_token = json.loads(urllib.request.urlopen(
    urllib.request.Request('https://oauth2.googleapis.com/token', data=body)
).read())['access_token']

# 2. Recursive list
def list_files(parent_id):
    entries = {}
    page_token = None
    while True:
        q = f'"{parent_id}" in parents and trashed=false'
        url = f'https://www.googleapis.com/drive/v3/files?q={urllib.parse.quote(q)}&pageSize=50&fields=files(id,name,mimeType,size),nextPageToken'
        if page_token:
            url += f'&pageToken={page_token}'
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {access_token}'})
        data = json.loads(urllib.request.urlopen(req).read())
        for f in data.get('files', []):
            entries[f['name']] = {'id': f['id'], 'mime': f.get('mimeType', ''), 'size': f.get('size')}
        page_token = data.get('nextPageToken')
        if not page_token:
            break
    return entries

# 3. Download file
def download_file(file_id, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    url = f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {access_token}'})
    resp = urllib.request.urlopen(req, timeout=30)
    with open(out_path, 'wb') as f:
        f.write(resp.read())

# 4. Recursive download
def download_folder(parent_id, prefix=''):
    for name, info in list_files(parent_id).items():
        if info['mime'] == 'application/vnd.google-apps.folder':
            download_folder(info['id'], os.path.join(prefix, name))
        else:
            download_file(info['id'], os.path.join(prefix, name))
```

## Pitfalls

- **Gebruik page tokens** — folders met >50 items hebben paginatie
- **403 Forbidden** — sommige Google Workspace files (niet binaries) kunnen niet via alt=media gedownload worden; skip of export via exportLinks
- **Token expiry** — refresh token geeft 3600s access token; bij lange downloads opnieuw refreshen
- **`json.load(f).get('installed', json.load(f))` faalt** — tweede `json.load(f)` leest van EOF. Fix: `raw = json.load(f); secret = raw.get('installed', raw)`
- **Gebruik `urllib.parse.quote()`** voor de query parameter anders breken speciale characters de URL

## Files on This Machine

- OAuth tokens: `~/.weblyfe-secrets/gmail-drive-token.json`, `seyed_token.json`, `weblyfenl_token.json`
- Client secret: `~/.config/gws/client_secret.json`
- Credentials: `~/.config/gws/credentials.json`
