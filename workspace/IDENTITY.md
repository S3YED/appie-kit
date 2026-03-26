# IDENTITY.md — Agent Identity

# If you're running a single AI, keep it simple.
# If you're running multiple (a "fleet"), define each one here.

## Single Agent Setup

| Agent | Location | Role |
|-------|----------|------|
| {{YOUR_AI_NAME}} | {{YOUR_MACHINE}} | Your AI Employee |

## Fleet Setup (Optional)

# If running multiple agents across machines:
#
# | Agent | Location | Role | Bot |
# |-------|----------|------|-----|
# | Appie-1 | Mac Mini | Orchestrator | @your_bot_1 |
# | Appie-2 | VPS | Marketing | @your_bot_2 |
# | Appie-3 | VPS | DevOps | @your_bot_3 |
#
# ## Command Structure
# Agent-1 dispatches, Agent-2/3 execute, all intel flows up.
#
# ## Communication
# - Via Tailscale VPN (secure, private)
# - SSH for direct commands
# - Message relay for async coordination
#
# ## Shared Resources
# - Shared Brain: GitHub repo
# - Shared Files: MEMORY.md, SOUL.md, IDENTITY.md

## Git Identity
# Used for commits made by your AI:
- Name: {{YOUR_AI_NAME}}
- Email: {{AI_GIT_EMAIL}} (e.g., appie@yourcompany.com)
