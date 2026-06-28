---
name: google-drive
description: List, download, upload, and share Google Drive files, including public shared folder video intake when OAuth is unavailable.
---

# Google Drive Skill

## Purpose
Interact with Google Drive: list files, upload, download, create folders, manage sharing, and recover media from public shared Drive folders for analysis or social publishing.

## Key Folders

| Folder | ID | Purpose |
|--------|----|---------|
| **CURRENT** | `1SfLKzSCFsFWaCUl63_L9GtJWMIKSWTyO` | Active client projects (Weblyfe) |

## Capabilities
- List files in folders
- Upload files
- Download files
- Create folders
- Set sharing permissions
- Search files
- Download public shared video files even when OAuth is expired/revoked

## Configuration Required

### Environment Variables
```bash
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
# OAuth token obtained via OAuth flow
GOOGLE_ACCESS_TOKEN=your-access-token
GOOGLE_REFRESH_TOKEN=your-refresh-token
```

### Setup
1. Create OAuth app in Google Cloud Console
2. Enable Google Drive API
3. Get credentials
4. Complete OAuth flow to get tokens

## Usage Examples

### List Files
```bash
gdrive list --folder "Appie Backups"
```

### Upload
```bash
gdrive upload /path/to/file.txt --name "backup.txt" --folder "Appie Backups"
```

### Download
```bash
gdrive download <file-id> --output /path/to/save.txt
```

### Create Folder
```bash
gdrive mkdir "New Folder" --parent "parent-folder-id"
```

## OAuth/private Drive access checks

When the user asks whether Drive access is available, do not rely on stored account presence alone. First run a real read-only Drive probe with `gog drive ls --account seyed@weblyfe.nl --json --no-input` and inspect `gog auth list --json` for scopes. See `references/oauth-drive-access-check.md` for the exact check sequence and safe reporting pattern.

## Appie-2 OAuth with `gog`

For private Drive/Docs/Sheets access on Appie-2, use `references/gog-oauth-drive.md`. Key points: `gog` stores config/tokens under `/root/.config/gogcli/`; verify with `gog drive ls --account seyed@weblyfe.nl`; if tokens are expired or revoked, use the remote two-step OAuth flow and never echo auth codes or token contents.

## Public shared folder video fallback

If Drive OAuth fails with `invalid_grant`, `401`, or missing scopes but the user gave a public folder link, do not stop immediately. Use `references/public-shared-folder-video-download.md`:

1. Fetch the public folder HTML with a browser user agent.
2. Extract embedded Drive file IDs, names, MIME types, and sizes.
3. For large videos, parse the Google virus-scan warning form inputs.
4. Download via `https://drive.usercontent.google.com/download` with `id`, `export=download`, `confirm=t`, and `uuid`.
5. Verify with `ffprobe` before analysis or publishing.
6. For social use, transcode MOV/HEVC to H.264/AAC MP4 first.

## API Wrapper

### `api/google-drive.js`
```javascript
const drive = require('./api/google-drive.js');

// List files
const files = await drive.listFiles({ folderId: 'xxx' });

// Upload
await drive.uploadFile('/path/to/file.txt', { name: 'file.txt', folderId: 'xxx' });

// Download
await drive.downloadFile('file-id', '/path/to/save.txt');

// Search
const results = await drive.searchFiles('query string');
```

## Folder-to-folder media transfers

When the user asks to move or copy batches of videos/assets between Drive folders, use `references/folder-to-folder-media-copy.md`. Prefer `gog drive copy` for Drive-native file copies, inventory source/destination first, skip exact-name duplicates, then verify count, missing files, and binary size matches before reporting.

## Common Use Cases

| Use Case | Implementation |
|----------|----------------|
| Auto-backup | Appie → Drive → Daily backup folder |
| File sharing | Generate share links |
| Public video intake | Parse public folder HTML and use the large-file interstitial flow; see `references/public-shared-folder-video-download.md` |
| Folder-to-folder media transfer | Copy accessible Drive media with `gog drive copy`; see `references/folder-to-folder-media-copy.md` |
| Document sync | Sync local files to Drive |
| Team folders | Create organized folder structure |

## Error Handling

- **401**: Token expired - refresh token, or use the public shared folder fallback if the URL is public
- **403**: Permission denied - check sharing settings
- **404**: File not found - verify file-id
- **429**: Rate limit - wait and retry
- **Google virus scan warning**: For large public files, parse the download form and use `drive.usercontent.google.com/download`

## See Also
- [Google Drive API Docs](https://developers.google.com/drive/api/v3)
