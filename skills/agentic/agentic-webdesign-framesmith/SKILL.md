---
name: agentic-webdesign-framesmith
description: Use Framesmith MCP server to give AI agents a visual design canvas — sketch UI, review in browser, agree on design before writing framework code. Scene graph → HTML/CSS → PNG rendering with evaluation and auto-fix.
metadata:
  source: agentic-webdesign-research 2026-07-04
  version: 1.7.0
tags: [visual-design, mcp-server, ai-design, canvas, framesmith]
---

# Framesmith — Visual Design Canvas for AI Agents

## What it is
Open-source MCP server (MIT) that gives AI coding agents a visual design canvas. Agents author UI via a scene graph, rendered as HTML/CSS through headless Chromium to PNG screenshots. Includes a standalone browser viewer, design evaluation, pattern library, and auto-fix.

## Quick start
```bash
# Start the viewer in a terminal
npx -p framesmith framesmith-viewer

# Add to Claude Code
claude mcp add framesmith -- npx framesmith
```

## MCP Tools

### Canvas Management
- `canvas_create` — Create a new canvas
- `canvas_bind` — Bind workspace/repo to framesmith
- `init` — Idempotent onboarding: bind repo, scaffold conventions, return workflow cheatsheet

### Design
- `batch_design` — Build UI with frames, text, icons, components, gradients. Returns `{ varName: nodeId }` map
- `apply_preset` — Apply a design preset
- `set_variables` — Set design tokens (colors, spacing, fonts)

### Evaluation & Fixing
- `canvas_evaluate` — Score 0-100 across 6 categories + cliché detection. Returns `READY`/`NOT READY`
- `canvas_autofix` — Mechanical fixes for flagged issues
- `canvas_revise` — Targeted revision for specific issues

### Export & Comparison
- `screenshot_responsive` — Preview at mobile/tablet/desktop
- `canvas_diff` — Visual before/after comparison
- `export` — Save to PNG/PDF

### Import
- `canvas_import_html` — Import existing HTML/CSS for inspection
- `canvas_import_url` — Import from live URL with drift detection
- `import_design_md` — Import DESIGN.md for token extraction

## Workflow

```
1. canvas_create → get canvas ID
2. apply_preset or set_variables → design tokens
3. batch_design → build the UI
4. canvas_evaluate → score the result
5. If < 95: canvas_autofix or canvas_revise → re-evaluate
6. screenshot_responsive → preview at breakpoints
7. canvas_diff → compare iterations
8. export → save final design
```

## Design System Support
- Workspace → project → canvas token inheritance
- DESIGN.md import
- Style presets (Material, glassmorphism, etc.)

## Pattern Library
11 vetted page archetypes + 5 component scaffolds, all scoring > 95. Taxonomy axes + diversification signal so successive screens vary.

## Viewer
- Gallery (`/`) — browse all canvases as clickable cards
- Project view (`/project/:id`)
- Canvas detail (`/canvas/:id`) — responsive viewports, Compare mode, JSON inspector
- Auto-refresh every 2 seconds during design
- Default port: 3001

## Storage
Open JSON in `.framesmith/` directory — committable, diffable, code-reviewable. The repo is the source of truth.

## Pitfalls
- Start the viewer BEFORE creating canvases — otherwise no visual feedback
- Use standalone viewer mode (not embedded) for long sessions
- Canvas IDs are re-keyed on `canvas_bind` — always use the returned IDs
- CSS gradients/shadows fixed in v1.2.0 (earlier versions crashed on screenshot)

## Supported Clients
Claude Code, Cursor, Windsurf, VS Code (Copilot), any MCP-compatible client.

## Version
v1.7.0 (June 2026). Active development, 15+ releases since v1.0.