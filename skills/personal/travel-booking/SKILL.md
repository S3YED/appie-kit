---
name: travel-booking
description: Research and book multi-leg travel (flights, ferries, trains, buses) via online aggregators using browser tools. Covers itinerary construction, transfer timing, and presenting realistic connection options.
category: knowledge
triggers:
  - book flight
  - book ferry
  - travel from X to Y
  - how to get from X to Y
  - multi-modal travel
  - transport connection
---

# Travel Booking Skill

Research and present multi-leg travel itineraries with realistic connection times. Primarily SE Asia booking sites (12Go.asia, Google Flights, Bangkok Airways).

## Workflow

### Step 1: Gather Requirements
- Origin to destination(s)
- Date(s) — exact or flexible
- Preferred time windows
- One way / return
- Number of passengers
- Any constraints (weight limits, class preference, direct-only)

### Step 2: Flight Research

**Start with 12Go.asia** (covers flights, ferries, buses, trains, taxis, combined tickets):
1. Navigate to `https://12go.asia/en/travel/<origin>/<destination>?date=YYYY-MM-DD`
2. Handle cookie consent popup — click Allow all
3. Use `document.body.innerText.substring(0, X)` via browser_console to extract results
4. For transport-type filtering, click filter buttons then Update
5. Extract schedule tables — they contain per-airline pricing (often cheaper than listing prices)

**Fallback: Google Flights** (most reliable with headless browser):
- Use this URL pattern: `https://www.google.com/travel/flights?q=flights+from+<ORIGIN>+to+<DEST>+on+YYYY-MM-DD+one+way&curr=THB`
- The `one+way` parameter is critical — without it Google shows round-trip pricing
- Use Escape key to dismiss popup dialogs
- Switch to the Cheapest tab

### Step 3: Ferry / Ground Transport Research

Use 12Go.asia for connecting routes:
- Filter by Ferries and relevant time window
- Note departure piers — some are far from airports
- Combined tickets often available (airport shuttle + ferry as single ticket)

### Step 4: Build the Itinerary

CRITICAL: Account for realistic transfer time between modes:
- Airport to Pier transfer: varies (10min to 45min)
- Baggage collection: +10-15min after landing
- Check-in cutoff: Ferries typically need 15-30min check-in before departure

### Step 5: Present Options

Present 2-3 scenarios with estimated arrival times:

```
**SCENARIO X: [Flight time] to [Ferry time]**
- Landing [time], baggage ~[time]
- [Transport] from [place], +[transfer time] transfer
- [Ferry/bus] departure ~[time], arrive [dest] ~[time]
- **Arrive [dest] ~[time]**
- Cost: [flight] + [ferry] = [total]
```

Include transfer time between modes in every scenario.

### Step 6: Offer to Book

Ask if they want you to proceed with booking. Do not auto-book.

### Step 7: Extract Booking Confirmations from Email

After the user books, check inbox for confirmations:
1. Scan recent emails for booking keywords (airline name, ferry, booking ref)
2. Read messages to find attached e-tickets/PDFs
3. Download attachments via email CLI
4. Extract PDF contents using pdftotext / PyPDF2 / pdfplumber fallback chain

## Pitfalls

- Bangkok Airways and Skyscanner block headless browsers — use Google Flights as fallback.
- 12Go pricing discrepancy: listing card prices differ from schedule table prices.
- 12Go dynamic loading: results don't always appear in accessibility tree — use browser_console.
- Google Flights shows round-trip prices by default.
- Ferry schedules after 17:00 become limited.
- Self-connect flights: 12Go sometimes groups flights with long layovers — flag these.
- Always note which airport (BKK vs DMK in Bangkok).
- Transfer time is non-negotiable: always account for baggage collection, transfer, and check-in.