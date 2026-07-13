---
name: client-orgo-provisioning
description: "Provision a Weblyfe client bot from scratch: Orgo machine + Hermes + GitHub deploy keys + Telegram gateway."
version: 1.0.0
---

# Client Orgo Provisioning

End-to-end provisioning of a Weblyfe client bot on an Orgo-managed machine with Hermes Agent, Telegram gateway, and GitHub deploy access.

## Triggers

- "Set up [client name]'s bot"
- "Provision [client] on Orgo"
- "Check [client]'s orgo bot"
- Any new Weblyfe client needs their own Hermes agent

## Prerequisites

Before starting, gather ALL secrets. Use a dedicated Python script that reads from all relevant env files:

```python
secrets = {}
for env_file in ["~/.weblyfe-secrets/.env",
                  "~/.weblyfe-secrets/orgo-openrouter-keys.env",
                  "~/.weblyfe-secrets/bot-provisioning-pool.env"]:
    path = os.path.expanduser(env_file)
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Handle 'export KEY="value"' format
                    if line.startswith('export '):
                        line = line[7:]
                    if '=' in line:
                        k, v = line.split('=', 1)
                        v = v.strip().strip('"').strip("'")
                        secrets[k.strip()] = v
```

Key sources:
- Master Orgo API key: `ORGO_API_KEY` from `~/.weblyfe-secrets/.env` (uses `export` prefix)
- Client Orgo API key: `ORGO_APPIE<N>_<NAME>` from `~/.weblyfe-secrets/orgo-openrouter-keys.env`
- Client Telegram bot token: `BOT_APPIE<N>_TOKEN` from `~/.weblyfe-secrets/bot-provisioning-pool.env`
- OpenRouter API key: `OPENROUTER_API_KEY` from `~/.weblyfe-secrets/.env` (uses `export` prefix)
- Vercel token if needed: `VERCEL_TOKEN` from `~/.weblyfe-secrets/.env`
- Bot assignment mapping: `~/.weblyfe-secrets/bot-provisioning-ledger.json`

## Workflow

### 1. Discover the Orgo computer

Orgo computer IDs are NOT stable across rebuilds. If a previous session had an ID, it's likely stale.

```bash
# First, list projects to find the client project
python3.11 -c "
import urllib.request, json, os
# Read master key
with open(os.path.expanduser('~/.weblyfe-secrets/.env')) as f:
    for line in f:
        if line.startswith('export ORGO_API_KEY='):
            key = line.split('=',1)[1].strip().strip('\"').strip(\"'\")
            break
# GET projects
req = urllib.request.Request('https://www.orgo.ai/api/projects', headers={
    'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as r:
    print(json.dumps(json.loads(r.read()), indent=2))
"
```

Look for the client's project. Nathan's project: `7a945fac-1f84-44af-aec9-87a462065878`.

**Critical**: The only working way to get a computer ID is to create one via POST. Use `workspace_id` + `name`:

```bash
curl -s -X POST https://www.orgo.ai/api/computers \
  -H "Authorization: Bearer $ORGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"workspace_id": "PROJECT_ID", "name": "list"}'
```

This returns 201 with the computer object including `id`. Save this ID.

### 2. Execute commands on Orgo

```python
url = f"https://www.orgo.ai/api/computers/{computer_id}/bash"
req = urllib.request.Request(url,
    data=json.dumps({"command": cmd}).encode(),
    method="POST",
    headers={"Authorization": f"Bearer {master_key}", "Content-Type": "application/json"})
```

Timeout is 60s default — bump to 180-300 for apt-get/npm install. Expect 504 for slow network operations (Orgo Fly.io machines have limited bandwidth).

### 3. Install base packages

```bash
apt-get update -qq && apt-get install -y -qq openssh-client git curl
```

Minimum: openssh-client (for GitHub deploy keys), git (for repo access), curl.

### 4. Install Hermes Agent

**DO NOT use the bootstrap script** (`install.sh`) — it times out on Orgo's slow network. Use `uv tool install` instead:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh          # install uv first
export PATH=$HOME/.local/bin:$PATH
uv tool install hermes-agent                              # install Hermes
```

Verify: `which hermes && hermes --version`

### 5. Generate SSH deploy key

```bash
ssh-keygen -t ed25519 -C 'CLIENT-bot-orgo-YYYYMMDD' -f /root/.ssh/id_ed25519 -N ''
cat /root/.ssh/id_ed25519.pub
```

Add to GitHub repo as deploy key:
```bash
# Delete old key first (get ID from gh api repos/OWNER/REPO/keys)
gh api repos/OWNER/REPO/keys/OLD_KEY_ID -X DELETE
# Add new key
gh api repos/OWNER/REPO/keys -X POST \
  -F "title=CLIENT-bot-orgo-YYYYMMDD" \
  -F "key=ssh-ed25519 AAA..." \
  -F "read_only=false"
```

Test: `ssh -o StrictHostKeyChecking=accept-new -T git@github.com`

### 6. Write Hermes config files

**Use base64 encoding** to write files — avoids shell escaping nightmares with special characters in API keys:

```python
import base64

def write_file_orgo(path, content, chmod="600"):
    b64 = base64.b64encode(content.encode()).decode()
    cmd = f"echo {b64} | base64 -d > {path} && chmod {chmod} {path}"
    # then run cmd via Orgo bash API
```

#### .env
```
TELEGRAM_BOT_TOKEN=<from pool>
OPENROUTER_API_KEY=<from vault>
VERCEL_TOKEN=<from vault>
```
chmod 600.

#### config.yaml
```yaml
model:
  default: deepseek/deepseek-v4-pro
  provider: openrouter

providers:
  openrouter:
    api_key: ${OPENROUTER_API_KEY}
    models:
      deepseek/deepseek-v4-pro: {}
      deepseek/deepseek-v4-flash: {}

terminal:
  backend: local
  cwd: /root
  timeout: 180

display:
  tool_progress: none
  show_cost: false

messaging:
  telegram:
    enabled: true
    token: ${TELEGRAM_BOT_TOKEN}
    allowed_users:
      - SEYED_TELEGRAM_ID
    allow_admin_from:
      - SEYED_TELEGRAM_ID
```

#### SOUL.md
Include: client identity, tech stack, design language, deploy instructions, guardrails. Keep it concise — the bot loads this every session.

See `references/nathan-nuyts-soul.md` for a worked example.

### 7. Clone the repo

```bash
mkdir -p /root/projects
cd /root/projects
git clone git@github.com:OWNER/REPO.git
```

`npm install` may timeout on first attempt — retry if needed.

### 8. Start the gateway

Orgo runs Docker containers — **no systemd**. Use `setsid` to detach:

```bash
# Kill any existing
pkill -f 'hermes gateway' 2>/dev/null

# Start detached
setsid /root/.local/bin/hermes gateway run </dev/null >/root/.hermes/logs/gateway.log 2>&1 &
disown

# Verify
sleep 2
pgrep -f 'hermes gateway'
tail -5 /root/.hermes/logs/gateway.log
```

Look for: `✓ telegram connected` and `Gateway running with 1 platform(s)`

### 9. Approve users

First message to the bot triggers pairing. The user gets a code like `33YPYMW2`. Approve on the Orgo machine:

```bash
export PATH=$HOME/.local/bin:$PATH
hermes pairing approve telegram PAIRING_CODE
```

Add client's Telegram ID to `config.yaml` under `allowed_users` once known.

### 10. Update the ledger

Update `~/.weblyfe-secrets/bot-provisioning-ledger.json`:
- `status`: `active`
- `orgo_computer`: new computer ID
- `verified_at`: today's date

### 11. Deploy standalone Cognify (client knowledge graph)

Client bots need their OWN Cognify instance — the fleet Cognify is Tailscale-only and reserved for Seyed's team. Deploy Cognify directly on the Orgo machine so the bot accesses it via `http://127.0.0.1:8799`.

**Prerequisites:**
- A separate OpenRouter API key for the client (do NOT reuse the fleet key)
- Python 3.10+ on the Orgo machine (comes standard)

**Steps:**

```python
# Clone Cognify (HTTPS — no SSH deploy key needed for this public repo)
bash("cd /root && git clone https://github.com/S3YED/cognify.git 2>&1", timeout=120)

# Run setup
bash("cd /root/cognify && bash setup.sh local 2>&1", timeout=300)
```

Write the `.env` file (base64-encode as always):
```bash
OPENROUTER_API_KEY=<client-specific key>
COGNIFY_BACKEND=local
# COGNIFY_DATA_DIR defaults to ~/.cognify — fine for local backend
```

Start `cognify-serve` as a background process (no systemd on Orgo):
```bash
cd /root/cognify
source .venv/bin/activate && set -a && . ./.env && set +a
setsid cognify-serve </dev/null >/root/.hermes/logs/cognify.log 2>&1 &
disown
```

Verify:
```python
out, code = bash("curl -s http://127.0.0.1:8799/health")
# Expected: {"status":"ok","backend":"local","version":"..."}
```

**Configure the bot** to use its local Cognify:
- Set `COGNIFY_HOST=127.0.0.1` and `COGNIFY_PORT=8799` in the bot's Hermes `.env`
- The `cognify` skill's recall endpoint is `http://$COGNIFY_HOST:$COGNIFY_PORT/recall`
- Namespace convention for client bots: `workspace:<bot-name>` (e.g. `workspace:zeus`)

**Differences from fleet Cognify:**
- Fleet: `100.101.29.56:8765/cognify/recall` (Tailscale-only, shared Neo4j backend)
- Client: `127.0.0.1:8799/recall` (localhost, local ChromaDB+networkx backend)
- Client endpoint does NOT have the `/cognify/` path prefix — that was nginx on the fleet machine
- Client has its own data directory (~/.cognify/), fully isolated

## Pitfalls

- **Orgo computer IDs are ephemeral.** A rebuilt machine gets a new ID. Always re-discover.
- **Client Orgo API keys often don't work.** Use the master key for all operations. Client keys (e.g. `ORGO_APPIE10_NATHAN`) may return 401.
- **Bootstrap install script times out.** Orgo has slow outbound network. Use `uv tool install`.
- **npm install times out.** Orgo bandwidth is limited. Retry or run in background.
- **No systemd in Docker.** Use `setsid ... </dev/null >/dev/null 2>&1 & disown` to detach the gateway.
- **Base64-encode file writes.** Shell heredocs with secrets risk escaping bugs. Base64 is deterministic.
- **Google Calendar token format.** If using `google-workspace` skill with existing tokens from `~/.weblyfe-secrets/`, the token JSON may need `"type": "authorized_user"` added and the file linked to `~/.hermes/google_token.json`.
- **`export` prefix in env files.** The vault env files use `export KEY="value"` format. Strip `export ` prefix and quotes before using values.
- **SSH key per-repo on Appie-1.** The default `id_ed25519` key may not have access to all repos. For repos like `S3YED/nathan-nuyts`, use the account-level `id_ed25519_github` key via `git config --local core.sshCommand "ssh -i ~/.ssh/id_ed25519_github -o IdentitiesOnly=yes"`.
- **Git pre-commit hook blocks em dashes.** Weblyfe projects have a hook that blocks commits containing `—` (U+2014). Replace with period, comma, colon, or hyphen before committing. Use `git commit --no-verify` only as emergency bypass.
- **Orgo auth scoping across projects.** Not all computers in Seyed's main workspace (`77e2768b`) are accessible with the master key — some return 401. Computers in project-specific workspaces (e.g. `7a945fac` for Nathan Nuyts) ARE accessible. The machine named "Zeus (Nathan Nuyts)" in Seyed's workspace is a different computer ID from the actual Zeus. Always test `echo 'ALIVE'` before building tooling around a computer ID. If 401, re-discover — the real bot machine may be in a different project.
- **Client bots get their OWN Cognify instance.** The fleet Cognify at `100.101.29.56:8765` is Tailscale-only and only for Appie's in Seyed's team. Client bots need their own standalone Cognify on their Orgo machine (see Cognify Deployment section below).
- **Cognify clone requires HTTPS, not SSH.** Orgo machines only have deploy keys for their specific client repo. Clone Cognify via `https://github.com/S3YED/cognify.git` (public repo) instead of SSH.
- **Disk fills up before Cognify install.** Orgo machines are often at 95%+ disk usage. Before `pip install`: clean `npm cache clean --force`, `rm -rf /root/.cache/pip /root/.cache/uv`, `apt-get clean`. Aim for 500MB+ free.
- **`setup.sh local` does NOT install the serve extra.** The server command `cognify-serve` fails with "FastAPI not installed" unless you separately run `source .venv/bin/activate && pip install -e ".[serve]"`. Run this in background + poll, same pattern as setup.sh.
- **Long commands must run in background.** Orgo's API gateway 504s at ~150s. For `setup.sh`, `pip install`, or `npm install`: use `nohup CMD > /tmp/log 2>&1 & echo PID:$!`, then poll with 10s intervals checking `pgrep` and `tail -1 /tmp/log`.
- **Cognify client server has NO `/cognify/` path prefix.** The fleet instance uses `/cognify/recall` (via nginx reverse proxy). Client-local instances expose endpoints directly: `/recall`, `/ingest`, `/health` on the configured port.
- **Don't blindly clean `/root/.cache/`.** That directory contains `chroma/` (ChromaDB ONNX embedder model). Cleaning pip/npm/uv caches is fine, but wiping the entire `.cache` breaks Cognify's vector search. If you must clean it, re-verify `curl /health` + `curl /recall` after. The Chroma model auto-redownloads on next use, but existing vector data may need re-ingest.

## References

- `references/nathan-nuyts-config.yaml` — full working config for Nathan's bot
- `references/secret-sourcing.md` — which env files hold which keys