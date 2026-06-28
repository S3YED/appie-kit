---
name: agent-cli-delegation
description: "Umbrella workflow for delegating coding work to local agent CLIs such as Claude Code, Codex, and OpenCode."
origin: user
---

# Agent CLI Delegation

Use this umbrella when the user wants coding work delegated to a local autonomous coding CLI rather than completed entirely in the current Hermes turn.

## Choose the agent CLI

| CLI | Best fit | Notes |
|---|---|---|
| Claude Code | Larger refactors, repo-aware implementation, PR-ready changes | Keep prompts scoped and include verification commands. |
| Codex | OpenAI Codex CLI feature/fix work and iterative patching | Provide exact paths, constraints, and tests to run. |
| OpenCode | Alternative coding agent and PR-review workflows | Useful when the user prefers OpenCode or when comparing agents. |

## Delegation prompt shape

Include:

1. Goal and non-goals.
2. Repository path and relevant files.
3. Constraints: style, dependencies, APIs, security, backwards compatibility.
4. Required verification commands.
5. Expected deliverables: patch, tests, summary, risks.

## Execution rules

- Run agent CLIs in a tracked terminal/background process, not an untracked shell background.
- Require the child agent to report changed files and verification output.
- Independently verify critical claims: inspect diffs and run tests/checks yourself.
- Never ask a child agent to use credentials, deploy, merge, or delete without explicit user authorization.

## Review after delegation

1. `git status --short` and `git diff`.
2. Check for unrelated changes, secrets, generated junk, or destructive edits.
3. Run the test/lint/typecheck commands that matter.
4. Summarize what was done and what remains.
