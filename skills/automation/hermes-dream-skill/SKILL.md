---
name: hermes-dream
description: >
  Nightly memory consolidation skill for Hermes agents (Appie-3 & Appie-4).
  Consolidates memory each night, writes to ~/hermes-dreams/, and delivers to fleet.
  Schedule: 03:10 AM daily via Hermes cron.
---

# Hermes Dream Skill

Install on Hermes agents (Appie-3/4) for fleet-wide memory consolidation.

## What It Does

```
03:10 AM — Hermes Agent
  → Read: memories/MEMORY.md, memories/USER.md, session transcripts (24h)
  → LLM consolidation (MiniMax M2.7 via api.minimaxi.chat)
  → Write: ~/hermes-dreams/YYYY-MM-DD.md
  → Deliver: push to fleet collection point OR message via Telegram
```

## Setup (once per Hermes agent)

1. Create skill dir:
   `mkdir -p ~/.hermes/skills/hermes-dream`

2. Save this SKILL.md

3. Set up cron (via Hermes CLI or Telegram):
   `/cron add "hermes-dream consolidation" at 03:10 daily`

4. Ensure MINIMAX_API_KEY is in ~/.hermes/.env

## Dream Output Format

```
# Hermes Dream: YYYY-MM-DD
## Nodes Memory
[machine-relevant memories]
## Session Patterns
[recurring themes from today]
## Cleanup Candidates
[old/stale entries]
## Fleet Notes
[things Appie-1 should know]
```

## Collection

Appie-1 collects via:
```bash
# Via git push (Hermes pushes its dream to a git repo each morning)
# OR via:
ssh appie-1 "cat >> ~/memory/fleet-dreams/appie-4-$(date +%Y-%m-%d).md" < ~/hermes-dreams/YYYY-MM-DD.md
```

## Key Notes for Hermes
- Use `hermes tools memory_add` to persist key learnings
- Use `hermes cron` to manage the dream schedule
- Dream skill auto-loads when "dream", "consolidate", or "sleep" mentioned
