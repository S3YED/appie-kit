---
name: hermes-auth-troubleshooting
description: Diagnose and fix Hermes Agent OAuth/API-key authentication failures for any provider (Codex, xAI, Nous, Anthropic, MiniMax, OpenRouter). Load when Hermes API calls fail with auth errors, token refresh breaks, or a provider silently returns nothing.
version: 1.0.0
author: Appie-2
tags: [hermes, auth, oauth, troubleshooting, codex, tokens]
---

# Hermes Auth Troubleshooting

Diagnose and fix authentication issues across all Hermes Agent providers. Covers OAuth device-code flows, token refresh failures, auth.json structure, credential pools, and manual workarounds for headless environments.

## When to Load

- Hermes API calls fail with `401`, `403`, `TypeError: 'NoneType' object is not iterable`, or silent empty responses
- Token refresh errors in logs
- User reports "can't authenticate" or "login not working"
- After migrating Hermes or switching profiles
- When `hermes auth add` hangs on a headless VPS

## Quick Diagnosis

```bash
# 1. Check auth state
hermes auth list

# 2. Search for auth errors (most recent first)
grep -i "codex\|oauth\|token.*expir\|401\|403\|unauthorized\|refresh.*fail\|API call failed" \
  ~/.hermes/logs/errors.log | tail -30

# 3. Check active provider and model
hermes config | grep -A3 "Model:"

# 4. Inspect auth.json structure
python3 -c "
import json
with open('$HOME/.hermes/auth.json') as f:
    d = json.load(f)
print('Providers:', list(d.get('providers',{}).keys()))
for p, creds in d.get('credential_pool',{}).items():
    for c in creds:
        print(f\"  {p}: {c.get('label')} ({c.get('auth_type')}) last_refresh={c.get('last_refresh','none')[:19]} last_status={c.get('last_status')}\")
"
```

## Common Error Patterns

| Error | Meaning | Fix |
|-------|---------|-----|
| `TypeError: 'NoneType' object is not iterable` (Codex) | Refresh token dead, OAuth response is None | Re-authenticate (device code flow) |
| `API call failed ... summary='NoneType' object is not iterable` | Same as above, credential pool retry loop | Same |
| `AuthError: missing refresh_token` | Token was cleared/quarantined | `hermes auth add` |
| `refresh_token_reused` | Another process (Codex CLI, VS Code) consumed the single-use refresh token | Logout + re-auth |
| `invalid_grant` | Token expired beyond refresh window | Re-authenticate |

## auth.json Structure

Two layers - both must be updated:

1. **`providers.<name>`** - legacy provider state (used by `resolve_*_runtime_credentials`)
2. **`credential_pool.<name>[]`** - pooled credentials (used by `CredentialPool.refresh_credentials`)

Both carry `access_token`, `refresh_token`, `last_refresh`. The credential pool entries also have `last_status`, `source`, `priority`.

When fixing manually, update BOTH layers or the stale layer will re-seed dead tokens.

## Codex OAuth Device Code Flow (Manual)

When `hermes auth add openai-codex --type oauth` hangs (common on headless VPS with no PTY), run the device code flow manually:

### Step 1: Request device code

```bash
curl -s https://auth.openai.com/api/accounts/deviceauth/usercode \
  -X POST -H "Content-Type: application/json" \
  -d '{"client_id":"app_EMoamEEZ73f0CkXaXp7hrann"}'
# Returns: device_auth_id, user_code, interval, expires_at
```

### Step 2: User authorizes

Tell the user to visit `https://auth.openai.com/codex/device` and enter the `user_code`. Expires in ~15 minutes.

### Step 3: Poll + exchange + save

Use the script at `references/codex-oauth-refresh.py`. It polls every 5s, exchanges the authorization code for tokens, and writes both auth.json layers.

```bash
# 1. Edit the DEVICE_AUTH_ID and USER_CODE in the script
# 2. Run with unbuffered output
python3 -u references/codex-oauth-refresh.py
```

**Reference:** `references/codex-oauth-refresh.py` - standalone script for the full device code → poll → exchange → save flow.

### Step 4: Restart gateway

```bash
hermes gateway restart
```

New tokens only take effect after restart.

## Provider-Specific Notes

### openai-codex (ChatGPT)
- **Auth type:** OAuth device code (`oauth_external`)
- **Token URL:** `https://auth.openai.com/oauth/token`
- **Device code URL:** `https://auth.openai.com/api/accounts/deviceauth/usercode`
- **Client ID:** `app_EMoamEEZ73f0CkXaXp7hrann` (hardcoded in Hermes)
- **Base URL:** `https://chatgpt.com/backend-api/codex`
- **CLI commands:** `hermes auth add openai-codex --type oauth`, `hermes auth logout openai-codex`
- **Pitfall:** `hermes login` was removed - use `hermes auth` instead

### openrouter (API Key)
- **Auth type:** API key (`OPENROUTER_API_KEY` in `.env`)
- If missing, set in `~/.hermes/.env` and restart

### copilot (GitHub)
- **Auth type:** OAuth device code or `GITHUB_TOKEN`
- **Pitfall:** Classic PATs (`ghp_*`) don't work - need `gho_*` tokens from `gh auth login`

## Pitfalls

1. **Token refresh consumes the refresh_token.** If another process (Codex CLI, VS Code Copilot extension, another Hermes profile) refreshes the same token, your copy becomes a "reused" single-use token and triggers `refresh_token_reused`. Solution: logout + re-auth with fresh device code.

2. **`hermes login` is gone.** Hermes migrated to `hermes auth` for credential management. The old `hermes login --provider openai-codex` no longer works.

3. **Gateway restart required.** Token changes in auth.json don't take effect until the gateway process reloads. Always `hermes gateway restart` after manual token updates.

4. **Stale auth.json can re-seed dead tokens.** The credential pool may pick up old device_code entries from auth.json on next load. Remove dead entries or the entire `openai-codex` pool section before re-adding.

5. **Headless VPS + device code = no local browser.** Use the manual curl flow (Step 1-3 above) - the device code flow doesn't need a callback URL, just the user visiting a URL on their own device.

6. **`--no-browser --manual-paste` is wrong for messaging platforms.** This flag combo waits for stdin paste of a callback URL - from Telegram/Discord/Slack the paste never arrives. Use `--no-browser` alone (standard device code print-and-poll) or the manual curl approach.

7. **Background processes for long-running polls.** When running Codex OAuth from a messaging platform (Telegram etc.), use `terminal(background=True, notify_on_complete=True)` so the poll doesn't block the agent. The device code poll can take up to 15 minutes.

8. **Always verify auth endpoint reachability first.** Before starting the flow, `curl` the device-code endpoint to confirm the VPS can reach `auth.openai.com`. A hung `hermes auth add` with zero output often means a network/firewall issue, not a flow bug.

9. **Device codes are single-use.** Launching a second poller with the same code (e.g., killing and restarting a background process) creates a stale poller - the first successful authorization consumes the code. Always request a fresh device code if restarting.
