---
name: openclaw-to-hermes-migration
title: OpenClaw Agent → Hermes Migration Procedure
description: Migrate an agent that currently runs on OpenClaw gateway to Hermes Agent. Covers pre-flight inventory, Hermes install, config, skills migration, faster-whisper/STT, gateway setup, cutover, and verification.
trigger: User asks to 'migrate' an agent from OpenClaw to Hermes, 'switch eugi to Hermes', 'replace OpenClaw with Hermes', or any request to move an existing Telegram/agent bot from OpenClaw to the Hermes framework.
---

# OpenClaw → Hermes Agent Migration

## When to Use

Migrate an existing OpenClaw-gateway agent to Hermes Agent when:
- User says "migrate [agent] to Hermes" or "switch [agent] from OpenClaw"
- Setting up fleet-wide standardization on Hermes
- Retiring OpenClaw instances in favor of the Hermes framework

## Target Machine Profile

The procedure assumes:
- **OS**: Ubuntu 24.04 (or Debian-based Linux) with apt
- **Python**: 3.12 (system) — PEP 668 enforced (use `--break-system-packages` for faster-whisper)
- **Node.js**: Installed (OpenClaw runs on Node.js, but Hermes does not require it)
- **Internet**: Outbound HTTPS access (for Hermes install, PyPI, OpenRouter API, Telegram API)
- **SSH**: Root access from the migrating agent's machine
- **Tailscale**: Installed (100.x.x.x IP)

## Pre-Flight: Inventory OpenClaw Instance

### 1. Check if OpenClaw is running

```bash
ps aux | grep openclaw
```

### 2. Find OpenClaw config and extract bot token

```bash
cat /root/.openclaw/openclaw.json | python3 -m json.tool
```

Key fields to extract:
- `channels.telegram.botToken` — the Telegram bot token (needed for Hermes .env)
- `channels.telegram.allowFrom` — authorized user IDs
- `agents.defaults.model.primary` — current model
- `agents.defaults.userTimezone`

### 3. Check OpenClaw service type

```bash
# Check systemd user service
systemctl --user status openclaw-gateway

# Check if symlinked for auto-start
ls -la /root/.config/systemd/user/default.target.wants/openclaw-gateway.service
```

OpenClaw can be:
- systemd user service (`systemctl --user`)
- systemd system service (`systemctl`)
- Docker container
- Raw process (started manually or via tmux/screen/init.d)

### 4. Check disk space

```bash
df -h /
```

Hermes takes ~500MB-1GB. Ensure at least 5GB free.

### 5. Check Python version

```bash
python3 --version
python3 -c "import sys; print(sys.executable)"
```

Hermes auto-installs its own python if missing, but Python 3.10+ is ideal.

## Step 1: Install Hermes

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"
hermes --version
```

Expected: `Hermes Agent v0.17.0+` (or latest)

Hermes auto-links into `/usr/local/bin/` — no shell reload needed.

## Step 2: Configure Provider

```bash
hermes config set model.default "deepseek/deepseek-v4-flash"
hermes config set model.provider "openrouter"
hermes config set model.context_length 1000000
```

Use OpenRouter + DeepSeek unless the user specifies otherwise. The OpenRouter API key goes in `.env` in Step 3.

### OpenRouter Key Check

Before setting up, verify the OpenRouter key has remaining credits:

```bash
curl -s https://openrouter.ai/api/v1/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" | \
  python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(f'Remaining: \${d[\"limit_remaining\"]:.1f} of \${d[\"limit\"]} monthly')"
```

If remaining < $10/month, warn the user before proceeding.

## Step 3: Set Up Environment (.env)

```bash
cat > /root/.hermes/.env << 'ENVEOF'
OPENROUTER_API_KEY=sk-or-v1-...
TELEGRAM_BOT_TOKEN=<bot-token-from-openclaw-config>
ENVEOF
chmod 600 /root/.hermes/.env
```

- **OPENROUTER_API_KEY**: Use the same key as other Hermes agents (Seyed's account). Get from an existing Hermes `.env`.
- **TELEGRAM_BOT_TOKEN**: Extract from OpenClaw config (`openclaw.json` → `channels.telegram.botToken`)

**Verify .env was written correctly** (mask secrets in output):
```bash
ls -la /root/.hermes/.env
cat /root/.hermes/.env | sed 's/sk-or-v1-[^ ]*/REDACTED/;s/[0-9]*:[A-Za-z0-9_-]*/REDACTED/'
```

## Step 4: Copy Skills from Existing Hermes Instance

From the existing Hermes instance (e.g. Appie-3):

```bash
# On source machine
tar czf /tmp/skills.tar.gz -C /root/.hermes skills/

# Copy to target
scp /tmp/skills.tar.gz root@<target-tailscale-ip>:/tmp/

# On target
mkdir -p /root/.hermes/skills
tar xzf /tmp/skills.tar.gz -C /root/.hermes/
rm /tmp/skills.tar.gz

# Verify
find /root/.hermes/skills -name 'SKILL.md' | wc -l
```

Expected: 100+ skills (Appie-3 has ~104 as of 2026-06-21).

## Step 5: Install Hub Skills (Optional "Up-Heat Kit")

```bash
hermes skills install github-code-review
hermes skills install web-research
```

These skills fail if the hub name doesn't match exactly. Check available skills with `hermes skills search <keyword>`. Non-critical — the copied skills from Step 4 cover most functionality.

## Step 6: Install faster-whisper (Voice STT)

Ubuntu 24.04 has PEP 668 — must use `--break-system-packages`:

```bash
pip3 install faster-whisper --break-system-packages
python3 -c 'import faster_whisper; print("faster-whisper OK:", faster_whisper.__version__)'
```

Expected: `faster-whisper OK: 1.2.1+`

## Step 7: Configure STT + Gateway Settings

```bash
# Enable local STT with faster-whisper
hermes config set stt.enabled true
hermes config set stt.provider local

# Enable Telegram features
hermes config set telegram.reactions true
hermes config set telegram.extra.rich_messages true
```

## Step 8: Install Gateway Service

```bash
yes | hermes gateway install
```

This installs a systemd user service and asks two yes/no questions. `yes` pipe auto-answers both.

Verify:
```bash
hermes gateway status
```

Expected: `Active: active (running)`, `Main PID: <pid> (hermes)`

## Step 9: Verify Telegram Connection

Check gateway logs for successful Telegram connection:

```bash
tail -10 /root/.hermes/logs/gateway.log
```

Expected lines:
```
[Telegram] set_my_commands OK for scope BotCommandScopeAllPrivateChats (30 cmds)
[Telegram] Connected to Telegram (polling mode)
Gateway running with 1 platform(s)
```

### Polling Conflict

If OpenClaw was still running when Hermes started, you'll see:

```
[Telegram] Telegram polling conflict (1/5) — previous session still held open...
```

This auto-resolves within 30 seconds once OpenClaw is stopped. If it persists, force-stop OpenClaw.

## Step 10: Stop and Disable OpenClaw

```bash
# Stop the service
systemctl --user stop openclaw-gateway

# Disable auto-start
systemctl --user disable openclaw-gateway

# Verify it's dead
systemctl --user status openclaw-gateway
# Expected: Active: inactive (dead); Loaded: ... disabled

# Kill any remaining OpenClaw processes
pkill -f 'openclaw-gateway' 2>/dev/null || true
```

**Important**: `kill` or `pkill` may terminate the SSH session if matching patterns overlap (e.g. `pkill -f openclaw` matching an SSH command). Use `systemctl --user stop` as the primary method. Only use `pkill` as fallback in a separate unprivileged command.

## Step 11: Final Verification

```bash
# 1. Only Hermes should be running
systemctl --user list-units --type=service --state=running | grep -E 'hermes|openclaw'
# Expected: hermes-gateway only

# 2. Telegram API responds
curl -s "https://api.telegram.org/bot$(grep TELEGRAM_BOT_TOKEN /root/.hermes/.env | cut -d= -f2)/getWebhookInfo" | python3 -m json.tool
# Expected: {"ok": true, "result": {"url": "", ...}}

# 3. Gateway is active and wasn't restarted by OpenClaw interference
hermes gateway status | grep Active
# Expected: active (running) since ... (match current time)

# 4. Disk after install
df -h /
```

## Rollback Plan

If Hermes doesn't work:

```bash
# 1. Stop Hermes
systemctl --user stop hermes-gateway
systemctl --user disable hermes-gateway

# 2. Restart OpenClaw
systemctl --user start openclaw-gateway
systemctl --user enable openclaw-gateway

# 3. Delete Hermes config (optional)
rm -rf /root/.hermes
```