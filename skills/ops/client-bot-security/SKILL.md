---
name: client-bot-security
title: Client Bot Security Audit & Hardening
description: Full-spectrum security audit for client Telegram bots across a multi-gateway fleet (Hermes + OpenClaw). Covers bot inventory & topology mapping, token provisioning security, SSH key hygiene, authorized_keys audit, secrets map documentation, and bot lifecycle management (free→assigned→active→retired).
trigger: User asks to 'secure all client bots', 'audit bot security', 'check bot tokens', 'inventory bots', 'harden bot deployment', or any request to assess security posture of deployed client Telegram bots across the fleet.
---

# Client Bot Security Audit & Hardening

## When to Use

Activate this skill when:
- User asks to "secure all client bots" or "make me the most secure CTO"
- Auditing security posture of deployed Telegram bots
- Inventorying which bots run where and with what secrets
- Checking SSH key hygiene for bot-hosting fleet nodes
- Setting up a bot provisioning pipeline
- Reviewing or creating the bot-provisioning-ledger.json

## Bot Discovery & Inventory

### 1. Find Bot Avatars

Bot avatars in the workspace reveal which Telegram bots exist:

```bash
ls -la ~/clawd/assets/agent-avatars/
# Pattern: <name>-<handle>.jpg
# e.g. priva-Privanotifybot.jpg → @Privanotifybot
```

### 2. Find Bot Projects

Search the workspace for bot-related projects:

```bash
ls ~/clawd/projects/ | grep -iE '(bot|telegram|notify|agent)'
```

### 3. Find Bot Configs & Secrets

Three layers of secret storage:
- `<secrets-vault>/` — central secrets vault (primary admin host only)
- Hermes `.env` files — per-node (<node>: `$HERMES_HOME/.env`)
- OpenClaw config — (<legacy-node>: `$OPENCLAW_CONFIG`)

```bash
# Central vault
ls -la ~/<secrets-vault>/
# → bot-provisioning-ledger.json (token_ref map)
# → bot-provisioning-pool.env (raw tokens for free pool)
# → telegram-bot.env (current bot token for this agent)
# → .env (all other API keys)

# Fleet node Hermes
ssh <user>@<tailscale_ip> "cat $HERMES_HOME/.env | grep -iE 'BOT|TOKEN'"

# Fleet node OpenClaw
ssh <user>@<tailscale_ip> "cat $OPENCLAW_CONFIG"
```

### 4. Bot Topology Map

Document per bot:

| Field | Example |
|-------|---------|
| name | <bot-role> |
| handle | @examplebot |
| token_ref | TELEGRAM_BOT_TOKEN (in telegram-bot.env) |
| host | appie-1 (this Mac Mini) |
| gateway | Hermes |
| status | active / assigned / free / retired |

The bot-provisioning-ledger.json tracks:
```json
{
  "name": "<bot-name>",
  "handle": "@examplebot",
  "token_ref": "APPIE_DOCTOR_BOT_TOKEN",
  "status": "assigned",
  "box": "<host>",
  "sale": null,
  "assigned_at": "2026-06-11",
  "notes": "..."
}
```

### 5. Gateways & Running Processes

Check what's running on each fleet node:

```bash
# Hermes gateway detection
ssh <host> "ps aux | grep -iE '(gateway|hermes)' | grep -v grep"
# → /usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace

# OpenClaw gateway detection
ssh <host> "ps aux | grep -iE '(openclaw|openclaw-gateway)' | grep -v grep"
# → openclaw-gateway

# Open ports
ssh <host> "ss -tlnp"  # Linux
# Hermes: varies (gateway port in config)
# OpenClaw: typically 18789 (HTTP API) + 18791 (internal)
```

## SSH Key Audit Procedure

### 1. Inventory Authorized Keys

```bash
for host in "<user>@<ip1>" "<user>@<ip2>"; do
  echo "=== $host ==="
  ssh -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no \
    -i "$HOME/.ssh/<key>" "$host" \
    "cat ~/.ssh/authorized_keys | awk '{print \$3}'"
done
```

This reveals:
- How many keys are authorized (baseline for changes)
- Who has access (the comment field = identity)
- Stale/decommissioned keys

### 2. Check for Deploy Keys

```bash
ssh <host> "ls -la ~/.ssh/ | grep -v authorized_keys | grep -v known_hosts"
```

Deploy keys (for CI/CD or service accounts) should be in separate files with clear filenames.

### 3. Audit SSH Config

```bash
ssh <host> "cat ~/.ssh/config"
```

Check for:
- `PasswordAuthentication no`
- `PubkeyAuthentication yes`
- No wildcard `Host *` that exposes sensitive hosts

### 4. Root Login Assessment

Determine if the node allows direct root SSH. If so, document and flag for hardening:
```bash
ssh <host> "grep -i 'permitrootlogin\|passwordauthentication' /etc/ssh/sshd_config"
```

## Bot Token Security

### Where Tokens Live

| Location | Risk | Mitigation |
|----------|------|------------|
| `~/<secrets-vault>/` (appie-1) | Medium (local machine compromise) | chmod 600, no git track |
| `$HERMES_HOME/.env` (<node>) | Medium (VPS compromise) | chmod 600, root-only read |
| OpenClaw config (<legacy-node>) | Medium (VPS compromise) | chmod 600 on config dir |
| Bot provisioning pool | High (bulk token leak) | Never echo to chat/logs |

### Token Discipline Rules

1. **Never** echo token values to chat, logs, or commits
2. **Never** put tokens in `package.json`, `bot.py`, or any tracked file
3. **Always** chmod 600 on .env files
4. **Always** use `token_ref` in the ledger, not raw tokens
5. **Token rotation**: rotate on each bot reassignment or security incident
6. **Provisioning**: new bots → pool tokens → assign in ledger → point env → test → activate

### Gitleaks for Token Detection

```bash
# Scan all project dirs for leaked tokens
gitleaks detect --source ~/clawd/projects --no-git --config ~/.gitleaks.toml --verbose
```

### Bot Lifecycle

```
free → assigned → active → retired
```

- **free**: token in provisioning pool, no box assigned
- **assigned**: token linked to a box/env, not yet tested
- **active**: confirmed running, serving users
- **retired**: token revoked, bot removed, ledger archived

## Secrets Map

Maintain a secrets map that documents:
- **Secret**: env var name
- **Location**: which file(s) and node(s)
- **Access**: which users/processes can read it
- **Rotation**: last rotated, rotation policy
- **Scope**: which bot(s) depend on it

Format:
```markdown
| Secret | Location | Access | Scope |
|--------|----------|--------|-------|
| TELEGRAM_BOT_TOKEN (<bot-role>) | `~/<secrets-vault>/telegram-bot.env` | <remote-user>@<node> | <bot-role> |
| TELEGRAM_BOT_TOKEN (<bot-gateway>) | `$HERMES_HOME/.env` | <remote-user>@<node> | <bot-gateway> |
```

## Client Bot Security Checklist

Run this checklist for each new client bot deployment:

- [ ] Bot token in `<secrets-vault>/bot-provisioning-pool.env` (not tracked)
- [ ] Bot registered in `bot-provisioning-ledger.json` with token_ref
- [ ] Status set to `assigned` (with box, sale, assigned_at)
- [ ] SSH access to host verified (key + user)
- [ ] authorized_keys reviewed (only current keys)
- [ ] .env file has chmod 600
- [ ] Gateway verified running (Hermes or OpenClaw)
- [ ] Bot responds to /start (telegram smoke test)
- [ ] Gitleaks scan passes on project dir
- [ ] Dep audit clean (npm audit / safety check)
- [ ] Tailscale ACL permits bot-to-user traffic

## Pitfalls

- **Remote SSH key mismatch**: Key `<ssh-key-name>` for <user>@<spark-tailscale-ip> returns `Permission denied`. May need a different user/key. Don't assume all fleet nodes are reachable.
- **Bot provisioning pool leak**: If leaked, every unassigned token in the pool is compromised. Guard with chmod 600.
- **OpenClaw vs Hermes configs are different**: OpenClaw stores tokens in `openclaw.json` (JSON), not `.env`. Know which gateway runs on which node before looking.
- **Ghost nodes return**: Nodes that were offline >30d may have different SSH keys when they come back. Verify before re-adding to active scan.
- **authorized_keys drift**: Manual SSH key additions by other agents/users can go undocumented. Compare against a known-good baseline.