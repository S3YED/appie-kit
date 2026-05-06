---
title: "Authentication & Session Management"
author: Kudosx Team
date: 2025-12-07
tags: [authentication, sessions, persistent-context, playwright, cookies]
---

# Authentication & Session Management

## Overview

Browser automation often requires maintaining login sessions across multiple runs. This guide covers best practices for saving, managing, and reusing authentication sessions.

---

## Storage Location

Authentication data is stored in the user's home directory:

```
~/.auth/
├── account-name.json          # Storage state (cookies, localStorage)
└── profiles/
    └── account-name/          # Persistent browser profile
```

**Why `~/.auth`?**
- Shared across all projects
- Not committed to git
- Survives project deletion
- Easy to backup

---

## Creating Login Sessions

### Basic Usage

```bash
# Create a new login session
uv run browser.py create-login "https://example.com/login" --account my-account

# With custom timeout (default: 120s)
uv run browser.py create-login "https://google.com" --account google --wait 300

# Using specific browser channel
uv run browser.py create-login "https://example.com" --account my-account --channel chrome
```

### How It Works

1. **Opens browser** with persistent profile at `~/.auth/profiles/account-name/`
2. **User logs in** manually (handles CAPTCHA, 2FA, OAuth)
3. **Detects browser close** or waits for timeout
4. **Saves session** to `~/.auth/account-name.json`

### Browser Close Detection

The script uses `page.evaluate("1")` to detect when browser is closed:

```python
while elapsed < wait_seconds:
    try:
        if page.is_closed():
            break
        # Verify browser is still responsive
        page.evaluate("1")
    except Exception:
        # Browser closed by user
        break
    time.sleep(1)
```

**Benefits:**
- Exits immediately when user closes browser
- No need to wait for timeout
- Session is saved automatically

---

## Using Saved Sessions

### With browser.py Commands

```bash
# === MANUAL BROWSING (opens browser for user interaction) ===
uv run browser.py open "https://example.com/dashboard" --account my-account
uv run browser.py open "https://example.com" --account my-account --wait 120

# === AUTOMATION (headless, returns content) ===
uv run browser.py auto "https://example.com/dashboard" --account my-account

# Take screenshot with authentication
uv run browser.py screenshot "https://example.com/profile" --account my-account -o profile.png

# Fill form with saved session
uv run browser.py fill "https://example.com/search" "input[name=q]" "query" --account my-account
```

### In Python Code

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

AUTH_DIR = Path.home() / ".auth"

def get_authenticated_context(playwright, account: str, headless: bool = True):
    """Create browser context with saved profile."""
    user_data_dir = AUTH_DIR / "profiles" / account

    if not user_data_dir.exists():
        raise FileNotFoundError(f"Account '{account}' not found")

    return playwright.chromium.launch_persistent_context(
        str(user_data_dir),
        headless=headless,
        channel="chrome",
        args=["--disable-blink-features=AutomationControlled"],
        ignore_default_args=["--enable-automation"],
    )

# Usage
with sync_playwright() as p:
    context = get_authenticated_context(p, "google")
    page = context.pages[0]
    page.goto("https://mail.google.com")
    # Already logged in!
```

---

## Managing Accounts

### List Saved Accounts

```bash
uv run browser.py accounts
```

Output:
```
Saved accounts:
  - google
  - github
  - twitter
```

### Delete Account

```bash
# Remove both JSON and profile directory
rm ~/.auth/account-name.json
rm -rf ~/.auth/profiles/account-name/
```

---

## Persistent Context vs Storage State

### Two Types of Session Data

| Type | Location | Contains | Use Case |
|------|----------|----------|----------|
| Storage State | `~/.auth/account.json` | Cookies, localStorage | Quick restore |
| Persistent Profile | `~/.auth/profiles/account/` | Full browser profile | Complex sessions |

### Why Both?

1. **Persistent Profile** (primary):
   - Auto-saved as user browses
   - Contains everything: cookies, cache, extensions
   - Works with sites that check browser fingerprint

2. **Storage State JSON** (backup):
   - Explicit snapshot of cookies/localStorage
   - Can be loaded into any context
   - Useful for `list_accounts()` enumeration

---

## Best Practices

### 1. Use Descriptive Account Names

```bash
# Good
uv run browser.py create-login "https://google.com" --account google-workspace-main
uv run browser.py create-login "https://google.com" --account google-personal

# Bad
uv run browser.py create-login "https://google.com" --account acc1
```

### 2. Separate Accounts by Purpose

```
~/.auth/profiles/
├── google-workspace/      # Work Google account
├── google-personal/       # Personal Gmail
├── github-work/           # Work GitHub
├── github-personal/       # Personal GitHub
└── twitter-bot/           # Bot account
```

### 3. Handle Session Expiry

Sessions can expire. Check and re-authenticate when needed:

```python
def ensure_logged_in(page, account: str) -> bool:
    """Check if still logged in, return False if session expired."""
    page.goto("https://example.com/dashboard")

    # Check for login redirect
    if "login" in page.url:
        logger.warning(f"Session expired for {account}")
        return False

    return True
```

### 4. Use Stealth Flags for Sensitive Sites

```python
context = playwright.chromium.launch_persistent_context(
    str(user_data_dir),
    headless=False,  # Some sites block headless
    channel="chrome",
    args=[
        "--disable-blink-features=AutomationControlled",
        "--disable-infobars",
        "--start-maximized",
    ],
    ignore_default_args=["--enable-automation"],
)
```

---

## Troubleshooting

### Session Not Saving

**Problem:** Account not appearing in `accounts` list after closing browser.

**Solution:** Ensure you're closing the browser window, not interrupting the command (Ctrl+C).

### Login Not Persisting

**Problem:** Need to re-login every time.

**Solution:** Use persistent context, not storage state:

```python
# Wrong - storage state can be incomplete
context = browser.new_context(storage_state="~/.auth/account.json")

# Right - full profile persistence
context = playwright.chromium.launch_persistent_context(
    "~/.auth/profiles/account",
    ...
)
```

### Site Detects Automation

**Problem:** Site shows CAPTCHA or blocks access.

**Solutions:**
1. Use `headless=False` for login
2. Add stealth flags
3. Use real Chrome channel: `channel="chrome"`
4. Clear automation indicators

---

## Quick Reference

```bash
# Create session (opens browser, close when done)
uv run browser.py create-login URL --account NAME [--wait SECONDS]

# List all saved sessions
uv run browser.py accounts

# Manual browsing (opens browser for user interaction)
uv run browser.py open URL --account NAME [--wait SECONDS]

# Automation (headless, returns content)
uv run browser.py auto URL --account NAME
uv run browser.py screenshot URL --account NAME -o file.png
uv run browser.py click URL SELECTOR --account NAME
uv run browser.py fill URL SELECTOR VALUE --account NAME
```

## Command Summary

| Command | Mode | Description |
|---------|------|-------------|
| `create-login` | Manual | Create new login session, close browser when done |
| `open` | Manual | Open browser for user interaction |
| `auto` | Headless | Navigate and return HTML content |
| `screenshot` | Headless | Take screenshot |
| `click`, `fill` | Headless | Interact with page elements |
