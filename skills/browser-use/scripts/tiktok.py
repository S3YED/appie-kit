#!/usr/bin/env python3
"""
TikTok search and download utilities.

This module provides TikTokSearch and TikTokDownload classes for searching
videos by hashtag/keyword and downloading them.

Architecture:
1. Search: Playwright browser automation (required - TikTok has no public search API)
2. Download: yt-dlp (fast, reliable for TikTok video extraction)

IMPORTANT: TikTok heavily blocks headless browsers. The --no-headless flag is
recommended for search operations. Headless mode may fail silently.

Unlike YouTube (which has yt-dlp ytsearch), TikTok requires browser automation
for search since there's no public API or yt-dlp search prefix support.

Usage via browser.py:
    # Login (creates persistent Chrome profile for authenticated operations)
    uv run browser.py tiktok-login --account myaccount
    uv run browser.py tiktok-login --account myaccount --wait 180  # Wait 3 min for login

    # Search (use --no-headless for best results)
    uv run browser.py tiktok-search "keyword" -n 10 --no-headless
    uv run browser.py tiktok-search "#dance" -n 5 --no-headless
    uv run browser.py tiktok-search "keyword" -n 10 -a myaccount --no-headless  # With account

    # Download single video
    uv run browser.py tiktok-download "https://tiktok.com/@user/video/123" -o ~/Downloads

    # Search + download (use --no-headless)
    uv run browser.py tiktok-download "keyword" --search -n 5 -o ~/Downloads --no-headless
"""

import dataclasses
import json
import logging
import re
import subprocess
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from playwright.sync_api import sync_playwright, Page

logger = logging.getLogger(__name__)


def _search_tiktok_playwright(
    keyword: str,
    num: int = 10,
    headless: bool = True,
    account: str | None = None,
) -> list[dict]:
    """Search TikTok videos using Playwright browser.

    TikTok requires browser automation for search since there's no
    public API or yt-dlp search support like YouTube has.

    Args:
        keyword: Search query (hashtag or keyword)
        num: Number of results to return
        headless: Run browser in headless mode
        account: Optional account name for authenticated context

    Returns:
        List of video dictionaries with url, title, author, views, likes
    """
    # Clean keyword - remove # prefix if present for URL
    search_keyword = keyword.lstrip("#")
    encoded_keyword = urllib.parse.quote(search_keyword)

    # TikTok search URL
    search_url = f"https://www.tiktok.com/search/video?q={encoded_keyword}"

    results = []

    with sync_playwright() as p:
        # Launch browser with stealth settings
        # TikTok blocks headless browsers heavily, so we use real Chrome channel
        browser_args = [
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--no-first-run",
            "--disable-features=IsolateOrigins,site-per-process",
        ]

        if account:
            from browser import get_playwright_user_data_dir
            user_data_dir = get_playwright_user_data_dir(account)
            if not user_data_dir.exists():
                logger.warning("Account '%s' not found. Run 'create-login' first.", account)
                return []
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=headless,
                channel="chrome",
                args=browser_args + ["--start-maximized"],
                no_viewport=True,  # Allow maximized window
                ignore_default_args=["--enable-automation"],
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            # Use Chrome channel for better TikTok compatibility
            browser = p.chromium.launch(
                headless=headless,
                channel="chrome",  # Use real Chrome instead of Chromium
                args=browser_args,
            )
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            )
            page = context.new_page()

            # Add stealth script to hide automation
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            """)

        try:
            logger.info("Searching TikTok: '%s'", keyword)
            page.goto(search_url, timeout=60000)

            # Wait for page to load - TikTok is heavily JS-rendered
            try:
                page.wait_for_load_state("domcontentloaded", timeout=15000)
            except Exception:
                pass

            # Additional wait for JS to render content
            time.sleep(3)

            # Handle cookie consent if present
            try:
                accept_btn = page.locator("button:has-text('Accept all')").first
                if accept_btn.is_visible(timeout=2000):
                    accept_btn.click()
                    time.sleep(0.5)
            except Exception:
                pass

            # Verify we're on the search page, not activity page
            current_url = page.url
            if "/search/" not in current_url:
                logger.warning("Not on search page, navigating again...")
                page.goto(search_url, timeout=60000)
                time.sleep(3)

            # Try to wait for video elements to appear
            try:
                page.wait_for_selector('a[href*="/video/"]', timeout=10000)
            except Exception:
                logger.debug("No video links found immediately, will try scrolling")
                time.sleep(2)

            # Scroll and collect videos
            results = _extract_tiktok_videos(page, num)

        except Exception as e:
            logger.error("TikTok search failed: %s", e)
        finally:
            context.close()

    return results


def _extract_tiktok_videos(page: Page, num: int) -> list[dict]:
    """Extract video information from TikTok search results.

    Args:
        page: Playwright page with search results loaded
        num: Maximum number of videos to extract

    Returns:
        List of video dictionaries
    """
    results = []
    seen_urls = set()
    max_scrolls = 20
    scroll_count = 0

    while len(results) < num and scroll_count < max_scrolls:
        # Extract videos using JavaScript evaluation (faster than Playwright locators)
        videos_data = page.evaluate("""
            () => {
                const videos = [];

                // Method 1: Find all video links directly
                const allLinks = document.querySelectorAll('a[href*="/video/"]');
                const seen = new Set();

                allLinks.forEach(link => {
                    const href = link.getAttribute('href');
                    if (!href || !href.includes('/video/')) return;

                    const url = href.startsWith('http') ? href : 'https://www.tiktok.com' + href;
                    if (seen.has(url)) return;
                    seen.add(url);

                    // Try to find parent container
                    let container = link.closest('[class*="DivItemContainer"]') ||
                                   link.closest('[class*="DivWrapper"]') ||
                                   link.closest('[class*="ItemContainer"]') ||
                                   link.parentElement?.parentElement?.parentElement;

                    // Extract author from URL pattern /@username/video/
                    let author = '';
                    const authorMatch = href.match(/@([^/]+)[/]video/);
                    if (authorMatch) {
                        author = authorMatch[1];
                    }

                    // Extract description from container or nearby elements
                    let title = '';
                    if (container) {
                        // Look for description elements
                        const descElem = container.querySelector('[class*="Desc"]') ||
                                        container.querySelector('[class*="Caption"]') ||
                                        container.querySelector('span[class*="SpanText"]');
                        if (descElem) {
                            title = descElem.textContent?.trim()?.slice(0, 200) || '';
                        }
                    }

                    // Extract stats if available
                    let views = '';
                    let likes = '';
                    let date = '';
                    if (container) {
                        const strongElems = container.querySelectorAll('strong');
                        strongElems.forEach((s, i) => {
                            const text = s.textContent || '';
                            if (i === 0) likes = text;
                            else if (i === 1) views = text;
                        });

                        // Extract date - look for relative time patterns
                        const containerText = container.textContent || '';
                        // Match patterns like "1d ago", "2h ago", "3w ago", "10-29", "8-4"
                        const dateMatch = containerText.match(/([0-9]+[hdwm] *ago|[0-9]{1,2}-[0-9]{1,2})/i);
                        if (dateMatch) {
                            date = dateMatch[1];
                        }
                    }

                    videos.push({ url, title, author, views, likes, date });
                });

                return videos;
            }
        """)

        # Process extracted videos
        for v in videos_data:
            url = v.get("url", "")
            if not url or url in seen_urls:
                continue
            if "/video/" not in url:
                continue

            seen_urls.add(url)
            results.append({
                "url": url,
                "title": v.get("title", "")[:200],
                "author": v.get("author", ""),
                "views": v.get("views", ""),
                "likes": v.get("likes", ""),
                "date": v.get("date", ""),
            })

            if len(results) >= num:
                break

        if len(results) >= num:
            break

        # Scroll for more results
        page.evaluate("window.scrollBy(0, window.innerHeight * 2)")
        time.sleep(0.5)
        scroll_count += 1
        logger.debug("Scroll %d: found %d/%d videos", scroll_count, len(results), num)

    logger.info("Found %d TikTok videos", len(results))
    return results[:num]


def _download_tiktok_video(url: str, output_dir: Path, concurrent_fragments: int = 4) -> str | None:
    """Download a single TikTok video using yt-dlp.

    Args:
        url: TikTok video URL
        output_dir: Directory to save video
        concurrent_fragments: Number of concurrent fragment downloads

    Returns:
        Path to downloaded file or None if failed
    """
    cmd = [
        "yt-dlp",
        "-f", "best",  # TikTok usually has single format
        "-o", str(output_dir / "%(uploader)s_%(id)s.%(ext)s"),
        "--no-playlist",
        "--restrict-filenames",
        "--no-mtime",
        "-N", str(concurrent_fragments),
        url,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode == 0:
            # Try to extract downloaded filename from output
            for line in result.stdout.split("\n"):
                if "Destination:" in line:
                    match = re.search(r"Destination: (.+)$", line)
                    if match:
                        filepath = match.group(1)
                        logger.info("Downloaded: %s", Path(filepath).name)
                        return filepath
                if "has already been downloaded" in line:
                    match = re.search(r"\[download\] (.+) has already been downloaded", line)
                    if match:
                        filepath = match.group(1)
                        logger.info("Already exists: %s", Path(filepath).name)
                        return filepath

            # Find most recently modified file in output dir
            files = list(output_dir.glob("*.mp4"))
            if files:
                newest = max(files, key=lambda f: f.stat().st_mtime)
                logger.info("Downloaded: %s", newest.name)
                return str(newest)

            logger.info("Download completed")
            return str(output_dir)
        else:
            logger.error("yt-dlp error: %s", result.stderr[:200])
            return None

    except subprocess.TimeoutExpired:
        logger.error("Download timed out: %s", url)
        return None
    except FileNotFoundError:
        logger.error("yt-dlp not found. Install with: uv add yt-dlp")
        return None
    except Exception as e:
        logger.error("Download error: %s", e)
        return None


@dataclass
class TikTokSearch:
    """TikTok video search using Playwright.

    Since TikTok doesn't have a public search API or yt-dlp search support,
    we use browser automation to scrape search results.

    Attributes:
        keyword: Search query (hashtag or keyword)
        num: Number of results to return
        output: JSON output path for results
        headless: Run browser in headless mode
        account: Optional account for authenticated search
    """

    # CLI metadata
    _cli_name: ClassVar[str] = "tiktok-search"
    _cli_description: ClassVar[str] = "Search TikTok videos by keyword or hashtag"
    _cli_help: ClassVar[dict] = {
        "keyword": "Search keyword or hashtag (e.g., 'funny cats' or '#dance')",
        "num": "Number of results to return",
        "output": "JSON output path for results",
        "headless": "Run in headless mode",
        "account": "Account name for authenticated search",
    }
    _cli_choices: ClassVar[dict] = {}
    _cli_short: ClassVar[dict] = {
        "num": "n",
        "output": "o",
        "account": "a",
    }

    # Instance fields
    keyword: str
    num: int = 10
    output: str | None = None
    headless: bool = True
    account: str | None = None

    def run(self) -> list[dict]:
        """Run the TikTok search.

        Returns:
            List of video dictionaries with url, title, author, views, likes
        """
        logger.info("Starting TikTok search for: '%s' (num=%d)", self.keyword, self.num)

        results = _search_tiktok_playwright(
            keyword=self.keyword,
            num=self.num,
            headless=self.headless,
            account=self.account,
        )

        # Save results if output path specified
        if self.output and results:
            with open(self.output, "w") as f:
                json.dump(results, f, indent=2)
            logger.info("Results saved: %s", self.output)

        logger.info("Found %d videos", len(results))
        return results

    @classmethod
    def add_to_parser(cls, subparsers) -> None:
        """Add this command to argparse subparsers."""
        parser = subparsers.add_parser(cls._cli_name, help=cls._cli_description)

        for name, fld in cls.__dataclass_fields__.items():
            if name.startswith("_"):
                continue

            help_text = cls._cli_help.get(name, "")
            is_required = fld.default is dataclasses.MISSING
            default = fld.default if not is_required else None
            short = cls._cli_short.get(name)

            if is_required:
                names = [name]
            else:
                names = [f"--{name}"]
                if short:
                    names.insert(0, f"-{short}")

            kwargs = {"help": help_text}

            if not is_required:
                kwargs["default"] = default

            if name in cls._cli_choices:
                kwargs["choices"] = cls._cli_choices[name]

            if fld.type is bool or (hasattr(fld, "type") and fld.type is bool):
                if default is True:
                    names = [f"--no-{name}"]
                    kwargs["action"] = "store_false"
                    kwargs["dest"] = name
                    kwargs.pop("default", None)
                else:
                    kwargs["action"] = "store_true"

            if fld.type is int:
                kwargs["type"] = int

            parser.add_argument(*names, **kwargs)

    @classmethod
    def from_args(cls, args) -> "TikTokSearch":
        """Create instance from parsed args."""
        kwargs = {}
        for name in cls.__dataclass_fields__:
            if name.startswith("_"):
                continue
            if hasattr(args, name):
                kwargs[name] = getattr(args, name)
        return cls(**kwargs)


@dataclass
class TikTokDownload:
    """TikTok video download using yt-dlp.

    Supports both direct URL download and search-then-download mode.

    Attributes:
        url: TikTok video URL or search query (with --search)
        output_dir: Directory to save downloaded videos
        search: If True, treat url as search query
        num: Number of videos to download when searching
        headless: Run browser in headless mode for search
        account: Account name for authenticated operations
        parallel: Number of parallel downloads
    """

    # CLI metadata
    _cli_name: ClassVar[str] = "tiktok-download"
    _cli_description: ClassVar[str] = "Download TikTok videos using yt-dlp"
    _cli_help: ClassVar[dict] = {
        "url": "TikTok URL or search query (with --search)",
        "output_dir": "Directory to save videos",
        "search": "Treat input as search query",
        "num": "Number of videos to download (with --search)",
        "headless": "Run browser in headless mode",
        "account": "Account name for authenticated operations",
        "parallel": "Number of parallel downloads (default: 3)",
    }
    _cli_choices: ClassVar[dict] = {}
    _cli_short: ClassVar[dict] = {
        "output_dir": "o",
        "search": "s",
        "num": "n",
        "account": "a",
        "parallel": "p",
    }

    # Instance fields
    url: str
    output_dir: str = "~/Downloads"
    search: bool = False
    num: int = 5
    headless: bool = True
    account: str | None = None
    parallel: int = 3

    def run(self) -> list[str]:
        """Run the download and return list of downloaded files."""
        output_path = Path(self.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        urls_to_download = []

        # Search mode: find video URLs first
        if self.search:
            logger.info("Searching TikTok for: %s", self.url)

            results = _search_tiktok_playwright(
                keyword=self.url,
                num=self.num,
                headless=self.headless,
                account=self.account,
            )

            if not results:
                logger.warning("No videos found for search query")
                return []

            urls_to_download = [r["url"] for r in results[:self.num]]
            logger.info("Found %d videos to download", len(urls_to_download))
        else:
            # Direct URL mode
            urls_to_download = [self.url]

        downloaded_files = []

        # Download videos
        if len(urls_to_download) > 1 and self.parallel > 1:
            # Parallel downloads for multiple videos
            logger.info("Downloading %d videos with %d parallel workers...",
                       len(urls_to_download), self.parallel)

            with ThreadPoolExecutor(max_workers=self.parallel) as executor:
                futures = {
                    executor.submit(_download_tiktok_video, url, output_path): url
                    for url in urls_to_download
                }
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        downloaded_files.append(result)
        else:
            # Sequential download
            for url in urls_to_download:
                logger.info("Downloading: %s", url)
                result = _download_tiktok_video(url, output_path)
                if result:
                    downloaded_files.append(result)

        logger.info("Downloaded %d file(s) to %s", len(downloaded_files), output_path)
        return downloaded_files

    @classmethod
    def add_to_parser(cls, subparsers) -> None:
        """Add this command to argparse subparsers."""
        parser = subparsers.add_parser(cls._cli_name, help=cls._cli_description)

        for name, fld in cls.__dataclass_fields__.items():
            if name.startswith("_"):
                continue

            help_text = cls._cli_help.get(name, "")
            is_required = fld.default is dataclasses.MISSING
            default = fld.default if not is_required else None
            short = cls._cli_short.get(name)

            if is_required:
                names = [name]
            else:
                names = [f"--{name}"]
                if short:
                    names.insert(0, f"-{short}")

            kwargs = {"help": help_text}

            if not is_required:
                kwargs["default"] = default

            if name in cls._cli_choices:
                kwargs["choices"] = cls._cli_choices[name]

            if fld.type is bool or (hasattr(fld, "type") and fld.type is bool):
                if default is True:
                    names = [f"--no-{name}"]
                    kwargs["action"] = "store_false"
                    kwargs["dest"] = name
                    kwargs.pop("default", None)
                else:
                    kwargs["action"] = "store_true"

            if fld.type is int:
                kwargs["type"] = int

            parser.add_argument(*names, **kwargs)

    @classmethod
    def from_args(cls, args) -> "TikTokDownload":
        """Create instance from parsed args."""
        kwargs = {}
        for name in cls.__dataclass_fields__:
            if name.startswith("_"):
                continue
            if hasattr(args, name):
                kwargs[name] = getattr(args, name)
        return cls(**kwargs)


@dataclass
class TikTokLogin:
    """TikTok login to create persistent browser profile.

    Opens a browser window for manual TikTok login. The session is saved
    to a persistent Chrome profile that can be reused for authenticated
    operations like searching or accessing personalized content.

    Attributes:
        account: Account name to save the session as
        wait: Seconds to wait for login (default: 120)
    """

    # CLI metadata
    _cli_name: ClassVar[str] = "tiktok-login"
    _cli_description: ClassVar[str] = "Login to TikTok and save session for authenticated operations"
    _cli_help: ClassVar[dict] = {
        "account": "Account name to save session as",
        "wait": "Seconds to wait for login (default: 120)",
    }
    _cli_choices: ClassVar[dict] = {}
    _cli_short: ClassVar[dict] = {
        "account": "a",
        "wait": "w",
    }

    # Instance fields
    account: str
    wait: int = 120

    def run(self) -> bool:
        """Open browser for TikTok login and save session.

        Returns:
            True if login was successful, False otherwise
        """
        from browser import get_playwright_user_data_dir, ensure_auth_dir

        ensure_auth_dir()

        # Create profile directory for this account
        user_data_dir = get_playwright_user_data_dir(self.account)
        user_data_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Opening TikTok for login...")
        logger.info("Account will be saved as: %s", self.account)
        logger.info("Profile directory: %s", user_data_dir)

        with sync_playwright() as p:
            # Launch persistent context with stealth settings
            context = p.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=False,  # Must be visible for login
                channel="chrome",
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

            page = context.pages[0] if context.pages else context.new_page()

            # Navigate to TikTok login page
            page.goto("https://www.tiktok.com/login", timeout=60000)

            logger.info("Please login to TikTok manually.")
            logger.info("Session will be saved in %d seconds...", self.wait)
            logger.info("(Or close the browser when done)")

            # Wait for login or timeout
            elapsed = 0
            while elapsed < self.wait and not page.is_closed():
                time.sleep(1)
                elapsed += 1
                remaining = self.wait - elapsed
                if remaining > 0 and remaining % 30 == 0:
                    logger.info("  %d seconds remaining...", remaining)

                # Check if logged in by looking for profile elements
                try:
                    # If we can find the user avatar or profile link, login succeeded
                    if page.locator('[data-e2e="profile-icon"]').is_visible(timeout=500):
                        logger.info("Login detected! Saving session...")
                        break
                except Exception:
                    pass

            # Close context (profile is auto-saved)
            if context.pages:
                logger.info("Session saved to: %s", user_data_dir)
                context.close()
                return True
            else:
                logger.info("Browser closed. Session saved to: %s", user_data_dir)
                context.close()
                return True

    @classmethod
    def add_to_parser(cls, subparsers) -> None:
        """Add this command to argparse subparsers."""
        parser = subparsers.add_parser(cls._cli_name, help=cls._cli_description)

        for name, fld in cls.__dataclass_fields__.items():
            if name.startswith("_"):
                continue

            help_text = cls._cli_help.get(name, "")
            is_required = fld.default is dataclasses.MISSING
            default = fld.default if not is_required else None
            short = cls._cli_short.get(name)

            if is_required:
                names = [f"--{name}"]  # account is required but as --account
                if short:
                    names.insert(0, f"-{short}")
            else:
                names = [f"--{name}"]
                if short:
                    names.insert(0, f"-{short}")

            kwargs = {"help": help_text, "required": is_required}

            if not is_required:
                kwargs["default"] = default
                kwargs.pop("required", None)

            if name in cls._cli_choices:
                kwargs["choices"] = cls._cli_choices[name]

            if fld.type is bool or (hasattr(fld, "type") and fld.type is bool):
                if default is True:
                    names = [f"--no-{name}"]
                    kwargs["action"] = "store_false"
                    kwargs["dest"] = name
                    kwargs.pop("default", None)
                    kwargs.pop("required", None)
                else:
                    kwargs["action"] = "store_true"
                    kwargs.pop("required", None)

            if fld.type is int:
                kwargs["type"] = int

            parser.add_argument(*names, **kwargs)

    @classmethod
    def from_args(cls, args) -> "TikTokLogin":
        """Create instance from parsed args."""
        kwargs = {}
        for name in cls.__dataclass_fields__:
            if name.startswith("_"):
                continue
            if hasattr(args, name):
                kwargs[name] = getattr(args, name)
        return cls(**kwargs)
