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

## React DevTools introspection (v0.27+)

Launch a browser with React DevTools pre-loaded:
```bash
agent-browser open --enable react-devtools http://localhost:3000
```

## React DevTools CLI (v0.27+)
Launch with `--enable react-devtools` for React component introspection:

| Command | Description |
|---------|-------------|
| `react tree` | Print React component tree with fiber IDs |
| `react inspect <id>` | Inspect props, hooks, state, source for one component |
| `react renders start/stop` | Profile re-renders |
| `react suspense --only-dynamic --json` | Walk Suspense boundaries, classify static vs dynamic |

## Core Commands

| Command | Description |
|---------|-------------|
| `react tree` | Print the React component tree with fiber IDs |
| `react inspect <id>` | Inspect props, hooks, state, and source for one component |
| `react renders start` | Begin recording component render commits |
| `react renders stop [--json]` | Stop recording and print a render profile |
| `react suspense [--only-dynamic] [--json]` | Walk Suspense boundaries, classify static vs dynamic |

Typical workflow:
```bash
# Open with React DevTools
agent-browser open --enable react-devtools http://localhost:3000
# Inspect component tree
agent-browser react tree
# Inspect a specific component
agent-browser react inspect 42
# Profile re-renders after an interaction
agent-browser click @e3
agent-browser react renders stop
# Check Suspense boundaries
agent-browser react suspense --only-dynamic
```

If the session already has a browser without the hook, pass `--enable react-devtools` to relaunch with it installed.

## Web Vitals

Measure Core Web Vitals on any site:
```bash
agent-browser vitals
agent-browser vitals https://example.com --json
```

Reports LCP, CLS, TTFB, FCP, INP, and hydration timing when available (React profiling build).

## SPA navigation

Client-side navigation without full reload:
```bash
agent-browser pushstate /dashboard
agent-browser wait --load networkidle
agent-browser snapshot -i
```

On Next.js apps, uses `window.next.router.push` so RSC fetches still run. Other frameworks fall back to `history.pushState`.

## Integration with Next.js 16.3

Combined with the `next-dev-loop` skill (Next.js 16.3+), agent-browser gives agents the full dev feedback loop:
```bash
# Install the skill
npx skills add vercel/next.js --skill next-dev-loop
# In your agent prompt: "After every edit, verify the page still works at runtime using the next-dev-loop skill."
```

## Architecture
Client-daemon: a Rust CLI talks to a native Rust daemon that drives Chrome over CDP. The daemon starts automatically and persists between commands.

## When to use vs other tools
- **Default** for shell-driven browser work (cheapest context, deterministic).
- Use Playwright/Stagehand only when you need their specific ecosystem features.
- Cross-platform: macOS (arm64/x64), Linux (arm64/x64), Windows (x64).

Works with: Claude Code, Cursor, Copilot, Codex, Gemini, opencode, and any agent that runs shell commands.
