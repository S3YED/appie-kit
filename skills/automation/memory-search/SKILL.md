---
name: memory-search
description: Search and retrieve information from the Appie brain — daily logs, project notes, decisions, topics, and long-term memory files stored in ~/.hermes/memory/. Use this skill whenever you need to recall past conversations, decisions, project context, personal preferences, or anything discussed previously.
version: 1.0.0
author: Weblyfe
license: MIT
metadata:
  hermes:
    tags: [Memory, Search, Context, History, Brain]
---

# Memory Search

Search the Appie brain — daily logs, project notes, decisions, topics, and long-term memory.

## When to Use

- User asks about past decisions, conversations, or context
- User says "remember when...", "what did we decide about...", "check my notes on..."
- You need project context, client info, or infrastructure details
- Looking up dates, events, or historical information

## Memory Structure

All files are in `~/.hermes/memory/`:

- **Daily logs**: `YYYY-MM-DD.md` — raw daily notes
- **Topics**: `topics/*.md` — subject-specific knowledge
- **Projects**: `projects/*.md` — project documentation
- **Decisions**: `decisions/*.md` — recorded decisions
- **Infrastructure**: `infrastructure/*.md` — server/fleet notes
- **Plans**: `plans/*.md` — future plans
- **Research**: `research/*.md` — research notes

Top-level brain files in `~/.hermes/`:
- `MEMORY.md` — curated long-term memory (read this first)
- `USER.md` — info about the human (Seyed)
- `TOOLS.md` — tool configuration and fleet SSH details
- `IDENTITY.md` — agent identity

## Search Commands

### Full-text search across all memory files
```bash
grep -ril "SEARCH_TERM" ~/.hermes/memory/ ~/.hermes/MEMORY.md ~/.hermes/USER.md ~/.hermes/TOOLS.md 2>/dev/null
```

### Search with context (shows surrounding lines)
```bash
grep -rin -C 3 "SEARCH_TERM" ~/.hermes/memory/ 2>/dev/null | head -60
```

### List recent daily logs
```bash
ls -t ~/.hermes/memory/????-??-??.md 2>/dev/null | head -10
```

### Read a specific daily log
```bash
cat ~/.hermes/memory/YYYY-MM-DD.md
```

### Search by date range (e.g., March 2026)
```bash
ls ~/.hermes/memory/2026-03-*.md 2>/dev/null
```

### Search topics
```bash
ls ~/.hermes/memory/topics/ 2>/dev/null
grep -ril "SEARCH_TERM" ~/.hermes/memory/topics/ 2>/dev/null
```

### Search projects
```bash
ls ~/.hermes/memory/projects/ 2>/dev/null
grep -ril "SEARCH_TERM" ~/.hermes/memory/projects/ 2>/dev/null
```

### Advanced: fuzzy search with script
```bash
python3 ~/.hermes/skills/productivity/memory-search/scripts/search.py "QUERY" [--limit 10] [--recent 7]
```

## Quick Reference

Always start with `MEMORY.md` for curated long-term context, then search daily logs for specifics.

## Workflow

1. Read `~/.hermes/MEMORY.md` for high-level context
2. If more detail needed, search with `grep -ril` across memory/
3. Read the specific files that match
4. Synthesize and answer
