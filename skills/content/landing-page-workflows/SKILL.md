---
name: landing-page-workflows
description: Build, duplicate, and deploy landing pages for Ibrahim Ramzy's coaching funnels. Covers copy patterns, asset linking, Vercel deployment, and client-specific design preferences.
version: 1.2.0
tags: [landing-pages, vercel, copywriting, ibrahim, the-creed]
---

# Landing Page Workflows (Ibrahim Ramzy)

Build landing pages for The Creed / Health in Motion / giveaways. All pages use the same design system (navy + silver + royal blue, or gold for giveaways).

## Source of Truth

The master high-ticket landing page lives at:
- **Local:** `/root/ibrahim/index.html`
- **Live:** `https://thecreed-one.vercel.app`

The giveaway landing page lives at:
- **Local:** `/root/ibrahim-giveaway/index.html` (complete, with VSL section)
- **Live:** `https://ibrahim-giveaway.vercel.app` (primary, includes VSL, hero, steps, prizes, testimonials, typeform)
- **Legacy (inactive):** `https://creed-coaching-giveaway.vercel.app` (older copy without VSL — do not edit)
- **Motion upgrade (Next.js + motion/react):** `https://ibrahim-giveaway-v2.vercel.app` — deployed from `/root/ibrahim-giveaway-v2`. Source: `src/app/components/Sections.tsx`, `ConversionOptimizers.tsx`, `page.tsx`. Has all animations, conversion optimizers, Lucide icons, and premium design. NOT yet domain-swapped — lives on its own Vercel project.

Always duplicate from one of these sources. Never start from scratch.

## Duplication Pattern

```bash
cp -r /root/ibrahim /root/ibrahim-{project-name}
rm -rf /root/ibrahim-{project-name}/.vercel   # critical — forces new Vercel project
```

Then edit `index.html`:
1. Change `<title>`, hero copy, CTAs
2. Update Typeform widget ID in the embed
3. Test locally with a browser

## Asset Linking

Videos and images are NOT copied to new projects. Reference the master deployment:

```html
<!-- Videos -->
<source src="https://thecreed-one.vercel.app/videos/{name}.mp4">

<!-- Transformation images -->
<img src="https://thecreed-one.vercel.app/transformations/{name}.jpg">

<!-- Video posters -->
<video poster="https://thecreed-one.vercel.app/posters/{name}.jpg">
```

Available videos: pangina, davide, mohammed, matthew, mariel, ashley, asmond
**Steven's video must be deployed locally** — see "Steven's Video Fix" below.

Available transformations: davide, fatuma, konstantin, marielle, matthew, mohammed, omar, pangina, steven

### Steven's Video Fix (CORS workaround)

Steven's video (113MB) is on Google Drive. **Do NOT stream from Google Drive** — the direct download URL (`drive.usercontent.google.com`) does NOT have CORS headers for browser video tags. Curl works (no CORS enforcement) but browser `<video>` tags fail with NETWORK_NO_SOURCE. Proven in session 20260701_042630.

**Correct approach — download, compress, deploy locally:**

1. Download from Google Drive:
   ```bash
   curl -L -o /tmp/steven_raw.mp4 "https://drive.usercontent.google.com/download?id=FILE_ID&confirm=t&authuser=0"
   ```

2. Compress with ffmpeg (113MB → ~17MB):
   ```bash
   ffmpeg -y -i /tmp/steven_raw.mp4 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 64k -movflags +faststart videos/steven.mp4
   ```
   - CRF 28: good quality/size balance
   - `-movflags +faststart`: enables streaming (video plays before full download)

3. Include `videos/steven.mp4` in the same deployment directory as `index.html`. Vercel serves static files from any subdirectory automatically — no vercel.json needed.

4. Reference with relative path:
   ```html
   <source src="videos/steven.mp4" type="video/mp4">
   ```

5. Clean up temp files after deploy:
   ```bash
   rm /tmp/steven_raw.mp4  # raw 113GB original
   ```

**Why this works:** Vercel serves the video from the same origin as the page — no CORS issue. The compressed 17MB file is well under Vercel's 100MB limit.

See `ops/vercel-deploy/references/google-drive-video-to-vercel.md` for a dedicated static-host variant (deploying video to a separate Vercel project).

## Deployment

```bash
cd /root/ibrahim-{project-name}
npx vercel --prod --token $VERCEL_TOKEN --yes
```

Output: `https://{project-name}.vercel.app`

### Custom domain (if needed)
```bash
vercel domain add {subdomain}.cali-creed.com {project-name} --token $VERCEL_TOKEN
```
Note: DNS is managed outside Vercel. User must add CNAME record at their provider.

### Pitfalls & Recoveries

**Vercel free tier deployment expiry:** Deployments on the free Hobby plan expire after 30 days. The Vercel project still exists (`.vercel/project.json` stays valid) but all deployments are wiped. Fix: just redeploy — `npx vercel deploy --prod --token $TOKEN --yes` from the same directory reuses the project ID.

**Project linking mismatch:** If `.vercel/project.json` points to a different project than the one assigned the domain, the deploy succeeds (new deployment URL) but the domain alias fails. Fix: edit `.vercel/project.json` to match the project that owns the domain, or reassign the domain via Vercel API:
```python
# Delete domain from old project, add to new project
requests.delete(f'https://api.vercel.com/v9/projects/{old_proj}/domains/{domain}?teamId={team}')
requests.post(f'https://api.vercel.com/v9/projects/{new_proj}/domains?teamId={team}',
              json={"name": domain})
```

**Next.js vs static project confusion:** If a Vercel project was originally created with a Next.js framework, subsequent static HTML-only deploys may silently serve the old Next.js build instead. The project's framework detection takes priority. Fix: create a new project for the static page and move the domain to it.

**Local file recovery (Vercel deploy expiry):** When `https://{project}.vercel.app` returns 404 or a stale page, DON'T rebuild from scratch. First check:
1. Does the local source directory still exist? Check `/root/{project-name}/index.html`
2. Check `.vercel/project.json` for the project ID
3. If the project exists on Vercel but has zero deployments, just redeploy from the local files
4. If the `.vercel/project.json` links to a different project than the one with the domain, update the file or reassign the domain

Common Vercel project IDs for Ibrahim:
- `creed-coaching-giveaway` → `prj_jt07yuTFHQJQRsdmdHvNYArq0cZV` (domain: creed-coaching-giveaway.vercel.app)
- `ibrahim-giveaway-lp` → `prj_8b9xHvKIPNFyvb0URaR4fyhN1wVj` **← this owns ibrahim-giveaway.vercel.app** (active, July 2026)
- `ibrahim-giveaway` → separate project, no domain (gets `-creed-ramzy.vercel.app` subdomain)
- `ibrahim-giveaway-v2` → Next.js + motion/react upgrade, deployed at `https://ibrahim-giveaway-v2.vercel.app`, local at `/root/ibrahim-giveaway-v2`
- `ibrahim-lowticket` → `prj_Yh0Wbqv9JaYlcWCLea6HA0KztjZm`
- `ibrahim` → `prj_USPQzYyNdhjxDxZIyw0AAh6h6GkG`
- `creed-funnel` → `prj_9lU3PPSggFIJpaETTf0Pt4zAXI96`

**⚠️ Dual-project domain trap:** The domain `ibrahim-giveaway.vercel.app` is assigned to project `ibrahim-giveaway-lp`. There is a SEPARATE project named `ibrahim-giveaway` (no assigned domain). If you `vercel link` without specifying `--project ibrahim-giveaway-lp`, auto-detection may link to the wrong one. Always force-link before deploying to that domain:
```bash
npx vercel link --yes --project ibrahim-giveaway-lp --token "$(cat /tmp/vtoken)"
```

**Dual-project deployment (same code, two domains):** When the same landing page needs to serve from two domains (e.g. `creed-coaching-giveaway.vercel.app` AND `ibrahim-giveaway.vercel.app`), you must deploy to each project separately:
1. Link to project A → deploy → confirms domain A
2. Relink to project B → deploy → confirms domain B
3. Both deployments are independent — update both when code changes
```bash
# Deploy to domain A
cd /root/ibrahim-giveaway
npx vercel link --yes --project creed-coaching-giveaway --token "$(cat /tmp/vtoken)"
npx vercel deploy --prod --token "$(cat /tmp/vtoken)"

# Deploy same code to domain B
npx vercel link --yes --project ibrahim-giveaway-lp --token "$(cat /tmp/vtoken)"
npx vercel deploy --prod --token "$(cat /tmp/vtoken)"
```

**Token masking bug:** Vercel tokens get masked to `***` in agent response text, corrupting inline commands. Store in `/tmp` via `printf`:
```bash
printf 'vcp_yourtokenhere' > /tmp/vtoken.txt
# Then use: --token "$(cat /tmp/vtoken.txt)"
```

**Google Drive video CORS trap:** `drive.usercontent.google.com` URLs work via curl (no CORS enforcement) but FAIL in browser `<video>` tags. The video element shows "Unable to play media" with NETWORK_NO_SOURCE. Always download and deploy locally — see "Steven's Video Fix" section above.

## Mobile Optimization

Every page must be optimized for phone-first viewing - Ibrahim explicitly confirmed that most visitors come from phone.

### Premium mobile breakpoints (768px and 400px)

```
@media (max-width: 768px) {
  section { padding: 70px 16px; }
  .hero { padding: 50px 16px 30px; }
  .hero-headline { font-size: clamp(1.6rem, 7vw, 2.2rem); }
  .hero-sub { font-size: 0.9rem; }
  .hero-price { font-size: 1.1rem; }
  .hero-cta { width: 100%; padding: 18px 24px; font-size: 1rem; }
  .hero-badge { font-size: 0.6rem; padding: 6px 14px; }
  .steps-grid, .prize-grid, .pillars-grid, .features-grid { grid-template-columns: 1fr; }
  .testimonial-grid { grid-template-columns: 1fr; }
  .trans-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .prize-card.gold { transform: none; }
  .testimonial-card { padding: 20px 16px; }
  .typeform-frame { border-radius: 12px; }
  .step-card, .prize-card, .pillar-card { padding: 28px 20px; }
  .prize-card .value { font-size: 1.3rem; }
  .trans-name { font-size: 0.75rem; }
  .trans-result { font-size: 0.7rem; }
  .feat-item { padding: 20px 16px; }
  .vsl-section { padding: 60px 16px; }
  .vsl-video { border-radius: 12px; }
  .section-sub { margin-bottom: 40px; }
  .step-num { width: 42px; height: 42px; font-size: 1.1rem; }
  .exit-modal { padding: 32px 24px; }
}
```

Key improvements from the old values:
- Hero top padding: 50px (was 80px) - content was sitting too low
- Section padding: 70px (was 50px) - more breathing room
- Card internal padding: 28px (was 24px)
- Breakpoint: 768px (was 640px) - covers more phone sizes
- Added exit-modal and hero-headline fine-tuning

### Sticky CTA safe areas
For fixed-bottom bars, respect notched phones:
```
padding-bottom: calc(12px + env(safe-area-inset-bottom, 0px));
```

### Verification on mobile
After deploy, open the page on a real phone or DevTools mobile emulation (iPhone SE / Galaxy S8+ viewports). Check:
- CTA button spans full width and is tappable with one thumb
- Headings fit in 2 lines (no overflow/ellipsis)
- Video player controls are usable at small sizes
- Typeform embed fills the screen width
- No horizontal scroll anywhere

## Content Preservation Rule (critical for design/motion upgrades)

When the user says **"don't change the content"** or **"keep the content the same"** during a design or motion upgrade:
- Every word, heading, subtitle, badge, button, and disclaimer must be copied exactly as-is.
- Do NOT rewrite, condense, rephrase, or "improve" any copy.
- Do NOT move sections around or reorder elements.
- Do NOT add new sections of copy (FAQ, entry counter, etc. are ADDED as separate UI elements, not inserted into existing copy blocks).
- The only acceptable changes: wrapping existing text in `<em>` tags for gold styling (if the original did that), or adding CSS classes/styles that don't affect text content.
- Test after deploy: grep the live page for key phrases from the original to verify they survived.

This rule is separate from (and overrides) any copywriting instincts. Motion/design upgrades are NOT copywriting passes.

## Icon Standards

Use **Lucide icons** for all UI elements. Never use emoji as icons — the user explicitly corrected this.

### Icon mapping for The Creed pages

| Purpose | Lucide Icon | Size |
|---|---|---|
| Hero badge alarm | `AlarmClock` | 14px |
| 1st place | `Trophy` | 36px |
| 2nd/3rd place | `Medal` | 36px |
| Everyone else | `Gift` | 36px |
| Pillar: Mindset | `Brain` | 36px |
| Pillar: Nutrition | `Apple` | 36px |
| Pillar: Training | `Dumbbell` | 36px |
| Feature: Mentorship | `Calendar` | 28px |
| Feature: Onboarding | `Target` | 28px |
| Feature: Training | `Dumbbell` | 28px |
| Feature: Nutrition | `CookingPot` | 28px |
| Feature: Touchpoints | `Phone` | 28px |
| Feature: Mastery | `BookOpen` | 28px |
| VSL play indicator | `Play` | 12px |
| FAQ arrow | `ChevronDown` | 16px |
| Exit close | `X` | 18px |
| Live dot | `Circle` (fill green) | 6-8px |
| CTA arrows | Inline SVG arrow (path) | 18px |

Style: All icons are `strokeWidth={2.5}` (default). Pillar icons use `color: var(--gold)`. Feature icons use `color: var(--gold)`. Render Lucide icons as JSX components, not string class names — they're SVGs that scale crisply at any resolution.

```tsx
import { Trophy, Medal, Gift, Brain, Apple, Dumbbell } from "lucide-react";
```

## Premium Design Patterns

When the user asks to "make the page more premium" or improve the look, apply these refinements.

### Typography hierarchy
- Hero headline: `clamp(2.2rem, 5.5vw, 3.8rem)` with `letter-spacing: -0.02em` and `font-weight: 900`
- Section headings: `clamp(1.6rem, 3.6vw, 2.6rem)` with `letter-spacing: -0.01em`
- Body text: `var(--silver-light)` (`#D4D4DC`) at `opacity: 0.7-0.85` — brighter than default silver for readability
### Gold accent for em tags

- All `em` tags inside headings get solid gold: `font-style: normal; color: var(--gold)`
- Gradient text variant (`-webkit-background-clip: text`) can render inconsistently — reserved for hero headline only
- Section headings default to solid gold as the verified safe choice

### Gold gradient usage
Always define a gold gradient for premium accents:
```css
--gold-gradient: linear-gradient(135deg, #FFD700, #FFA500);
--gold-light: #FFED4A;
```
Apply to: CTA buttons, prize values, heading em tags, scroll progress bar, winner badge borders.

### Glass-morphism cards
Every card should use a subtle glass background instead of bare transparent:
```css
--glass-bg: rgba(255, 255, 255, 0.03);
--glass-border: rgba(255, 255, 255, 0.08);
--glass-border-hover: rgba(255, 215, 0, 0.25);
```
Cards get: `border-radius: 16px`, `background: var(--glass-bg)`, `border: 1px solid var(--glass-border)`.

### Section transitions
Every section needs a `::before` pseudo-element with a 1px gold gradient line at the top:
```css
section::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent);
}
```
Sections should alternate background gradients (e.g., `linear-gradient(180deg, var(--near-black) 0%, #151515 100%)` then `linear-gradient(180deg, var(--dark-navy) 0%, #06203A 100%)`).

### Hero enhancements
- Background: dark gradient with radial gold glow overlay + grid pattern
- Badge: **solid gold background** (`background: var(--gold); color: #000`) — the user rejected outlined/transparent badges. Solid gold is the verified preference.
- CTA: 12px border-radius, gold gradient, drop shadow (`box-shadow: 0 4px 24px rgba(255, 215, 0, 0.3)`)
- Bottom fade: `::after` with `linear-gradient(to top, var(--near-black), transparent)` at 120px height
- Entry counter + countdown timer must be placed **inside** the hero section (as direct children of the `<section className="hero">`), not between hero and VSL.

### Card hover effects
- Lift: `y: -3` to `y: -4` on hover
- Step cards: gold gradient top border that appears on hover (2px, `::before` with `opacity: 0 → 1`)
- Gold prize card: `scale: 1.05` with `box-shadow: 0 8px 40px rgba(255, 215, 0, 0.08)`, hover to `scale: 1.08`
- Feature cards: glass background + border (not bare text), hover lift `y: -3`

### Testimonial refinements
- Result badges: **solid gold background** (`background: var(--gold); color: #000`) — the user rejected outlined badges. Solid gold is the verified preference.
- Author avatars: **solid gold background** (`background: var(--gold); color: #000`) — not gradient.
- Video elements: 12px border-radius inside 16px card border-radius (concentric radii)

### Pillar card refinements
- Bullet list items: use gold checkmark (`'\\2713'` character via `::before` pseudo-element). This is the verified original pattern from Ibrahim's existing pages. Gold dot variant (`width: 6px; height: 6px; border-radius: 50%`) is experimental — use checkmark as the safe default.
- Icons: gold color (`svg { color: var(--gold) }`)
- Text: `opacity: 0.8` for readability

### Easing
Use `var(--ease-out-expo)` = `cubic-bezier(0.16, 1, 0.3, 1)` for all hover transitions and section animations. This is the same easing used by motion/react defaults.

## Copy Preferences (Ibrahim)

- **Headings:** 2 lines max. Use `<br>` for manual line break. No text overflow.
- **No em dashes (—).** Use regular hyphens (-) or commas.
- **Button copy:** "Enter the Giveaway", "Join Now", "Start Your Transformation" — specific per funnel. Not "Submit" or "Apply".
- **Hero spacing (giveaway pages):** Content should sit HIGH with minimal top gap. Use min-height: auto (NOT 100vh), align-items: flex-start, padding: 40px 20px 50px. User rejected centered-vertical-hero — wants badge/headline/CTA visible at top without scrolling.
- **Under-How-to-Win copy (giveaway):** Always include below the 3-step grid: "Follow the simple steps and look out for the message you will receive once done."
- **Gold accent for giveaways:** Use var(--gold) for highlights, not royal blue.
- **Style corrections the user has flagged:**
  - Headings MUST be max 2 lines. If a heading wraps to 3 lines on mobile, condense it.
  - Remove all em dashes from copy immediately when building new pages.
  - Testimonial videos and before/after images must be verified live after deploy — user will notice if they don't load.

### Edit Precision (critical workflow rule)

When the user says **"replace X with Y"**, do EXACTLY that:
- Find X in its current location and replace it with Y there
- Do NOT add Y somewhere else while leaving X in place
- Do NOT duplicate Y in a second location unless explicitly told to
- EXAMPLE: User said "replace the text that says 'I'm looking for the next testimonial' with 'Follow the simple steps...'" — the fix is to find THAT `.section-sub` paragraph and change its content. NOT add the new text below the steps grid and leave the old one in place.

This is the single most common correction the user makes. Read his edit instruction twice before executing.

## Page Sections — Design Patterns

### VSL (Video Sales Letter) Section

Place between hero and "How to Win" — Ibrahim's preferred position. The VSL sits in a dark section (same as hero bg or `var(--near-black)`) to avoid competing with the gold/Hero.

**When to add:**
- Giveaway pages (high-value prize / $5K coaching)
- High-ticket landing pages where proof of results is the sticking point
- Any page where a short video (30-90s) can communicate value faster than text

**CSS (add to the existing styles):**
```css
/* ===== VSL SECTION ===== */
.vsl-section {
  padding: 60px 20px;
  background: var(--near-black);
  text-align: center;
}
.vsl-wrapper { max-width: 800px; margin: 0 auto; }
.vsl-section .section-sub { margin-bottom: 32px; }
.vsl-video {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.4);
  display: block;
}
.vsl-caption {
  font-size: 0.85rem;
  color: var(--silver);
  opacity: 0.6;
  margin-top: 16px;
}
```

**HTML (insert between hero closing `</section>` and How to Win opening `<section>`):**
```html
<section class="vsl-section">
  <div class="vsl-wrapper">
    <h2 class="section-h2">See What <em>$5,000 Coaching</em> Looks Like</h2>
    <p class="section-sub">Hit play. This is what 12 weeks of 1:1 work with me actually delivers.</p>
    <video class="vsl-video" controls playsinline poster="">
      <source src="vsl.mp4" type="video/mp4">
    </video>
    <p class="vsl-caption">▶ 1 minute — no fluff. This is what you're playing for.</p>
  </div>
</section>
```

**Headline formula:** `"See What [Prize Value] Looks Like"` or `"Watch [Client Name]'s Transformation"`. Always use `<em>` tags on the high-value phrase (e.g. `$5,000 Coaching`) to trigger the gold accent from `var(--gold)` via `.section-h2 em`.

**Mobile overrides (add to `@media (max-width: 640px)` block):**
```css
.vsl-section { padding: 40px 16px; }
.vsl-video { border-radius: 8px; }
.vsl-section .section-sub { margin-bottom: 20px; }
.vsl-caption { font-size: 0.82rem; margin-top: 12px; }
```

### Video Compression for Landing Pages

Two patterns depending on use case:

**A. Testimonial videos (longer, ~60-120s, 100MB+ raw):** Use CRF-based compression. Quality priority, filesize secondary. CRF 28 is the sweet spot (good quality, ~6-8x smaller):
```bash
ffmpeg -y -i input.mov -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 64k -movflags +faststart output.mp4
```

**B. VSL / short promo videos (~30-90s, need under 5MB for fast loading):** Use bitrate-based compression with a hard cap. Size target controls the bitrate:
```bash
ffmpeg -y -i input.mov -vf "scale=848:464" -c:v libx264 -preset fast \
  -b:v 600k -maxrate 800k -bufsize 1200k -c:a aac -b:a 64k -movflags +faststart output.mp4
```
- `-b:v 600k`: target bitrate (adjust: 600k → ~5MB per 60s, 1M → ~8MB per 60s)
- `-maxrate 800k`: peak cap (avoids quality spikes causing buffering)
- Scale to 848px wide (standard mobile-friendly width)

**Both patterns require `-movflags +faststart`** — enables progressive download so the video starts playing before fully buffered.

**Audio quality trap when re-encoding for web:** The default `-b:a 64k` (or Typeform's native 62kbps AAC) sounds noticeably degraded, especially on voice/fitness videos where audio clarity matters. Ibrahim flagged this after the first compressed VSL deployed. Fix: use `-b:a 128k` for voice-heavy VSL content. The filesize increase is negligible (~7.5MB vs 5.4MB for a 60s video) but the quality difference is obvious.

```bash
# BAD — muddy audio
ffmpeg -i input.mov ... -c:a aac -b:a 64k output.mp4

# GOOD — crisp audio for voice/VSL content
ffmpeg -i input.mov ... -c:a aac -b:a 128k output.mp4
```

**Post-compression cleanup:**
```bash
rm /root/ibrahim-giveaway/vsl-original.mov  # raw original
```

## Funnel-Specific Copy

### Giveaway Page
- Headline: "Win 12 Weeks 1:1 Coaching With Ibrahim Ramzy"
- Subtitle: "Valued at $5,000 — Yours Free If You Win"
- Badge: "14 Days Left to Enter" (gold, pulsing)
- Prize cards: 1st/$5K, 2nd+3rd/$500 off, Everyone/exclusive offer
- How to Win: 3-step section (Fill in the Form → Reply to WhatsApp → Winner Announced on 7 July). Subtitle reads: "Follow the simple steps and look out for the message you will receive once done."
- What's Included: 3 pillars (Head Right / Eat Without Rules / Train for Body You Want) from OCR'd images
- Testimonials: flood with 8 transformation cards + 8 video testimonials

### Low-Ticket Page ($99/mo Health in Motion)
- Headline: "Get the body, energy, and confidence you deserve — for $99/month"
- Benefits: 6-card grid (Training, Nutrition, Community, Live Session, Everfit app, Mastery Library)
- Pricing card: $99/month, cancel anytime
- FAQ: 6 low-ticket specific questions
- Typeform: Simplified flow (Yes/No gate → Why now → Contact)

## Verification

After deploy, validate in order:

### 1. HTTP status
```bash
curl -s -o /dev/null -w "%{http_code}" https://{project}.vercel.app
# Must be 200
```

### 2. Page content check
```bash
curl -s https://{project}.vercel.app | grep -c 'N4LbJCHT\|Win 12 Weeks\|The Creed'
# Must match at least 1 — confirms the right page is serving, not a stale Next.js default
```

### 3. Video/asset health (browser-level)
HTTP 200 is NOT enough. Videos that return 200 via curl can still fail in browsers due to CORS. Use browser console on the live page:
```javascript
document.querySelectorAll('video').forEach((v,i) => {
  let err = v.error ? `${v.error.code}: ${v.error.message}` : 'OK';
  let src = v.querySelector('source')?.src?.split('/').pop() || 'no source';
  console.log(`Video ${i}: ${src} → ${err}`);
});
```
All should show "OK". Any "NETWORK_NO_SOURCE" or "MEDIA_ERR_SRC_NOT_SUPPORTED" means a CORS or broken URL.

### 4. Typeform embed
Check the widget div exists and the embed script tag is present:
```javascript
document.querySelector('[data-tf-widget]') ? 'widget OK' : 'MISSING widget'
```
The widget loads an iframe asynchronously. If `<script src="https://embed.typeform.com/next/embed.js">` is missing from the page bottom, the form won't render.

### 5. Transformation images
```javascript
document.querySelectorAll('.trans-card img').forEach((img,i) => {
  console.log(`Img ${i}: ${img.complete && img.naturalWidth > 0 ? 'LOADED' : 'BROKEN'} ${img.src.split('/').pop()}`);
});
```

---

### Related References
- `references/giveaway-page-state.md`
- `references/giveaway-conversion-research.md` — Research-backed conversion optimizer patterns for giveaway landing pages: entry counter, countdown timer, sticky mobile CTA, exit-intent popup, FAQ accordion, scroll progress bar.

## Motion/Animation Upgrade (Static HTML → Next.js + motion/react)

When the user asks to add animations/motion to an existing landing page, follow this pattern.

### How the conversion works

1. **Create a fresh Next.js project** (never modify the existing static HTML in-place):
   ```bash
   npx create-next-app@latest {project-name} --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm
   cd {project-name}
   npm install motion
   ```

2. **Port every CSS class 1:1 into `globals.css`** — do NOT rewrite or simplify the styles. The brand styling (navy, silver, gold, dark background, grid patterns, card borders, responsive breakpoints) must survive unchanged.

3. **Split sections into client components** under `src/app/components/`:
   - Each section (Hero, VSL, HowToWin, Prizes, etc.) is one component
   - All are `"use client"` since they use `motion/react`
   - Page files must NOT have `"use client"` — the page itself stays a server component; individual section components carry the directive

4. **The Typeform embed script** must be added dynamically in the page component:
   ```tsx
   useEffect(() => {
     const script = document.createElement("script");
     script.src = "https://embed.typeform.com/next/embed.js";
     script.async = true;
     document.body.appendChild(script);
   }, []);
   ```

### Animation patterns used

| Pattern | Code | Used for |
|---|---|---|
| **Staggered entrance** | `stagger` variant + `cardFade` variant on each child | All grids (steps, prizes, transformations, testimonials, pillars, features) |
| **Scroll reveal** | `whileInView={{ opacity: 1, y: 0 }}` + `viewport={{ once: true }}` | Every section on the page |
| **Hover lift** | `whileHover={{ y: -3, borderColor: "var(--gold)" }}` | Cards, CTAs |
| **Button feedback** | `whileHover={{ scale: 1.03 }}` + `whileTap={{ scale: 0.97 }}` | All CTAs |
| **Icon/emoji hover** | `whileHover={{ scale: 1.15, rotate: 5 }}` | Pillar icons, feature icons |
| **Continuous pulse** | `animate={{ scale: [1, 1.05, 1] }}` with `repeat: Infinity` | Badge (countdown), hero CTA |
| **FadeInView wrapper** | Reusable wrapper component around each section | Consistent section entrance animation |

### The FadeInView wrapper

```tsx
function FadeInView({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  const reduce = useReducedMotion();
  return (
    <motion.div
      className={className}
      variants={{ hidden: { opacity: 0, y: reduce ? 0 : 24 }, visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] as const } } }}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-60px" }}
    >
      {children}
    </motion.div>
  );
}
```

### Pitfall: TypeScript easing type

`motion/react` (v12+) requires cubic bezier arrays to have `as const` assertion:

```tsx
// WRONG — TypeScript error
ease: [0.22, 1, 0.36, 1]

// CORRECT
ease: [0.22, 1, 0.36, 1] as const
```

Same applies anywhere you embed an easing array in a `transition` object or `variants` definition.

### Reduced motion support

Every animated component must check `useReducedMotion()`:

```tsx
const reduce = useReducedMotion();
// When reduce is true, set y: 0 in hidden states, skip scale transforms
```

The `FadeInView` wrapper handles this — but individual section components that use custom variants (like stagger children) need explicit reduce checks on their `cardFade`/`fadeUp` variants.

## Giveaway Page Conversion Optimizers

These are ADDED elements (not content replacements) that research shows improve conversion and retention on giveaway landing pages. Keep existing copy 100% intact — these slot into the page as new UI.

### 1. Scroll Progress Bar

Fixed to top of viewport. A thin (2-3px) bar that fills as the user scrolls down the page.

```tsx
import { motion, useScroll, useSpring } from "motion/react";

export function ScrollProgress() {
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, { stiffness: 100, damping: 30 });
  return <motion.div className="scroll-progress" style={{ scaleX }} />;
}
```

CSS: `position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(90deg, var(--gold), #FFA500); z-index: 9999; transform-origin: left;`

### 2. Sticky Mobile CTA

A fixed bottom bar with the CTA button that appears when the hero scrolls past viewport. Mobile-only. Helps recover abandoners who scroll without entering.

```tsx
const [visible, setVisible] = useState(false);
useEffect(() => {
  const handleScroll = () => {
    const hero = document.querySelector(".hero");
    if (hero) setVisible(hero.getBoundingClientRect().bottom < 0);
  };
  window.addEventListener("scroll", handleScroll, { passive: true });
  return () => window.removeEventListener("scroll", handleScroll);
}, []);
```

CSS: `position: fixed; bottom: 0; z-index: 9998; background: rgba(var(--dark-navy), 0.95); backdrop-filter: blur(12px); transform: translateY(100%); transition: transform 0.3s var(--ease); &.visible { transform: translateY(0); }`

### 3. Live Entry Counter

Shows social proof: "X people have entered so far". Count increments randomly every ~8s to feel live. Place **inside** the Hero section (after the hero-inner div), not between hero and VSL.

```tsx
const [count, setCount] = useState(128);
useEffect(() => {
  const interval = setInterval(() => setCount(prev => prev + Math.floor(Math.random() * 3) + 1), 8000);
  return () => clearInterval(interval);
}, []);
```

Use `font-variant-numeric: tabular-nums` on the count number to prevent layout shift as digits change.

### 4. Countdown Timer

A real-time countdown to the giveaway close date. Place **inside** the Hero section, after the EntryCounter.

```tsx
const [timeLeft, setTimeLeft] = useState({ days: 0, hours: 0, mins: 0, secs: 0 });
useEffect(() => {
  const target = new Date("2026-07-07T23:59:59");
  const tick = () => { /* calculate diff, set state */ };
  tick(); const i = setInterval(tick, 1000); return () => clearInterval(i);
}, []);
```

Display: `"Closes in 02d 14h 32m 08s"`. Also use `tabular-nums` for digit stability.

### 5. Exit Intent Popup

Triggers when the mouse cursor leaves the viewport (user about to close tab). Shows a last-chance message: "Wait — don't lose this chance". Only show once per session (use `sessionStorage` to track dismissal).

```tsx
useEffect(() => {
  const handleMouseLeave = (e: MouseEvent) => {
    if (e.clientY <= 0 && !sessionStorage.getItem("exit-popup-dismissed")) setShow(true);
  };
  document.addEventListener("mouseleave", handleMouseLeave);
  return () => document.removeEventListener("mouseleave", handleMouseLeave);
}, []);
```

Modal content: Headline `"Wait — <em>don't lose this chance</em>"`, subtext about everyone getting access to the coaching package, and a CTA button linking to `#enter`.

### 6. FAQ Accordion

Placed between the features strip and the Typeform section. Addresses common objections about the giveaway: winner selection, eligibility, what happens if you don't win, program duration, suitability for beginners.

Implementation: Animate height and opacity using `motion.div animate={{ height: open ? "auto" : 0, opacity: open ? 1 : 0 }}`. Each question is a button that toggles open/close. Only one open at a time.

5 questions minimum. Topics based on real visitor concerns:
1. "How is the winner chosen?" — transparency about selection
2. "Do I need to be in a specific country?" — addresses eligibility worry
3. "What happens if I don't win?" — frames consolation offer
4. "How long does the coaching last?" — sets expectations
5. "Is this suitable for beginners?" — removes intimidation

### Order on page (giveaway)

```
ScrollProgress (always visible)
StickyCTA (appears on scroll)
ExitIntentPopup (triggers on mouse leave)
Hero
  └─ EntryCounter (inside Hero, after the hero-inner div)
  └─ CountdownTimer (inside Hero, after EntryCounter)
VSL
HowToWin
Prizes
Transformations
Testimonials
Included
FeaturesStrip
FAQ (NEW — between features and typeform)
Typeform
Footer
```