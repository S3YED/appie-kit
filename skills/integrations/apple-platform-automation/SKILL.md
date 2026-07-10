---
name: apple-platform-automation
description: Manage Apple/macOS personal apps and device workflows from Hermes, including Apple Notes, Reminders, Find My, iMessage/SMS, and UI automation. Use when a task involves Apple ecosystem data or macOS-only CLIs such as memo, remindctl, imsg, FindMy.app, AppleScript, or Peekaboo.
---

# Apple Platform Automation

Use this umbrella for Apple/macOS personal-productivity and device tasks. Prefer native or purpose-built CLIs first; fall back to AppleScript/GUI automation only when no CLI exists.

## Prerequisite checks

1. Confirm the task is running on macOS before promising Apple app access.
2. Check the specific CLI exists (`memo`, `remindctl`, `imsg`) before using it.
3. For GUI workflows, prefer Peekaboo or screenshot-assisted automation and verify the visible state before acting.
4. For outbound messages or destructive edits, confirm the recipient/item and exact action with the user.

## Apple Notes (`memo`)

Use for creating, searching, viewing, moving, exporting, editing, or deleting Apple Notes. Typical flow:

```bash
memo list
memo search "query"
memo create --title "Title" --body "Body"
memo edit <note-id>
```

Rules: do not use Apple Notes as the default knowledge base if the user asked for Obsidian/Notion/Google Docs; verify note IDs before edits or deletes.

## Apple Reminders (`remindctl`)

Use for listing reminder lists, adding dated reminders, completing items, or deleting stale tasks.

```bash
remindctl lists
remindctl list --list "Inbox"
remindctl add "Task text" --due "tomorrow 9am" --list "Inbox"
remindctl complete <reminder-id>
```

Natural due dates are usually accepted, but verify parsed dates when timing matters.

## Find My / AirTags / Apple devices

Use FindMy.app when the user asks for Apple device or AirTag locations. There is no reliable universal CLI; use one of:

- AppleScript to open Find My and switch tabs.
- Peekaboo/screenshot capture to inspect device or item location.
- Repeated captures for tracking over time while the item detail remains open.

Limitations: location may be stale, approximate, hidden behind privacy prompts, or unavailable until the app has focus. Report uncertainty explicitly.

## iMessage / SMS (`imsg`)

Use for listing chats, reading history, sending text or attachments, and watching for new messages.

```bash
imsg chats
imsg history <chat-id> --limit 20
imsg send <chat-id> "message text"
imsg send <chat-id> --attachment /path/to/file "caption"
```

Safety: before sending, confirm the resolved chat/contact and message body unless the user has already specified an unambiguous target and content in the same request.

## Common pitfalls

- Apple automation is macOS-only; fail fast on Linux/remote containers.
- GUI state is not proof of completion; capture or query after acting.
- Contact names can match multiple chats; disambiguate before sending.
- Do not claim precise Find My coordinates unless the app or tool actually exposes them.
