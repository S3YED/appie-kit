---
name: social-proof-widgets
description: Pull live reviews from Google Places API (and other platforms) and embed them as responsive sliders/carousels in Next.js landing pages with Google branding. Use when the user asks to add reviews, testimonials, or social proof sections to a site.
---

# Social Proof Widgets

Pull live third-party reviews and embed them as branded, responsive carousels on landing pages.

## Trigger Conditions
- User asks to add Google reviews, Trustpilot reviews, Facebook reviews to a website
- User wants a "What Clients Say" or testimonials section with live data
- User wants to integrate review platform data into a Next.js/React landing page

## Workflow

### 1. Fetch Reviews from Google Places API

```
# Step 1: Find the Place ID
curl -s "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=<business name> <city>&inputtype=textquery&fields=place_id,name,rating&key=<API_KEY>"

# Step 2: Pull reviews (max 5 returned by API)
curl -s "https://maps.googleapis.com/maps/api/place/details/json?place_id=<ID>&fields=name,rating,user_ratings_total,reviews&key=<API_KEY>&language=en&reviews_sort=newest"
```

### 2. Maximize Review Count

The Google Places API hard-limits to **5 reviews per call**. Multi-language calls return the same reviews translated — do not count them as unique. The only way to get more is:
- Scraping via the Google Maps web UI (often blocked by bot detection)
- Third-party services like Outscraper or SerpApi
- Accept the 5-review limit and supplement with the total count badge (`"59 Google reviews"`)

For most landing pages, 4-5 quality reviews in a slider + the total count badge is sufficient social proof.

### 3. Build the Slider Component

See `references/responsive-slider-pattern.md` for the full component template.

Key architectural decisions:
- Client component (`'use client'`) for motion/interactivity
- Framer Motion for card transitions (`initial/animate/exit`)
- Auto-advance via `useEffect` + `setInterval` (pause on hover via state)
- Manual prev/next buttons + dot indicators
- Google brand badge: Inline SVG G-logo + star row + count pill
- Profile pictures from Google photos array (use `unoptimized` to avoid Next.js image limits)
- External link to full Google Maps review page via CID

### 4. Mobile Optimization

Apply the standard responsive cascade on ALL elements:
```
mobile:  base classes (text-xs, p-5, w-8, h-8, round-2xl)
tablet+: md: prefix   (md:text-sm, md:p-10, md:w-10, md:h-10, md:rounded-3xl)
desktop: lg: prefix   (when needed)
```

Every visual element scales: badge size, star size, card padding, arrow buttons, profile photo, section padding, heading font size.

### 5. Deploy

Push to GitHub → Vercel auto-deploys. Verify at preview URL. Test at 375px, 768px, and 1440px.

## Pitfalls

- **API returns only 5 reviews**: The Google Places API does not support pagination for reviews. Multi-language calls (`language=nl`, `language=de`) return the same 5 reviews translated — filter by unique text to avoid duplicates.
- **Google Maps scraping blocks**: Headless browsers navigating to `google.com/maps` often get empty pages or captchas. The Places API is the reliable path.
- **`git reset --soft` with `--no-verify`**: When cherry-picking specific changes, a soft reset stages EVERYTHING from the remote HEAD. Untracked imported files (like `MetaEvents.tsx`) get left behind, causing build failures. Use `git cherry-pick` for surgical commits or double-check `git status` for missing imports.
- **Profile photo URLs**: Google's `profile_photo_url` returns Google CDN URLs. Set `unoptimized={true}` on Next.js `Image` to avoid domain allowlist issues.