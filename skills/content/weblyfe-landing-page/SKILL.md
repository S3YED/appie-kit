---
name: weblyfe-landing-page
description: Build a complete conversion-optimized landing page for Weblyfe clients. Full pipeline from competitor audit through SEO analysis, brand style guide, Next.js build, and Vercel deploy. Use when building or rebuilding any client website from scratch.
version: 1.0.0
triggers:
  - build a website
  - rebuild a landing page
  - new client website
  - modernize website
  - landing page for
  - website for client
---

# Weblyfe Landing Page Builder

Complete pipeline for building modern, conversion-optimized landing pages for Weblyfe clients.

## Seyed's Design Preferences (NON-NEGOTIABLE)

These preferences were established through direct feedback and corrections:

1. **Light theme by default** — white backgrounds, NOT dark mode. Dark is only for specific clients who explicitly request it.
2. **Use the client's original brand colors** — extract from existing site or logo. Don't invent new palettes unless the client wants a rebrand.
3. **Lots of images** — Unsplash photography throughout. Hero images, service cards, image strips, location photos. A bike shop needs bike photos. Be generous.
4. **Rich animations** — Framer Motion everywhere: scroll reveals, parallax, floating badges, counter animations, image clip-path reveals, hover lifts. Make it feel alive but not childish.
5. **Brand style guide FIRST** — Before writing any code, produce a style guide with: color system, typography, imagery direction, UI components, animation philosophy, section architecture. Get the vibe right before building.
6. **NO emoji overuse** — Emojis only in chat, never in production code. Use SVG icons (Lucide, Heroicons).
7. **Clean, minimal aesthetic** ("exaggerated minimalism") — white space is not wasted space.
8. **German clients need German precision** — conservative but modern. Think Porsche/Audi design language, not TikTok trends.

## Full Pipeline

### Phase 0: Class the site correctly
Before designing, decide whether this is:
- a straight service landing page,
- a local business site,
- or a personal brand / creator ecosystem.

If it is a personal brand or creator site, do not force it into a single-page lead-gen shape. Map the authority ecosystem first.

Reference notes: `references/personal-brand-site-research.md`

Existing-project review example: `references/nathan-nuyts-project-review.md` covers a real Weblyfe personal-brand repo audit, including handoff-first reading, doc/code conflict handling, canonical-domain gotchas, placeholder asset detection, legal-link checks, and stubbed lead-capture risks.

Dutch law-firm proposal/site pattern: `references/dutch-law-firm-website-pattern.md` covers NOvA/KVK/Rechtspraak discovery, controlled confidential CTAs, legal trust/compliance content, small-firm positioning, imagery, and SEO page maps for advocaat websites.

Law-firm client call synthesis: `references/law-firm-client-call-synthesis.md` covers how to turn a lawyer call transcript into sanitized project notes, sharper positioning, hero copy, asset asks, and honest Notion sync status without leaking private relationship context.

Drive assets and responsive QA example: `references/drive-assets-and-mobile-qa.md` covers public Google Drive asset extraction, validating downloaded files, choosing personal-brand imagery, mobile hardening, and honest Playwright verification reporting.

Legal services website playbook: `references/legal-services-website-playbook.md` covers Dutch lawyer/law-firm research, NOvA/KVK-style trust checks, confidential conversion, compliance-aware CTAs, SEO page mapping, and premium legal visual direction.

Law-firm branding and growth-system pattern: `references/law-firm-branding-and-growth-system.md` covers when a legal website expands into brand identity, logo/moodboard process, asset briefs, optional intake/onboarding pages, blog/SEO engine, Google Business Profile, and domain strategy.

Law-firm client call synthesis and branding workflow: `references/law-firm-client-call-synthesis.md` covers how to turn long legal-client calls into sanitized project docs, Weblyfe's branding-first process, logo system exploration, asset briefs, intake/system pages, blog approval workflows, and Google Business Profile quick wins.

Law-firm branding process: `references/law-firm-branding-process.md` covers moving from legal website audit into full Weblyfe-style branding: brand audit, moodboard directions, logo routes, brand system, asset brief, reviewed SEO content engine, and optional intake/system pages.

### Phase 1: Audit (30% of effort)
```
1. Browser-navigate to the current site
2. Browser-vision for visual analysis (colors, fonts, layout, flaws)
3. Browser-console for technical SEO: title, meta, H1 count, schema, OG tags, alt text
4. Run UI/UX Pro Max design system:
   python3 ~/.hermes/skills/ui-ux-pro-max/scripts/search.py "<industry> <keywords>" --design-system -p "Client Name"
5. Compile audit: what's broken, what's missing, what's ugly
```

### Phase 2: Style Guide (15% of effort)
```
Write STYLE_GUIDE.md in project root with:
- Brand positioning + target audience segments
- Color system (primary, neutral, accent palettes)
- Typography (why this font, scale)
- Imagery direction (Unsplash categories, treatments)
- UI components (buttons, cards, layout specs)
- Animation philosophy + easing curves
- Section architecture (ordered list of sections)
```

### Phase 3: Build (40% of effort)

#### PRD handoff implementation loop
When the user says to scrutinize a PRD and start design/development in an existing repo:
1. Read the PRD, project instructions, current git status, and the homepage/page components before editing.
2. Treat existing uncommitted work as in-progress handoff work. Audit it against the PRD instead of replacing it blindly.
3. Identify concrete PRD gaps first: section order, visual direction, copy/proof claims, CTAs/routes, accessibility, responsive behavior, and build health.
4. Apply minimal targeted edits that move the page closer to the PRD's direction while preserving route contracts and client content.
5. Verify with `npm run build` and, for visual work, browser/mobile review. If editing or build is blocked by permissions, report the blocker and the exact remaining issues, not a vague plan.

#### Reference-site header cleanup loop
When the user asks to make a site header clean like a reference site:
1. Load project docs first: handoff, README, PRDs, cached Notion/Drive notes, and any reference-site notes. These often define the intended nav architecture better than the current component does.
2. Inspect the current header component and global tokens before editing. Header fixes are usually small component/token changes, not a full page redesign.
3. Reduce visible choices to the conversion architecture. For personal-brand hubs, keep the core routes and one primary CTA. Remove secondary/anchor links from desktop nav unless the docs explicitly require them.
4. Match the reference qualities, not just colors: compact height, generous whitespace, light type weights, quiet borders, subtle glass/blur, one clear CTA, and simple mobile drawer.
5. If the reference URL cannot be fetched, do not claim visual certainty. Use checked-in docs and cached context, then state the limitation and the exact files changed or blocked.

```
1. npx create-next-app@latest <project> --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --no-turbopack
2. npm install framer-motion lucide-react
3. Write layout.tsx with:
   - Google Font (DM Sans for German clients, Instrument Sans/Plus Jakarta Sans for modern)
   - Full SEO metadata (title, description, keywords, openGraph, canonical)
   - Schema.org structured data (LocalBusiness, Organization, Service, etc.)
4. Write globals.css with:
   - CSS custom properties for all colors
   - Custom scrollbar styling
   - Animation keyframes (float, draw-line)
   - Selection colors matching brand
5. Write page.tsx as single-page app with ALL sections:
   - NAVIGATION: sticky, white bg with backdrop-blur, brand color logo
   - HERO: 50/50 split (text left, image right), floating badges, stat counters
   - IMAGE STRIP: 5+ images in horizontal flex
   - SERVICES: 3-column cards with image headers, icon + tags
   - ABOUT: 2-column (image + overlapping smaller image left, text + checklist right)
   - IMAGE BREAKER: full-width photo with gradient overlay + slogan
   - LOCATIONS: 2-column cards with map placeholder and opening hours
   - TRUST: 4-column icons with guarantees
   - CTA: full-width brand-color background with white text + phone + email
   - FOOTER: dark/minimal, Impressum link
   - IMPRESSUM: hidden section at bottom
```

### Phase 4: Deploy (15% of effort)
```
1. npm run build (fix any TS errors -- common: as const on ease arrays)
2. gh repo create <project> --public --source . --remote origin --push
3. npx vercel --prod --yes --token $VERCEL_TOKEN
4. curl verify: 200 OK
5. Send live URL to Seyed
```

## Animation Patterns (Copy-Paste Ready)

### Scroll-triggered fade-up
```tsx
function FadeUp({ children, delay = 0, className = "" }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  return (
    <motion.div ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.7, delay, ease: [0.19, 1, 0.22, 1] }}>
      {children}
    </motion.div>
  );
}
```

### Counter animation
```tsx
function useCountUp(end: number, duration = 2, startCounting: boolean) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!startCounting) return;
    let start = 0;
    const step = (end / (duration * 60)) | 0 || 1;
    const timer = setInterval(() => {
      start += step;
      if (start >= end) { setCount(end); clearInterval(timer); }
      else { setCount(start); }
    }, 16);
    return () => clearInterval(timer);
  }, [end, duration, startCounting]);
  return count;
}
```

### Image clip-path reveal
```tsx
function ImageReveal({ src, alt, className }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-60px" });
  return (
    <div ref={ref} className={`overflow-hidden rounded-2xl ${className}`}>
      <motion.img src={src} alt={alt}
        initial={{ scale: 1.15 }}
        animate={inView ? { scale: 1 } : {}}
        transition={{ duration: 1.2, ease: [0.19, 1, 0.22, 1] }}
        className="w-full h-full object-cover" loading="lazy" />
    </div>
  );
}
```

### Floating badge
```tsx
<motion.div
  animate={{ y: [0, -8, 0] }}
  transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
  className="absolute -bottom-6 -left-6 bg-white rounded-2xl shadow-xl p-4">
  ...
</motion.div>
```

### Hero parallax
```tsx
const { scrollY } = useScroll();
const heroScale = useTransform(scrollY, [0, 600], [1, 1.08]);
// Apply style={{ scale: heroScale }} to hero image container
```

## SEO Checklist (Must Include)

- [ ] H1 with primary keyword (exactly 1 per page)
- [ ] Meta description with keyword + CTA
- [ ] OG title, description (NOT template text)
- [ ] Canonical URL
- [ ] Schema.org structured data (LocalBusiness, Service, etc.)
- [ ] All images have descriptive alt text
- [ ] Keywords meta tag with 5-8 relevant terms
- [ ] Heading hierarchy: H1, H2, H3 (no skips)
- [ ] Viewport meta tag present

## Scroll-Video Hero Pattern

For client sites where you want a cinematic "transformative" reveal (interior design empty→finished, renovation before→after, construction timelapse), use a canvas-scroll scrub video:

```html
<section class="hero" style="height:300vh;background:#0d0a08">
  <div class="hero-sticky" style="position:sticky;top:0;height:100vh;overflow:hidden">
    <canvas id="heroCanvas"></canvas>
    <div class="hero-overlay"><!-- title, tagline, scroll hint --></div>
  </div>
</section>
```

Scroll logic (vanilla JS, no framework needed):
```js
const canvas = document.getElementById('heroCanvas');
const ctx = canvas.getContext('2d');
const video = document.createElement('video');
video.preload = 'auto'; video.muted = true; video.playsInline = true;
video.src = 'videos/transformation.mp4'; // MUST be H.264, not MPEG4
let fps = 30, totalFrames, ready = false;

video.addEventListener('loadedmetadata', () => {
  ready = true; totalFrames = Math.round(video.duration * fps);
});

function resize() {
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width; canvas.height = rect.height;
}

function render() {
  if (!ready) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const scale = Math.max(canvas.width / video.videoWidth, canvas.height / video.videoHeight);
  const sw = video.videoWidth * scale, sh = video.videoHeight * scale;
  ctx.drawImage(video, (canvas.width-sw)/2, (canvas.height-sh)/2, sw, sh);
}

function onScroll() {
  const hero = document.getElementById('hero');
  const scrolled = -hero.getBoundingClientRect().top;
  const scrollable = hero.offsetHeight - window.innerHeight;
  const progress = Math.max(0, Math.min(1, scrolled / scrollable));
  const targetFrame = Math.round(progress * totalFrames);
  const targetTime = targetFrame / fps;
  if (ready && Math.abs(video.currentTime - targetTime) > 0.02) {
    video.currentTime = targetTime;
  }
}
window.addEventListener('scroll', onScroll, { passive: true });
video.addEventListener('seeked', () => { if (ready) render(); });
window.addEventListener('resize', resize);
video.load();
```

**Frame-accurate tips:**
- Use `Math.round(progress * totalFrames)` to map scroll to discrete frames — prevents redundant seeks
- Smooth overlay fade: calculate `Math.max(0, 1 - Math.max(0, progress - 0.05) / 0.2)` and apply to `overlay.style.opacity`
- Scroll hint text: something specific like "Scroll om de transformatie te zien" or "Scroll om interieur te stijlen"
- Progress bar: pair with `progressBar.style.width = (progress * 100) + '%'`

**Video codec check (critical):**
```bash
ffprobe -v error -show_entries stream=codec_name -of default=noprint_wrappers=1 video.mp4
# Expect: h264 — if mpeg4, transcode:
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -movflags +faststart -c:a aac output.mp4
```

## Standard Landing Page Components (Copy-Paste Ready)

### Lucide Icons
Load from CDN: `<script src="https://unpkg.com/lucide@latest"></script>`
Add icons: `<i data-lucide="icon-name"></i>` — init with `lucide.createIcons()` after DOM ready.
Replace all emoji in production UI with Lucide equivalents (armchair, truck, gift, camera, phone, map-pin, clock, arrow-right, chevron-down, menu, message-circle, instagram, facebook).

### WhatsApp Floating Bubble
```html
<style>
.wa-button {
  position:fixed; bottom:1.5rem; right:1.5rem; z-index:100;
  width:56px; height:56px; border-radius:50%;
  background:#25d366; border:none; cursor:pointer;
  display:flex; align-items:center; justify-content:center;
  box-shadow:0 4px 16px rgba(37,211,102,.35);
  animation:waPulse 2s ease-in-out infinite;
}
@keyframes waPulse { 0%,100% { box-shadow:0 4px 16px rgba(37,211,102,.35); } 50% { box-shadow:0 4px 24px rgba(37,211,102,.6); } }
</style>
<button class="wa-button" onclick="window.open('https://wa.me/31XXXXXXXXX','_blank')" aria-label="WhatsApp">
  <i data-lucide="message-circle" style="width:26px;height:26px;color:#fff"></i>
</button>
```
Add a tooltip div that fades after 5s: "Hoe kunnen we helpen?"

### FAQ Accordion
```html
<div class="faq-item" style="border-bottom:1px solid #ece8e2;cursor:pointer">
  <div class="faq-q" onclick="this.parentElement.classList.toggle('open')"
       style="display:flex;justify-content:space-between;align-items:center;padding:1.25rem 0">
    <span>Vraag</span>
    <i data-lucide="chevron-down" style="width:18px;height:18px;transition:transform .3s"></i>
  </div>
  <div class="faq-a" style="max-height:0;overflow:hidden;transition:max-height .4s;font-size:.9rem;color:#6a5a4a">
    <p style="padding-bottom:1.25rem">Antwoord</p>
  </div>
</div>
```
CSS: `.faq-item.open .faq-a { max-height: 300px; }` and `.faq-item.open .faq-q .lucide { transform: rotate(180deg); }`

### Custom Scrollbar
```css
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f8f6f3; }
::-webkit-scrollbar-thumb { background: #c4b5a5; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #a09080; }
```

## Pitfalls

1. **Don't use dark theme unless asked** — Seyed corrected this. White/light is default.
2. **Don't invent new colors** — use the client's existing brand palette.
3. **Don't skimp on images** — Seyed asked for "dramatically more pictures." Use 10+ Unsplash images.
4. **Framer Motion ease arrays need `as const`** in Next.js 16: `ease: [0.19, 1, 0.22, 1] as const`
5. **Never deploy with an expired Vercel token** — refresh first.
6. **Always verify the deploy with curl** before reporting success.
7. **Check Next.js version** — conventions change between major versions. Use `cat node_modules/next/package.json | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"`
8. **For creator/personal brand sites, don't flatten everything into one offer** — preserve multiple pathways, proof layers, and the social identity from Instagram.
9. **Separate template content from true brand assets** — template scaffolds like Olivia can hide the real brand direction if you don't audit carefully.
10. **Preserve approved hero/header imagery** — when Seyed says the hero/header image was good, treat it as locked. Improvements from Drive assets should enrich supporting visuals, brand/proof sections, and responsive presentation unless he explicitly asks to replace the hero.
11. **Vercel token gets masked in terminal** — `$VERCEL_TOKEN` and token values containing `vcp_` get masked to `***` in Hermes terminal output. The token IS stored correctly in `.env.secrets` but you can't use it directly in shell commands. Workaround: read via Python from the file and pass to `subprocess.run(['npx','vercel','--token',token,'--yes','--prod'], cwd='/path')` instead of inline terminal commands.
12. **Dark background sites use glass morphism, NOT pure white** — Seyed rejected pure white boxes on dark backgrounds as "te fel". Use `bg-white/30 backdrop-blur-md border-white/30` with dark green text. See `references/apple-glass-morphism.md` for the full pattern.
13. **Always verify the Vercel team scope** — weblyfe.ai was locked because Vercel Authentication was enabled. Also, the Vercel team scope changed from `weblyfe` to `weblyfe-team-s-projects` — check `vercel teams ls` before deploying.===ME:weblyfe-landing-page