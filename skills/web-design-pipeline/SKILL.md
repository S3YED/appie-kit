---
name: web-design-pipeline
description: Build premium, multi-page, animated websites fast and with real design rigor — design-system-first, Claude Design + Claude Code, Next.js + GSAP, deploy to Vercel. Use for any client site, landing page, or the Clark/Weblyfe properties.
---

# Web Design Pipeline (premium sites, fast, with rigor)

The repeatable way to ship awwwards-tier sites without vibe-coding. Design tokens first, components second, motion last. Never one loose HTML file for flagship work.

## 0. Principle
Separate **DESIGN** (brand system) from **STRUCTURE** (layout) from **MOTION** (animation). Decide each deliberately. Padding/spacing always come from a scale, never by feel. See companion skills: `design-mastery`, `21st-dev`, `ui-ux-pro-max`, `design-system`, `motion`.

## 1. Design system FIRST
Build one coherent brand before any page:
- Tokens as one source: color, type scale, spacing on a 4/8pt grid, radii, shadows, motion curves. Light + dark.
- Max 2 typefaces (one display, one text). Single accent colour used sparingly. Tabular numbers for figures.
- Options to generate/seed a system:
  - Our locked **Stitch / Weblyfe Enterprise** tokens (canonical for Clark).
  - **Claude.ai → Design** tab → create a Design System (reusable across pages, decks, motion).
  - **getdesign.md** — free brand kits for 68 major brands (colors, type, icons, buttons, dark mode). Paste a brand's `design.md` into Claude Design "additional notes" to generate a reusable system in ~5 min. Use for inspiration/structure, never to copy a competitor's identity.

## 2. Structure from a reference
Pick a proven layout skeleton, then reskin with your design system:
- **durable.com** (or 21st.dev / awwwards) → screenshot a layout (e.g. "marketing agency website").
- Tell the model: use the design system for branding, use the screenshot only for structure. Same skeleton, your brand's look.

## 3. Prototype
Claude Design → **high fidelity** (not wireframe) + select your design system. Generate the multi-page set (home / services / about / case studies / contact). Edit visually: comment+select an element, edit for color/font/size, draw/circle a region to change specifics.

## 4. Hand off to Claude Code and one-shot
Export → "Handoff to Claude Code". In an empty folder, paste the command + append:
> Build this with **Next.js**, use **GSAP** for animations wherever appropriate — staggered scroll reveals, count-up numbers, parallax, moving logo strip — stunning but never cheesy. Read `claude.md` and build it in one go.

Add a **claude.md** blueprint first (system instructions / "employee manual": stack, tokens, do/don'ts, motion budget). It materially improves one-shot quality.

## 5. Motion with GSAP
GSAP is the high-end layer plain CSS misses. Patterns: scroll-triggered staggered reveals, count-ups on stat tiles, parallax, pinned sections, marquee logo strip, magnetic buttons. Effect library: demos.greensock.com (copy an effect, ask Claude to add it). Keep within the design-mastery motion budget: purposeful, micro-interactions <200ms, a few high-impact reveals, respect `prefers-reduced-motion`.

## 6. Deploy
GitHub (private repo) → Vercel → framework preset **Next.js** → add a **custom domain**. Never ship a client a `*.vercel.app` URL.

## 7. Verify before shipping
- Real overflow check via in-page `scrollWidth` vs `clientWidth` (headless `--window-size` screenshots are unreliable — they clamp the viewport).
- CSS specificity traps: a class like `.wrap` on a `<header>`/`<section>` beats type-selector padding and silently collapses vertical rhythm. Scope `header.wrap` / `section.wrap`.
- Light + dark, desktop + mobile (380px), AA contrast.

## Anti-patterns
- One giant hand-coded HTML file for flagship work.
- Spacing by feel; >2 fonts; emoji/code-fonts as UI icons (use monoline SVGs).
- "Not X but Y" / "geen X, geen Y" antithesis copy — write declaratively.
- "As many animations as possible" with no taste budget.
- Inline-transcribing source videos — scrape captions (`yt-dlp --write-auto-sub`) instead.

## Resources
- getdesign.md · durable.com · demos.greensock.com · 21st.dev · awwwards.com
- Source learnings: Jono Catliff "How I Built INSANE Claude Design Websites In 10 Minutes" (yt xYv4_cTOSNM) — full notes in `knowledge/webdesign-claude-design-pipeline-xYv4/`.
