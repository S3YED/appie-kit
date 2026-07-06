# Legal Design Research — Exa AI Deep Search (June 2026)

Bronnen gevonden via Exa neural search voor premium law firm website design. Gebruik deze als referentie bij advocatuur/legal redesigns.

## Internationale bronnen

| Bron | Samenvatting |
|------|-------------|
| [PxlPeak - 10 Best Law Firm Website Designs 2026](https://pxlpeak.com/blog/web-design/best-law-firm-website-designs-2026) | Dark sophistication, outcome visualization, "empathy for client + aggression toward adversary" |
| [PaperStreet - 2026 Law Firm Website Design Trends](https://www.paperstreet.com/blog/2026-law-firm-website-design-trends/) | Editorial-inspired layouts, bold typography, subtle motion, intentional photography |
| [Clio - Top 20 Best Law Firm Websites 2026](https://www.clio.com/blog/best-law-firm-websites/) | Trust/authority UX, premium typography, strategic content, fast performance |
| [Dan Gilroy - Law Firm Website Design Guide](https://www.dangilroy.com/law-firm-website-design-guide/) | 20+ years legal-specific design: legal is genuinely different from other professional services |
| [Attorney at Work - Law Firm Website Trends 2026](https://www.attorneyatwork.com/law-firm-website-design-trends-2026/) | Authority, trust, discoverability in a post-search world |
| [Smotrów Design - AVELLUM case study](https://smotrow.com/works/avellum) | Premium Ukrainian law firm - sophisticated digital ecosystem |
| [ArtVersion - Dinsmore brand refresh](https://artversion.com/portfolio/dinsmore/) | National law firm brand refresh + WordPress VIP deployment |

## Nederlandse bronnen

| Bron | Samenvatting |
|------|-------------|
| [Onwaarts - Vilen Advocatuur](https://www.onwaarts.nl/cases/vilen-advocatuur/) | Persoonlijk, praktisch en juridisch sterk — NL advocatuur design case |
| [iO Digital - Stibbe](https://www.iodigital.com/nl/cases/stibbe) | Vooraanstaand Benelux kantoor, UX en merkbeleving optimalisatie |
| [Evers+de Gier - Stadermann Luiten](https://www.eversendegier.nl/projecten/stadermann-luiten) | Advocaat met kennisbank (900+ artikelen), fotografie, visuele identiteit |
| [Mediabirds - Van Veen Advocaten](https://mediabirds.nl/cases/webdesign-ede-van-veen-advocaten/) | Kennisdeling voor autoriteit, SEO, snelle laadtijd |
| [Legalista - 7 Elementen](https://legalista.nl/de-advocatenwebsite-die-scoort/) | Advocatenwebsite die scoort: 7 elementen voor vindbaarheid en overtuiging |
| [WebDelft - Structuur advocatenwebsite](https://webdelft.com/insights/structuur-advocatenwebsite/) | Ideale structuur, wat verwachten bezoekers |
| [WebDelft - Online autoriteit](https://webdelft.com/insights/website-voor-advocatenkantoren/) | Hoe je online autoriteit en vertrouwen opbouwt |
| [IYFM - Noorlander Advocatuur](https://iyfm.nl/portfolio/noorlander-advocatuur/) | Stijlvol WordPress, SEO, FAQ-sectie, dedicated hosting |

## Design tokens voor "Suits style" legal sites

```css
--navy: #0f2644;        /* buttons, headings, brand */
--navy-deep: #06111f;   /* hero, footer, dark sections */
--ivory: #f5efe6;       /* backgrounds, light cards */
--champagne: #c9a76b;   /* accents, thin rules, gold details */
--champagne-light: #d9bd8a;
--charcoal: #1a232e;    /* body text */
--radius-sm: 2px;       /* buttons */
--radius-md: 4px;       /* cards */
--radius-lg: 6px;       /* containers */
```

## Key principes uit research

1. **Empathy + Authority**: warmte naar client, scherpte naar tegenpartij (PxlPeak)
2. **Dark sophistication**: diepe kleuren + serif typografie = institutional trust (PaperStreet)
3. **Sharp corners (2-4px)**: geen `rounded-full` op primary legal UI (Soleiman refinement)
4. **Editorial layout**: bold headlines, magazine-style sections (PaperStreet trend)
5. **Geen stock rechtbank/gavels**: echte portretten, kantoorcontext, desaturated (brand guide)
6. **Cinematic motion**: slow fade-up, subtiele parallax, geen bounce (Framer Motion)