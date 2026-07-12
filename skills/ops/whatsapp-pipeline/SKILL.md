---
name: whatsapp-pipeline
description: Use when managing Ibrahim's WhatsApp lead pipeline — monitoring wacli, checking GHL leads, sending Typeform follow-ups, or generating daily pipeline overviews. Covers the full giveaway-to-client funnel oversight.
triggers:
  - "How's my pipeline looking?"
  - "Show me today's leads"
  - "Check WhatsApp"
  - "Draft DMs"
  - "Typeform entries"
  - "lead follow-up"
---

# WhatsApp Pipeline Operations

## Architecture

```
Typeform (N4LbJCHT) → GHL (CRM) → WhatsApp (wacli) → Client
                                ↕
                         Kratos (oversight)
```

- **wacli**: WhatsApp CLI linked to Ibrahim's number (+44 7822 014367)
- **GHL**: GoHighLevel CRM with pipeline stages (Survey Submitted, 24 Hours Before, No Answer/Unresponsive, etc.)
- **Typeform**: Giveaway form ID N4LbJCHT, account ramzy@cali-creed.com
- **Webhook**: creed-coaching-giveaway.vercel.app/api/lead

## Daily Operations

### 1. Pipeline Overview
Run the overview script:
```bash
python3 /root/pipeline_overview.py
```
This checks wacli status, Typeform captures, and GHL pipeline.

### 2. WhatsApp Sync
```bash
wacli sync
```
Check status: `wacli doctor`
If locked: kill the stale sync PID first, then re-sync.

### 3. Lead Triage (from wacli)
```bash
wacli chats list --limit 30
```
Filter to unread, recent chats. Read messages with:
```bash
wacli messages list --chat <jid> --limit 8 --json
```

### 4. GHL Pipeline Check
Leads are cached in `/root/full_data.json`. Filter by `pipelineStageId` and `createdAt` to find leads needing action.

## Follow-up Cadence

| Stage | Action | Timing |
|---|---|---|
| New Typeform entry | WhatsApp welcome message | Within 1 hour |
| No reply after 24h | Follow-up DM | 24h after welcome |
| Triage call booked | Call prep (transcript analysis) | 1h before call |
| Triage call done | Value follow-up + book sales call | Same day |
| Cold (>14d no reply) | Re-engagement sequence | 3-email + 1 DM |

## Auto-Refresh Systems

### Google Auth
Cron: `Google Token Auto-Refresh` (every 1h)
Script: `~/.hermes/scripts/refresh_google_token.py`

### WhatsApp Sync
Manual: `wacli sync` (run when needed, not continuous)

## Daily Cron Jobs

| Job | Schedule | Delivery |
|---|---|---|
| Creed Stack Report | 07:00 Dubai | Telegram |
| Lead Summary | 09:00 Dubai | Telegram |
| Pipeline Overview | 09:00 Dubai | Telegram |
| Brainstorm Check-in | 14:00 Dubai | Telegram |
| Typeform Poller | Hourly | Local |

## Pitfalls

- `wacli` locks during sync — always check `wacli doctor` before write operations
- GHL API uses header `Version: 2021-07-28`
- Typeform webhook may miss entries if form is embedded via iframe — verify with direct Typeform API
- Google auth tokens expire after 1h — the cron job handles this, but verify with `gws drive files list` if auth fails
- Ibrahim's country disqualification rule: Asia/Africa/South America entrants are disqualified from winning but still captured