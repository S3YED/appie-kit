---
name: 21st-dev
description: "Install and use 21st.dev components — the largest shadcn/ui-compatible registry of React + Tailwind + Framer Motion components (Magic UI, Aceternity UI, originui, eldoraui, kokonutui, Skiper UI, etc.). Use when the user wants Awwwards-tier homepage polish, animated heroes, marquees, bento grids, scroll reveals, pricing cards, testimonials, FAQ accordions, or any high-quality landing-page block. Stack: Next.js + Tailwind 4 + React 19 + framer-motion."
---

# 21st.dev

21st.dev is the "npm for design engineers" — an open-source community registry (MIT) of high-quality React + Tailwind components, blocks, and hooks. It is shadcn-compatible: every component is installed with the standard `npx shadcn@latest add` CLI, just pointed at a 21st.dev URL.

## Prerequisites

- Node 18+ and `npx`
- A Next.js / Vite / React Router / Astro project
- Tailwind CSS v3 or v4 (Tailwind 4 requires shadcn CLI v4+, March 2026 or newer)
- React 18 or 19
- shadcn initialized once (writes `components.json`, `src/lib/utils.ts`, `src/components/ui/button.tsx`, and shadcn theme tokens into `globals.css`)

## One-time setup (per project)

```bash
# Initialize shadcn — creates components.json, ui/, lib/utils.ts, theme tokens
cd <project-root>
npx --yes shadcn@latest init -d --force
```

`-d` uses defaults (Next.js template, base-nova preset). `--force` overwrites any prior config.

Important — **the init step rewrites `--background`, `--foreground`, `--primary`, `--accent` in `globals.css` to neutral oklch values**. If your project already has brand colors mapped to those CSS variables (Weblyfe does — emerald + gold + snow), you must restore the brand mappings immediately after init:

```css
:root {
  /* Keep brand vars */
  --brand-emerald: #247459;
  --brand-gold: #DFB771;
  --brand-snow: #F6FEFC;
  /* ... */

  /* Re-map shadcn slots to brand */
  --background: var(--brand-snow);
  --foreground: var(--brand-green-goblin);
  --primary: var(--brand-emerald);
  --accent: var(--brand-gold);
  /* keep the rest of shadcn's tokens (card, popover, secondary, border, ring, etc.) */
}
```

Also restore `--font-sans` if you use a custom font variable (shadcn replaces it with `var(--font-sans)`):

```css
@theme inline {
  --font-sans: var(--font-rethink), system-ui, sans-serif;
  --font-heading: var(--font-rethink), system-ui, sans-serif;
}
```

## Adding a 21st.dev component

Browse https://21st.dev → pick a component → click "Code" / copy the install URL. Then:

```bash
npx --yes shadcn@latest add "https://21st.dev/r/<author>/<component>" --yes
```

The CLI:
1. Creates `src/components/ui/<component>.tsx`
2. Installs npm dependencies (e.g. framer-motion, @radix-ui/*)
3. Patches `globals.css` with any required `@theme` keyframes / variables

Import with the alias:

```tsx
import { Marquee } from "@/components/ui/marquee";
```

## Component catalogue — best for Weblyfe homepage

Browse the full registry at https://21st.dev. Here are the picks most relevant to the Appie hero + TIPS structure:

| Use case | Component | Registry path |
|---|---|---|
| Hero with animated avatar + gradient | `magicui/animated-hero` | `https://21st.dev/r/magicui/animated-hero` |
| Hero with text shimmer + spotlight | `aceternity/spotlight` | `https://21st.dev/r/aceternity/spotlight` |
| Sticky scroll narrative (the TIPS reveal) | `aceternity/sticky-scroll-reveal` | `https://21st.dev/r/aceternity/sticky-scroll-reveal` |
| Logo / partner marquee strip | `magicui/marquee` | `https://21st.dev/r/magicui/marquee` |
| Customer-case bento grid | `aceternity/bento-grid` | `https://21st.dev/r/aceternity/bento-grid` |
| 3D card hover (case-study cards) | `aceternity/3d-card` | `https://21st.dev/r/aceternity/3d-card` |
| Pricing tier cards | `originui/pricing` (search `pricing-section`) | `https://21st.dev/community/components/s/pricing-section` |
| Testimonial marquee | `magicui/testimonial-marquee` | `https://21st.dev/r/magicui/testimonials` |
| Animated FAQ accordion | `kokonutui/faq-accordion` | `https://21st.dev/community/components/s/faq` |
| Animated number counter (KPIs) | `magicui/number-ticker` | `https://21st.dev/r/magicui/number-ticker` |
| Globe / world-map (Bangkok ↔ NL trust) | `magicui/globe` | `https://21st.dev/r/magicui/globe` |
| Particle / dot background | `magicui/particles` | `https://21st.dev/r/magicui/particles` |
| Animated beam (network diagram) | `magicui/animated-beam` | `https://21st.dev/r/magicui/animated-beam` |
| Border beam glow effect | `magicui/border-beam` | `https://21st.dev/r/magicui/border-beam` |

Many authors publish multiple variants (e.g. magicui has hero-pill, hero-video-dialog, hero-section). Always preview on 21st.dev before installing.

## Discovery workflow

1. Open https://21st.dev/s/<keyword> (e.g. `/s/hero`, `/s/pricing`, `/s/testimonial`)
2. Filter by Popular or Featured
3. Click a card → preview the live demo
4. Click "Code" → copy the `npx shadcn@latest add` URL
5. Paste into terminal in project root

For semantic search across the registry, the **Magic Console** (https://21st.dev/magic/console) offers free semantic component search and SVG icon search. Generation features (auto-creating bespoke variants) require the $20/month Pro plan but are not needed for installing existing components.

## Magic MCP (optional — paid feature)

For prompt-driven component generation inside Claude Code:

```bash
npx --yes @21st-dev/cli@latest install claude --api-key <KEY>
```

API keys come from https://21st.dev/magic/console. The MCP exposes `/ui` for prompt-to-component generation. **This is not required** — the free `npx shadcn add <url>` flow gives you every published component on the registry.

## Stack-specific notes for weblyfe-ai

- **Tailwind 4**: Already wired. shadcn v4 CLI (March 2026+) handles `@theme inline` and `@custom-variant dark` automatically.
- **Next.js 16 + React 19**: Fully supported. shadcn writes Server-Component-safe code by default.
- **framer-motion 12**: Already installed; many 21st.dev components depend on it and will reuse the existing version rather than re-installing.
- **Brand preservation**: After every `shadcn add`, scan `globals.css` for newly-added `--background` / `--primary` overrides and re-map to brand vars if needed. The CLI usually only appends `@theme` rules and keyframes (safe), but `init` is the one to watch.
- **Path aliases**: Components land in `src/components/ui/*.tsx` and import via `@/components/ui/*` and `@/lib/utils`. Already set up in `tsconfig.json`.
- **Dark mode**: shadcn writes a `.dark` block. We currently do not use dark mode on <project-domain> — leave the block in place but do not toggle the class.

## Smoke-test pattern

Always verify a new install with a throwaway page before integrating into the homepage:

```tsx
// src/app/labs/<component-name>/page.tsx
import { NewComponent } from "@/components/ui/new-component";

export default function Lab() {
  return (
    <main className="min-h-screen container py-24">
      <NewComponent />
    </main>
  );
}
```

Then `npm run build` to confirm it compiles end-to-end. Once verified, port the component into the real homepage section and delete the lab page (or keep `/labs/*` as a private gallery).

## Licensing

21st.dev itself is MIT. Individual components inherit each author's license — check the component page footer. Most are MIT/Apache and safe for commercial use. Aceternity UI, Magic UI, originui, kokonutui are all MIT.

## Red flags

- Some components depend on heavy 3D libs (three, @react-three/fiber, ogl). Check the `dependencies` block on the 21st.dev component page before installing — the CLI will pull them in silently.
- A few authors ship components that import paid Aceternity Pro assets. The free preview will install but render placeholder text. Read the component page carefully.
- If a component references `cn` from `@/lib/utils` and your project uses a different alias, edit the import after install.

## References

- Registry: https://21st.dev
- GitHub: https://github.com/serafimcloud/21st (MIT)
- Magic MCP (paid): https://github.com/21st-dev/magic-mcp
- shadcn v4 changelog: https://ui.shadcn.com/docs/changelog/2026-03-cli-v4
- Tailwind 4 + shadcn: https://ui.shadcn.com/docs/tailwind-v4
