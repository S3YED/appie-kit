---
name: landing-page-workflows
description: Build, duplicate, and deploy landing pages for Ibrahim Ramzy's coaching funnels. Covers copy patterns, asset linking, Vercel deployment, and client-specific design preferences.
version: 1.0.0
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
- `ibrahim-giveaway` → `prj_...` (separate project, no domain — gets `-creed-ramzy.vercel.app` subdomain if deployed to)
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

Every page must be optimized for phone-first viewing — Ibrahim explicitly confirmed "everyone will come from phone."

### Mandatory mobile overrides (substitute into `@media (max-width: 640px)` block):

```css
@media (max-width: 640px) {
  /* Stack all grids to 1 column */
  .steps-grid, .prize-grid, .pillars-grid, .features-grid { grid-template-columns: 1fr; }
  .testimonial-grid { grid-template-columns: 1fr; }

  /* Transformation grid: 2 columns works for before/after images */
  .trans-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }

  /* Remove gold card scale (overlaps in single column) */
  .prize-card.gold { transform: none; }

  /* Hero: reduce padding, scale down text */
  .hero { padding: 80px 16px 40px; }
  .hero-headline { font-size: clamp(1.6rem, 7vw, 2.4rem); }
  .hero-sub { font-size: 0.92rem; }
  .hero-price { font-size: 1.15rem; }
  .hero-cta {
    width: 100%;              /* full-width tap target */
    justify-content: center;
    padding: 18px 20px;       /* bigger thumb target */
    font-size: 1rem;
  }
  .hero-badge { font-size: 0.65rem; padding: 6px 14px; }

  /* Section spacing */
  section { padding: 50px 16px; }

  /* Testimonial cards: tighter padding, smaller quote text */
  .testimonial-card { padding: 20px 16px; }
  .testimonial-card .quote { font-size: 0.82rem; }

  /* Typeform embed: lighter border radius */
  .typeform-frame { border-radius: 8px; }

  /* Cards in grid sections: tighter padding */
  .step-card, .prize-card, .pillar-card { padding: 24px 18px; }
  .prize-card .value { font-size: 1.3rem; }

  /* Transformation card text: smaller to fit 2-col grid */
  .trans-name { font-size: 0.75rem; }
  .trans-result { font-size: 0.7rem; }

  /* Feature strip: tighter */
  .feat-item { padding: 14px 10px; }
  .pillar-card ul li { font-size: 0.78rem; }
}

@media (max-width: 400px) {
  /* Extra tightening for tiny screens */
  .trans-grid { gap: 8px; }
  .testimonial-card { padding: 16px 12px; }
  .hero { padding: 60px 12px 32px; }
  section { padding: 40px 12px; }
  .author-avatar { width: 34px; height: 34px; font-size: 0.8rem; }
  .result-badge { font-size: 0.65rem; padding: 3px 8px; }
}
```

### Verification on mobile
After deploy, open the page on a real phone or DevTools mobile emulation (iPhone SE / Galaxy S8+ viewports). Check:
- CTA button spans full width and is tappable with one thumb
- Headings fit in 2 lines (no overflow/ellipsis)
- Video player controls are usable at small sizes
- Typeform embed fills the screen width
- No horizontal scroll anywhere

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

- `references/systems-thinking-frameworks.md` — Synthesized frameworks from MIT Monk (DART diagnostic) and Dr. Justin Sung (3 building principles). Useful when Ibrahim talks about building or redesigning systems for his business funnel.
