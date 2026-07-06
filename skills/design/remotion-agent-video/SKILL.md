---
name: remotion-agent-video
description: "Remotion v4.0.4xx with agent skill support for AI-driven video creation. Covers programmatic video generation with React, the new effects ecosystem, and first-party agent skills."
author: Appie-1
tags: [remotion, video, react, ai, agent, effects, animation]
related_skills: [remotion-video-creation, remotion-best-practices]
---

# Remotion Agent Video Creation

Remotion v4.0.4xx lets you create videos programmatically with React — and now ships first-party agent skills.

## Agent Skills

Install Remotion's official skills for AI coding agents:

```bash
npx skills add remotion-dev/skills
```

This adds skills for: Claude Code, Codex, and Cursor with best practices for Remotion projects.

## New Effects (@remotion/effects)

v4.0.4xx adds a composable effects ecosystem:

| Effect | Description |
|--------|-------------|
| `cornerPin` | Perspective/distortion corner pinning |
| `lightTrail` | Motion light trail effect |
| `checkerboard` | Checkerboard transition pattern |
| `emboss` | 3D emboss effect |
| `gridlines` | Grid overlay |
| `zoomBlur` | Zoom-based radial blur |
| `radialProgressiveBlur` | Progressive blur from center out |
| `linearGradient` | Linear gradient overlay |

Composable: stack multiple effects on a single `<Sequence>`.

## Studio Improvements

- Element drag-and-drop in timeline
- Timeline edge dragging for trim
- Sequence renaming
- Inspector controls grouped by category
- Effect context menu
- Keyframe easing handles
- WebGL HtmlInCanvas callbacks preserved

## Player Improvements

```typescript
import { Player } from "@remotion/player";

<Player
  component={MyVideo}
  durationInFrames={120}
  compositionWidth={1920}
  compositionHeight={1080}
  fps={30}
  pixelDensity={2} // fine-grained quality control
/>
```

- Muted players skip AudioContext creation (avoids autoplay blocks)
- `pixelDensity` for fine-grained output quality

## Getting Started with AI Agents

```bash
# Create a new Remotion project
npx create-video

# Install agent skills
npx skills add remotion-dev/skills

# Start the Studio
npx remotion studio

# Render
npx remotion render
```

## AI-Driven Workflow

When using an AI agent with Remotion:

1. **Create project** via `npx create-video` with your template
2. **Load remotion-agent-video skill** so the agent knows the latest APIs
3. **Use @remotion/effects** for polished transitions (cornerPin, zoomBlur, etc.)
4. **Leverage agent skills** via `npx skills add remotion-dev/skills` for guided patterns
5. **Render with pixelDensity** for high-quality output

## Pitfalls
- Agent skills are new — verify suggested patterns against Remotion docs
- Effects system is composable but order matters (effects apply in sequence)
- Large projects may need `--timeout` flag on render command