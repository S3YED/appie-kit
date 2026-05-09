# content

Skills for design, visual production, code generation, and content creation. Use these when your Appie needs to produce UI components, generate images, write structured content, edit video, or apply design systems.

Prerequisite tools: varies per skill - Node.js/React for frontend skills, Python for image/video pipeline skills, `fal.ai` API key for AI image generation.

## Skills

| Skill | Description | Required env | Compat |
|-------|-------------|-------------|--------|
| [21st-dev](21st-dev/) | Install shadcn/ui-compatible React components from 21st.dev registry (Magic UI, Aceternity, etc.) | - | Both |
| [ai-course-supplements](ai-course-supplements/) | 17-lesson AI course supplement covering 2025-2026 model advances | - | Both |
| [ai-course-transcripts](ai-course-transcripts/) | 164 Herman Carter AI course transcripts for reference and study | - | Both |
| [appie-video-production](appie-video-production/) | End-to-end video production workflow: script, voiceover, b-roll, export | ELEVENLABS_API_KEY | Both |
| [architecture-diagram](architecture-diagram/) | Generate system architecture diagrams from descriptions via Mermaid or Excalidraw | - | Both |
| [ascii-art](ascii-art/) | Convert images or text to ASCII art for terminal display or plain-text output | - | Both |
| [ascii-video](ascii-video/) | Render video frames as ASCII animation in terminal | - | Both |
| [banner-design](banner-design/) | Multi-format banners across 22 art styles for social, ads, web, and print | FAL_API_KEY | Both |
| [baoyu-comic](baoyu-comic/) | Generate comic strips and sequential art panels | FAL_API_KEY | Both |
| [baoyu-infographic](baoyu-infographic/) | Generate structured infographics from data or bullet points | FAL_API_KEY | Both |
| [brand](brand/) | Brand identity, voice, messaging frameworks, asset management, design tokens | - | Both |
| [claude-design](claude-design/) | Claude-specific design patterns and component library for Anthropic-style UI | - | Both |
| [comfyui](comfyui/) | ComfyUI workflow automation for local Stable Diffusion pipelines | COMFYUI_URL | Both |
| [content-safe-zones](content-safe-zones/) | Safe zone guides for social media crop boundaries across platforms | - | Both |
| [design](design/) | Unified design skill: logo generation (55 styles), CIP mockups, banners, icons, social photos | FAL_API_KEY | Both |
| [design-mastery](design-mastery/) | Core design knowledge: hierarchy, spacing, typography, color, depth, UX laws | - | Both |
| [design-md](design-md/) | Markdown-to-designed-document pipeline with custom CSS themes | - | Both |
| [design-system](design-system/) | Token architecture: three-layer tokens (primitive/semantic/component), CSS variables, slide generation | - | Both |
| [excalidraw](excalidraw/) | Create and edit Excalidraw diagrams programmatically | - | Both |
| [frontend-design](frontend-design/) | Production-grade frontend UI patterns for React and HTML/CSS | - | Both |
| [frontend-design-3](frontend-design-3/) | Production-grade UI (React, HTML/CSS, Next.js, Vue). Bold typography, motion systems, gradient meshes | - | Both |
| [humanizer](humanizer/) | Rewrite AI-generated text to read more naturally for human audiences | - | Both |
| [nextjs-expert](nextjs-expert/) | Next.js 15 App Router specialist. Server Components, Server Actions, auth, caching, streaming | - | Both |
| [thumbnails](thumbnails/) | Generate YouTube and social media thumbnails with consistent branding | FAL_API_KEY | Both |
| [tips-landing-pages](tips-landing-pages/) | TIPS conversion framework (Tempt, Influence, Persuade, Sell) for landing pages | - | Both |
| [ui-styling](ui-styling/) | shadcn/ui + Tailwind CSS. Accessible components, dark mode, responsive layouts | - | Both |
| [ui-ux-pro-max](ui-ux-pro-max/) | Design decision engine. 67+ UI styles, 161 palettes, 57 font pairings, 99 UX guidelines | - | Both |
| [video-editing-pro](video-editing-pro/) | Cut-decision framework for short-form video. Pause thresholds, hook precision, energy curve, caption strategy | - | Both |
| [video-frames](video-frames/) | Extract, label, and process video frames for AI pipeline input | - | Both |
| [viral-shorts-course](viral-shorts-course/) | Framework for producing viral short-form video content (Reels, TikTok, Shorts) | - | Both |

## Install

```bash
cp -r skills/content/<skill> ~/.hermes/skills/
# or for OpenClaw:
cp -r skills/content/<skill> ~/.openclaw/skills/
```
