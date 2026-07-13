---
name: wacli
description: Send WhatsApp messages, search/sync history, and analyze/triage open chats with draft responses via the wacli CLI.
homepage: https://wacli.sh
metadata:
  {
    "openclaw":
      {
        "emoji": "📱",
        "requires": { "bins": ["wacli"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "steipete/tap/wacli",
              "bins": ["wacli"],
              "label": "Install wacli (brew)",
            },
            {
              "id": "go",
              "kind": "go",
              "module": "github.com/steipete/wacli/cmd/wacli@latest",
              "bins": ["wacli"],
              "label": "Install wacli (go)",
            },
          ],
      },
  }
---

# wacli

Use `wacli` when the user asks you to message someone on WhatsApp, search/sync history, **or** analyze/open their chats and draft responses.
Do NOT use `wacli` for routine user chats without explicit instruction; the user (Seyed) chats with you directly on a different platform.

## Safety

- Require explicit recipient + message text when sending.
- Confirm recipient + message before sending.
- If anything is ambiguous, ask a clarifying question.

## Stale lock handling

Before any command, check if a `wacli sync --follow` process is running stale:

```
ps aux | grep wacli | grep -v grep
```

If a sync process is days old and blocking, kill it:
```
kill <pid>
```
Then run `wacli doctor` again. The lock clears in ~1 second.

## Auth + sync

- First check version, auth state, and lock status: `wacli version && wacli doctor && wacli auth status --json`.
- `wacli sync --follow` (continuous sync)
- `wacli doctor`

Find chats + messages

- `wacli chats list --limit 20 --query "name or number"`
- `wacli messages list --chat <jid> --limit 10` — get recent messages from a chat (no search term needed)
  - Add `--json` for machine-readable output with full message metadata
- `wacli messages search "query" --limit 20 --chat <jid>`
- `wacli messages search "invoice" --after 2025-01-01 --before 2025-12-31`

History backfill

- `wacli history backfill --chat <jid> --requests 2 --count 50`

Send

- Text: `wacli send text --to "+14155551212" --message "Hello! Are you free at 3pm?"`
- Group: `wacli send text --to "1234567890-123456789@g.us" --message "Running 5 min late."`
- File: `wacli send file --to "+14155551212" --file /path/agenda.pdf --caption "Agenda"`

## Outbound replies

When a lead replies to an outbound WhatsApp message, especially with objections or skepticism, handle the emotion before the sale. See `references/outbound-reply-patterns.md` for reply templates and trust-rebuilding patterns.

Notes

## Chat triage & draft workflow

When the user asks you to analyze their open WhatsApp chats and prepare responses:

1. Check for stale sync processes first: `ps aux | grep "wacli sync" | grep -v grep`
2. Run `wacli doctor` to verify auth
3. `wacli chats list --limit 30` to see unread counts
4. `wacli messages list --chat <jid> --limit 10` to read recent context
5. Prioritize by: recency (today > yesterday) > unread count > DM > business context
6. Present a structured overview with priority tiers and draft responses

### Pitfalls

- **Stale sync process blocks commands.** A `wacli sync --follow` left running for days holds the lock. Kill it with `kill <pid>` before reading.
- **`wacli doctor` shows LOCKED=true, CONNECTED=false** — normal for local DB reads. FTS5 is readable even disconnected.
- **`wacli messages search` requires a query.** Use `wacli messages list` to browse recent messages regardless of content.
- **`wacli chats list` has no `--unread-only` flag.** Filter manually from unread_count column.
- **LLM context budget.** Batch chat reads via delegate_task (max 3 at a time) when analyzing 10+ chats.

## Pitfalls

### LaunchAgent store lock
macOS has a LaunchAgent `com.wacli.sync` that auto-starts `wacli sync --follow` on login and keeps it alive (`KeepAlive=true`). This holds an exclusive lock on `~/.wacli/store/` and blocks all other wacli operations (backfill, search, send) with `store is locked (another wacli is running?)`.

**To temporarily stop it** for a single operation:
```bash
launchctl bootout gui/$(id -u)/com.wacli.sync
pkill -f "wacli sync"
rm -f ~/.wacli/store/LOCK
```

**To permanently disable:**
```bash
launchctl bootout gui/$(id -u)/com.wacli.sync
rm ~/Library/LaunchAgents/com.wacli.sync.plist
```

The LaunchAgent is at `~/Library/LaunchAgents/com.wacli.sync.plist`.

### Search by name
`wacli messages search "Name"` is accent-sensitive. Use lowercase for broader matching. For JIDs, always use `--json` output and parse with Python.

### Store unlock race
After killing the sync process, another instance may immediately respawn (KeepAlive). Wait 2 seconds between kill and operation. Use `pkill -f "wacli sync"` not just `kill <PID>`.
- Use `--json` for machine-readable output when parsing.
- Backfill requires your phone online; results are best-effort.
- WhatsApp CLI is not needed for routine user chats; it's for messaging other people.
- JIDs: direct chats look like `<number>@s.whatsapp.net`; groups look like `<id>@g.us` (use `wacli chats list` to find).
