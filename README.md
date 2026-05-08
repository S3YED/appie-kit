# 🧙🏽‍♂️ Appie Kit: Build Your Own AI Employee

> The same system that runs a real web design agency, now with 155 production skills extracted from a live 7-agent fleet.

[![Hermes Agent](https://img.shields.io/badge/Powered%20by-Hermes%20Agent-031D16?style=for-the-badge)](https://github.com/NousResearch/hermes-agent)
[![OpenClaw](https://img.shields.io/badge/Also%20works%20with-OpenClaw-0a4020?style=for-the-badge)](https://github.com/openclaw/openclaw)
[![Skills](https://img.shields.io/badge/Skills-155%20public%20%7C%20302%20total-DFB771?style=for-the-badge)](skills/INDEX.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-555?style=for-the-badge)](LICENSE)

## What Is This?

This is the **exact configuration, tools, and skills** extracted from running [Weblyfe](https://weblyfe.ai): a web design agency powered by AI employees (Appies) that handle:

- 📧 Email triage and responses
- 📅 Calendar management
- 🎯 Lead capture and CRM automation
- 📝 Proposal generation and tracking
- 🌐 Website builds and deployments
- 📊 Competitor monitoring
- 🔒 Security scanning
- 💬 Customer support across Telegram, WhatsApp, Discord

**This is not a chatbot.** This is a digital team member that works 24/7, learns from mistakes, and gets stronger every day.

---

## What's New in v4.4

Released April 2026, going public May 2026.

- **155 deduped public skills** consolidated from 800+ raw skills across the full Appie fleet (Mac Mini, Spark Atlas, Hetzner nodes, Wolfdiddy). Up from 33 in v4.3.
- **Hermes Agent compatibility** across the board. Skills were originally OpenClaw-only; the fleet now runs primarily on [Hermes Agent](https://github.com/NousResearch/hermes-agent).
- **MiniMax M2.7 as the default model** via OpenRouter: 17x cheaper than Claude at GPT-4 class quality.
- **fal.ai + RunPod media stack** for image and video generation (Kling, Nano Banana, ComfyUI workers).
- **UI/UX Pro Max design framework**: 67+ UI styles, 161 palettes, 57 font pairings, 99 UX guidelines bundled as a skill.
- **9-category skill layout**: automation, communication, content, integrations, knowledge, meta, ops, personal + unsorted.

Full setup guide: [Build Your Own Appie PDF v4.4](https://weblyfe.ai/store)

---

## Quick Start (5 minutes)

### Prerequisites
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) installed (or [OpenClaw](https://github.com/openclaw/openclaw))
- An OpenRouter API key (MiniMax M2.7 recommended, ~$0.01/1M tokens)
- A Telegram bot token (optional, for messaging interface)

### Recommended: MiniMax M2.7 via OpenRouter

The default for v4.4 is **MiniMax M2.7** via OpenRouter:

- Cost: ~$0.01/1M tokens (vs $3.50/1M for Claude Opus)
- Quality: equivalent to GPT-4 class
- Setup: get an OpenRouter key at [openrouter.ai](https://openrouter.ai)

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
# or copy entire categories:
cp -r skills/content/* ~/.hermes/skills/
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

That's it. Your AI employee is live.

---

## Skills by Category

155 public skills across 8 categories. Each category has its own index.

| Category | Net Skills | What it covers |
|---|---|---|
| [automation](skills/automation/INDEX.md) | 19 | Agent self-management, fleet coordination, brain sync, sub-agent spawning, ClawFlow workflows |
| [communication](skills/communication/INDEX.md) | 6 | Telegram, Discord, Slack, iMessage (BlueBubbles), WhatsApp (wacli), voice calls |
| [content](skills/content/INDEX.md) | 49 | UI/UX design, image gen, video production, SEO, copywriting, Next.js, TTS, stable diffusion |
| [integrations](skills/integrations/INDEX.md) | 31 | Airtable, Notion, Google Workspace, GitHub, n8n, fal.ai, Spotify, Webflow, Trello, Gemini |
| [knowledge](skills/knowledge/INDEX.md) | 22 | LLM fine-tuning (LoRA/GRPO), quantization, vLLM, Whisper STT, DSPy, model evaluation |
| [meta](skills/meta/INDEX.md) | 8 | Skill authoring, ClawHub registry, task planning, dogfood QA, brainstorming frameworks |
| [ops](skills/ops/INDEX.md) | 16 | GitHub/git, DigitalOcean, tmux, 1Password, healthcheck, session management, fleet maintenance |
| [personal](skills/personal/INDEX.md) | 4 | Bear Notes, Spotify, Things 3 (macOS), weather |

Total raw across fleet: 302 unique skills. 147 are Hermes builtins that ship with every Hermes install and are therefore not duplicated here.

---

## Skills Highlights

### Design and Creative

| Skill | Description |
|---|---|
| [frontend-design-3](skills/content/frontend-design-3/) | Production-grade UI (React, HTML/CSS, Next.js, Vue). Bold typography, motion systems, gradient meshes |
| [ui-ux-pro-max](skills/content/ui-ux-pro-max/) | Design decision engine: 67+ UI styles, 161 palettes, 57 font pairings, 99 UX guidelines |
| [tips-landing-pages](skills/content/tips-landing-pages/) | Conversion-optimized landing pages using the TIPS framework |
| [21st-dev](skills/content/21st-dev/) | Install shadcn/ui-compatible React components from 21st.dev registry |
| [design](skills/content/design/) | Logo generation (55 styles), CIP mockups (50 deliverables), banners, icons, social |
| [design-mastery](skills/content/design-mastery/) | Core design knowledge: hierarchy, spacing, typography, color, depth, UX laws |
| [design-system](skills/content/design-system/) | Token architecture, three-layer tokens (primitive/semantic/component), CSS variables |
| [ui-styling](skills/content/ui-styling/) | shadcn/ui + Tailwind CSS. Accessible components, dark mode, responsive layouts |
| [banner-design](skills/content/banner-design/) | Multi-format banners across 22 art styles |
| [brand](skills/content/brand/) | Brand identity, voice, messaging frameworks, design tokens |
| [slides](skills/integrations/slides/) | Strategic HTML presentations with Chart.js and design tokens |

### Development

| Skill | Description |
|---|---|
| [nextjs-expert](skills/content/nextjs-expert/) | Next.js 15 App Router specialist. Server Components, auth, caching, streaming |
| [coding](skills/automation/coding/) | Code quality guidelines, patterns, security rules, debugging workflow |
| [gitclaw](skills/ops/gitclaw/) | Automated workspace backup to GitHub via crontab |
| [architecture-diagram](skills/content/architecture-diagram/) | Generate system architecture diagrams from descriptions |
| [github](skills/integrations/github/) | GitHub repository management, PR review, issue tracking |

### Content and Media

| Skill | Description |
|---|---|
| [agentic-video-tools](skills/content/agentic-video-tools/) | Compare and automate agentic video editing APIs (Vizard, Submagic, Descript) |
| [video-editing-pro](skills/content/video-editing-pro/) | Cut-decision framework for short-form video. Hook precision, energy curve, captions |
| [appie-video-production](skills/content/appie-video-production/) | End-to-end AI video production pipeline |
| [viral-shorts-course](skills/content/viral-shorts-course/) | System for producing viral short-form video content |
| [seo-checklist](skills/content/seo-checklist/) | Pre-publish on-page SEO checklist: title, meta, H1, images, breadcrumbs |
| [content-creation](skills/content/content-creation/) | Structured content creation across formats and platforms |

### Infrastructure and DevOps

| Skill | Description |
|---|---|
| [digital-ocean](skills/ops/digital-ocean/) | Manage DigitalOcean droplets, domains, infrastructure via DO API |
| [n8n](skills/integrations/n8n/) | Interact with n8n workflows: list, trigger, monitor, manage automations |
| [n8n-pro](skills/integrations/n8n-pro/) | Advanced n8n operations, backup, hardening, Telegram alerts |
| [healthcheck](skills/ops/healthcheck/) | Fleet health monitoring and alerting |
| [web-scraping-javascript-sites](skills/automation/web-scraping-javascript-sites/) | Scrape SPA/React sites. urllib-first strategy, Playwright fallback, stealth mode |

### Research and Search

| Skill | Description |
|---|---|
| [exa-plus](skills/integrations/exa-plus/) | Neural web search via Exa AI. People, companies, news, research, code |
| [read-github](skills/integrations/read-github/) | Read GitHub repos via gitmcp.io. Semantic search, zero hallucination on structure |

### Automation

| Skill | Description |
|---|---|
| [clawflow](skills/automation/clawflow/) | Multi-step task execution spanning detached background jobs |
| [kanban-orchestrator](skills/automation/kanban-orchestrator/) | Decomposition playbook and specialist-roster conventions for parallel work |
| [dispatch-multiple-agents](skills/automation/dispatch-multiple-agents/) | Spawn 2+ independent agents in parallel for independent tasks |
| [brain-sync](skills/automation/brain-sync/) | Sync knowledge and learnings to the shared appie-brain repo |
| [memory-search](skills/automation/memory-search/) | Search and retrieve from the Appie brain: daily logs, project notes, topics |

---

## What's Inside

```
appie-kit/
├── workspace/          # Core agent identity and behavior files
│   ├── SOUL.md         # Personality, values, communication style
│   ├── USER.md         # Who you are: timezone, preferences, context
│   ├── TOOLS.md        # Available tools and API references
│   ├── AGENTS.md       # Operating rules, safety, group chat behavior
│   ├── IDENTITY.md     # Multi-agent identity (for fleets)
│   ├── HEARTBEAT.md    # Proactive check-in configuration
│   └── memory/         # Persistent memory directory
├── skills/             # 155 public skills, 8 categories
│   ├── automation/     # Agent self-management, fleet coordination
│   ├── communication/  # Messaging platform integrations
│   ├── content/        # Design, video, SEO, copywriting, frontend
│   ├── integrations/   # Third-party APIs and SaaS connectors
│   ├── knowledge/      # ML/AI fine-tuning, search, research
│   ├── meta/           # Skill authoring, planning, QA
│   ├── ops/            # Infrastructure, git, DevOps
│   ├── personal/       # Notes, tasks, music (macOS)
│   └── INDEX.md        # Master skill index with counts
├── tools/              # Production shell scripts
│   ├── setup-openclaw-mac.sh    # Full Mac setup
│   ├── setup-openclaw-vps.sh    # VPS setup (Ubuntu/Debian)
│   ├── hermes-agent-install.sh  # Install Hermes Agent on VPS
│   ├── security-scan.sh         # Scan for exposed secrets
│   ├── health-check.sh          # Fleet health monitoring
│   ├── session-manager.sh       # Clean stale sessions
│   └── safe-gateway-restart.sh  # Zero-downtime gateway restart
├── configs/            # Platform configuration examples
│   ├── telegram.example.yml
│   ├── discord.example.yml
│   ├── whatsapp.example.yml
│   └── multi-agent.example.yml
├── prompts/            # Production-tested prompt library
├── case-studies/       # Real-world examples with numbers
├── install.sh          # One-command installer
├── .env.example        # Environment variables template
├── CONTRIBUTING.md     # How to add skills and contribute
├── CHANGELOG.md        # Version history
└── LICENSE             # MIT
```

---

## The Weblyfe Stack

| Category | Tool | Why |
|---|---|---|
| AI model | MiniMax M2.7 (OpenRouter) | 17x cheaper than Claude, GPT-4 class quality |
| Agent framework | Hermes Agent (Nous Research) | Open source, persistent memory, multi-platform |
| Alternative framework | OpenClaw | macOS-native, good for desktop automation |
| Messaging | Telegram | Best bot API, instant delivery, group support |
| CRM | Airtable | Flexible, API-first, automatable |
| Automation | n8n | Self-hosted, 400+ integrations |
| Hosting | Vercel | Zero-config deploys, edge functions |
| VPS | DigitalOcean | Simple API, affordable |
| Networking | Tailscale | Zero-config VPN for fleet communication |
| Image gen | fal.ai (Nano Banana) | Fast, cost-effective, consistent results |
| Video gen | fal.ai (Kling 3.0) | Best character consistency, 4K |
| Search | Exa | AI-native search API, better than Google for research |
| Desktop agent | Clawd Cursor | Screen control, universal app automation |

---

## Case Studies

### Lead capture automation

Before: manual email checks, copy-paste to spreadsheet, manual follow-ups.
After: Form submission triggers Airtable record, Brevo list entry, confirmation email, and timed follow-up sequence.
Result: 0 manual steps, under 2 seconds end-to-end, 24/7.

### Multi-agent fleet (3 Appies)

Appie-1 (Orchestrator, Mac Mini), Appie-2 (Marketing, VPS), Appie-3 (DevOps, VPS).
Cost: ~$148/month for 3 AI employees running continuously.
Setup: [configs/multi-agent.example.yml](configs/multi-agent.example.yml)

### Content pipeline

Input: one brand brief or topic idea.
Output: AI video (Kling 3.0) + voiceover + social posts + blog draft.
Time: 15 minutes vs 4+ hours manual.

### Desktop automation (Clawd Cursor)

Problem: every SaaS tool needs its own API integration, keys, auth flows, rate limits.
Solution: Clawd Cursor gives your Appie eyes and hands. It sees your screen and controls your cursor.
Result: one skill replaces dozens of API integrations. If you can click it, your agent can too.

[Full case studies](case-studies/)

---

## Brand Values

1. **Always Be Kind**: Your AI should be warm and respectful
2. **Always Help**: Go beyond the minimum, anticipate needs
3. **Value Life and Humanity**: AI serves humans, not the other way around
4. **Spread Positivity**: Optimism is a strategy
5. **Expand Abundance**: Create more than you consume

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

## Resources

- v4.4 guide: [Build Your Own Appie PDF](https://weblyfe.ai/store)
- Hermes Agent: [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- OpenClaw: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- MiniMax M2.7 via OpenRouter: [openrouter.ai](https://openrouter.ai)
- [CONTRIBUTING.md](CONTRIBUTING.md): how to add skills and contribute
- [CHANGELOG.md](CHANGELOG.md): version history

---

## License

MIT: Use it, modify it, build on it. Just don't blame us if your AI orders 1000 pizzas.

---

Built by [Seyed Hosseini](https://instagram.com/seyed.jpg) at [Weblyfe](https://weblyfe.ai).

Powered by [Hermes Agent](https://github.com/NousResearch/hermes-agent) and [OpenClaw](https://github.com/openclaw/openclaw).

*"From doctor to automation architect. If I can do it, you can too."*
