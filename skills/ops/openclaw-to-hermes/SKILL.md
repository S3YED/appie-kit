---
name: openclaw-to-hermes
description: Port OpenClaw Appie to Hermes Agent and spawn new instances. Clone appie-brain, configure identity files (SOUL.md, USER.md, IDENTITY.md, AGENTS.md), set up git sync, copy secrets, and start Hermes gateway.
version: 1.0.0
author: Appie-3
tags: [migration, setup, infrastructure, appie]
---

# OpenClaw to Hermes Agent Migration

Complete guide for migrating an Appie from OpenClaw to Hermes Agent.

## Quick Start

```bash
# 1. SSH key for GitHub (on new server)
ssh-keygen -t ed25519 -C "hermes-agent" -f ~/.ssh/id_ed25519 -N ""
# Add public key to github.com/settings/keys

# 2. Clone appie-brain
git clone git@github.com:S3YED/appie-brain.git ~/.hermes/appie-brain

# 3. Create identity files (SOUL.md, USER.md, IDENTITY.md, AGENTS.md)
# See full guide at ~/.hermes/docs/APPIE-PORT-GUIDE.md

# 4. Git setup
cd ~/.hermes
git init
git remote add origin git@github.com:S3YED/appie-brain.git
git config user.email "appieN@yourdomain.com"
git config user.name "Appie-N"

# 5. Install deps
pip install pymupdf requests --break-system-packages

# 6. Create .env with secrets
# Copy from appie-brain/.env.secrets

# 7. Start Hermes
hermes-agent start
```

## Key Files to Create

### SOUL.md
Identity, role, values, communication style, boundaries.

### USER.md
Seyed's profile: name, timezone (Bangkok), company (Weblyfe), contact info.

### IDENTITY.md
Appie family roster: Appie-1 (Orchestrator), Appie-2 (CMO), Appie-3 (CTO).

### AGENTS.md
Session startup rules, memory discipline, red lines.

## Required API Keys (.env)

```
CUSTOM_OPENAI_API_KEY=
CUSTOM_OPENAI_BASE_URL=
CUSTOM_OPENAI_MODEL=
## Required API Keys (.env)

```
CUSTOM_OPENAI_API_KEY=...
CUSTOM_OPENAI_BASE_URL=http://localhost:11434/v1
CUSTOM_OPENAI_MODEL=gemma4:26b
TELEGRAM_BOT_TOKEN=...
TELEGRAM_ALLOWED_USERS=1817919454
HERMES_WORKING_DIR=$HOME/workspace
EXA_API_KEY=...
NOTION_API_KEY=ntn_...   # Required for Notion access
NOTION_CONTENT_FACTORY=<content-database-id>  # Set from the target workspace
NOTION_TASK_LIST=<task-database-id>
NOTION_PROJECTS=<projects-database-id>
```

**Note:** Notion token variable name is `NOTION_API_KEY` (from Notion integration setup).

## Verify Setup

```bash
# GitHub SSH
ssh -T git@github.com

# Notion API test
curl -s "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" | python3 -c "import sys,json; print('✅', json.load(sys.stdin).get('name'))"

# Skills available
ls ~/.hermes/skills/

# Python packages
pip list | grep -i pymupdf
```

## Full Guide

See: `~/.hermes/docs/APPIE-PORT-GUIDE.md`

## Pitfalls

1. **SSH key not linked** - Add to github.com/settings/keys
2. **Missing .env.secrets** - Copy from source machine
3. **Git push fails with "fetch first"** - `git pull origin master --rebase` then push
4. **Git has unrelated histories** - `git pull origin master --allow-unrelated-histories`
5. **Bot not responding** - Check TELEGRAM_BOT_TOKEN in .env
6. **Notion token variable** - Must be `NOTION_API_KEY`, not `NOTION_TOKEN`
7. **Git conflicts on pull** - Use `git stash`, `git pull --rebase`, `git stash pop`
