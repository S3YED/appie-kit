---
name: ui-ux-pro-max
description: "AI-powered design intelligence with 67+ UI styles, 161 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types. Use for UI/UX design decisions, color schemes, typography, design systems, landing pages, and pre-delivery checklists."
---

# UI/UX Pro Max

AI-powered design intelligence with 67+ UI styles, 161 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 15+ tech stacks.

## Prerequisites

Python 3.x (no external dependencies needed).

## Search Command

```bash
python3 {{SKILL_DIR}}/scripts/search.py "<query>" --domain <domain> [-n <max_results>]
```

### Design System Generation (start here for new projects)

```bash
python3 {{SKILL_DIR}}/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

Persist across sessions:
```bash
python3 {{SKILL_DIR}}/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

Page-specific override:
```bash
python3 {{SKILL_DIR}}/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

### Domain Search

```bash
python3 {{SKILL_DIR}}/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `product` | Product type recommendations | SaaS, e-commerce, portfolio, healthcare, beauty |
| `style` | UI styles, colors, effects | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Font pairings, Google Fonts | elegant, playful, professional, modern |
| `color` | Color palettes by product type | saas, ecommerce, healthcare, beauty, fintech |
| `landing` | Page structure, CTA strategies | hero, testimonial, pricing, social-proof |
| `chart` | Chart types, library recommendations | trend, comparison, timeline, funnel |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index, loading |
| `react` | React/Next.js performance | waterfall, bundle, suspense, memo, rerender |
| `web` | App interface guidelines | accessibilityLabel, touch targets, safe areas |
| `prompt` | AI prompts, CSS keywords | (style name) |

### Stack-Specific Search

```bash
python3 {{SKILL_DIR}}/scripts/search.py "<keyword>" --stack <stack>
```

Available stacks: `html-tailwind` (default), `react`, `nextjs`, `astro`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

### Output Formats

```bash
# ASCII box (default)
python3 {{SKILL_DIR}}/scripts/search.py "fintech crypto" --design-system

# Markdown
python3 {{SKILL_DIR}}/scripts/search.py "fintech crypto" --design-system -f markdown
```

## Workflow

| Scenario | Start From |
|----------|------------|
| New project / page | Step 1 → `--design-system` |
| New component | `--domain style` or `--domain ux` |
| Choose style / color / font | `--design-system` |
| Review existing UI | Pre-delivery checklist below |
| Fix a UI bug | Domain search for relevant area |
| Add charts / data viz | `--domain chart` |
| Stack best practices | `--stack <stack>` |

### Step 1: Analyze Requirements
Extract: product type, target audience, style keywords, tech stack.

### Step 2: Generate Design System (REQUIRED for new projects)
Run `--design-system` first. Always.

### Step 3: Supplement with Domain Searches
Deep-dive specific areas (style, color, typography, ux, etc.)

### Step 4: Stack Guidelines
Get implementation-specific best practices for the target stack.

## Pre-Delivery Checklist

### Visual Quality
- [ ] No emojis used as icons (use SVG: Phosphor, Heroicons, Lucide)
- [ ] cursor-pointer on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Official brand assets with correct proportions
- [ ] Semantic theme tokens (no hardcoded per-screen colors)

### Contrast & Color
- [ ] Light mode: text contrast ≥4.5:1
- [ ] Dark mode: primary ≥4.5:1, secondary ≥3:1
- [ ] Dividers/borders visible in both themes
- [ ] Color is not the only indicator

### Layout
- [ ] Responsive: 375px, 768px, 1024px, 1440px
- [ ] Safe areas respected for fixed elements
- [ ] 4/8dp spacing rhythm maintained
- [ ] Long text readable (not edge-to-edge on wide screens)

### Accessibility
- [ ] Focus states visible for keyboard nav
- [ ] prefers-reduced-motion respected
- [ ] Touch targets ≥44pt (iOS) / ≥48dp (Android)
- [ ] All meaningful images/icons have alt text / labels

### Interaction
- [ ] Touch feedback within 80-150ms
- [ ] Micro-interactions 150-300ms with native easing
- [ ] Disabled states visually clear and non-interactive
- [ ] No gesture conflicts in nested interactive regions
