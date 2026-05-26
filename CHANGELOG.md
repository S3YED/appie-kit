# Changelog

All notable changes to Appie Kit are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## v4.4 (May 2026)

### Added
- 156 production skills organized into 8 categories: automation, communication, content, integrations, knowledge, meta, ops, personal.
- Skills extracted from the live Appie fleet (Mac Mini, Spark Atlas, Hetzner nodes, Wolfdiddy). Each skill is ready to drop into any Hermes or OpenClaw workspace.
- `skills/integrations/spark-comfy/`: Spark Atlas ComfyUI client for Tailnet-only image generation. Indexed into the integrations library and category listings.
- Hermes Agent compatibility across all skills. Skills were originally OpenClaw-only; the v4.4 fleet runs primarily on Hermes Agent (Nous Research).
- `skills/INDEX.md`: master skill index with per-category counts and links.
- Per-category INDEX.md and README.md files inside each skill category.
- `skills/content/`: 49 skills covering UI/UX design, image generation, video production, SEO, copywriting, Next.js, TTS, stable diffusion, and more.
- `skills/knowledge/`: 22 skills for LLM fine-tuning (LoRA, GRPO, DPO), quantization (GGUF, llama.cpp), vLLM inference, Whisper STT, DSPy, model evaluation.
- `skills/integrations/`: 32 skills for Airtable, Notion, Google Workspace, GitHub, n8n, fal.ai, Spotify, Webflow, Trello, Gemini, Oracle, and others.
- `skills/ops/`: 16 skills for infrastructure management, git workflows, tmux, 1Password, healthcheck, and fleet maintenance.
- `skills/automation/`: 19 skills including ClawFlow multi-step workflows, kanban orchestration, parallel agent dispatch, brain-sync, and memory search.
- `skills/communication/`: 6 skills for Telegram, Discord, Slack, iMessage (BlueBubbles), WhatsApp (wacli), and voice calls.
- `skills/meta/`: 8 skills for skill authoring, ClawHub registry, task planning, dogfood QA, and brainstorming.
- `skills/personal/`: 4 skills for Bear Notes, Spotify, Things 3, and weather (macOS).
- `tools/hermes-agent-install.sh`: automated Hermes Agent setup script for VPS (Ubuntu/Debian).
- `.env.example` expanded with Pinecone, Supermemory, fal.ai, and additional Google Workspace entries.

### Changed
- Default AI model recommendation updated from Claude to **MiniMax M2.7 via OpenRouter** (~$0.01/1M tokens, 17x cheaper than Claude Opus at equivalent quality).
- `install.sh` updated to handle the new nested `skills/<category>/<skill>/` directory structure.
- README fully rewritten for v4.4 with category tables, updated stack, and new highlights section.

### Fixed
- Skills install path now correctly copies `skills/<category>/<skill>/` into target, preserving category structure.

---

## v4.3 (April 2026)

### Added
- `tools/hermes-agent-install.sh`: automated Hermes Agent setup for VPS nodes (commit `6e30d8e`).
- Technical skills, fleet patterns, and operational learnings documented and organized (commit `24dc1d5`).

---

## v4.2 (April 2026)

### Added
- `skills/frontend-design-3/`: production-grade UI skill (React, Next.js, motion systems, gradient meshes).
- `skills/ui-ux-pro-max/`: design decision engine: 67+ UI styles, 161 palettes, 57 font pairings, 99 UX guidelines.
- `skills/tips-landing-pages/`: TIPS conversion framework for landing pages.
- `skills/anthropics-frontend-design/`: lightweight frontend companion skill (commit `2cd326b`).
- Clawd Cursor desktop automation case study and stack reference (commit `49f3bf9`).

---

## v4.1 (March 2026)

### Added
- MiniMax M2.7 support documented as primary AI model recommendation (commit `a0d7c56`).

---

## v1.1 (2025)

### Changed
- Repo structure cleaned up: configs, tools, workspace directories organized.
- README rewritten with Quick Start, stack table, and case studies.
- `.env.example` introduced for safe key management (commit `fb9fa21`).

---

## v1.0 (2025)

Initial release (commit `873c83f`).

### Added
- Core workspace files: SOUL.md, USER.md, TOOLS.md, AGENTS.md, IDENTITY.md, HEARTBEAT.md.
- 33 initial AgentSkills across design, development, content, SEO, infrastructure, research, and persona categories.
- Production shell scripts: setup-openclaw-mac.sh, setup-openclaw-vps.sh, security-scan.sh, health-check.sh, session-manager.sh, safe-gateway-restart.sh.
- Platform config examples: Telegram, Discord, WhatsApp, multi-agent fleet.
- Prompt library: business automations, content creation, customer support, development ops.
- Case studies: lead capture automation, multi-agent fleet, content pipeline.
- `install.sh` one-command installer.
- MIT license.
