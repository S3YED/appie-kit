# Browser Automation Script

A command-line tool for browser automation using Playwright with Chrome/Edge support and authentication persistence.

## Installation

Dependencies are managed via `pyproject.toml`. Run commands with:
```bash
cd .claude/skills/browser-use/scripts
uv run browser.py <command> [options]
```

## Commands

### Quick Reference

| Command | Description |
|---------|-------------|
| `create-login` | Save login session for reuse |
| `accounts` | List saved accounts |
| `goto` | Navigate to URL |
| `screenshot` | Take screenshot |
| `text` | Extract text content |
| `links` | Extract all links |
| `pdf` | Save page as PDF |
| `click` | Click an element |
| `fill` | Fill input field |
| `extract` | Extract attribute from elements |
| `download` | Download file by clicking |
| `upload` | Upload files |
| `download-images` | Download images from src |
| `download-from-gallery` | Download from click-to-reveal galleries |
| `google-image` | Search & download images (DuckDuckGo/Google) |
| `youtube-search` | Search YouTube and get video URLs |
| `youtube-download` | Download YouTube videos using yt-dlp |
| `tiktok-login` | Login to TikTok and save session |
| `tiktok-search` | Search TikTok videos by keyword/hashtag |
| `tiktok-download` | Download TikTok videos using yt-dlp |

### `create-login` - Save Login Session

Opens a browser for manual login and saves the session for later use. Uses Chrome with stealth mode to bypass automation detection (works with Google, etc.).

```bash
uv run browser.py create-login <url> --account <name> [options]
```

**Arguments:**
- `url` - URL to open for login
- `--account, -a` - Account name to save as (required)
- `--wait, -w` - Seconds to wait for login (default: 120)
- `--channel, -c` - Browser: `chrome`, `msedge`, `chromium` (default: chrome)

**Example:**
```bash
uv run browser.py create-login https://gemini.google.com/app --account google --wait 180
```

### `accounts` - List Saved Accounts

```bash
uv run browser.py accounts
```

### `goto` - Navigate to URL

Navigate to a URL and return page content.

```bash
uv run browser.py goto <url> [options]
```

**Options:**
- `--screenshot, -s` - Save screenshot to file
- `--no-headless` - Show browser window
- `--wait, -w` - Extra wait time in seconds after page load
- `--account, -a` - Use saved account for authentication

**Example:**
```bash
uv run browser.py goto https://gemini.google.com/app --account google --screenshot output.png
```

### `screenshot` - Take Screenshot

```bash
uv run browser.py screenshot <url> [options]
```

**Options:**
- `--output, -o` - Output file (default: screenshot.png)
- `--no-full-page` - Capture viewport only instead of full page
- `--wait, -w` - Extra wait time in seconds after page load
- `--account, -a` - Use saved account for authentication

**Example:**
```bash
uv run browser.py screenshot https://example.com -o page.png --wait 2
```

### `text` - Extract Text

Extract text content from a page using CSS selector.

```bash
uv run browser.py text <url> [options]
```

**Options:**
- `--selector, -s` - CSS selector (default: body)

**Example:**
```bash
uv run browser.py text https://example.com --selector "h1"
```

### `links` - Extract Links

Extract all links from a page as JSON.

```bash
uv run browser.py links <url>
```

### `pdf` - Save as PDF

Save a page as PDF.

```bash
uv run browser.py pdf <url> [options]
```

**Options:**
- `--output, -o` - Output file (default: page.pdf)

### `click` - Click Element

Click an element on a page.

```bash
uv run browser.py click <url> <selector> [options]
```

**Options:**
- `--wait, -w` - Wait time after click (default: 1)
- `--screenshot, -s` - Save screenshot after click
- `--button, -b` - Mouse button: `left`, `right`, `middle`
- `--dblclick` - Double click
- `--shift` - Hold Shift while clicking
- `--ctrl` - Hold Control while clicking
- `--force` - Force click even if element is obscured
- `--no-headless` - Show browser window
- `--account, -a` - Use saved account

### `fill` - Fill Input Field

Fill an input field and optionally press a key.

```bash
uv run browser.py fill <url> <selector> <value> [options]
```

**Options:**
- `--press, -p` - Key to press after filling (e.g., `Enter`)
- `--screenshot, -s` - Save screenshot after action
- `--wait, -w` - Extra wait time after pressing key
- `--no-headless` - Show browser window
- `--account, -a` - Use saved account

**Example:**
```bash
uv run browser.py fill "https://google.com" "input[name=q]" "search term" --press Enter
```

### `extract` - Extract Attribute

Extract attribute value(s) from element(s).

```bash
uv run browser.py extract <url> <selector> [options]
```

**Options:**
- `--attr` - Attribute to extract (default: `src`). Use `text` for text content.
- `--all` - Extract from all matching elements
- `--no-headless` - Show browser window
- `--account, -a` - Use saved account

### `download` - Download File

Download a file by clicking an element that triggers download.

```bash
uv run browser.py download <url> <selector> [options]
```

**Options:**
- `--output-dir, -o` - Directory to save file (default: `.`)
- `--account, -a` - Use saved account
- `--timeout, -t` - Download timeout in ms (default: 30000)

### `upload` - Upload Files

Upload files to a page using a file input element.

```bash
uv run browser.py upload <url> <selector> <files...> [options]
```

**Options:**
- `--submit, -s` - CSS selector of submit button
- `--account, -a` - Use saved account

### `upload-chooser` - Upload via File Chooser

Upload files via file chooser dialog (for dynamic inputs).

```bash
uv run browser.py upload-chooser <url> <trigger> <files...> [options]
```

---

## Image Download Commands

### `download-images` - Download from src

Download images directly from `src` attribute.

```bash
uv run browser.py download-images <url> <selector> [options]
```

**Options:**
- `--num, -n` - Number of images (default: 5)
- `--output-dir, -o` - Directory to save images
- `--no-headless` - Show browser window
- `--account, -a` - Use saved account

### `download-from-gallery` - Download from Gallery (Optimized)

Download full-size images from click-to-reveal galleries. **Optimized for Google Images with 19x faster extraction.**

```bash
uv run browser.py download-from-gallery <url> <thumb_selector> <full_selector> [options]
```

**Arguments:**
- `url` - Gallery page URL
- `thumb_selector` - CSS selector for thumbnails
- `full_selector` - CSS selector for full-size image after click

**Options:**
- `--num, -n` - Number of images (default: 5)
- `--output-dir, -o` - Directory to save images
- `--no-headless` - Show browser window
- `--account, -a` - Use saved account

**Example - Google Images:**
```bash
# Download 100 large images of "keyword"
uv run browser.py download-from-gallery \
  "https://www.google.com/search?q=keyword&tbm=isch&tbs=isz:l" \
  "div[data-id] img" \
  "img[jsname='kn3ccd']" \
  -n 100 \
  -o ~/Downloads \
  -a myaccount
```

**Performance:**
| Method | Time for 20 images | Time for 100 images |
|--------|-------------------|---------------------|
| Click-based | ~110 seconds | N/A |
| Fast regex extraction | ~5.7 seconds | ~15 seconds |
| **DuckDuckGo (no browser)** | **~9 seconds** | **~19 seconds** |

### `google-image` - Search and Download Images

Search images using DuckDuckGo (fastest, no browser) or Google Images with tiered fallback.

```bash
uv run browser.py google-image <keyword> [options]
```

**Arguments:**
- `keyword` - Search keyword

**Options:**
- `--account, -a` - Account name for Google authentication (optional, not needed for DuckDuckGo)
- `--size, -s` - Size filter: `4k`, `fullhd`, `Large`, `Medium`, `Icon` (default: Large)
  - `4k` - 3840px minimum dimension
  - `fullhd` - 1920px minimum dimension
  - `Large` - 1000px minimum dimension
  - `Medium` - 400px minimum dimension
  - `Icon` - No minimum
- `--download, -n` - Number of images to download (default: 0 = no download)
- `--download-dir, -o` - Directory to save downloaded images (default: ~/Downloads)
- `--source, -S` - Image source: `auto`, `duckduckgo`, `google` (default: auto)
- `--output, -O` - Screenshot output path
- `--no-headless` - Show browser window
- `--keep-open, -k` - Keep browser open for N seconds
- `--workers, -w` - Number of parallel download workers (default: 10)
- `--time-range, -t` - Time range filter: `Day`, `Week`, `Month`, `Year`
- `--date-from, -df` - Custom date range start (YYYYMMDD format) - Google only
- `--date-to, -dt` - Custom date range end (YYYYMMDD format) - Google only

**Examples:**
```bash
# DuckDuckGo mode - fastest, no browser needed
uv run browser.py google-image "landscape wallpaper" -n 100 -o ~/Downloads

# DuckDuckGo with size filter
uv run browser.py google-image "nature" -n 50 -o ~/Downloads -S duckduckgo -s Large

# Download 4K images (3840px+ minimum)
uv run browser.py google-image "wallpaper" -n 20 -o ~/Downloads -s 4k

# Download FullHD images (1920px+ minimum)
uv run browser.py google-image "wallpaper" -n 50 -o ~/Downloads -s fullhd

# Google mode - requires account
uv run browser.py google-image "keyword" -a myaccount -n 50 -o ~/Downloads -S google

# Auto mode (default) - tries DuckDuckGo first, falls back to Google
uv run browser.py google-image "keyword" -n 100 -o ~/Downloads

# DuckDuckGo with time range filter
uv run browser.py google-image "news" -n 50 -o ~/Downloads -S duckduckgo -t Day

# Google with custom date range (YYYYMMDD format)
uv run browser.py google-image "event photos" -a myaccount -n 50 -o ~/Downloads -S google -df 20240601 -dt 20240630
```

**Source Options:**
| Option | Browser | Speed | Use Case |
|--------|---------|-------|----------|
| `duckduckgo` | No | ~2-3s search | Default, fastest |
| `google` | Yes | ~8-15s search | More results, needs account |
| `auto` | Maybe | Varies | DuckDuckGo first, Google fallback |

---

## YouTube Commands

### `youtube-search` - Search YouTube Videos

Search YouTube and get video information as JSON with optional duration filtering.

```bash
uv run browser.py youtube-search <keyword> [options]
```

**Arguments:**
- `keyword` - Search query

**Options:**
- `--num, -n` - Number of results to return (default: 10)
- `--output, -o` - JSON output path for results
- `--screenshot, -s` - Screenshot output path
- `--min-duration, -min` - Minimum video duration in minutes
- `--max-duration, -max` - Maximum video duration in minutes
- `--upload-date, -t` - Filter by upload date: `hour`, `today`, `week`, `month`, `year`
- `--date-from, -df` - Custom date range start (YYYYMMDD format, e.g., 20240101)
- `--date-to, -dt` - Custom date range end (YYYYMMDD format, e.g., 20241231)
- `--no-headless` - Show browser window

**Example:**
```bash
# Search and display results
uv run browser.py youtube-search "python tutorial" -n 5

# Save results to JSON
uv run browser.py youtube-search "lofi music" -n 20 -o results.json

# Take screenshot of search results
uv run browser.py youtube-search "coding music" -s search.png

# Search with duration filter (4-20 minutes only)
uv run browser.py youtube-search "lofi music" -n 10 -min 4 -max 20

# Search videos from the last week
uv run browser.py youtube-search "news" -n 10 -t week

# Search videos from a custom date range
uv run browser.py youtube-search "tutorial" -n 10 -df 20240101 -dt 20241231
```

**Output Format:**
```json
[
  {
    "url": "https://www.youtube.com/watch?v=...",
    "title": "Video Title",
    "channel": "Channel Name",
    "duration": "10:30",
    "views": "1.2M views",
    "date": "2024-12-01"
  }
]
```

### `youtube-download` - Download YouTube Videos

Download YouTube videos using yt-dlp with quality and duration options.

```bash
uv run browser.py youtube-download <url> [options]
```

**Arguments:**
- `url` - YouTube video URL or search query (with `--search`)

**Options:**
- `--output_dir, -o` - Directory to save videos (default: `.`)
- `--quality, -q` - Video quality: `best`, `1080p`, `720p`, `480p`, `360p`, `audio` (default: best)
- `--search, -s` - Treat input as search query instead of URL
- `--audio_only, -a` - Download audio only as MP3
- `--num, -n` - Number of videos to download with `--search` (default: 1)
- `--min-duration, -min` - Minimum video duration in minutes (with `--search`)
- `--max-duration, -max` - Maximum video duration in minutes (with `--search`)
- `--date-from, -df` - Custom date range start (YYYYMMDD format, with `--search`)
- `--date-to, -dt` - Custom date range end (YYYYMMDD format, with `--search`)
- `--parallel, -p` - Number of parallel downloads (default: 3)
- `--concurrent-fragments, -N` - Concurrent fragment downloads per video (default: 8)

**Examples:**
```bash
# Download single video
uv run browser.py youtube-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o ./videos

# Download with specific quality
uv run browser.py youtube-download "https://youtube.com/watch?v=..." -q 720p -o ./videos

# Download audio only
uv run browser.py youtube-download "https://youtube.com/watch?v=..." -a -o ./music

# Search and download (combines search + download)
uv run browser.py youtube-download "python tutorial" --search -o ./videos

# Search and download multiple videos
uv run browser.py youtube-download "lofi music" --search -n 5 -o ./music

# Search and download with duration filter (4-20 min videos only)
uv run browser.py youtube-download "lofi music" --search -n 5 -min 4 -max 20 -o ./music

# Search and download videos from a date range
uv run browser.py youtube-download "tutorial" --search -n 5 -df 20240101 -dt 20241231 -o ./videos
```

**Quality Options:**
| Option | Description |
|--------|-------------|
| `best` | Best available quality (default) |
| `1080p` | 1080p or lower |
| `720p` | 720p or lower |
| `480p` | 480p or lower |
| `360p` | 360p or lower |
| `audio` | Best audio only |

---

## TikTok Commands

**IMPORTANT:** TikTok heavily blocks headless browsers. Use `--no-headless` for search operations.

### `tiktok-login` - Login and Save Session

Login to TikTok interactively and save the session for authenticated operations.

```bash
uv run browser.py tiktok-login --account <name> [options]
```

**Options:**
- `--account, -a` - Account name to save session as (required)
- `--wait, -w` - Seconds to wait for login (default: 120)

**Example:**
```bash
# Basic login
uv run browser.py tiktok-login -a mytiktok

# Extended wait time for complex login (2FA, etc.)
uv run browser.py tiktok-login -a mytiktok -w 180
```

### `tiktok-search` - Search TikTok Videos

Search TikTok videos by keyword or hashtag.

```bash
uv run browser.py tiktok-search <keyword> [options]
```

**Arguments:**
- `keyword` - Search keyword or hashtag (e.g., `"funny cats"` or `"#dance"`)

**Options:**
- `--num, -n` - Number of results to return (default: 10)
- `--output, -o` - JSON output path for results
- `--account, -a` - Account name for authenticated search
- `--no-headless` - Show browser window (**recommended** for TikTok)

**Examples:**
```bash
# Basic search (use --no-headless for best results)
uv run browser.py tiktok-search "funny cats" -n 10 --no-headless

# Search by hashtag
uv run browser.py tiktok-search "#dance" -n 5 --no-headless

# Search with saved account (better results)
uv run browser.py tiktok-search "cooking" -n 10 -a mytiktok --no-headless

# Save results to JSON
uv run browser.py tiktok-search "music" -n 20 -o results.json --no-headless
```

**Output Format:**
```json
[
  {
    "url": "https://www.tiktok.com/@user/video/123456789",
    "title": "Video description...",
    "author": "username",
    "views": "1.2M",
    "likes": "50K",
    "date": "2d ago"
  }
]
```

### `tiktok-download` - Download TikTok Videos

Download TikTok videos using yt-dlp.

```bash
uv run browser.py tiktok-download <url> [options]
```

**Arguments:**
- `url` - TikTok video URL or search query (with `--search`)

**Options:**
- `--output-dir, -o` - Directory to save videos (default: `~/Downloads`)
- `--search, -s` - Treat input as search query instead of URL
- `--num, -n` - Number of videos to download with `--search` (default: 5)
- `--account, -a` - Account name for authenticated operations
- `--parallel, -p` - Number of parallel downloads (default: 3)
- `--no-headless` - Show browser window for search

**Examples:**
```bash
# Download single video by URL
uv run browser.py tiktok-download "https://www.tiktok.com/@user/video/123456789" -o ~/Downloads

# Search and download videos
uv run browser.py tiktok-download "funny cats" --search -n 5 -o ~/Downloads --no-headless

# Search by hashtag and download
uv run browser.py tiktok-download "#cooking" --search -n 10 -o ~/Downloads --no-headless

# With parallel downloads
uv run browser.py tiktok-download "dance" --search -n 10 -o ~/Downloads -p 3 --no-headless

# With saved account
uv run browser.py tiktok-download "music" --search -n 5 -a mytiktok -o ~/Downloads --no-headless
```

---

## Authentication

Authentication data is stored in:
- `.auth/profiles/<account>/` - Browser profile (cookies, localStorage, etc.)
- `.auth/<account>.json` - Exported cookies

Both directories are automatically added to `.gitignore`.

### How it works

1. `create-login` opens Chrome with stealth flags to bypass automation detection
2. User logs in manually
3. Browser profile is saved to `.auth/profiles/<account>/`
4. Other commands use `launch_persistent_context` to reuse the saved profile

### Stealth Features

The script uses several techniques to avoid automation detection:
- Uses real Chrome browser (`channel="chrome"`)
- Disables automation flags (`--disable-blink-features=AutomationControlled`)
- Removes `--enable-automation` flag
- Uses persistent browser profile
