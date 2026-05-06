#!/usr/bin/env python3
"""
YouTube automation utilities using Playwright and yt-dlp.

This module provides YouTubeSearch and YouTubeDownload classes for searching
videos and downloading them with various quality options.

Optimizations:
- Fast search via youtube-search-python (no browser needed, 10x faster)
- Fallback to Playwright if fast search fails
- aria2c external downloader for 3-5x faster downloads
- Concurrent fragment downloads

Usage via browser.py:
    uv run browser.py youtube-search "keyword" -n 10
    uv run browser.py youtube-download "https://youtube.com/watch?v=..." -o ./downloads
    uv run browser.py youtube-download "keyword" --search -o ./downloads
"""

import dataclasses
import json
import logging
import re
import shutil
import subprocess
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Literal

from playwright.sync_api import sync_playwright, Page

logger = logging.getLogger(__name__)

# Check if aria2c is available for faster downloads
ARIA2C_AVAILABLE = shutil.which("aria2c") is not None


def _search_ytdlp_fast(
    keyword: str,
    num: int = 10,
    min_duration: int | None = None,
    max_duration: int | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict] | None:
    """Ultra-fast YouTube search using yt-dlp ytsearch (no browser, no extra library).

    This is the fastest method (~1.6s vs 11s for full extraction).
    Uses --flat-playlist to skip full video info extraction.

    Args:
        keyword: Search query
        num: Number of results to return
        min_duration: Minimum video duration in minutes
        max_duration: Maximum video duration in minutes
        date_from: Filter videos uploaded after this date (YYYYMMDD format)
        date_to: Filter videos uploaded before this date (YYYYMMDD format)

    Returns None if yt-dlp is not available or search fails.
    """
    # Convert to int if passed as string from CLI
    min_dur = int(min_duration) if min_duration else None
    max_dur = int(max_duration) if max_duration else None

    # Fetch more results to account for duration/date filtering
    # With filters, we need more results since many will be filtered out
    has_filters = min_dur or max_dur or date_from or date_to
    fetch_num = num * 5 if has_filters else num
    fetch_num = min(fetch_num, 50)  # yt-dlp reasonable limit

    # Note: --flat-playlist is faster but doesn't return upload_date
    # We need full extraction to get dates, which is slower (~10s vs ~1.5s)
    # but necessary for date filtering and date display
    cmd = [
        "yt-dlp",
        f"ytsearch{fetch_num}:{keyword}",
        "--dump-json",
        "--skip-download",
        "--quiet",
        "--no-warnings",
        "--ignore-errors",
    ]
    # Note: --dateafter/--datebefore don't work well with ytsearch
    # We do post-filtering by date instead

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,  # Full extraction needs more time than flat-playlist
        )

        if result.returncode != 0:
            logger.debug("yt-dlp search failed: %s", result.stderr[:100])
            return None

        # Parse JSON lines output
        results = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            try:
                v = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Extract duration (in seconds from yt-dlp)
            duration_sec = v.get("duration")
            if duration_sec:
                duration_min = duration_sec / 60
                # Format as MM:SS or HH:MM:SS
                if duration_sec >= 3600:
                    duration_str = f"{int(duration_sec // 3600)}:{int((duration_sec % 3600) // 60):02d}:{int(duration_sec % 60):02d}"
                else:
                    duration_str = f"{int(duration_sec // 60)}:{int(duration_sec % 60):02d}"
            else:
                duration_min = None
                duration_str = ""

            # Filter by duration if specified
            if duration_min is not None:
                if min_dur and duration_min < min_dur:
                    continue
                if max_dur and duration_min > max_dur:
                    continue
            elif min_dur or max_dur:
                # Skip videos without duration when filtering
                continue

            # Filter by date if specified (upload_date is YYYYMMDD string)
            raw_upload_date = v.get("upload_date", "")
            if date_from or date_to:
                if not raw_upload_date:
                    continue  # Skip videos without upload date when filtering
                if date_from and raw_upload_date < date_from:
                    continue
                if date_to and raw_upload_date > date_to:
                    continue

            video_id = v.get("id", "")
            url = v.get("url") or f"https://www.youtube.com/watch?v={video_id}"

            # Get view count - yt-dlp returns it as integer
            view_count = v.get("view_count")
            if view_count:
                if view_count >= 1_000_000_000:
                    views = f"{view_count / 1_000_000_000:.1f}B views"
                elif view_count >= 1_000_000:
                    views = f"{view_count / 1_000_000:.1f}M views"
                elif view_count >= 1_000:
                    views = f"{view_count / 1_000:.1f}K views"
                else:
                    views = f"{view_count} views"
            else:
                views = ""

            # Format upload date from YYYYMMDD to YYYY-MM-DD
            upload_date_fmt = ""
            if raw_upload_date and len(raw_upload_date) == 8:
                upload_date_fmt = f"{raw_upload_date[:4]}-{raw_upload_date[4:6]}-{raw_upload_date[6:8]}"

            results.append({
                "url": url,
                "title": v.get("title", ""),
                "channel": v.get("channel") or v.get("uploader", ""),
                "duration": duration_str,
                "views": views,
                "date": upload_date_fmt,
            })

            if len(results) >= num:
                break

        logger.info("yt-dlp fast search found %d videos", len(results))
        return results if results else None

    except subprocess.TimeoutExpired:
        logger.warning("yt-dlp search timed out")
        return None
    except FileNotFoundError:
        logger.debug("yt-dlp not found")
        return None
    except Exception as e:
        logger.warning("yt-dlp search failed: %s", e)
        return None


def _search_youtube_fast(
    keyword: str,
    num: int = 10,
    min_duration: int | None = None,
    max_duration: int | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict] | None:
    """Fast YouTube search using youtube-search-python (no browser needed).

    Note: youtube-search-python does not support date filtering directly.
    Date filtering is done post-search by parsing upload dates when available.

    Returns None if the library is not available or search fails.
    This is ~10x faster than Playwright-based search.
    """
    try:
        from youtubesearchpython import VideosSearch
    except ImportError:
        logger.debug("youtube-search-python not available, using Playwright")
        return None

    try:
        # Fetch more results to account for duration/date filtering
        has_filters = min_duration or max_duration or date_from or date_to
        fetch_num = num * 3 if has_filters else num
        search = VideosSearch(keyword, limit=min(fetch_num, 50))  # API limit is 50
        raw_results = search.result().get("result", [])

        results = []
        for v in raw_results:
            # Parse duration
            duration_str = v.get("duration", "")
            duration_min = parse_duration_to_minutes(duration_str)

            # Filter by duration if specified
            if duration_min is not None:
                if min_duration and duration_min < min_duration:
                    continue
                if max_duration and duration_min > max_duration:
                    continue
            elif min_duration or max_duration:
                # Skip videos without duration when filtering
                continue

            video_id = v.get("id", "")
            # Get published time (e.g., "2 days ago", "1 year ago")
            published_time = v.get("publishedTime", "")
            results.append({
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": v.get("title", ""),
                "channel": v.get("channel", {}).get("name", ""),
                "duration": duration_str,
                "views": v.get("viewCount", {}).get("short", ""),
                "date": published_time,
            })

            if len(results) >= num:
                break

        logger.info("Fast search found %d videos", len(results))
        return results if results else None

    except Exception as e:
        logger.warning("Fast search failed: %s, falling back to Playwright", e)
        return None


def parse_duration_to_minutes(duration_str: str) -> float | None:
    """Parse duration string like '3:45' or '1:23:45' to minutes."""
    if not duration_str:
        return None

    duration_str = duration_str.strip()
    parts = duration_str.split(":")

    try:
        if len(parts) == 2:  # MM:SS
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes + seconds / 60
        elif len(parts) == 3:  # HH:MM:SS
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return hours * 60 + minutes + seconds / 60
        else:
            return None
    except (ValueError, IndexError):
        return None


# Quality options for video download
QualityOption = Literal["best", "1080p", "720p", "480p", "360p", "audio"]

# Upload date filter options
UploadDateOption = Literal["hour", "today", "week", "month", "year", None]

# YouTube sp parameter values for upload date filters
UPLOAD_DATE_PARAMS = {
    "hour": "EgIIAQ%3D%3D",
    "today": "EgIIAg%3D%3D",
    "week": "EgIIAw%3D%3D",
    "month": "EgIIBA%3D%3D",
    "year": "EgIIBQ%3D%3D",
}

# Format strings for yt-dlp - prefer mp4/m4a over webm for compatibility
QUALITY_FORMATS = {
    "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
    "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480p": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]",
    "360p": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]",
    "audio": "bestaudio[ext=m4a]/bestaudio/best",
}


@dataclass
class YouTubeSearch:
    """YouTube video search automation.

    This class handles searching YouTube and extracting video information.

    Attributes:
        keyword: Search query string (required).
        num: Number of results to return (default: 10).
        output: JSON output path for results (optional).
        screenshot: Screenshot output path (optional).
        headless: Run browser in headless mode.
    """

    # CLI metadata (class variables)
    _cli_name: ClassVar[str] = "youtube-search"
    _cli_description: ClassVar[str] = "Search YouTube videos and get URLs"
    _cli_help: ClassVar[dict] = {
        "keyword": "Search keyword",
        "num": "Number of results to return",
        "output": "JSON output path for results",
        "screenshot": "Screenshot output path",
        "headless": "Run in headless mode",
        "min_duration": "Minimum video duration in minutes",
        "max_duration": "Maximum video duration in minutes",
        "upload_date": "Filter by upload date (hour, today, week, month, year)",
        "date_from": "Custom date range start (YYYYMMDD format, e.g., 20240101)",
        "date_to": "Custom date range end (YYYYMMDD format, e.g., 20241231)",
    }
    _cli_choices: ClassVar[dict] = {
        "upload_date": ["hour", "today", "week", "month", "year"],
    }
    _cli_short: ClassVar[dict] = {
        "num": "n",
        "output": "o",
        "screenshot": "s",
        "min_duration": "min",
        "max_duration": "max",
        "upload_date": "t",
        "date_from": "df",
        "date_to": "dt",
    }

    # Instance fields (order matters for positional args)
    keyword: str
    num: int = 10
    output: str | None = None
    screenshot: str | None = None
    headless: bool = True
    min_duration: int | None = None
    max_duration: int | None = None
    upload_date: str | None = None
    date_from: str | None = None  # YYYYMMDD format
    date_to: str | None = None    # YYYYMMDD format

    def execute(self, page: Page) -> list[dict]:
        """Execute the YouTube search on the given page.

        Args:
            page: Playwright page instance.

        Returns:
            List of video dictionaries with url, title, channel, duration, views.
        """
        # Build search URL with duration filter in URL params (more reliable than UI clicking)
        encoded_keyword = urllib.parse.quote(self.keyword)
        search_url = f"https://www.youtube.com/results?search_query={encoded_keyword}"

        # Add upload date filter via URL parameter (sp parameter)
        # These take priority over duration filters (can't easily combine in YouTube)
        if self.upload_date and self.upload_date in UPLOAD_DATE_PARAMS:
            search_url += f"&sp={UPLOAD_DATE_PARAMS[self.upload_date]}"
            logger.info("Using YouTube URL filter: upload date = %s", self.upload_date)
        else:
            # Add duration filter via URL parameter (sp parameter)
            # Short (< 4 min): EgIYAQ%3D%3D
            # Medium (4-20 min): EgIYAw%3D%3D
            # Long (> 20 min): EgIYAg%3D%3D
            min_dur = int(self.min_duration) if self.min_duration else None
            max_dur = int(self.max_duration) if self.max_duration else None
            if min_dur and max_dur:
                if min_dur >= 4 and max_dur <= 20:
                    search_url += "&sp=EgIYAw%3D%3D"  # Medium (4-20 min)
                    logger.info("Using YouTube URL filter: 4-20 minutes")
                elif max_dur <= 4:
                    search_url += "&sp=EgIYAQ%3D%3D"  # Short (< 4 min)
                    logger.info("Using YouTube URL filter: < 4 minutes")
                elif min_dur >= 20:
                    search_url += "&sp=EgIYAg%3D%3D"  # Long (> 20 min)
                    logger.info("Using YouTube URL filter: > 20 minutes")

        logger.info("Searching YouTube: '%s'", self.keyword)
        page.goto(search_url)
        self._wait_for_load(page)

        # Accept cookies if prompted
        try:
            accept_btn = page.locator("button:has-text('Accept all')").first
            if accept_btn.is_visible(timeout=1000):
                accept_btn.click()
                time.sleep(0.3)
        except Exception:
            pass

        # Extract videos, scrolling as needed to find enough matching results
        results = self._extract_videos_with_scroll(page)

        if self.screenshot:
            page.screenshot(path=self.screenshot, full_page=True)
            logger.info("Screenshot saved: %s", self.screenshot)

        if self.output:
            with open(self.output, "w") as f:
                json.dump(results, f, indent=2)
            logger.info("Results saved: %s", self.output)

        return results

    def _extract_videos_with_scroll(self, page: Page) -> list[dict]:
        """Extract videos, scrolling as needed to find enough matching results."""
        results = []
        seen_urls = set()
        max_scrolls = 20  # Increase scrolls since we filter by duration
        scroll_count = 0

        # Convert duration filters to int
        min_dur = int(self.min_duration) if self.min_duration else None
        max_dur = int(self.max_duration) if self.max_duration else None

        while len(results) < self.num and scroll_count < max_scrolls:
            # Extract from current view
            new_results = self._extract_videos(page, seen_urls)

            # Filter by duration if specified
            for video in new_results:
                duration_min = parse_duration_to_minutes(video.get("duration", ""))
                if duration_min is None:
                    continue  # Skip videos without duration

                # Check min duration
                if min_dur and duration_min < min_dur:
                    logger.debug("  Skipped (too short: %.1f min): %s", duration_min, video["title"][:40])
                    continue

                # Check max duration
                if max_dur and duration_min > max_dur:
                    logger.debug("  Skipped (too long: %.1f min): %s", duration_min, video["title"][:40])
                    continue

                results.append(video)
                logger.info("  [%d/%d] %.1f min: %s", len(results), self.num, duration_min, video["title"][:50])

                if len(results) >= self.num:
                    break

            if len(results) >= self.num:
                break

            # Scroll for more
            page.evaluate("window.scrollBy(0, window.innerHeight)")
            time.sleep(0.3)
            scroll_count += 1

        return results[:self.num]

    def _extract_videos(self, page: Page, seen_urls: set | None = None) -> list[dict]:
        """Extract video information from search results using fast JS evaluation."""
        if seen_urls is None:
            seen_urls = set()

        # Extract all video data in one JS call (much faster than multiple Playwright calls)
        videos_data = page.evaluate("""
            () => {
                const videos = [];
                document.querySelectorAll('ytd-video-renderer').forEach(elem => {
                    const titleLink = elem.querySelector('a#video-title');
                    if (!titleLink) return;

                    const href = titleLink.getAttribute('href');
                    const title = titleLink.getAttribute('title') || titleLink.textContent;

                    if (!href || !href.includes('/watch?v=')) return;

                    const channelElem = elem.querySelector('ytd-channel-name a');
                    const durationElem = elem.querySelector('span.ytd-thumbnail-overlay-time-status-renderer');
                    const metadataSpans = elem.querySelectorAll('#metadata-line span');

                    // Date is usually the second span in metadata-line (e.g., "2 days ago")
                    const date = metadataSpans.length > 1 ? metadataSpans[1].textContent.trim() : '';

                    videos.push({
                        href: href,
                        title: title ? title.trim() : '',
                        channel: channelElem ? channelElem.textContent.trim() : '',
                        duration: durationElem ? durationElem.textContent.trim() : '',
                        views: metadataSpans.length > 0 ? metadataSpans[0].textContent.trim() : '',
                        date: date
                    });
                });
                return videos;
            }
        """)

        logger.info("Found %d video elements", len(videos_data))

        results = []
        for v in videos_data:
            href = v.get("href", "")
            if not href or href in seen_urls:
                continue

            seen_urls.add(href)
            url = f"https://www.youtube.com{href}" if href.startswith("/") else href

            results.append({
                "url": url,
                "title": v.get("title", ""),
                "channel": v.get("channel", ""),
                "duration": v.get("duration", ""),
                "views": v.get("views", ""),
                "date": v.get("date", ""),
            })

        return results

    def run(self) -> list[dict]:
        """Run the complete search with browser management.

        Uses a 3-tier fallback strategy:
        1. yt-dlp ytsearch (fastest, ~1.5s, no browser)
        2. youtube-search-python (fast, ~2-3s, no browser)
        3. Playwright browser (slowest, ~6-10s, most reliable)
        """
        date_info = ""
        if self.date_from or self.date_to:
            date_info = f", date={self.date_from or 'any'} to {self.date_to or 'any'}"
        logger.info("Starting YouTube search for: '%s' (num=%d, duration=%s-%s min%s)",
                    self.keyword, self.num,
                    self.min_duration or "any", self.max_duration or "any", date_info)

        # Try fastest method first: yt-dlp ytsearch
        results = _search_ytdlp_fast(
            self.keyword,
            num=self.num,
            min_duration=self.min_duration,
            max_duration=self.max_duration,
            date_from=self.date_from,
            date_to=self.date_to,
        )
        if results:
            self._save_results(results)
            return results

        # Fallback to youtube-search-python
        results = _search_youtube_fast(
            self.keyword,
            num=self.num,
            min_duration=self.min_duration,
            max_duration=self.max_duration,
            date_from=self.date_from,
            date_to=self.date_to,
        )
        if results:
            self._save_results(results)
            return results

        # Final fallback: Playwright browser
        logger.info("Fast search unavailable, using Playwright browser")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=self.headless,
                args=["--start-maximized"] if not self.headless else [],
            )
            context = browser.new_context(no_viewport=True) if not self.headless else browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

            try:
                results = self.execute(page)
                logger.info("Found %d videos", len(results))
                return results
            finally:
                context.close()
                browser.close()

    def _save_results(self, results: list[dict]) -> None:
        """Save results to output file if specified."""
        if self.output:
            with open(self.output, "w") as f:
                json.dump(results, f, indent=2)
            logger.info("Results saved: %s", self.output)
        logger.info("Found %d videos", len(results))

    def _wait_for_load(self, page: Page, timeout: int = 5000) -> None:
        """Wait for page to fully load."""
        try:
            page.wait_for_load_state("domcontentloaded", timeout=timeout)
            # Wait for video elements to appear
            page.wait_for_selector("ytd-video-renderer", timeout=timeout)
        except Exception:
            pass

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

            if fld.type is bool or (hasattr(fld, 'type') and fld.type is bool):
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
    def from_args(cls, args) -> "YouTubeSearch":
        """Create instance from parsed args."""
        kwargs = {}
        for name in cls.__dataclass_fields__:
            if name.startswith("_"):
                continue
            if hasattr(args, name):
                kwargs[name] = getattr(args, name)
        return cls(**kwargs)


@dataclass
class YouTubeDownload:
    """YouTube video download using yt-dlp.

    This class handles downloading YouTube videos with quality options.
    Requires yt-dlp to be installed (uv add yt-dlp).

    Attributes:
        url: YouTube video URL or search query if --search is used.
        output_dir: Directory to save downloaded videos.
        quality: Video quality option.
        search: If True, treat url as search query and download first result.
        audio_only: Download audio only (mp3).
        num: Number of videos to download when searching (default: 1).
    """

    # CLI metadata (class variables)
    _cli_name: ClassVar[str] = "youtube-download"
    _cli_description: ClassVar[str] = "Download YouTube videos using yt-dlp"
    _cli_help: ClassVar[dict] = {
        "url": "YouTube URL or search query (with --search)",
        "output_dir": "Directory to save videos",
        "quality": "Video quality",
        "search": "Treat input as search query",
        "audio_only": "Download audio only (mp3)",
        "num": "Number of videos to download (with --search)",
        "headless": "Run browser in headless mode",
        "min_duration": "Minimum video duration in minutes",
        "max_duration": "Maximum video duration in minutes",
        "parallel": "Number of parallel downloads (default: 3)",
        "concurrent_fragments": "Concurrent fragment downloads per video (default: 4)",
        "date_from": "Custom date range start (YYYYMMDD format, e.g., 20240101)",
        "date_to": "Custom date range end (YYYYMMDD format, e.g., 20241231)",
    }
    _cli_choices: ClassVar[dict] = {
        "quality": ["best", "1080p", "720p", "480p", "360p", "audio"],
    }
    _cli_short: ClassVar[dict] = {
        "output_dir": "o",
        "quality": "q",
        "search": "s",
        "audio_only": "a",
        "num": "n",
        "min_duration": "min",
        "max_duration": "max",
        "parallel": "p",
        "concurrent_fragments": "N",
        "date_from": "df",
        "date_to": "dt",
    }

    # Instance fields
    url: str
    output_dir: str = "."
    quality: QualityOption = "best"
    search: bool = False
    audio_only: bool = False
    num: int = 1
    headless: bool = True
    min_duration: int | None = None
    max_duration: int | None = None
    parallel: int = 3
    concurrent_fragments: int = 8  # Higher = faster for DASH/HLS streams
    date_from: str | None = None  # YYYYMMDD format
    date_to: str | None = None    # YYYYMMDD format

    def run(self) -> list[str]:
        """Run the download and return list of downloaded files."""
        output_path = Path(self.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        urls_to_download = []

        # If search mode, find video URLs first
        if self.search:
            logger.info("Searching for: %s", self.url)

            # Try fastest method first: yt-dlp ytsearch (no browser needed)
            results = _search_ytdlp_fast(
                self.url,
                num=self.num,
                min_duration=self.min_duration,
                max_duration=self.max_duration,
                date_from=self.date_from,
                date_to=self.date_to,
            )

            # Fallback to youtube-search-python
            if not results:
                results = _search_youtube_fast(
                    self.url,
                    num=self.num,
                    min_duration=self.min_duration,
                    max_duration=self.max_duration,
                    date_from=self.date_from,
                    date_to=self.date_to,
                )

            # Final fallback to Playwright browser
            if not results:
                logger.info("Fast search unavailable, using Playwright browser")
                searcher = YouTubeSearch(
                    keyword=self.url,
                    num=self.num,
                    headless=self.headless,
                    min_duration=self.min_duration,
                    max_duration=self.max_duration,
                    date_from=self.date_from,
                    date_to=self.date_to,
                )
                results = searcher.run()

            if not results:
                logger.warning("No videos found for search query")
                return []

            urls_to_download = [r["url"] for r in results[:self.num]]
            logger.info("Downloading %d video(s) with %d parallel workers...", len(urls_to_download), self.parallel)
        else:
            urls_to_download = [self.url]

        downloaded_files = []

        # Use parallel downloads for multiple videos
        if len(urls_to_download) > 1 and self.parallel > 1:
            with ThreadPoolExecutor(max_workers=self.parallel) as executor:
                futures = {
                    executor.submit(self._download_single, url, output_path): url
                    for url in urls_to_download
                }
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        downloaded_files.append(result)
        else:
            # Single download or parallel=1
            for url in urls_to_download:
                result = self._download_single(url, output_path)
                if result:
                    downloaded_files.append(result)

        logger.info("Downloaded %d file(s) to %s", len(downloaded_files), output_path)
        return downloaded_files

    def _download_single(self, url: str, output_path: Path) -> str | None:
        """Download a single video with optimized speed settings."""
        logger.info("Downloading: %s", url)

        # Build yt-dlp command
        cmd = ["yt-dlp"]

        # Set format based on quality and audio_only
        if self.audio_only:
            cmd.extend(["-f", "bestaudio/best"])
            cmd.extend(["-x", "--audio-format", "mp3"])
        else:
            format_str = QUALITY_FORMATS.get(self.quality, "best")
            cmd.extend(["-f", format_str])
            cmd.extend(["--merge-output-format", "mp4"])

        # Output template
        output_template = str(output_path / "%(title)s.%(ext)s")
        cmd.extend(["-o", output_template])

        # Basic options
        cmd.extend([
            "--no-playlist",        # Don't download playlists
            "--progress",
            # Note: removed --restrict-filenames to preserve Unicode in filenames
        ])

        # Speed optimizations
        # Use native downloader with high concurrent fragments (best for YouTube DASH)
        # aria2c is slower for DASH streams that need merging
        cmd.extend([
            "-N", str(self.concurrent_fragments),  # Concurrent fragment downloads (best for DASH/HLS)
        ])

        # Additional speed optimizations
        cmd.extend([
            "--buffer-size", "64K",     # Larger buffer for better throughput
            "--http-chunk-size", "10M", # Larger chunks reduce overhead
            "--no-check-certificates",  # Skip cert verification (faster)
            "--no-mtime",               # Don't set mtime (faster)
        ])

        # Add URL at the end
        cmd.append(url)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,  # 10 minute timeout
            )

            if result.returncode == 0:
                # Try to find the downloaded file
                # yt-dlp prints the destination file
                for line in result.stdout.split("\n"):
                    if "Destination:" in line or "has already been downloaded" in line:
                        # Extract filename from output
                        match = re.search(r"Destination: (.+)$", line)
                        if match:
                            logger.info("Downloaded: %s", match.group(1))
                            return match.group(1)

                        match = re.search(r"\[download\] (.+) has already been downloaded", line)
                        if match:
                            logger.info("Already exists: %s", match.group(1))
                            return match.group(1)

                # If we can't find specific file, just report success
                logger.info("Download completed")
                return str(output_path)
            else:
                logger.error("Error: %s", result.stderr[:200])
                return None

        except subprocess.TimeoutExpired:
            logger.error("Download timed out")
            return None
        except FileNotFoundError:
            logger.error("yt-dlp not found. Install with: uv add yt-dlp")
            return None
        except Exception as e:
            logger.error("Error: %s", e)
            return None

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

            if fld.type is bool or (hasattr(fld, 'type') and fld.type is bool):
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
    def from_args(cls, args) -> "YouTubeDownload":
        """Create instance from parsed args."""
        kwargs = {}
        for name in cls.__dataclass_fields__:
            if name.startswith("_"):
                continue
            if hasattr(args, name):
                kwargs[name] = getattr(args, name)
        return cls(**kwargs)
