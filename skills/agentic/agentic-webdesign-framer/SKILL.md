---
name: agentic-webdesign-framer
description: Use Framer 3.0 Agents and External Agents — AI-driven website building, design, and CMS management from Claude Code, Cursor, and Codex. Canvas-native agents generate pages, designs, layouts, code components, and run audits.
metadata:
  source: agentic-webdesign-research 2026-07-05
  last_updated: 2026-07-05
tags: [framer, ai-agents, visual-builder, mcp, website-builder, external-agents]
---

# Framer 3.0 — AI Agents for Visual Web Design

## What it is
Framer 3.0 (June 16, 2026) brings AI agents directly into the Framer canvas. Two modes:
1. **Framer Agents** (canvas-native) — AI works inside Framer, generating pages, writing code components, managing CMS, auditing SEO/accessibility
2. **External Agents** — Claude Code, Cursor, Codex, and other AI tools connect directly to Framer projects (no separate MCP setup needed)

Also: **Branching** for team collaboration — isolated branches, review, compare, merge approved changes.

## AI Credits
| Plan | Credits | Reset | Roughly |
|------|---------|-------|---------|
| Free | 500 | Daily | ~2 landing pages |
| Basic | 1,000 | Monthly | ~5 landing pages |
| Pro | 3,000 | Monthly | ~10 landing pages |

Editor seats: $20/mo (halved from $40).

## What Framer Agents Can Do
- Generate pages from scratch
- Generate designs from screenshots
- Handle responsive breakpoints
- Design within existing pages
- Create layouts and sections
- Organize color and text styles
- Add effects and interactions
- Write custom code components (React)
- Write and improve content
- Import and organize content
- Generate SEO metadata
- Manage CMS collections
- Create CMS detail pages
- Audit for broken links
- Audit accessibility issues
- Audit inconsistent styling

## External Agents Setup
Connect Claude Code, Cursor, or Codex without separate MCP setup:
1. Open Framer project → Settings → External Agents
2. Copy the connection string
3. Paste into your AI tool's configuration

External agents get access to the same canvas, CMS, styles, and publishing workflow.

## Open-Source MCP Server (alternative)
For custom setups, use the community MCP server:
```json
{
  "mcpServers": {
    "framer": {
      "command": "npx",
      "args": ["-y", "framer-mcp-server"],
      "env": {
        "FRAMER_PROJECT_URL": "https://framer.com/projects/YourProject--abc123",
        "FRAMER_API_KEY": "fr_your_api_key_here"
      }
    }
  }
}
```

## MCP Tools (community server)
- **CMS:** list/get/add/remove collection items, get field schemas
- **Design:** read page structure, apply canvas changes via DSL
- **Code:** list/get/set code component files (React)
- **Preview:** generate local HTML preview, publish deployments
- **Undo:** all write operations snapshot previous state for rollback

## When to Use
- Building marketing sites, landing pages, portfolios
- Teams that need visual design + AI assistance
- When you want AI to work inside a visual canvas (not just generate code)
- Rapid prototyping with design fidelity

## Pitfalls
- Complex web apps with custom logic/deeply nested components may need manual intervention
- Agent occasionally produces templated layouts despite respecting style systems
- AI credits consumed per agent action — monitor usage on high-iteration tasks
- External Agents is Framer-native (not open MCP) — locked to Framer's connection method
- Community MCP server is third-party, not official Framer

## Version
Framer 3.0, released June 16, 2026. All plans.