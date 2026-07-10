---
name: travel-accommodation
description: Research and recommend hotels, resorts, Airbnbs, and villas for client travel. Covers family-friendliness assessment, luxury evaluation, price-range estimation, and compiling with booking links.
category: knowledge
triggers:
  - find hotel
  - find resort
  - find Airbnb
  - find villa
  - accommodation research
  - family-friendly hotel
  - luxury resort
  - hotel recommendation
  - booking site
  - travel accommodation
---

# Travel Accommodation Research Skill

Research and recommend accommodations (hotels, resorts, Airbnbs, villas) for client or personal travel. Produces a ranked overview with ratings, price context, amenities, and booking links.

## Workflow

### Step 1: Gather Requirements

Ask or extract:
- Destination (city/area)
- Traveler profile: solo / couple / family with kids (ages) / group
- Preferred vibe: luxury, budget, boutique, eco, party, quiet
- Must-haves: private pool, kids club, beach access, babysitting, specific location
- Budget range per night
- Dates (if specific — affects availability/price)

### Step 2: Research Hotels & Resorts

**Primary method — DuckDuckGo HTML endpoint** (works without API key):

```python
import urllib.request, re

def ddg_search(query):
    url = "https://html.duckduckgo.com/html/"
    data = urllib.parse.urlencode({"q": query}).encode()
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"})
    html = urllib.request.urlopen(req, timeout=10).read().decode()
    results = re.findall(r'uddg=(https?[^&]+)', html)
    titles = re.findall(r'class="result__title"[^>]*>(.*?)</', html, re.DOTALL)
    return list(zip(titles, results))
```

**Search queries that work well:**
- `best family [luxury] hotels [area] [destination] [year]`
- `top 10 resorts [area] [destination] kids friendly`
- `best Airbnbs [area] [destination] family private pool`
- `luxury villas [area] [destination] private pool`

**Fallback when DDG blocks** (CAPTCHA):
- Try browser_navigate directly to known review/aggregator sites
- Try `html.duckduckgo.com/html/` with different User-Agent
- Use curl via terminal with the same URL + headers

### Step 3: Extract Details from Articles

Once you have article URLs from search results:

```python
import urllib.request, re

def extract_article_text(url):
    html = urllib.request.urlopen(url, timeout=10).read().decode()
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', html)
    return re.sub(r'\n+', '\n', text).strip()
```

Then scan for hotel/resort names and details using keyword matching:
- Hotel/resort names + star ratings
- Amenities: kids club, babysitting, pool, spa
- Pricing mentions
- Location descriptions

**Keywords:** `hotel`, `resort`, `villa`, `kids`, `family`, `club`, `pool`, `suite`, `luxury`, `price`, `rate`, `beach`, `restaurant`, `spa`

### Step 4: Research Airbnb/Villa Options

Use same DDG search with queries like:
- `Airbnb [area] [destination] family villa`
- `best Airbnb [area] [destination] private pool`
- `vacation rentals [area] [destination]`

Direct Airbnb URL:
`https://www.airbnb.com/[area]/[region]-[country]/stays`

Also check specialized villa rental sites for the destination.

### Step 5: Compile the Overview

For each option, present:

```
**[Name]** ⭐[rating]/5
- **Vibe:** [luxury / budget / boutique / family]
- **Price:** ~$XXX-XXX/night
- **Kids:** [kids club? babysitting? nurse?]
- **Location:** [area, quiet/busy, proximity to attractions]
- **Booking:** [Booking.com](link) | [Agoda](link) | [Airbnb](link) | [Direct](link)
- **Note:** [why this fits the traveler profile]
```

### Step 6: Rank with Recommendation

Always end with a top pick recommendation and why. If asked for alternatives, suggest 1-2 contrasting options (e.g. one ultra-luxury, one better value).

Include booking sites that work for the region:
- **Booking.com** — wide selection, free cancellation on many
- **Agoda** — often cheaper for Asia
- **Airbnb** — villas, apartments, family homes
- **Hotels.com** — loyalty program (10th night free)
- **Direct via resort** — sometimes better rates + upgrades

## Pitfalls

- Travel/booking sites block headless browsers (TripAdvisor, Booking.com) — use curl with real browser User-Agent as fallback, or search via DuckDuckGo HTML endpoint instead.
- Google, Bing, TripAdvisor all CAPTCHA from headless — DDG HTML endpoint is the most reliable.
- Airbnb listing pages are JavaScript-heavy — the initial HTML may not contain full listing data.
- Price ranges are seasonal — mention that rates vary by season.
- "Family-friendly" means different things — a baby needs different amenities than a 10yo.
- Article data can be stale — check publication dates; prices and ratings change.
- DuckDuckGo HTML endpoint may also CAPTCHA after many requests — space queries 2-3 seconds apart via time.sleep().