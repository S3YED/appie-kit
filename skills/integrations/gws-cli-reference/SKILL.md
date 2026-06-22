---
name: gws-cli-reference
description: Use when working with the Google Workspace `gws` CLI across Gmail, Calendar, Drive, Docs, Sheets, Chat, Tasks, Meet, Forms, Classroom, Events, Model Armor, People, and cross-service workflows. This is the class-level umbrella for command discovery, auth, helper-command selection, and safe execution patterns.
---

# GWS CLI Reference

Class-level reference for the generated Google Workspace CLI skill family. Prefer this umbrella instead of narrow per-service helpers.

## Core workflow
1. Authenticate once with `gws auth login` or service-account env vars.
2. Start from `gws <service> --help` to see resources.
3. Inspect a concrete method with `gws schema <service>.<resource>.<method>` before building flags.
4. Prefer `--dry-run` for writes and any bulk operation.
5. Use `--format table` for quick scans, `json` for piping, `csv` for exports.

## Shared command pattern
```bash
gws <service> <resource> [sub-resource] <method> [flags]
```

Common flags:
- `--params '{...}'` for query/path params
- `--json '{...}'` for request bodies
- `--upload <path>` for file content
- `--output <path>` for downloads/exports
- `--page-all` for paginated listings
- `--sanitize <template>` when Model Armor screening is relevant

## Service map
### Communication
- Gmail: message/thread/draft/label/history operations, triage, reply, forward, send, watch.
- Chat: spaces, messages, announcements.
- Meet: conference management.

### Scheduling
- Calendar: calendars, ACLs, freebusy, events, agenda views, quick event insertion.

### Files and docs
- Drive: files, permissions, comments, shared drives, uploads, change watches.
- Docs / Sheets / Slides / Forms: content read/write and file-specific operations.

### People and org data
- People, Classroom, Admin Reports, Tasks, Keep.

### Safety and eventing
- Events / events subscriptions / renewals.
- Model Armor template creation plus prompt/response sanitization.

### Workflow helpers
- Meeting prep, standup reports, weekly digests, email-to-task, file announcements.

## Helper-command selection
Use the short helper form when it clearly matches the job:
- Calendar helpers: `+agenda`, `+insert`
- If `gws` is unavailable but `gog` is available, use `references/gog-calendar-oauth-recovery.md` for Calendar OAuth recovery and agenda listing via `gog calendar events`.
- Gmail helpers: `+send`, `+triage`, `+reply`, `+reply-all`, `+forward`, `+watch`
- Gmail helpers: `+send`, `+triage`, `+reply`, `+reply-all`, `+forward`, `+watch`
- Drive helper: `+upload`
- Workflow helpers: `+meeting-prep`, `+standup-report`, `+weekly-digest`, `+email-to-task`, `+file-announce`
- Events helpers: renew or subscribe when maintaining watches
- Model Armor helpers: create-template, sanitize-prompt, sanitize-response

## When to branch into references
Read `references/services-index.md` when choosing a service or helper. Read `references/absorbed-skills.md` when you need the exact old micro-skill names that were absorbed here.

## Safety rules
- Confirm scope before destructive writes/deletes/shares.
- Use `--dry-run` before multi-item changes.
- For permissions/sharing, verify target IDs and recipient emails first.
- For watches/subscriptions, record renewal requirements.

## Verification checklist
- [ ] Chosen the right service for the user task
- [ ] Inspected schema before constructing the call
- [ ] Used dry-run or read-before-write when possible
- [ ] Captured resulting IDs/URLs/status from the command output
