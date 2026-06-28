---
name: travel-booking
description: Research and book multi-leg travel (flights, ferries, trains, buses) via online aggregators using browser tools. Covers itinerary construction, transfer timing, and presenting realistic connection options.
category: productivity
triggers:
  - book flight
  - book ferry
  - travel from X to Y
  - how to get from X to Y
  - multi-modal travel
  - transport connection
  - reis boeken
  - vlucht + boot
---

# Travel Booking Skill

Research and present multi-leg travel itineraries with realistic connection times. Primarily SE Asia booking sites (12Go.asia, Google Flights, Bangkok Airways).

## Workflow

### Step 1: Gather Requirements
- Origin → destination(s)
- Date(s) — exact or flexible
- Preferred time windows
- Enkele reis / retour
- Number of passengers
- Any constraints (weight limits, class preference, direct-only)

### Step 2: Flight Research

**Start with 12Go.asia** (covers flights, ferries, buses, trains, taxis, combined tickets):
1. Navigate to `https://12go.asia/en/travel/<origin>/<destination>?date=YYYY-MM-DD`
   - Use lowercase, hyphenated names: `bangkok/koh-samui`, `koh-samui/koh-phangan`
2. Handle cookie consent popup — click `Allow all`
3. The page loads dynamically. Use `document.body.innerText.substring(0, X)` via browser_console to extract results
4. For transport-type filtering, click on transport filter buttons (e.g. `Flights 23 From THB5,911`) then click `Update`
5. Extract schedule tables from the page body — they contain per-airline pricing (often cheaper than 12Go listing prices)

**Fallback: Google Flights** (preferred — most reliable with headless browser)
- **USE THIS URL PATTERN** — proven working for one-way pricing:
  `https://www.google.com/travel/flights?q=flights+from+<ORIGIN>+to+<DEST>+on+YYYY-MM-DD+one+way&curr=THB`
  - The `one+way` parameter is **critical** — without it Google shows round-trip pricing with a ~5-day return baked in
  - `&curr=THB` shows Thai baht
  - Example: `https://www.google.com/travel/flights?q=flights+from+BKK+to+USM+on+2026-06-01+one+way&curr=THB`
- Use Escape key to dismiss popup dialogs (time filters, etc.) that cover results
- Switch to the **Cheapest** tab — often reveals better prices than the default Best tab
- **Dialog handling**: Time filters dialog may persist after Escape — press Escape again or click outside
- When Bangkok Airways / travel sites block the browser (Access Denied / captcha), Google Flights generally works

### Step 3: Ferry / Ground Transport Research

For the same route or connecting routes, use 12Go.asia:
- Filter by `Ferries` and relevant time window
- Note departure piers — some are far from airports (see Pitfalls)
- Lomprayah is the most reliable operator for Samui→Phangan (frequent, on-time)
- **Lomprayah Airport Shuttle** (USM → Thong Sala): combined ticket — shuttle bus from airport to pier + ferry. 1h total, ~THB 400. Most convenient option for flight+ferry combos. URL: `https://12go.asia/en/travel/samui-airport/thong-sala?date=YYYY-MM-DD&adults=1`
- Songserm Express offers speedboats (faster, smaller)
- Lomlahkkhirin offers catamarans from Bangrak Pier (~THB 351, 30min)

### Step 4: Build the Itinerary

CRITICAL: Account for realistic transfer time between modes:
- **Airport → Pier transfer time**: USM → Bangrak Pier: ~10min taxi, USM → Nathon Pier: ~25min
- **Baggage collection**: +10-15min after landing
- **Check-in cutoff**: Ferries typically need 15-30min check-in before departure
- **Combined tickets**: Some operators (Lomprayah) offer airport shuttle + ferry as a single ticket (e.g. USM Airport → Thong Sala Pier in 1h total for THB 400)

### Step 5: Present Options

Present 2-3 scenarios with estimated arrival times at final destination. Format:

```
**SCENARIO X: [Flight time] → [Ferry time]**
- Landing [time], baggage ~[time]
- [Transport type] from [airport/pier], +[transfer time] transfer
- [Ferry/bus] departure ~[time], arrive [destination] ~[time]
- **Arrive [destination] ~[time]**
- Kosten: [flight cost] + [ferry cost] = [total]
```

CRITICAL: Include transfer time between modes in every scenario. Do not skip this — the user expects a realistic total journey time, not a disconnected list of departure times.

### Step 6: Offer to Book

Ask if they want you to proceed with booking on 12Go.asia. Do not auto-book.

### Step 7: Extract Booking Confirmations from Email

After the user books, check their inbox for confirmations:

1. Scan recent emails for booking keywords (airline name, 12Go, ferry, booking ref)
2. Read messages to find attached e-tickets/PDFs
3. Download attachments via `himalaya attachment download <ID>`
4. Extract PDF contents using `pdftotext` → `PyPDF2` → `pdfplumber` fallback chain

See `references/email-confirmation-extraction.md` for the full workflow, including the extraction table mapping PDF fields to user-facing info (booking ref, times, baggage allowance, fare breakdown).

Multiple email accounts (Gmail App Passwords) are common — check with `--account <name>`.

## Pitfalls

- **Bangkok Airways** and **Skyscanner** block headless browsers (Access Denied / captcha). Use Google Flights as fallback for schedule data, and 12Go for booking.
- **12Go pricing discrepancy**: The listing card prices (e.g. THB 5,911) differ from the schedule table prices (e.g. THB 2,430 direct on Bangkok Airways). The schedule table shows the airline's own pricing — mention this to the user.
- **12Go dynamic loading**: Results don't always appear in the accessibility tree. Use `browser_console` with `document.body.innerText.substring()` to extract the full content.
- **12Go "Show more" pitfall**: Clicking "Show more" on the listings often scrolls to the footer instead of expanding results. To see all options: scroll past reviews to the **schedule table** at the bottom, or use filters + "Update" button to reduce result set.
- **Cookie popup reappears** after navigating to a new 12Go page — always click Allow all first.
- **Google Flights shows round-trip prices** by default — the "From X THB" price includes the return leg. For one-way, the actual fare is roughly half.
- **Ferry schedules after 17:00** become limited. Last ferries Samui→Phangan typically around 17:30-18:00.
- **Self-connect flights**: 12Go sometimes groups flights with long layovers (5h+) as "self-connect" — flag these to the user rather than presenting them as direct.
- **BKK vs DMK**: Bangkok has two airports. Most BKK→USM flights are from Suvarnabhumi (BKK), but some use Don Mueang (DMK). Always note which airport.
- **Transfer time is non-negotiable**: Always account for baggage collection (10-15 min), pier/station transfer (varies wildly — 10 min to 45 min), and check-in cutoff. Presenting departure times without these makes the itinerary misleading. If uncertain, ask the user or pad conservatively.
