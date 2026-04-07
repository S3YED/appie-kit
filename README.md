# 🧙🏽‍♂️ Appie Kit — Build Your Own AI Employee

> The same system that runs 3 AI agents managing a real web design agency. Now yours.

[![OpenClaw](https://img.shields.io/badge/Powered%20by-OpenClaw-031D16?style=for-the-badge)](https://github.com/openclaw/openclaw)
[![License: MIT](https://img.shields.io/badge/License-MIT-DFB771?style=for-the-badge)](LICENSE)

## What Is This?

This is the **exact configuration, tools, and learnings** from running [Weblyfe](https://weblyfe.ai) — a web design agency powered by 3 AI employees (we call them Appies) that handle:

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

## Quick Start (5 minutes)

### Prerequisites
- [OpenClaw](https://github.com/openclaw/openclaw) installed
- An OpenRouter API key (MiniMax M2.7 recommended)
- A Telegram bot token (optional, for messaging)



### Recommended: MiniMax M2.7 via OpenRouter (17x cheaper)

The default recommendation for v4.4 is **MiniMax M2.7** via OpenRouter:
- Cost: ~$0.01/1M tokens (vs $3.50/1M for Claude Opus)
- Quality: equivalent to GPT-4 class
- Setup: Get an OpenRouter key at [openrouter.ai](https://openrouter.ai) and set it as your model provider

For full comparison and setup: see the [Build Your Own Appie PDF v4.4](https://weblyfe.ai/guide/Build-Your-Own-Appie-v4.pdf).

### 1. Clone & install

```bash
git clone https://github.com/S3YED/appie-kit.git
cd appie-kit
./install.sh /path/to/your/openclaw/workspace/
```

### 2. Customize your files

```bash
nano SOUL.md        # Who your AI is (personality, values, voice)
nano USER.md        # Who you are (name, timezone, preferences)
nano TOOLS.md       # What tools it can use (API references)
```

### 3. Set up environment

```bash
cp .env.example .env.secrets
chmod 600 .env.secrets
nano .env.secrets   # Fill in your API keys
```

### 4. Start your Appie

```bash
openclaw gateway start
```

That's it. Your AI employee is live.

---

## What's Inside

```
appie-kit/
├── workspace/          # Core AI personality & behavior files
│   ├── AGENTS.md       # Operating rules, safety, group chat behavior
│   ├── SOUL.md         # Personality, values, communication style
│   ├── USER.md         # Info about you (timezone, preferences)
│   ├── TOOLS.md        # Available tools and API references
│   ├── IDENTITY.md     # Multi-agent identity (for fleets)
│   ├── HEARTBEAT.md    # Proactive check-in configuration
│   └── memory/         # Persistent memory directory
├── tools/              # Production shell scripts
│   ├── setup-openclaw-mac.sh    # Full Mac setup
│   ├── setup-openclaw-vps.sh    # VPS setup (Ubuntu/Debian)
│   ├── security-scan.sh         # Scan for exposed secrets & bad permissions
│   ├── health-check.sh          # Fleet health monitoring
│   ├── session-manager.sh       # Clean stale sessions, manage memory
│   └── safe-gateway-restart.sh  # Zero-downtime gateway restart
├── configs/            # Platform configuration examples
│   ├── telegram.example.yml     # Telegram bot setup
│   ├── discord.example.yml      # Discord bot setup
│   ├── whatsapp.example.yml     # WhatsApp integration
│   └── multi-agent.example.yml  # Multi-agent fleet setup
├── prompts/            # Production-tested prompt library
│   ├── business-automations.md  # Lead capture, CRM, proposals
│   ├── content-creation.md      # Blog, social, video content
│   ├── customer-support.md      # Support workflows
│   └── development-ops.md       # DevOps, deployments, monitoring
├── case-studies/       # Real-world examples with numbers
│   ├── weblyfe-agency.md        # 3-agent agency fleet
│   ├── lead-automation.md       # Automated lead pipeline
│   └── content-pipeline.md      # AI content generation
├── video/              # Launch video production docs
│   ├── PRODUCTION.md            # Scene-by-scene production bible
│   └── RESEARCH-CHARACTER-CONSISTENCY.md
├── install.sh          # One-command installer
├── .env.example        # Environment variables template
└── LICENSE             # MIT
```

---

## The Weblyfe Stack

The tools we use and recommend:

| Category | Tool | Why |
|----------|------|-----|
| **AI Brain** | MiniMax M2.7 (OpenRouter) | 17x cheaper than Claude, same quality |
| **Framework** | [OpenClaw](https://github.com/openclaw/openclaw) | Open source, self-hosted, persistent memory |
| **Messaging** | Telegram | Best bot API, instant delivery, groups |
| **Websites** | Webflow | Visual builder, CMS, no-code |
| **CRM** | Airtable | Flexible, API-first, automatable |
| **Email** | Brevo | Transactional + marketing, generous free tier |
| **Proposals** | Offorte | API + MCP server, e-signatures |
| **Automation** | n8n | Self-hosted, 400+ integrations |
| **Hosting** | Vercel | Zero-config deploys, edge functions |
| **VPS** | DigitalOcean | Simple, affordable, good API |
| **Networking** | Tailscale | Zero-config VPN, secure remote access |
| **Voice** | ElevenLabs | Natural TTS, voice cloning |
| **Video** | fal.ai (Kling 3.0) | Best character consistency, 4K |
| **Search** | Exa | AI-native search API |
| **Desktop Agent** | [Clawd Cursor](https://clawdcursor.com) | Screen control, universal app automation |

---

## Case Studies

### 1. Lead Capture Automation
**Before:** Manually checking email, copying leads to spreadsheet, sending follow-ups.
**After:** Form → Airtable lead → Brevo list → Confirmation email → Auto follow-up timing.
**Result:** 0 manual steps, <2 second end-to-end, 24/7 capture.

### 2. Multi-Agent Fleet (3 Appies)
**Setup:** Appie-1 (Orchestrator, Mac Mini), Appie-2 (Marketing, VPS), Appie-3 (DevOps, VPS).
**Cost:** ~$148/month total for 3 AI employees working 24/7.
See [`configs/multi-agent.example.yml`](configs/multi-agent.example.yml) for setup details.

### 3. Content Pipeline
**Input:** One brand brief or topic idea.
**Output:** AI video (Kling 3.0) + voiceover (ElevenLabs) + social posts + blog draft.
**Time:** 15 minutes vs 4+ hours manual.

### 4. Desktop Automation (Clawd Cursor)
**Problem:** Every SaaS tool needs its own API integration, keys, auth flows, rate limits.
**Solution:** [Clawd Cursor](https://clawdcursor.com) gives your Appie eyes and hands. It sees your screen and controls your cursor.
**Result:** One skill replaces dozens of API integrations. If you can click it, your agent can too.
**Cost:** $0 for simple tasks (local Ollama), ~$0.01 for complex multi-app workflows.

[Full case studies →](case-studies/)

---

## Brand Values

Everything in this kit reflects these values:

1. **Always Be Kind** — Your AI should be warm and respectful
2. **Always Help** — Go beyond the minimum, anticipate needs
3. **Value Life and Humanity** — AI serves humans, not the other way around
4. **Spread Positivity** — Optimism is a strategy
5. **Expand Abundance** — Create more than you consume

---

## Security

This repo contains **zero secrets**. All API keys and tokens use placeholders.

Before going live:
- [ ] Review `SOUL.md` for any personal info
- [ ] Check `.env.secrets` has no real keys committed
- [ ] Run `tools/security-scan.sh` after setup
- [ ] Set file permissions: `chmod 600 .env.secrets`
- [ ] Use Tailscale for remote access (never expose SSH publicly)

---

## Contributing

Found a bug? Built a cool skill? [Open an issue](https://github.com/S3YED/appie-kit/issues) or PR.

---

## License

MIT — Use it, modify it, sell it, whatever. Just don't blame us if your AI orders 1000 pizzas.

---

Built by [Seyed Hosseini](https://instagram.com/seyed.jpg) at [Weblyfe](https://weblyfe.ai).

Powered by [OpenClaw](https://github.com/openclaw/openclaw) and [Claude](https://anthropic.com).

*"From doctor to automation architect. If I can do it, you can too."*
