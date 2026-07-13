---
name: travel-planning
description: Plan urgent or time-sensitive travel options across train, bus, flight, and driving, with live schedules/prices when possible.
version: 1.0.0
metadata:
  hermes:
    tags: [travel, itinerary, train, bus, flight, driving, fares, urgent-travel]
    category: productivity
    requires_toolsets: [browser, terminal]
---

# Travel Planning

Use this when the user asks for how to get somewhere, compare travel modes, estimate costs, or choose the best itinerary. Especially important for urgent, emotional, or time-sensitive trips where arrival windows matter more than generic route advice.

## Default output style

- Start with empathy only when appropriate; keep it short and real.
- Give a clear recommendation first, then alternatives.
- Use bullets with exact departure/arrival times, transfer count, price, and source.
- For Telegram, avoid tables; use labeled bullets.
- State prices as observed/current, not guaranteed.
- Do not book anything unless the user explicitly asks and confirms passenger/payment details.

## Workflow

1. **Clarify only if required.** If origin/destination are obvious enough, proceed and state assumptions.
2. **Resolve dates.** Use the live date/time tool before interpreting "Thursday", "Friday night", etc.
3. **Define hard constraints.** Arrival deadline, return window, budget sensitivity, baggage, car availability, passport/ID needs, emotional context.
4. **Check multiple modes in parallel when useful:**
   - Train: national/international rail APIs or carrier sites.
   - Bus: FlixBus/other coach sites.
   - Flights: Google Flights or airline sites; include airport ground transfers.
   - Driving: distance/time plus fuel/parking/tolls estimate.
5. **Prefer door-to-door usefulness over raw ticket price.** Add local transfer cost/time for airports and stations.
6. **Verify at least the top recommendation with the carrier/source page if possible.**
7. **Summarize:** recommended option, cheapest option, fastest/most comfortable option, return options, booking links/sources.

## Useful sources and techniques

### Urgent flight + ferry island transfers

When the destination has no airport or requires a ferry after flying, plan door-to-door, not just flight-to-airport.

- Identify the fastest gateway airport and the cheaper mainland fallback.
- Check the user-friendly arrival window before optimizing price. For island transfers, arriving too late can strand the user or force late speedboats.
- Search both relevant Bangkok airports when the user says "Bangkok" (e.g. BKK and DMK), but keep the final recommendation simple.
- Pair flight options with realistic ferry windows before recommending them. Allow at least 75-90 minutes from airport landing to ferry departure unless explicitly labeling a tight/risky connection.
- If airline or OTA deep-search pages are blocked by CAPTCHA/anti-bot, do not conclude there is no availability. Cross-check official schedule pages, multiple aggregator search snippets, route/flight-status pages, and ferry timetables. Present as observed availability and tell the user to verify at checkout.
- For urgent next-day travel, give a clear decision threshold: e.g. "book tomorrow if under X, otherwise shift to the fallback date/route."

See `references/bangkok-koh-phangan-flight-ferry.md` for the Bangkok → Koh Samui → Koh Phangan pattern, ferry windows, and search queries.

### European trains via DB transport.rest

For cross-border European rail, the public DB transport.rest endpoint can return journeys and sometimes fares:

```bash
python3 - <<'PY'
import urllib.request, urllib.parse, json
params = urllib.parse.urlencode({
  'from': '8400530',        # Rotterdam Centraal
  'to': '8002549',          # Hamburg Hbf
  'departure': '2026-05-13T15:00:00+02:00',
  'results': '5',
  'language': 'en',
})
url = 'https://v6.db.transport.rest/journeys?' + params
req = urllib.request.Request(url, headers={'User-Agent': 'hermes-travel-planner'})
data = json.load(urllib.request.urlopen(req, timeout=40))
for j in data.get('journeys', []):
    legs = j['legs']
    lines = [l.get('line', {}).get('name', 'walk') for l in legs if l.get('line') or l.get('walking')]
    print(legs[0].get('plannedDeparture'), '->', legs[-1].get('plannedArrival'), j.get('price'), 'via', ' | '.join(lines))
PY
```

Find station IDs first with `/locations?query=...` or a client library. Treat `partialFare: true` as incomplete and say so.

### FlixBus

FlixBus route pages often expose useful static route facts and a "See prices" interactive flow:

- Static route page gives average duration, distance, cheapest price, first/last bus, average trips/day.
- Click **See prices**, then step through dates using the next-day button.
- Capture directness, exact stops, "almost full" / "only 1 seat left", and whether arrival is next day.

### Flights

For Netherlands to nearby European cities, check Amsterdam Schiphol even when the user is near Rotterdam; smaller airports can be much worse. Include:

- Flight price and times.
- Ground transfer: e.g. Rotterdam Centraal to Schiphol train, destination airport to city center.
- Door-to-door estimate and reliability tradeoff.

### Driving estimates

When route APIs are flaky, use route-page distances or common mapping sources and calculate fuel explicitly. Example fuel estimate:

```python
km = 574
liters_per_100 = 6.5
fuel_price = 2.05
round_trip_fuel = km * liters_per_100 / 100 * fuel_price * 2
```

Add parking/tolls separately and mark as estimate.

## Pitfalls

- Do not present a single-mode answer for urgent travel unless clearly requested; compare bus/train/flight/driving.
- For funerals, medical, legal, or other emotional travel: prioritize arrival certainty and rest, not just cheapest fare.
- Avoid overloading the user with every itinerary; give the top 2-4 and a recommendation.
- Prices can change quickly; say "observed" and include booking source.
- Browser travel sites can be slow or flaky. If one source stalls, switch sources rather than waiting indefinitely.
- Do not retry blocked/timeout route commands that the environment explicitly flags as blocked.
- Do not treat OTA anti-bot blocks as route unavailability. Use snippets and independent schedule sources, then label confidence and checkout-verification needs.
- For flight-to-ferry routes, avoid recommending flights that land after the normal ferry schedule unless explicitly framed as a late/risky fallback.

## References

- `references/netherlands-hamburg-urgent-travel.md` — session notes from Rotterdam/Hamburg urgent funeral travel research, including FlixBus, DB transport.rest, KLM/Google Flights findings, and routing pitfalls.
- `references/flight-booking-calendar-fit.md` — pattern for finding a specific flight, handling blocked airline deep links, and checking whether the departure works with the user's calendar and airport buffer.

## Verification checklist

Before final response:

- Dates match the user's requested weekdays and current year.
- Arrival/departure windows are explicitly satisfied or called out as imperfect.
- Prices have sources and are not implied as guaranteed.
- Return options are included if requested.
- Booking links/sources are included without performing booking.