---
name: tailwind-v4-shadcn-setup
description: "Set up Tailwind CSS v4 + shadcn/ui for a new Next.js SaaS project in 2026. Covers CSS-first @theme configuration, OKLCH colors, tw-animate-css, container queries, RSC optimization, and all critical gotchas."
tags: [tailwind, shadcn, nextjs, rsc, design-tokens, setup]
---

# Tailwind CSS v4 + shadcn/ui Setup for AI Agents

Use this skill when setting up a new Next.js project with Tailwind CSS v4 and shadcn/ui, or when writing code for one. It encodes all the critical gotchas that differ from Tailwind v3.

## Quick Setup

```bash
# 1. Create Next.js project
npx create-next-app@latest my-app --typescript --tailwind --app

# 2. shadcn/ui init (auto-detects Tailwind v4)
npx shadcn@latest init

# 3. Add core components
npx shadcn@latest add button card input dialog tabs select form

# 4. Install tw-animate-css (replaces tailwindcss-animate)
npm install tw-animate-css
```

## globals.css Template

This is the canonical globals.css for Tailwind v4 + shadcn/ui:

```css
@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

@theme inline {
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);

  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-border: var(--border);
  --color-ring: var(--ring);
  --color-input: var(--input);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
}

:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.96 0.01 264);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.96 0.01 264);
  --muted-foreground: oklch(0.46 0.02 264);
  --accent: oklch(0.96 0.01 264);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.53 0.22 27);
  --destructive-foreground: oklch(0.985 0 0);
  --border: oklch(0.91 0.01 264);
  --input: oklch(0.91 0.01 264);
  --ring: oklch(0.205 0 0);
  --chart-1: oklch(0.55 0.22 250);
  --chart-2: oklch(0.63 0.18 170);
  --chart-3: oklch(0.45 0.14 40);
  --chart-4: oklch(0.68 0.19 300);
  --chart-5: oklch(0.58 0.16 10);
  --radius: 0.5rem;
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.145 0 0);
  --card-foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.26 0.02 264);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.26 0.02 264);
  --muted-foreground: oklch(0.64 0.02 264);
  --accent: oklch(0.26 0.02 264);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.55 0.22 27);
  --destructive-foreground: oklch(0.985 0 0);
  --border: oklch(0.26 0.02 264);
  --input: oklch(0.26 0.02 264);
  --ring: oklch(0.84 0.01 264);
  --chart-1: oklch(0.65 0.22 250);
  --chart-2: oklch(0.70 0.18 170);
  --chart-3: oklch(0.68 0.14 40);
  --chart-4: oklch(0.72 0.19 300);
  --chart-5: oklch(0.65 0.16 10);
}

/* Override with your brand colors */
:root {
  --primary: oklch(0.55 0.22 250);        /* your brand blue */
  --primary-foreground: oklch(0.98 0 0);   /* white text on primary */
  --radius: 0.5rem;
}
.dark {
  --primary: oklch(0.70 0.18 250);         /* lighter for dark mode */
  --primary-foreground: oklch(0.10 0 0);   /* dark text on primary */
}
```

## components.json Template

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/styles/globals.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "iconLibrary": "lucide",
  "aliases": {
    "components": "@/shared/components",
    "utils": "@/shared/utils",
    "ui": "@/shared/components/ui",
    "lib": "@/lib",
    "hooks": "@/shared/hooks"
  }
}
```

## Container Queries Pattern

Use container queries for truly reusable components:

```tsx
// Parent — establish the container
<div className="@container">  {/* or @container/card for named */}
  <ProductCard />
</div>

// Child — respond to container, not viewport
function ProductCard() {
  return (
    <div className="flex flex-col @md:flex-row @lg:gap-8">
      <Image className="w-full @md:w-1/3" />
      <div>
        <h3 className="text-lg @md:text-xl @lg:text-2xl font-bold">Title</h3>
        <span className="hidden @sm:inline text-primary">$29.99</span>
      </div>
    </div>
  );
}
```

## Critical Gotchas

| # | Gotcha | What to do |
|---|--------|------------|
| 1 | `tailwindcss-animate` doesn't work in v4 | Use `tw-animate-css` instead — import in CSS: `@import "tw-animate-css"` |
| 2 | OKLCH, not HSL | shadcn 2.3.0+ uses OKLCH color space. Use `oklch()` not `hsl()` |
| 3 | Container parent needs measurable width | Flex columns with no explicit width break container queries |
| 4 | `@md:` ≠ `md:` | `@md:` = container query, `md:` = viewport media query. Don't mix |
| 5 | shadcn components.json needs `"rsc": true` | Required for Server Component projects |
| 6 | Static shadcn components are server-safe | Interactive ones (Dialog, Dropdown) include 'use client' already — no need to wrap |
| 7 | Tailwind v4 is incompatible with Sass/Less | CSS-first @theme directive: Sass can't parse it. Use plain CSS |
| 8 | No `forwardRef` in components | v4 uses `React.ComponentProps<typeof Button>` + `data-slot` attributes |
| 9 | Default style deprecated | New projects use `"style": "new-york"` exclusively |
| 10 | Toast deprecated | Use `sonner` instead |

## Design Token Hierarchy

```
Brand tokens (--brand-blue-500) → Semantic tokens (--color-primary) → Component tokens (--button-bg)
```

Use semantic tokens in your CSS. AI agents (Claude Code, Cursor) parse CSS variables more reliably than JS config files.

```css
@theme {
  /* Brand tokens */
  --color-brand-blue: oklch(0.55 0.22 250);
  --color-brand-green: oklch(0.63 0.18 170);

  /* Semantic tokens (map brand values) */
  --color-primary: var(--color-brand-blue);
  --color-success: var(--color-brand-green);
}
```

## RSC Optimization

- **Server components** for all static Tailwind-styled UI (no `'use client'`)
- **Client islands** only where state/events exist
- **Variant computation** server-side with class composition, not runtime

```tsx
// ✅ Server Component — styling is just inert strings
function ProductCard({ title, price }: { title: string; price: number }) {
  const sizeClass = price > 100 ? 'text-xl' : 'text-base';
  return (
    <div className="rounded-lg border p-4">
      <h2 className={`font-bold ${sizeClass}`}>{title}</h2>
    </div>
  );
}
```

## Reference Documents

- `references/research-2026-07-02.md` — Full research context with source URLs, MCP server evaluation table, and all 10 AI agent gotchas in one place.

## MCP Servers for Tailwind (recommended)

Install these in your Hermes/Claude config:

```json
{
  "mcpServers": {
    "tailwindcss-docs-mcp": {
      "command": "npx",
      "args": ["-y", "tailwindcss-docs-mcp"]
    },
    "designmcp-server": {
      "command": "npx",
      "args": ["-y", "@cdej-lgtm/designmcp-server"]
    }
  }
}
```

- `tailwindcss-docs-mcp`: Local semantic search over Tailwind docs (v3 + v4)
- `designmcp-server`: shadcn/ui theming with OKLCH color science