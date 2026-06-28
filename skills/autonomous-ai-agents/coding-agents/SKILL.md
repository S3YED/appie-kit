---
name: coding-agents
description: "Delegate coding tasks to external autonomous AI coding CLI agents — Claude Code, Codex, OpenCode, and Kanban+Codex lane patterns. Covers install, auth, one-shot tasks, interactive sessions, PR reviews, parallel worktrees, and reconciliation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-agents, claude-code, codex, opencode, autonomous-coding, code-generation]
    related_skills: [kanban-worker, github-pr-workflow]
---

# Coding Agents — Delegate to AI Coding CLIs

Delegate coding to external autonomous AI coding agent CLIs via Hermes terminal/process tools. This umbrella covers **Claude Code** (Anthropic), **Codex** (OpenAI), and **OpenCode** (provider-agnostic, open-source), plus the **Kanban Codex Lane** pattern for Hermes Kanban workers.

## When to Use Coding Agents

Use any coding agent CLI when:
- Building features, refactoring, or batch fixing issues
- The task requires autonomous file exploration and multi-step reasoning
- You want to run parallel implementation lanes

Do NOT use a coding agent when:
- A small direct edit is faster and safer
- The change touches secrets, credentials, or production order-entry systems
- You need human judgment that can't be captured in a prompt

## Shared Prerequisites

All coding agents need:
- A **git repository** — most refuse to run outside one
- **Auth credentials** (agent-specific, see sections below)
- **`pty=true`** for interactive TUI sessions; print/one-shot mode may not need it

## Section 1: Claude Code

Anthropic's autonomous coding agent CLI. v2.x can read files, write code, run shell commands, spawn subagents, and manage git workflows.

### Install & Auth

```bash
npm install -g @anthropic-ai/claude-code
claude auth login                   # Browser OAuth
claude auth login --console         # API key billing
claude auth login --sso             # Enterprise SSO
claude auth status                  # Verify
```

### Print Mode (PREFERRED for one-shot tasks)

```bash
# Non-interactive, exits when done. No PTY needed.
terminal(command="claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10", workdir="/path/to/project", timeout=120)
```

Key flags: `--allowedTools 'Read,Edit'`, `--max-turns N`, `--max-budget-usd N`, `--output-format json`, `--json-schema '{...}'`, `--continue` (resume last session), `--resume <id>` (specific session), `--bare` (fastest startup, needs ANTHROPIC_API_KEY).

### Interactive Mode (via tmux)

```bash
terminal(command="tmux new-session -d -s claude-work -x 140 -y 40")
terminal(command="tmux send-keys -t claude-work 'cd /path/to/project && claude' Enter")
# Handle trust dialog
terminal(command="sleep 4 && tmux send-keys -t claude-work Enter")
# Send task
terminal(command="tmux send-keys -t claude-work 'Refactor the auth module' Enter")
# Monitor
terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -50")
```

### PR Review

```bash
# Quick via print mode
terminal(command="git diff main...feature-branch | claude -p 'Review this diff for bugs, security issues, and style problems.' --max-turns 1", timeout=60)

# Deep via worktree
terminal(command="claude -p 'Review this PR thoroughly' --from-pr 42 --max-turns 10", workdir="/path/to/repo", timeout=120)
```

### Key Pitfalls
- Interactive mode **REQUIRES tmux** — print mode (`-p`) skips dialog handling
- `--dangerously-skip-permissions` defaults to "No, exit" — send Down then Enter to accept
- Session resumption requires same directory
- `/compact` prevents context degradation above 70% usage

---

## Section 2: Codex (OpenAI)

OpenAI's autonomous coding agent CLI. Good for features, refactoring, and batch issue fixing.

### Install & Auth

```bash
npm install -g @openai/codex
```
Auth via `OPENAI_API_KEY` or Codex CLI OAuth (`~/.codex/auth.json`). For Hermes-managed OAuth: `hermes auth add openai-codex`.

#### Headless Server Auth (OAuth Device Flow)

On headless servers (Hetzner, EC2, DO droplet), `hermes auth add openai-codex` runs an interactive OAuth device code flow. It does NOT fail; it waits for you:

1. Run the command in a foreground terminal — it prints:
   - URL: `https://auth.openai.com/codex/device`
   - Code: `W04N-ADDSI` (6-char alphanumeric, hyphenated)
2. Open that URL in a browser **on your local machine** and enter the code.
3. The CLI polls for up to 15 minutes. No additional flags needed; `--no-browser` only suppresses the local-browser-open attempt, it does not change the device flow (and is implicit on headless boxes).

Do NOT run this in `background=true` — you will never see the URL+code. Use foreground or PTY mode. If you accidentally background it, kill it (`process(action='kill', ...)`) and retry in foreground. After the credential is stored, verify with `hermes auth list`.

See `references/codex-auth-headless.md` for the exact API endpoints and step-by-step flow.

### One-Shot Tasks

```bash
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

### Background Mode (Long Tasks)

```bash
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
process(action="poll", session_id="<id>")
```

### Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Auto-approves file changes in sandbox |
| `--yolo` | No sandbox, no approvals (dangerous, fastest) |
| `--sandbox danger-full-access` | Bypass sandbox when bubblewrap fails |

### Parallel Issue Fixing with Worktrees

```bash
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="codex --yolo exec 'Fix issue #78'", workdir="/tmp/issue-78", background=true, pty=true)
```

### Pitfalls
- **Always use `pty=true`** — Codex hangs without a PTY
- **Git repo required** — use `mktemp -d && git init` for scratch
- Hermes gateway contexts may need `--sandbox danger-full-access` due to bubblewrap errors
- **Headless Codex auth is a device flow** — `hermes auth add openai-codex` prints a URL+code and polls for 15min. Run it foreground, not background. Share the URL+code with the user to complete in their browser. See `references/codex-auth-headless.md`.

---

## Section 3: OpenCode

Provider-agnostic, open-source AI coding agent. Supports multiple providers (OpenRouter, Anthropic, OpenAI).

### Install & Auth

```bash
npm i -g opencode-ai@latest
opencode auth login                   # Interactive auth
opencode auth list                    # Verify providers
```

### One-Shot Tasks

```bash
terminal(command="opencode run 'Add retry logic to API calls and update tests'", workdir="~/project")
```

Attach context: `-f config.yaml -f .env.example`
Show thinking: `--thinking`
Force model: `--model openrouter/anthropic/claude-sonnet-4`

### Interactive Sessions (Background)

```bash
terminal(command="opencode", workdir="~/project", background=true, pty=true)
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow")
process(action="log", session_id="<id>")
process(action="write", data="\x03")  # Ctrl+C to exit (NOT /exit)
```

### PR Review

```bash
terminal(command="opencode pr 42", workdir="~/project", pty=true)
```

### Pitfalls
- `/exit` is NOT a valid command — it opens an agent selector. Use Ctrl+C (`\x03`)
- Enter may need to be pressed twice to submit in TUI
- PATH mismatch can select wrong binary — check with `which -a opencode`

---

## Section 4: Kanban Codex Lane

Use when a Hermes Kanban worker wants to run Codex as an isolated implementation lane while Hermes keeps ownership of task lifecycle, reconciliation, testing, and handoff.

### When to Use the Codex Lane

Use when ALL are true:
- Task has clear acceptance criteria and bounded diff
- Repo can be isolated in a git worktree/branch
- Hermes can run canonical tests independently
- Prompt can state all safety constraints

Do NOT use when:
- Task requires human judgment not in the Kanban body
- Change touches secrets, credentials, or production order-entry
- A small direct edit is safer

### Ownership Rules

1. **Hermes owns the Kanban lifecycle** — Codex never calls `kanban_complete`, `kanban_block`, or `kanban_create`
2. **Hermes owns final acceptance** — treat Codex commits/diffs as untrusted patches
3. **Hermes owns test execution** — repeat tests from Hermes after Codex exits
4. **Hermes owns safety** — reject the lane if boundaries are violated

### Required Worktree Pattern

```bash
TASK_ID="${HERMES_KANBAN_TASK:-t_manual}"
REPO="/path/to/repo"
BASE="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
SAFE_TASK="$(printf '%s' "$TASK_ID" | tr -cd '[:alnum:]_-')"
BRANCH="codex/${SAFE_TASK}/$(date -u +%Y%m%d%H%M%S)"
WORKTREE="/tmp/${SAFE_TASK}-codex-lane"

git -C "$REPO" fetch --all --prune
git -C "$REPO" worktree add -b "$BRANCH" "$WORKTREE" "$BASE"
```

### Prompt Construction

Every Codex lane prompt must include:
- `task_id`, title, and full Kanban acceptance criteria
- Repo path, worktree path, branch name, allowed file scope
- Explicit statement: "Hermes owns Kanban lifecycle; Codex is an input lane only"
- Prohibited actions list
- Verification commands

### Reconciliation Checklist

- [ ] `git status --short --branch` shows only expected files
- [ ] `git diff --stat` reviewed by Hermes
- [ ] No secrets, credentials, or unrelated artifacts
- [ ] Hermes ran canonical tests independently
- [ ] Accepted commits applied to Hermes-owned workspace
- [ ] Stuck/killed Codex processes cleaned up

### Codex Lane Metadata Schema

```json
{
  "codex_lane": {
    "used": true,
    "mode": "exec | goal | skipped",
    "worktree": "/absolute/path",
    "branch": "codex/t_caa69668/20260508100000",
    "result": "accepted | rejected | partial | timed_out",
    "tests_run": [
      {"command": "pytest tests/", "exit_code": 0, "owner": "hermes"}
    ]
  }
}
```

---

## Section 5: Shared Patterns

### Parallel Task Execution

All three agents support parallel worktree-based execution:

```bash
# Create worktrees
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# Launch agents in each (use whichever CLI is available)
terminal(command="codex --yolo exec 'Fix issue #78'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="opencode run 'Fix issue #99'", workdir="/tmp/issue-99", background=true, pty=true)
```

### PR Review Patterns

| Agent | Quick Review | Deep Review |
|-------|-------------|-------------|
| Claude Code | `claude -p 'Review this diff' --max-turns 1` | `claude --from-pr 42` or interactive worktree |
| Codex | `codex review --base origin/main` | Clone to temp dir + `codex exec` |
| OpenCode | `opencode run 'Review this PR'` | `opencode pr 42` |

### Choice Guide

| Situation | Recommended Agent |
|-----------|------------------|
| Need structured JSON output | Claude Code (`--output-format json --json-schema`) |
| Provider-agnostic / open-source | OpenCode (works with OpenRouter, multiple providers) |
| Fast parallel batch fixes | Codex (lightweight `--yolo` mode) |
| Kanban worker needs an implementation lane | Codex via Kanban Codex Lane pattern |
| Multi-turn interactive session | Claude Code with tmux or OpenCode TUI |
| CI/automation with strict tool permissions | Claude Code (`--allowedTools`, `--bare`) |

---

## Pitfalls (All Agents)

1. **Git repo required** — most agents refuse to run outside a git directory
2. **Do NOT trust self-report** — always inspect the diff, re-run tests independently
3. **Isolate untrusted work** — use worktrees/branches, never run in shared dirty checkout
4. **PTY for TUI** — interactive sessions hang without a pseudo-terminal
5. **Clean up background processes** — kill tmux sessions and remove worktrees when done
6. **Scoped prompts prevent accidents** — use `--allowedTools` and explicit file scopes
7. **Large diffs are expensive** — scope down to specific files/directories when reasonable
8. **Check binary resolution** — `which -a codex` / `which -a opencode` to verify which binary runs
