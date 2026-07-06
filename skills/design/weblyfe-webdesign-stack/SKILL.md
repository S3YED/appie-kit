---
name: legal-advocatuur-design-polish
description: "Class-level workflow for refining Dutch legal/advocatuur websites to a premium standard. Two aesthetic paths: Classic Sharp (Harvey Specter / Suits) and Mercury Premium (light-weight + pill CTAs)."
---

# Legal / Advocatuur Design Polish Reference

Class-level workflow for refining Dutch legal/advocatuur websites to a premium standard. Use for Soleiman-like boutique law firm projects.

Two aesthetic paths are documented below — choose based on the client brief and reference inspiration:

## Design Principles (shared)

- **Empathy + Authority**: warmth toward the client, sharpness toward the adversary
- **Dark sophistication**: deep navy/ink + champagne-gold accents
- **Typography**: editorial serif for display (Cormorant Garamond), clean sans for body (Manrope)
- **No gavels/scales** stock imagery; prefer real office context, desaturated photography

---

## Path A: Classic Sharp Polish (default)

Harvey Specter / Suits aesthetic. Sharp confidence, structured and traditional premium.

| Token | Value | Usage |
|-------|-------|-------|
| Navy | `#0f2644` | Buttons, headings, brand |
| Deep ink | `#06111f` | Hero, footer, dark sections |
| Ivory | `#f5efe6` | Backgrounds, light cards |
| Champagne | `#c9a76b` | Accents, thin rules, gold details |
| Charcoal | `#1a232e` | Body text |
| Button radius | `rounded-[4px]` | Sharp corners |
| Card radius | `rounded-[4px]` | Sharp corners |
| Shadows | `box-shadow` present | Structured card elevation |

### Find/replace pattern
| Pattern | From | To |
|---------|------|-----|
| Navy | `#102b4e` | `#0f2644` |
| Ink | `#071522` | `#06111f` |
| Champagne | `#b9945d` | `#c9a76b` |
| Ivory | `#f7f2ea` | `#f5efe6` |
| Button radius | `rounded-full` on buttons | `rounded-[4px]` |
| Card radius | `rounded-[5px]` | `rounded-[4px]` |
| Legal blue | `#184a78` | `#1a5276` |
| Muted text | `#43505b` | `#3a4753` |
| Text muted | `#5c6873` | `#4f5d6a` |

---

## Path B: Mercury Premium Polish

Inspired by Mercury (refero.style/3172cd4d). "Authority through restraint" — lighter, airier, with extreme typography and minimal chrome.

| Token | Value | Usage |
|-------|-------|-------|
| Navy deep | `#0a1628` | Hero, footer, dark sections (not `#06111f`) |
| Navy card | `#0f2644` | Section backgrounds |
| Champagne | `#d4b07a` | **Single accent** — CTA hover, icon accent only (not text, not borders) |
| Champagne subtle | `rgba(212, 176, 122, 0.2)` | Hover washes |
| Ivory | `#f4ede4` | Light canvas |
| Ivory card | `#faf6f0` | Card surface |
| Warm charcoal | `#2d3d4a` | Body text |
| Champagne wash | `rgba(212, 176, 122, 0.08)` | Subtle glow |

### Typography
| Role | Style |
|------|-------|
| Hero display | **72px / weight 300** (font-light), `tracking-[-0.04em]` |
| Section heading | 56px / weight 400, `tracking-[-0.03em]` |
| Subheading label | 12px uppercase, `track-[0.2em]`, `font-bold` |
| Body | 17px, `leading-[1.7]` |
| Font stack | Cormorant Garamond (300/500/600/700) + Manrope (400/500/600/700) |

### Buttons & radius
| Element | Style |
|---------|-------|
| Primary CTA | `rounded-full` (pill) |
| Secondary button | `rounded-full` (pill) |
| Cards | `rounded-[4px]` (keep sharp) |
| Input fields | `rounded-full` |
| Tags/chips | `rounded-full` |

### Elevation
- **No shadows on cards** — use 1px borders (`border border-[#0f2644]/8`) instead
- Card hover: `border-[#d4b07a]/20` + `hover:bg-white` (no translate)
- CTA: no shadow, let color speak
- Navy section: solid `bg-[#0a1628]` instead of overlay

### Section spacing
| Device | Section padding | Between sections |
|--------|----------------|-----------------|
| Mobile | `py-16` (64px) | `gap-12` |
| Tablet+ | `py-20` (80px) | `gap-16` |
| Desktop | `py-24` (96px) | `gap-20` |

### Navigation
- Fade-out on scroll down, fade-in on scroll up (use `framer-motion` with `useScroll` / `useMotionValueEvent`)
- Phone number as ghost button (`.border border-white/18`) instead of plain text
- CTA in header is pill-shaped

### Icons
- Replace Lucide static icons with Framer Motion animated SVG components for key spots (scale, heart, building, file, shield, phone, mail, check, arrow)
- If LottieFiles CDN blocks downloads (HTTP 403), do not fight it — use Framer Motion animated inline SVGs instead
- Lightweight: each icon adds ~0.5KB, no extra dependency, full color control, intersection-observer Pause/Play

### Scroll progress bar
- Thin gold line (3px), `origin-left scaleX` via `useScroll` + `useSpring`
- Color: `#d4b07a` (single solid, not gradient)

### Header fade-on-scroll pattern
```tsx
const [hidden, setHidden] = useState(false);
const [atTop, setAtTop] = useState(true);
const { scrollY } = useScroll();

useMotionValueEvent(scrollY, "change", (latest) => {
  const prev = scrollY.getPrevious();
  setHidden(latest > 120 && latest > (prev ?? 0));
  setAtTop(latest < 20);
});

<motion.header
  animate={{ y: hidden ? -100 : 0, opacity: hidden ? 0 : 1 }}
  transition={{ duration: 0.35, ease: "easeOut" }}
  className={`... ${atTop ? "border-transparent bg-transparent" : "border-white/10 bg-[#0a1628]/90 backdrop-blur-2xl"}`}
>
```

---

## Revision Workflow (shared)

1. **Research** — Exa AI for premium legal design references (PaperStreet, Clio, Dan Gilroy, Mercury, PxlPeak intl + Onwaarts, iO Digital, Legalista NL)
2. **Visual audit** — load live site in browser (Chrome DevTools MCP), screenshot, `vision_analyze` with a specific prompt
3. **PRD first** — document before/after, tokens, plan
4. **CSS tokens first** — update globals.css
5. **Bulk replace via subagent** — define ALL find/replace pairs in a structured list (color codes, radius tokens, button styles, shadow values), then dispatch a `delegate_task` with file paths and list. The subagent runs every replacement in sequence. Verify with `search_files` afterward. Saves ~15-20 manual patch calls.
6. **Also update components**: SiteHeader, ScrubHero, SiteFooter, TeamSection — these often have separate inline styles
7. **Build + preview deploy** (`npm run build`, then `vercel --yes`)
8. **Client review** on preview URL
9. **Production push**: GitHub auto-deploy (`git add && git commit && git push origin main`) or manual `vercel --prod --yes`
10. **Verify production URL** with `curl` and optionally a screenshot

## Research reference
Full Exa search results with URLs in `references/legal-design-exa-research-2026-06.md`