# Google Drive Skill

## Purpose
Interact with Google Drive - list files, upload, download, and manage sharing.

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

### Upload File
```bash
gdrive upload /path/to/file.txt --name "backup.txt" --folder "Appie Backups"
```

### Download File
```bash
gdrive download <file-id> --output /path/to/save.txt
```

### Create Folder
```bash
gdrive mkdir "New Folder" --parent "parent-folder-id"
```

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

## Common Use Cases

| Use Case | Implementation |
|----------|----------------|
| Auto-backup | Appie → Drive → Daily backup folder |
| File sharing | Generate share links |
| Document sync | Sync local files to Drive |
| Team folders | Create organized folder structure |

## Error Handling

- **401**: Token expired - refresh token
- **403**: Permission denied - check sharing settings
- **404**: File not found - verify file-id
- **429**: Rate limit - wait and retry

## See Also
- [Google Drive API Docs](https://developers.google.com/drive/api/v3)
