# Canonical links for flight research

## Goal
When collecting flight options for a user-facing message, use clean destination URLs instead of search redirect links.

## Preferred sources
- Google Flights route pages for quick discovery and canonical route lookup.
- FlightConnections for route structure and direct-route verification.
- Airline booking pages for direct bookability when available.
- Skyscanner, Expedia, Trip.com only for fare signals when canonical pages are unavailable or protected.

## Link cleaning rules
- Remove DuckDuckGo redirect wrappers like `https://duckduckgo.com/l/?uddg=...`.
- Decode the `uddg` value to the actual target URL.
- Remove tracking suffixes like `&rut=...` when they are not part of the canonical destination.
- Prefer route pages such as:
  - `https://www.google.com/travel/flights/flights-from-ko-samui-to-bangkok.html`
  - `https://www.flightconnections.com/flights-from-usm-to-bkk`
  - `https://www.skyscanner.com/routes/vie/rmo/vienna-to-chisinau.html`

## Verification checklist
- The URL opens the intended route page directly.
- The page title matches the route.
- The link is stable enough to share in chat.
- The response is concise and ready to forward.

## Example pattern
- Search with broad phrases to find the best candidate route page.
- Open or inspect the result.
- Replace any redirect URL with the canonical destination URL.
- Present the cleaned links in the user's requested language.
