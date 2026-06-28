---
name: deployment-inspection
title: Deployment Inspection & Client Project Discovery
description: End-to-end investigation of a live client deployment — platform detection, subdomain discovery, deployment API access (Netlify), JS bundle analysis, repo discovery.
trigger: User asks to "find", "open", "check", "look at", "investigate" a client's website, app, or project. Also triggered by "wat staat er op [domain]", "kan je de deploy checken", "waar staat dit project".
---

# Deployment Inspection

## When to Use

Load this skill when the user says:
- "Vind het project [domain]" / "Open de site"
- "Check de deploy" / "Kijk in de codebase"
- "Waar staat dit project?"
- Any request to investigate a live web project, its hosting platform, codebase, or deployment setup

## Detection Flow

### 1. Platform Detection

Run these checks in order to identify where the site is hosted:

```bash
# Check HTTP response headers
curl -sI https://domain.com | grep -i "server\|x-powered-by\|x-served-by\|cache-status"
```

| Header value | Platform |
|---|---|
| `server: cloudflare` | Behind Cloudflare — check further |
| `server: Netlify` + `Netlify Edge` cache | **Netlify** |
| `server: Vercel` | **Vercel** |
| `x-powered-by: Express` | Custom Node.js server |
| `x-served-by: Webflow` or scripts from `cdn.prod.website-files.com` | **Webflow** |

**Webflow confirmation** — check script sources in the HTML for `cdn.prod.website-files.com`:
```bash
curl -s https://domain.com | grep -o 'src="[^"]*"' | grep -i 'website-files'
```

### 2. Subdomain Discovery

When the user says the app is at a subdomain that doesn't resolve:
```bash
# Check DNS first
dig booking.domain.com +short
dig book.domain.com +short
dig app.domain.com +short

# Check nameservers for hosting clues
dig domain.com NS +short

# Check local screenshot tool configs for the real URL
grep -r 'domain.com\|domain' ~/clawd/projects/*/screenshot-tool.js 2>/dev/null
grep -r 'domain.com\|domain' ~/clawd/tools/*.js 2>/dev/null
```

**Known pattern:** The screenshot-tool.js in Weblyfe projects often has the correct subdomain URLs for client sites. Always check there first when a subdomain doesn't resolve.

### 3. Netlify API Access

When the site is confirmed on Netlify:

```bash
# Token location
source ~/.weblyfe-secrets/.env  # exports NETLIFY_AUTH_TOKEN

# List sites and search by name
curl -s -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
  "https://api.netlify.com/api/v1/sites?page=1&per_page=100" | \
  python3 -c "import sys,json; sites=json.load(sys.stdin); [print(f\"{s.get('name')} | {s.get('custom_domain','-')} | {s.get('ssl_url','-')}\") for s in sites]"

# Get full site info
curl -s -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
  "https://api.netlify.com/api/v1/sites/{site_id}"

# Check deploys (latest 5)
curl -s -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
  "https://api.netlify.com/api/v1/sites/{site_id}/deploys?page=1&per_page=5"

# Check environment variables
curl -s -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
  "https://api.netlify.com/api/v1/sites/{site_id}/env"
```

**Key fields from site info:**
- `name` — Netlify site name
- `custom_domain` — custom domain (e.g. book.titantransfers.be)
- `state` — `current` = live
- `build_settings.repo_url` — GitHub repo
- `build_settings.repo_branch` — deploy branch
- `build_settings.cmd` — build command
- `build_settings.dir` — publish directory
- `created_at` — when it was deployed

**Deploy fields:**
- `state` — `ready` = success, `error` = build failed
- `published` — `true` = currently served
- `created_at` — deploy time
- `commit_ref` — commit SHA
- `commit_url` — link to GitHub commit
- `deploy_time` — seconds
- `error_message` — build error details

### 4. GitHub Repo Discovery

The Netlify build settings include `repo_url` (e.g. `https://github.com/S3YED/titan-transfers-2`).

To access the repo:
```bash
# Try gh CLI first
gh repo view owner/repo --json name,description,defaultBranch,updatedAt,languages

# Fallback: GitHub API with token from .env
source ~/.weblyfe-secrets/.env
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/owner/repo"

# Check latest commit on branch
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/owner/repo/branches/main"
```

**Pitfall:** GitHub tokens expire. Check the token before relying on it:
```bash
source ~/.weblyfe-secrets/.env
curl -s -w "\nHTTP: %{http_code}" -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/user"
# 401 = expired/revoked token
```

### 5. JS Bundle Analysis (SPA Inspection)

When you need to understand what a production SPA does internally:

```bash
# Find the JS bundle from the HTML
curl -s https://app.domain.com | grep -o 'src="[^"]*\.js[^"]*"' 

# Download and analyze
curl -s https://app.domain.com/assets/index-hash.js > /tmp/bundle.js

# Check for framework clues
head -1 /tmp/bundle.js | grep -o 'react|vue|svelte|angular|preact' 

# Search for key features
grep -c 'admin\|dashboard' /tmp/bundle.js
grep -c 'supabase\|firebase\|auth0\|clerk' /tmp/bundle.js
grep -c 'stripe\|payment\|checkout' /tmp/bundle.js

# Extract admin routes (Supabase pattern)
grep -oP '/admin/[a-z_/]+' /tmp/bundle.js | sort -u

# Check Vite/Vue/React indicator
curl -s https://app.domain.com | grep -i 'vite\.svg\|_nuxt\|__NEXT_DATA__\|__NUXT__'
```

**Admin dashboard patterns:** Supabase admin routes commonly include:
- `/admin/generate_link` — invite links
- `/admin/users` — user management
- `/admin/users/{id}/factors` — auth factors

**Framework indicators:**
- `vite.svg` favicon = Vite-based (React/Svelte/Vue)
- `__NEXT_DATA__` script = Next.js
- `_nuxt/` in script paths = Nuxt.js
- `/assets/index-{hash}.js` = Vite default

### 6. Live App Navigation

For SPA booking apps and multi-step forms:
- Check the console for the actual route/state after interacting
- Try common protected routes: `/admin`, `/dashboard`, `/login`, `/api`
- Check footer for platform attribution ("App created by Weblyfe", "Powered by...")
- Identify the auth provider (Supabase, Firebase, Auth0) from JS bundle

## Pitfalls

- **Subdomain confusion** — User says "booking." but the actual URL is "book." (or "app.", "portal."). Always check DNS + screenshot configs before reporting failure.
- **Published deploy confusion** — Netlify recent deploys can show `published: null` even when the site is live. An older deploy may be published.
- **Empty SPA routes** — Protected routes like `/admin` show an empty page shell when not authenticated. This doesn't mean the admin panel doesn't exist — check the JS bundle for route patterns.
- **GitHub token expiry** — GH tokens in `.weblyfe-secrets/.env` may be expired. Check before relying on them. The Netlify token is more stable.
- **JS bundle size** — Production bundles can be 500KB+. For large bundles, use streamed extraction instead of loading the full file:
  ```bash
  curl -s https://domain.com/assets/bundle.js | grep -oP '.{0,100}admin.{0,100}' | head -5
  ```

## Related

- `web-research` — for general web research and SEO content extraction
- `webflow-seo-audit` — for Webflow-specific site audits
- `security-scanning` — for security header and CVE checks on deployed sites
- `github-repo-management` — for working with discovered repos