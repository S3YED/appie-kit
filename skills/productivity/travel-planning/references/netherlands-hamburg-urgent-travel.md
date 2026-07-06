# Netherlands to Hamburg urgent travel research notes

Session context: user near Rotterdam needed to reach Hamburg for a funeral, arriving Wed evening or Thu early, returning Fri night or Sat early. Dates researched: Wed 13 May 2026 to Sat 16 May 2026.

## Current-source techniques that worked

### FlixBus browser flow

- Route page: `https://global.flixbus.com/bus-routes/bus-rotterdam-hamburg`
- Reverse: `https://global.flixbus.com/bus-routes/bus-hamburg-rotterdam`
- Click **See prices** on the route page, then step dates with the next-day button.
- Snapshot text exposes usable structured details: exact departure/arrival, direct/transfer, price, stops, duration, capacity hints.

Observed examples from the session:

- Rotterdam -> Hamburg, Wed 13 May:
  - 08:40 -> 16:55 direct, Rotterdam CS -> Hamburg ZOB, €81.98.
  - 21:45 -> 07:00 Thu, 1 transfer, Rotterdam Zuidplein -> Hamburg ZOB, €98.47, only 1 seat available.
  - 22:05 -> 07:00 Thu, 1 transfer, Rotterdam CS -> Hamburg ZOB, €98.47, only 1 seat available.
- Rotterdam -> Hamburg, Thu 14 May:
  - 19:00 -> 02:20 Fri direct, €62.98.
  - 00:20 Fri -> 08:25 Fri direct, €50.98.
- Hamburg -> Rotterdam, Fri 15 May:
  - 21:00 -> 04:45 Sat direct, Hamburg ZOB -> Rotterdam CS, €50.98.
  - 22:30 -> 08:15 Sat, 1 transfer, to Rotterdam Zuidplein, €56.97.
  - 03:55 Sat -> 11:30 Sat direct, €52.98.

Static FlixBus page facts observed:

- Rotterdam -> Hamburg: average duration 7h57m, distance 574 km, cheapest from €35.47, first bus 00:20, last bus 22:05, 7 rides/day.
- Hamburg -> Rotterdam: average duration 7h49m, distance 570 km, cheapest from €34.47, first bus 01:10, last bus 22:30, 7 rides/day.

### DB transport.rest rail query

The `db-vendo-client` package stalled in one run, but the public HTTP API worked quickly:

```bash
python3 - <<'PY'
import urllib.request, urllib.parse, json
params = urllib.parse.urlencode({
  'from': '8400530',
  'to': '8002549',
  'departure': '2026-05-13T15:00:00+02:00',
  'results': '5',
  'language': 'en',
})
url = 'https://v6.db.transport.rest/journeys?' + params
req = urllib.request.Request(url, headers={'User-Agent':'hermes-travel-planner'})
data = json.load(urllib.request.urlopen(req, timeout=40))
for j in data.get('journeys', []):
    legs = j['legs']
    lines = [l.get('line', {}).get('name', 'walk') for l in legs if l.get('line') or l.get('walking')]
    print(legs[0].get('plannedDeparture'), '->', legs[-1].get('plannedArrival'), j.get('price'), 'via', ' | '.join(lines))
PY
```

Station IDs used:

- Rotterdam Centraal: `8400530`
- Hamburg Hbf: `8002549`

Observed rail examples:

- Wed 13 May outbound:
  - 15:50 Rotterdam -> 22:32 Hamburg, €84.99, via IC/RB61/ICE, 3 transfers.
  - 15:20 -> 21:32, €119.99, via IC/ICE, 3 transfers.
  - 12:53 -> 19:28, €64.99 but `partialFare: true`, so incomplete fare.
- Thu 14 May outbound:
  - 07:20 -> 13:28, €77.99 but `partialFare: true`.
  - 07:50 -> 14:32, €121.80.
- Fri 15 May return:
  - 18:23 Hamburg -> 01:10 Sat Rotterdam, €48.99.
  - 17:23 -> 00:10 Sat, €64.99.
  - 19:23 -> 02:57 Sat, €35.99 but 4 transfers.
- Sat 16 May early return:
  - 05:22 -> 12:10, €48.99.

## Flight findings from delegated browser research

- Rotterdam The Hague Airport to Hamburg was not practical: observed around €1,170 round trip with London connection/airport change.
- Amsterdam Schiphol was the practical airport from Rotterdam.
- KLM direct examples:
  - Wed 13 May AMS 16:50 -> HAM 17:50, observed from about €396 round trip with Sat return.
  - Wed 13 May AMS 20:50 -> HAM 21:55, more expensive, roughly €574-€725 round trip depending return.
  - Thu 14 May AMS 06:55 -> HAM 07:55, observed from about €346 round trip with Sat return; much higher with Fri return.
- Add door-to-door ground transport:
  - Rotterdam Centraal -> Schiphol: roughly 25-30 min by train, around €17-20 one-way including supplement depending ticket.
  - Hamburg airport -> city center: S-Bahn S1 roughly 25 min, around €3-4.
  - Total ground transport estimate: roughly €45-55 round trip.

## Routing pitfalls

- `maps_client.py distance "Rotterdam Centraal" --to "Hamburg Hauptbahnhof" --mode driving` failed with OSRM SSL handshake error.
- Direct `curl` to OSRM later timed out and was blocked by the environment; do not retry the same blocked command.
- Use FlixBus route distance (~570-574 km) or another mapping source as fallback, then compute fuel explicitly.

Fuel estimate used:

- 574 km one way, 6.5 L/100km, €2.05/L petrol -> about €76 one-way fuel, €153 round-trip fuel.
- Add Hamburg parking separately; rough estimate €20-40+.

## Presentation pattern that worked

For urgent/emotional travel, answer with:

1. One-sentence compassion.
2. `My recommendation` with best mode.
3. `Best budget option`, `Best comfort/speed`, `Best train option`.
4. Prices and times as bullets, no table.
5. Booking/source link.
6. A plain-English take: which option to choose based on arrival deadline.
