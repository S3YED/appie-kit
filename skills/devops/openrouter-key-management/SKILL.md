---
name: openrouter-key-management
description: "Manage OpenRouter API keys across the fleet: check status/usage, set spending limits, configure model guardrails, and set up usage alerts. Covers both organization-level control and per-key management."
version: 1.0.0
author: Appie
license: MIT
metadata:
  hermes:
    tags: [devops, openrouter, api-keys, spending, fleet, guardrails]
    related_skills: [agent-fleet-operations]
---

# OpenRouter Key Management

Use this skill when managing OpenRouter API keys across the fleet: checking per-key usage and limits, updating spending caps, restricting model access, setting up usage alerts, or creating/rotating keys.

## Architecture

OpenRouter has two key-management mechanisms that stack:

1. **Per-key spending limits** (`limit` field) — set on individual API keys via the Management API. Hard cap: requests are rejected when exceeded.
2. **Guardrails** (organization-level) — restrict models, providers, data retention per key or per member. Model allowlists, provider allowlists, and budget limits that layer on top of per-key limits (the lower limit wins).

Both require a **Management API key** — a special key type that can only manage keys, not make inference calls.

## Key inventory and status check

All keys on this fleet are tracked in `~/.weblyfe-secrets/orgo-openrouter-keys.env` (chmod 600, never git-tracked). Structure:

```
ORGO_APPIE6_FERDOWS=sk-or-...
OWN_APPIE1=sk-or-...
```

### Check all keys' current status

Each key can query its own status (no Management key needed):

```python
import json, urllib.request

keys = {
    # Load from env file
}
base_url = "https://openrouter.ai/api/v1/key"

for name, api_key in keys.items():
    req = urllib.request.Request(base_url)
    req.add_header("Authorization", f"Bearer {api_key}")
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
        d = data.get('data', {})
        print(f"{name}: limit=${d.get('limit')}, "
              f"remaining=${d.get('limit_remaining')}, "
              f"usage=${d.get('usage',0):.4f}, "
              f"reset={d.get('limit_reset')}")
```

Response fields on each key:

| Field | Type | Meaning |
|---|---|---|
| `limit` | number or null | Spending limit in USD (null = unlimited) |
| `limit_remaining` | number or null | Remaining credits for this period |
| `limit_reset` | "daily"/"weekly"/"monthly" or null | When limit resets |
| `usage` | number | Total credits used (all time) |
| `usage_daily`/`weekly`/`monthly` | number | Usage for current period |
| `disabled` | boolean | Whether the key is active |
| `include_byok_in_limit` | boolean | Whether BYOK usage counts toward limit |

## Setting spending limits

Requires a **Management API key**.

### Update an existing key's limit

```bash
curl -X PATCH https://openrouter.ai/api/v1/keys/{hash} \
  -H "Authorization: Bearer YOUR_MANAGEMENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"limit": 40}'
```

The `hash` is the key's hash identifier (from GET /api/v1/keys or the Management API list).

### Create a new key with a limit

```bash
curl -X POST https://openrouter.ai/api/v1/keys \
  -H "Authorization: Bearer YOUR_MANAGEMENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Client Name", "limit": 40, "limit_reset": "monthly"}'
```

### Reset types

- `null` — one-time hard cap (total spend, never resets)
- `"daily"` — resets at midnight UTC
- `"weekly"` — resets Monday midnight UTC
- `"monthly"` — resets 1st of month midnight UTC

### Get a key hash from the Management API

```bash
curl -s https://openrouter.ai/api/v1/keys \
  -H "Authorization: Bearer YOUR_MANAGEMENT_KEY" \
  | jq '.data[] | {name, hash, label, limit, usage}'
```

## Restricting models (Guardrails)

OpenRouter Guardrails let you restrict which models and providers a key or member can use.

### Programmatic guardrail management

```bash
curl -X POST https://openrouter.ai/api/v1/guardrails \
  -H "Authorization: Bearer YOUR_MANAGEMENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cheap-models-only",
    "allowed_models": ["deepseek/deepseek-v4-flash", "openai/gpt-4o-mini"],
    "limit_usd": 40,
    "reset_interval": "monthly"
  }'
```

Guardrails can be assigned to:
- **Members** — applies to all keys they create
- **Specific keys** — layered on top of member guardrails
- **Workspace default** — applies to all traffic in the workspace

Only models allowed by ALL applicable guardrails are available (intersection).

### Fleet doctrine

For Appie/Weblyfe fleet:
- **OpenRouter only for cheap/free models** (deepseek, etc.)
- **Frontier models** (Claude, GPT) ALWAYS via OAuth/platform keys, NEVER via OpenRouter
- Per-key limits: client bots $40, own fleet $60 (adjust as needed)
- Always include Seyed's user in `TELEGRAM_ALLOWED_USERS` for fleet access

## Usage alerts (cron-based)

OpenRouter has no native usage webhooks. Set up a Hermes cronjob:

```yaml
# Example cronjob: every 6h, check keys approaching limit
schedule: "0 */6 * * *"
prompt: |
  Check all OpenRouter keys in ~/.weblyfe-secrets/orgo-openrouter-keys.env.
  Alert if any key's usage exceeds 25% of its limit.
  Use the GET /api/v1/key endpoint for each key.
```

## Fleet key inventory (reference)

See `references/fleet-key-inventory.md` for the complete key list, Orgo/OWN split, per-key limits, and provisioning status as of the last update.

## Pitfalls

- **Management API key is NOT the same as a regular API key.** It cannot make inference calls. Create one via OpenRouter dashboard → Management API Keys.
- **Own keys cannot modify themselves via the Management API.** You need the designated management key.
- **Key hash is NOT the key string.** The hash is a separate identifier returned by `GET /api/v1/keys`. A given key's hash can be found by looking it up via the Management API.
- **Guardrail budgets are per-user/per-key, not shared.** Each key has its own $40 budget even if multiple keys share the same guardrail.
- **Limit intersection:** When both a per-key limit and a guardrail budget apply, the lower value wins. Set both consistently.
- **Monthly reset at UTC midnight.** If you set a limit at 3pm UTC on the 15th, it resets on the 1st of next month, not 30 days later.
- **Never expose keys in chat or logs.** The `.env` file is chmod 600 for a reason.