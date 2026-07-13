---
name: agentic-webdesign-wordpress-mcp
description: Connect AI agents to WordPress via MCP — native WP 7.0 adapter, WP Navigator, NibWP, Publishio. AI agents create drafts, manage content, audit SEO, build pages, and switch page builders.
metadata:
  source: agentic-webdesign-research 2026-07-12
  last_updated: 2026-07-12
tags: [wordpress, mcp, ai-agents, headless-cms, wp-navigator, nibwp, publishio, wp-astro-mcp]
---

# WordPress MCP — AI Agent Ecosystem

## Overview
WordPress 7.0 (April 9, 2026) shipped native MCP adapter — the biggest update in WordPress history. Combined with a fast-growing third-party ecosystem, AI agents can now interact with any WordPress site through structured, permission-controlled MCP tools.

## WordPress 7.0 Core (Free, Built-in)

### What ships in core:
- **Native AI Client** — WordPress can call AI providers
- **Abilities API** — granular capability-based access control (replaces role-based permissions)
- **Connectors UI** — manage AI provider credentials in admin
- **MCP Adapter** — adapts every registered ability into MCP tools/resources/prompts
- **Expanded REST API** — analytics, user management, content scheduling endpoints. Response compression + conditional GET.

### How it works for AI agents:
1. WordPress site exposes MCP endpoint (built into core)
2. AI agent (Claude, Cursor, Codex) connects via MCP
3. Agent discovers capabilities: create drafts, audit content, manage taxonomies
4. All operations respect WordPress roles and permissions

### MCP Client Configuration

STDIO transport (local WP-CLI):
```json
{
  "mcpServers": {
    "wordpress": {
      "command": "wp",
      "args": ["--path=/path/to/wp", "mcp-adapter", "serve", "--server=mcp-adapter-default-server", "--user=admin"]
    }
  }
}
```

HTTP transport via remote proxy:
```bash
npx @automattic/mcp-wordpress-remote --url https://yoursite.com --user admin --app-password "XXXX XXXX XXXX XXXX"
```

MCP endpoint: `https://yoursite.com/wp-json/mcp/mcp-adapter-default-server`

### Headless pattern:
WordPress (MCP backend) → Next.js/Astro/Vite frontend → AI agent at content layer

## Third-Party Tools

### WP Navigator (wpnav.ai)
- **93 specialized MCP tools** — organized in dynamic toolsets for context efficiency
- **8×4 permission matrix:** None / Read / Suggest / Write across 8 categories
- **Plan-Diff-Apply workflow:** AI previews changes as diffs → review → approve/apply
- **Instant kill switch:** one-click termination of all AI sessions
- **Builder cookbooks:** compact references for Gutenberg, Elementor, WPBakery
- **Audit trail:** every AI action logged with who/what/when
- **Status:** MVP coming mid-2026 (waitlist)

### NibWP (nibwp.com)
- **132 tools, 26 categories, 33+ integrations** — WooCommerce, ACF, page builders, forms, CRM, LMS
- **Screenshot-to-build:** hand over screenshot/link/Figma → on-brand build in Bricks/Elementor/Etch
- **Page builder switching:** AI reads existing design, recreates in new builder (pixel-perfect)
- **3-step setup:** install plugin → paste one-line connection → start prompting
- **Status:** Live, production-ready

### Publishio (rtCamp, open source)
- **GPL-2.0 license** — free, open source
- **Block pattern intelligence:** reads `WP_Block_Patterns_Registry`, fills patterns with AI content
- **Section-by-section building:** each pattern previewed in chat before appending to draft
- **Schema-constrained editing:** AI edits only content values (headlines, body, images, buttons) — cannot touch markup/CSS
- **Yoast SEO integration:** handles slugs, excerpts, meta fields
- **AI skill file included:** teaches assistants WordPress content rules
- **Status:** Available now. Production-ready.

### WP Astro MCP (Community, open source)
- **57 specialized tools** across 9 groups: site management, content extraction, transformation, output, media, GitHub, export, sync, setup wizard
- **Router pattern:** 3 meta-tools (`wp_astro_run`, `wp_astro_help`, `wp_astro_describe`) — AI discovers tools conversationally
- **Full pipeline:** REST API → 13-step transformation → Astro scaffold → GitHub push → Vercel deploy
- **Webhook dispatcher:** auto-rebuild Astro frontend on WP publish (HMAC-signed, ~1-2 min)
- **Setup wizard:** single guided flow from "I have a WP blog" to "deployed Astro frontend on Vercel"
- **Status:** Production-ready. Active development.

## When to Use
- Any WordPress site you want to manage via AI agent
- Headless WordPress + Next.js stacks needing AI content operations
- Agency workflows: bulk updates, audits, client site management
- Page builder migrations (switch builders without manual rebuild)

## Pitfalls
- WordPress 7.0 MCP adapter requires WP 7.0+ (not available on older sites)
- WP Navigator is pre-release — not production-tested at scale
- NibWP's screenshot-to-build quality varies with design complexity
- Headless WordPress requires WPGraphQL setup for frontend frameworks
- MCP tools consume context budget — use dynamic toolsets (WP Navigator) or compact cookbooks

## Version
WordPress 7.0 (April 9, 2026). 40% of web market share.