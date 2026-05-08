---
name: ai-course-supplements
description: 17-lesson 2026-current supplement to the AI Model Factory by Herman Carter course. Each lesson fills a specific gap in Herman's 2025-vintage stack with the May 2026 state-of-the-art tools, models, and creator-tested techniques.
version: 1.1.0
created: 2026-05-07
license: private (research notes — Exa-sourced URLs, not redistributable course material)
related_skills: ai-course-transcripts, comfyui, agentic-video-tools, n8n-pro
---

# AI course supplements

Companion to `ai-course-transcripts` (Herman Carter's AI Model Factory course). Where the transcripts skill captures **what Herman teaches**, this skill captures **what Herman misses or gets wrong by 2026**.

## What's inside

17 lessons, one per topic gap, located in `lessons/`. Each lesson is 800-1500 words and follows a fixed structure:

1. Why this lesson exists (the gap)
2. What's the 2026 state of the art (concrete tools + versions)
3. How to set it up on Spark (commands)
4. Quality benchmarks (numbers + creator quotes)
5. Common failure modes + fixes
6. When to choose this over the course's recipe (decision rule)
7. Sources (5+ Exa-discovered URLs each)

## Lessons

| # | File | Gap filled |
|---|---|---|
| 01 | `lessons/01-character-consistency.md` | PuLID-FLUX2, InfiniteYou, OmniGen2, Flux.2 multi-ref replace paid Jack LoRAs |
| 02 | `lessons/02-lora-training.md` | ai-toolkit + kohya + FluxGym + correct hyperparameters fix Herman's "all came out like shit" |
| 03 | `lessons/03-image-models.md` | FLUX.2, Qwen-Image, Z-Image, HunyuanImage 3.0 supersede FLUX.1-dev FP8 |
| 04 | `lessons/04-video-models.md` | Wan 2.2 + Wan2.2-Animate + Wan2.2-S2V + HunyuanVideo 1.5 + LTX-Video v2 replace WAN 2.1 + Kling |
| 05 | `lessons/05-lipsync.md` | MuseTalk 1.5 + LatentSync + Wan2.2-S2V add talking-head capability the course skips |
| 06 | `lessons/06-voice-cloning.md` | F5-TTS + Voxtral TTS + OmniVoice replace ElevenLabs |
| 07 | `lessons/07-nsfw-techniques.md` | Z-Image base + ADetailer Nipples + Florence-2 + clothing-swap workflows beat course's YOLO + Damn Pony |
| 08 | `lessons/08-spark-blackwell-opt.md` | sm_121 SageAttention 2.2 + NVFP4 + TeaCache + cu130 PyTorch (Spark-specific, not in course) |
| 09 | `lessons/09-ig-fanvue-2026.md` | Updated shadowban patterns, Threads/Bluesky channels, Meta Verified, ManyChat funnels |
| 10 | `lessons/10-multi-creator-scale.md` | Subgraph blueprints + ComfyDeploy + per-creator config layer for 5-10 creator agencies |
| 11 | `lessons/11-auto-prompting.md` | DSPy + MIPROv2 + JoyCaption Two reverse-prompt + ComfyUI in-workflow LLM expansion |
| 12 | `lessons/12-post-processing.md` | SUPIR + ImpurePores LoRA + Optical-Realism + Magnific local replicas obsolete Photoshop + CCSR + Enhancer.AI |
| 13 | `lessons/13-spark-only-workflows.md` | Wan 2.2 14B BF16, HunyuanVideo 1.5 + DisCa, multi-character batch, NVFP4 + FLUX.2, concurrent multi-modal pipelines, on-prem privacy — workflows that don't fit on a 4090 |
| 14 | `lessons/14-pricing-and-revenue-2026.md` | Fanvue tier benchmarks ($4.99-$30+ subs, $0-$50k+ MRR distribution), PPV pricing curves, Spark vs RunPod vs SaaS margin math, top-earner profiles (Lani $60k, Ami BNW $50k, Lily Hayes £3k) |
| 15 | `lessons/15-content-calendar-90-day.md` | Day-by-day 12-week launch calendar from aged IG to first $1k month — warmup, Reels ramp, funnel switch-on, paid ads, customs, ambassador application |
| 16 | `lessons/16-legal-rights-and-takedowns.md` | Fanvue TOS, Meta NSFW policy, EU AI Act Article 50 (live 2 Aug 2026), TN ELVIS Act, DMCA procedure, right of publicity, IRS 1099-K $20k+200 threshold, NL ZZP/BV + EU VAT |
| 17 | `lessons/17-automation-and-orchestration.md` | n8n + Hermes blueprint for 5-creator agency: ComfyUI → R2 → Notion → Fanvue webhooks → ManyChat → Telegram multi-bot per creator |

## How this skill complements `ai-course-transcripts`

- `ai-course-transcripts` is the canonical record of what Herman taught.
- `ai-course-supplements` is the diff against 2026 reality.

Use them together:

```
# Look up what Herman said about <topic>
grep -ril "<topic>" ~/clawd/skills/ai-course-transcripts/transcripts/

# Then check what's better in 2026
ls ~/clawd/skills/ai-course-supplements/lessons/ | xargs -I{} grep -l "<topic>" ~/clawd/skills/ai-course-supplements/lessons/{}
```

For RAG: index both skills into the same vector store (e.g. `ai-course` namespace in Pinecone). Tag chunks by source (`transcripts` vs `supplements`) so retrieval can prioritize one or the other.

## Provenance

Research conducted 2026-05-07 by Appie-Opus on Mac Mini using Exa AI search across r/comfyui, r/StableDiffusion, Civitai, GitHub repos, NVIDIA dev blogs, arxiv papers, FanVue creator threads, Reddit, Skool community posts, IRS / EU Commission / state-law primary sources, Fanvue / ManyChat / Notion / n8n developer docs. Total ~85 Exa queries across two batches (lessons 1-12 plus 13-17 supplement, 2026-05-07).

Each lesson cites at least 5 Exa-discovered URLs. All sources are dated where the source provides a date. Tools and model versions reflect the May 2026 state of the field.

## When to update

- **Per quarter**: refresh `03-image-models.md`, `04-video-models.md`, `05-lipsync.md`, `06-voice-cloning.md`, `13-spark-only-workflows.md`. Frontier models and hardware-specific workflows churn fast.
- **Per major Meta/Fanvue update**: refresh `09-ig-fanvue-2026.md` and `14-pricing-and-revenue-2026.md`. Algorithm and platform policies shift.
- **Per major regulatory event**: refresh `16-legal-rights-and-takedowns.md`. Watch EU AI Act enforcement (post-2 Aug 2026), new US state deepfake bills, IRS threshold changes.
- **Per Fanvue / ManyChat / n8n API breaking change**: refresh `17-automation-and-orchestration.md`.
- **As needed**: `01`, `02`, `07`, `08`, `10`, `11`, `12`, `15` are stable until major underlying tech or platform changes.

## Related skills

- `ai-course-transcripts` (sibling — Herman's course material)
- `comfyui` (Hermes built-in — operational ComfyUI ops)
- `agentic-video-tools` (production tooling shortlist)
- `appie-video-production` (Appie-fleet video pipeline)
