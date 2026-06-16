---
name: web-research
title: Web Research
description: Research any topic via web search, content extraction, and multi-source synthesis. Covers DuckDuckGo lite scraping, browser-based extraction, and parallel delegated research.
trigger: User asks to research, investigate, find information about, or look up any topic on the web.
---

# Web Research Skill

## Tools Available

| Tool | When to use |
|------|------------|
| `execute_code` (Python) + DuckDuckGo lite | FIRST - fastest, no auth needed. Use for initial search queries to find relevant URLs. |
| `browser_navigate` | After getting URLs from search. Navigate directly to known-good pages. |
| `browser_console` + `document.body.innerText` | When browser_snapshot truncates (large pages). Extract full text via JS evaluation. |
| `delegate_task` | For multi-source parallel research. Split 3-5 sources across subagents, each extracts one page. |
| Curl + jq | For APIs that return JSON (GitHub, HN, Reddit). No auth needed for public endpoints. |

## Primary Search Method: DuckDuckGo HTML

DuckDuckGo's HTML endpoint works without any API key or login and returns structured results. Two variants:

### Method A: `html.duckduckgo.com/html/` (GET - preferred)

Use curl with a real browser User-Agent (the HTML endpoint is more resilient than lite):

```bash
curl -sL "https://html.duckduckgo.com/html/?q=<query>" -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
```

Parse results with Python `re.findall(r'uddg=(https?[^&]+)', html)` for URLs, and extract titles from `class="result__title"` elements.

### Method B: `lite.duckduckgo.com/lite/` (POST - fallback)

Use Python's `urllib` when you need programmatic access:

```python
import urllib.request, urllib.parse, re

def search_ddg(query):
    url = "https://lite.duckduckgo.com/lite/"
    data = urllib.parse.urlencode({"q": query}).encode()
    req = urllib.request.Request(url, data=data)
    req.add_header("User-Agent", "Mozilla/5.0")
    resp = urllib.request.urlopen(req, timeout=10)
    html = resp.read().decode()
    results = re.findall(r'<a[^>]*href="(https?://[^"]*)"[^>]*>([^<]*)</a>', html)
    return [(title.strip(), href) for title, href in results if title.strip() and len(title.strip()) > 10]
```

After getting URLs, visit the top 3-5 results via browser_navigate for details.

## Full-Text Extraction from Large Pages

Browser snapshots truncate. Use `browser_console` with JS:

```javascript
document.body.innerText
```

Use `substring(0, 8000)` to get a controllable chunk when the full text is too large:

```javascript
document.body.innerText.substring(0, 8000)
```

## Multi-Source Parallel Research Pattern

For topics that need synthesis across multiple sources:

1. Run DDG search to get candidate URLs
2. Pick 3-5 diverse, authoritative-looking sources
3. Delegate each to a subagent via `delegate_task` with explicit extraction instructions
4. Compile results into structured output

## Pitfalls

- **Dutch ambiguity: "veiligheid"** - When Seyed asks about "veiligheid skills" or "veiligheid tools" in Dutch, always clarify: does he mean **cybersecurity** (firewalls, pentesting, CVEs) or **AI agent safety/agentic skills** (MCP, tool use, prompt injection, agent orchestration)? These are completely different domains. Default to asking before researching.
- **Exa.ai playground requires login** - cannot use without API key. Fall back to DDG lite.
- **404s are common** on older URLs from search results - skip and try the next result.
- **JavaScript-heavy SPAs** may not render fully in the browser. Try extracting via browser_console or find a lighter version of the page.
- **Rate limiting** - DDG lite is fast but has limits. Space requests 1-2 seconds apart if doing many.
- **SANS.org** and similar security training sites consistently return 404 on deep links - navigate from their homepage instead.
- **Wikipedia** always works and loads fast - good fallback for foundational knowledge.
- **Booking/travel sites** (12Go, airline sites) often block headless browsers or have aggressive bot detection. Use route-specific URLs (e.g. `/en/travel/bangkok/koh-samui`) to skip homepage search forms. Cross-reference listing prices with the schedule table - booking platforms often show markup prices in the main view vs operator-direct prices in the bottom schedule table. **Google Flights** is a reliable fallback when airline sites block - just note prices default to round-trip.

## Reference Files

- `references/cybersecurity-skills-tools-2025.md` - condensed research findings from a session on top cybersecurity skills and pentesting tools for 2025-2026.
- `references/agentic-ai-landscape-2025.md` - agentic AI frameworks, protocols, tools, security, and learning resources. Covers LangChain, CrewAI, AutoGen, MCP, A2A, ACP, vector DBs, observability.
- `references/travel-booking-extraction.md` - extracting schedules, prices, and routes from booking/travel sites (12Go.asia) via browser tools. Covers route-specific URLs, console-based full-schedule extraction, date button selection, and the 12Go listing-vs-schedule price markup pattern.
