# Secret sourcing for Weblyfe client bots

## Env files (all under `~/.weblyfe-secrets/`)

| File | Key | Purpose |
|---|---|---|
| `.env` | `ORGO_API_KEY` | Master Orgo key — use for ALL API calls |
| `.env` | `OPENROUTER_API_KEY` | OpenRouter for LLM access (export-prefixed) |
| `.env` | `VERCEL_TOKEN` | Vercel deploy (may expire — re-auth with `vercel login`) |
| `orgo-openrouter-keys.env` | `ORGO_APPIE6_FERDOWS` | Ferdows Soleiman's Orgo key |
| `orgo-openrouter-keys.env` | `ORGO_APPIE7_BAKKALI` | Soleiman Bakkali's Orgo key |
| `orgo-openrouter-keys.env` | `ORGO_APPIE9_RAMZY` | Ibrahim Ramzy's Orgo key |
| `orgo-openrouter-keys.env` | `ORGO_APPIE10_NATHAN` | Nathan Nuyts' Orgo key (currently INVALID — use master) |
| `bot-provisioning-pool.env` | `BOT_APPIE6_TOKEN` through `BOT_APPIE10_TOKEN` | Telegram bot tokens |
| `bot-provisioning-ledger.json` | — | Which bot is assigned to which client |

## Note on `export` prefix

The main `.env` file uses `export KEY="value"` syntax. When parsing in Python:

```python
if line.startswith('export '):
    line = line[7:]
k, v = line.split('=', 1)
v = v.strip().strip('"').strip("'")
```

## Client Orgo keys

Client-specific Orgo API keys (`ORGO_APPIE10_NATHAN`, etc.) have been found to return 401 for Orgo API calls. Always fall back to the master key (`ORGO_API_KEY`) for provisioning and management operations.