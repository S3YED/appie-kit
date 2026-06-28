---
name: ai-course-transcripts
description: Full transcripts of the AI Model Factory by Herman Carter course (AI Influencer / spicy-creator playbook). 164 unique lesson transcripts with timestamped lines.
version: 1.0.0
created: 2026-05-07
license: private (course content, do not redistribute)
---

# AI Model Factory transcripts

This skill bundles the complete searchable transcripts of the **AI Model Factory by Herman Carter** course. The course covers building, growing, and monetizing AI-influencer (NSFW + SFW) accounts end-to-end on Instagram, Fanvue, and adjacent platforms.

## What's inside

164 unique lesson transcripts grouped by module (after content-hash dedupe of 178 raw files):

| Module | Lessons | Topic |
|---|---|---|
| 1. AI Influencer Course V2 | 54 | Phases 0-6: foundations, audience, character creation, IG setup, boosting, content, launch |
| 2. ComfyUI Masterclass | 8 | ComfyUI install + workflows for character generation |
| 3. Sugarlab AI Masterclass | 11 | Cloud alternative to ComfyUI for hands-off image gen |
| 4. Instagram Posts Masterclass | 3 | Photoshop + IG post specifics |
| 5. Fanvue Masterclass | 6 | Setting up Fanvue, content strategy, verification |
| 8. AI Influencer Course (LEGACY) | 53 | Older curriculum — useful comparison + extra material |
| 9. Instagram Reels Masterclass | 22 | Reels strategy: foundation, advanced, tips, American Gooners |
| 6. Vault | 2 | Bonus content (Fanvue Likes, ComfyUI LoRA) |
| _other | 5 | Misc unprefixed transcripts |

## Format

Each transcript is plain text with timestamped lines:

```
# LESSON_NAME
Source: /path/to/source.mp4

[0.0s - 3.0s] So you want to get yourself a really good banner...
[3.0s - 6.4s] There are two types of banners that perform best.
```

Format makes it easy to: cite specific lines, jump to source video frames, vector-index per chunk, or pipe through an LLM for summarization.

## How to use

- **Browse:** open `INDEX.md` and click any lesson.
- **Search by topic:** `grep -ril "ComfyUI" transcripts/` or use ripgrep for speed.
- **Semantic search:** index `transcripts/` directory into Pinecone (suggested namespace `ai-course`) or Chroma. Each transcript is small (1-10 KB), trivial to embed.
- **Q&A on the course:** ingest into a RAG pipeline. Course is opinionated and strategy-heavy, so a top-3 retrieval against transcripts answers most "what did the course say about X" prompts.

## Provenance

- Source: AI Model Factory by Herman Carter (paid Skool community).
- Downloaded as 91 MP4s on 2026-03-18 by Appie-Opus to `~/clawd/learning/ai-course/`.
- Re-transcribed by Wolfie (Harry Van Deursen's Mac Mini, `diddywolf888@100.102.181.116`) using faster-whisper. Job completed 2026-05-07.
- Pulled to Mac Mini at `~/clawd/learning/ai-course-transcripts/wolfie-knowledge/` then deduped + packaged into this skill.

## Related skills

- `comfyui` (Hermes builtin)
- `viral-shorts-course` (separate course, viral shorts creation)
- `agentic-video-tools` (production tooling shortlist)
