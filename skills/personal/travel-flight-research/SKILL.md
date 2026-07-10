---
name: travel-flight-research
description: Research flight options, compare route families, and present clean booking links and concise recommendations.
---

# Travel Flight Research

Use this skill when the user asks for flight options, route comparisons, fare discovery, or a shareable message listing booking links.

## Workflow
1. Identify the exact origin, destination, dates, and whether the ask is for cheapest, fastest, best-balance, or a route-family breakdown.
2. Search broadly first to discover viable route families and fare signals.
3. If the user asks for "all flights" or "the first route", treat that as a route-family request and list legs separately. Start with the direct leg, then the onward leg, then the practical complete itinerary.
4. If the user requires checked baggage, filter out `Light`, `Basic`, `Hand baggage only`, and similar fare families unless the fare page explicitly shows a checked bag included.
5. Prefer route families where the baggage allowance is attached to the full ticket, not just one leg. Do not assume through-check baggage on separate tickets.
6. Prefer canonical booking pages for the final answer:
   - Google Flights route pages
   - FlightConnections route pages
   - Airline pages when they are direct and stable
   - Skyscanner, Expedia, Trip.com only when needed for fare context or when canonical pages are unavailable
7. When airline-specific route pages are sparse or partially blocked, use route directories to identify operating carriers and pair them with price-context pages from aggregators.
8. Strip tracking wrappers and redirect URLs before presenting links.
9. If a search result page is a redirect or tracker, replace it with the underlying canonical URL.
10. Keep the final response concise and practical. If the user wants a message, format it as a ready-to-send message in the requested language.

## Link rules
- Prefer direct URLs over DuckDuckGo / search redirect links.
- Prefer route pages, not generic home pages.
- When possible, use the exact route query URL that a human can click and immediately inspect.
- Verify that the final URL is the actual destination page, not a search wrapper or consent interstitial.

## Good answer shape
- Route family name
- Short price / convenience note
- 1 to 2 links per leg
- A brief recommendation at the end

## Pitfalls
- Do not paste search engine redirect links.
- Do not include broken tracking parameters if a canonical destination exists.
- Do not recommend fares that omit checked baggage when the user explicitly needs a checked bag.
- Do not assume a checked bag will be through-checked across separate tickets.
- Do not over-explain if the user asked for a message or link list.
- For urgent same-day missed-transfer cases, do not return a generic travel overview. Prioritize departures still catchable now and include a fallback for sold-out/last-boat scenarios.

## Urgent disruption pattern (missed pickup / delayed arrival)
When the traveler is already in transit and under time pressure:
1. Compute local time first and state it clearly.
2. Rank options by "can still catch now" rather than cheapest.
3. Lead with the next 1-3 departures and booking links.
4. Add a fast fallback tree:
   - online booking now,
   - taxi to pier plus walk-up ticket,
   - first departure next morning.
5. Keep response short, operational, and decision-oriented.

## Anti-bot / blocked-source fallback
If browser automation or aggregator pages are blocked (403/202/challenge):
1. Fall back to terminal HTTP fetches for operator and route pages.
2. Prefer pages that embed schedule data directly in HTML or inline JSON.
3. Extract concrete departures, arrivals, and price ranges from embedded route objects when available.
4. Cross-check with a second source for sanity (operator page + aggregator summary).
5. Be explicit that times and seat availability are live and must be re-checked before payment.

## Checked-baggage shortcut
- When checked baggage is mandatory, the default priority for this route family is usually:
  1. `USM -> BKK -> IST -> RMO` on Turkish Airlines
  2. `USM -> BKK -> VIE -> RMO` on Austrian Airlines
  3. `USM -> BKK -> DOH -> RMO` on Qatar Airways if it is clearly cheaper or better timed
- Bangkok Airways on the first leg is the clean nonstop choice from Samui; then verify the onward long-haul fare includes a checked bag before presenting it as the winner.
## Support files
- See `references/canonical-links.md` for a compact link-cleaning playbook and route-page examples.
- See `references/route-family-output-patterns.md` for how to answer "all flights" and multi-leg route-family requests cleanly.
