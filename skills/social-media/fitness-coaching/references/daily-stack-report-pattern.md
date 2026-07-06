# Daily Stack Report Cron Pattern

A zero-token-cost cron that checks multiple business systems and delivers a formatted Telegram report. Designed for fitness coaches who want one daily snapshot of their entire operation.

## Architecture

```
cronjob (no_agent=True, script="daily-stack-report.py")
  ├── System health (CPU load, disk %, RAM %)
  ├── Website (HTTP status, page size, TTFB)
  ├── GoHighLevel (pipelines, contacts count, calendars)
  ├── Typeform (active form count)
  └── Slack (active channel count)
     → stdout → Telegram (formatted markdown)
```

## What It Checks

| System | Data Point | Source | Why It Matters |
|--------|-----------|--------|----------------|
| System | Load avg, disk %, RAM % | `os.getloadavg()`, `df`, `free` | Proactive alerting — disk fills up on small VPS |
| Website | HTTP 200/4xx/5xx, size, TTFB | Vercel landing page `urllib.request` | Instant outage detection |
| GHL | Pipeline names + stages | `GET /opportunities/pipelines` | See the funnel health at a glance |
| GHL | Total contacts | `GET /contacts/?limit=1` | Growth trend over time |
| GHL | Calendars configured | `GET /calendars/` | Verify booking system is intact |
| Typeform | Active form count | `GET /forms` | Confirm lead-capture forms are live |
| Slack | Active channel count | `GET /conversations.list` | Team activity pulse |

## Token Setup

All tokens go to `/tmp/` via `printf` (never `write_file` — token masking bug corrupts them):

```bash
printf 'pit-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' > /tmp/ghl_token.txt
printf 'tfp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' > /tmp/tf_token.txt
printf 'xoxb-xxxxxxxx-xxxxxxx-xxxxxxxxxxxx' > /tmp/slack_token.txt
```

The script reads them at runtime with `open(path).read().strip()`.

## The `no_agent=True` Rule

When `no_agent=True`:
- The script's `stdout` is delivered verbatim as the Telegram message
- No LLM is invoked — zero token cost
- Empty stdout = silent (no message sent)
- Non-zero exit = error alert sent

This means the script IS the message body. Design the output as formatted Telegram markdown with clear headings, emoji indicators, and sections.

## Colour Coding

Use emoji for health status:
- 🟢 All good (disk < 80%, RAM < 70%, site 200)
- 🟡 Warning (disk 80-90%, RAM 70-85%)
- 🔴 Critical (disk > 90%, RAM > 85%, site down)

## Cron Schedule

Set for the client's morning. For Dubai (UTC+4):
- Report: `0 3 * * *` (07:00 DUBAI)
- Delivery: `deliver="origin"` (sends to home Telegram channel)

## Pitfalls

- **Script path must be relative.** `daily-stack-report.py`, not `/root/.hermes/scripts/daily-stack-report.py`.
- **GHL calendar events endpoint is finicky.** The `GET /calendars/events?startDate=&endDate=` params may return 422. Safer to just list calendars via `GET /calendars/` as a pulse check.
- **GWS calendar auth is unreliable.** Google refresh tokens expire. Calendar data may not be available every day. Don't block the report on it.
- **No secret exposure.** Tokens are hardcoded in `/tmp/` on Hermes agent, not in the script itself. Safe to share.