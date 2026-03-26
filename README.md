# 🧙🏽‍♂️ Appie Kit — Build Your Own AI Employee

> The same system that runs 3 AI agents managing a real web design agency. Now yours.

[![OpenClaw](https://img.shields.io/badge/Powered%20by-OpenClaw-031D16?style=for-the-badge)](https://github.com/openclaw/openclaw)
[![License: MIT](https://img.shields.io/badge/License-MIT-DFB771?style=for-the-badge)](LICENSE)

## What Is This?

This is the **exact configuration, skills, tools, and learnings** from running [Weblyfe](https://weblyfe.ai) — a web design agency powered by 3 AI employees (we call them Appies) that handle:

- 📧 Email triage and responses
- 📅 Calendar management
- 🎯 Lead capture and CRM automation
- 📝 Proposal generation and tracking
- 🌐 Website builds and deployments
- 📊 Competitor monitoring
- 🔒 Security scanning
- 💬 Customer support across Telegram, WhatsApp, Discord
- 🎬 AI video and content generation

**This is not a chatbot.** This is a digital team member that works 24/7, learns from mistakes, and gets stronger every day.

## Quick Start (5 minutes)

### Prerequisites
- [OpenClaw](https://github.com/openclaw/openclaw) installed
- An Anthropic API key (Claude)
- A Telegram bot token (optional, for messaging)

### 1. Clone this repo
```bash
git clone https://github.com/S3YED/appie-kit.git
cd appie-kit
```

### 2. Copy workspace files into your OpenClaw directory
```bash
# Copy the workspace template into your OpenClaw working directory
cp -r workspace/* /path/to/your/openclaw/workspace/

# Or if you want the full kit with tools:
./install.sh /path/to/your/openclaw/workspace/
```

### 3. Customize your files
Edit these files to make it yours:
```bash
# Who your AI is
nano workspace/SOUL.md        # Personality, values, voice

# Who you are
nano workspace/USER.md         # Your name, timezone, preferences

# What tools it can use
nano workspace/TOOLS.md        # API keys, services, platforms
```

### 4. Set up your environment
```bash
cp .env.example .env
# Fill in your API keys
nano .env
```

### 5. Start your Appie
```bash
openclaw gateway start
```

That's it. Your AI employee is live.

---

## What's Inside

### 📂 `/workspace` — Drag & Drop Configuration
The core files that define your AI's personality, memory, and behavior. Copy these directly into your OpenClaw workspace.

| File | Purpose |
|------|---------|
| `AGENTS.md` | How your AI operates, safety rules, group chat behavior |
| `SOUL.md` | Personality, values, communication style |
| `USER.md` | Info about you (timezone, preferences, contacts) |
| `TOOLS.md` | Available tools and API references |
| `IDENTITY.md` | Multi-agent identity (if running a fleet) |
| `HEARTBEAT.md` | Proactive check-in configuration |

### 🛠 `/skills` — Battle-Tested Capabilities
Skills we've built and refined over months of production use:

| Skill | What It Does |
|-------|-------------|
| `lead-capture` | Captures leads from web forms → Airtable + Brevo + confirmation email |
| `competitor-watch` | Monitors competitors weekly, generates reports |
| `security-scan` | Daily security audit (exposed keys, permissions, ports) |
| `health-monitor` | Checks fleet health across multiple machines |
| `email-automation` | Brevo template management + transactional emails |
| `content-factory` | AI-generated content pipeline (video + voice + social) |
| `deploy-helper` | Git push → Vercel deployment with safety checks |
| `memory-manager` | Long-term memory with Supermemory + local files |

### 🔧 `/tools` — Utility Scripts
Production-hardened shell scripts and Node.js tools:

| Tool | Purpose |
|------|---------|
| `setup-openclaw-mac.sh` | Full Mac setup (Homebrew, Node, OpenClaw, config) |
| `setup-openclaw-vps.sh` | VPS setup (Ubuntu/Debian, firewall, Tailscale) |
| `security-scan.sh` | Scan for exposed secrets, bad permissions, open ports |
| `session-manager.sh` | Clean stale sessions, manage memory |
| `token-guard.sh` | Auto-refresh OAuth tokens before expiry |
| `health-check.sh` | Fleet health monitoring |
| `safe-gateway-restart.sh` | Zero-downtime gateway restart |
| `namecheap.sh` | Domain DNS management via API |

### 📋 `/configs` — Platform Templates
Example configurations for every supported platform.

### 📖 `/case-studies` — Real Examples
How Weblyfe actually uses this system in production. Real numbers, real workflows, real results.

### 📝 `/prompts` — Ready-Made Prompt Library
20+ production-tested prompts for common business tasks.

### 📚 `/docs` — The Full Guide
The complete "Build Your Own Appie" guide as markdown (also available as [PDF](https://weblyfe.ai/openclaw)).

---

## The Weblyfe Software Stack

This is the stack we use and recommend:

| Category | Tool | Why |
|----------|------|-----|
| **AI Brain** | Claude (Anthropic) | Best reasoning, tool use, and safety |
| **Framework** | OpenClaw | Open source, self-hosted, persistent memory |
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
| **DNS** | Namecheap | Cheap domains, good API |
| **Version Control** | GitHub | Standard, Actions, Pages |

---

## Case Studies

### 1. Lead Capture Automation
**Before:** Manually checking email, copying leads to spreadsheet, sending follow-ups.
**After:** Form submission → Airtable lead created → Brevo list updated → Confirmation email sent → Appie monitors for follow-up timing.
**Result:** 0 manual steps, <2 second end-to-end, 24/7 capture.

### 2. Multi-Agent Fleet (3 Appies)
**Setup:** Appie-1 (Orchestrator, Mac Mini), Appie-2 (Marketing, VPS), Appie-3 (DevOps, VPS)
**Each agent** has its own personality, skills, and responsibilities.
**Communication:** Via Tailscale VPN, direct SSH, or message relay.
**Cost:** ~$50/month total infrastructure.

### 3. Content Pipeline
**Input:** One brand brief or topic idea.
**Output:** AI-generated video (Kling 3.0) + voiceover (ElevenLabs) + social media posts (Buffer) + blog draft.
**Time:** 15 minutes vs 4+ hours manual.

[See full case studies →](case-studies/)

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

This repo contains **zero secrets**. All API keys, tokens, and personal data use placeholders.

Before going live:
- [ ] Review `SOUL.md` for any personal info
- [ ] Check `.env` has no real keys committed
- [ ] Run `tools/security-scan.sh` after setup
- [ ] Set file permissions: `chmod 600 .env .env.secrets`
- [ ] Use Tailscale for remote access (never expose SSH publicly)

---

## Contributing

Found a bug? Built a cool skill? [Open an issue](https://github.com/S3YED/appie-kit/issues) or PR.

---

## License

MIT — Use it, modify it, sell it, whatever. Just don't blame us if your AI orders 1000 pizzas.

---

## Credits

Built by [Seyed Hosseini](https://instagram.com/seyed.jpg) at [Weblyfe](https://weblyfe.ai).

Powered by [OpenClaw](https://github.com/openclaw/openclaw) and [Claude](https://anthropic.com).

*"From doctor to automation architect. If I can do it, you can too."*
