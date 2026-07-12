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

Always confirm the repo root before you touch git. This repo may live in different places on different hosts, so do not hardcode a path from memory. Use the actual checkout you are already in, or resolve it with `git rev-parse --show-toplevel`.

```bash
cd /path/to/appie-brain

# Check what changed, including untracked files
git status --short --branch

# Review the exact delta before staging
git diff --stat
git diff --name-only

# Add files selectively. Avoid sweeping in secrets or unrelated noise.
git add path/to/your/changes/

# Commit with Appie identity
git commit -m "🪽 Appie-X: Brief description"

# Push the current branch
git push origin HEAD
```

Pitfall: a sync often includes lots of generated or historical files. Review staged content with `git diff --cached --check` before push so you catch whitespace issues and accidental bulk adds early.

See `references/safe-sync-checklist.md` for a compact pre-push checklist.

## Packaging rule

When a topic shows up more than once, or it could help future fleet work, promote it to a **class-level umbrella doc** in `knowledge/docs/` or a comparable top-level knowledge area.

- Put the reusable rules in the umbrella doc.
- Put session-specific evidence in `references/<topic>.md` under the relevant skill.
- Add one short cross-link from the umbrella doc to the reference file.
- Do not create narrow one-session skills unless the workflow is genuinely reusable across unrelated tasks.

See `references/class-level-packaging.md` for the house pattern.

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
