---
name: ibrahim-daily-briefing
description: Generate Ibrahim's daily briefing — new leads, upcoming calls, pending follow-ups, system health, and one strategic question. Delivered to Telegram.
version: 1.0.0
author: Ibrahim's Assistant
tags: [ibrahim, daily, briefing, business, ops]
---

# Ibrahim Daily Briefing

## When to Use

Run every morning before Ibrahim starts his day (07:00 Dubai time = 03:00 UTC). Also triggered when Ibrahim asks "what's on today?" or "give me the rundown."

## Briefing Structure

### 1. New Leads (Last 24h)
- How many new Typeform entries
- Their names, locations, key answers
- Priority leads (high commitment score)

### 2. Today's Calls
- Triage calls scheduled (time, lead name)
- Second calls scheduled
- Any no-shows from yesterday to follow up

### 3. Pending Follow-ups
- Leads who need a WhatsApp message today
- Which stage they're in (welcome, post-call, reactivation)
- Suggested message (draft, needs approval)

### 4. System Health
- Website up/down
- Typeform working
- WhatsApp connected
- Cognee status

### 5. Strategic Question
One thought-provoking question about the business, funnel, content, or goals. Example: "We had 3 no-shows this week. Is the call reminder sequence strong enough?"

## Data Sources

Check these for each briefing:
- Typeform API (new entries)
- Lead database (/root/leads-database.json)
- WhatsApp (recent chats)
- GHL pipeline (if available)
- System health checks

## Delivery

Send to Ibrahim on Telegram with a clean, scannable format. Use bullet points. Keep it under 800 words. End with the strategic question.===ME:client-acquisition/ibrahim-daily-briefing