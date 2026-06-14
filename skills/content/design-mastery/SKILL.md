---
name: design-mastery
description: "Apply Appie and Weblyfe design principles for hierarchy, spacing, typography, color, UI polish, and premium minimal interfaces."
version: 1.0.0
category: content
---

# Design Mastery - Appie's Design Brain

**Doel:** Dit is mijn interne kennis voor design. Raadplegen bij ELK design project.

---

## Core Principes (Refactoring UI)

### 1. HIERARCHY IS EVERYTHING
- **Niet alle elementen zijn gelijk** — Bepaal wat belangrijk is VOORDAT je begint
- **Size isn't everything** — Gebruik ook weight, color, spacing voor hierarchy
- **De-emphasize to emphasize** — Maak secundaire content zachter, niet primary louder
- **Labels are a last resort** — Data kan vaak voor zichzelf spreken

### 2. LAYOUT & SPACING
- **Start with too much white space** — Makkelijker om weg te halen dan toe te voegen
- **8pt spacing system:** 8, 16, 24, 32, 40, 48, 64, 80px
- **You don't have to fill the whole screen** — Lege ruimte is geen verspilling
- **Avoid ambiguous spacing** — Elementen moeten duidelijk gegroepeerd zijn

### 3. TYPOGRAPHY
- **Establish a type scale:** 12, 14, 16, 18, 20, 24, 30, 36, 48, 60px
- **Max 2 fonts** — Meestal 1 is genoeg
- **Line length: 45-75 characters** — Nooit volle breedte tekst
- **Line-height:** 1.5 voor body, 1.2-1.3 voor headings
- **Letter-spacing:** Tighter voor headings, normal voor body

### 4. COLOR
- **Ditch hex for HSL** — Makkelijker om variaties te maken
- **Je hebt meer kleuren nodig dan je denkt** — 8-10 shades per kleur
- **Greys don't have to be grey** — Voeg een tint toe (warm/cool)
- **60-30-10 regel:** Primary 60%, Secondary 30%, Accent 10%
- **Max 3 kleuren + neutrals**

### 5. DEPTH & SHADOWS
- **Emulate a light source** — Shadows gaan consistent één kant op
- **Two-part shadows:** Een scherpe kleine + een zachte grote
- **Overlap elements** — Creëert lagen en diepte
- **Flat can have depth** — Gebruik kleur en spacing

### 6. FINISHING TOUCHES
- **Supercharge the defaults** — Bullets → icons, borders → shadows
- **Add color with accent borders** — Top/left borders in brand color
- **Use fewer borders** — Shadows of spacing zijn vaak beter
- **Empty states matter** — Nooit een lege pagina zonder guidance

---

## Laws of UX (Psychology)

| Law | Betekenis | Toepassing |
|-----|-----------|------------|
| **Fitts's Law** | Grotere targets = sneller te raken | Buttons minstens 44px, belangrijke acties groot |
| **Hick's Law** | Meer keuzes = langere beslissing | Limiteer opties, progressive disclosure |
| **Jakob's Law** | Users verwachten dat je site werkt zoals andere sites | Volg conventies, innoveer niet onnodig |
| **Miller's Law** | 7±2 items in werkgeheugen | Chunk informatie, max 5-7 menu items |
| **Von Restorff** | Het ding dat anders is wordt onthouden | 1 CTA opvallend, rest subtiel |
| **Aesthetic-Usability** | Mooie dingen voelen bruikbaarder | Investeer in visual polish |
| **Doherty Threshold** | Responses <400ms voelen instant | Animaties kort houden |

---

## Mijn Design Checklist

### Voor ik begin:
- [ ] Wat is de BELANGRIJKSTE actie op deze pagina?
- [ ] Wie is de gebruiker en wat willen ze?
- [ ] Welke bestaande sites doen dit goed? (referenties verzamelen)

### Tijdens design:
- [ ] Is de hierarchy duidelijk zonder kleur?
- [ ] Zijn alle spacings uit mijn 8pt systeem?
- [ ] Max 2 fonts, max 3 kleuren?
- [ ] Geen orphaned elementen (alles duidelijk gegroepeerd)?
- [ ] Line-length onder 75 characters?

### Voor oplevering:
- [ ] Empty states ontworpen?
- [ ] Mobile responsive?
- [ ] Contrast check (WCAG AA minimum)?
- [ ] Hover/focus states?
- [ ] Loading states?

---

## Mijn Defaults

### Spacing Scale (8pt)
```
4px   - icon padding, tight gaps
8px   - small gaps, icon margins
16px  - standard padding, gaps between related items
24px  - section gaps within components
32px  - gaps between components
48px  - section padding
64px  - large section gaps
96px  - hero padding, major sections
```

### Typography Scale
```
12px  - captions, labels, meta
14px  - secondary text, UI elements  
16px  - body text (base)
18px  - large body, intro text
20px  - small headings, card titles
24px  - H4, section titles
30px  - H3
36px  - H2
48px  - H1, page titles
60px  - Hero headlines
```

### Neutral Palette (Default)
```
50:  #fafafa  - backgrounds
100: #f4f4f5 - subtle backgrounds
200: #e4e4e7 - borders, dividers
300: #d4d4d8 - disabled text
400: #a1a1aa - placeholder text
500: #71717a - secondary text
600: #52525b - icons
700: #3f3f46 - body text
800: #27272a - headings
900: #18181b - primary text
950: #09090b - darkest
```

---

## Sites om te studeren (mijn referenties)

### Premium SaaS
- **Linear.app** — Clean, dark, fast
  - Dark mode als default = premium tech feel
  - Hoge information density zonder chaos
  - Subtle glows en gradients voor depth
  - Consistent spacing, alles aligned
  
- **Vercel.com** — Gradients done right
- **Stripe.com** — Typography master
- **Notion.so** — Whitespace, simplicity

### Landing Pages
- **Apple.com** — Hero mastery
- **Airbnb.com** — Trust building
- **Figma.com** — Playful maar pro

### Dark Mode Excellence
- **Raycast.com** — Glow effects
- **Arc.net** — Subtle gradients
- **GitHub.com** — Readable dark

---

## Wanneer te gebruiken

**ALTIJD** dit bestand lezen voordat ik een design maak.
**NA** elk design: checklist doorlopen.
**BIJ** feedback: principes gebruiken om te articuleren.

---

## Case Studies

### SAFESITE Security (2026-03-05)
**Project:** Elite security website for ex-military bodyguard
**Result:** Complete website in one session, client "wild" over quality

**What Worked:**
- **Framer Motion animations** — Staggered reveals, parallax, scroll-triggered
- **Iconography** — Lucide icons in service cards and stats made content scannable
- **Dark theme + amber accents** — Premium, tactical feel
- **Hero's Journey structure** — Story-driven sections that flow

**Key Learnings:**
1. **Word choice matters for targeting** — "Podium" targets performers, "Voorgrond" targets everyone
2. **Team messaging builds trust** — Even solo operators benefit from showing a network
3. **Corporate ≠ boring** — You can be professional AND have strong copy
4. **Stats with icons** — "24/7 Surveillance" with Eye icon > just text
5. **Anchor nav + scroll-mt** — Use `scroll-mt-24` to offset for fixed headers

**Reusable Patterns:**
- `AnimatedSection` component for scroll-triggered reveals
- `StaggerContainer` + `StaggerItem` for sequential animations
- `ImageReveal` with clip-path for dramatic image entrances
- `FloatingBadge` for overlapping stat callouts
- `HoverCard` for service cards with lift effect

**Client Feedback Applied:**
- Broader audience (executives, not just artists)
- More corporate/professional tone
- Team section added
- Name change based on brand direction

---

*Laatst bijgewerkt: 2026-03-05 11:37 PST*
*Case study toegevoegd: SAFESITE Security*
