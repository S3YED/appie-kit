---
name: coaching-landing-pages
description: Build high-converting coaching, consulting, and infobusiness landing pages with quiz-based qualification, TIPS framework, and dark luxury design. Use when a client is a coach, consultant, or personal brand — NOT for SaaS or product pages.
version: 1.0.0
author: Appie
platforms: [linux, macos, web]
tags: [coaching, funnel, quiz, conversion, tips, infobusiness, landing-page]
---

# Coaching Landing Pages

**Extends:** `tips-landing-pages` for the coaching/infobusiness vertical.
**Applies to:** Coaches, consultants, personal brands, infobusiness owners.

---

## Core Rule: No Prices on Site

Coaching is a relationship sale. The price conversation happens on the call, after qualification. Never show prices on the landing page — use a quiz-based qualification funnel instead.

## Conversion Flow

```
Home (TIPS) → Quiz (4 stappen) → Resultaat
  ├─ Niet gekwalificeerd → Downsell (gratis lead magnet + email opt-in)
  └─ Gekwalificeerd → Booking pagina (TidyCal/Calendly embed)
       └─ Na call → Stripe checkout link (per SMS/email)
            └─ Thank-you pagina (video + platform link)
```

## Quiz-Based Qualification

De quiz vervangt de pricing table als core conversion mechanism.

### Mechanics
- 4 vragen, 4 antwoorden per vraag
- Elk antwoord kent scores toe aan aanbiedingen (`Record<string, number>`)
- Na 4 stappen: hoogste score bepaalt aanbeveling
- Drempel: score < 4 → downsell (niet genoeg signaal voor sales call)
- Lucide iconen per antwoord (herkenbaar, niet zweverig)

### Scoring Example
```typescript
const steps = [{
  question: "Wat brengt je hier vandaag?",
  answers: [
    { label: "Ik loop vast", score: { coaching: 3, alignment: 1 } },
    { label: "Succes maar leeg vanbinnen", score: { coaching: 3, circle: 1 } },
    { label: "Zoek richting", score: { alignment: 2, coaching: 1 } },
    { label: "Naar volgend niveau", score: { alchemist: 3, corporate: 1 } },
  ],
}];
```

## Pages (Complete Funnel)

| Route | Doel | Sleutelelement |
|---|---|---|
| `/` | TIPS landing page | 3D hero, visual storytelling, testimonials |
| `/quiz` | Standalone quiz | Geen afleiding, alleen quiz |
| `/quiz/downsell` | Niet-gekwalificeerd | Gratis lead magnet + email capture |
| `/quiz/book?offer=X` | Gekwalificeerd | TidyCal embed, aanbevolen offer |
| `/contact` | Contact formulier | Form + WhatsApp fallback |
| `/book` | Directe booking | TidyCal full-page |
| `/booked` | Bevestiging | Social proof + verwachtingen |
| `/checkout?offer=X` | Stripe redirect | Auto-redirect naar Stripe Payment Link |
| `/thank-you` | Post-checkout | Welkomstvideo + platform next steps |

## Design System (Dark Luxury)

```
--canvas: #05080f     near-black bg
--surface: #0a0e1a    cards
--ink: #f0ede5        warm white text
--ink-dim: #a09888    secondary text
--gold: #c9a84c       accent, CTAs
--gold-glow: rgba(201,168,76,0.18)
--cosmic-purple: #5b4a9e
```

**Fonts:** Cormorant (serif display) + Hanken Grotesk (sans body)
**Icons:** Lucide (`lucide-react`)
**Effects:** Glass morphism cards, gold glow orbs, 3D particle background (Three.js + GSAP)

## TIPS Adaptation for Coaching

| Fase | Section | Coaching-specifiek |
|---|---|---|
| **Tempt** | Hero + Pain | Emotionele hook: "Je hebt alles. Waarom voelt het leeg?" |
| **Influence** | Story + Social Proof | Founder's personal journey, echte klantfoto's, 3 testimonials met transformatie |
| **Persuade** | Method + Ladder | Framework (bijv. The Triangle), offer ladder zonder prijzen |
| **Sell** | CTA + FAQ + WhatsApp | Quiz CTA, FAQ voor bezwaren, WhatsApp fallback |

## Pitfalls

- **Nooit prijzen tonen** — de prijs komt op de call, niet op de site
- **Geen "koop nu" CTAs** — altijd "plan gesprek" of "ontdek je pad"
- **Downsell moet waardevol zijn** — niet als troostprijs voelen
- **Testimonials over transformatie**, niet over features
- **Echte klantfoto's, geen stock** — visueel vertrouwen is cruciaal bij personal brands
- **Geen emoji als icons** — gebruik Lucide of custom SVG

## References

- `references/luminaire-implementation.md` — Full Luminaire Coaching build: stack, tokens, fonts, quiz scoring, deliverables
- `references/google-drive-asset-indexing.md` — Python pattern for recursive Drive folder indexing + download via OAuth
- `references/threejs-cosmic-background.md` — Three.js particle galaxy pattern for dark luxury sites

Voor het lesplatform / community gedeelte na checkout:

| Platform | Prijs | Best For |
|---|---|---|
| SchoolMaker | €29/mo | Courses + community + coaching, white-label |
| Skool | €99/mo | Gamified community + courses |
| Hopper | €58/mo | Mobile-first, async coaching |

Default: SchoolMaker (beste prijs/kwaliteit voor coaching academies).
