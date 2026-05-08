#!/usr/bin/env node
/**
 * Google Drive API Wrapper for Appie
 * Handles OAuth and provides file operations
 * 
 * Usage:
 *   node api.js auth                    # Start OAuth flow
 *   node api.js list [--folder ID]      # List files
 *   node api.js search "query"          # Search files
 *   node api.js upload <file> [--folder ID] [--name NAME]
 *   node api.js download <fileId> <output>
 *   node api.js mkdir <name> [--parent ID]
 *   node api.js share <fileId> <email> [--role reader|writer]
 *   node api.js info <fileId>           # Get file info
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL, URLSearchParams } = require('url');

// Configuration
const CONFIG_PATH = process.env.GDRIVE_CONFIG || path.join(process.env.HOME, '.config/gdrive/tokens.json');
const CLIENT_ID = process.env.GOOGLE_CLIENT_ID || '91158309108-r4ib3v2ot6ag3o5bdn8ph1i705pkd0ho.apps.googleusercontent.com';
const CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET || ''  /* set GOOGLE_CLIENT_SECRET env var; never hardcode */;
const REDIRECT_URI = 'http://localhost:3333/callback';
const SCOPES = [
  'https://www.googleapis.com/auth/drive.file',
  'https://www.googleapis.com/auth/drive.readonly',
];

// Token storage
function loadTokens() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    }
  } catch (e) { /* ignore */ }
  return null;
}

function saveTokens(tokens) {
  const dir = path.dirname(CONFIG_PATH);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(tokens, null, 2), { mode: 0o600 });
}

// OAuth flow
async function startAuthFlow() {
  const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?` + new URLSearchParams({
    client_id: CLIENT_ID,
    redirect_uri: REDIRECT_URI,
    response_type: 'code',
    scope: SCOPES.join(' '),
    access_type: 'offline',
    prompt: 'consent',
  }).toString();

  console.log('\n🔐 Google Drive OAuth Setup\n');
  console.log('1. Open this URL in your browser:\n');
  console.log(authUrl);
  console.log('\n2. Sign in and authorize the app');
  console.log('3. You will be redirected to localhost:3333\n');

  return new Promise((resolve, reject) => {
    const server = http.createServer(async (req, res) => {
      const url = new URL(req.url, `http://${req.headers.host}`);
      
      if (url.pathname === '/callback') {
        const code = url.searchParams.get('code');
        
        if (code) {
          try {
            const tokens = await exchangeCode(code);
            saveTokens(tokens);
            
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end('<h1>✅ Authorization successful!</h1><p>You can close this window.</p>');
            
            console.log('✅ Tokens saved to', CONFIG_PATH);
            server.close();
            resolve(tokens);
          } catch (err) {
            res.writeHead(500, { 'Content-Type': 'text/html' });
            res.end(`<h1>❌ Error</h1><p>${err.message}</p>`);
            server.close();
            reject(err);
          }
        } else {
          res.writeHead(400, { 'Content-Type': 'text/html' });
          res.end('<h1>❌ No code received</h1>');
        }
      }
    });

    server.listen(3333, () => {
      console.log('Waiting for authorization...\n');
    });
    
    // Timeout after 5 minutes
    setTimeout(() => {
      server.close();
      reject(new Error('OAuth timeout'));
    }, 300000);
  });
}

async function exchangeCode(code) {
  return new Promise((resolve, reject) => {
    const postData = new URLSearchParams({
      code,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      redirect_uri: REDIRECT_URI,
      grant_type: 'authorization_code',
    }).toString();

    const req = https.request({
      hostname: 'oauth2.googleapis.com',
      path: '/token',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': postData.length,
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const tokens = JSON.parse(data);
        if (tokens.error) {
          reject(new Error(tokens.error_description || tokens.error));
        } else {
          resolve(tokens);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function refreshAccessToken(refreshToken) {
  return new Promise((resolve, reject) => {
    const postData = new URLSearchParams({
      refresh_token: refreshToken,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      grant_type: 'refresh_token',
    }).toString();

    const req = https.request({
      hostname: 'oauth2.googleapis.com',
      path: '/token',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': postData.length,
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const response = JSON.parse(data);
        if (response.error) {
          reject(new Error(response.error_description || response.error));
        } else {
          resolve(response.access_token);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function getAccessToken() {
  const tokens = loadTokens();
  if (!tokens) {
    throw new Error('Not authenticated. Run: node api.js auth');
  }
  
  // Check if token is expired (with 5 min buffer)
  if (tokens.expires_at && Date.now() > tokens.expires_at - 300000) {
    console.log('Refreshing access token...');
    const newAccessToken = await refreshAccessToken(tokens.refresh_token);
    tokens.access_token = newAccessToken;
    tokens.expires_at = Date.now() + 3600000; // 1 hour
    saveTokens(tokens);
  }
  
  return tokens.access_token;
}

// API calls
async function driveRequest(path, method = 'GET', body = null, isUpload = false) {
  const accessToken = await getAccessToken();
  const hostname = isUpload ? 'www.googleapis.com' : 'www.googleapis.com';
  
  return new Promise((resolve, reject) => {
    const options = {
      hostname,
      path: `/drive/v3${path}`,
      method,
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Accept': 'application/json',
      },
    };

    if (body && !isUpload) {
      options.headers['Content-Type'] = 'application/json';
    }

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.error) {
            reject(new Error(parsed.error.message));
          } else {
            resolve(parsed);
          }
        } catch {
          resolve(data);
        }
      });
    });

    req.on('error', reject);
    if (body && !isUpload) req.write(JSON.stringify(body));
    req.end();
  });
}

// Commands
async function listFiles(folderId = 'root', pageSize = 20) {
  const query = folderId === 'root' ? '' : `'${folderId}' in parents`;
  const params = new URLSearchParams({
    pageSize: pageSize.toString(),
    fields: 'files(id,name,mimeType,size,modifiedTime)',
    orderBy: 'modifiedTime desc',
  });
  if (query) params.set('q', query);
  
  const result = await driveRequest(`/files?${params}`);
  
  console.log('ID | Name | Type | Size | Modified');
  console.log('-'.repeat(80));
  
  (result.files || []).forEach(f => {
    const type = f.mimeType.includes('folder') ? '📁' : '📄';
    const size = f.size ? `${Math.round(f.size / 1024)}KB` : '-';
    const modified = f.modifiedTime ? new Date(f.modifiedTime).toLocaleDateString() : '-';
    console.log(`${f.id} | ${type} ${f.name} | ${size} | ${modified}`);
  });
  
  return result.files;
}

async function searchFiles(query) {
  const params = new URLSearchParams({
    q: `name contains '${query}' or fullText contains '${query}'`,
    pageSize: '20',
    fields: 'files(id,name,mimeType,size,modifiedTime)',
  });
  
  const result = await driveRequest(`/files?${params}`);
  
  console.log(`Found ${result.files?.length || 0} files matching "${query}":\n`);
  (result.files || []).forEach(f => {
    const type = f.mimeType.includes('folder') ? '📁' : '📄';
    console.log(`${type} ${f.name} (${f.id})`);
  });
  
  return result.files;
}

async function getFileInfo(fileId) {
  const params = new URLSearchParams({
    fields: 'id,name,mimeType,size,modifiedTime,webViewLink,parents',
  });
  const result = await driveRequest(`/files/${fileId}?${params}`);
  console.log(JSON.stringify(result, null, 2));
  return result;
}

async function createFolder(name, parentId = 'root') {
  const result = await driveRequest('/files', 'POST', {
    name,
    mimeType: 'application/vnd.google-apps.folder',
    parents: [parentId],
  });
  
  console.log(`✅ Created folder: ${name} (${result.id})`);
  return result;
}

async function shareFile(fileId, email, role = 'reader') {
  const result = await driveRequest(`/files/${fileId}/permissions`, 'POST', {
    type: 'user',
    role,
    emailAddress: email,
  });
  
  console.log(`✅ Shared with ${email} as ${role}`);
  return result;
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  try {
    switch (command) {
      case 'auth':
        await startAuthFlow();
        break;
        
      case 'list': {
        const folderIdx = args.indexOf('--folder');
        const folderId = folderIdx > -1 ? args[folderIdx + 1] : 'root';
        await listFiles(folderId);
        break;
      }
      
      case 'search':
        if (!args[1]) throw new Error('Usage: search "query"');
        await searchFiles(args[1]);
        break;
        
      case 'info':
        if (!args[1]) throw new Error('Usage: info <fileId>');
        await getFileInfo(args[1]);
        break;
        
      case 'mkdir': {
        if (!args[1]) throw new Error('Usage: mkdir <name> [--parent ID]');
        const parentIdx = args.indexOf('--parent');
        const parentId = parentIdx > -1 ? args[parentIdx + 1] : 'root';
        await createFolder(args[1], parentId);
        break;
      }
      
      case 'share': {
        if (!args[1] || !args[2]) throw new Error('Usage: share <fileId> <email> [--role reader|writer]');
        const roleIdx = args.indexOf('--role');
        const role = roleIdx > -1 ? args[roleIdx + 1] : 'reader';
        await shareFile(args[1], args[2], role);
        break;
      }
      
      default:
        console.log(`
Google Drive API Wrapper for Appie

Commands:
  auth                          Start OAuth flow (one-time setup)
  list [--folder ID]            List files in folder
  search "query"                Search for files
  info <fileId>                 Get file details
  mkdir <name> [--parent ID]    Create folder
  share <fileId> <email> [--role reader|writer]

First time? Run: node api.js auth
        `);
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
