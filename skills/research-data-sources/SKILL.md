---
name: research-data-sources
description: "Query online research data sources: arXiv papers, RSS/blog feeds (blogwatcher), and Polymarket prediction markets. Single-skill index with per-source reference docs."
version: 1.0.0
author: Hermes Agent (umbrella, absorbing arxiv, blogwatcher, polymarket)
license: MIT
metadata:
  hermes:
    tags: [research, arxiv, papers, rss, feeds, blogwatch, polymarket, prediction-markets, data-sources]
    related_skills: [llm-wiki, research-paper-writing]
---

# Research Data Sources

This umbrella skill covers three online data-sourcing tools. Use the decision table below to pick the right one, then jump to the reference file for detailed commands.

## Quick Decision

| You want to... | Use | Reference |
|---|---|---|
| Search academic papers by keyword, author, category | **arXiv** | `references/arxiv.md` |
| Monitor blogs and RSS/Atom feeds for new content | **Blogwatcher** | `references/blogwatcher.md` |
| Query prediction market prices, orderbooks, history | **Polymarket** | `references/polymarket.md` |

---

## arXiv (`references/arxiv.md`)

Search and retrieve papers from arXiv's free REST API. No API key needed — just curl.

**Quickest command:**
```bash
curl -s "https://export.arxiv.org/api/query?search_query=all:YOUR+QUERY&max_results=5" | python3 -c "
import sys, xml.etree.ElementTree as ET
for e in ET.fromstring(sys.stdin.read())[0].findall('{http://www.w3.org/2005/Atom}entry'):
    title = e.find('{http://www.w3.org/2005/Atom}title').text.strip().replace(chr(10),' ')
    print(f'{title[:80]}')
"
```

Script: `scripts/search_arxiv.py`

---

## Blogwatcher (`references/blogwatcher.md`)

Track blog and RSS/Atom feed updates via the `blogwatcher-cli` tool. Supports automatic feed discovery, HTML scraping fallback, OPML import.

```bash
# Install
go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest

# Add feed
blogwatcher-cli add https://blog.nousresearch.com/feed.xml

# Scan for new articles
blogwatcher-cli scan
```

---

## Polymarket (`references/polymarket.md`)

Query prediction market data from Polymarket's public REST APIs. All read-only, no auth needed.

**Quickest commands:**
```bash
# Search markets
curl -s "https://gamma-api.polymarket.com/public-search?q=QUERY"

# Price history for a condition
curl -s "https://clob.polymarket.com/price/condition/CONDITION_ID"
```

Full endpoint reference: `references/polymarket-api-endpoints.md`
Script: `scripts/polymarket.py`