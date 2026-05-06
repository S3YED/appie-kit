---
title: "Image Download Optimization: From 110s to 9s (12x Faster)"
author: Kudosx Team
date: 2025-12-05
tags: [duckduckgo, google-images, optimization, no-browser]
---

# Image Download Optimization

This document records the process of optimizing image downloads from various sources.

## Results Overview

| Method | 20 images | 100 images | Browser | Success Rate |
|--------|-----------|------------|---------|--------------|
| Click thumbnails (old) | 110s | N/A | Yes | ~100% |
| Google regex | 11s | 15s | Yes | ~98% |
| **DuckDuckGo (new)** | **9s** | **19s** | **No** | **~98%** |

**Improvement: 12x faster, no browser needed!**

---

## Part 1: DuckDuckGo Search (Recommended)

### Why DuckDuckGo?

- **No browser needed** - HTTP requests only
- **No API key required** - Completely free
- **Fast** - ~2-3s to find 100 URLs
- **Supports filters** - Size, color, type, license

### Installation

```bash
uv add duckduckgo-search
```

### Implementation

```python
from duckduckgo_search import DDGS

def search_duckduckgo_images(keyword: str, num: int = 100, size: str = None):
    """Search images using DuckDuckGo (no browser needed)."""
    with DDGS() as ddgs:
        results = list(ddgs.images(
            keywords=keyword,
            region="wt-wt",
            safesearch="off",
            size=size,  # Large, Medium, Small
            max_results=num,
        ))

    return [{"url": r["image"], "title": r["title"]} for r in results]
```

### CLI Usage

```bash
# DuckDuckGo only - NO BROWSER NEEDED
uv run browser.py google-image "landscape wallpaper" -n 100 -o ~/Downloads -S duckduckgo

# With size filter
uv run browser.py google-image "nature" -n 50 -o ~/Downloads -S duckduckgo -s Large

# 4K images (3840px+ minimum)
uv run browser.py google-image "wallpaper" -n 20 -o ~/Downloads -s 4k

# FullHD images (1920px+ minimum)
uv run browser.py google-image "wallpaper" -n 50 -o ~/Downloads -s fullhd

# With time range filter (DuckDuckGo supports Day, Week, Month, Year)
uv run browser.py google-image "news" -n 50 -o ~/Downloads -S duckduckgo -t Day
```

### Size Filter Options

| Option | Minimum Dimension | Description |
|--------|-------------------|-------------|
| `4k` | 3840px | 4K resolution (3840x2160) |
| `fullhd` | 1920px | Full HD resolution (1920x1080) |
| `Large` | 1000px | Large images |
| `Medium` | 400px | Medium images |
| `Icon` | 0px | No minimum |

### Experimental Benchmark

**100 images (Large size):**
```
23:51:50 - Using DuckDuckGo (no browser)
23:51:50 - Trying DuckDuckGo search (no browser)...
23:51:53 - DuckDuckGo found 100 images
23:51:53 - Downloading 100 images with 10 workers...
23:52:09 - Downloaded 98/100 images (98%) to test_downloads

Total: 19 seconds for 100 images (no browser needed)
```

**50 images (FullHD size - 1920px+):**
```
00:26:10 - Using DuckDuckGo (no browser)
00:26:10 - Trying DuckDuckGo search (no browser)...
00:26:14 - DuckDuckGo found 50 images meeting size criteria (filtered 28 smaller)
00:26:14 - Downloading 50 images with 10 workers...
00:27:04 - Downloaded 43/50 images (86%) to downloads

Total: ~54 seconds (fast search, slower download due to larger images)
```

**Note:** 4K and FullHD filters check actual dimensions from metadata, so the number of images found may be less than requested.

---

## Part 2: Google Images with Regex (Fallback)

### When to use Google?

- DuckDuckGo doesn't return enough results
- Need results specifically from Google
- Already have a logged-in account

### Key Insight

Google Images stores URLs in `AF_initDataCallback`:

```javascript
["https://example.com/full-size-image.jpg", 1920, 1080]
```

### Regex Extraction

```python
def extract_image_urls_from_source(html: str, limit: int) -> list[str]:
    """Extract full-size image URLs from Google Images page source."""
    urls = []
    seen = set()

    pattern = r'\["(https?://[^"]+)",\s*\d+,\s*\d+\]'

    for match in re.finditer(pattern, html):
        url = match.group(1)

        # Skip thumbnails
        if "encrypted-tbn0.gstatic.com" in url:
            continue

        # Decode unicode escapes
        url = bytes(url, 'ascii').decode('unicode-escape')

        if url not in seen:
            seen.add(url)
            urls.append(url)
            if len(urls) >= limit:
                break

    return urls
```

### CLI Usage

```bash
# Google mode (requires account)
uv run browser.py google-image "keyword" -a account_name -n 50 -o ~/Downloads -S google

# Google with time range filter
uv run browser.py google-image "news" -a account_name -n 50 -o ~/Downloads -S google -t Week

# Google with custom date range (YYYYMMDD format) - Google only
uv run browser.py google-image "event photos" -a account_name -n 50 -o ~/Downloads -S google -df 20240601 -dt 20240630
```

**Note:** Custom date range (`-df`, `-dt`) only works with Google mode because DuckDuckGo doesn't support custom date ranges.

---

## Part 3: Tiered Fallback Strategy

### Architecture

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Tier 1: DuckDuckGo (~2-3s)         │  ← No browser, fastest
│  - duckduckgo-search library        │
│  - HTTP requests only               │
└────────┬────────────────────────────┘
         │ if insufficient
         ▼
┌─────────────────────────────────────┐
│  Tier 2: Google Regex (~8s)         │  ← Browser, fast
│  - Playwright + regex extraction    │
│  - No clicking thumbnails           │
└────────┬────────────────────────────┘
         │ if insufficient
         ▼
┌─────────────────────────────────────┐
│  Tier 3: Google Scroll (~15s)       │  ← Browser, most results
│  - Scroll to load more              │
│  - Multiple extractions             │
└─────────────────────────────────────┘
```

### Implementation

```python
def _download_images(self, page: Page | None) -> list[str]:
    # Tier 1: DuckDuckGo (fastest, no browser)
    results = search_duckduckgo_images(keyword, num, size)
    if len(results) >= num:
        return download_parallel(results)

    # Tier 2: Google regex (if browser available)
    if page:
        html = page.content()
        google_urls = extract_image_urls_from_source(html, num * 2)
        results.extend(google_urls)

    # Tier 3: Scroll for more
    if len(results) < num and page:
        # Scroll and extract more...
        pass

    return download_parallel(results[:num])
```

---

## Part 4: Parallel Downloads

### Optimizing downloads with ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_parallel(urls: list[str], output_dir: Path, workers: int = 10):
    downloaded = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(download_single, (i, url, output_dir)): i
            for i, url in enumerate(urls)
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                downloaded.append(result)

    return downloaded
```

### Benchmark

| Workers | 100 images | Notes |
|---------|------------|-------|
| 1 | ~60s | Sequential |
| 5 | ~25s | |
| 10 | ~16s | Sweet spot |
| 20 | ~15s | Diminishing returns |

---

## Part 5: Comparison with YouTube Pattern

| Aspect | YouTube | Images |
|--------|---------|--------|
| No-browser method | yt-dlp ytsearch | DuckDuckGo search |
| Speed | ~1.5s search | ~2-3s search |
| Browser fallback | Playwright | Google + Playwright |
| Parallel | 3 workers (rate limit) | 10 workers |

---

## CLI Commands Reference

```bash
# DuckDuckGo - fastest, no browser needed
uv run browser.py google-image "keyword" -n 100 -o ~/Downloads -S duckduckgo

# Auto mode - tries DuckDuckGo first
uv run browser.py google-image "keyword" -n 100 -o ~/Downloads

# Google mode - requires account
uv run browser.py google-image "keyword" -a account_name -n 50 -o ~/Downloads -S google

# With size filter
uv run browser.py google-image "keyword" -n 100 -o ~/Downloads -S duckduckgo -s Large

# 4K images (3840px+ minimum)
uv run browser.py google-image "wallpaper" -n 20 -o ~/Downloads -s 4k

# FullHD images (1920px+ minimum)
uv run browser.py google-image "wallpaper" -n 50 -o ~/Downloads -s fullhd

# DuckDuckGo with time range (Day, Week, Month, Year)
uv run browser.py google-image "news" -n 50 -o ~/Downloads -S duckduckgo -t Day

# Google with custom date range (YYYYMMDD) - requires account
uv run browser.py google-image "event" -a myaccount -n 50 -o ~/Downloads -S google -df 20240601 -dt 20240630
```

---

## Best Practices

### Search
1. **Prefer DuckDuckGo** - No browser needed, fastest
2. **Fallback to Google** when more results or custom date range needed
3. **Use size filter** to get high-quality images
4. **Time range filter** (-t) supported by both DuckDuckGo and Google
5. **Custom date range** (-df, -dt) only supported by Google

### Download
1. **10 workers** is the sweet spot for parallel downloads
2. **15s timeout** per image to avoid getting stuck
3. **Skip duplicates** using URL set

### Error Handling
1. **Retry failed downloads** (optional)
2. **Log success rate** for monitoring
3. **Graceful fallback** between tiers

---

## References

- [duckduckgo-search PyPI](https://pypi.org/project/duckduckgo-search/)
- [ScrapingAnt - How to Scrape Google Images](https://scrapingant.com/blog/how-to-scrape-google-images)
- [Guide To Google Image Search API - ScrapFly](https://scrapfly.io/blog/posts/guide-to-google-image-search-api-and-alternatives)
