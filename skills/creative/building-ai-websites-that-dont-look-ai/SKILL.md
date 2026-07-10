---
name: building-ai-websites-that-dont-look-ai
description: Use when building or reviewing a website with AI (Claude Design/Claude Code/Next.js) and it risks looking generic or "AI-generated" - flat backgrounds, no hover states, inconsistent spacing, dead static pages, single accent color, wall-of-text sections
---

# Building AI Websites That Don't Look AI-Generated

Distilled from a 67-min masterclass (YT 2Gda_ZvV1V4, transcript at `~/clawd/knowledge/webdesign-video-2Gda_ZvV1V4/transcript.txt`). Core thesis: AI sites look like slop because people start from a blank canvas. Fix: **extract a real brand's design system first, merge it with a proven layout structure, then layer design fundamentals on top.**

## The key insight

Separate **brand** from **structure** — they come from different sources:
- Brand kit (colors/type/radii/shadows): extract from a reference site's screenshots or a pre-built kit (Get Design has 71 brand kits as `design.md`)
- Page structure: a Dribbble screenshot that fits the BUSINESS TYPE (don't copy Stripe's software-company layout for a service business)
- Merge both in Claude Design: brand system + structure screenshot → hi-fi multi-page prototype → hand off to Claude Code ("copy it pixel for pixel", Next.js + Tailwind)

## Workflow (17 steps, condensed)

1. Pick style reference (screenshots) + structure reference (Dribbble: search "[niche] website")
2. Claude Design > Design Systems > upload screenshots or design.md > publish
3. Generate hi-fi prototype: name the pages, "use the brand design system for branding, use the attached screenshot for page structure"
4. Hand off to Claude Code; CLAUDE.md persona: "You are a senior UI designer and front end developer. You build premium, modern, elegant interfaces."
5. Layout: 6 decisions = direction, column ratio (60/40, 70/30 beats equal), container width, section rhythm, padding, alignment. Generous padding, applied consistently to ALL sections
6. Typography: 3 distinct font families (heading dark/bold/large, body lighter, caption in accent color); gradient on key heading words; roomy line-height
7. Imagery: Pixabay (royalty-free) + Freepik illustrations + Lucide icons. Never leave placeholders
8. "Expensive" backgrounds = LAYERS: solid + radial gradient + subtle noise/dot texture + grid + color blobs + frosted glass. "People won't see the noise, but it fills out the page"
9. Shadows = elevation (3D leap off the page); border radius identical everywhere (from the kit)
10. Hover/focus states with **300ms transitions** (never instant): buttons scale +10% + shadow, nav links get left-to-right underline, inputs get ring + ring offset, cards lift
11. Nav: sticky + frosted glass; mobile hamburger with slide-out
12. Dark/light toggle (optionally default by user timezone)
13. Motion: scroll-triggered pop-ins with STAGGERED delays (never simultaneous), logo marquee, count-up numbers, shimmer, floating elements. Prompt lever: "10x the amount of animations on this page", then dial back to taste
14. 3D hero: remix a Spline community scene, transparent bg, brand colors, export embed (caveat: ~5MB, hurts page speed)
15. AI video: Higgs Field MCP (`http://mcp.higgsfield.ai`, Seedance 2.0) — video bg also costs load speed
16. Responsive: "optimize for desktop, tablet and mobile" + verify in DevTools device emulation. **Mobile first: 70% of traffic**
17. Deploy: push to GitHub (private) > Vercel import > custom domain

## Anti-patterns (what screams "AI-generated")

| Anti-pattern | Fix |
|---|---|
| Blank-canvas start, no design system | Extract real brand kit first |
| Wrong structure for business type | Dribbble reference matching the niche |
| Single accent color + black/white | Full palette from the kit |
| Instant color-swap on hover / no states | 300ms transitions everywhere |
| Flat single-color backgrounds | Layered: gradient + noise + grid + blobs |
| All text same weight/size | 3-tier type hierarchy, 3 families |
| Tight padding, no breathing room | Generous consistent padding |
| Static dead page | Staggered scroll animations |
| Wall of text on about pages | Break with imagery |
| Desktop-only | Mobile first (70% of traffic) |
| Mixed border radii / shadows | One kit, reused everywhere |

## Tools quick reference

Claude Design (brand extraction + hi-fi prototypes) · Get Design (71 free brand kits) · Dribbble (structure) · Next.js + Tailwind + ShadCN · fonts.google.com · Pixabay / Freepik / Lucide · Spline (3D) · Higgs Field MCP (video) · GitHub + Vercel + Namecheap

House rules override video defaults where they conflict: image gen = nano-banana via fal.ai (never FLUX), 3D = fal.ai Hunyuan3D-2 first, design stack per `feedback_design_stack_for_weblyfe` (21st.dev + ui-ux-pro-max + Framer Motion/GSAP).

## Heuristics worth quoting

- "As long as you know what is possible to be built, Claude Code can design it and build it for you. You're the boss and it's the employee."
- Ring vs border: ring sits OUTSIDE the element; ring offset = white gap between border and ring
- Full-width dark sections must bleed to the edges — a cut-off dark background "just wouldn't look good"
