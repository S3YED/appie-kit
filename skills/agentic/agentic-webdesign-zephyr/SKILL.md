---
name: agentic-webdesign-zephyr
description: Use Zephyr Framework for zero-JS interactive web components with built-in MCP server, A2UI catalog, and Agent API. AI agents control live UI through typed tools, not generated markup.
metadata:
  source: agentic-webdesign-research 2026-07-04
tags: [web-components, zero-js, mcp-server, a2ui, agent-ui, zephyr]
---

# Zephyr Framework — Zero-JS Agentic Web Components

## What it is
"The first UI framework built for AI agents." 14 interactive web components (modal, tabs, accordion, toast, combobox, carousel, select, dropdown, datepicker, infinite scroll, sortable, file upload, virtual list, etc.) with pure CSS interactions. Zero runtime JavaScript after initial ~7KB page load. MCP server gives AI agents typed tools to control live components — they don't generate HTML, they interact with existing components.

## Quick start
```bash
# Scaffold new project
npx create-zephyr-framework my-app
cd my-app && npm start

# Or via CDN (zero build)
# Add two script tags, use components directly
```

## Core Packages
| Package | Description |
|---------|-------------|
| `zephyr-framework` | Core: 14 web components, CSS, agent API, A2UI catalog |
| `zephyr-framework-mcp` | MCP server: bridges Claude Desktop/Cursor/Windsurf to live components |
| `create-zephyr-framework` | CLI scaffolder with starter page |

## MCP Tools (6 typed tools)

```json
// Agents call these on live components
zephyr_get_state()      → JSON snapshot of all component states
zephyr_get_schema()     → Schema for all 14 components
zephyr_get_prompt()     → LLM context for prompting
zephyr_act(selector, action, args?)  → Execute action: open modal, switch tab, etc.
zephyr_describe(selector) → Deep inspect one component
zephyr_render(html)     → Render HTML into page
```

Agent doesn't see raw HTML — it sees typed tools with structured I/O:
```
zephyr_act('#modal-demo', 'open') → { success: true }
zephyr_get_state() → [{ id: "modal-demo", state: "open", actions: ["close", "toggle"] }, ...]
```

## Agent API (Browser)
```javascript
// Direct browser access for JS-based agents
Zephyr.agent.getState()     // Snapshot all components
Zephyr.agent.act('#id', 'action')  // Act on component
Zephyr.agent.describe('#id')       // Deep inspect
Zephyr.agent.render(html)          // Render HTML
Zephyr.agent.compose(components)   // Compose layout
Zephyr.agent.observe(callback)     // Watch state changes
Zephyr.agent.record() / replay()   // Record/replay interactions
Zephyr.agent.headless()            // Toggle fast mode
```

## A2UI Integration
Zephyr publishes `zephyr-a2ui-catalog.json` — Google's Agent-to-UI protocol catalog. Any A2UI-compatible agent (Gemini, CopilotKit) discovers Zephyr components without integration code.

## Drop-in Chat Widget
```html
<zephyr-agent-chat data-api-key="sk-..."></zephyr-agent-chat>
```
Visitors type natural language, agent controls UI. Works with Anthropic and OpenAI. Proxy mode for production.

## CSS-Only Interactions
- Modal: CSS Grid + `:has()` selector for open/close — no JS
- Tabs: View Transitions API for smooth slide animations
- Accordion: CSS `:has()` + `grid-template-rows` transition
- Carousel: CSS scroll-snap + `:has()` for prev/next
- Toast: CSS animations with auto-dismiss via `animation-delay`
- Dropdown/Combobox: `:focus-within` + keyboard nav

All GPU-accelerated, 60fps, zero main-thread overhead during interaction.

## Comparison
| | Zephyr | MCP Apps | AG-UI | Generative UI |
|---|---|---|---|---|
| Framework | None (Web Components) | React | React | React |
| Build step | No | Yes | Yes | Yes |
| Agent generates markup | No | Yes | No | Yes |
| Pre-built components | 14 + dashboard | None | None | None |
| MCP integration | Yes | Native | No | No |
| A2UI catalog | Yes | No | No | No |

## MCP Client Setup
```json
{
  "mcpServers": {
    "zephyr": {
      "command": "npx",
      "args": ["zephyr-framework-mcp"],
      "env": {
        "ZEPHYR_ROOT": "/path/to/project",
        "ZEPHYR_MCP_PORT": "3456"
      }
    }
  }
}
```

## Pitfalls
- Components require the framework JS to register custom elements (one-time, ~7KB)
- MCP server needs a running browser/page to connect to (WebSocket bridge on port 3456)
- Chat widget in production should use proxy mode (don't expose API keys in HTML)
- Dashboard add-on and runtime add-on are separate packages

## Version
MIT License. Active development. npm packages published and maintained.