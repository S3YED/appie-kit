# Flight booking + calendar-fit checks

Use this when the user asks for a specific flight and whether it works with their schedule.

## Pattern

1. Resolve the requested date with the live date/time tool before searching.
2. Search Google Flights first for broad availability and price. Extract exact displayed flights from the page if needed with browser DOM text, not just the visible snapshot.
3. If the airline site blocks automation or does not expose a stable deep link, give the Google Flights query link and tell the user exactly which flight row to select. Do not pretend it is a carrier checkout link.
4. Check the user's calendar for the full local day at the relevant travel timezone. For Thailand domestic flights, use `+07:00` day boundaries.
5. Assess conflicts against the actual flight departure and a realistic airport buffer. For USM domestic flights, assume the user should be at the airport around 45-60 minutes before departure unless they state otherwise.
6. Recommend the next viable flight if the requested flight overlaps a meeting or airport arrival buffer.

## Example from USM to BKK

For a 17:35 USM -> BKK flight on 18 June:

- Calendar had meetings 15:00-16:00, 16:00-17:00, and 17:00-18:00 Bangkok time.
- The 17:35 departure directly overlapped the 17:00-18:00 call and also required leaving before the call ended.
- Better recommendations were later nonstop Bangkok Airways flights, especially 18:55 -> 20:25 when available.

## Output shape

- Direct link or best available search link first.
- State the exact flight row: departure, arrival, airline, route, price shown.
- Then schedule verdict: `works`, `tight`, or `does not work cleanly`.
- Name the conflicting calendar windows without dumping private attendee lists.
- Give one safer alternative.