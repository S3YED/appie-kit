---
name: static-site-deployment
description: Deploy static HTML/CSS/JS sites to production hosting platforms (Vercel, Netlify, Cloudflare Pages). Covers both CLI and API-based deployment, including fallback patterns when CLI tools have compatibility issues.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [deployment, hosting, vercel, netlify, static-site, ops]
    related_skills: []
---

# Static Site Deployment

Deploy a static site (HTML/CSS/JS) to a production host. Supports Vercel (primary), with patterns extensible to Netlify and Cloudflare Pages.

## Prerequisites

- Static files (HTML, CSS, JS, assets) in a clean project directory
- Platform-specific credentials (API token or CLI auth)

## Vercel Deployment

### Method 1: Vercel CLI (Recommended — simpler, but token-dependent)

```bash
# From project directory (containing vercel.json + index.html)
cd /path/to/project
vercel deploy --yes --prod --name project-name
```

**Requires:** `VERCEL_TOKEN` env var or `vercel login` auth.

**Pitfall:** Vercel CLI v54+ may reject `vcp_` token format with "Must not contain" errors, even when the token is valid. This is a CLI version compatibility issue, not a token issue.

### Method 2: Vercel REST API (Fallback — works when CLI rejects token)

Use the Vercel API directly when the CLI has token compatibility issues:

```python
import json, subprocess, os, base64

payload = {
    "name": "your-project-name",
    "projectSettings": {"framework": None},
    "files": [
        {"file": "index.html", "data": base64.b64encode(open("index.html").read().encode()).decode()},
        {"file": "vercel.json", "data": base64.b64encode(open("vercel.json").read().encode()).decode()}
    ]
}

r = subprocess.run([
    "curl", "-s", "-X", "POST",
    "https://api.vercel.com/v12/deployments",
    "-H", f"Authorization: Bearer {token}",
    "-H", "Content-Type: application/json",
    "-d", json.dumps(payload)
], capture_output=True, text=True, timeout=30)

result = json.loads(r.stdout)
alias = result.get("alias", [result.get("url", "")])
print(f"Live: https://{alias[0]}")
```

The API returns a `url` field and an `alias` array with the live domain(s). The deployment may take 15-30 seconds to go live after INITIALIZING state.

### Required: vercel.json

```json
{
  "version": 2,
  "builds": [
    { "src": "*.html", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/index.html" }
  ]
}
```

**Key points:**
- `@vercel/static` build is for pure HTML/CSS — no framework needed
- The catch-all route ensures SPA-style navigation works
- Name must match between vercel.json and the deploy command/API

## Token Handling

### Safe Token Extraction from .env

When reading tokens from `.env` files, use positional parsing to avoid quoting issues:

```python
# SAFE — avoids markdown/tool corruption of token patterns
tok = None
with open("/path/to/.env") as f:
    for line in f:
        idx = line.find("=")
        if idx > 0 and line[:idx] == "KEY_NAME":
            tok = line[idx+1:].strip()
            break
```

**Pitfall:** Avoid `startswith("KEY_NAME=***")` pattern — the `***` gets corrupted by tool-level markdown rendering. Use `find("=")` and exact string matching on the key part only.

### Shell Extraction (for scripts)

```bash
TOK=$(awk -F= '/^KEY_NAME=*** $2}' /root/.hermes/.env | tail -1)
export TOKEN_KEY=*** deploy ...
```

## Verification

After deploying, verify availability:

```bash
curl -s -o /dev/null -w "HTTP %{http_code}" -L -m 10 "https://your-project.vercel.app"
```

Expected: `HTTP 200`. If `404` after 30+ seconds, check:
- routing in vercel.json (dest path must match actual filename)
- deployment build logs via Vercel dashboard or API
- whether index.html is the entry point

## Pitfalls

- **Vercel CLI + `vcp_` tokens:** CLI v54 may reject valid tokens. Use the API method (Method 2) as fallback.
- **INITIALIZING state:** The API returns immediately but the site may take 15-30s to go live. Wait and retry.
- **Home directory deployment:** Always `cd` into the project directory first. Vercel defaults to deploying CWD.
- **Token in shell scripts:** Tokens with special characters (`+`, `=`, `/`) break double-quoted strings in bash. Always write JSON payloads to a temp file with Python, or use single-quote heredocs.
- **Base64 encoding:** File contents must be base64-encoded for the Vercel API deployment payload. The API does not accept raw file uploads.