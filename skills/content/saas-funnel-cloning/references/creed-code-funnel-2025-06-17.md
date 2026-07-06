# Creed Code Funnel Clone — Session Log (2025-06-17)

**Source:** GoHighLevel preview URL
**Client:** Ibrahim Ramzy / Cali Creed
**Deployed:** https://creed-funnel.vercel.app
**Repo:** https://github.com/Ramzy-Creed/creed-code-funnel

## Brand Tokens (Extracted from GHL Source)

### Colours
| Token | Hex | Usage |
|-------|-----|-------|
| Dark Navy | `#072a42` | Primary background |
| Near Black | `#212121` | Section backgrounds, form modals |
| Dark Gray | `#303030` | Dividers |
| Medium Gray | `#4d4d4d` | Muted text |
| Text Gray | `#a2a1a6` | Body text |
| Light Gray | `#d0d0d2` | Border elements |
| Neon Green | `#39ff14` | Headline highlights, CTAs |
| Bright Green | `#00e676` | Gradient partner |
| Primary Green | `#37ca37` | Button primary |
| Gold | `#d4af37` | Secondary highlights, prices |
| Orange Gold | `#f79d0c` | Button gold gradient |
| Dark Gold | `#b8901f` | Dark gold accent |
| Blue | `#1475b6` | Inline links |
| Secondary Blue | `#188bf6` | Link colour |
| White | `#ffffff` | On dark backgrounds |

### Fonts
| Role | Font |
|------|------|
| Primary Headlines | **Montserrat** (600-700 weight) |
| Body / Text | **Plus Jakarta Sans** (400 weight) |
| Fallback | **Inter** (code/system) |

### CSS Variables From Source
```css
--primary: #37ca37;
--secondary: #188bf6;
--headlinefont: 'Inter';  /* actual rendering uses Montserrat */
--contentfont: 'Inter';   /* actual rendering uses Plus Jakarta Sans */
--text-color: #000000;
--link-color: #188bf6;
```

## Page Structure (All Sections in Order)

1. **Header** — Fixed nav, logo (left), CTA button (right)
2. **Hero** — Badge, heading stack (3 lines), italic sub, primary CTA, stats row
3. **Video Section** — Section label, description, video placeholder, CTA
4. **Testimonials** — 3x before/shift/result cards (Adeenah, Ashley, Fatima)
5. **Member Results** — Grid of 6+ quote cards with author names
6. **Scarcity CTA** — "One day or Day one?", spots counter (8/10), waitlist(38)
7. **Features/What You Get** — 6 feature grid with icons
8. **Coach Section** — Split layout: image (left) + bio (right), CTA
9. **Pricing** — 3 tiers (297/mo, 497/mo featured, 2997/yr)
10. **FAQ** — 5 accordion items
11. **Final CTA** — Secondary scarcity CTA
12. **Footer** — Logo, copyright, Facebook disclaimer

## Multi-Step Qualification Form

5-step modal flow triggered by ANY "Apply Now" button:

| Step | Question | Options |
|------|----------|---------|
| 1 | Primary goal? | Fat loss / Muscle / Health / Confidence |
| 2 | Days/week committed? | 2 / 3-4 / 5+ |
| 3 | Biggest struggle? | Motivation / Nutrition / Time / Knowledge |
| 4 | Commitment 1-10? | 1-3 / 4-6 / 7-8 / 9-10 |
| 5 | Contact details | Name / Email / Phone |

Hot leads (9-10 commitment, fat loss goal) get routed to high-ticket sequence.

## Thank You Page Flow

1. "Application Being Reviewed" headline
2. Check email + spam
3. **Urgency box**: "Your spot is not locked in yet — 8/10 spots remain"
4. **Calendar embed placeholder** — accepts any embed code
5. Russell Brunson "keep the loop open" principle (not confirmed, being reviewed)

## Conversion Optimisations Applied

- Russell Brunson Hook-Story-Offer on every section
- Real scarcity numbers
- Price anchoring (value before price)
- Questions that both engage AND qualify
- Thank you page keeps loop open
- Progress bar visible across 5-step form
- Shake animation on unselected steps
- Progress bar shows step completion