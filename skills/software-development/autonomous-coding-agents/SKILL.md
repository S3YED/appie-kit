---
name: autonomous-coding-agents
description: Delegate coding, refactoring, PR review, and long-running implementation work to autonomous coding CLIs such as Claude Code, Codex, and OpenCode. Use when deciding which coding agent CLI to run, orchestrating one-shot or interactive sessions, handling PTYs/tmux/background processes, or parallelizing issue/PR work.
---

# Autonomous Coding Agents

Use this umbrella when Hermes should hand work to a separate coding agent process rather than performing every edit itself. Pick the backend based on availability, task shape, and required interaction.

## Selection guide

| Agent | Best for | Default mode | Notes |
|---|---|---|---|
| Claude Code | Large feature work, refactors, codebase navigation, structured review | `claude -p` print mode | Strong non-interactive JSON/streaming modes; interactive mode needs PTY dialog handling. |
| Codex CLI | OpenAI-backed coding, PR reviews, parallel issue fixes | one-shot or background PTY | Useful with OpenAI-Codex OAuth and git worktrees. |
| OpenCode | Feature work, refactoring, PR review with open tooling | one-shot or background PTY | Resolve the binary path first; supports interactive sessions and resuming. |

Prefer `delegate_task` for bounded subtasks inside the current Hermes turn. Use external CLIs for longer work, richer codebase autonomy, or tools/models not exposed through `delegate_task`.

## Universal orchestration pattern

1. Inspect repo state and define the task with exact files, acceptance criteria, and constraints.
2. Choose one-shot mode for bounded work; choose tmux/PTY for multi-turn or interactive tools.
3. Run the agent from the correct workdir. Use git worktrees for parallel tasks that will edit files.
4. Monitor output; answer prompts explicitly; kill stuck sessions cleanly.
5. Verify the result yourself with tests, diffs, and file reads before reporting success.

## Claude Code

Preferred for most non-interactive work:

```bash
claude -p "Implement X. Run tests. Summarize files changed."
```

Interactive mode requires a real PTY, usually tmux. First-run dialogs may require accepting workspace trust and the permissions warning. Do not run blind; capture the pane and verify that Claude is at the prompt or actively working.

## Codex CLI

Use for OpenAI Codex-backed changes and PR reviews. Patterns:

```bash
codex "Review this PR for correctness and security"
# or background/PTY when it may ask questions
```

For parallel issue fixing, create separate git worktrees, launch one Codex process per worktree, then review/merge results centrally.

## OpenCode

Resolve the binary first (`opencode`, `opencode-ai`, local install path, etc.). Use one-shot mode for simple tasks and a PTY for multi-turn sessions. Watch cost/session state and resume existing sessions when continuing prior work.

## PR review workflow

- Fetch/check out the PR locally when possible.
- Ask the coding agent for findings, but verify every claimed bug against the diff and tests.
- Post only actionable comments; distinguish blockers from suggestions.

## Pitfalls

- Never assume an external agent completed work because it said so; inspect the filesystem and test output.
- Do not launch multiple editors in the same worktree.
- PTY tools may hang on trust/permission prompts; handle dialogs before waiting for final output.
- Background processes should use Hermes `background=true` plus `notify_on_complete=true` for bounded runs, or tmux for interactive sessions.
