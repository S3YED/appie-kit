---
name: nextjs-agent-first
description: "Next.js 16.3+ agent-first features: AGENTS.md, first-party Skills, agent-browser React introspection, actionable errors. Use when building Next.js apps with AI coding agents."
author: Appie-1
tags: [nextjs, agent-first, ai, development, vercel]
related_skills: [nextjs-expert, agent-browser, nextjs-turbopack]
---

# Next.js Agent-First Features

Next.js 16.3+ is the first framework designed explicitly for AI-agent-driven development.

## Key Features

### AGENTS.md (auto-generated docs)
- `next dev` auto-writes version-matched docs pointers into `AGENTS.md`
- Agents read actual docs instead of guessing from training data
- Opt-out via `agentRules: false` in `next.config.ts`

### First-Party Skills (npx-installable)
Install via `npx skills add vercel/next.js`:

| Skill | Purpose |
|-------|---------|
| `next-dev-loop` | Full dev feedback loop: drive browser, read console, inspect React tree, follow network requests |
| `next-cache-components-adoption` | Incremental or direct adoption of Cache Components (`"use cache"`) |
| `next-cache-components-optimizer` | Optimize routes for instant navigation by growing the static shell |

### Agent Browser React Introspection
`agent-browser` v0.27+ can run React DevTools commands from CLI:

```bash
# Launch with React DevTools
agent-browser --enable react-devtools

# Inspect component tree
agent-browser react tree
agent-browser react inspect <fiber-id>
agent-browser react renders start
agent-browser react suspense --only-dynamic --json
```

### Actionable Errors (Instant Insights)
Error overlay shows labeled fixes (Stream / Cache / Block) with a "Copy prompt" button that copies a paste-ready agent prompt.

### Streamlined MCP Server
Two new tools: `get_compilation_issues` and `compile_route` — check compilation without full `next build`.

### Turbopack Improvements (16.3)
- ~90% less memory (21.5GB → 2GB for vercel.com)
- ~2.3x faster cached builds
- Experimental Rust React Compiler (20-50% faster)
- `import.meta.glob` API support
- ~15% faster dev cold start

## Usage

When building or debugging Next.js projects with an AI agent:

1. **Enable AGENTS.md**: Ensure `next dev` runs in the project so docs are auto-generated
2. **Use next-dev-loop skill**: Load it when you need browser-based verification
3. **Run agent-browser with React**: `agent-browser --enable react-devtools` for component inspection
4. **Copy actionable error prompts**: Use the error overlay's "Copy prompt" button for instant fixes
5. **Cache Components optimizer**: Run after building to optimize routes for instant nav

## Pitfalls
- 16.3 is on `@preview` npm tag — stable expected in weeks
- AGENTS.md is auto-overwritten each `next dev` run — don't manually edit it
- agent-browser React DevTools requires `--enable react-devtools` flag
