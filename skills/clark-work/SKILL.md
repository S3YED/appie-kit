---
name: clark-work
description: Use when you (a Clark agent) must read or update the customer's work in Clark Work, or create projects/tasks. Covers picking up tasks the customer put on the To Do board and creating your own projects and tasks.
---

# Clark Work (agent lane)

The customer's tasks live in **Clark Work** on the dashboard (dash.getclark.app). As
the customer's own agent you can read your customer's work, move tasks through
their statuses, comment on them, and create your own projects and tasks there.

## Identity and endpoint (never hardcode)

Your box already carries its own credentials. Source them instead of copying secrets:

```bash
CLARK="${CLARK:-$HOME/.clark}"
. "$CLARK/heartbeat.env"            # provides APPIE_ID, APPIE_SECRET, APPIE_HEARTBEAT_URL
DASH="${APPIE_HEARTBEAT_URL%/api/appie/heartbeat}"   # the dashboard origin
```

Call every action as `POST $DASH/api/agent/work` with two headers:

```bash
-H "X-Appie-Id: $APPIE_ID" -H "X-Appie-Secret: $APPIE_SECRET"
```

and a JSON body that describes the action. **Never send a `userId` or
`agentReference` in the body. The dashboard derives your customer from your box
identity.** A box can only ever touch its own customer's workspace, so these
calls are safe by construction.

## Actions

### list_work — read all projects + tasks
```bash
curl -s -X POST "$DASH/api/agent/work" \
  -H "X-Appie-Id: $APPIE_ID" -H "X-Appie-Secret: $APPIE_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"action":"list_work"}'
```
Returns `{ workspace, projects, items }`. Each item has `id`, `projectId`,
`title`, `description`, `status`, `priority`, `dueAt`, `createdAt`, `updatedAt`.

### create_project — start a new project
```bash
curl -s -X POST "$DASH/api/agent/work" \
  -H "X-Appie-Id: $APPIE_ID" -H "X-Appie-Secret: $APPIE_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"action":"create_project","name":"Q3 campaign","description":"optional"}'
```
Returns `{ project }` with its `id`.

### create_item — add a task to an existing project
```bash
curl -s -X POST "$DASH/api/agent/work" \
  -H "X-Appie-Id: $APPIE_ID" -H "X-Appie-Secret: $APPIE_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"action":"create_item","projectId":"<project-id>","title":"Draft newsletter","description":"optional","priority":"medium","status":"todo"}'
```
Statuses: `backlog`, `todo`, `in_progress`, `in_review`, `done`, `cancelled`.
Priorities: `none`, `low`, `medium`, `high`, `urgent`.

### update_item_status — move a task forward
```bash
curl -s -X POST "$DASH/api/agent/work" \
  -H "X-Appie-Id: $APPIE_ID" -H "X-Appie-Secret: $APPIE_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"action":"update_item_status","itemId":"<item-id>","status":"done"}'
```

### add_comment — leave a note on a task
```bash
curl -s -X POST "$DASH/api/agent/work" \
  -H "X-Appie-Id: $APPIE_ID" -H "X-Appie-Secret: $APPIE_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"action":"add_comment","itemId":"<item-id>","body":"Handled. Closing."}'
```

## Routine management (optional)

`POST $DASH/api/agent/routines` with the same headers and body
`{"action":"list_routines"}` (or `create_routine` with `title`/`instructions`/
`cronExpr`/`timezone`, or `toggle_routine` with `routineId`/`isActive`).

## The two workflows

**A. Customer put a task on the board, you execute it.**
1. `list_work` and look for items with `status: "todo"` (or `backlog`) in your
   customer's workspace.
2. Claim it: `update_item_status` to `in_progress`.
3. Read `title` and `description`, do the work.
4. Finish: `update_item_status` to `done` (or `in_review` if it needs review),
   and `add_comment` summarising what you did.

**B. You create your own work.**
1. `create_project` (or reuse an existing project from `list_work`).
2. `create_item` inside that project as you break the work down.
3. Progress each item through `update_item_status` as you go.

## Pitfalls

- Always derive `DASH` from `APPIE_HEARTBEAT_URL` at runtime; never hardcode the
  domain or any secret in the skill.
- If `list_work` returns 404 `workspace-not-found`, the customer has no Work
  workspace yet. Create one by `create_project`.
- Never log request bodies from these calls; they are tenant data.
- A 401 means the box credential is wrong or stale; re-run the heartbeat setup,
  do not bypass auth.
