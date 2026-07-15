---
name: brain-sync
description: "Sync knowledge and learnings to the shared appie-brain repo. Every Appie commits with their own identity so contributions are traceable. Use after: complex tasks (5+ tool calls), significant discoveries, new skills, or client work. Fleet: Appie-1 (Orchestrator/MacMini), Appie-2 (CMO/DO), Appie-3 (CTO/VPS)."
tags: [git, knowledge, fleet, sync, brain]
---

# Brain Sync Skill

Sync knowledge and learnings to the shared `appie-brain` GitHub repo so all Appies in the fleet benefit.

## Why This Matters

Every Appie has their own git identity. When you commit, it shows up in the git log as:
- `appie1@weblyfe.nl` - Appie-1 (Orchestrator, Mac Mini)
- `appie2@weblyfe.nl` - Appie-2 (CMO/Herald, DO VPS)
- `appie3@weblyfe.nl` - Appie-3 (CTO/Worker, DO VPS)

This makes contributions traceable across the fleet.

## When to Sync

**ALWAYS sync after:**
- Complex tasks (5+ tool calls)
- Debugging sessions where you discovered something
- New skills created or significantly updated
- Client project work (new files created)
- Research findings (from Exa/web search)
- Process improvements
- Error solutions that could help others

**You can skip for:**
- Simple one-off commands
- Read-only exploration
- Quick questions answered

## How to Sync

```bash
cd /root/.hermes/appie-brain

# Check what changed
git status

# Add files (be selective - don't expose secrets)
git add path/to/your/changes/

# Commit with Appie-3 identity
git commit -m "🪽 Appie-3: Your learning/change description"

# Push to remote
git push origin master
```

## Commit Message Format

```
[emoji] Appie-X: Brief description of what changed
```

**Emoji per Appie:**
- Appie-1: 🧙 (Wizard/Orchestrator)
- Appie-2: 📊 (CMO/Data)
- Appie-3: 🪽 (Wing/Hermes - messenger)

**Examples:**
```
🪽 Appie-3: Added viral marketing strategy for Weblyfe Appie
🪽 Appie-3: New skill: brain-sync for fleet knowledge sharing
🪽 Appie-3: Exa research: AI agent market 2026 trends
🪽 Appie-3: Fixed: PDF reading with pymupdf instead of pdftotext
📊 Appie-2: Content calendar for April 2026
🧙 Appie-1: New client onboarding: Baraka Arbitrage
```

## What to Sync

**DO sync:**
- Skills (`/skills/`)
- Memory files (`/memory/`)
- Projects (`/projects/`)
- Scripts/tools (`/scripts/`, `/tools/`)
- Documentation
- Learned approaches/patterns

**NEVER sync:**
- `.env` or secrets
- Session transcripts (too large)
- Temporary files
- Build artifacts (`node_modules/`, etc.)

## Safety Checks

Before committing:
1. `git status` - see what changed
2. `git diff --cached` - review staged changes
3. Ensure no API keys or secrets in changes
4. Check that changes are relevant to the fleet

## Quick Commands

```bash
# Sync specific file
cd /root/.hermes/appie-brain
git add path/file.md
git commit -m "🪽 Appie-3: Updated X"
git push

# Sync entire skills directory
cd /root/.hermes/appie-brain
git add skills/
git commit -m "🪽 Appie-3: Skills update"
git push

# Check recent commits from all Appies
cd /root/.hermes/appie-brain
git log --format="%h %ae %s" -20

# Check only my commits
cd /root/.hermes/appie-brain
git log --format="%h %ae %s" --author="appie3@weblyfe.nl" -10
```

## Git Identity Setup (REQUIRED First Time)

If you get "Author identity unknown" error, configure your identity:

```bash
cd /root/.hermes/appie-brain
git config user.email "appie3@weblyfe.nl"
git config user.name "Appie-3 (Wing)"
```

Each Appie MUST use their own email to maintain traceability.

## Conflict Resolution (When Remote Has New Work)

When `git push` fails because remote has new commits:

```bash
# Option 1: Pull with merge (creates merge commit)
cd /root/.hermes/appie-brain
git fetch origin
git pull origin master

# If conflicts occur, resolve with --theirs (keep remote version)
git checkout --theirs IDENTITY.md MEMORY.md  # example files
git add IDENTITY.md MEMORY.md
git commit -m "Merge: resolved conflicts with remote"
git push

# Option 2: Rebase (cleaner history but can get stuck)
cd /root/.hermes/appie-brain
git fetch origin
git pull --rebase origin master

# If conflicts during rebase:
git checkout --theirs conflicted-file.md
git add conflicted-file.md
git rebase --continue

# If rebase gets stuck (EDITOR unset error), abort and use Option 1:
git rebase --abort
```

**Rule:** When in doubt, use Option 1 (merge) - it's more robust.

## Fleet Contribution Stats
To see who's contributing what:
```bash
cd /root/.hermes/appie-brain
git log --format="%ae" | sort | uniq -c | sort -rn
```

## Related Skills

- `gitclaw` - Backup OpenClaw workspace to GitHub
- `memory-search` - Search the brain for past learnings
