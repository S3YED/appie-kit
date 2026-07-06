---
name: kanban-workflows
description: "Umbrella playbook for Hermes Kanban orchestration and worker execution patterns."
origin: user
---

# Kanban Workflows

Use this umbrella for Hermes Kanban tasks, whether acting as the orchestrator decomposing work or as a worker executing one assigned lane.

## Role split

### Orchestrator

- Decompose work into independently verifiable cards.
- Route cards to specialists instead of doing implementation work directly.
- Keep dependencies explicit and avoid overloading one worker with unrelated goals.
- Define acceptance checks before dispatch.

### Worker

- Load task context and relevant skills.
- Work only the assigned card unless scope must be clarified.
- Report concrete artifacts: files changed, commands run, tests, blockers.
- Do not silently skip verification; state what could not be verified.

## Lifecycle

1. Intake: restate goal, constraints, and done criteria.
2. Plan cards: make tasks independently executable where possible.
3. Dispatch: assign with exact repo/path/context and verification command.
4. Monitor: collect outputs, resolve blockers, prevent duplicated work.
5. Integrate: verify combined result and summarize residual risk.

## Pitfalls

- Orchestrator temptation: doing the work instead of routing it.
- Worker drift: expanding scope beyond assigned card.
- Hidden dependency: two cards editing the same file without coordination.
- False completion: summary without test/log evidence.
