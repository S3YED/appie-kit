# Luminaire Coaching — Implementation Reference

**Client:** Hamid Zahedi | **Deal:** €6,950 ex BTW | **Date:** 2026-07-09

## Stack

- Next.js 16 (Turbopack), TypeScript
- Three.js (`@react-three/fiber`, `@react-three/drei`) — 3D cosmic background
- GSAP + ScrollTrigger — hero animations, scroll reveals
- Lucide React — icon library
- TidyCal embed — booking
- Stripe Payment Links — checkout
- SchoolMaker/Skool — coaching platform (post-checkout)

## Color Tokens

```css
--canvas: #05080f;
--canvas-deep: #02040a;
--surface: #0a0e1a;
--surface-raised: #111527;
--ink: #f0ede5;
--ink-dim: #a09888;
--ink-muted: #6b6358;
--gold: #c9a84c;
--gold-bright: #e6c95e;
--gold-dim: #8b7235;
--gold-glow: rgba(201,168,76,0.18);
--gold-glow-strong: rgba(201,168,76,0.35);
--cosmic-purple: #5b4a9e;
--cosmic-indigo: #2a2455;
--line: rgba(255,255,255,0.06);
```

## Fonts

- **Cormorant** — serif, variable. Weights: 300-700. Headings, quotes, large text.
- **Hanken Grotesk** — sans, variable. Weights: 300-700. Body, UI, labels.

## 3D Background Pattern

Three.js particle galaxy:
- 800 particles, spherical distribution with clustering
- Colors: gold + white + purple mix with vertex colors
- Circular glow texture (Canvas API radial gradient)
- Two rotating torus rings (gold + purple, additive blending)
- Ambient sphere with shader material
- Mouse parallax (lerp-based, 0.02 smoothing)
- Scroll-driven zoom out
- Fade opacity on scroll

```typescript
// Key pattern: register GSAP ScrollTrigger conditionally
if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger);
}
```

## Quiz Scoring Pattern

```typescript
const steps = [
  { question: "...", answers: [
    { id: "a", label: "...", icon: <Icon />, score: { coaching: 3, alignment: 1 } },
  ]},
];

// Scoring: accumulate per-offer, threshold < 4 = downsell
function getRecommendation(scores: Record<string, number>) {
  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  if (sorted.length === 0 || sorted[0][1] < 4) return null; // downsell
  return recommendations[sorted[0][0]];
}
```

## Sources

- Brand assets: Google Drive `1MiutrpNCQAP8UiMSetj4M3FSc8wfploa`
- PRD: `projects/luminaire-coaching/PRD-FULL-SITE.md`
- Drive index: `projects/luminaire-coaching/DRIVE-INDEX.md`
- Site analysis: `projects/luminaire-coaching/site-analysis.md`
- Brand intake: `projects/luminaire-coaching/brand-strategy-intake.md`
- Offorte deal: https://weblyfe.offorte.com/viewer/194762/pp/nbtjzftCaC293693

## Deliverables (from Offorte)

1. Branding & Strategy — €650
2. Page Designs & Assets — €1,800
3. Building Pages + Interactions + Automated Emails — €3,000
4. Learning Platform Design & Development — €1,500
