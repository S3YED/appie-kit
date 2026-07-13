---
name: agentic-webdesign-tailwind-v4-tokens
description: Build Tailwind v4 design token systems with @theme inline + OKLCH + color-mix(). Use when creating a new project with Tailwind v4, migrating from v3, or setting up a design system that AI coding agents should follow.
metadata:
  created: 2026-07-09
  author: Appie-1
  tags: [tailwind, design-tokens, oklch, css, shadcn, ai-agents]
---

# Tailwind v4 Design Tokens for AI Agents

## Purpose

Tailwind v4 moved configuration from `tailwind.config.js` to CSS, making design tokens natively readable by AI coding tools. This skill provides the canonical pattern for setting up design tokens that both humans and AI agents can use reliably.

## Why CSS-First Matters for AI Agents

AI coding tools (Claude, Codex, Cursor) read CSS natively. They do NOT always parse JavaScript config files correctly. Design tokens in CSS custom properties are universally understood.

## The 3-Layer Token Chain

```
CSS variables (:root/.dark) → @theme inline → Tailwind utility classes
```

### Step 1: Define tokens as CSS variables

```css
:root {
  --background: oklch(0.985 0.007 65);
  --foreground: oklch(0.155 0.015 55);
  --primary: oklch(0.21 0.02 265);
  --primary-foreground: oklch(0.985 0.003 65);
  --muted: oklch(0.955 0.01 65);
  --muted-foreground: oklch(0.52 0.015 55);
  --border: oklch(0.92 0.01 65);
  --ring: oklch(0.708 0.015 265);
  --radius: 0.75rem;
}

.dark {
  --background: oklch(0.23 0.008 260);
  --foreground: oklch(0.985 0.005 270);
  --primary: oklch(0.62 0.22 265);
  /* ... override all for dark mode */
}
```

### Step 2: Map to Tailwind with @theme inline

```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-border: var(--border);
  --color-ring: var(--ring);
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}
```

### Step 3: Use semantic utilities in components

```tsx
// ✅ GOOD — semantic tokens
<div className="bg-background text-foreground border-border rounded-lg">

// ❌ BAD — hardcoded values
<div className="bg-white text-gray-900 border-gray-200 rounded-lg">
```

## OKLCH Color Format

OKLCH is perceptually uniform — equal changes = equal visual shifts. Format: `oklch(lightness chroma hue)`
- Lightness: 0–1 (0 = black, 1 = white)
- Chroma: 0–0.4 (0 = gray, higher = more saturated)
- Hue: 0–360 (0 = red, 120 = green, 240 = blue)

### Auto-generating palettes with color-mix()

```css
@theme {
  --color-brand: oklch(59% 0.24 255);
  --color-brand-100: color-mix(in oklch, var(--color-brand) 12%, white);
  --color-brand-200: color-mix(in oklch, var(--color-brand) 25%, white);
  --color-brand-300: color-mix(in oklch, var(--color-brand) 40%, white);
  --color-brand-400: color-mix(in oklch, var(--color-brand) 70%, white);
  --color-brand-500: var(--color-brand);
  --color-brand-600: color-mix(in oklch, var(--color-brand) 85%, black);
  --color-brand-700: color-mix(in oklch, var(--color-brand) 70%, black);
  --color-brand-800: color-mix(in oklch, var(--color-brand) 55%, black);
  --color-brand-900: color-mix(in oklch, var(--color-brand) 35%, black);
}
```

## Dark Mode Setup

```css
@custom-variant dark (&:is(.dark *));
```

With next-themes:
```tsx
<ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
  {children}
</ThemeProvider>
```

## shadcn/ui Integration

- PostCSS: `@tailwindcss/postcss` (NOT the old `tailwindcss` plugin)
- Animation: `@import "tw-animate-css"` (NOT `tailwindcss-animate`)
- Config: `"tailwind.config": ""`, `"rsc": true`, `"cssVariables": true`

## Agent Design Rules

When instructing AI agents to build with Tailwind v4, include these rules:

```
- All colors: semantic tokens (bg-primary, text-muted-foreground)
- Never hardcode: bg-blue-500, text-gray-700, hex values
- Container queries: @md: not md: for component-internal breakpoints
- RSC: "use client" only for state/effects/event handlers
- Dark mode: always include dark: variants for colors, borders, shadows
- Colors in OKLCH: oklch(L C H) format
```

## Pitfalls

- **Missing @theme inline**: Variables defined but Tailwind doesn't know about them → no `bg-primary` autocomplete
- **Using hex in @theme**: Works but loses OKLCH benefits (perceptual uniformity, color-mix quality)
- **Old animation plugin**: `tailwindcss-animate` doesn't work in v4 → use `tw-animate-css`
- **Old PostCSS plugin**: `tailwindcss` in postcss.config → use `@tailwindcss/postcss`
- **Forgetting .dark block**: Dark mode works but all colors stay light → define every token in `.dark`

## Verification

1. `bg-primary` should autocomplete in your editor
2. `dark:bg-primary` should switch correctly with theme toggle
3. Inspect a component: colors should resolve to `oklch()` values, not hex
4. `bg-primary/50` should produce a semitransparent version (via color-mix)