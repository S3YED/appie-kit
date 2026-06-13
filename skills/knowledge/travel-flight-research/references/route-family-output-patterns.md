# Route-family output patterns

Use this when a user asks for "all flights", "the first route", or a route from point A to point C where the practical answer is a multi-leg itinerary.

## Output order
1. Direct first leg, if it exists.
2. Onward leg options, grouped by hub or carrier family.
3. Best complete itinerary recommendation.
4. Clean links for each leg or route page.

## Practical rules
- Name the route family explicitly, for example `USM -> BKK -> RMO`.
- Treat the direct leg and the final leg as separate research problems.
- If the final destination has no nonstop from the origin, identify the most practical hub(s) first.
- Prefer route pages that show the whole routing structure and airline options.
- Use aggregator snippets only for fare context or when the canonical page is blocked.
- For airline-specific route pages, verify that the link lands on the exact route, not a generic homepage or search wrapper.

## Suggested response shape
- Route family name
- Leg 1 with 1 to 3 links
- Leg 2 with 1 to 3 links
- Cheapest or fastest note
- Short recommendation

## Example wording
- "USM -> BKK is nonstop and operated by Bangkok Airways."
- "BKK -> RMO is usually one-stop, with Turkish, Austrian, LOT, Lufthansa, and EL AL appearing in route directories."
- "Best cheap family: USM -> BKK -> RMO."
