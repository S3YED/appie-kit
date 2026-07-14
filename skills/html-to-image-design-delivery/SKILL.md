---
name: html-to-image-design-delivery
description: Convert HTML design artifacts to image deliverables (PNG) when image generation APIs are unavailable. Covers magazine covers, posters, social graphics, and any fixed-size visual asset built as HTML and exported via Playwright screenshot.
version: 1.0.0
author: agent
metadata:
  hermes:
    tags: [design, html, screenshot, playwright, image-delivery, coverage, magazine, poster]
    related_skills: [claude-design, popular-web-designs, ckm:design]
---

# HTML-to-Image Design Delivery

Use this skill when the user asks for a **visual design deliverable** (magazine cover, poster, social graphic, flyer, quote card, announcement visual) and image generation tools (FAL, Higgsfield, etc.) are unavailable, unconfigured, or inappropriate for the task.

The technique: build the design as a self-contained HTML page, then screenshot it with Playwright to deliver a PNG image to the user.

## When To Use

- User sends a photo (selfie, portrait, product shot) and asks "make this a magazine cover" / "turn this into a poster" / "make it look like [Forbes/Time/Vogue/etc.]"
- Any fixed-size editorial layout with text overlays on a photo
- Branded quote cards, announcements, social media graphics
- Fixed-size banners where HTML precision is easier than prompt-only image gen
- Image gen is not configured (FAL_KEY missing, no Higgsfield account, etc.)

## When NOT To Use

- The user wants a generic text-to-image (no specific brand layout) — let them know image gen is unconfigured first
- The deliverable needs to be interactive or animated (use plain HTML delivery instead)
- A video or reel is needed (use branded-reel-pipeline or short-form-video-production)

## The Workflow

### 1. Build the HTML artifact

Create a self-contained HTML file with:

- **User photo embedded as base64 data URI** — encode the image first:
  ```python
  import base64
  with open('photo.jpg', 'rb') as f:
      b64 = base64.b64encode(f.read()).decode()
  ```
  Then in HTML: `<img src="data:image/jpeg;base64,{b64}">`

- **CSS overlays and gradients** — use `position: absolute` overlay divs with background gradients (e.g., `linear-gradient(180deg, rgba(0,0,0,0.55) 0%, ... rgba(0,0,0,0.4) 100%)`) so text stays readable over the photo.

- **Typographic treatment** — use Google Fonts for brand-relevant typography (Playfair Display for editorial/Forbes-style serif, Inter for modern sans). Import via `@import url(...)` in CSS.

- **Fixed dimensions** — wrap everything in a container div with exact pixel dimensions matching the intended output (e.g., `width: 720px; height: 1280px` for portrait magazine covers).

- **All visual elements as CSS** — mastheads, accent bars, cover lines, barcodes, diamonds, price tags, taglines. No images needed except the user photo.

### 2. Serve locally (required for base64 images)

Browser security blocks file:// protocol from loading base64 images in some environments. Always serve via HTTP:

```bash
python3 -m http.server <port> --bind 127.0.0.1
```

Run this in the directory containing your HTML file.

### 3. Screenshot with Playwright

Install Playwright in a temp directory:

```bash
mkdir -p /tmp/screenshot && cd /tmp/screenshot
npm init -y && npm install playwright
```

Create a screenshot script:

```js
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 720, height: 1280 } });
  await p.goto('http://127.0.0.1:<port>/<file>.html', {
    waitUntil: 'networkidle',
    timeout: 15000
  });
  await p.screenshot({ path: '/output/path.png', fullPage: true });
  await b.close();
  console.log('DONE');
})();
```

Run it: `node screenshot.js`

### 4. Deliver the image

Send the resulting PNG to the user via `MEDIA:/absolute/path/to/output.png`.

### 5. Clean up

- Kill the HTTP server
- Remove temp npm install directory

## Magazine Cover Templates

### Forbes-style layout
- **Masthead**: Playfair Display, 900 weight, ~72px, letter-spacing 14px, white with text-shadow
- **Subhead**: "The Creator Economy Issue" or similar, Inter 300, 11px, letter-spacing 6px
- **Red accent bar**: 80px wide, 2px height, #e60000
- **Diamond shape**: 14x14px rotated 45deg with 2px white border
- **Top cover line**: "EXCLUSIVE · [MONTH YEAR]" in small caps
- **Main headline**: Inter 900, 58px, white, -1px letter-spacing — punchy, aspirational
- **Subheadline**: Inter 300, 22px, semi-transparent white
- **Cover lines**: 3-4 bullet-style lines on bottom-left, white, ~16px
- **Barcode area**: repeating-linear-gradient barcode, "$7.99 US/CAN" price tag
- **Tagline bottom-left**: "forbes.com · @handle"

### General layout rules
- 720x1280px portrait (standard phone-screen portrait ratio)
- Gradient overlay: dark at top (for logo visibility) → semi-transparent middle → dark at bottom (for text readability)
- Center author photo as main cover image
- Light text on the dark overlay
- Use `box-shadow` on the cover itself for a physical magazine feel

## Pitfalls

- **Always serve via HTTP** — file:// with base64 images causes blank renders in headless browsers.
- **Match viewport to output** — set `{ viewport: { width, height } }` to the exact pixel dimensions of the intended output.
- **Use `waitUntil: 'networkidle'`** — ensures Google Fonts and images fully load before the screenshot fires.
- **Check the Playwright install path** — Playwright chromium needs to be downloaded first (`npx playwright install chromium`). If that's already done in a system cache, `npm install playwright` picks it up automatically.
- **Clean up after yourself** — HTTP server and temp npm installs consume disk space.
- **Let the user know** image gen wasn't available and you used HTML→screenshot instead, so they understand why it's not a "real" magazine cover.
- **Don't use too many Google Fonts** — each import adds load time. Stick to 1-2 families max.