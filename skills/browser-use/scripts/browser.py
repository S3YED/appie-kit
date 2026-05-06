#!/usr/bin/env python3
"""
Browser automation utilities using Playwright.
Run with: uv run browser.py <command> [options]
"""

import argparse
import base64
import json
import logging
import time
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, TimeoutError as PlaywrightTimeout
from google_image import GoogleImage
from youtube import YouTubeSearch, YouTubeDownload
from tiktok import TikTokSearch, TikTokDownload, TikTokLogin


# Configure logging
LOG_FILE = Path.cwd() / "browser.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Default auth directory in user's home folder
AUTH_DIR = Path.home() / ".auth"


def get_auth_file(account: str) -> Path:
    """Get the auth file path for an account."""
    return AUTH_DIR / f"{account}.json"


def ensure_auth_dir() -> None:
    """Create .auth directory and add to .gitignore if needed."""
    AUTH_DIR.mkdir(parents=True, exist_ok=True)

    gitignore = AUTH_DIR.parent / ".gitignore"
    gitignore_entry = ".auth"

    if gitignore.exists():
        content = gitignore.read_text()
        if gitignore_entry not in content.split('\n'):
            with gitignore.open('a') as f:
                f.write(f"\n{gitignore_entry}\n")
    else:
        gitignore.write_text(f"{gitignore_entry}\n")


def create_session_dir(output_dir: str | None = None) -> Path:
    """Create a new session directory with timestamp.

    Args:
        output_dir: Base directory for sessions. Defaults to ./sessions in current directory.
    """
    from datetime import datetime
    base_dir = Path(output_dir).expanduser() if output_dir else Path.cwd() / "sessions"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = base_dir / timestamp
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def setup_session_logger(session_dir: Path) -> logging.FileHandler:
    """Setup a file handler for session-specific logging."""
    log_file = session_dir / "session.log"
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(handler)
    return handler


def wait_for_page_load(page: Page, timeout: int = 10000, extra_wait: float = 0) -> None:
    """Wait for page to load with fallback for sites with continuous network activity."""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PlaywrightTimeout:
        # Fallback for sites like Gemini with continuous network activity
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)  # Allow JS to render

    if extra_wait > 0:
        time.sleep(extra_wait)


def wait_with_browser_check(page: Page, timeout: int) -> None:
    """Wait for timeout seconds, exit early if browser is closed.

    Args:
        page: Playwright page to monitor.
        timeout: Maximum seconds to wait.
    """
    elapsed = 0
    while elapsed < timeout:
        try:
            # Check if page is closed
            if page.is_closed():
                logger.info("Browser closed by user")
                return

            # Try to access page to verify it's still responsive
            page.evaluate("1")
        except Exception:
            logger.info("Browser closed by user")
            return

        time.sleep(1)
        elapsed += 1


def create_browser(headless: bool = True) -> tuple[Browser, Page]:
    """Create a browser instance and return browser and page."""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)
    page = browser.new_page()
    return browser, page


def get_playwright_user_data_dir(account: str) -> Path:
    """Get a separate user data directory for Playwright (won't conflict with running Chrome)."""
    return AUTH_DIR / "profiles" / account


def create_authenticated_context(playwright, account: str, headless: bool = True, channel: str = "chrome") -> BrowserContext:
    """Create a browser context with saved authentication profile.

    Args:
        playwright: Playwright instance from sync_playwright().
        account: Account name to use.
        headless: Run in headless mode.
        channel: Browser channel (chrome, msedge, chromium).

    Returns:
        BrowserContext with loaded profile.

    Raises:
        FileNotFoundError: If account profile doesn't exist.
    """
    user_data_dir = get_playwright_user_data_dir(account)
    if not user_data_dir.exists():
        raise FileNotFoundError(f"Account '{account}' not found. Run 'create-login' first.")

    return playwright.chromium.launch_persistent_context(
        str(user_data_dir),
        headless=headless,
        channel=channel,
        no_viewport=True,
        args=[
            "--disable-infobars",
            "--start-maximized",
            "--disable-blink-features=AutomationControlled",
        ],
        ignore_default_args=["--enable-automation", "--no-sandbox"],
    )


def create_login(url: str, account: str, wait_seconds: int = 120, channel: str | None = "chrome") -> None:
    """Open browser for manual login and save authentication state."""
    ensure_auth_dir()
    auth_file = get_auth_file(account)

    # Create a persistent profile directory for this account
    user_data_dir = get_playwright_user_data_dir(account)
    user_data_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        logger.info("Using browser channel: %s", channel)
        logger.debug("Using profile directory: %s", user_data_dir)

        # Use persistent context to maintain login state and bypass automation detection
        context = p.chromium.launch_persistent_context(
            str(user_data_dir),
            headless=False,
            channel=channel,
            no_viewport=True,
            args=[
                "--disable-infobars",
                "--no-first-run",
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
            ],
            ignore_default_args=["--enable-automation"],
        )
        logger.debug("Browser version: %s", context.browser.version if context.browser else "N/A")
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(url)

        logger.info("Browser opened at: %s", url)
        logger.info("Please login manually. Session will be saved in %d seconds...", wait_seconds)
        logger.info("(Or close the browser tab when done)")

        # Wait for either timeout or browser close
        elapsed = 0
        browser_closed_early = False
        while elapsed < wait_seconds:
            try:
                # wait_for_timeout keeps connection alive and properly detects browser close
                # unlike page.evaluate() which fails on page redirects
                page.wait_for_timeout(1000)
            except Exception as e:
                error_msg = str(e).lower()
                if "target closed" in error_msg or "browser" in error_msg or "closed" in error_msg:
                    logger.info("Browser closed by user")
                    browser_closed_early = True
                    break
                # Other errors (navigation, etc.) - continue waiting

            elapsed += 1
            remaining = wait_seconds - elapsed
            if remaining > 0 and remaining % 30 == 0:
                logger.info("  %d seconds remaining...", remaining)

        # Save storage state (cookies, localStorage, etc.)
        # With persistent context, profile data is auto-saved to user_data_dir
        # We also save a JSON file for listing accounts
        if browser_closed_early:
            # Browser closed - profile already saved in user_data_dir
            logger.info("Profile saved to: %s", user_data_dir)
            # Create marker file for account listing
            if not auth_file.exists():
                auth_file.write_text('{"cookies":[],"origins":[]}')
        else:
            try:
                context.storage_state(path=str(auth_file))
                logger.info("Authentication saved to: %s", auth_file)
            except Exception:
                logger.info("Profile saved to: %s", user_data_dir)
                if not auth_file.exists():
                    auth_file.write_text('{"cookies":[],"origins":[]}')
            # Clean up context
            try:
                context.close()
            except Exception:
                pass

        logger.info("Account '%s' created successfully!", account)


def list_accounts() -> list[str]:
    """List all saved accounts."""
    if not AUTH_DIR.exists():
        return []
    return [f.stem for f in AUTH_DIR.glob("*.json")]


def open_browser(url: str, account: str | None = None, wait_seconds: int = 60, channel: str | None = "chrome", record: bool = False, output_dir: str | None = None) -> None:
    """Open browser for manual browsing. Waits for user to close browser or timeout."""
    session_dir = None
    session_handler = None

    if record:
        session_dir = create_session_dir(output_dir)
        session_handler = setup_session_logger(session_dir)
        logger.info("Session recording started: %s", session_dir)
        logger.info("URL: %s", url)
        logger.info("Account: %s", account or "none")

    browser_closed_early = False
    with sync_playwright() as p:
        if account:
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=False,
                channel=channel,
                no_viewport=True,
                args=[
                    "--disable-infobars",
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled",
                ],
                ignore_default_args=["--enable-automation"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=False, channel=channel)
            context = browser.new_context()
            page = context.new_page()

        # Start tracing if recording
        if record and session_dir:
            context.tracing.start(screenshots=True, snapshots=True)

        page.goto(url)
        logger.info("Browser opened at: %s", url)
        logger.info("Close browser when done (timeout: %ds)", wait_seconds)

        # Wait for browser close or timeout
        elapsed = 0
        screenshot_count = 0
        last_screenshot_time = 0
        screenshot_interval = 2  # Take screenshot every 2 seconds

        while elapsed < wait_seconds:
            try:
                # wait_for_timeout keeps connection alive and will throw if browser closes
                page.wait_for_timeout(500)
                elapsed += 0.5

                # Take periodic screenshots if recording
                if record and session_dir and (elapsed - last_screenshot_time) >= screenshot_interval:
                    try:
                        screenshot_count += 1
                        screenshot_path = session_dir / f"screenshot_{screenshot_count:03d}.png"
                        page.screenshot(path=str(screenshot_path))
                        logger.info("Screenshot saved: %s", screenshot_path.name)
                        last_screenshot_time = elapsed
                    except Exception as e:
                        # Ignore screenshot errors during navigation
                        pass

            except Exception as e:
                error_msg = str(e).lower()
                if "target closed" in error_msg or "browser" in error_msg or "closed" in error_msg:
                    logger.info("Browser closed by user")
                    browser_closed_early = True
                    break
                # Other errors (navigation, etc.) - continue waiting
                elapsed += 0.5

        logger.info("Browser session ended.")

        # Save final recording if enabled and browser not closed early
        if record and session_dir and not browser_closed_early:
            try:
                # Take final screenshot
                screenshot_count += 1
                screenshot_path = session_dir / f"screenshot_{screenshot_count:03d}_final.png"
                page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info("Final screenshot saved: %s", screenshot_path.name)

                # Stop and save trace
                trace_path = session_dir / "trace.zip"
                context.tracing.stop(path=str(trace_path))
                logger.info("Trace saved: %s", trace_path)
            except Exception as e:
                logger.warning("Failed to save recording: %s", e)

        # Clean up
        try:
            context.close()
        except Exception:
            pass

    # Clean up session logger
    if session_handler:
        logger.removeHandler(session_handler)
        session_handler.close()
        logger.info("Session recording saved to: %s", session_dir)


def goto(url: str, headless: bool = True, screenshot: str | None = None, wait: float = 0, account: str | None = None, channel: str | None = None, record: bool = False, output_dir: str | None = None) -> str:
    """Navigate to a URL and return page content.

    Args:
        url: URL to navigate to.
        headless: Run in headless mode.
        screenshot: Path to save screenshot (optional).
        wait: Extra wait time after page load.
        account: Account name to use for authentication.
        channel: Browser channel (chrome, msedge, chromium).
        record: Enable session recording (trace, logs, screenshot).
        output_dir: Directory to save session recording (default: ./sessions).

    Returns:
        Page HTML content.
    """
    session_dir = None
    session_handler = None

    # Setup session recording
    if record:
        session_dir = create_session_dir(output_dir)
        session_handler = setup_session_logger(session_dir)
        logger.info("Session recording started: %s", session_dir)
        logger.info("URL: %s", url)
        logger.info("Account: %s", account or "none")

    with sync_playwright() as p:
        if account:
            # Use persistent context with saved profile
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return ""

            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=headless,
                channel=channel or "chrome",
                viewport={"width": 1920, "height": 1080},
                args=["--disable-infobars"],
                ignore_default_args=["--enable-automation", "--no-sandbox"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=headless, channel=channel or "chrome")
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

        # Start tracing if recording
        if record and session_dir:
            context.tracing.start(screenshots=True, snapshots=True)
            logger.info("Tracing started")

        page.goto(url)
        logger.info("Page loaded: %s", url)
        wait_for_page_load(page, extra_wait=wait)

        # Save screenshot
        if screenshot:
            page.screenshot(path=screenshot, full_page=True)
            logger.info("Screenshot saved to: %s", screenshot)

        # Session recording artifacts
        if record and session_dir:
            # Final screenshot
            screenshot_path = session_dir / "final.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            logger.info("Final screenshot saved: %s", screenshot_path)

            # Save HTML
            html_path = session_dir / "page.html"
            html_path.write_text(page.content())
            logger.info("HTML saved: %s", html_path)

            # Stop tracing
            trace_path = session_dir / "trace.zip"
            context.tracing.stop(path=str(trace_path))
            logger.info("Trace saved: %s", trace_path)

        content = page.content()
        context.close()

        # Cleanup session logger
        if session_handler:
            logger.info("Session recording complete: %s", session_dir)
            logger.removeHandler(session_handler)
            session_handler.close()

        # Print session directory for user
        if record and session_dir:
            print(f"\nSession recorded to: {session_dir}")
            print(f"  - session.log (logs)")
            print(f"  - final.png (screenshot)")
            print(f"  - page.html (HTML content)")
            print(f"  - trace.zip (Playwright trace)")
            print(f"\nView trace: npx playwright show-trace {session_dir}/trace.zip")

        return content


def screenshot(url: str, output: str = "screenshot.png", full_page: bool = True, wait: float = 0, account: str | None = None, channel: str | None = None) -> None:
    """Take a screenshot of a URL with full screen viewport."""
    with sync_playwright() as p:
        if account:
            # Use persistent context with saved profile
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=True,
                channel=channel or "chrome",
                viewport={"width": 1920, "height": 1080},
                args=["--disable-infobars"],
                ignore_default_args=["--enable-automation", "--no-sandbox"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=True, channel=channel)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

        page.goto(url)
        wait_for_page_load(page, extra_wait=wait)
        page.screenshot(path=output, full_page=full_page)
        logger.info("Screenshot saved to: %s", output)
        context.close()


def get_text(url: str, selector: str = "body") -> str:
    """Extract text content from a URL using a selector."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(url)
        wait_for_page_load(page)

        text = page.locator(selector).text_content()
        browser.close()
        return text or ""


def get_links(url: str) -> list[dict]:
    """Extract all links from a URL."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(url)
        wait_for_page_load(page)

        links = page.locator("a").all()
        result = []
        for link in links:
            href = link.get_attribute("href")
            text = link.text_content()
            if href:
                result.append({"href": href, "text": text.strip() if text else ""})

        browser.close()
        return result


def fill_form(url: str, fields: dict[str, str], submit_selector: str | None = None) -> str:
    """Fill a form and optionally submit it."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(url)
        wait_for_page_load(page)

        for selector, value in fields.items():
            page.fill(selector, value)

        if submit_selector:
            page.click(submit_selector)
            wait_for_page_load(page)

        content = page.content()
        browser.close()
        return content


def click(url: str, selector: str, wait_after: float = 1, screenshot: str | None = None,
          button: str = "left", click_count: int = 1, modifiers: list[str] | None = None,
          position: dict | None = None, force: bool = False,
          headless: bool = True, account: str | None = None, channel: str | None = None) -> str:
    """Click an element on a page.

    Args:
        selector: CSS selector of element to click
        button: Mouse button - "left", "right", or "middle"
        click_count: Number of clicks (1=click, 2=dblclick)
        modifiers: Keyboard modifiers - ["Shift"], ["Control"], ["Alt"], ["Meta"]
        position: Click position relative to element - {"x": 0, "y": 0}
        force: Force click even if element is obscured
    """
    with sync_playwright() as p:
        if account:
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return ""
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=headless,
                channel=channel or "chrome",
                viewport={"width": 1920, "height": 1080},
                args=["--disable-infobars"],
                ignore_default_args=["--enable-automation", "--no-sandbox"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=headless, channel=channel)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

        page.goto(url)
        wait_for_page_load(page)

        # Build click options
        click_opts = {
            "button": button,
            "click_count": click_count,
            "force": force,
        }
        if modifiers:
            click_opts["modifiers"] = modifiers
        if position:
            click_opts["position"] = position

        # Perform click
        page.locator(selector).click(**click_opts)
        click_type = "Double-clicked" if click_count == 2 else "Clicked"
        logger.info("%s: %s (button=%s)", click_type, selector, button)

        if wait_after > 0:
            time.sleep(wait_after)

        if screenshot:
            page.screenshot(path=screenshot, full_page=True)
            logger.info("Screenshot saved to: %s", screenshot)

        content = page.content()
        context.close()
        return content


def extract(url: str, selector: str, attribute: str = "src", all_matches: bool = False,
            headless: bool = True, account: str | None = None, channel: str | None = None) -> str | list[str]:
    """Extract attribute value(s) from element(s) on a page.

    Args:
        selector: CSS selector of element(s)
        attribute: Attribute to extract (default: src). Use "text" for text content.
        all_matches: If True, return all matching elements. If False, return first match only.
    """
    with sync_playwright() as p:
        if account:
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return "" if not all_matches else []
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=headless,
                channel=channel or "chrome",
                viewport={"width": 1920, "height": 1080},
                args=["--disable-infobars"],
                ignore_default_args=["--enable-automation", "--no-sandbox"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=headless, channel=channel)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

        page.goto(url)
        wait_for_page_load(page, extra_wait=1)

        results = []
        elements = page.locator(selector).all()
        logger.info("Found %d elements matching: %s", len(elements), selector)

        for elem in elements:
            try:
                if attribute == "text":
                    value = elem.text_content()
                else:
                    value = elem.get_attribute(attribute)
                if value:
                    results.append(value)
                    if not all_matches:
                        break
            except Exception as e:
                logger.error("Error extracting %s: %s", attribute, e)
                continue

        context.close()

        if all_matches:
            for i, r in enumerate(results):
                logger.info("[%d] %s", i + 1, r[:100] + "..." if len(r) > 100 else r)
            return results
        else:
            result = results[0] if results else ""
            logger.info("Extracted: %s", result)
            return result


def pdf(url: str, output: str = "page.pdf") -> None:
    """Save a page as PDF or download if URL is a direct PDF link."""
    import requests

    # Expand ~ in output path
    output = str(Path(output).expanduser())

    # Check if URL is a direct PDF link
    if url.lower().endswith('.pdf') or '/pdf/' in url.lower():
        try:
            logger.info("Downloading PDF directly from URL...")
            response = requests.get(url, timeout=60, stream=True)
            response.raise_for_status()

            with open(output, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info("PDF saved to: %s", output)
            return
        except Exception as e:
            logger.warning("Direct download failed (%s), trying browser...", e)

    # Use browser to render page as PDF
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080}, accept_downloads=True)
        page = context.new_page()

        try:
            page.goto(url)
            wait_for_page_load(page)
            page.pdf(path=output)
            logger.info("PDF saved to: %s", output)
        except Exception as e:
            # Handle case where navigation triggers download
            if "Download is starting" in str(e):
                logger.info("URL triggers download, using direct download...")
                context.close()
                browser.close()
                # Retry with requests
                response = requests.get(url, timeout=60, stream=True)
                response.raise_for_status()
                with open(output, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logger.info("PDF saved to: %s", output)
                return
            raise
        finally:
            browser.close()


def download(url: str, click_selector: str, output_dir: str = ".", account: str | None = None, channel: str | None = None, timeout: int = 30000) -> str | None:
    """Download a file by clicking an element that triggers download."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        if account:
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return None
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=True,
                channel=channel or "chrome",
                viewport={"width": 1920, "height": 1080},
                args=["--disable-infobars"],
                ignore_default_args=["--enable-automation", "--no-sandbox"],
                accept_downloads=True,
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=True, channel=channel)
            context = browser.new_context(viewport={"width": 1920, "height": 1080}, accept_downloads=True)
            page = context.new_page()

        page.goto(url)
        wait_for_page_load(page)

        # Start waiting for download before clicking
        with page.expect_download(timeout=timeout) as download_info:
            page.click(click_selector)

        download_obj = download_info.value
        filename = download_obj.suggested_filename
        save_path = output_path / filename
        download_obj.save_as(str(save_path))
        logger.info("Downloaded: %s", save_path)

        context.close()
        return str(save_path)


def upload(url: str, input_selector: str, files: list[str], submit_selector: str | None = None, account: str | None = None, channel: str | None = None) -> str:
    """Upload files to a page using a file input element."""
    with sync_playwright() as p:
        if account:
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return ""
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=True,
                channel=channel or "chrome",
                viewport={"width": 1920, "height": 1080},
                args=["--disable-infobars"],
                ignore_default_args=["--enable-automation", "--no-sandbox"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=True, channel=channel)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

        page.goto(url)
        wait_for_page_load(page)

        # Upload files
        if len(files) == 1:
            page.locator(input_selector).set_input_files(files[0])
            logger.info("Uploaded: %s", files[0])
        else:
            page.locator(input_selector).set_input_files(files)
            logger.info("Uploaded %d files", len(files))

        # Optionally submit form
        if submit_selector:
            page.click(submit_selector)
            wait_for_page_load(page)
            logger.info("Form submitted")

        content = page.content()
        context.close()
        return content


def upload_with_chooser(url: str, trigger_selector: str, files: list[str], account: str | None = None, channel: str | None = None) -> str:
    """Upload files using file chooser dialog (for dynamic file inputs)."""
    with sync_playwright() as p:
        if account:
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return ""
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=True,
                channel=channel or "chrome",
                viewport={"width": 1920, "height": 1080},
                args=["--disable-infobars"],
                ignore_default_args=["--enable-automation", "--no-sandbox"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=True, channel=channel)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

        page.goto(url)
        wait_for_page_load(page)

        # Handle file chooser dialog
        with page.expect_file_chooser() as fc_info:
            page.click(trigger_selector)

        file_chooser = fc_info.value
        if len(files) == 1:
            file_chooser.set_files(files[0])
            logger.info("Uploaded via chooser: %s", files[0])
        else:
            file_chooser.set_files(files)
            logger.info("Uploaded %d files via chooser", len(files))

        wait_for_page_load(page)
        content = page.content()
        context.close()
        return content


def fill(url: str, selector: str, value: str, press_key: str | None = None, screenshot: str | None = None,
         wait: float = 0, headless: bool = True, account: str | None = None, channel: str | None = None) -> str:
    """Fill an input field and optionally press a key (like Enter)."""
    with sync_playwright() as p:
        if account:
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return ""
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=headless,
                channel=channel or "chrome",
                viewport={"width": 1920, "height": 1080},
                args=["--disable-infobars"],
                ignore_default_args=["--enable-automation", "--no-sandbox"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=headless, channel=channel)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

        page.goto(url)
        wait_for_page_load(page)

        # Fill the input field
        page.locator(selector).fill(value)
        logger.info("Filled '%s' with: %s", selector, value)

        # Optionally press a key (e.g., Enter)
        if press_key:
            page.locator(selector).press(press_key)
            logger.info("Pressed: %s", press_key)
            wait_for_page_load(page, extra_wait=wait)

        if screenshot:
            page.screenshot(path=screenshot, full_page=True)
            logger.info("Screenshot saved to: %s", screenshot)

        content = page.content()
        context.close()
        return content


def download_from_gallery(url: str, thumb_selector: str, full_selector: str, num_images: int = 5,
                          output_dir: str = ".", headless: bool = True,
                          account: str | None = None, channel: str | None = None,
                          parallel: int = 10, fast: bool = True) -> list[str]:
    """Download full-size images by clicking thumbnails then extracting from preview.

    Generic function for click-to-reveal galleries (works with Google Images, Pinterest, etc.)

    Args:
        thumb_selector: CSS selector for thumbnail elements to click
        full_selector: CSS selector for full-size image element after clicking
        parallel: Number of parallel downloads (default: 10)
        fast: Use fast regex extraction for Google Images (default: True)
    """
    import re
    from concurrent.futures import ThreadPoolExecutor, as_completed

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    collected_urls = []

    def download_single(args: tuple) -> str | None:
        """Download a single image. Returns filename or None."""
        idx, src = args
        try:
            if src.startswith("data:"):
                header, data = src.split(",", 1)
                ext = "jpg"
                if "png" in header:
                    ext = "png"
                elif "gif" in header:
                    ext = "gif"
                elif "webp" in header:
                    ext = "webp"

                img_data = base64.b64decode(data)
                if len(img_data) < 1000:
                    return None
                filename = output_path / f"image_{idx}.{ext}"
                with open(filename, "wb") as f:
                    f.write(img_data)
                return str(filename)

            elif src.startswith("http"):
                response = requests.get(src, timeout=10, headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                })
                if response.status_code == 200 and len(response.content) > 1000:
                    content_type = response.headers.get("content-type", "")
                    ext = "jpg"
                    if "png" in content_type:
                        ext = "png"
                    elif "gif" in content_type:
                        ext = "gif"
                    elif "webp" in content_type:
                        ext = "webp"

                    filename = output_path / f"image_{idx}.{ext}"
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    return str(filename)
        except Exception:
            pass
        return None

    def extract_urls_from_source(html: str, limit: int) -> list[str]:
        """Extract full-size image URLs from Google Images page source using regex."""
        urls = []
        seen = set()

        # Pattern to match full-res image URLs in script tags
        # Matches URLs like ["https://example.com/image.jpg",width,height]
        pattern = r'\["(https?://[^"]+)",\s*\d+,\s*\d+\]'

        for match in re.finditer(pattern, html):
            url = match.group(1)
            # Skip thumbnails and data URLs
            if "encrypted-tbn0.gstatic.com" in url:
                continue
            if url.startswith("data:"):
                continue
            # Decode unicode escapes
            try:
                url = bytes(url, 'ascii').decode('unicode-escape')
            except Exception:
                pass

            if url not in seen and url.startswith("http"):
                seen.add(url)
                urls.append(url)
                if len(urls) >= limit:
                    break

        return urls

    with sync_playwright() as p:
        if account:
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return []
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=headless,
                channel=channel or "chrome",
                viewport={"width": 1920, "height": 1080},
                args=["--disable-infobars"],
                ignore_default_args=["--enable-automation", "--no-sandbox"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=headless, channel=channel)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

        page.goto(url)
        wait_for_page_load(page, extra_wait=1)

        # Try fast extraction from page source first (for Google Images)
        if fast and "google.com" in url:
            logger.info("Fast mode: Extracting URLs from page source...")
            html = page.content()
            collected_urls = extract_urls_from_source(html, num_images)
            logger.info("  Found %d URLs from page source", len(collected_urls))

            # If not enough, scroll and try again
            scroll_count = 0
            while len(collected_urls) < num_images and scroll_count < 10:
                page.evaluate("window.scrollBy(0, window.innerHeight * 2)")
                time.sleep(0.5)
                html = page.content()
                new_urls = extract_urls_from_source(html, num_images * 2)
                for u in new_urls:
                    if u not in collected_urls:
                        collected_urls.append(u)
                        if len(collected_urls) >= num_images:
                            break
                scroll_count += 1
                logger.debug("  Scroll %d: %d URLs", scroll_count, len(collected_urls))

            collected_urls = collected_urls[:num_images]

        # Fallback to click method if fast extraction didn't work
        if not collected_urls:
            logger.info("Fallback: Clicking thumbnails to collect URLs...")
            thumbnails = page.locator(thumb_selector).all()
            logger.info("Found %d thumbnails", len(thumbnails))

            seen_urls = set()
            for thumb in thumbnails:
                if len(collected_urls) >= num_images:
                    break
                try:
                    thumb.click()
                    try:
                        page.locator(full_selector).first.wait_for(state="visible", timeout=2000)
                    except Exception:
                        time.sleep(0.5)

                    full_img = page.locator(full_selector).first
                    if full_img.is_visible():
                        src = full_img.get_attribute("src")
                        if src and src not in seen_urls:
                            if not (src.startswith("data:") and len(src) < 1000):
                                seen_urls.add(src)
                                collected_urls.append(src)
                                logger.debug("  [%d/%d] URL collected", len(collected_urls), num_images)

                    page.keyboard.press("Escape")
                    time.sleep(0.2)
                except Exception:
                    try:
                        page.keyboard.press("Escape")
                    except Exception:
                        pass
                    time.sleep(0.1)

        context.close()

    # Download in parallel
    logger.info("Downloading %d images (parallel=%d)...", len(collected_urls), parallel)
    downloaded_files = []

    with ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = {
            executor.submit(download_single, (i + 1, u)): i
            for i, u in enumerate(collected_urls)
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                downloaded_files.append(result)
                logger.debug("  Downloaded: %s", Path(result).name)

    logger.info("Completed! Downloaded %d images to %s", len(downloaded_files), output_path)
    return downloaded_files


def download_images(url: str, selector: str, num_images: int = 5, output_dir: str = ".",
                    headless: bool = True, account: str | None = None, channel: str | None = None) -> list[str]:
    """Download images directly from src attribute (for simple galleries with direct URLs)."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    downloaded_files = []

    with sync_playwright() as p:
        if account:
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return []
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=headless,
                channel=channel or "chrome",
                viewport={"width": 1920, "height": 1080},
                args=["--disable-infobars"],
                ignore_default_args=["--enable-automation", "--no-sandbox"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = p.chromium.launch(headless=headless, channel=channel)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

        page.goto(url)
        wait_for_page_load(page, extra_wait=2)

        # Find all images matching the selector
        images = page.locator(selector).all()
        logger.info("Found %d images matching selector: %s", len(images), selector)

        downloaded = 0
        for i, img in enumerate(images):
            if downloaded >= num_images:
                break

            try:
                src = img.get_attribute("src")
                if not src:
                    continue

                if src.startswith("data:"):
                    # Base64 encoded image
                    header, data = src.split(",", 1)
                    ext = "jpg"
                    if "png" in header:
                        ext = "png"
                    elif "gif" in header:
                        ext = "gif"
                    elif "webp" in header:
                        ext = "webp"

                    filename = output_path / f"image_{downloaded + 1}.{ext}"
                    with open(filename, "wb") as f:
                        f.write(base64.b64decode(data))
                    logger.info("Downloaded: %s", filename)
                    downloaded_files.append(str(filename))
                    downloaded += 1

                elif src.startswith("http"):
                    # URL - download via requests
                    response = requests.get(src, timeout=10)
                    if response.status_code == 200:
                        content_type = response.headers.get("content-type", "")
                        ext = "jpg"
                        if "png" in content_type:
                            ext = "png"
                        elif "gif" in content_type:
                            ext = "gif"
                        elif "webp" in content_type:
                            ext = "webp"

                        filename = output_path / f"image_{downloaded + 1}.{ext}"
                        with open(filename, "wb") as f:
                            f.write(response.content)
                        logger.info("Downloaded: %s", filename)
                        downloaded_files.append(str(filename))
                        downloaded += 1

            except Exception as e:
                logger.error("Error downloading image %d: %s", i + 1, e)
                continue

        logger.info("Downloaded %d images to %s", downloaded, output_path)
        context.close()
        return downloaded_files


def main():
    import sys
    # Log startup with separator for easy log reading
    logger.info("-" * 60)
    logger.info("browser.py started: %s", " ".join(sys.argv[1:]) or "(no args)")
    logger.info("-" * 60)

    parser = argparse.ArgumentParser(description="Browser automation with Playwright")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # create-login command
    login_parser = subparsers.add_parser("create-login", help="Open browser for manual login and save session")
    login_parser.add_argument("url", help="URL to login page")
    login_parser.add_argument("--account", "-a", required=True, help="Account name to save as")
    login_parser.add_argument("--wait", "-w", type=int, default=120, help="Seconds to wait for login (default: 120)")
    login_parser.add_argument("--channel", "-c", default="chrome", help="Browser channel: chrome, msedge, chromium (default: chrome)")

    # accounts command
    subparsers.add_parser("accounts", help="List saved accounts")

    # open command (manual browsing)
    open_parser = subparsers.add_parser("open", help="Open browser for manual browsing")
    open_parser.add_argument("url", help="URL to open")
    open_parser.add_argument("--account", "-a", help="Use saved account for authentication")
    open_parser.add_argument("--wait", "-w", type=int, default=60, help="Timeout in seconds (default: 60)")
    open_parser.add_argument("--channel", "-c", default="chrome", help="Browser channel: chrome, msedge, chromium")
    open_parser.add_argument("--record", "-r", action="store_true", help="Record session (trace, screenshot)")
    open_parser.add_argument("--output-dir", "-o", help="Directory to save session recording")

    # auto command (automation)
    auto_parser = subparsers.add_parser("auto", help="Navigate to URL and return content (automation)")
    auto_parser.add_argument("url", help="URL to navigate to")
    auto_parser.add_argument("--screenshot", "-s", help="Save screenshot to file")
    auto_parser.add_argument("--no-headless", action="store_true", help="Show browser window")
    auto_parser.add_argument("--wait", "-w", type=float, default=0, help="Extra wait time in seconds after page load")
    auto_parser.add_argument("--account", "-a", help="Use saved account for authentication")
    auto_parser.add_argument("--record", "-r", action="store_true", help="Record session (trace, logs, screenshot)")
    auto_parser.add_argument("--output-dir", "-o", help="Directory to save session recording (default: ./sessions)")

    # screenshot command
    screenshot_parser = subparsers.add_parser("screenshot", help="Take a screenshot")
    screenshot_parser.add_argument("url", help="URL to screenshot")
    screenshot_parser.add_argument("--output", "-o", default="screenshot.png", help="Output file")
    screenshot_parser.add_argument("--no-full-page", action="store_true", help="Capture viewport only")
    screenshot_parser.add_argument("--wait", "-w", type=float, default=0, help="Extra wait time in seconds after page load")
    screenshot_parser.add_argument("--account", "-a", help="Use saved account for authentication")

    # text command
    text_parser = subparsers.add_parser("text", help="Extract text from a page")
    text_parser.add_argument("url", help="URL to extract text from")
    text_parser.add_argument("--selector", "-s", default="body", help="CSS selector")

    # links command
    links_parser = subparsers.add_parser("links", help="Extract links from a page")
    links_parser.add_argument("url", help="URL to extract links from")

    # click command
    click_parser = subparsers.add_parser("click", help="Click an element on a page")
    click_parser.add_argument("url", help="URL of the page")
    click_parser.add_argument("selector", help="CSS selector of element to click")
    click_parser.add_argument("--wait", "-w", type=float, default=1, help="Wait time after click (default: 1)")
    click_parser.add_argument("--screenshot", "-s", help="Save screenshot after click")
    click_parser.add_argument("--button", "-b", default="left", choices=["left", "right", "middle"], help="Mouse button")
    click_parser.add_argument("--dblclick", action="store_true", help="Double click")
    click_parser.add_argument("--shift", action="store_true", help="Hold Shift while clicking")
    click_parser.add_argument("--ctrl", action="store_true", help="Hold Control while clicking")
    click_parser.add_argument("--force", action="store_true", help="Force click even if element is obscured")
    click_parser.add_argument("--no-headless", action="store_true", help="Show browser window")
    click_parser.add_argument("--account", "-a", help="Use saved account for authentication")

    # extract command
    extract_parser = subparsers.add_parser("extract", help="Extract attribute from element(s)")
    extract_parser.add_argument("url", help="URL of the page")
    extract_parser.add_argument("selector", help="CSS selector of element(s)")
    extract_parser.add_argument("--attr", default="src", help="Attribute to extract (default: src). Use 'text' for text content")
    extract_parser.add_argument("--all", action="store_true", help="Extract from all matching elements")
    extract_parser.add_argument("--no-headless", action="store_true", help="Show browser window")
    extract_parser.add_argument("--account", "-a", help="Use saved account for authentication")

    # pdf command
    pdf_parser = subparsers.add_parser("pdf", help="Save page as PDF")
    pdf_parser.add_argument("url", help="URL to save")
    pdf_parser.add_argument("--output", "-o", default="page.pdf", help="Output file")

    # download command
    download_parser = subparsers.add_parser("download", help="Download a file by clicking an element")
    download_parser.add_argument("url", help="URL of the page with download link")
    download_parser.add_argument("selector", help="CSS selector of element to click for download")
    download_parser.add_argument("--output-dir", "-o", default=".", help="Directory to save downloaded file")
    download_parser.add_argument("--account", "-a", help="Use saved account for authentication")
    download_parser.add_argument("--timeout", "-t", type=int, default=30000, help="Download timeout in ms (default: 30000)")

    # upload command
    upload_parser = subparsers.add_parser("upload", help="Upload files to a page")
    upload_parser.add_argument("url", help="URL of the page with upload form")
    upload_parser.add_argument("selector", help="CSS selector of file input element")
    upload_parser.add_argument("files", nargs="+", help="File(s) to upload")
    upload_parser.add_argument("--submit", "-s", help="CSS selector of submit button (optional)")
    upload_parser.add_argument("--account", "-a", help="Use saved account for authentication")

    # upload-chooser command (for dynamic file inputs)
    upload_chooser_parser = subparsers.add_parser("upload-chooser", help="Upload files via file chooser dialog")
    upload_chooser_parser.add_argument("url", help="URL of the page")
    upload_chooser_parser.add_argument("trigger", help="CSS selector of element that opens file chooser")
    upload_chooser_parser.add_argument("files", nargs="+", help="File(s) to upload")
    upload_chooser_parser.add_argument("--account", "-a", help="Use saved account for authentication")

    # fill command
    fill_parser = subparsers.add_parser("fill", help="Fill an input field and optionally press a key")
    fill_parser.add_argument("url", help="URL of the page")
    fill_parser.add_argument("selector", help="CSS selector of the input element")
    fill_parser.add_argument("value", help="Value to fill")
    fill_parser.add_argument("--press", "-p", help="Key to press after filling (e.g., Enter)")
    fill_parser.add_argument("--screenshot", "-s", help="Save screenshot after action")
    fill_parser.add_argument("--wait", "-w", type=float, default=2, help="Extra wait time after pressing key (default: 2)")
    fill_parser.add_argument("--no-headless", action="store_true", help="Show browser window")
    fill_parser.add_argument("--account", "-a", help="Use saved account for authentication")

    # download-images command
    download_images_parser = subparsers.add_parser("download-images", help="Download images directly from src")
    download_images_parser.add_argument("url", help="URL of the page with images")
    download_images_parser.add_argument("selector", help="CSS selector for img elements")
    download_images_parser.add_argument("--num", "-n", type=int, default=5, help="Number of images to download (default: 5)")
    download_images_parser.add_argument("--output-dir", "-o", default=".", help="Directory to save images")
    download_images_parser.add_argument("--no-headless", action="store_true", help="Show browser window")
    download_images_parser.add_argument("--account", "-a", help="Use saved account for authentication")

    # download-from-gallery command
    gallery_parser = subparsers.add_parser("download-from-gallery", help="Download images by clicking thumbnails")
    gallery_parser.add_argument("url", help="URL of the gallery page")
    gallery_parser.add_argument("thumb_selector", help="CSS selector for thumbnail elements to click")
    gallery_parser.add_argument("full_selector", help="CSS selector for full-size image after click")
    gallery_parser.add_argument("--num", "-n", type=int, default=5, help="Number of images to download (default: 5)")
    gallery_parser.add_argument("--output-dir", "-o", default=".", help="Directory to save images")
    gallery_parser.add_argument("--no-headless", action="store_true", help="Show browser window")
    gallery_parser.add_argument("--account", "-a", help="Use saved account for authentication")

    # google-image command (auto-generated from GoogleImage class)
    GoogleImage.add_to_parser(subparsers)

    # youtube commands (auto-generated from YouTube classes)
    YouTubeSearch.add_to_parser(subparsers)
    YouTubeDownload.add_to_parser(subparsers)

    # tiktok commands (auto-generated from TikTok classes)
    TikTokLogin.add_to_parser(subparsers)
    TikTokSearch.add_to_parser(subparsers)
    TikTokDownload.add_to_parser(subparsers)

    args = parser.parse_args()

    if args.command == "create-login":
        channel = args.channel if args.channel != "chromium" else None
        create_login(args.url, args.account, args.wait, channel)
    elif args.command == "accounts":
        accounts = list_accounts()
        if accounts:
            logger.info("Saved accounts:")
            for acc in accounts:
                logger.info("  - %s", acc)
        else:
            logger.info("No saved accounts. Use 'create-login' to save one.")
    elif args.command == "open":
        channel = args.channel if args.channel != "chromium" else None
        open_browser(args.url, args.account, args.wait, channel, record=args.record, output_dir=args.output_dir)
    elif args.command == "auto":
        content = goto(args.url, headless=not args.no_headless, screenshot=args.screenshot, wait=args.wait, account=args.account, record=args.record, output_dir=args.output_dir)
        if not args.record:  # Only print content if not recording (recording prints session info)
            print(content[:2000] if len(content) > 2000 else content)
    elif args.command == "screenshot":
        screenshot(args.url, args.output, full_page=not args.no_full_page, wait=args.wait, account=args.account)
    elif args.command == "text":
        text = get_text(args.url, args.selector)
        print(text)
    elif args.command == "links":
        links = get_links(args.url)
        print(json.dumps(links, indent=2))
    elif args.command == "click":
        modifiers = []
        if args.shift:
            modifiers.append("Shift")
        if args.ctrl:
            modifiers.append("Control")
        click_count = 2 if args.dblclick else 1
        content = click(args.url, args.selector, args.wait, args.screenshot,
                        args.button, click_count, modifiers if modifiers else None,
                        None, args.force, headless=not args.no_headless, account=args.account)
        print(content[:2000] if len(content) > 2000 else content)
    elif args.command == "extract":
        result = extract(args.url, args.selector, args.attr, getattr(args, 'all', False),
                         headless=not args.no_headless, account=args.account)
        if isinstance(result, list):
            print(json.dumps(result, indent=2))
        else:
            print(result)
    elif args.command == "pdf":
        pdf(args.url, args.output)
    elif args.command == "download":
        download(args.url, args.selector, args.output_dir, args.account, timeout=args.timeout)
    elif args.command == "upload":
        upload(args.url, args.selector, args.files, args.submit, args.account)
    elif args.command == "upload-chooser":
        upload_with_chooser(args.url, args.trigger, args.files, args.account)
    elif args.command == "fill":
        content = fill(args.url, args.selector, args.value, args.press, args.screenshot,
                       args.wait, headless=not args.no_headless, account=args.account)
        print(content[:2000] if len(content) > 2000 else content)
    elif args.command == "download-images":
        download_images(args.url, args.selector, args.num, args.output_dir,
                        headless=not args.no_headless, account=args.account)
    elif args.command == "download-from-gallery":
        download_from_gallery(args.url, args.thumb_selector, args.full_selector,
                              args.num, args.output_dir,
                              headless=not args.no_headless, account=args.account)
    elif args.command == "google-image":
        gimg = GoogleImage.from_args(args)
        gimg.run()
    elif args.command == "youtube-search":
        yt_search = YouTubeSearch.from_args(args)
        results = yt_search.run()
        print(json.dumps(results, indent=2))
    elif args.command == "youtube-download":
        yt_download = YouTubeDownload.from_args(args)
        yt_download.run()
    elif args.command == "tiktok-login":
        tt_login = TikTokLogin.from_args(args)
        tt_login.run()
    elif args.command == "tiktok-search":
        tt_search = TikTokSearch.from_args(args)
        results = tt_search.run()
        print(json.dumps(results, indent=2))
    elif args.command == "tiktok-download":
        tt_download = TikTokDownload.from_args(args)
        tt_download.run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
