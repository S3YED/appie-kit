---
name: agentic-webdesign-html-anything
description: Install and use html-anything — the agentic HTML editor where your local AI agent writes HTML and you ship it. 75 skills × 9 surfaces, BYOK, zero API key. Use when building magazine articles, keynote decks, resumes, posters, social cards, web prototypes, data reports, or Hyperframes videos with AI coding agents.
author: Appie-1 (researched 2026-07-11)
tags: [html-anything, agentic-design, byok, claude-design-alternative, html-editor, skills, publishing]
---

# html-anything — Agentic HTML Editor

## What it is

html-anything is an **agentic HTML editor** from the [nexu-io](https://github.com/nexu-io) team (the same team behind Open Design, 40k+ stars). It turns any AI coding agent CLI into an HTML publishing engine.

**The pitch:** Markdown is the draft. HTML is what humans read. Your local agent writes it. One-click ship to WeChat/X/Zhihu/PNG.

## Quick facts

- **Repo:** https://github.com/nexu-io/html-anything
- **Stars:** 7,700+ (as of July 2026)
- **License:** Apache-2.0
- **Install:** `npm install -g @nexu-io/html-anything`
- **Runs on:** Local (`pnpm dev`) or Vercel (agent stays on your laptop)

## Supported coding agents

Auto-detected on PATH (including `~/.local/bin`, `~/.bun/bin`, `/opt/homebrew/bin`, `~/.npm-global/bin`):

| Agent | Detection | Invocation |
|-------|-----------|------------|
| Claude Code | `claude` | `claude -p --output-format stream-json` |
| OpenAI Codex | `codex` | `codex exec --json --sandbox workspace-write` |
| Cursor Agent | `cursor-agent` | `cursor-agent --print --output-format stream-json --force --trust` |
| Gemini CLI | `gemini` | `gemini --output-format stream-json --yolo` |
| GitHub Copilot | `copilot` | `copilot --allow-all-tools --output-format json` |
| OpenCode | `opencode-cli` / `opencode` | `opencode run --format json --dangerously-skip-permissions -` |
| Qwen Coder | `qwen` | `qwen --yolo -` |
| Aider | `aider` | `aider --no-pretty --no-stream --yes-always --message-file -` |

**No API key needed.** Reuses your existing CLI auth (`claude login`, `cursor login`, etc.).

## 75 skills × 9 surfaces

Skills live under `src/lib/templates/skills/` and follow the Claude Code `SKILL.md` convention with extended frontmatter (`mode`, `scenario`, `surface`, `preview`, `design_system`).

### Surfaces

| Surface | Mode | Skills |
|---------|------|--------|
| 📖 Magazine article | `prototype` | 7-12 |
| 🎬 Keynote deck | `deck` | 20 (Swiss International, Guizang Editorial, XHS Pastel, Hermes Cyber, Replit, Magazine Web...) |
| 📄 Résumé | `prototype` | Multiple |
| 🖼️ Poster | `prototype` | Multiple |
| 📱 Xiaohongshu card | `social` | Multiple |
| 🐦 Tweet card | `social` | Multiple |
| 🛠️ Web prototype | `prototype` | web, SaaS landing, dashboard, data report |
| 📊 Data report | `prototype` | Multiple |
| 🎞️ Hyperframes video | `frame` | 10 (liquid hero, NYT data chart, sticky-note flowchart, glitch title, cinema light-leak, macOS notification, logo outro...) |

### Office skills
`pm-spec`, `eng-runbook`, `finance-report`, `hr-onboarding`, `invoice`, `okrs`, `weekly-update`, `meeting-notes`, `kanban`

## One-click export targets

| Target | Method |
|--------|--------|
| WeChat | `juice` CSS inlining → paste with zero re-formatting |
| X/Twitter | `modern-screenshot` → 2× PNG → `ClipboardItem` |
| Zhihu | `<mjx-container>` → `data-eeimg` placeholder (equations auto-render) |
| HTML download | Standalone `.html` |
| PNG download | High-DPI `.png` |

## Architecture

```
Layer | Stack
------|------
Frontend | Next.js 16 App Router + Turbopack · React 19 · Tailwind v4 · zustand
Agent transport | `child_process.spawn` · one adapter per CLI
Browser processing | `juice` (CSS inline) · `modern-screenshot` (PNG) · `xlsx`/`papaparse` · `marked` + `highlight.js` · `dompurify`
Preview | `iframe[sandbox="allow-scripts allow-same-origin"]` + `srcdoc`
Export | `.html` standalone · `.png` high-DPI · `ClipboardItem` (text/html + image/png)

## Why it matters for AI agents

1. **BYOK is proven at scale.** 7,700+ stars, the same team behind Open Design (40k stars). The paradigm of reusing existing CLI auth works.
2. **Skills = portable agent knowledge.** 75 SKILL.md templates that any MCP-compatible agent can consume. Fork them into your own projects.
3. **Ship-ready bar.** The artifact IS the deliverable — no "I'll touch it up later" pass. This forces quality into the generation loop.
4. **Sister to Open Design.** html-anything for one-shot HTML publishing; Open Design for persistent design systems. Same team, same protocol, different scope.
5. **Hermes-compatible.** The dappweb community fork of Open Design already supports Hermes ACP — html-anything likely follows the same adapter pattern.

## Relevant for Hermes users

Html-anything detects agent CLIs on PATH. Hermes could be added as an adapter by following the pattern in `src/lib/agents/argv.ts`. The SKILL.md protocol html-anything uses is the same format Hermes skills use — templates are portable.

## Relationship to Open Design

| | html-anything | Open Design |
|---|---|---|
| Scope | One-shot HTML artifacts | Persistent design systems |
| Surfaces | 9 publishable surfaces | Web/mobile/desktop prototypes |
| Skills | 75 templates | 31 templates |
| Design systems | Skill-embedded | 129 DESIGN.md files |
| Daemon | No daemon | Local daemon + SQLite |
| Same team? | Yes (nexu-io) | Yes (nexu-io) |
| License | Apache-2.0 | Apache-2.0 |
