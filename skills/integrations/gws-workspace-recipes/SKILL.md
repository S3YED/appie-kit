---
name: gws-workspace-recipes
description: "Use when the task is a reusable Google Workspace multi-step recipe rather than a single API call: scheduling from sheets, inbox-to-task flows, file sharing, doc generation, team announcements, event management, Drive organization, and cross-service automations built on the `gws` CLI."
---

# Google Workspace Recipes

Umbrella skill for reusable `gws` cross-service recipes. Prefer this over one-recipe-per-skill micro entries.

## Recipe pattern
1. Identify the source artifact: email, sheet, doc, folder, calendar event, task list, or form.
2. Identify the destination artifact or side effect.
3. Read/inspect first.
4. Dry-run the write if supported.
5. Execute the transformation.
6. Verify the resulting IDs, links, or attendee/share state.

## Recipe families
### Calendar and meeting operations
- Create, reschedule, and batch-create events
- Block focus time
- Find free time
- Invite attendees in bulk
- Share event materials
- Review participants

### Email and communications
- Draft email from doc
- Send announcements across Gmail + Chat
- Forward labeled messages
- Save attachments to Drive
- Save email contents to Docs
- Create Gmail filters / vacation responders

### Docs, Drive, and knowledge assets
- Copy templates into new docs
- Share docs/folders and notify recipients
- Organize Drive folders
- Bulk-download folder contents
- Email Drive links
- Watch Drive changes

### Sheets-driven workflows
- Append updates, back up to CSV, compare tabs, duplicate monthly templates
- Generate reports from sheets
- Create events from sheets
- Sync contacts to sheets
- Log deal updates

### Tasks, classroom, forms, and reporting
- Create task lists
- Review overdue tasks
- Collect form responses
- Create Classroom courses
- Create expense trackers / feedback forms / presentations

## Selection guidance
If the task sounds like “take data from X and create/update Y”, it belongs here. If it is just one service call, use `gws-cli-reference` instead.

## References
- `references/recipe-index.md` groups absorbed recipes by job type.
- `references/absorbed-skills.md` maps old recipe skill names to their umbrella slots.

## Verification checklist
- [ ] Read source state first
- [ ] Verified destination identifiers
- [ ] Confirmed every write side effect the user asked for
- [ ] Returned the resulting event IDs, file links, or updated record counts
