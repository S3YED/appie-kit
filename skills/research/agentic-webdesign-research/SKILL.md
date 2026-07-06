---
name: agentic-webdesign-research
description: Daily research into agentic web design tools, frameworks, shadcn/ui patterns, Magic UI, and workflows that help AI agents build better websites. Outputs structured knowledge into appie brain + cognify fleet KB.
metadata:
  schedule: daily at 07:00 AM Bangkok (00:00 UTC)
  author: Appie-1
tags: [research, webdesign, agentic, shadcn, ui, knowledge-ingest]
---

# Agentic Web Design Research

## Purpose

Daily deep research into the evolving ecosystem of agentic web design tools. The goal is to find frameworks, tools, repos, design systems, and workflows that help AI coding agents (Claude, Codex, Cursor, etc.) build better production websites.

## Research Topics (rotate per day)

| Day | Primary Topic |
|-----|--------------|
| Mon | shadcn/ui v4 blocks, themes, components, patterns |
| Tue | Magic UI, Aceternity, 21st.dev — animated/premium components |
| Wed | Agentic web frameworks (v0, Bolt, Lovable, Tempo, Windsurf) |
| Thu | Tailwind v4 + CSS — new patterns, container queries, design tokens |
| Fri | Production stack: Next.js 16, Vite, Remotion, motion libraries |
| Sat | Open source agentic tools: CLI tools, MCP servers for design |
| Sun | Webflow + AI: automation, headless CMS, Framer alternatives |

## Output Format

Each run writes to:
1. `~/clawd/appie-brain/memory/research/agentic-webdesign/YYYY-MM-DD.md` — structured research notes
2. Auto-creates or updates reusable skill files under `~/.hermes/skills/agentic-webdesign-research/`
3. Pushes to cognify fleet KB via `http://100.101.29.56:8765/cognify/ingest`

## Research Prompt Template

```
Research the latest developments in [TOPIC] that help AI coding agents build better production websites.
Focus on:
1. New frameworks, libraries, or tools released in the last 7 days
2. Significant updates to existing tools (new APIs, breaking changes)
3. Open source repos with active development
4. Design patterns that make AI-generated UIs look more professional
5. Production considerations: performance, accessibility, SEO

For each finding provide:
- Name and URL
- What problem it solves
- How it specifically helps AI agents generate better code
- Key version/release date
- Quality assessment (production-ready / experimental / concept)
```

## Ingestion

Push to cognify fleet KB after writing. The API uses `text` (not `content`) and `source` (not `agent`). Documents ~10KB need 120s timeout.

Use Python for reliability (avoids shell escaping issues):

```python
import json, urllib.request

file_path = "~/clawd/appie-brain/memory/research/agentic-webdesign/YYYY-MM-DD.md"
with open(file_path) as f:
    text = f.read()

payload = {
    "source": "appie-1",
    "namespace": "workspace:appie-1",
    "text": text
}

data = json.dumps(payload).encode()
req = urllib.request.Request(
    "http://100.101.29.56:8765/cognify/ingest",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=120) as resp:
    result = json.loads(resp.read())
    print(f"Ingested: {result['chunks']} chunks, {result['entities']} entities, {result['relations']} relations")
```

## Skills to Update

When research discovers a significant new tool or pattern, create or update a dedicated skill:
- `~/.hermes/skills/<tool-name>/SKILL.md` for reusable knowledge
- Format: YAML frontmatter + markdown body with usage examples
