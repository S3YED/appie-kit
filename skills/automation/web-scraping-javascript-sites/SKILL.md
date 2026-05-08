---
name: web-scraping-javascript-sites
version: 1.0.0
description: Scrape TypeScript, React, Next.js, Nuxt, Vue SPA sites. Know when to use raw HTML fetch vs browser automation.
metadata:
  owner: appie-3
  created: 2026-04-08
  tags: [scraping, e2e, testing, typescript, spa, react, nextjs]
---

# Web Scraping JavaScript/SPA Sites

## The Core Insight

> **For SPA/TypeScript sites: try `urllib` FIRST before launching a browser.**

TypeScript sites (Next.js, Nuxt, React, Vue) send full HTML on first request — the content is there. Browser tools show empty snapshots because they capture before JS finishes rendering. A raw HTTP fetch often gets all the data you need.

## Decision Tree

```
Is the site an SPA (React/Next/Nuxt/Vue)?
│
├── YES → Try urllib/requests FIRST
│         └─ Got content? → DONE
│         └─ Content empty? → Use Playwright
│
└── NO (static HTML) → Use urllib/requests directly
```

## Layer 1: Raw HTML Fetch (Fastest)

```python
import urllib.request
import re

url = "https://example.com"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
response = urllib.request.urlopen(req, timeout=10)
html = response.read().decode('utf-8')

# Extract content
# Option A: regex search
prices = re.findall(r'€[\d,]+', html)

# Option B: find section context
section = re.search(r'id="pricing".{0,5000}', html, re.DOTALL | re.IGNORECASE)
if section:
    content = re.sub(r'<[^>]+>', ' ', section.group())
    content = re.sub(r'\s+', ' ', content).strip()

# Option C: parse HTML properly
from html.parser import HTMLParser
class ContentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_target = False
        self.text = []
    def handle_starttag(self, tag, attrs):
        if tag in ('h1','h2','h3','p', 'li'):
            self.in_target = True
    def handle_data(self, data):
        if self.in_target:
            self.text.append(data.strip())
    def handle_endtag(self, tag):
        if tag in ('h1','h2','h3','p', 'li'):
            self.in_target = False
```

### Why urllib Often Works for "Lazy" Sites

Many TypeScript/React sites pre-render HTML on the server (SSR) or send full content in initial HTML, but use JS to make it look animated/lazy. The data is in the first response — you just need to parse it.

## Layer 2: Playwright (When Needed)

Use when:
- Content loads via AJAX/fetch calls AFTER page load
- Content requires user interaction (click to expand, scroll, login)
- Site has strong bot detection
- Single-page app with client-side routing

### Setup

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Human-like headers
    page.set_extra_http_headers({
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    })
    page.set_viewport_size({"width": 1920, "height": 1080})
    
    # Navigate and wait properly
    page.goto(url, wait_until='networkidle', timeout=30000)
    
    # Wait for specific content (NOT just page load)
    page.wait_for_selector(".pricing-card", timeout=10000)
    
    # Extract
    content = page.text_content("body")
    
    browser.close()
```

### Waiting Patterns (Humanize)

```python
# ❌ Robot: instant read after click
page.click("button")
result = page.text_content(".result")  # Empty!

# ✅ Human: wait for DOM change
page.click("button")
page.wait_for_selector(".result:not(:empty)", timeout=5000)
result = page.text_content(".result")

# ❌ Robot: no wait
page.goto(url)
title = page.text_content("h1")

# ✅ Human: wait for content
page.goto(url)
page.wait_for_selector("h1", timeout=10000)
title = page.text_content("h1")
```

### Scroll Like a Human

```python
for _ in range(3):
    page.mouse.wheel(0, 500)
    page.wait_for_timeout(300)
```

### Hover Before Click (Pass Sophisticated Bot Detection)

```python
page.hover("nav .menu-item")
page.wait_for_timeout(100)
page.click("nav .menu-item")
```

## Stealth Mode (Puppeteer Extra)

For sites with bot detection:

```javascript
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

(async () => {
  const browser = await puppeteer.launch({ 
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.goto('https://bot-detected-site.com');
  // ...
})();
```

Available at: `/root/.hermes/hermes-agent/node_modules/puppeteer-extra-plugin-stealth`

## TypeScript Site Patterns

### Next.js Static Export
```python
# These are fully scrapeable with urllib - HTML is complete
page.goto("https://site.com/page")
# Content is in initial HTML
```

### Next.js SSR
```python
# Server renders full HTML - urllib works
page.goto("https://site.com/page")
```

### Client-Side Only (CRA/Vite)
```python
# Must use Playwright - no HTML content without JS
page.goto("https://site.com/page")
page.wait_for_selector(".content")
```

### Nuxt/Vue
```python
# Often SSR with hydration - urllib works
page.goto("https://site.com/page")
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Element not found | Add `wait_for_selector()` before interacting |
| Page loads blank | Use `wait_until='networkidle'` |
| Bot detection | Use puppeteer-extra with StealthPlugin |
| Lazy loading | Scroll or wait for specific element |
| Cloudflare challenge | Try fetching Cloudflare clearance cookie first, or use Playwright |
| CAPTCHA | Cannot be bypassed programmatically in most cases |

## Bot Detection Bypass

```python
# Try these headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}
```

## Tools Available on Appie-3 VPS

| Tool | Location | Use |
|------|----------|-----|
| **playwright** | `/root/.hermes/hermes-agent/node_modules/playwright` | Browser automation |
| **puppeteer-extra + stealth** | Same | Bot-evasion browser |
| **httpx** | Python venv | Async HTTP |
| **requests** | Python venv | Simple HTTP |
| **urllib** | Python stdlib | Raw HTML fetch |

## Quick Test Script

```python
#!/usr/bin/env python3
"""Test if a site is scrapeable with urllib or needs Playwright"""

import urllib.request
import sys

def test_site(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    try:
        response = urllib.request.urlopen(req, timeout=10)
        html = response.read().decode('utf-8')
        print(f"SUCCESS: {len(html)} bytes received")
        
        # Check for meaningful content
        if len(html) < 5000:
            print("WARNING: Very small HTML - likely needs JS rendering")
            return False
        
        # Check for text content
        import re
        text = re.sub(r'<[^>]+>', '', html)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"Text content: {len(text)} chars")
        
        if text.count(' ') < 50:
            print("WARNING: Little text content - likely JS-rendered SPA")
            return False
            
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://weblyfe.ai/openclaw"
    print(f"Testing: {url}")
    can_scrape = test_site(url)
    print(f"\nRecommendation: {'urllib works' if can_scrape else 'Use Playwright'}")
```

Run: `python3 /root/.hermes/skills/web-scraping-javascript-sites/scripts/test-site.py https://example.com`

## See Also

- `skills/playwright` — Full Playwright reference
- `skills/ui-ux-pro-max` — For taking screenshots of scraped sites
