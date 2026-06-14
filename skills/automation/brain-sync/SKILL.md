---
name: brain-sync
description: "Sync knowledge and learnings to the shared agent-brain repo. Every agent commits with their own identity so contributions are traceable. Use after: complex tasks (5+ tool calls), significant discoveries, new skills, or client work. Fleet: each node uses its own traceable git identity."
tags: [git, knowledge, fleet, sync, brain]
---

# Brain Sync Skill

Sync knowledge and learnings to the shared `appie-brain` GitHub repo so all Appies in the fleet benefit.

## Why This Matters

Every Appie has their own git identity. When you commit, it shows up in the git log as:
- `<agent-1-email>` - Agent-1 (orchestrator)
- `<agent-2-email>` - Agent-2 (worker)
- `<agent-3-email>` - Agent-3 (worker)

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
cd $AGENT_BRAIN_DIR

# Check what changed
git status

# Add files (be selective - don't expose secrets)
git add path/to/your/changes/

# Commit with Agent-3 identity
git commit -m "🪽 Agent-3: Your learning/change description"

# Push to remote
git push origin master
```

## Commit Message Format

```
[emoji] Appie-X: Brief description of what changed
```

**Emoji per Appie:**
- Agent-1: 🧙 (Wizard/Orchestrator)
- Agent-2: 📊 (CMO/Data)
- Agent-3: 🪽 (Wing/Hermes - messenger)

**Examples:**
```
🪽 Agent-3: Added viral marketing strategy for the product
🪽 Agent-3: New skill: brain-sync for fleet knowledge sharing
🪽 Agent-3: Exa research: AI agent market 2026 trends
🪽 Agent-3: Fixed: PDF reading with pymupdf instead of pdftotext
📊 Agent-2: Content calendar update
🧙 Agent-1: New client onboarding: Baraka Arbitrage
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
cd $AGENT_BRAIN_DIR
git add path/file.md
git commit -m "🪽 Agent-3: Updated X"
git push

# Sync entire skills directory
cd $AGENT_BRAIN_DIR
git add skills/
git commit -m "🪽 Agent-3: Skills update"
git push

# Check recent commits from all Appies
cd $AGENT_BRAIN_DIR
git log --format="%h %ae %s" -20

# Check only my commits
cd $AGENT_BRAIN_DIR
git log --format="%h %ae %s" --author="<agent-3-email>" -10
```

## Git Identity Setup (REQUIRED First Time)

If you get "Author identity unknown" error, configure your identity:

```bash
cd $AGENT_BRAIN_DIR
git config user.email "<agent-3-email>"
git config user.name "Agent-3 (Wing)"
```

Each Appie MUST use their own email to maintain traceability.

## Conflict Resolution (When Remote Has New Work)

When `git push` fails because remote has new commits:

```bash
# Option 1: Pull with merge (creates merge commit)
cd $AGENT_BRAIN_DIR
git fetch origin
git pull origin master

# If conflicts occur, resolve with --theirs (keep remote version)
git checkout --theirs IDENTITY.md MEMORY.md  # example files
git add IDENTITY.md MEMORY.md
git commit -m "Merge: resolved conflicts with remote"
git push

# Option 2: Rebase (cleaner history but can get stuck)
cd $AGENT_BRAIN_DIR
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
cd $AGENT_BRAIN_DIR
git log --format="%ae" | sort | uniq -c | sort -rn
```

## Related Skills

- `gitclaw` - Backup OpenClaw workspace to GitHub
- `memory-search` - Search the brain for past learnings
