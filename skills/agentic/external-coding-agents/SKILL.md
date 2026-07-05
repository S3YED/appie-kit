---
name: external-coding-agents
description: "Delegate coding tasks to external AI coding agent CLIs: Claude Code, Codex, OpenCode."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-agent, delegation, claude-code, codex, opencode, orchestration, pty]
    related_skills: [hermes-agent, plan, github-code-review]
---

# External AI Coding Agents

Delegate coding work to third-party AI coding agents from within Hermes. These tools (Claude Code, Codex, OpenCode) are autonomous CLI agents that can read files, write code, run shell commands, and manage git workflows — each with its own strengths.

## When to Delegate vs Do It Yourself

| Situation | Approach |
|-----------|----------|
| Bug fix in a known file | Do it yourself with `patch`/`write_file` — faster, no overhead |
| Complex multi-file refactor | Delegate — the external agent has persistent context across files |
| Task needs a fresh perspective | Delegate — the external agent will spot things you might miss |
| CI/CD automation | Delegate — use print mode for clean automation |
| PR review of someone else's code | Delegate — the external agent can see the full diff in context |
| Research/reconnaissance | Delegate — agent can browse and explore independently |
| Simple one-line change | Do it yourself |

## Common Orchestration Patterns

All three coding agents use the same core patterns:

### Print Mode (Non-Interactive — Preferred)
Cleanest integration. No PTY, no dialog handling, structured output:

```
terminal(command="<agent> -p 'Add error handling to all API calls in src/'", workdir="/path/to/project", timeout=120)
```

### PTY Background Mode (Interactive)
For iterative work needing multi-turn conversation. Use `background=true, pty=true` and `process` tool to monitor:

```
terminal(command="<agent>", workdir="~/project", background=true, pty=true)
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow")
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")
process(action="kill", session_id="<id>")
```

### Get the Diff Back
After delegation completes, always inspect what changed:

```
git diff
git diff --stat
```

## Agent Decision Guide

| Need | Best Agent | Why |
|------|-----------|-----|
| Best overall coding ability | Claude Code | Anthropic's most capable model, v2.2+, rich feature set |
| Cheapest / open-source preference | OpenCode | Provider-agnostic (OpenRouter, Anthropic, OpenAI, local models) |
| OpenAI ecosystem | Codex | OpenAI's autonomous agent, OAuth integration |
| PR review with inline comments | Claude Code | Built-in `--from-pr` flag, formal review workflow |
| Batch multi-issue fixing | Codex or OpenCode | Lightweight, parallel worktree pattern |
| Long-running autonomous session | Any | Use background=true + process tool for monitoring |

## Common Pitfalls

1. **PTY is required for interactive sessions** — all three agents are TUI apps; skip `pty=true` and they hang
2. **Git repo required** — Codex and OpenCode refuse to run outside a git directory. Use `mktemp -d && git init` for scratch work
3. **Always inspect the diff after delegation** — external agents can make surprising decisions. Use `git diff --stat` to verify scope
4. **Keep tasks focused** — narrow prompts produce better results than vague requests
5. **Set timeouts** — external agents can loop indefinitely. Use `--max-turns` (Claude Code) or `timeout` in terminal calls
6. **Cleanup background sessions** — kill tmux sessions and worktree directories when done
7. **Parallel worktrees need isolation** — don't share a single working directory across parallel agents

## Agent-Specific References

Detailed reference docs for each agent:

- **references/claude-code.md** — Full Claude Code orchestration guide (flags, auth, hooks, MCP, slash commands, 745 lines)
- **references/codex.md** — Codex CLI usage (flags, background mode, worktrees)
- **references/opencode.md** — OpenCode CLI usage (binary resolution, parallel patterns, TUI keybindings)

## Getting Started

### Which Agent is Installed?

```
which claude codex opencode 2>/dev/null || echo "check npm list -g"
```

### Quick One-Shot (any agent)

```
# Claude Code
terminal(command="claude -p 'Add input validation to all endpoint handlers' --max-turns 10", workdir="~/project", timeout=120)

# Codex
terminal(command="codex exec 'Add input validation to all endpoint handlers'", workdir="~/project", pty=true)

# OpenCode
terminal(command="opencode run 'Add input validation to all endpoint handlers'", workdir="~/project")
```