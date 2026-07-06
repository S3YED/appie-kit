# Lead CRM Tracking (Manual Call Funnel)

When no CRM API is available (GHL V1 deprecated, V2 auth issues), track leads manually through the call funnel using a local JSON database. The agent maintains this on the server and provides daily status updates.

## Database Structure

A single JSON file (`/root/creed-crm.json`) stores all leads with their current status through the funnel.

### Status Flow

```
entered → welcomed → replied → triage_booked → triage_done → sales_booked → converted
                                                                              → lost (ghosted)
                                                                              → winner
```

### Lead Entry Format

```json
{
  "name": "Ahmed Khan",
  "email": "ahmed@example.com",
  "phone": "+97150...",
  "commitment": 10,
  "situation": "I know I need to do more",
  "vision": "Finally get abs and feel confident",
  "source": "giveaway",
  "status": "entered",
  "triage_call_notes": "",
  "sales_call_notes": "",
  "next_action": "Send welcome message",
  "last_updated": "2026-07-03T10:00:00Z",
  "entry_date": "2026-07-02T05:49:30Z"
}
```

## Workflow

1. **Agent imports** leads from the main lead database (`/root/leads-database.json`) into the CRM
2. **Agent sends** Ibrahim the morning summary + priority list (who needs calls today)
3. **Ibrahim reports back** after calls: who he spoke to, what happened, any notes
4. **Agent updates** the CRM with the new status and notes
5. **Agent sends** next-day summary with updated priorities

## Status Commands

```bash
# Import new leads from main database
python3 /root/creed-crm.py import

# View current status and next actions
python3 /root/creed-crm.py status

# Update a lead's status
python3 /root/creed-crm.py update "email@example.com" "triage_done" "Notes from call here"
```

## Daily Summary Format

Sent to Ibrahim via Telegram each morning:

```
**🏆 Giveaway Lead Status — [Date]**

**Total leads:** X
- Entered (no action): X
- Welcomed: X
- Triage booked: X
- Triage done: X
- Converted: X
- Lost: X

**Priority today:**
- Call these 3 who booked triage: [names]
- Send welcome to these 2 new entries: [names]
- Follow up with these 2 who ghosted: [names]
```