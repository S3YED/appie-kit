---
title: "Web Scraping: Tools, Techniques & Performance"
author: Kudosx Team
date: 2025-12-07
tags: [scraping, yt-dlp, requests, performance, optimization]
---

# Web Scraping: Tools, Techniques & Performance

## The Golden Rule

**The fastest scraping is no browser at all.**

Before writing any code, ask: What's the simplest tool for this job?

```
Speed & Reliability Hierarchy:

1. Official APIs        (~100ms)  - Best: rate limits, stable, documented
2. CLI Tools            (~1-2s)   - yt-dlp, curl, wget - battle-tested
3. HTTP + Regex/JSON    (~1-3s)   - requests + parsing, no JS needed
4. Headless Browser     (~5-10s)  - Playwright, Puppeteer
5. Headed Browser       (~10-20s) - Visible browser, last resort
```

---

## Tool Selection Guide

### Quick Reference

| Task | Best Tool | Speed |
|------|-----------|-------|
| YouTube search/download | `yt-dlp` | ~1.5s |
| Image search | `duckduckgo-search` | ~2-3s |
| TikTok download | `yt-dlp` + cookies | ~2-3s |
| Static HTML | `requests` + `BeautifulSoup` | ~0.5s |
| JSON APIs | `requests` | ~0.3s |
| File downloads | `aria2c`, `wget`, `curl` | varies |

### Speed Comparison

| Method | YouTube Search | Image Search | API Call |
|--------|---------------|--------------|----------|
| CLI (yt-dlp) | 1.5s | N/A | 0.3s |
| DuckDuckGo lib | N/A | 2-3s | N/A |
| Python requests | N/A | N/A | 0.5s |
| Playwright headless | 6-10s | 15s | 2s |
| Selenium | 10-15s | 20s+ | 3s |

---

## Real Examples

### YouTube Search

```python
# SLOWEST: Selenium (~15-20s)
driver = webdriver.Chrome()
driver.get(f"https://youtube.com/results?search_query={keyword}")
# ... wait, scroll, parse DOM

# SLOW: Playwright (~6-10s)
page.goto(f"https://youtube.com/results?search_query={keyword}")
# ... wait for JS, extract data

# FAST: youtube-search-python (~2-3s)
from youtubesearchpython import VideosSearch
search = VideosSearch(keyword, limit=10)
results = search.result()

# FASTEST: yt-dlp CLI (~1.5s)
cmd = ["yt-dlp", f"ytsearch{num}:{keyword}", "--dump-json", "--flat-playlist"]
result = subprocess.run(cmd, capture_output=True, text=True)
```

**Lesson:** yt-dlp already solved YouTube scraping. Don't reinvent the wheel.

### Image Search

```python
# SLOWEST: Click thumbnails (~110s for 20 images)
for thumb in page.locator("img[data-src]").all():
    thumb.click()
    # ... wait for full image, extract URL

# SLOW: Playwright + regex (~15s for 100 images)
page.goto(f"https://google.com/search?q={keyword}&tbm=isch")
html = page.content()
urls = re.findall(r'\["(https?://[^"]+)",\s*\d+,\s*\d+\]', html)

# FASTEST: DuckDuckGo library (~2-3s for 100 images, NO BROWSER)
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    results = list(ddgs.images(keywords=keyword, max_results=100))
    urls = [r["image"] for r in results]
```

**Lesson:** DuckDuckGo provides free image search API. No browser, no API key needed.

### TikTok Search & Download

```python
# WILL NOT WORK: Headless mode (TikTok blocks it)
browser = p.chromium.launch(headless=True)  # BLOCKED!
page.goto("https://tiktok.com/search?q=...")
# Error: Captcha detected or page blocked

# WORKS: Headful mode with stealth flags
browser = p.chromium.launch(
    headless=False,  # REQUIRED for TikTok
    args=[
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage",
        "--no-sandbox",
    ]
)

# FASTEST: yt-dlp for downloads (~2-3s per video)
cmd = ["yt-dlp", "--cookies-from-browser", "chrome", url]
result = subprocess.run(cmd, capture_output=True)
```

**Lesson:** TikTok uses aggressive bot detection. Headless browsers are blocked. Use headful mode for search, yt-dlp for downloads.

---

## Performance Optimization

### 1. Batch DOM Operations

```python
# SLOW: 30 separate calls
for item in page.locator(".item").all():
    title = item.locator(".title").text_content()
    price = item.locator(".price").text_content()

# FAST: 1 JavaScript call (10-30x faster)
data = page.evaluate("""
    () => [...document.querySelectorAll('.item')].map(el => ({
        title: el.querySelector('.title')?.textContent,
        price: el.querySelector('.price')?.textContent,
    }))
""")
```

### 2. Block Unnecessary Resources

```python
# Block images, fonts, CSS when only scraping text
async def route_handler(route):
    if route.request.resource_type in ["image", "font", "stylesheet"]:
        await route.abort()
    else:
        await route.continue_()

await page.route("**/*", route_handler)
```

### 3. Caching

```python
import hashlib
from pathlib import Path

def cached_fetch(url: str, cache_dir: Path = Path(".cache")) -> str:
    cache_dir.mkdir(exist_ok=True)
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_file = cache_dir / f"{cache_key}.json"

    if cache_file.exists():
        return cache_file.read_text()

    response = requests.get(url)
    cache_file.write_text(response.text)
    return response.text
```

### 4. Download Optimization

For yt-dlp:

```bash
# Optimized yt-dlp settings
yt-dlp \
  -N 8 \                    # 8 concurrent fragment downloads
  --buffer-size 64K \       # Larger buffer
  --http-chunk-size 10M \   # Reduce request overhead
  --no-mtime \              # Skip file time modification
  "$URL"
```

**Note:** aria2c is NOT faster for YouTube/DASH streams:
- YouTube uses separate video + audio streams
- Native yt-dlp handles merging better
- aria2c is only faster for direct HTTP downloads

---

## CLI Tools Integration

### yt-dlp (Video/Audio)

```bash
# Install
pip install yt-dlp
# or
brew install yt-dlp

# Search without downloading
yt-dlp "ytsearch10:python tutorial" --dump-json --flat-playlist

# Download with quality selection
yt-dlp -f "bestvideo[height<=720]+bestaudio" --merge-output-format mp4 "$URL"

# Audio only
yt-dlp -x --audio-format mp3 "$URL"

# With cookies (for age-restricted/private)
yt-dlp --cookies-from-browser chrome "$URL"
```

### duckduckgo-search (Images)

```bash
pip install duckduckgo-search
```

```python
from duckduckgo_search import DDGS

# Basic search
with DDGS() as ddgs:
    results = list(ddgs.images(
        keywords="nature wallpaper",
        max_results=100,
    ))

# With filters
with DDGS() as ddgs:
    results = list(ddgs.images(
        keywords="landscape",
        region="wt-wt",        # Worldwide
        safesearch="off",
        size="Large",          # Large, Medium, Small
        max_results=50,
    ))
```

### curl/wget (HTTP)

```bash
# Simple download
curl -O "$URL"

# With headers
curl -H "Authorization: Bearer $TOKEN" "$URL"

# Resume interrupted download
wget -c "$URL"

# Download with custom filename
curl -o filename.ext "$URL"
```

### aria2c (Parallel Downloads)

```bash
# Install
brew install aria2

# Multi-connection download (for direct HTTP, NOT for YouTube)
aria2c -x 16 -s 16 "$URL"

# Download from file list
aria2c -i urls.txt -j 5

# With custom output
aria2c -d /path/to/dir -o filename "$URL"
```

---

## Data Extraction Patterns

### HTML with BeautifulSoup

```python
import requests
from bs4 import BeautifulSoup

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract elements
titles = [el.text for el in soup.select('h2.title')]
links = [el['href'] for el in soup.select('a.link')]
```

### JSON APIs

```python
import requests

response = requests.get(api_url, headers={'Authorization': f'Bearer {token}'})
data = response.json()

# Handle pagination
all_results = []
while url:
    response = requests.get(url)
    data = response.json()
    all_results.extend(data['results'])
    url = data.get('next')
```

### Regex Extraction

```python
import re

# Extract URLs from HTML
urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', html)

# Extract JSON from script tags
json_match = re.search(r'var data = (\{.*?\});', html, re.DOTALL)
if json_match:
    data = json.loads(json_match.group(1))

# Extract image URLs from Google Images
image_urls = re.findall(r'\["(https?://[^"]+)",\s*\d+,\s*\d+\]', html)
```

---

## Decision Tree

```
Need to scrape data?
│
├─ Has official API? → Use API
│
├─ CLI tool exists?
│   ├─ YouTube/TikTok → yt-dlp
│   ├─ Images → duckduckgo-search
│   └─ Files → curl/wget/aria2c
│
├─ Static HTML?
│   └─ requests + BeautifulSoup
│
├─ Need JS rendering?
│   ├─ Simple page → Playwright headless
│   ├─ Anti-bot site → Playwright headful + stealth
│   └─ Complex SPA → Playwright + wait strategies
│
└─ Need interaction?
    └─ Playwright with persistent profile
```

---

## browser.py Scraping Commands

```bash
cd .claude/skills/browser-use/scripts

# Get page HTML (automation/headless)
uv run browser.py auto URL --account NAME

# Extract text
uv run browser.py text URL --selector "CSS_SELECTOR"

# Get all links
uv run browser.py links URL

# Extract attributes
uv run browser.py extract URL "img" --attr src --all

# Download images
uv run browser.py download-images URL "img.selector" -n 10 -o ./images

# Google Images search
uv run browser.py google-image "keyword" -n 50 -o ~/Downloads -s Large

# YouTube search
uv run browser.py youtube-search "keyword" -n 10

# YouTube download
uv run browser.py youtube-download URL -o ~/Downloads
```

---

## References

- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [duckduckgo-search](https://github.com/deedy5/duckduckgo_search)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [requests Documentation](https://docs.python-requests.org/)
- [aria2 Manual](https://aria2.github.io/manual/en/html/)
