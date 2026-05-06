---
title: "Browser Automation: Patterns & Best Practices"
author: Kudosx Team
date: 2025-12-07
tags: [automation, playwright, reliability, anti-detection, best-practices]
---

# Browser Automation: Patterns & Best Practices

## Overview

This guide covers browser automation patterns using Playwright - when to use browsers, architecture patterns, reliability, and anti-detection techniques.

For web scraping and data extraction, see [web-scraping.md](./web-scraping.md).

---

## When to Use Browser Automation

### Browser Required

| Scenario | Why Browser Needed |
|----------|-------------------|
| OAuth login flows | Complex redirects, popups |
| CAPTCHA handling | Need visual interaction |
| Heavy JS frameworks | React/Vue SPAs need rendering |
| WebSocket connections | Real-time data |
| Cookie consent dialogs | DOM interaction required |
| Anti-bot protected sites | TikTok, Instagram |

### Browser NOT Needed

| Scenario | Better Alternative |
|----------|-------------------|
| YouTube search/download | `yt-dlp` CLI |
| Image search | `duckduckgo-search` library |
| Static HTML | `requests` + `BeautifulSoup` |
| JSON APIs | `requests` directly |
| File downloads | `curl`, `wget`, `aria2c` |

---

## Architecture Patterns

### 1. Tiered Fallback Strategy

Never rely on a single method. Build systems that degrade gracefully:

```python
def search_youtube(keyword: str, num: int = 10) -> list[dict]:
    """3-tier fallback: CLI → Library → Browser"""

    # Tier 1: yt-dlp CLI (fastest, most reliable)
    results = _search_via_ytdlp(keyword, num)
    if results:
        return results

    # Tier 2: Python library (fast, no browser)
    results = _search_via_library(keyword, num)
    if results:
        return results

    # Tier 3: Browser automation (slowest, handles edge cases)
    logger.info("Fast methods failed, using browser fallback")
    return _search_via_browser(keyword, num)
```

**Benefits:**
- 95% of requests use the fast path
- Handles API changes gracefully
- No single point of failure
- Easy to add new tiers

### 2. Parallel Execution

Use the right parallelism for each task:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

# For I/O-bound tasks (downloads, HTTP requests)
def download_parallel(urls: list[str], max_workers: int = 3) -> list[str]:
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_single, url): url for url in urls}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    return results
```

**Worker Guidelines:**
| Task | Workers | Reason |
|------|---------|--------|
| Video downloads | 3 | Avoid rate limiting |
| API calls | 5-10 | Balance speed/limits |
| Image downloads | 10-20 | Lightweight requests |

### 3. Browser Automation Pattern

Standard pattern for Playwright automation:

```python
from playwright.sync_api import sync_playwright

def browser_automation(headless: bool = True):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ]
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
        )
        page = context.new_page()

        try:
            # Your automation code here
            page.goto("https://example.com")
            # ...
        finally:
            context.close()
            browser.close()
```

### 4. Persistent Profile Pattern

For sites requiring login/session persistence:

```python
from pathlib import Path

AUTH_DIR = Path.home() / ".auth"

def with_persistent_profile(account: str, headless: bool = True):
    user_data_dir = AUTH_DIR / "profiles" / account

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            str(user_data_dir),
            headless=headless,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
        )
        page = context.pages[0] if context.pages else context.new_page()

        try:
            yield page
        finally:
            context.close()
```

---

## Reliability Patterns

### 1. Retry with Exponential Backoff

```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay:.1f}s")
            time.sleep(delay)
```

### 2. Safe Element Extraction

```python
def safe_extract(extractor_func, default=None):
    """Wrap extraction in try/except, return default on failure."""
    try:
        result = extractor_func()
        return result if result else default
    except Exception:
        return default

# Usage
title = safe_extract(lambda: page.locator("h1").text_content(), default="Unknown")
price = safe_extract(lambda: page.locator(".price").text_content(), default="N/A")
```

### 3. Wait for Dynamic Content

```python
# Wait for specific element
page.wait_for_selector(".content-loaded", timeout=10000)

# Wait for network idle
page.wait_for_load_state("networkidle")

# Custom wait condition
page.wait_for_function("() => window.dataLoaded === true")
```

### 4. Handle Common Obstacles

```python
def handle_cookie_consent(page):
    """Handle GDPR cookie dialogs."""
    selectors = [
        "button:has-text('Accept all')",
        "button:has-text('Accept')",
        "[data-testid='cookie-accept']",
        "#onetrust-accept-btn-handler",
    ]
    for selector in selectors:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=2000):
                btn.click()
                time.sleep(0.5)
                return True
        except:
            continue
    return False


def handle_popup(page):
    """Close common popups."""
    close_selectors = [
        "[aria-label='Close']",
        "button.close",
        ".modal-close",
    ]
    for selector in close_selectors:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=1000):
                btn.click()
                return True
        except:
            continue
    return False
```

---

## Anti-Detection Techniques

### 1. Stealth Browser Launch

```python
context = p.chromium.launch_persistent_context(
    user_data_dir,
    headless=False,  # Some sites block headless
    channel="chrome",  # Use real Chrome
    args=[
        "--disable-blink-features=AutomationControlled",
        "--disable-infobars",
        "--disable-dev-shm-usage",
        "--no-sandbox",
        "--start-maximized",
    ],
    ignore_default_args=["--enable-automation"],
)
```

### 2. Rotate User Agents

```python
import random

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

context = browser.new_context(
    user_agent=random.choice(USER_AGENTS)
)
```

### 3. Human-like Delays

```python
import random
import time

def human_delay(min_sec=0.5, max_sec=2.0):
    """Random delay to mimic human behavior."""
    time.sleep(random.uniform(min_sec, max_sec))

def human_type(page, selector, text):
    """Type with human-like delays between keystrokes."""
    element = page.locator(selector)
    for char in text:
        element.type(char, delay=random.randint(50, 150))
```

### 4. Platform-Specific Requirements

| Platform | Headless OK? | Key Requirement |
|----------|--------------|-----------------|
| YouTube | Yes | Use yt-dlp instead |
| Google | Yes | Rotate user agents |
| TikTok | **NO** | Headful + stealth flags |
| Instagram | **NO** | Login + anti-detection |
| Twitter/X | Partial | API preferred |
| LinkedIn | **NO** | Login + rate limiting |

---

## Best Practices Checklist

### Before Starting
- [ ] Check if API exists (fastest option)
- [ ] Check if CLI tool exists (yt-dlp, curl)
- [ ] Determine if browser is actually needed

### Implementation
- [ ] Use persistent profiles for login-required sites
- [ ] Implement tiered fallback strategy
- [ ] Add retry logic with exponential backoff
- [ ] Handle common obstacles (cookies, popups)
- [ ] Use appropriate timeouts

### Anti-Detection
- [ ] Use stealth flags for sensitive sites
- [ ] Add human-like delays
- [ ] Rotate user agents if needed
- [ ] Check platform-specific requirements

### Reliability
- [ ] Log actions for debugging
- [ ] Handle errors gracefully
- [ ] Clean up resources (close browsers)
- [ ] Respect rate limits

---

## Quick Reference

### browser.py Commands

```bash
cd .claude/skills/browser-use/scripts

# Manual browsing
uv run browser.py open URL --account NAME --wait 60

# Create login session
uv run browser.py create-login URL --account NAME

# Automation (headless)
uv run browser.py auto URL --account NAME

# Other automation commands
uv run browser.py screenshot URL -o file.png
uv run browser.py click URL "selector"
uv run browser.py fill URL "selector" "value"
```

### Common Selectors

```python
# By ID
page.locator("#element-id")

# By class
page.locator(".class-name")

# By text
page.locator("text=Button Text")
page.locator("button:has-text('Submit')")

# By role
page.locator("role=button[name='Submit']")

# By CSS
page.locator("div.container > p.content")

# By XPath
page.locator("xpath=//div[@class='item']")
```

---

## References

- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright Selectors](https://playwright.dev/docs/selectors)
- [Anti-Bot Detection Techniques](https://blog.castle.io/what-tiktoks-virtual-machine-tells-us-about-modern-bot-defenses/)
