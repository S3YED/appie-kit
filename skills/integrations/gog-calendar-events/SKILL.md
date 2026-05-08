---
name: gog-calendar-events
version: 1.0.0
description: "Lists Google Calendar events using the gog CLI tool."
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gog"]
---

# `gog` Calendar Events

This skill outlines how to retrieve Google Calendar events using the `gog` command-line tool, which is confirmed to be available in this environment.

## Usage

To list events for a specific day (e.g., today), using a plain text output:

```bash
gog calendar events --today --plain --account <your-email-address>
```

Replace `<your-email-address>` with the email associated with the Google Calendar you wish to query.

### Common Flags

*   `--today`: Shows events for the current day.
*   `--tomorrow`: Shows events for the next day.
*   `--week`: Shows events for the current week.
*   `--days N`: Shows events for the next `N` days.
*   `--plain`: Outputs stable, parseable text (TSV; no colors), good for scripting.
*   `--json`: Outputs JSON to stdout, best for scripting.
*   `--account <email>`: Specifies the Google account email to use. This is often required if a default is not configured.
*   `<calendarId>`: Optionally specify a particular calendar ID (defaults to primary).

## Pitfalls

*   **Missing `--account`**: `gog` commands often require the `--account` flag (e.g., `--account you@yourdomain.com`) if a default account hasn't been set via `gog auth manage`.
*   **Incorrect Help Syntax**: To get help for a `gog` subcommand, use `gog <command> --help` (e.g., `gog calendar --help`), not `gog help <command>`.

## See Also

*   `gog calendar --help`: For a full list of `gog calendar` subcommands and flags.
*   `gog calendar events --help`: For specific flags related to listing events.
