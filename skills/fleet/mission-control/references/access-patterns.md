# Mission Control Access Control — Proxy Logic

## The Problem

External access (MacBook Pro → Mac Mini via Tailscale) returns `403 Forbidden` even though:
- Server is bound to `0.0.0.0` (all interfaces)
- Port is reachable
- No firewall blocking

## Root Cause

`src/proxy.ts` line 163:
```ts
const allowAnyHost = envFlag('MC_ALLOW_ANY_HOST') || process.env.NODE_ENV !== 'production'
```

In production (`NODE_ENV=production`), this always falls through to the allowlist check unless `MC_ALLOW_ANY_HOST` is explicitly set.

Lines 162-178:
```ts
const requestHosts = getRequestHostCandidates(request)
const allowAnyHost = envFlag('MC_ALLOW_ANY_HOST') || process.env.NODE_ENV !== 'production'
const allowedPatterns = String(process.env.MC_ALLOWED_HOSTS || '')
  .split(',')
  .map((s) => s.trim())
  .filter(Boolean)
const implicitAllowedHosts = getImplicitAllowedHosts()

const enforceAllowlist = !allowAnyHost && allowedPatterns.length > 0
const isAllowedHost = !enforceAllowlist
  || requestHosts.some((hostName) =>
    implicitAllowedHosts.some((candidate) => hostMatches(candidate, hostName))
    || allowedPatterns.some((pattern) => hostMatches(pattern, hostName))
  )

if (!isAllowedHost) {
  return addSecurityHeaders(new NextResponse('Forbidden', { status: 403 }), request)
}
```

When `enforceAllowlist` is true and the requesting hostname (e.g. `100.101.29.56`) doesn't match any pattern in `MC_ALLOWED_HOSTS`, it returns 403.

## Fix

Add Tailscale range (`100.*`) and local network (`192.168.*`) to `.env`:

```
MC_ALLOWED_HOSTS=localhost,127.0.0.1,::1,100.*,192.168.*
```

### Pattern Types

- `localhost` — exact match
- `*.example.com` — subdomain wildcard
- `100.*` — prefix wildcard (matches any IPv4 starting with 100.)

## Restart Required

`.env` changes are read at server startup. Must restart:
```bash
kill <PID>
cd /Users/appie/mission-control
npx next start --hostname 0.0.0.0 --port 3480
```

## Verification

```bash
# From local machine
curl -s -o /dev/null -w "%{http_code}" http://localhost:3480/setup
# Expected: 200

# From external machine (MacBook Pro)
curl -s -o /dev/null -w "%{http_code}" http://100.101.29.56:3480/setup
# Expected: 200
```
