---
name: baoyu-visual-skills
description: "Generate infographics, knowledge comics, and article illustrations using the baoyu system (by 宝玉/JimLiu). Covers 21 layouts × 21 styles for infographics, 6 art styles × 7 tones for comics, and 6 illustration types. All use image_generate tool with prompt-only workflow."
version: 1.0.0
author: Hermes Agent (adapted from baoyu-skills by JimLiu)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [baoyu, infographic, comic, article-illustration, image-generation, visual-content]
    related_skills: []
---

# Baoyu Visual Skills — Infographics, Comics & Article Illustrations

Three visual content generators from the baoyu suite (by 宝玉/JimLiu), all sharing the same `image_generate`-based backend, prompt-only workflow, and file structure conventions.

## Section 1: Infographics (baoyu-infographic)

21 layouts × 21 styles for creating information graphics, data visualizations, and educational diagrams.

### When to Use
User asks for infographic, visual summary, information graphic, "信息图", "可视化", or "高密度信息大图".

### Layouts (21)

| Layout | Best For |
|--------|----------|
| `linear-progression` | Timelines, processes, tutorials |
| `binary-comparison` | A vs B, before-after, pros-cons |
| `comparison-matrix` | Multi-factor comparisons |
| `hierarchical-layers` | Pyramids, priority levels |
| `tree-branching` | Categories, taxonomies |
| `hub-spoke` | Central concept with related items |
| `structural-breakdown` | Exploded views, cross-sections |
| `bento-grid` | Multiple topics, overview (default) |
| `iceberg` | Surface vs hidden aspects |
| `bridge` | Problem-solution |
| `funnel` | Conversion, filtering |
| `isometric-map` | Spatial relationships |
| `dashboard` | Metrics, KPIs |
| `periodic-table` | Categorized collections |
| `comic-strip` | Narratives, sequences |
| `story-mountain` | Plot structure, tension arcs |
| `jigsaw` | Interconnected parts |
| `venn-diagram` | Overlapping concepts |
| `winding-roadmap` | Journey, milestones |
| `circular-flow` | Cycles, recurring processes |
| `dense-modules` | High-density modules, data-rich guides |

### Styles (21)

`craft-handmade` (default), `claymation`, `kawaii`, `storybook-watercolor`, `chalkboard`, `cyberpunk-neon`, `bold-graphic`, `aged-academia`, `corporate-memphis`, `technical-schematic`, `origami`, `pixel-art`, `ui-wireframe`, `subway-map`, `ikea-manual`, `knolling`, `lego-brick`, `pop-laboratory`, `morandi-journal`, `retro-pop-grid`, `hand-drawn-edu`

### Workflow
1. Analyze content → save source + analysis files
2. Recommend 3-5 layout × style combinations based on content structure
3. Confirm with user (combination, aspect ratio, language)
4. Generate prompt using layout + style definitions → save to `prompts/infographic.md`
5. Generate image via `image_generate` → download URL to output directory
6. Report summary

Output structure: `infographic/{topic-slug}/` with `source`, `analysis.md`, `structured-content.md`, `prompts/`, and final PNG.

### Keyword Shortcuts
- `high-density-info` / `高密度信息大图` → auto-select `dense-modules` + `morandi-journal`/`pop-laboratory`/`retro-pop-grid`
- `infographic` / `信息图` → auto-select `bento-grid` + `craft-handmade`

---

## Section 2: Knowledge Comics (baoyu-comic)

Create educational/educational comics with flexible art style × tone combinations.

### When to Use
User asks for knowledge comic, 知识漫画, educational comic, biography comic, tutorial comic, or Logicomix-style.

### Art Styles (6)

| Style | Best For |
|-------|----------|
| `ligne-claire` (default) | Clear line, Tintin-style, clean storytelling |
| `manga` | Japanese manga aesthetics |
| `realistic` | Detailed, lifelike rendering |
| `ink-brush` | Traditional Chinese ink painting style |
| `chalk` | Chalkboard/classroom feel |
| `minimalist` | Simple, clean, icon-focused |

### Tones (7)
`neutral` (default), `warm`, `dramatic`, `romantic`, `energetic`, `vintage`, `action`

### Presets (5)
| Preset | Art + Tone | Special |
|--------|-----------|---------|
| `ohmsha` | manga + neutral | Visual metaphors, no talking heads, gadget reveals |
| `wuxia` | ink-brush + action | Qi effects, combat visuals, atmospheric |
| `shoujo` | manga + romantic | Decorative elements, eye details, romantic beats |
| `concept-story` | manga + warm | Visual symbol system, growth arc |
| `four-panel` | minimalist + neutral + four-panel layout | 起承转合 structure, B&W + spot color |

### Layouts
`standard` (default), `cinematic`, `dense`, `splash`, `mixed`, `webtoon`, `four-panel`

### Workflow
1. Analyze content → save source + analysis
2. Confirm style, tone, layout, aspect ratio with user
3. Generate storyboard + character definitions
4. Generate prompts per page (with character descriptions embedded)
5. Generate images via `image_generate` → download each to local PNG
6. Character sheet optional (human review artifact)

Output structure: `comic/{topic-slug}/` with `source`, `analysis.md`, `storyboard.md`, `characters/`, `prompts/`, and PNG pages.

### Character Consistency
- Character descriptions in `characters/characters.md` text format
- Embedded inline in every page's `image_generate` prompt
- PNG character sheet optional (human-facing, not input to image model)

---

## Section 3: Article Illustrations (baoyu-article-illustrator)

Analyze articles, identify illustration positions, generate images with Type × Style × Palette consistency.

### When to Use
User asks to illustrate an article, add images, generate illustrations for content, "为文章配图", or "illustrate article".

### Types (6)
| Type | Best For |
|------|----------|
| `infographic` | Data, metrics, technical |
| `scene` | Narratives, emotional |
| `flowchart` | Processes, workflows |
| `comparison` | Side-by-side, options |
| `framework` | Models, architecture |
| `timeline` | History, evolution |

### Styles
Core: `notion-style`, `warm-illustration`, `minimal-flat`, `tech-blueprint`, `watercolor`, `elegant-line`

Full style gallery: `references/styles.md`

### Palettes (optional)
`macaron`, `warm`, `neon` — override style's default colors. Or define custom palette.

### Workflow
1. Detect reference images (analyze via `vision_analyze` for style traits)
2. Analyze content (type, purpose, core arguments, positions for illustrations)
3. Confirm settings (preset/type, density, style, palette, language)
4. Generate outline with per-illustration entries
5. Generate prompts per illustration
6. Generate images via `image_generate` → download each
7. Insert `![](relative/path)` into article after corresponding paragraph

Output structure: `{output-dir}/` with `source`, `analysis.md`, `outline.md`, `prompts/`, and PNGs.

---

## Shared Conventions

### File Structure
```
{type}/{topic-slug}/
├── source-{slug}.{ext}
├── analysis.md
├── prompts/
│   └── NN-{type}-{slug}.md
└── NN-{type}-{slug}.png
```

### Aspect Ratio Mapping
| Storyboard/Design ratio | image_generate format |
|------------------------|-----------------------|
| `16:9`, `4:3`, `3:2` | `landscape` |
| `9:16`, `3:4`, `2:3` | `portrait` |
| `1:1` | `square` |

### Core Principles (All Baoyu Skills)
1. **Data integrity** — never summarize or paraphrase source statistics
2. **Strip secrets** — scan for API keys, tokens, or credentials before writing any output
3. **Prompt files are mandatory** — save prompt to disk before every `image_generate` call
4. **Always download** the URL returned by `image_generate` to a local file (the tool returns a URL, not a file)
5. **Use absolute paths for curl** — never trust persistent-shell CWD across batches
6. **Backup before regenerating** — existing files get `-backup-YYYYMMDD-HHMMSS` suffix

### `clarify` Timeout Handling
When `clarify` times out (no user response):
- Use best judgment for THAT question only
- Continue asking remaining questions if more are needed
- Surface the default visibly so user can correct later

---

## Pitfalls

1. **image_generate does not accept images** — it's prompt + aspect ratio only. Reference images must be described textually via `vision_analyze`.
2. **Always download URLs** — `image_generate` returns a URL, not a local path. Use `curl -fsSL "<url>" -o /abs/path/to/file.png`
3. **Absolute output paths** — never relative paths for `curl -o`; CWD can drift between batches
4. **No backend selection** — `image_generate` uses whatever model the user configured; don't write model names into prompts
5. **One concept per section** — each illustration/comic page/infographic section should convey one clear concept
6. **Comic Step 2 confirmation required** — don't skip style+tone confirmation
7. **Metaphors vs concepts** — illustrate the underlying concept, not the literal metaphor
8. **Character consistency is text-driven** — embed character descriptions in every page prompt