# Mirroring session context into Mission Control Kanban

Use this when Seyed asks to "put tasks/context into Mission Control" or similar.

## Command pattern

Run from the Hermes Agent repo when `./hermes` exists:

```bash
./hermes kanban boards list

./hermes kanban create "<concise task title>" \
  --body "Context from active session:
- User request: <verbatim or short quote>
- Current repo/workdir: <absolute path>
- Active goal/session id: <id if available>
- Constraints: <do not revert unrelated edits, no secrets, etc.>

Tasks mirrored here:
1. <task>
2. <task>
3. Verify Mission Control exposes the entry." \
  --priority 80 \
  --workspace dir:<absolute-path>

./hermes kanban list
./hermes kanban show <task-id>
```

## Notes

- The Mission Control task UI is the Hermes Kanban dashboard plugin at `/kanban`.
- The backend is `hermes_cli/kanban_db.py`.
- Priority is an integer. Do not pass label strings like `high`.
- If `python -m hermes_cli.kanban ...` does nothing, use `./hermes kanban ...` or `hermes kanban ...` instead.
- If the Kanban DB is read-only from the current sandbox, request approval for writing the shared Hermes Kanban database. Do not claim Mission Control was updated until `kanban list/show` verifies the task.
