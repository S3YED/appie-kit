---
title: "YouTube Search & Download Optimization"
author: Kudosx Team
date: 2025-12-05
tags: [youtube, yt-dlp, optimization, performance, automation]
---

# YouTube Search & Download Optimization

This document records lessons learned from optimizing YouTube search and download operations, based on real-world experiments.

## Results Overview

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Search time | 6-10s | 1.5s | **4-5x** |
| Download (12 min video) | 12s | 8.5s | **30%** |
| Search + 5 downloads | 60s+ | 22s | **3x** |

---

## Part 1: Search Optimization

### Initial Problem

Using Playwright to search YouTube took 6-10 seconds:

```
22:38:41 - Searching YouTube: 'lofi music'
22:38:47 - Found 20 video elements          # 6 seconds just to search
```

**Root Causes:**
- Browser startup (~2s)
- YouTube page load (~2-3s)
- JavaScript render wait (~1-2s)
- DOM parsing (~0.5s)

### Solution: 3-Tier Fallback

```python
def search_youtube(keyword, num=10):
    # Tier 1: yt-dlp CLI (~1.5s) - Fastest
    results = _search_ytdlp_fast(keyword, num)
    if results:
        return results

    # Tier 2: youtube-search-python (~2-3s)
    results = _search_library(keyword, num)
    if results:
        return results

    # Tier 3: Playwright browser (~6-10s) - Fallback
    return _search_browser(keyword, num)
```

### Tier 1: yt-dlp ytsearch (Recommended)

**Why it's fast:**
- No browser needed
- `--flat-playlist` skips full extraction
- Returns JSON directly

```python
def _search_ytdlp_fast(keyword, num=10, min_duration=None, max_duration=None, date_from=None, date_to=None):
    # Need more results when filtering
    has_filters = min_duration or max_duration or date_from or date_to
    fetch_num = num * 5 if has_filters else num

    cmd = [
        "yt-dlp",
        f"ytsearch{fetch_num}:{keyword}",
        "--dump-json",
        "--skip-download",  # Full extraction needed for date
        "--quiet",
        "--no-warnings",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    # Parse JSON lines
    videos = []
    for line in result.stdout.strip().split("\n"):
        v = json.loads(line)
        # Filter by duration if needed
        duration_sec = v.get("duration")
        if duration_sec and min_duration and duration_sec/60 < min_duration:
            continue
        if duration_sec and max_duration and duration_sec/60 > max_duration:
            continue

        # Filter by date (upload_date is YYYYMMDD string)
        upload_date = v.get("upload_date", "")
        if date_from and upload_date < date_from:
            continue
        if date_to and upload_date > date_to:
            continue

        videos.append({
            "url": f"https://www.youtube.com/watch?v={v['id']}",
            "title": v.get("title", ""),
            "duration": format_duration(duration_sec),
            "date": format_date(upload_date),  # YYYY-MM-DD format
        })
        if len(videos) >= num:
            break
    return videos
```

**Experimental Results:**

```
23:27:39 - Starting search for: 'claude code'
23:27:40 - yt-dlp fast search found 5 videos    # 1 second!
```

### Search Benchmark

| Method | Time | Browser | Reliability |
|--------|------|---------|-------------|
| yt-dlp + flat-playlist | 1.5s | No | High |
| youtube-search-python | 2-3s | No | Medium |
| Playwright | 6-10s | Yes | Highest |

---

## Part 2: Download Optimization

### Problem: aria2c is NOT faster for YouTube

**Experiment:**

```
# Test 1: Native yt-dlp
23:32:33 - Downloading...
23:32:41 - Downloaded              # 8 seconds

# Test 2: aria2c
23:31:49 - Downloading...
23:32:18 - Downloaded              # 29 seconds (!)
```

**Why aria2c is slower:**
- YouTube uses DASH streams (separate video + audio)
- aria2c downloads separately, then merges
- Native yt-dlp handles DASH better

**Conclusion:** Use native yt-dlp with `-N` concurrent fragments.

### Optimal Configuration

```python
cmd = [
    "yt-dlp",
    "-f", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best",
    "-N", "8",                  # 8 concurrent fragments
    "--buffer-size", "64K",    # Larger buffer
    "--http-chunk-size", "10M", # Larger chunks
    "--no-mtime",              # Skip modification time
    "--no-check-certificates", # Skip SSL verify
    "-o", "%(title)s.%(ext)s",
    url
]
```

### Download Benchmark

**Short video (2 minutes):**
```
23:31:10 - Downloading Python_in_100_Seconds
23:31:18 - Downloaded              # 8 seconds
```

**Long video (12 minutes):**
```
23:33:21 - Downloading How_I_use_Claude_Code
23:33:29 - Downloaded              # 8 seconds
```

**Concurrent fragments comparison:**

| -N value | 2 min video | 12 min video |
|----------|-------------|--------------|
| 4 (default) | 8s | 12s |
| 8 | 7.5s | 8.5s |
| 16 | 7.4s | 8.5s |

**Conclusion:** `-N 8` is the sweet spot, increasing further doesn't significantly improve performance.

---

## Part 3: Parallel Downloads

### Initial Problem

Sequential downloads:
```
22:50:04 - Downloading video 1...
22:50:13 - Downloaded
22:50:13 - Downloading video 2...
22:50:23 - Downloaded
# 5 videos = 57 seconds
```

### Solution: ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_parallel(urls, max_workers=3):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_single, url): url for url in urls}
        for future in as_completed(futures):
            result = future.result()
```

**Results:**
```
23:08:48 - Downloading 5 video(s) with 3 parallel workers...
23:08:48 - Downloading: video1, video2, video3 (simultaneously)
23:08:57 - Downloaded: video1
23:09:00 - Downloaded: video2, video3
23:09:06 - Downloaded: video4
23:09:10 - Downloaded: video5
23:09:10 - Downloaded 5 file(s)     # 22 seconds (instead of 57 seconds)
```

**Why max_workers=3:**
- Too many workers → Rate limiting
- 3 workers balances speed and stability

---

## Part 4: Duration & Date Filters

### Method 1: URL Parameter (Fast but limited)

```python
# YouTube duration filters
# Short (< 4 min): sp=EgIYAQ%3D%3D
# Medium (4-20 min): sp=EgIYAw%3D%3D
# Long (> 20 min): sp=EgIYAg%3D%3D

search_url = f"https://youtube.com/results?search_query={keyword}"
if min_duration >= 4 and max_duration <= 20:
    search_url += "&sp=EgIYAw%3D%3D"
```

**Limitation:** Only 3 presets, not flexible.

### Method 2: Filter in code (Flexible)

```python
def filter_by_duration(videos, min_dur, max_dur):
    filtered = []
    for v in videos:
        duration_min = parse_duration(v["duration"])
        if min_dur and duration_min < min_dur:
            continue
        if max_dur and duration_min > max_dur:
            continue
        filtered.append(v)
    return filtered
```

**Experiment:**
```
23:08:48 - [1/5] 19.0 min: lofi songs for slow days
23:08:48 - [2/5] 18.6 min: ALBUM CHILL WITH VICKY NHUNG
23:08:48 - [3/5] 14.6 min: If Wiz Khalifa ft Post Malone...
```

### Method 3: Date Filtering (Custom date range)

```python
# YouTube upload date preset filters (URL parameter)
UPLOAD_DATE_PARAMS = {
    "hour": "EgIIAQ%3D%3D",
    "today": "EgIIAg%3D%3D",
    "week": "EgIIAw%3D%3D",
    "month": "EgIIBA%3D%3D",
    "year": "EgIIBQ%3D%3D",
}

# Custom date range - filter in Python
def filter_by_date(videos, date_from, date_to):
    """Filter videos by upload date (YYYYMMDD format)."""
    filtered = []
    for v in videos:
        upload_date = v.get("upload_date", "")
        if date_from and upload_date < date_from:
            continue
        if date_to and upload_date > date_to:
            continue
        filtered.append(v)
    return filtered
```

**CLI Usage:**
```bash
# Preset upload date filters
uv run browser.py youtube-search "news" -n 10 -t week
uv run browser.py youtube-search "news" -n 10 -t today

# Custom date range (YYYYMMDD format)
uv run browser.py youtube-search "tutorial" -n 10 -df 20240101 -dt 20241231
uv run browser.py youtube-download "music" --search -n 5 -df 20240601 -dt 20240630 -o ./videos
```

**Note:** Custom date range requires full extraction (no `--flat-playlist`), so it's slower than preset filters (~10s vs ~1.5s).

---

## Part 5: Common Errors

### Error 1: Duration filter with string

```
23:27:47 - WARNING - yt-dlp search failed: '<' not supported between instances of 'float' and 'str'
```

**Cause:** CLI passes duration as string, not converted.

**Fix:**
```python
min_dur = int(min_duration) if min_duration else None
max_dur = int(max_duration) if max_duration else None
```

### Error 2: Timeout clicking filter button

```
22:55:18 - WARNING - Could not apply duration filter: Locator.click: Timeout 2000ms exceeded.
```

**Cause:** YouTube UI changed.

**Fix:** Use URL parameter instead of clicking UI.

### Error 3: youtube-search-python proxies error

```
23:27:47 - WARNING - Fast search failed: post() got an unexpected keyword argument 'proxies'
```

**Cause:** Library version conflict.

**Fix:** Fallback to next tier.

---

## CLI Commands

```bash
# Fast search (using yt-dlp)
uv run browser.py youtube-search "keyword" -n 10

# Search with duration filter
uv run browser.py youtube-search "keyword" -n 5 -min 4 -max 20

# Search with upload date filter
uv run browser.py youtube-search "news" -n 10 -t week
uv run browser.py youtube-search "news" -n 10 -t today

# Search with custom date range (YYYYMMDD)
uv run browser.py youtube-search "tutorial" -n 10 -df 20240101 -dt 20241231

# Direct download
uv run browser.py youtube-download "URL" -o ~/Downloads -q 720p

# Search + download
uv run browser.py youtube-download "keyword" --search -n 5 -o ~/Downloads

# Full options
uv run browser.py youtube-download "lofi music" \
    --search \
    -n 5 \
    -min 4 -max 20 \
    -o ~/Downloads \
    -q 720p \
    -N 8
```

---

## Best Practices Summary

### Search
1. **Prefer yt-dlp ytsearch** with `--flat-playlist` (except when date filter is needed)
2. **Fallback strategy** to ensure reliability
3. **Fetch more than needed** when duration/date filter is used (5x)
4. **Date filter needs full extraction** - slower but accurate

### Download
1. **DON'T use aria2c** for YouTube DASH streams
2. **Use `-N 8`** concurrent fragments
3. **Parallel downloads** with 3 workers
4. **Buffer 64K, chunk 10M** to optimize throughput

### Error Handling
1. **Convert types** from CLI (string → int)
2. **Fallback** when fast method fails
3. **Reasonable timeouts** (30s search, 600s download)

---

## References

- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [yt-dlp Speed Methods](https://github.com/yt-dlp/yt-dlp/issues/7987)
- [yt-dlp Format Selection](https://github.com/yt-dlp/yt-dlp#format-selection)
