# Fleet context ingestion into Mission Control

Use this when Seyed asks to put all tasks/context into Mission Control, especially across Appie profiles.

## Goal

Create a durable Mission Control/Kanban representation of current work without dumping raw private logs or transient session noise.

## Evidence sources to inspect

Prefer small authoritative state files over full transcripts:

- Primary profile memories: `~/.hermes/profiles/<profile>/memories/{USER.md,MEMORY.md}`
- Live profile homes: check actual `HERMES_HOME` pointers before editing or reading role identity. Example: Appie-3 live home may be `~/.hermes-appie3`, while `~/.hermes/appie-3-cto` can be a legacy pointer.
- Shared fleet queue: `~/.hermes/appies/_shared/memory/tasks.json`
- Shared learnings: `~/.hermes/appies/_shared/memory/learnings.json`
- Heartbeat/status: `~/.hermes/appies/_shared/heartbeat/status.json`
- Cron jobs per profile: `~/.hermes-*/cron/jobs.json`
- Role identity docs: `SOUL.md`, `IDENTITY.md`, `CLAUDE.md`, `AGENTS.md`
- Security/ops reports only as supporting evidence, not as task dumps.

Avoid copying secrets, complete chat transcripts, or large reports into card bodies.

## Mission Control card shape

For each task/context card, include:

- Source profile and role
- Evidence paths read
- Current status: active, queued, completed, blocked, or context-only
- Owner or assignee
- Mission Control destination board
- Short action checklist
- Verification command or UI path

Use a dedicated board when the request is fleet-wide, for example `appie-fleet-context`, instead of dumping into the default board.

## Idempotency

Prefer Kanban task creation with stable `idempotency_key` values when using `hermes_cli.kanban_db.create_task()` directly. Good keys:

- `mc-context:<profile>:<source-id>`
- `mc-fleet-task:<task-json-id>`
- `mc-session:<session-id>:<topic>`

If using CLI commands that do not expose idempotency, first list/search the board and reuse or update existing cards rather than creating duplicates.

## Verification

Before replying:

1. List the destination board.
2. Show at least one created/updated card body.
3. Confirm the Mission Control URL or route that should display it, usually `/kanban`.
4. Mention any evidence source that was empty or intentionally skipped.

## Pitfalls

- Do not assume `~/.hermes/appies/memories` is populated. It may exist but be empty.
- Do not treat legacy role folders as live identity without checking pointer files and active `HERMES_HOME`.
- Telegram cannot render markdown tables reliably. Report concise bullets instead.
- Avoid status claims like “completed” unless verified from current files or DB state.