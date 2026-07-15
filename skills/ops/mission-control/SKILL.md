---
name: mission-control
description: Deploy, configure, and troubleshoot Mission Control (OpenClaw/Appie fleet dashboard). Use when setting up MC, fixing access issues, or managing gateways.
tags: [fleet, dashboard, mission-control, nextjs, deployment]
---

# Mission Control — Fleet Dashboard

Open-source agent orchestration dashboard (Next.js 16). Runs on Mac Mini, accessible fleet-wide via Tailscale.

## Quickstart

```bash
cd /Users/appie/mission-control
pnpm run start --port 3480
```

If `pnpm run start` fails on `verify:node` or `pnpm install` checks, bypass it:
```bash
npx next start --hostname 0.0.0.0 --port 3480
```

## Access

Dashboard: `http://100.101.29.56:3480` (Tailscale IP of Mac Mini)
Default creds: see `references/credentials.md`

## Pitfalls

### 0. AUTH_USER/AUTH_PASS from .env doesn't propagate to database on first run

**Root cause:** Setting `AUTH_USER` and `AUTH_PASS` in `.env` seeds the admin credentials into MC's config but does NOT create a user record in the database. The `/api/login` endpoint checks the DB, not the env vars, so returns 401 even with correct creds.

**Fix:** Visit `http://localhost:3480/setup` in a browser on first run to complete the admin account creation wizard. The env vars only take effect if the setup has already seeded from them — if the setup page was never visited, no DB user exists.

**Workaround (headless):** Post to `/api/setup` endpoint with the same credentials to create the DB record.

### 1. External access returns 403 Forbidden

**Root cause:** `MC_ALLOWED_HOSTS` in `.env` defaults to `localhost,127.0.0.1,::1`. In production (`NODE_ENV=production`), the proxy (src/proxy.ts:163) blocks any host not in the allowlist.

**Fix:** Add Tailscale and local network ranges to `.env`:
```
MC_ALLOWED_HOSTS=localhost,127.0.0.1,::1,100.*,192.168.*
```

Patterns supported: exact match, `*.example.com` (subdomain), `100.*` (prefix wildcard).

**Then restart the server** — `.env` changes are read at startup, not hot-reloaded.

### 2. pnpm verify:node fails

`pnpm run start` runs `verify:node` first which may fail on `pnpm install` checks. Workaround: skip pnpm entirely with `npx next start --hostname 0.0.0.0 --port 3480`.

### 3. Server process not found after restart

Check what's listening:
```bash
lsof -i :3480
```

Find project dir of running process:
```bash
lsof -p <PID> | grep cwd
# or:
ps aux | grep <PID>
# gives path like: /Users/appie/mission-control
```

### 4. DeepSeek models fail on vision/image tools

DeepSeek V4 Pro (and likely other DeepSeek models) return `404 - No endpoints found that support image input`. For vision tasks, use `anthropic/claude-opus-4-6` or another vision-capable model.

## Connecting session tasks/context to Mission Control

Mission Control's agent task surface is the bundled Hermes Kanban dashboard plugin at `/kanban`, backed by `hermes_cli/kanban_db.py`. When Seyed asks to put tasks/context into Mission Control, mirror the active session objective into the Hermes Kanban board rather than only keeping an in-chat todo.

Recommended flow:
1. Inspect boards with `./hermes kanban boards list` from the Hermes Agent repo, or `hermes kanban boards list` if the CLI is on PATH.
2. Create a task with a concise title and rich `--body` containing: user request, current repo/workdir, active goal/session identifier if available, relevant constraints, and a short checklist of mirrored tasks.
3. Use numeric priority values, not labels. Example: `--priority 80`, not `--priority high`.
4. Prefer `--workspace dir:<absolute-path>` when the context belongs to an existing checkout.
5. Verify with `./hermes kanban list` and `./hermes kanban show <task-id>` so Mission Control has the expected body.

Pitfall: `python -m hermes_cli.kanban ...` may have no CLI entrypoint in repo checkouts. Use the Hermes CLI command path instead.

Reference: `references/session-context-kanban.md` has a concrete command template for mirroring session context into Mission Control.

For fleet-wide context ingestion across Appie profiles, use `references/fleet-context-ingestion.md`: it lists authoritative evidence files, card body shape, idempotency keys, and verification steps. Prefer a dedicated board such as `appie-fleet-context` over dumping cross-profile cards into the default board.

## Diagnostics

### Check Diddy/Appie Hermes logs

```bash
# Recent errors
tail -50 ~/.hermes/logs/errors.log
# Gateway errors
tail -20 ~/.hermes/logs/gateway.error.log
# Agent activity
tail -30 ~/.hermes/logs/agent.log
```

Common patterns to watch for:
- `unknown provider 'openai'` — vision provider not configured; falls back to auto
- `No endpoints found that support image input` — current model can't handle images
- `Telegram network error` — connectivity issue (usually transient)
- `Discord RESUMED session` — normal if occasional; if every 2-3h, gateway may be unstable

## References

- `references/access-patterns.md` — full MC_ALLOWED_HOSTS proxy logic and access control
- `references/log-patterns.md` — common Hermes log warnings and their meanings
- `references/fleet-topology.md` — current Appie fleet layout (local vs remote agents)