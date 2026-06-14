---
name: agent-browser
description: Browser automation CLI built for AI agents — compact ref-based text output (200-400 tokens vs 3000-5000 for full DOM), native Rust, 50+ commands. Default browser-automation tool for the fleet. Use for any web navigation, scraping, form-filling, screenshots, or testing from the shell.
---

# agent-browser — fleet default for browser automation

A native-Rust browser-automation CLI designed for AI agents. Compact text output minimises context usage. Use it instead of heavier browser stacks for shell-driven web tasks.

## Install
```bash
npm install -g agent-browser      # all platforms
# or: brew install agent-browser  # macOS
agent-browser install             # download Chrome (first run only)
# try without installing:
npx agent-browser open example.com
```

## Core loop (ref-based)
```bash
agent-browser open example.com
agent-browser snapshot -i          # accessibility tree with refs: heading "..." [ref=e1], link "..." [ref=e2]
agent-browser click @e2            # act on a ref from the snapshot
agent-browser screenshot page.png
agent-browser close
```

## Why refs (the context win)
`snapshot` returns a compact accessibility tree where each element has a ref (`@e1`, `@e2`):
- Context-efficient: ~200-400 tokens vs ~3000-5000 for full DOM.
- Deterministic: a ref points to the exact element from the snapshot (no fragile selectors).
- Fast: no DOM re-query. AI-friendly: text output parses naturally.

## What it covers (50+ commands)
Navigation, forms, screenshots, network control, storage/cookies/auth-state, file upload/download, tabs, frames, debugging. Built-in: video recording, streaming, profiler, diffing. First-class docs for React/Web Vitals, init scripts, and Next.js + Vercel. Stateful: sessions, profiles, proxy, security controls — good for long-running agents.

## Architecture
Client-daemon: a Rust CLI talks to a native Rust daemon that drives Chrome over CDP. The daemon starts automatically and persists between commands.

## When to use vs other tools
- **Default** for shell-driven browser work (cheapest context, deterministic).
- Use Playwright/Stagehand only when you need their specific ecosystem features.
- Cross-platform: macOS (arm64/x64), Linux (arm64/x64), Windows (x64).

Works with: Claude Code, Cursor, Copilot, Codex, Gemini, opencode, and any agent that runs shell commands.
