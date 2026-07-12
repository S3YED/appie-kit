---
name: appie-self-maintenance
title: Appie Fleet Maintenance & Troubleshooting
description: Healthchecks, SSH access, model switching, and systemd debugging for the Appie fleet. Covers Appie-2 (Hetzner Hermes) and common failure modes.
---

## Opus Crash Loop Fix (Appie-1)
The Opus supervisor (`~/bin/appie-1-brain-start.sh`) was causing ~15min crash loops because `tmux_server_alive()` returned false negatives during Claude mid-generation. Fix:

1. Health check: check `claude_alive` FIRST. If Claude process is alive, skip tmux probe entirely.
2. `tmux_server_alive()` timeout increased from 3×1s to 10×2s (20s total).
3. Transient-spike guard at top of recovery section: `if claude_alive; then exit 0; fi`

## Appie Opus Token Rotation
Bot token goes in TWO places:
- `~/.weblyfe-secrets/telegram-bot.env` (env var for start script)
- `~/.claude/channels/telegram/.env` (channel plugin reads here)
BOTH must be updated on token rotation.

## Purpose

Maintain and troubleshoot the Appie Hermes agent fleet. Documents how to reach each agent, common failure modes, diagnostic commands, and proven fixes.

## Appie/Hermes self-scan

When Seyed asks for a scan/analyse of Appie, Hermes, gateway health, or the local agent runtime, use `references/hermes-self-scan.md` for the read-only checklist and reporting style. Key reminders:

- Return the final scan only, no tool-call play-by-play.

## Telegram bridge healthcheck (Appie Opus / Claude Code bots)

Appie Opus runs in tmux via the supervisor. The Telegram bridge is a `bun server.ts` subprocess of Claude Code's channel plugin. Three failure modes:

1. **Bridge process alive but not polling** — `lsof` shows the process exists but no ESTABLISHED connection to `149.154.166.110:443`. The supervisor's `telegram_alive()` check was upgraded from "process exists" to "ESTABLISHED TCP connection via `lsof -i -p $bridge_pid | grep 149.154.*ESTABLISHED`".

2. **`.env` token file emptied** — `~/.claude/channels/telegram/.env` can become empty (0 bytes). Recovery: restore from `.env.bak-*` or from `~/.weblyfe-secrets/telegram-bot.env`. The bridge loads the token on startup; if the file is empty at launch, the bridge exits immediately.

3. **Healthcheck restart loops** — Too many layers (supervisor + watchdog + cronjob) can create a vicious cycle where each layer detects "unhealthy" and restarts before the bridge has time (30-90s) to establish a connection. Fix: supervisor handles restarts (every 15s with 90s grace period); watchdog and cronjob must be **alert-only** (detect + log, no restart).

### Healthcheck script

`~/bin/appie-1-telegram-health.sh` — 3-level deep check:
- Level 1: bridge process alive (kill -0 on bot.pid)
- Level 2: ESTABLISHED TCP connection to Telegram API (`lsof -i -p $PID | grep 149.154.*ESTABLISHED`)
- Level 3: API-level canary (`curl bot${TOKEN}/getMe` returns HTTP 200)

Pass `--restart` to auto-kill the tmux session on failure (for the supervisor). Without `--restart`, it's alert-only (log + exit non-zero).

### 3-layer architecture

| Layer | Mechanism | Interval | Role |
|---|---|---|---|
| Supervisor | launchd `appie-1-supervisor.sh` | ~15s | **Restarts** — deepened `telegram_alive()` checks ESTABLISHED connection |
| Watchdog | launchd `com.weblyfe.appie-1-telegram-watchdog` | 2 min | **Alert-only** — runs healthcheck, logs to file, no restart |
| Cron | Hermes cronjob `appie-1-telegram-health-alert.sh` | 5 min | **Alert-only** — same check, delivers notification if persistent failure |

Pitfall: no_agent cronjobs with `script` parameter do NOT support arguments (script + args is treated as a single filename). Use a wrapper script that hardcodes the args.

## Cronjob reliability

### no_agent cron scripts

When using `cronjob(action='create', no_agent=True, script='...')`, the `script` value must be a filename relative to `~/.hermes/scripts/`. Arguments appended to the filename string are treated as part of the filename. To pass arguments, create a wrapper script in `~/.hermes/scripts/` that calls the real script with the desired arguments.

### Security scan (launchd)

The security scan at `~/clawd/tools/security-scan.sh` can hang on step 2 (hardcoded secrets grep) if it searches through `node_modules/` or `.next/` directories. Fix: use `--exclude-dir=` flags instead of piped `grep -v`:

```bash
grep -r -l --include="*.ts" --include="*.js" \
    --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.git \
    -E "(pattern)" "$SCAN_DIR" 2>/dev/null | head -10
```

Also avoid `set -e` in monitoring scripts — one transient failure kills the whole scan. Use `set -uo pipefail` instead.

## Claude Code Telegram Bridge Reliability

When diagnosing a Claude Code agent that uses `--channels plugin:telegram@claude-plugins-official` and has stopped replying:

- The Telegram bridge (`bun server.ts`) can lose its polling connection while the process stays alive. A running process does NOT mean working messages.
- See `references/telegram-bridge-healthcheck.md` for the full diagnostic pattern, 3-level healthcheck (process → TCP → API), and the recovery architecture (supervisor + cron + launchd).
- Treat multiple launchd gateways as a topology decision first, not an automatic bug.
- Check skill-name collisions because duplicate skills can make `skill_view("name")` fail. Retry with categorized paths when ambiguity appears.
- Check compression/model warnings in logs, not just `hermes status`.
- Report risky host posture such as FileVault off, public `*:3000` listeners, or long-running sync jobs, but do not change/kill anything without explicit approval.

## Appie-1 Claude Code brain diagnostics

When Seyed asks whether the Appie-Opus / Appie-1 brain is fixed, remember it is Claude Code in tmux, not a Hermes profile. For the stuck Telegram symptom where typing/activity appears but no final response is delivered, use `references/appie-opus-telegram-stuck-turn.md` before restarting the whole brain.

When Seyed asks whether the Appie-Opus / Appie-1 ...

Key durable signatures:
- `Could not resolve authentication method. Expected either apiKey or authToken to be set.` means Claude launched but has no usable OAuth/API auth. Not a crash.
- `Plugin telegram not found in marketplace claude-plugins-official` is a secondary bridge/tooling issue unless auth is healthy.
- `~/bin/appie-1-brain-start.sh` intentionally runs Claude with `env -u ANTHROPIC_API_KEY`; if OAuth is missing, the brain becomes alive-but-unusable.
- A pane message like `Claude Fable 5 is currently unavailable. Please use Opus 4.8 or another available model.` means the brain is alive but pinned to an unavailable model. Patch the launcher to a known available model, kill the bad tmux session, restart, then verify the new process command line and pane banner.
- Also check `~/.claude/settings.json`: Claude Code can keep a global `"model": "fable"` even after `~/bin/appie-1-brain-start.sh` is fixed. Set it to `"claude-opus-4-8"` or another known-available model before recycling Appie-Opus.
- Before restarting Appie-Opus, verify the live tmux socket/session and process command line. If `claude --model claude-opus-4-8 --channels plugin:telegram@claude-plugins-official` is already running and the Telegram bridge child is alive, do not recycle the session just because stale comments or old notes mention another model. Patch stale launcher comments/docs only.
- Run `bash -n ~/bin/appie-1-brain-start.sh` before restart, and guard manual/supervisor races with a start lock if tmux startup becomes flaky.

Pitfall: an Appie brain can be alive in tmux and still reply to every Telegram message with the same provider/model error. Always capture the pane before assuming overload or gateway failure. Also avoid the opposite mistake: if the live process is healthy, do not restart it unnecessarily. `/start` and `/help` are Telegram plugin commands, so they show pairing/help text even for an allowlisted user; test responsiveness with normal text like `Appie`, not `/start`.

## Mac Mini fleet audit

- Use `references/mac-mini-fleet-audit.md` when Seyed asks to check cron jobs, local device/service health, Appie-1/Appie3/Appie4 status, appie-brain security, or cleanliness on the Mac Mini.
- Audit read-only first. Do not disable LaunchAgents, delete clutter, rotate secrets, or rewrite configs without explicit approval.
- Timestamp log findings before treating them as current; stale stderr can look like an active failure after the issue was already repaired.

## Tailscale reachability

- Use `references/tailscale-reachability.md` for the repeatable pattern where Tailscale shows a peer as online but TCP 22 still times out.
- If the local client looks stale after a restart or network change, run `tailscale up` before deeper debugging.

## Content boundary: appie-brain vs appie-kit

- Keep NSFW or adult-course material in `appie-brain` only, never in `appie-kit`.
- Appie-Opus follows the same separation.
- See `references/appie-brain-vs-kit.md` for the concise handling rule.

## Appie-2 gateway recovery

- Use `references/appie-2-gateway-recovery.md` for the repeatable path when Appie-2 needs SSH cleanup, service recovery, or persistent gateway hardening.
- Use `references/appie-2-gateway-freeze-recovery.md` when the gateway is running but frozen (300-500% CPU, unresponsive to Telegram, no health endpoint response). Recovery: `kill -9 <PID>` — systemd auto-restarts.
- Prefer the Tailscale DNS hostname in SSH config when the host is already on tailnet.
- Treat `hermes gateway install --system` as a system-service operation and pass `--run-as-user root` when the install flow is running as root in a container-style environment.

## Fleet Overview (May 2026)

**Seyed's fleet:**
| Agent | Host | Type | Provider | Status |
|-------|------|------|----------|--------|
| **Appie** (Appie-1) | Seyed's Mac Mini | Hermes Agent | OpenRouter | Primary |
| Appie-2 | Hetzner VPS | Hermes Agent | OpenRouter | Worker |
| Appie-3/4 | Seyed's Mac Mini (planned) | Hermes Agent | — | Not yet |
| Spark Atlas | DGX | Hermes Agent | — | Tailscale |

**Client bots (NOT Appie fleet — separate machines):**
| Agent | Host | Type | Key | Notes |
|-------|------|------|-----|-------|
| Diddy | Harry's Mac Mini (`wolf-diddy.tail43b300.ts.net`) | Hermes Agent | Harry's OpenRouter | Separate machine, separate Tailscale account (`diddywolfpack888@`), separate OpenRouter key. Do NOT use Seyed's keys here. |

**⚠️ IDENTITY PITFALL: Appie is NOT Diddy.** Appie runs on Seyed's Mac Mini. Diddy runs on Harry's Mac Mini — a completely separate machine, separate OpenRouter key, separate Tailscale account. Never refer to yourself as Diddy. Never confuse the two. This error has been corrected multiple times.

## Key Management: Client Bot Isolation (CRITICAL)

**Every Hermes agent must use its own API key. Client bots must NEVER use Seyed's keys.**

- **Appie** (Seyed's Mac Mini): Seyed's OpenRouter key `sk-or-v1-48c1c2a59ce...`
- **Appie-2** (Hetzner): Seyed's secondary OpenRouter key `sk-or-v1-02902735...`
- **Diddy** (Harry's Mac Mini): **Harry's own key** `sk-or-v1-ee6fbe23...` — a separate OpenRouter account
- **Never copy Seyed's key to Diddy.** Never copy Diddy's key to Appie. Each agent gets its own.
- When repairing a client bot, ask the client to provide their own API key. Do NOT reuse Seyed's key as a "temporary fix."

**How to check which key an agent is using:**
```bash
# On the agent, check the .env file
grep OPENROUTER ~/.hermes/.env

# Verify key identity via OpenRouter API
curl -s https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer <KEY>" | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(f'Limit: \${d[\"limit\"]}, Remaining: \${d[\"limit_remaining\"]:.2f}')"
```

## Appie-2 Access

- **Public IP:** `178.104.154.117` (Hetzner Cloud)
- **Tailscale IP:** `100.118.143.10` (hostname: `appie-2-hermes`)
- **SSH:** `root@178.104.154.117` (key `~/.ssh/id_ed25519`). Use PUBLIC IP - Tailscale SSH may be blocked by firewall/iptables even when the box is online on tailnet.
- **SSH via Tailscale IP may fail** (Connection refused on port 22) even when public IP works. This is normal - iptables blocks Tailscale interface on port 22.
- **Hetzner Server ID:** `126240194`
- **Hetzner API Key:** in `~/clawd/.env.secrets` as `HETZNER_API_KEY`
- **Root password:** reset via Hetzner API -> `curl -s -H "Authorization: Bearer $HETZNER_API_KEY" -X POST "https://api.hetzner.cloud/v1/servers/126240194/actions/reset_password"`
- **Config:** `/root/.hermes/config.yaml`
- **Logs:** `/root/.hermes/logs/gateway.log`, `errors.log`
- **Model:** `openrouter/anthropic/claude-sonnet-4` (switched from Codex due to OAuth rate-limit)
- **Approvals:** `auto` (both `approvals.mode` and `approvals.cron_mode`)

## Spark Atlas Codex OAuth

- Spark uses `admin@100.69.197.43` via the SSH host `spark`.
- Hermes is installed at `/home/admin/.local/bin/hermes`.
- `hermes auth status openai-codex` can be logged in while the same account still rejects unsupported model slugs.
- For this account, `model.provider: openai-codex` plus `model.default: gpt-5.4` worked.
- `gpt-5` returned HTTP 400 on the Codex ChatGPT account.
- If Spark still shows a stale `model.base_url: http://127.0.0.1:8000/v1`, remove it before testing Codex.
- Verification recipe lives in `references/spark-codex-oauth.md`.

## Wolfie / OpenClaw routing

- Wolfie is Harry's Mac mini on Tailscale: `wolf-diddy.tail43b300.ts.net` / `100.102.181.116`.
- If SSH times out, check Tailscale status first. Offline host is not the same thing as broken SSH config.
- When the host is back, inspect the local OpenClaw config before editing assumptions. The layout may be `~/.openclaw/openclaw.json` or `~/.openclaw/config/agents/main/auth.json` depending on install history.
- Desired policy for this box: GPT OAuth primary, direct MiniMax M2.7 fallback, no Claude or Anthropic routed through OpenRouter.
- Use `references/wolfie-openclaw-routing.md` for the session checklist and model policy.

## Diagnostic Commands (run via SSH)

```bash
# Is gateway running?
ps aux | grep 'hermes.*gateway' | grep -v grep

# Auth status — shows rate limits!
hermes auth list

# Specific provider auth
hermes auth status openai-codex
hermes auth status openrouter

# Model config
grep -A3 '^model:' /root/.hermes/config.yaml

# Recent errors
tail -50 /root/.hermes/logs/errors.log

# Gateway log
tail -30 /root/.hermes/logs/gateway.log

# Find systemd hermes units
find /etc/systemd /usr/lib/systemd /root/.config -name '*hermes*' -type f 2>/dev/null

# Check listening ports
ss -tlnp | grep 1877
```

## Common Failure Mode: Systemd Restart Loop

**Symptoms:** Gateway starts, prints "Hermes Gateway Starting..." banner, immediately shuts down with SIGTERM. Port 18777 never opens. `ps aux` shows a hermes gateway process but it keeps cycling.

**Root cause:** A systemd user service at `/root/.config/systemd/user/hermes-gateway.service` with `Restart=always` keeps restarting the gateway with the OLD config/model. Each restart kills any manually-started gateway via `--replace` takeover.

**Diagnosis:** Check logs for repeated "Shutdown context: signal=SIGTERM under_systemd=yes" entries.

**Fix:**
1. Find unit files: `find /etc/systemd /usr/lib/systemd /root/.config -name '*hermes*' -type f 2>/dev/null`
2. Remove them directly: `rm /root/.config/systemd/user/default.target.wants/hermes-gateway.service && rm /root/.config/systemd/user/hermes-gateway.service`
3. Kill all gateway processes: `pkill -9 -f 'hermes.*gateway'`
4. Start fresh: `hermes gateway run --replace`

**DO NOT use `systemctl`** — it hangs because SSH sessions lack D-Bus.

## Common Failure Mode: Codex OAuth Rate Limit (429) → Hard Block (403)

**Symptoms:** Gateway starts but API calls fail with HTTP 429. `hermes auth list` shows `rate-limited (429) (XXh left)` on Codex credentials.

**Severe case (403):** When rate limit is extreme, OpenAI blocks new device code requests entirely:
```
hermes_cli.auth.AuthError: Device code request returned status 403.
```
This is an IP-level block that clears when the rate limit expires.

**Spark-specific Codex note:** For ChatGPT Codex OAuth, the model slug must match the allow-list accepted by the endpoint.
- `gpt-5` was rejected on Spark with HTTP 400.
- `gpt-5.4` worked.
- Set `model.context_length` to `272000` for the Codex OAuth path.

**Fix:**
1. Check rate limit: `hermes auth list`
2. If rate-limited with hours left, switch to OpenRouter:
   ```bash
   hermes config set model.default openrouter/anthropic/claude-sonnet-4
   hermes config set model.provider openrouter
   ```
3. Kill and restart gateway (see systemd loop fix above if needed)
4. Switch back to Codex when rate limit clears: `hermes config set model.provider openai-codex`
5. **Do NOT try `hermes auth add openai-codex` while 403 is active** — it won't work. Wait for the rate limit timer to expire.
   - See `references/codex-403-hard-block.md` for the full progression from 429 → 403 and recovery steps.
   - See `references/spark-codex-gateway-quirks.md` for the Spark-specific model/context and startup quirks.

### Codex Rate-Limit Timing Ambiguity

`hermes auth list` shows a cached/estimated cooldown timer (`XXm YYs left`) that can disagree with the real OpenAI cooldown. A credential showing `429 (rate-limited)` with a few minutes left may actually be usable now if the real cooldown has already expired — the displayed timer is an estimate from when the 429 was received, not a live refresh from OpenAI. When in doubt, `hermes config set model.default openai-codex` + `hermes config set model.provider openai-codex`, start a session, and see if it works rather than waiting for the displayed countdown to hit zero.

## Gateway startup: missing platform dependencies

Sometimes `hermes gateway restart` fails because the service venv is missing a platform dependency even though `hermes doctor` looks mostly healthy.

**Observed on Spark:**
- The gateway refused to start because `python-telegram-bot` was missing in `~/.hermes/hermes-agent/.venv`.
- That venv had `python` but no `pip`, so bootstrap required `python -m ensurepip` first.

**Recovery sequence:**
```bash
~/.hermes/hermes-agent/.venv/bin/python -m ensurepip --upgrade
~/.hermes/hermes-agent/.venv/bin/python -m pip install --upgrade pip
~/.hermes/hermes-agent/.venv/bin/python -m pip install python-telegram-bot
```

**Then:**
- rerun `hermes gateway restart`
- confirm `hermes gateway status` is active

**Related startup pitfall:** If the SMS adapter is enabled but neither `SMS_WEBHOOK_URL` nor `SMS_INSECURE_NO_SIGNATURE=true` is set, the gateway refuses to boot. For local/dev recovery, `SMS_INSECURE_NO_SIGNATURE=true` is the fast unblocker, but it should not be used for production.

## Running Interactive Commands via SSH (TTY-Required)

Some Hermes commands (`hermes model`, `hermes auth add openai-codex`) require a TTY and refuse to run via pipes. Use `script` to fake one:

```bash
# Run interactive command via SSH with fake TTY
ssh root@HOST "script -q -c 'timeout 60 hermes auth add openai-codex' /dev/null 2>&1"
```

This prints the device code URL + code, then polls for completion. The `timeout` prevents indefinite hanging if user doesn't complete the flow in time.

## Fleet Standard: Approvals Auto

All Hermes agents should have approvals set to `auto`:
```bash
hermes config set approvals.mode auto
hermes config set approvals.cron_mode auto
```

This prevents approval prompts during fleet operations (killing processes, deleting files, SSH access). Set this on every agent during initial setup.

## Hetzner API Quick Reference

```bash
HETZNER_KEY="CarUgCobx0MQGN77G1TwEwz9i9Lyri9zhqosjwVCWSU76EutvCACnrE2PLLLmWys"

# List servers
curl -s -H "Authorization: Bearer $HETZNER_KEY" "https://api.hetzner.cloud/v1/servers"

# Server details
curl -s -H "Authorization: Bearer $HETZNER_KEY" "https://api.hetzner.cloud/v1/servers/126240194"

# Reboot
curl -s -H "Authorization: Bearer $HETZNER_KEY" -X POST "https://api.hetzner.cloud/v1/servers/126240194/actions/reboot"

# Reset root password (returns new password + triggers reboot)
curl -s -H "Authorization: Bearer $HETZNER_KEY" -X POST "https://api.hetzner.cloud/v1/servers/126240194/actions/reset_password"
```

### tmux / interactive agent hangs

When a Claude Code or Hermes-like agent looks unresponsive but the process is still alive, inspect the tmux pane before restarting anything.

- Capture the pane first so you can see whether the session is stuck in a modal prompt or long self-audit loop.
- If the pane shows a prompt like `What should Claude do instead?`, send `Esc` to close the modal.
- If it is still wedged, send `Ctrl+C` to interrupt the current loop.
- Re-capture the pane after a short wait and only restart if it is still blocked.
- Reference: `references/tmux-hung-claude-recovery.md`.

## What to Check When an Agent Is Unresponsive

1. **Is the host online?** `tailscale status` - check Peer Online field
2. **Can you SSH?** Try public IP first, then Tailscale IP
3. **Is Hermes running?** `ps aux | grep hermes`
4. **Is the model provider healthy?** `hermes auth list` - check for rate limits, expired OAuth
5. **Is systemd interfering?** Check logs for repeated shutdowns
6. **Last resort:** Reboot via Hetzner API, then start gateway manually after removing systemd units

## Mission Control Debugging

Mission Control is the fleet orchestration dashboard (`/Users/appie/mission-control`, Next.js). Common issues:

### 403 Forbidden from external clients

**Symptom:** Accessing Mission Control from another machine (MacBook Pro) returns `403 Forbidden`.

**Root cause:** Production mode (`NODE_ENV=production`) default-denies all hosts unless `MC_ALLOWED_HOSTS` or `MC_ALLOW_ANY_HOST` is set. The proxy layer (`src/proxy.ts:163`) enforces this:
```ts
const allowAnyHost = envFlag('MC_ALLOW_ANY_HOST') || process.env.NODE_ENV !== 'production'
```

**Fix:**
```bash
# Edit .env and add Tailscale + LAN ranges:
MC_ALLOWED_HOSTS=localhost,127.0.0.1,::1,100.*,192.168.*

# Restart:
kill $(lsof -ti :3480)
cd /Users/appie/mission-control && npx next start --hostname 0.0.0.0 --port 3480 &
```

### pnpm start fails with install check error

**Symptom:** `pnpm run start` fails with `Command failed with exit code 1: pnpm install` before Next.js even starts.

**Root cause:** `pnpm run start` chains `verify:node && next start`. The `verify:node` script triggers a pnpm dependency check that fails in some environments.

**Workaround:** Bypass pnpm entirely — use `npx next start` directly:
```bash
cd /Users/appie/mission-control && npx next start --hostname 0.0.0.0 --port 3480 &
```

**Credentials** (set on first `/setup`):
- User: `admin`
- Pass: `9qF2b3DUndj2h1ofdFYHSGlW`
- API Key: `ab28a9a4c384a9d807136506b8285c0e`

Appie-1's Hermes logs live on the Mac Mini itself:

```bash
# Recent errors (vision failures, provider issues, network outages)
tail -50 ~/.hermes/logs/errors.log

# Gateway errors only
tail -20 ~/.hermes/logs/gateway.error.log

# Agent activity + session lifecycles
tail -30 ~/.hermes/logs/agent.log

# Gateway full log (high volume — grep for specific patterns)
grep -iE 'error|warn|fail|crash|timeout' ~/.hermes/logs/gateway.log | tail -30
```

### Common Warning Patterns

| Pattern | Meaning | Severity | Fix |
|---------|---------|----------|-----|
| `unknown provider 'openai'` | Vision provider `openai` not in config.yaml; falls back to auto | 🟡 Low | Add OpenAI provider or switch vision to `anthropic` |
| `Vision provider openai unavailable, falling back to auto vision backends` | Same as above — auto fallback works but with non-vision model | 🟡 Low | Configure a vision-capable model |
| `No endpoints found that support image input` / `404` | Current model (e.g. DeepSeek V4 Pro) doesn't support images | 🔴 Medium | Switch to `anthropic/claude-opus-4-6` for vision tasks |
| `Telegram network error, scheduling reconnect` | `api.telegram.org` unreachable — usually transient ISP issue | 🟢 Info | Self-healing; check if persists >10 min |
| `Discord RESUMED session` every 2-3 hours | Gateway session unstable — may indicate memory/resource pressure | 🟡 Low | Monitor; restart gateway if accompanied by dropped messages |

### OpenAI API 421 Block

**Symptom:** `curl api.openai.com` returns `421 Misdirected Request`. The HTTP 421 status means OpenAI is refusing to serve this client on this endpoint — typically an IP/region-level block, not a rate limit.

**Context:** Appie-1 (Mac Mini) hits this. It's a network-level block, not an auth issue. Codex OAuth flows that depend on reaching OpenAI endpoints will fail from this machine. Workaround: use OpenRouter as the main provider (already configured), and use OpenRouter-proxied models for any task that needs OpenAI models.

## Google OAuth Multi-Account Keepalive

When setting up Google Workspace (Gmail/Calendar/Drive) access for fleet agents, Testing-mode OAuth refresh tokens expire after 7 days of inactivity. Solution: daily token refresh cron.

### Per-Account Credential Files

Store each account's OAuth client + refresh token in `~/.weblyfe-secrets/<label>_token.json`:
- `reyed_token.json` — seyed@weblyfe.nl (client REDACTED-PROJECT-NUMBER-...)
- `weblyfenl_token.json` — weblyfenl@gmail.com (client 921873183075-...)
- `abdullah_token.json` — abdullah0hosseini@gmail.com (client 420184674172-...)

### Daily Refresh Script

Script at `~/.hermes/scripts/token-keepalive.py`:
1. Reads each token file
2. Refreshes access token via OAuth2
3. Touches Gmail API to keep refresh token active
4. Updates stored refresh token if Google rotated it

Set up as no_agent cron:
```bash
cronjob action=create name="Google Token Keepalive" schedule="0 12 * * *" script=token-keepalive.py no_agent=true
```

### OAuth Flow Pattern

1. Create Desktop App OAuth client in GCP Console
2. Set to Testing, add email as test user
3. Generate link with `access_type=offline` and needed scopes
4. User opens on phone, sends callback URL
5. Exchange code via token endpoint
6. Save refresh token to credential file

### API Key Masking Workaround

Hermes masks sensitive values (`***`, `...`) in terminal output AND when writing files. The actual bytes ARE correct — verify with `xxd /path/to/file | head -3`. When deploying with masked tokens, read from `.env.secrets` via Python and pass to `subprocess.run()` instead of inline shell.

## Post-Fix Verification

```bash
# Gateway running?
ps aux | grep 'hermes.*gateway' | grep -v grep

# Model correct?
grep -A3 '^model:' /root/.hermes/config.yaml

# Approvals correct?
grep -A4 '^approvals:' /root/.hermes/config.yaml

# Recent logs clean?
tail -10 /root/.hermes/logs/gateway.log | grep -i error

# No systemd units lingering?
find /root/.config/systemd -name '*hermes*' -type f 2>/dev/null
```

## OpenClaw → Hermes Workspace Migration

When migrating from an old OpenClaw/Clawd workspace to the Hermes workspace, copy these directories:

```bash
# Essential identity docs
cp ~/clawd/{IDENTITY,USER,PERSONAL,APPIE-DNA,HEARTBEAT,TOOLS,SKILLS-INDEX,VERSIONS,AGENTS}.md ~/.hermes/docs/

# Projects (can be large — use rsync)
rsync -a ~/clawd/projects/ ~/.hermes/projects/

# Skills from old workspace
rsync -a ~/clawd/skills/ ~/.hermes/skills-imported/

# Memory, scripts, knowledge
rsync -a ~/clawd/memory/ ~/.hermes/memory/
rsync -a ~/clawd/scripts/ ~/.hermes/scripts/
rsync -a ~/clawd/knowledge/ ~/.hermes/knowledge/
rsync -a ~/clawd/tasks/ ~/.hermes/tasks/
rsync -a ~/clawd/content/ ~/.hermes/content/
rsync -a ~/clawd/research/ ~/.hermes/research/

# Agent persona configs (Appie-3 CTO, Appie-4 CFO)
cp -r ~/clawd/appie-3-cto/ ~/.hermes/appie-3-cto/
cp -r ~/clawd/appie-4-cfo/ ~/.hermes/appie-4-cfo/

# Secrets (import only — keep as reference, use ~/.hermes/.env as canonical)
cp ~/clawd/.env.secrets ~/.hermes/.env.secrets.imported

# Security, directives, alerts
rsync -a ~/clawd/security/ ~/.hermes/security/
rsync -a ~/clawd/directives/ ~/.hermes/directives/
rsync -a ~/clawd/alerts/ ~/.hermes/alerts/
```

**After migration:** Keep `~/clawd/` as backup until verification is complete. Update SOUL.md to reference Hermes paths. Update memory entries with new fleet structure.

## Fleet Topology

| Agent | Location | Role |
|---|---|---|
| Appie-1 | Mac Mini | Primary Hermes agent |
| Appie-2 | Hetzner 178.104.154.117 | CMO/Herald (+ Neo4j) |
| Appie-3 | Hetzner 46.225.233.232 | CTO/DevOps |
| Appie-4 | Mac Mini (~/.hermes-appie4/) | CFO/Business Intelligence |
| Appie-5 | tmux on Appie-2 | Claude Code + Telegram |

**Appie-4 is NOT on Hetzner** — it's a separate Hermes profile on the same Mac Mini as Appie-1.

### Appie-5 TUI Trap
Appie-5 runs as `claude --channels plugin:telegram --dangerously-skip-permissions` in tmux. Its TUI menus (select prompts, numbered choices) are **invisible** over Telegram. The user sees nothing and the session appears stuck. Fix: kill the stuck process and restart with an instruction to never use TUI menus. Add to `~/.claude/claude.md` on Appie-2:
```
Never use interactive TUI menus. The user communicates via Telegram and cannot see terminal UI. Use plain text questions only.
```

- **Persistent Memory Limit:** 2,200 characters. Consolidate when full.
- **Fleet memory entries:** Keep fleet info compact — one entry for all agents.
- **SSH entries in memory blocked:** Don't store IPs with "ssh_access" patterns.
