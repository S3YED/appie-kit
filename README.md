# Appie Kit

The skill library and configuration kit for building your own 24/7 AI employee.

This repo ships with the [Build Your Own Appie v4.4 guide](https://weblyfe.ai/store). If you have the PDF, you have everything you need to deploy a working agent and wire these skills into it.

---

## About

Appie Kit is the production skill library extracted from running [Weblyfe](https://weblyfe.nl) - a web design agency operated by AI employees (Appies) handling email triage, lead capture, content production, deployments, and client communication.

What this repo contains:

- **155 deduplicated public skills** across 8 categories. Pulled from 800+ raw skills across the Appie fleet (Mac Mini OpenClaw + Hermes, Spark Atlas Hermes, Eva OpenClaw, Wolfdiddy Hermes+OpenClaw, Hetzner Appie-2/3/4 Hermes), deduped by md5, name-collision-resolved, and Hermes-builtins removed (those ship with every Hermes install)
- Workspace configuration templates (SOUL.md, USER.md, TOOLS.md, IDENTITY.md)
- Production shell scripts for setup, health checking, session management
- Platform config examples (Telegram, Discord, WhatsApp, multi-agent fleet)
- Case studies with real numbers

Skills are compatible with [Hermes Agent](https://github.com/NousResearch/hermes-agent) and [OpenClaw](https://github.com/openclaw/openclaw). Most skills work with both. A small number require macOS (OpenClaw-only) or a local GPU (ML/fine-tuning skills).

---

## What's New - May 2026

The May 2026 release adds:

- 155 deduplicated public skills consolidated from the full Appie fleet (302 unique deduped total; 147 are Hermes builtins that already ship with Hermes installs and therefore excluded from this kit). Up from 33 in the previous release.
- Organized into 8 categories: automation, communication, content, integrations, knowledge, meta, ops, personal.
- Hermes Agent compatibility across the board. Skills were originally OpenClaw-only; the fleet now runs primarily on Hermes Agent (Nous Research) with MiniMax M2.7 via OpenRouter.
- v4.4 PDF reference: the [Build Your Own Appie v4.4 guide](https://weblyfe.ai/store) covers fleet setup, MiniMax M2.7 as the primary model, Hermes Agent install, and how skills integrate with the SOUL/USER/TOOLS layer.

---

## Quick Start

Prerequisites:
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) installed, or [OpenClaw](https://github.com/openclaw/openclaw)
- An OpenRouter API key (MiniMax M2.7 recommended, ~$0.01/1M tokens)
- Telegram bot token (optional, for messaging interface)

### 1. Clone and install

```bash
git clone https://github.com/S3YED/appie-kit.git
cd appie-kit
./install.sh /path/to/your/workspace/
```

### 2. Customize your agent files

```bash
nano workspace/SOUL.md     # Who your AI is: personality, values, communication style
nano workspace/USER.md     # Who you are: name, timezone, preferences, context
nano workspace/TOOLS.md    # What tools it can access: API references, credentials
```

### 3. Set up environment variables

```bash
cp .env.example .env.secrets
chmod 600 .env.secrets
nano .env.secrets          # Fill in your API keys
```

### 4. Copy skills to your agent

For Hermes Agent:
```bash
cp -r skills/content/design ~/.hermes/skills/
cp -r skills/knowledge/exa-plus ~/.hermes/skills/
# etc.
```

For OpenClaw:
```bash
cp -r skills/content/design ~/.openclaw/skills/
```

### 5. Start your agent

```bash
# Hermes Agent
hermes start

# OpenClaw
openclaw gateway start
```

---

## Skill Categories

| Category | Skills | What it contains |
|----------|--------|-----------------|
| [automation](skills/automation/) | 8 | Agent self-management, fleet coordination, brain sync, sub-agent spawning |
| [communication](skills/communication/) | 25 | Telegram, Discord, Slack, iMessage, email clients, webhook management |
| [content](skills/content/) | 30 | UI/UX design, image generation, video production, copywriting, Next.js |
| [data](skills/data/) | 14 | Google Sheets, Drive, Docs, Airtable, Notion, Forms |
| [integrations](skills/integrations/) | 87 | Third-party APIs, Google Workspace, ML frameworks, SaaS connectors |
| [knowledge](skills/knowledge/) | 58 | Web search, scraping, email triage, SEO, memory management, research |
| [meta](skills/meta/) | 2 | Skill authoring, agent self-evaluation, brainstorming frameworks |
| [ops](skills/ops/) | 16 | GitHub, DigitalOcean, git workflows, tmux, infrastructure management |
| [personal](skills/personal/) | 10 | Apple Notes, Things 3, Spotify, Google Tasks, weather, kanban |
| [unsorted](skills/unsorted/) | 52 | Workspace recipes, personas, tools pending category assignment |

Total: 302 skills.

---

## Architecture

### How skills work

Each skill is a directory containing a `SKILL.md` file. The SKILL.md has a YAML frontmatter block followed by the skill body:

```
---
name: exa-plus
description: "Neural web search via Exa AI."
version: 1.0.0
prerequisites:
  env_vars: [EXA_API_KEY]
metadata:
  hermes:
    tags: [search, research, web]
---

# Exa Plus

...skill instructions...
```

When Hermes Agent or OpenClaw starts, it loads all SKILL.md files from the skills directory into the agent's context. The agent can then invoke any skill by name.

### How the agent loads skills

Hermes Agent loads skills from `~/.hermes/skills/` at session start. Each skill folder name becomes a callable skill identifier.

OpenClaw loads skills from `~/.openclaw/skills/` in the same fashion.

You can drop any skill from this repo into the appropriate directory and it will be available in the next session without any restart.

### Workspace files

The `workspace/` directory contains the core identity and configuration files that shape agent behavior across all skills:

- `SOUL.md` - personality, values, communication style, tone
- `USER.md` - who you are, your timezone, your preferences
- `TOOLS.md` - tools available, API references, environment details
- `IDENTITY.md` - fleet identity for multi-agent setups
- `AGENTS.md` - operating rules, safety, group chat behavior
- `HEARTBEAT.md` - proactive check-in configuration
- `memory/` - persistent memory directory

---

## Resources

- v4.4 guide: available at [weblyfe.ai/store](https://weblyfe.ai/store)
- Hermes Agent docs: [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- OpenClaw docs: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- MiniMax M2.7 via OpenRouter: [openrouter.ai](https://openrouter.ai)

---

## The Weblyfe Stack

| Category | Tool | Why |
|----------|------|-----|
| AI model | MiniMax M2.7 (OpenRouter) | 17x cheaper than Claude, GPT-4 class quality |
| Agent framework | Hermes Agent (Nous Research) | Open source, persistent memory, multi-platform |
| Alternative framework | OpenClaw | macOS-native, good for desktop automation |
| Messaging | Telegram | Best bot API, instant delivery, group support |
| CRM | Airtable | Flexible, API-first, automatable |
| Automation | n8n | Self-hosted, 400+ integrations |
| Hosting | Vercel | Zero-config deploys, edge functions |
| VPS | DigitalOcean | Simple API, affordable |
| Networking | Tailscale | Zero-config VPN for fleet communication |
| Image gen | fal.ai (Nano Banana) | Fast, cost-effective, good quality |
| Search | Exa | AI-native search API, better than Google for research |
| Desktop agent | Clawd Cursor | Screen control, universal app automation |

---

## Case Studies

### Lead capture automation

Before: manual email checks, copy-paste to spreadsheet, manual follow-ups.
After: Form submission triggers Airtable record, Brevo list entry, confirmation email, and timed follow-up sequence. Zero manual steps, under 2 seconds end-to-end, 24/7.

### Multi-agent fleet (3 Appies)

Appie-1 (Orchestrator, Mac Mini), Appie-2 (Marketing, VPS), Appie-3 (DevOps, VPS).
Cost: ~$148/month for 3 AI employees running continuously.
Setup details: [configs/multi-agent.example.yml](configs/multi-agent.example.yml).

### Content pipeline

Input: one brand brief or topic.
Output: AI video + voiceover + social posts + blog draft.
Time: 15 minutes vs 4+ hours manual.

[Full case studies](case-studies/)

---

## Security

This repo contains no secrets. All API keys use placeholder values.

Before going live:
- Review `workspace/SOUL.md` for any personal information
- Verify `.env.secrets` has no real keys committed
- Run `tools/security-scan.sh` after setup
- Set file permissions: `chmod 600 .env.secrets`
- Use Tailscale for remote access, never expose SSH publicly

---

## Contributing

Found a bug? Built a new skill? [Open an issue](https://github.com/S3YED/appie-kit/issues) or pull request.

For skill contributions: follow the SKILL.md frontmatter format, include a description, prerequisites, and at least a basic usage section. Drop it in the appropriate category directory.

---

## License

MIT. Use it, modify it, build on it.

---

Built by [Seyed Hosseini](https://weblyfe.nl) at Weblyfe.
