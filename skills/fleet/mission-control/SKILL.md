---
name: mission-control
description: Deploy, configure, and troubleshoot Mission Control (OpenClaw/Appie fleet dashboard). Use when setting up MC, fixing access issues, or managing gateways.
tags: [fleet, dashboard, mission-control, nextjs, deployment]
---

# Mission Control — Fleet Dashboard

Open-source agent orchestration dashboard (Next.js 16, builderz-labs fork with Weblyfe skin). **Canonical deployment runs on `appie-mc-1` (Hetzner), NOT the Mac Mini.** Systemd service `mission-control`, port 3000, tailnet-only via `tailscale serve`.

The Mac Mini runs the **heartbeat** (`mc-heartbeat-manifest.py`, `~/clawd/tools/`) that pushes agent status to MC-1. Local MC clones on the mini are planning/staging copies only — never run production tasks against them.

## Access

- **Canonical URL:** `https://appie-mc-1.tail61f54b.ts.net` (tailnet-only)
- **Tailnet IP:** `100.107.179.3` (reachable via appie-2 hop if MagicDNS is off on mini)
- **Access pattern:** `ssh appie-2 "curl -s http://100.107.179.3:3000/api/health"`
- Default creds: see `references/credentials.md`

## Deploy model (NEVER edit `/opt/mission-control` directly on mc-1)

MC-1 uses a gated wave-deploy with auto-rollback. The full process, branch naming conventions, and verification checklist are in `references/mc-deploy-handoff.md`. Key rules:
- Hardlink copy (`cp -al`) to `/opt/mc-build`, overlay changed source files, build with pnpm, atomic swap → `systemctl restart`
- Backup DB before every deploy
- Verify: health 200, correct BUILD_ID, agents ≥21, `/api/knowledge/graph source=cognify-kb`
- Preserve `.env.local` across deploys (contains FLEET_MEMORY_URL, LOCAL_LLM_API_KEY, MC_DISPATCH_MODEL, etc.)

## Heartbeat (Mac Mini → MC-1)

The fleet heartbeat daemon lives on the Mac Mini at `~/clawd/tools/mc-heartbeat-manifest.py` (301 lines, Python 3). It POSTs agent status (crons, skills, integrations) to MC-1's `/api/agents/<agent>/heartbeat` endpoint every 60s.

**Mac Mini agents run via launchd (60s interval):**
- `com.weblyfe.mc-heartbeat-appie1` — Appie-1
- `com.weblyfe.mc-heartbeat-opus` — Appie-Opus
- `com.weblyfe.mc-heartbeat-appie4` — Appie-4 (CFO, separate Hermes instance)

**Remote agents run via systemd timer (60s):**
- Appie-2 (Hetzner): `/etc/systemd/system/mc-heartbeat-appie2.{service,timer}` — runs `/opt/mc-heartbeat-manifest.py --agent Appie-2`
- Appie-3 (Hetzner): same pattern via appie-2 hop — `/opt/mc-heartbeat-manifest.py --agent Appie-3`

**Critical script detail — `MC_TAILSCALE_IP`:** The script's IP fallback must point to MC-1's Tailscale IP (`100.107.179.3`). If the Mac Mini has MagicDNS off, the script falls back to a direct HTTPS connection to this IP. A wrong IP here (e.g., the mini's own `100.101.29.56`) causes SSL errors on every heartbeat.

**Sync to remote agents after script changes:**
```bash
scp ~/clawd/tools/mc-heartbeat-manifest.py appie-2:/opt/mc-heartbeat-manifest.py
ssh appie-2 "scp /opt/mc-heartbeat-manifest.py root@100.69.131.51:/opt/mc-heartbeat-manifest.py"
```

**Diagnose heartbeats:**
```bash
# Mac Mini: check launchd logs
cat ~/Library/Logs/mc-heartbeat-appie1.log
cat ~/Library/Logs/mc-heartbeat-appie1.err.log

# Remote: check systemd logs
ssh appie-2 "journalctl -u mc-heartbeat-appie2 --no-pager -n 5"
ssh appie-2 "ssh -n root@100.69.131.51 'journalctl -u mc-heartbeat-appie3 --no-pager -n 5'"

# Dry-run test (no POST, just collect and print)
python3 ~/clawd/tools/mc-heartbeat-manifest.py --agent Appie-1 --dry-run
```

## Accessing MC-1 from the Mac Mini

The Mac Mini has **MagicDNS off** — `appie-mc-1.tail61f54b.ts.net` won't resolve. Use the Tailnet IP directly, or hop through appie-2:

```bash
# Direct (from mini, if Tailnet IP is reachable)
curl http://100.107.179.3:3000/api/health

# Via appie-2 hop
ssh appie-2 "curl -s --max-time 5 http://100.107.179.3:3000/api/health"

## Pitfalls

### 0. MC-1 unreachable from Mac Mini

**Root cause:** Mac Mini has MagicDNS off. `appie-mc-1.tail61f54b.ts.net` won't resolve.

**Fix:** Use Tailnet IP directly (`100.107.179.3`) or hop through appie-2 (`ssh appie-2 "curl http://100.107.179.3:3000/api/health"`).

### 1. All agents show "idle" / stale status

### 1. All agents show "idle" / stale status

**Root cause:** Heartbeat not running on the Mac Mini. `mc-heartbeat-manifest.py` is NOT in launchd.

**Fix:** Start it manually or add to launchd (see Heartbeat section above). Without heartbeats, MC-1 stores the last known status but never updates.

### 2. MC-1 server appears DOWN

**Root cause:** The `mission-control` systemd service on appie-mc-1 may have stopped. The box itself is usually alive on Tailscale.

**Diagnose:**
```bash
ssh appie-2 "ssh -n root@100.107.179.3 'systemctl is-active mission-control'"
ssh appie-2 "curl -s --max-time 5 http://100.107.179.3:3000/api/health"
```

**Fix:**
```bash
ssh appie-2 "ssh -n root@100.107.179.3 'systemctl restart mission-control'"
# Wait 5s, then verify health check
ssh appie-2 "curl -s --max-time 10 http://100.107.179.3:3000/login"
```

### 3. Dispatch not working (tasks stuck)

**Root cause:** `MC_DISPATCH_MODEL` pointing at wrong provider, or dispatch routing stripped prefix → routes to Anthropic with no key.

**Fix (on mc-1):** Set in `.env.local`:
```
MC_DISPATCH_MODEL=litellm/deepseek/deepseek-v4-flash
LOCAL_LLM_ENDPOINT=https://openrouter.ai/api/v1
```
The `litellm/` prefix preserves provider routing. Never use `provider: auto`.

### 5. Routing 404s on New Projects
When creating a new Vercel project from terminal, it may default to a generic name or have `autoExposeSystemEnvs` / `ssoProtection` enabled which causes a 404 / 302 wall for unauthenticated agents.
**Fix:** Force link to existing project name: `vercel link --project <name> --yes`. Ensure SSO is disabled via `PATCH /v9/projects/{id}` body `{"ssoProtection": null, "autoExposeSystemEnvs": false}`.

### 6. Domain ownership (403 Forbidden)
If `GET /v5/domains/{domain}` returns 403, the domain belongs to a different Vercel account/user, not just a different team on the current token.
**Verification:** Check all stored tokens: `grep -r "VERCEL_TOKEN" ~/.hermes/.env`. If all fail, the user must manually remove the domain from the old account.

## References

- `references/mc-feature-roadmap.md` — open features and defects from the July 4 handoff audit

### 5. Routing 404s on New Projects
When creating a new Vercel project from terminal, it may default to a generic name or have `autoExposeSystemEnvs` / `ssoProtection` enabled which causes a 404 / 302 wall for unauthenticated agents.
**Fix:** Force link to existing project name: `vercel link --project <name> --yes`. Ensure SSO is disabled via `PATCH /v9/projects/{id}` body `{"ssoProtection": null, "autoExposeSystemEnvs": false}`.

### 6. Domain ownership (403 Forbidden)
If `GET /v5/domains/{domain}` returns 403, the domain belongs to a different Vercel account/user, not just a different team on the current token.
**Verification:** Check all stored tokens: `grep -r "VERCEL_TOKEN" ~/.hermes/.env`. If all fail, the user must manually remove the domain from the old account.

## References

- `references/access-patterns.md` — full MC_ALLOWED_HOSTS proxy logic and access control
- `references/log-patterns.md` — common Hermes log warnings and their meanings
- `references/fleet-topology.md` — current Appie fleet layout (local vs remote agents)
- `references/session-context-kanban.md` — mirroring session context into MC kanban
- `references/fleet-context-ingestion.md` — fleet-wide context ingestion workflow
- `references/mc-deploy-handoff.md` — MC-1 wave deploy process, branches, access topology, and verification checklist
- `references/mc-feature-roadmap.md` — open features and defects from the July 4 handoff audit
