# Fleet OpenRouter Key Inventory (2026-06-22)

Source of truth: `~/.weblyfe-secrets/orgo-openrouter-keys.env`
Keys are `sk-or-v1-*` format, 73 chars.

## Per-agent keys (OWN / Weblyfe fleet)

| Key ref | Agent | Host | Limit | Usage (2026-06-22) | Remaining |
|---|---|---|---|---|---|
| `OWN_APPIE1` | Appie-1 | Mac Mini (this box) | $60 | $1.97 | $58.03 |
| `OWN_APPIE2` | Appie-2 | Hetzner | $60 | $8.68 | $51.32 |
| `OWN_APPIE3` | Appie-3 | Hetzner | $60 | $0.10 | $59.90 |
| `OWN_APPIE4` | Appie-4 | Mac Mini | $60 | $3.84 | $56.16 |

**Note:** OWN keys are currently at $60 limit. User requested lowering to $40 max. Also needs $10 alert threshold.

## Client bot keys (Orgo / Orgo organization)

| Key ref | Client | Orgo UUID | Limit | Usage | Remaining |
|---|---|---|---|---|---|
| `ORGO_APPIE6_FERDOWS` | Ferdows Soleiman | `5cbeed61-...` | $40 | $0.00 | $40.00 |
| `ORGO_APPIE7_BAKKALI` | Soleiman Bakkali | `5db3e89c-...` | $40 | $0.00 | $40.00 |
| `ORGO_APPIE9_RAMZY` | Ibrahim Ramzy | `1670d33d-...` | $40 | $1.75 | $38.25 |
| `ORGO_APPIE10_NATHAN` | Nathan Nuyts | `ad99bb9f-...` | $40 | $0.00 | $40.00 |
| `DEADPOOL_APPIE8_ROSLAN` | Roslan | Hetzner box | $40 | $3.05 | $36.95 |

**Note:** Client bots are already at $40 limit (correct per user's request).

## Management API key

A Management API key is needed to programmatically:
- Create new keys with spending limits
- Update existing keys' limits
- Create and assign Guardrails
- List all keys and their hashes

**Location:** Check `~/.weblyfe-secrets/.env` for `OPENROUTER_PROVISIONING_KEY` (mentioned in `FLEET-BOTS-INVENTORY.md` line 33).

## Action items (from 2026-06-22 session)

1. Find or create Management API key
2. Lower OWN keys from $60 to $40 via PATCH /api/v1/keys/{hash}
3. Set up Guardrails to restrict to cheap models only (deepseek-v4-flash, no expensive frontier models)
4. Create Hermes cronjob for $10 usage alerts (check every 6h, notify if any key exceeds 25% of limit)
5. Document everything in this file

## Telegram bot handles for reference

| Bot | Handle | User |
|---|---|---|
| Appie-1 | @appieweblyfebot | Seyed |
| Appie-6 | @weblyfeappie6bot | Ferdows |
| Appie-7 | @appieweblyfe7bot | Bakkali |
| Appie-8 | @appieweblyfe8bot | Roslan |
| Appie-9 | @appieweblyfe9bot | Ramzy |
| Appie-10 | @appieweblyfe10bot | Nathan |
| Appie-11 | @appieweblyfe11bot | Shah |