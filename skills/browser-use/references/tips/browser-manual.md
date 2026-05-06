---
title: "Manual Browser Sessions: Recording & Logging"
author: Kudosx Team
date: 2025-12-07
tags: [browser, manual, recording, logging, debugging, playwright]
---

# Manual Browser Sessions: Recording & Logging

## Overview

When working with browser automation, sometimes you need to open a browser manually to:
- Debug hard-to-reproduce issues
- Record the entire interaction process
- Capture webpage content in real-time
- Analyze website behavior

---

## Manual Commands

### 1. `open` - Browse Manually

Open browser for user interaction. Browser stays open until user closes it or timeout.

```bash
cd .claude/skills/browser-use/scripts

# Open browser (temporary session)
uv run browser.py open "https://example.com"

# Open with saved account
uv run browser.py open "https://example.com" --account my-account

# Custom timeout (default: 60s)
uv run browser.py open "https://example.com" --account my-account --wait 300
```

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| `--account, -a` | Use saved session |
| `--wait, -w` | Timeout in seconds (default: 60) |
| `--channel, -c` | Browser: chrome, msedge, chromium |

**Behavior:**
- Opens browser in **headed mode** (visible window)
- Waits for user to **close the browser** or timeout
- Detects browser close immediately using `page.evaluate("1")`
- Session changes are preserved (if using `--account`)

### 2. `create-login` - Create New Session

Open browser to login manually and save the session for reuse.

```bash
# Create new login session
uv run browser.py create-login "https://google.com" --account google-main

# Extended timeout for complex login (2FA, CAPTCHA)
uv run browser.py create-login "https://google.com" --account google-main --wait 300
```

**Workflow:**
1. Browser opens at specified URL
2. User logs in manually (handles CAPTCHA, 2FA, OAuth)
3. User **closes browser** when finished
4. Session saved to `~/.auth/`
5. Account appears in `uv run browser.py accounts`

**Parameters:**
| Parameter | Description |
|-----------|-------------|
| `--account, -a` | Account name to save (required) |
| `--wait, -w` | Timeout in seconds (default: 120) |
| `--channel, -c` | Browser: chrome, msedge, chromium |

---

## Recording Manual Sessions

### Playwright Trace

Record entire session with screenshots, DOM snapshots, and network activity:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

AUTH_DIR = Path.home() / ".auth"

with sync_playwright() as p:
    # Setup with account
    account = "my-account"
    user_data_dir = AUTH_DIR / "profiles" / account

    context = p.chromium.launch_persistent_context(
        str(user_data_dir),
        headless=False,
        channel="chrome",
        args=["--disable-blink-features=AutomationControlled"],
    )

    # Start tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://example.com")

    print("Browse manually. Close browser when done...")

    # Wait for user to close browser
    while True:
        try:
            if page.is_closed():
                break
            page.evaluate("1")
            time.sleep(1)
        except Exception:
            break

    # Save trace
    context.tracing.stop(path="trace.zip")
    print("Trace saved to trace.zip")
```

**View trace:**
```bash
npx playwright show-trace trace.zip
```

### Video Recording

Record screen as video during manual session:

```python
context = browser.new_context(
    record_video_dir="./videos/",
    record_video_size={"width": 1920, "height": 1080}
)
page = context.new_page()
page.goto("https://example.com")

# ... user browses manually ...

context.close()  # Video saved when context closes
```

---

## Logging During Manual Sessions

### Network Activity

Log all HTTP requests and responses:

```python
def on_request(request):
    print(f">> {request.method} {request.url}")

def on_response(response):
    print(f"<< {response.status} {response.url}")

page.on("request", on_request)
page.on("response", on_response)
```

### Console Messages

Capture browser console output:

```python
def on_console(msg):
    print(f"[console.{msg.type}] {msg.text}")

page.on("console", on_console)
```

### Page Errors

Capture JavaScript errors:

```python
def on_error(error):
    print(f"[ERROR] {error}")

page.on("pageerror", on_error)
```

---

## Complete Recording Script

Full script to record manual browsing session with all logs and artifacts:

```python
#!/usr/bin/env python3
"""Record complete manual browser session."""

import json
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright


class ManualSessionRecorder:
    def __init__(self, output_dir: str = "./recording"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.output_dir / "session.log"
        self.requests = []
        self.responses = []
        self.console_logs = []

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        print(entry)
        with open(self.log_file, "a") as f:
            f.write(entry + "\n")

    def on_request(self, request):
        self.requests.append({
            "timestamp": datetime.now().isoformat(),
            "method": request.method,
            "url": request.url,
        })
        self.log(f">> {request.method} {request.url[:80]}")

    def on_response(self, response):
        self.responses.append({
            "timestamp": datetime.now().isoformat(),
            "status": response.status,
            "url": response.url,
        })
        self.log(f"<< {response.status} {response.url[:80]}")

    def on_console(self, msg):
        self.console_logs.append({
            "timestamp": datetime.now().isoformat(),
            "type": msg.type,
            "text": msg.text,
        })
        self.log(f"[console.{msg.type}] {msg.text[:100]}")

    def save_artifacts(self, page, context):
        """Save all recorded data."""
        self.log("Saving artifacts...")

        try:
            # Screenshot
            page.screenshot(path=str(self.output_dir / "final.png"), full_page=True)
            self.log("Saved: final.png")
        except:
            pass

        try:
            # HTML
            html = page.content()
            (self.output_dir / "final.html").write_text(html)
            self.log("Saved: final.html")
        except:
            pass

        try:
            # Trace
            context.tracing.stop(path=str(self.output_dir / "trace.zip"))
            self.log("Saved: trace.zip")
        except:
            pass

        # JSON logs
        (self.output_dir / "requests.json").write_text(
            json.dumps(self.requests, indent=2)
        )
        (self.output_dir / "responses.json").write_text(
            json.dumps(self.responses, indent=2)
        )
        (self.output_dir / "console.json").write_text(
            json.dumps(self.console_logs, indent=2)
        )
        self.log("Saved: requests.json, responses.json, console.json")

    def run(self, url: str, account: str | None = None, wait_seconds: int = 300):
        AUTH_DIR = Path.home() / ".auth"

        with sync_playwright() as p:
            # Setup browser
            if account:
                user_data_dir = AUTH_DIR / "profiles" / account
                if not user_data_dir.exists():
                    self.log(f"Account '{account}' not found")
                    return

                context = p.chromium.launch_persistent_context(
                    str(user_data_dir),
                    headless=False,
                    channel="chrome",
                    no_viewport=True,
                    args=["--disable-blink-features=AutomationControlled"],
                    ignore_default_args=["--enable-automation"],
                )
                page = context.pages[0] if context.pages else context.new_page()
            else:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()

            # Start recording
            context.tracing.start(screenshots=True, snapshots=True)
            page.on("request", self.on_request)
            page.on("response", self.on_response)
            page.on("console", self.on_console)

            # Navigate
            self.log(f"Opening: {url}")
            page.goto(url)
            self.log(f"Browse manually. Close browser when done (timeout: {wait_seconds}s)")

            # Wait for user to close browser
            elapsed = 0
            while elapsed < wait_seconds:
                try:
                    if page.is_closed():
                        break
                    page.evaluate("1")
                except Exception:
                    break
                time.sleep(1)
                elapsed += 1

            self.log("Browser closed")
            self.save_artifacts(page, context)

            try:
                context.close()
            except:
                pass

            self.log("Recording complete!")
            self.log(f"Output: {self.output_dir.absolute()}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Record manual browser session")
    parser.add_argument("url", help="URL to open")
    parser.add_argument("--account", "-a", help="Account to use")
    parser.add_argument("--wait", "-w", type=int, default=300, help="Timeout (default: 300)")
    parser.add_argument("--output", "-o", default="./recording", help="Output directory")

    args = parser.parse_args()

    recorder = ManualSessionRecorder(args.output)
    recorder.run(args.url, args.account, args.wait)
```

**Usage:**
```bash
# Without account
python record_manual.py "https://example.com" -o ./my-session

# With account
python record_manual.py "https://example.com" -a my-account -o ./my-session
```

**Output:**
```
./my-session/
├── session.log      # Activity log
├── requests.json    # All HTTP requests
├── responses.json   # All HTTP responses
├── console.json     # Console messages
├── final.png        # Final screenshot
├── final.html       # Final HTML
└── trace.zip        # Playwright trace
```

**View trace:**
```bash
npx playwright show-trace ./my-session/trace.zip
```

---

## Use Cases

### Debug Login Issues
```bash
uv run browser.py open "https://site.com/login" --account problematic --wait 300
# Observe behavior, check browser.log after
```

### Record Bug Reproduction
```bash
python record_manual.py "https://buggy-site.com" -o ./bug-report
# Reproduce the bug, close browser
# Share trace.zip with developers
```

### Capture Authentication Flow
```bash
uv run browser.py create-login "https://complex-site.com" --account new-account --wait 600
# Complete 2FA, OAuth, etc.
```

---

## Quick Reference

```bash
# Manual browsing (close browser when done)
uv run browser.py open URL [--account NAME] [--wait SECONDS]

# Create login session (close browser when done)
uv run browser.py create-login URL --account NAME [--wait SECONDS]

# List saved accounts
uv run browser.py accounts

# Record with full logging
python record_manual.py URL [-a ACCOUNT] [-o OUTPUT_DIR] [-w TIMEOUT]
```

| Command | Purpose | Browser Mode |
|---------|---------|--------------|
| `open` | Browse with saved session | Headed, wait for close |
| `create-login` | Create new session | Headed, wait for close |
