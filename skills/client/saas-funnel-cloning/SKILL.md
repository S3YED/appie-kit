---
name: saas-funnel-cloning
description: "Clone landing pages and funnels from SaaS builders (GoHighLevel, ClickFunnels, etc.) into standalone static HTML, then deploy to GitHub + Vercel. Covers extraction, reconstruction, and deployment."
version: 1.2.0
author: Ibrahim Ramzy (via Hermes Agent)
license: MIT
metadata:
  hermes:
    tags: [funnel, cloning, gohighlevel, landing-page, vercel, github, deployment]
    category: content
    related_skills: [web-design-pipeline, frontend-design, ui-ux-pro-max, popular-web-designs, building-ai-websites-that-dont-look-ai]
---

# SaaS Funnel Cloning

Clone a landing page or funnel from a SaaS builder (GoHighLevel, ClickFunnels, etc.) into a standalone HTML/CSS site and deploy it on GitHub + Vercel.

## When to use

- User gives you a URL to a GoHighLevel, ClickFunnels, or similar SaaS funnel preview
- User wants a "one-to-one clone" as static HTML on their own domain
- User wants to move away from the SaaS builder and iterate faster with voice/chat

## Workflow

### Step 1: Extract the page structure

Use the browser tool to visit the preview URL:

```
browser_navigate(url)
```

From the snapshot, identify:
- Layout structure (hero, sections, CTA, footer)
- All headings, text content, and button labels
- Image URLs from browser_get_images()
- Fonts from Google Fonts links in the page
- CSS custom properties / design tokens (colours, font families)

Also extract the raw HTML source with curl for design token extraction:

```
curl -sL '<URL>' -o source.html
grep -E '"\-\-(color|primary|secondary|headline|content|text-color|link-color)"' source.html
```

### Step 2: Download key assets

Use curl to download images from the CDN. Target the highest resolution available (r_1200 or higher). Save into `assets/` directory.

```
curl -sL '<CDN_URL>' -o assets/<name>.<ext>
```

Expected assets:
- logo.png (brand logo)
- hero-bg.png (hero background)
- ibrahim-hero.jpg (coach/trainer photo)
- favicon.jpg
- testimonial-bg.webp (testimonial backgrounds)
- feature-icon-*.png (feature section icons)
- result-*.jpg (before/after transformation photos)

### Step 3: Research conversion principles (coaching/fitness funnels)

If the funnel is for a coaching, fitness, or info-product vertical, research Russell Brunson's conversion frameworks before building:

- **DotCom Secrets**: Value Ladder (5 rungs), Hook-Story-Offer, The Secret Formula
- **Expert Secrets**: Attractive Character, Soap Opera Sequence, Application/Quiz Funnel
- **Traffic Secrets**: Traffic temperature determines the funnel entry page

Key principles to apply:
- One CTA per page -- eliminate navigation links that distract
- Hook-Story-Offer -- every section leads with emotion, proves with logic, closes with a CTA
- Price anchoring -- show the value wall (e.g. 2,497 value) before the price (e.g. 497)
- Real scarcity -- "I only take 10 new clients per month" not "limited time offer"
- Keep the loop open -- thank you pages say "being reviewed / being customised" not "confirmed"
- Qualify with questions -- 4-7 questions that both engage AND segment

If the user has given you an Exa API key and asked you to use Exa, search for design references and conversion research via Exa before building.

### Step 4: Reconstruct as static HTML

Build a single `index.html` with embedded CSS. Key requirements:

- **Pixel-fidelity first**: match the original layout, spacing, and hierarchy. Do not redesign unless the user explicitly asks for it.
- **Extract design tokens from the original**: CSS custom properties, font stacks, colours. Use them in your CSS.
- **Responsive**: mobile-first with breakpoints at 768px and 480px.
- **Local assets**: reference downloaded images from `assets/` directory.
- **No JS frameworks**: pure HTML + CSS. Use vanilla JS only for interactive elements (FAQ toggles, smooth scroll).
- **Three-column pricing grid** if it exists, with a featured/most-popular card that scales up slightly.
- **Scarcity elements**: spots counters, waitlist counts, urgency badges.
- **Social proof**: testimonial cards, result quotes, before/after metrics.
- **Footer disclaimers**: Facebook/Trademark disclaimers from the original.
- **Multi-step qualification form**: When the user wants an "Apply Now" flow, build a 5-step modal questionnaire:
  - Step 1: Goal (fat loss / muscle / health / confidence)
  - Step 2: Commitment level (days per week)
  - Step 3: Biggest struggle
  - Step 4: Self-rated commitment (1-10 -- scores hot leads)
  - Step 5: Contact details (name, email, phone)
  - Progress bar across all steps
  - Shake animation if an option is missed
  - Store form data in localStorage for tracking
- **Thank you page**: After form submission, show a thank you page that:
  - Says "being reviewed" not "confirmed" (keeps the loop open)
  - Has an urgency box ("your spot is not locked in yet")
  - Includes a calendar/booking embed placeholder
- **Funnel breakdown**: When the user asks for a "breakdown of where to go", deliver a structured map of every page/section and what happens at each step.

### Step 5: Set up Git and push to GitHub

```
cd /path/to/project
git init
git add -A
git commit -m "Initial commit: cloned funnel"

# Create GitHub repo
gh repo create <repo-name> --private --description "<description>"

# If you get "could not read Username" when pushing:
#   1. Run: gh auth setup-git
#   2. Or set remote URL with embedded token:
#      git remote set-url origin https://<username>:<token>@github.com/<username>/<repo>.git
#   3. Then push normally

git remote add origin https://github.com/<username>/<repo>.git
git branch -M main
git push -u origin main

# IMPORTANT: After the push, clean the remote URL to remove the token:
git remote set-url origin https://github.com/<username>/<repo>.git
```

### Step 6: Deploy to Vercel

Read the Vercel token from the .env file:

```
npm i -g vercel

# Deploy using the env-stored token
vercel --token "$(grep '^VERCEL_API_TOKEN=' ~/.hermes/.env | tail -1 | sed 's/.*=//')" --yes --prod

# The deploy URL appears in the output.
# Clean aliased URL will be: https://<project>.vercel.app
# Verify it's live:
curl -s -o /dev/null -w "%{http_code}" https://<project>.vercel.app/
```

Deliver the URL to the user with a summary of what was done.

## Pitfalls

- **Auth first**: Check GitHub auth status before trying to push. If not authenticated, give the user a device code. CRITICAL: `gh auth login` in PTY mode TIMES OUT while waiting for the user. Do not use pty mode for device code login. Instead use Option A or B below:
  - Option A: Have the user paste a GitHub personal access token, then use `echo "<token>" | gh auth login --with-token`
  - Option B: Run `gh auth login` in background mode (not pty) and give the user the device code. Wait for them to confirm before continuing.
- **git push authentication**: Even after `gh auth login`, git push may fail with "could not read Username". Fix: `gh auth setup-git` OR set the remote URL with the token embedded, then clean it after push.
- **Expired preview URLs**: SaaS preview links may expire. If the page comes back empty, re-navigate or ask for a fresh link.
- **GHL-generated HTML is bloated** (2.9MB+). Do not try to clean up the raw HTML. Extract the structure manually from the browser snapshot and rebuild from scratch.
- **Em dashes in the original content**: The user hates em dashes. Replace them with commas or periods during reconstruction.
- **Video embeds**: GHL previews may not show the actual video URL. Use a placeholder player element and flag it for the user to replace.
- **Testimonials section may have a "Load More" button**: In the clone, show all testimonials upfront (better UX for standalone pages).
- **PEP 668 (pip install fails)**: If pip refuses to install packages globally, create a venv first: `python3 -m venv /path/to/venv && /path/to/venv/bin/pip install <package>`

## Related skills

- `creative/humanizer` -- with `references/client-preferences.md` for user-specific communication rules
- `web-design-pipeline` -- for full animated multi-page builds
- `frontend-design` -- for design-first approach
- `ui-ux-pro-max` -- for design system decisions
- `github-auth` -- for GitHub auth setup