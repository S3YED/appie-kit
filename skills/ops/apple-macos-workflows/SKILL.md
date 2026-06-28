---
name: apple-macos-workflows
description: "Umbrella workflow for Apple/macOS personal automation: Notes, Reminders, Messages, Find My, and background GUI control."
origin: user
---

# Apple/macOS Workflows

Use this umbrella when a task involves native Apple apps, macOS-only CLIs, cross-device Apple data, or GUI automation on the user's Mac.

## Choose the surface first

| User intent | Tooling pattern |
|---|---|
| Create/search/edit Apple Notes | Use `memo` against Notes.app; prefer memory only for agent-internal facts. |
| Add/list/complete reminders | Use `remindctl`; prefer Reminders for user-visible tasks and due dates. |
| Send/read iMessage or SMS | Use `imsg`; verify recipient/chat before sending. |
| Locate Apple devices/AirTags | Use the FindMy app/CLI pattern; treat locations as sensitive. |
| Drive arbitrary native apps | Use background `computer_use` capture/click/type workflow; verify after state changes. |

## Apple Notes via `memo`

Prereqs: macOS Notes.app, `brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`, Automation permission to Notes.

Common commands:

```bash
memo notes
memo notes -s "query"
memo notes -a "Title"
memo notes -e
memo notes -ex
```

Rules: use Notes for cross-device synced user notes; use Obsidian for Markdown-native vault work; do not use Notes for agent memory.

## Apple Reminders via `remindctl`

Prereqs: macOS Reminders.app and `remindctl` installed/configured. Use for visible to-dos, due dates, and task lists. Confirm destructive completion/deletion when ambiguous.

## iMessage/SMS via `imsg`

Use when the user asks to message a person through Apple Messages. Search or list chats first when the target is ambiguous. Never send secrets, 2FA codes, payment details, or sensitive content without explicit user text and target verification.

## Find My

Use only for user-requested device/person/item location checks. Treat location output as private. Return concise status and timestamp; do not background-track unless explicitly requested.

## Background macOS computer use

Canonical loop:

1. Capture the target app with numbered elements.
2. Click/type by element index, not coordinates, when possible.
3. Re-capture after every state-changing action.

Rules: do not raise windows unless asked; scope captures to the relevant app; never interact with permission dialogs, passwords, payment UI, or 2FA prompts without explicit approval.

## Safety checklist

- Verify the app/account/context before modifying user-visible data.
- Prefer CLI/API tools over GUI driving when available.
- Ask before destructive changes or messages to external people.
- Keep screenshots and locations out of summaries unless needed.
