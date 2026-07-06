---
name: kanban
description: Hermes Kanban multi-agent workflow — orchestrator decomposition playbook and worker pitfalls/examples for routing work across profiles through the durable SQLite board.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, multi-agent, orchestration, routing, collaboration, workflow]
    related_skills: [coding-agents, hermes-agent, plan]
---

# Kanban Multi-Agent Workflow

## Overview

Hermes Kanban is a durable SQLite board for multi-profile / multi-worker collaboration. Two roles:

- **Orchestrator** — decomposes goals into tasks, assigns to specialist profiles, routes and tracks
- **Worker** — picks up assigned tasks, does the work, completes or blocks with handoff context

The core worker lifecycle (including the `kanban_create` fan-out pattern and "decompose, don't execute" rule) is auto-injected into every kanban process via the `KANBAN_GUIDANCE` system-prompt block. This skill provides the deeper playbook for both roles.

---

## Part A: Orchestrator Playbook

### Profiles are user-configured — not a fixed roster

There is **no default specialist roster**. The orchestrator skill does not know what profiles exist on this machine. The dispatcher silently fails to spawn unknown assignee names.

**Step 0: discover available profiles before planning.**

```bash
hermes profile list   # prints available profiles
kanban_list(assignee="<some-name>")  # sanity-check a single name
# Or just ask the user
```

### When to use the board

Create Kanban tasks when:
1. **Multiple specialists are needed**
2. **The work should survive a crash or restart**
3. **The user might want to interject**
4. **Multiple subtasks can run in parallel**
5. **Review / iteration is expected**
6. **The audit trail matters**

If none apply — use `delegate_task` instead or answer directly.

### Anti-Temptation Rules

- **Do not execute the work yourself** — create a task for the right specialist
- **Split multi-lane requests before creating cards**
- **Run independent lanes in parallel**
- **Never create dependent work as independent ready cards** — use `parents=[...]`
- **If no specialist fits, ask the user** — don't invent profile names

### Decomposition Playbook

**Step 1 — Understand the goal.** Ask clarifying questions if ambiguous.

**Step 2 — Sketch the task graph.** Extract lanes, map to profiles, decide dependencies. Show the graph to the user before creating cards.

**Step 3 — Create tasks and link.** Use `kanban_create` with `parents=[...]`:

```python
t1 = kanban_create(title="research: Postgres cost vs current", assignee="<profile-A>",
    body="Compare costs over 3-year window.")["task_id"]

t2 = kanban_create(title="research: Postgres performance vs current", assignee="<profile-A>",
    body="Compare latency, throughput at 500GB/10k QPS.")["task_id"]

t3 = kanban_create(title="synthesize migration recommendation", assignee="<profile-B>",
    body="Read T1 and T2, produce recommendation.", parents=[t1, t2])["task_id"]

t4 = kanban_create(title="draft decision memo", assignee="<profile-C>",
    body="Turn recommendation into CTO memo.", parents=[t3])["task_id"]
```

Create parent cards first, capture IDs, pass to child cards. Avoid creating all cards and linking afterward.

**Step 4 — Complete your own task.** Pass `created_cards` with IDs from `kanban_create` return values (never hallucinated IDs).

**Step 5 — Report back** in plain prose naming actual profiles used.

### Common Patterns

- **Fan-out + fan-in**: N research cards → one synthesis card with all as parents
- **Pipeline**: planner → implementer → reviewer, each gated on previous
- **Same-profile queue**: N tasks to same profile, no deps, dispatched serially
- **Human-in-the-loop**: `kanban_block()` with clear reason; operator unblocks with answer in comment

### Goal-Mode Cards (Persistent Workers)

For open-ended work requiring multiple turns:

```python
kanban_create(title="Translate full docs site to French", body="Every page translated.",
    assignee="<profile>", goal_mode=True, goal_max_turns=15)
```

Worker keeps going until it calls `kanban_complete`/`kanban_block` or budget exhausts. Write body as explicit acceptance criteria.

### Recovering Stuck Workers

Three actions from the kanban dashboard:
1. **Reclaim** — abort running worker, reset task to `ready`
2. **Reassign** — switch to different profile
3. **Change profile model** — edit profile config, then retry

---

## Part B: Worker Pitfalls and Examples

### Workspace Handling

| Kind | What it is | How to work |
|------|------------|-------------|
| `scratch` | Fresh tmp dir, yours alone | Read/write freely |
| `dir:<path>` | Shared persistent directory | Treat like long-lived state |
| `worktree` | Git worktree at resolved path | Add worktree if `.git` missing, commit work |

### Tenant Isolation

If `$HERMES_TENANT` is set, prefix memory entries with the tenant.

### Good Summary + Metadata Shapes

**Coding task:**
```python
kanban_complete(summary="shipped rate limiter — token bucket, 14 tests",
    metadata={"changed_files": ["rate_limiter.py"], "tests_run": 14, "tests_passed": 14})
```

**Coding task needing human review:** Block with `review-required:` prefix, leave structured metadata in a comment first:
```python
kanban_comment(body="review-required handoff:\nchanged_files: [...], tests_passed: 14")
kanban_block(reason="review-required: needs eyes on key choice before merging")
```

**Research task:**
```python
kanban_complete(summary="3 libraries reviewed; vLLM wins on throughput",
    metadata={"recommendation": "vLLM", "benchmarks": {"vllm": 1.0, "sglang": 0.87}})
```

### Claiming Cards

Pass `created_cards` on `kanban_complete` with IDs captured from `kanban_create` return values. Never invent IDs from prose or paste from earlier runs.

### Block Reasons

Bad: `"stuck"` — no context. Good: one sentence naming the specific decision needed.

```python
kanban_comment(body="Full context: ...")
kanban_block(reason="Rate limit key choice: IP or user_id?")
```

### Heartbeats

Name progress: `"epoch 12/50, loss 0.31"`. Skip for tasks under ~2 minutes.

### Retry Diagnostics

Check prior run outcomes:
- `timed_out` — chunk or shorten work
- `crashed` — OOM/segfault, reduce memory
- `spawn_failed` — config issue, ask human via `kanban_block`
- `reclaimed` — previous run was archived; check status carefully

### Notification Routing

In `~/.hermes/config.yaml`:
- `notification_sources: ['*']` — all profiles
- `notification_sources: ['default', 'zilor-ppt']` — specific profiles

### Do NOT

- Call `delegate_task` as substitute for `kanban_create`
- Call `clarify` in worker — use `kanban_comment` + `kanban_block` instead
- Modify files outside `$HERMES_KANBAN_WORKSPACE` unless task says to
- Complete a task you didn't finish — block it instead

### Pitfalls

1. **Task state can change between dispatch and startup** — always `kanban_show` first
2. **Workspace may have stale artifacts** from previous runs
3. **Don't rely on CLI in containerized backends** — use tools, not `hermes kanban <verb>`
4. **Reassignment vs new task** — if reviewer blocks with "needs changes", create a NEW task
5. **Argument order for links** — `kanban_link(parent_id=..., child_id=...)`. Parent first
6. **Don't pre-create whole graph if shape depends on intermediate findings**

### CLI Fallback

Every tool has a CLI equivalent for human operators:
- `kanban_show` ↔ `hermes kanban show <id> --json`
- `kanban_complete` ↔ `hermes kanban complete <id> --summary "..." --metadata '{...}'`
- `kanban_block` ↔ `hermes kanban block <id> "reason"`
- `kanban_create` ↔ `hermes kanban create "title" --assignee <profile>`