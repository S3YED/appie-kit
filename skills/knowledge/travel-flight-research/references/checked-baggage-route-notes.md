# Checked-baggage route notes

Use this when the user says checked baggage is required and you need to compare route families quickly.

## Decision rule
- Exclude fares labeled `Light`, `Basic`, `Hand baggage only`, or similar unless the fare page explicitly shows a checked bag.
- Prefer itineraries where the baggage allowance is attached to the full ticket, not just one leg.
- If a connection is on separate tickets, do not assume through-check baggage is available.

## Useful route-family heuristics for USM -> RMO
- `USM -> BKK` is a clean nonstop on Bangkok Airways.
- `BKK -> IST -> RMO` is usually the best balance of price and convenience when checked baggage is required.
- `BKK -> VIE -> RMO` is a solid backup.
- `BKK -> DOH -> RMO` can work, but often prices higher.
- `BKK -> RMO` searches may surface multiple airlines, but not all fare families include checked bags.

## Carrier baggage reminders
- Bangkok Airways: baggage allowance info is published on its baggage pages; through-check guidance exists for participating carriers.
- Turkish Airlines: checked baggage is included on all flights, but exact allowance varies by route and booking.
- Qatar Airways: checked baggage is included on all flights.
- Lufthansa / Austrian / EL AL: verify fare family before recommending, because lower fare types may exclude checked baggage.

## Link-handling tip
When presenting links, use the direct route page or baggage page, not a search redirect wrapper. Clean `&rut=` and other tracker suffixes before sharing.