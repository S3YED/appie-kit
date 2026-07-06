# Fleet Topology (Appie-1 / Mac Mini)

Current fleet structure on the Mac Mini:

## Local Hermes Agents

| Agent | Config Dir | Role | Status |
|-------|-----------|------|--------|
| **Appie-1** (default) | `~/.hermes/` | Primary agent | ✅ Active |
| **Appie-4** | `~/.hermes-appie4/` | CFO/Business Intelligence | ✅ Active, Telegram @appieweblyfe4bot |

## Remote Agents

| Agent | Host | Role | Status |
|-------|------|------|--------|
| **Appie-2** | Hetzner 178.104.154.117 | CMO/Herald | ✅ Gateway + Neo4j |
| **Appie-3** | Hetzner 46.225.233.232 (Tailscale 100.69.131.51) | CTO/DevOps | ✅ Gateway |

## Client Agents

| Agent | Host | Status |
|-------|------|--------|
| **Diddy** | Harry's Mac Mini (100.79.180.56) | ✅ rsync actief |

## Stale SSH Config Entries

The following hosts in `~/.ssh/config` are **outdated** and should be removed or updated:

- `appie-4-hetzner` (178.104.118.167) — Appie-4 is no longer on Hetzner. This host might be a different machine or decommissioned.
- `appie-4-hermes` (100.80.107.25) — Appie-4 is local on Mac Mini, not Tailscale.