---
name: fleet-dream
description: >
  Nightly memory consolidation across the Weblyfe agent fleet (Appie-1/2/5 OpenClaw + Appie-3/4 Hermes).
  Use when: running the nightly dream sweep, checking fleet memory status, or manually triggering consolidation.
  Collects memory from all fleet nodes, runs LLM analysis (MiniMax M2.7), and writes consolidated insights.
---

# Fleet Dream — Cross-Fleet Memory Consolidation

Runs every night at 03:05 AM. Collects memory from all agents, consolidates with MiniMax M2.7, writes to `memory/fleet-dreams/`.

## How It Works

```
03:05 AM — Appie-1 (Mac Mini)
  ├─ SSH → Appie-2: collect ~/.openclaw/memory/YYYY-MM-DD.md
  ├─ SSH → Appie-3: collect ~/.hermes/memories/*.md
  ├─ SSH → Appie-4: collect ~/.hermes/memories/*.md
  └─ Local:  ~/memory/YYYY-MM-DD.md
         ↓
  MiniMax M2.7 consolidation prompt
         ↓
  Writes:
  - ~/memory/fleet-dreams/YYYY-MM-DD.md (unified fleet dream log)
  - Updates ~/memory/YYYY-MM-DD.md with fleet-level insights
```

## Manual Trigger

```
/fleet-dream
```
Or from this skill: "Run the fleet dream now"

## Config

- `scripts/fleet-dream.sh` — main cron script
- `memory/fleet-dreams/` — consolidated dream logs
- Schedule: `5 3 * * *` (3:05 AM daily)
