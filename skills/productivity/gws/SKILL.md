---
name: gws
description: Google Workspace via the gws CLI across Gmail, Calendar, Drive, Docs, Sheets, Chat, Tasks, Meet, Forms, Classroom, People, Events, Model Armor, and cross-service workflows. Use when a task spans multiple gws services, when you need to choose the right Workspace service, or when an older service-specific recipe would have applied.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [google-workspace, gws, productivity, email, calendar, drive, docs, sheets]
    related_skills: [gws-shared]
---

# GWS Workspace Suite

## Overview
Use `gws` when the task lives anywhere in Google Workspace and may cross service boundaries. Keep the shared auth, safety, and formatting rules from `gws-shared` in mind.

## Workflow
1. Read `gws-shared` for auth, global flags, and safety rules.
2. Identify the target service (`gmail`, `calendar`, `drive`, `docs`, `sheets`, `chat`, `tasks`, `meet`, `forms`, `classroom`, `people`, `events`, `modelarmor`).
3. Inspect the exact method with `gws <service> --help` and `gws schema ...` before writes.
4. Prefer the smallest service-specific command that solves the task.
5. For write/delete/share actions, confirm scope before acting.

## References
- `references/common-workflows.md` for cross-service recipe families and service combinations.
- `references/mac-mini-oauth-creds.md` for Google OAuth credential locations on this machine (n8n client, gog built-in, credential file paths).

## Service Map
- **Email:** triage, send, reply, forward, watch.
- **Calendar:** list, create, reschedule, free/busy, recurring events.
- **Drive:** search, upload, download, share, permissions, shared drives.
- **Docs:** read documents, create documents, batch update content.
- **Sheets:** read/update cells, append rows, create reports.
- **Chat / Tasks / Meet / Forms / People / Classroom / Events / Model Armor:** use the service that matches the object you are manipulating; inspect schemas first.

## Common Cross-Service Workflows
- Convert email into tasks or calendar events.
- Announce Drive files in Chat.
- Prepare meeting briefs from calendar + docs + drive links.
- Generate weekly digests from inbox, meetings, and tasks.
- Apply content safety with Model Armor before sending or posting.

## Pitfalls
- Don’t guess field names or payload shapes; inspect the schema.
- Don’t use the wrong service just because it is nearby.
- Don’t skip confirmation for mail, calendar creation, sharing, or deletions.
- Don’t duplicate the shared auth rules; defer to `gws-shared`.
