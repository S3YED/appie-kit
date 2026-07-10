---
name: kanban-agent-workflows
description: "Operate Hermes Kanban multi-agent boards as an orchestrator or worker: decompose work, route tasks, follow worker lifecycle, manage dependencies, heartbeat, block/unblock, recover stuck workers, and summarize results. Use for any Hermes Kanban collaboration workflow."
---

# Kanban Agent Workflows

Use this umbrella for Hermes Kanban work. The board is the durable boundary between orchestrators and workers; do not bypass it for multi-agent work that should survive a single session.

## Orchestrator role

Use the board when work benefits from parallelism, specialist profiles, durable handoff, or isolation. Do not use it for a tiny single-turn task.

Orchestrator flow:

1. Understand the user's goal and acceptance criteria.
2. Sketch a dependency graph before creating cards.
3. Create focused tasks with clear inputs, outputs, and verification requirements.
4. Link dependencies so workers can start only when prerequisites are complete.
5. Assign tasks to the right specialist profile.
6. Complete the orchestrator task after the board is set up, then report routing decisions.

Anti-temptation rule: if you are acting as orchestrator, do not secretly implement worker tasks yourself just because you can.

## Worker role

Worker flow:

1. Read the assigned card and linked context.
2. Work only inside the assigned workspace/tenant boundary.
3. Send useful heartbeats for long tasks.
4. Complete with a summary that includes files changed, verification run, and follow-up needs.
5. Block instead of guessing when credentials, access, or upstream artifacts are missing.

Good block reasons are specific and answerable: missing env var, unavailable repo path, failing upstream task, ambiguous acceptance criterion.

## Task design patterns

- **Fan-out/fan-in:** split independent implementation/research tasks, then create a synthesis/review task depending on all outputs.
- **Reviewer lane:** create a second task for review/verification before merge or delivery.
- **Recovery lane:** when a worker blocks, create a small unblocker task instead of rewriting the original task.

## Pitfalls

- Do not claim cards by guessed IDs; capture returned IDs from create/list calls.
- Do not mix tenants/workspaces; isolation matters more than convenience.
- Do not leave long-running tasks silent; heartbeat with meaningful progress.
- Do not mark complete without verification evidence or an explicit blocker.

## CLI fallback

When the dedicated Kanban tools are unavailable, use the `hermes kanban` CLI with the board path from environment/config and mirror the same lifecycle manually.
