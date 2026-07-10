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
