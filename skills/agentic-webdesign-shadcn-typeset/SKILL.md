---
name: agentic-webdesign-shadcn-typeset
description: Use shadcn/typeset — a CSS-only styling system for HTML and rendered markdown. One class, streaming-safe, theme-aware. Use when styling raw HTML/markdown content in shadcn/ui projects for blog posts, docs, chat messages, or AI-generated content.
metadata:
  created: 2026-07-13
  source: shadcn/ui July 2026 changelog
  tags: [shadcn, css, typeset, markdown, streaming, styling]
---

# shadcn/typeset

A single CSS file that styles HTML elements and rendered markdown. Add one class, everything inside gets styled. No per-element classes needed.

## Quick Start

```bash
npx shadcn@latest add typeset
```

```tsx
<div className="typeset">{markdownContent}</div>
```

## Core Controls (3 CSS custom properties)

| Property | Purpose | Default |
|----------|---------|---------|
| `--typeset-size` | Base font size | Inherits from container |
| `--typeset-leading` | Line height multiplier | ~1.6 |
| `--typeset-flow` | Spacing between block elements | ~1em |

## Multiple Contexts

```css
.typeset-chat {
  --typeset-leading: 1.6;
  --typeset-flow: 1em;
}

.typeset-docs {
  --typeset-size: 15px;
  --typeset-leading: 1.75;
  --typeset-flow: 1.5em;
}
```

```tsx
<div className="typeset typeset-chat">{message}</div>
<article className="typeset typeset-docs">{page}</article>
```

## Why This Helps AI Agents

1. **Single class** — agents don't need to add per-element Tailwind classes
2. **Streaming-safe** — new blocks appended during streaming don't restyle earlier ones
3. **No dependencies** — CSS file lives in your project, no package layer
4. **Theme-aware** — uses your existing shadcn theme tokens (colors, fonts)
5. **Flexible** — create as many typesets as you need for different contexts

## Use Cases

- Blog posts rendered from MDX/markdown
- Documentation pages
- Chat message content (AI-generated markdown)
- Product descriptions
- Any content where you have raw HTML or markdown that needs consistent typography

## Pitfalls

- Typeset only styles semantic HTML elements (h1-h6, p, ul, ol, table, pre, code, etc.)
- If your content has class-based styling already, typeset won't override it
- For streaming, wrap only the content portion, not the entire conversation