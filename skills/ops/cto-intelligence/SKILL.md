---
name: cto-intelligence
title: CTO Intelligence Briefing
description: Set up recurring cron jobs that monitor a technology domain and deliver formatted briefings. Covers search strategy, domain categorization, briefing format, and delivery via Telegram.
---

# CTO Intelligence Briefing

Set up recurring monitoring for a technology domain and deliver formatted briefings. Use when asked to set up daily/weekly monitoring, a briefing, a cron job for news, or "keep me updated" about a tech domain.

## Structure

### 1. Identify the Domain

Clarify scope:
- **Core domain** (e.g., agentic AI, cybersecurity, LLM ops)
- **Sub-categories** to monitor
- **Delivery preference** (Telegram DM, email, daily/weekly)
- **Time preference** (morning, evening, specific hour)

### 2. Search Strategy

For each sub-category, define 2-3 search queries:

```
Category: [name]
Queries:
  - "latest [category] news 2026"
  - "[category] update release 2026"
  - "new [category] tool framework 2026"
```

#### Available Search Methods

| Method | Best for | Notes |
|--------|----------|-------|
| DuckDuckGo lite (Python urllib) | Broad category searches (5-10 categories) | Preferred for breadth-first research. Direct URLs, no hallucination. |
| `delegate_task` with web toolsets | Deep-dive on 1-3 topics needing synthesis | Max 3 concurrent. Verify key claims via browser. |
| HN Algolia API via curl | Real-time tech/AI news | Best single source. Use broadest keyword first. |
| Browser to HN front page | What's trending right now | Complementary to Algolia search. |

#### Two-Pass Search Workflow

**Pass 1 — HN Algolia (parallel broad queries):** Use curl to search_by_date endpoint. Filter by `created_at_i` timestamp in Python. No auth required.

**Pass 2 — DDG lite for gaps:** Run DDG lite batch for categories with thin coverage. Rate limit: 2 seconds between queries.

If both passes return empty, the topic had no news that day — record as quiet and move on.

#### Cron-Compatible Search Methods

In cron context, `execute_code` and `browser_navigate` are blocked. Use terminal-only:

```bash
# HN Algolia API via curl
curl -s 'https://hn.algolia.com/api/v1/search_by_date?query=KEYWORD&tags=story&hitsPerPage=30' --max-time 15 | python3 -c "
import json, sys, time
data = json.load(sys.stdin)
now = time.time()
for h in data.get('hits', []):
    ts = h.get('created_at_i', 0)
    age_hours = (now - ts) / 3600
    if age_hours > 48: continue
    title = h.get('title', '')[:120]
    pts = h.get('points', 0)
    url = h.get('url', '') or 'https://news.ycombinator.com/item?id=' + str(h.get('objectID', ''))
    print(f'{age_hours:5.1f}h | {pts:>4}pts | {title}')
    print(f'       {url}')
"
```

```bash
# DDG Lite via Python in terminal
python3 -c "
import urllib.request, urllib.parse, re, time

def ddg_search(query):
    url = 'https://lite.duckduckgo.com/lite/'
    data = urllib.parse.urlencode({'q': query}).encode()
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=10)
    html = resp.read().decode('utf-8', errors='replace')
    results = re.findall(r'<a[^>]*href=\"(https?://[^\"]+)\"[^>]*>(.*?)</a>', html)
    return [(t.strip(), u) for t, u in results if t.strip() and 'duckduckgo' not in u.lower()][:5]

for q in ['query 1', 'query 2', 'query 3']:
    print(f'=== {q} ===')
    for title, url in ddg_search(q):
        print(f'  {title[:100]} -> {url}')
    time.sleep(2)
"
```

### 3. Build the Cron Job

Use `cronjob` tool with:

| Field | Value |
|-------|-------|
| `name` | `daily-[domain]-briefing` |
| `schedule` | `0 7 * * *` for daily 07:00, `0 8 * * 1` for weekly Monday |
| `deliver` | `telegram:<user_id>` |
| `prompt` | Self-contained briefing instructions |

The prompt must be self-contained. Include actual search methodology, not just categories.

### 4. Post-Delivery Workflow

When user asks to act on a briefing:

1. **Categorize findings:** 🔴 Check (CVEs), 🟢 Install (tools), 📡 Monitor (trends), ℹ️ Note (no action)
2. **Evaluate each tool/project:** Visit GitHub, check stars, commits, releases, dependencies
3. **Verify security claims across fleet:** Check if affected packages are installed on all nodes
4. **Install selected tools:** Standard workflow (clone/build, smoke test, save knowledge doc)
5. **Save to knowledge store:** Write findings to a dated knowledge file

### 5. Pitfalls

- Subagents hallucinate release versions, CVEs, and dates — always verify.
- HN Algolia uses `search_by_date` endpoint, NOT `search?sort=byDate` (returns 400).
- `execute_code` and `patch` are blocked in cron context — use `terminal` with Python or `curl`.
- DDG lite can return 0 results — pivot to HN Algolia when that happens.
- `printf` breaks with emoji and `%` characters — use Python `with open` for file appends.
- Always check publication dates — stale articles can appear as top results.
- Use `[SILENT]` (exact, no other text) to suppress delivery when nothing new to report.