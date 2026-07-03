## 2026-07-03 — Fleet sync import: refero-design, creative ideation, component refactoring, content intelligence

- Imported 4 new skills (667 → 671 SKILL.md, 632 → 636 unique names).
- From **appie-2 (Seyed's agent)**: `refero-design` — Seyed's primary research-first design methodology (skills/design); `react-component-refactoring` — safe large-React-component splitting patterns (skills/software-development); `short-form-content-intelligence` — reels-only opportunity market research (skills/content).
- From **eugi**: `creative-ideation` — 20+ named ideation methods from creative practice, authored by SHL0MS (skills/creative). Created 2026-07-02.
- Skipped: `weblyfe-landing-page` (Weblyfe-specific, not generic enough for fleet reuse), `world-solutions-project` and `petdex` (personal), `wai-tenant-provisioning` (client secrets), `computer-use` (already covered by `macos-computer-use`), `google-maps-*` (niche prospecting), all archived skills on appie-2, `czΩa-database-migrations` and `n8n-pro` (host-specific).
- **Fleet broadcast:** pending (appie-2 already has these skills; eugi needs `refero-design` and `react-component-refactoring`).

## 2026-07-01 — Fleet sync import: n8n deep skills, macOS Computer Use, GWS recipes

- Imported 10 new skills across 3 categories (656 → 666 total).
- From **appie-2**: 7 n8n technical deep-dive skills (agents, binary/data, code tool, error handling, multi-instance, self-hosting, subworkflows).
- From **eugi**: `macos-computer-use` — background macOS desktop automation driver (added to ops).
- From **appie-2**: 2 GWS recipes (collect form responses, create classroom course) added to openclaw-imports.
- Skipped: `jenny-voice` (personal to eugi), `fleet-inventory` (embedded in security-scanning, not standalone).
- **Fleet refresh:** appie-2, appie-3-hermes, eugi all reachable. Broadcast pending.

## 2026-06-30 — Fleet sync import from eugi\n\n- Imported 10 new agentic and operations skills from eugi (total 656).\n- Created 'Agentic  Loops' category index.\n- Verified reachability for appie-2, appie-3, eugi.\n\n# Changelog

All notable changes to Appie Kit are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## v4.5 (2026-06-06)

### Added 2026-06-29
- `kanban-codex-lane` from appie-2 fleet sync: Hermes Kanban + Codex dual-lane pattern for bounded implementation tasks. Added to `skills/autonomous-ai-agents/`.
- Cleaned up duplicate `skills/knowledge/research/web-research/` — canonical copy at `skills/research/web-research/`.

### Changed 2026-06-26
- INDEX.md, SKILLS.md, CHANGELOG.md counts updated to reflect 598 skills (585 → 598) following yesterday's 13-skill commit (GitHub workflows, media gen, mlops, persona).



### Added
- 5 fleet skills from `appie-3-hermes`: `cto-intelligence` (cron-based tech monitoring), `hermes-gateway-troubleshooting` (Hermes gateway diagnostics), `travel-accommodation` (hotel/resort research), `travel-booking` (multi-leg SE Asia travel), and `webflow-seo-audit` (Webflow-specific SEO audit). Imported 2026-06-22.
### Added 2026-06-23
- `short-form-video-production` from `appie-2` fleet sync: umbrella skill for Reels, Shorts, and TikTok production covering ideation, retention, editing, captions, thumbnails, and tooling. Imported to `skills/content/`.
- 3 curated fleet skills from `appie-3-hermes`: `deployment-inspection`, `webhook-subscriptions`, and `web-research`; normalized `agent-browser` and `rtk-token-killer` into category directories. (added 2026-06-16)
- `configs/fleet-access.example.yml`, `docs/FLEET-ACCESS.md`, and `tools/validate-public-skills.py` for public-safe fleet host onboarding and pre-publish validation. (added 2026-06-14)
- `skills/integrations/spark-comfy/`: GPU/media worker ComfyUI client for Tailnet-only image generation via SDXL + FLUX schnell; style presets, queue + status polling, X-API-Key auth. (added 2026-05-26)
- 6 additional skills synced from live fleet across automation and meta categories, bringing total to **162 production skills**.
- 5 operational fleet skills from `appie-2`: `hermes-runtime-operations`, `ssh-access-recovery`, `content-production-workflow`, `seo-weblyfe`, and `travel-flight-research`. (added 2026-06-13)
- 3 operational fleet skills from `appie-1` and `appie-3-hermes`: `agent-fleet-operations`, `fleet-skill-sync`, and `client-bot-security`. (added 2026-06-14)
- `skills/ops/fleet-infra-fixes/`: recurring Appie fleet infrastructure fixes from `appie-2` / external worker, covering Node/simdjson breakage, deploy-key isolation, token reauth, and Tailscale Serve discipline. (added 2026-06-14)

### Changed
- Public skill indexes corrected to **557** after the 2026-06-20 fleet sync repaired the 16-skill import, removed four duplicate skill directories, and regenerated category indexes.
- Public skill indexes corrected to **545** after the 2026-06-19 fleet sync found 5 committed Higgsfield/viral-shorts content skills missing from category indexes.
- Removed duplicate `skills/ops/modal-serverless-gpu`; canonical `modal-serverless-gpu` remains under `skills/integrations/modal`.
- Public skill indexes updated to **540** after the 2026-06-16 fleet sync.
- README and SKILLS.md skill count updated from 156 to 162 (verified by `find skills -name SKILL.md | wc -l`).
- Public skill indexes reconciled with tracked `SKILL.md` files; total count is now **510** including the imported ECC set. (2026-06-13)
- Public skill indexes updated to **513** after the 2026-06-14 fleet sync.
- Public skill indexes updated to **514** after the follow-up 2026-06-14 fleet sync.
- Public tree sanitized and re-indexed to **526** public skills with private/client-specific material quarantined outside the repo. (2026-06-14)
- Per-category counts corrected: automation 19 -> 20, meta 8 -> 13.
- Version label updated from v4.4 to v4.5 to align with the [Build Your Own Techwiz PDF v4.5](https://weblyfe.ai/pdf) guide.

---

## v4.4 (May 2026)

### Added
- 156 production skills organized into 8 categories: automation, communication, content, integrations, knowledge, meta, ops, personal.
- Skills extracted from the live Appie fleet (Mac Mini, GPU/media workers, VPS nodes, and approved client-bot hosts). Each skill is ready to drop into any Hermes or OpenClaw workspace.
- `skills/integrations/spark-comfy/`: GPU/media worker ComfyUI client for Tailnet-only image generation. Indexed into the integrations library and category listings.
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
## 2026-06-28 — Fleet skill sync: 48 new skills imported from appie-2 and appie-3

- Imported 48 new skills across 13 categories (646 total, +48).
- Sources: appie-2 (30 skills: 14 active + 16 GWS/OpenClaw imports), appie-3 (14 skills), appie-1-local (5 skills).
- New categories added: autonomous-ai-agents, content-creation, creative, design, devops, github, media, openclaw-imports, productivity, red-teaming, research, seo, software-development.
- Updated google-drive with proper frontmatter and expanded capabilities.
- Created 13 category INDEX files for the new directories.
- Skipped: cto-intelligence (role-specific, 46KB), 2 archived skills.
- Fleet broadcast: pending — no appie-kit clone on fleet hosts (git push required).

## 2026-06-14 - Skill audit and hygiene pass

- Added evidence-backed origin/quality audit reports under `reports/skill-audit/2026-06-14/`.
- Added missing frontmatter descriptions to legacy Appie/Weblyfe skills so Hermes can trigger them reliably.
- Quarantined private/sensitive first-party skills under `skills/_quarantine/sensitive-review/` pending manual review instead of publishing them in the public index.
- Regenerated skill indexes and category counts from filesystem evidence.
