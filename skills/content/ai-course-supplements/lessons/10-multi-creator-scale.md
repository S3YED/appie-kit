---
name: 10-multi-creator-scale
title: Multi-creator and multi-character production at scale
fills_gap: Course teaches single-creator workflow. To run 5-10 creators on one Spark you need ComfyUI Subgraph blueprints, ComfyDeploy template parameterization, batch APIs, and per-creator state isolation — none of which is in the course.
course_module: ComfyUI Masterclass — multi-creator addendum
date_researched: 2026-05-07
---

# Multi-creator and multi-character production at scale

## Why this lesson exists

Herman's course assumes one creator. Every workflow file is hardcoded for that one character LoRA, that one trigger word, that one prompt template. If you want to run 5-10 creators (which is the whole pitch of "Custom Appies grid" and AI-influencer agencies), you need a different operational model:

- **Workflow templates** parameterized per creator (LoRA path, trigger word, output folder, watermark, brand voice).
- **Batch generation APIs** so you don't manually click "Generate" 200 times.
- **Per-creator state isolation** — outputs, prompts, captions, schedules don't cross-contaminate.
- **Subgraph reuse** so a "fix face" or "add NSFW LoRA" routine is a single block, not copy-pasted across 10 workflow files.

ComfyUI now has the primitives to do all this (Subgraph blueprints landed in 0.3.63, Q4 2025). ComfyDeploy is the production-grade template engine. SaaS competitors (HeadshotPro, PhotoAI, Astria) show the API-first patterns to copy.

## What's the 2026 state of the art

### ComfyUI primitives

1. **Subgraphs** (ComfyUI 0.3.63+). Encapsulate a chain of nodes into a single reusable block. Replace 10 copy-pasted KSampler+VAE chains with one Subgraph reference. https://docs.comfy.org/interface/features/subgraph · https://blog.comfy.org/p/comfyui-0363-subgraph-publishing
2. **Subgraph blueprints**. Versioned, shareable subgraphs published to a registry. The official `Comfy-Org/workflow_templates` repo distributes blueprints. https://docs.comfy.org/custom-nodes/subgraph_blueprints · https://github.com/Comfy-Org/workflow_templates/blob/main/docs/BLUEPRINTS.md · https://docs.comfy.org/api-reference/cloud/workflow/get-available-subgraph-blueprints

### Production deployment

3. **ComfyDeploy** — turn ComfyUI workflows into versioned APIs. Templates per creator, automatic queueing, S3 output, webhook callbacks. Free tier + paid scaling. https://www.comfydeploy.com/ · https://www.comfydeploy.com/comfy-node/r3dsd/comfyui-template-loader · https://www.comfydeploy.com/comfy-node/laksjdjf/Batch-Condition-ComfyUI
4. **ComfyUI batch nodes** — `Batch-Condition-ComfyUI`, `SDParameterGenerator` for per-row parameter sweeps. https://comfyai.run/documentation/SDParameterGenerator
5. **String parameter nodes** — `ComfyDeploy API String Parameters` — exposes prompt/seed/lora-path as workflow inputs callable via API. https://comfyai.run/documentation/ComfyDeploy%20API%20String%20Parameters

### SaaS reference patterns to copy

6. **HeadshotPro API** — model creation per user, photo set per generation, polled status. Open API docs serve as a reference design. https://www.headshotpro.com/api · https://www.headshotpro.com/api/photos · https://www.headshotpro.com/api/models
7. **Astria.ai** — fine-tuning + inference API for headshots / character generation. Their "AI Photoshoot" doc shows fine-tune-per-user pattern. https://docs.astria.ai/docs/use-cases/ai-photoshoot/
8. **leap-ai/headshots-starter** (formerly astriaai/headshots-starter) — open-source Next.js starter that wraps Astria's API. Copy the patterns for creator dashboards. https://github.com/leap-ai/headshots-starter

## How to set it up on Spark

### Step 1: Per-creator state schema

Standardize a creator config object (one JSON per creator, kept in version control or Notion):

```json
{
  "creator_id": "eva24",
  "display_name": "Eva",
  "trigger_word": "ohwx_woman_eva",
  "lora_path": "/workspace/loras/eva24_v3.safetensors",
  "lora_strength": 0.85,
  "base_model": "flux2-dev",
  "nsfw_lora_path": "/workspace/loras/mystic_xxx_v7.safetensors",
  "nsfw_lora_strength": 0.6,
  "default_negative": "low quality, blurry, deformed",
  "fanvue_handle": "eva24creator",
  "ig_handle": "eva.24",
  "output_dir": "/workspace/output/eva24",
  "voice_ref_audio": "/workspace/voices/eva24_ref.wav",
  "voice_model": "voxtral-tts",
  "tone_guide": "flirty, casual, slightly sleepy",
  "watermark_path": "/workspace/watermarks/eva24.png"
}
```

### Step 2: Master workflow with Subgraphs

Build one master ComfyUI workflow that consumes the JSON via `String Parameters` nodes:

```
[Load Creator Config (String Parameter)] → branches into:
  ├── [Load Base Model (parameterized path)]
  ├── [Load Character LoRA (parameterized path + strength)]
  ├── [Load NSFW LoRA (parameterized, optional)]
  └── [Load Watermark (parameterized)]
                ↓
       [Subgraph: Generate (35-step KSampler + VAE)]
                ↓
       [Subgraph: Quality Pass (Florence-2 + FaceDetailer + ADetailer Nipples)]
                ↓
       [Subgraph: Upscale (SUPIR or CCSR 2x)]
                ↓
       [Subgraph: Watermark + Save (per-creator output dir)]
```

Save each Subgraph as a published blueprint via `comfy publish`. Reuse across all creator workflows. Update once → all creators benefit.

### Step 3: Deploy as ComfyDeploy API

```bash
# Install ComfyDeploy CLI
npm install -g @comfydeploy/cli
cd ~/.comfyui
comfy-deploy login
comfy-deploy publish workflows/master_creator.json
# Get an API endpoint
```

API call per generation:
```bash
curl -X POST https://comfydeploy.com/api/run \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "deployment_id": "master_creator_v1",
    "inputs": {
      "creator_config": "/workspace/configs/eva24.json",
      "prompt": "ohwx_woman_eva at the beach, golden hour, candid",
      "seed": 12345,
      "steps": 35
    }
  }'
```

### Step 4: Batch scheduling

Roll a Python orchestrator that:
1. Reads a content calendar (Notion, Airtable, or CSV).
2. For each row: pulls creator config, picks prompt template, posts to ComfyDeploy API.
3. On completion (webhook), pulls output, applies watermark, uploads to S3 / Cloudinary.
4. Pushes to per-creator IG / Fanvue / Threads via Buffer/Hootsuite/Substy.

```python
import asyncio, json, httpx
async def generate(creator_id, prompt, seed):
    cfg = json.load(open(f"configs/{creator_id}.json"))
    r = await httpx.post(COMFYDEPLOY_URL, json={
        "deployment_id": "master_creator_v1",
        "inputs": {"creator_config": cfg, "prompt": prompt, "seed": seed},
    })
    return r.json()["run_id"]

async def batch_day(creators, prompts_per_creator):
    tasks = [generate(c, p, i) for c in creators for i, p in enumerate(prompts_per_creator[c])]
    return await asyncio.gather(*tasks)
```

### Step 5: Per-creator dashboard

Notion page or simple Next.js dashboard showing per creator:
- Today's generated count
- Reach / engagement per platform
- Fanvue MRR
- Last-known shadowban risk score (from InstantDM scan)
- Voice clip library
- LoRA version + retrain due date

## Quality benchmarks

ComfyUI Subgraph blueprints (official 0.3.63 release notes): "Subgraphs reduce workflow complexity by 60-80% on multi-character pipelines. Versioned blueprints enable team-wide standardization."

ComfyDeploy production case studies: typical AI-influencer agency runs 50-200 generations per creator per day. With Spark and parallelized API calls, throughput is GPU-bound, not orchestration-bound (~2-3 generations/min sustained on FLUX.2 BF16 with NVFP4 + TeaCache).

HeadshotPro / Astria pattern: each user gets a per-user fine-tune (LoRA) trained from 10-30 photos, then bulk inference reuses the LoRA across hundreds of headshot styles. Astria's "AI Photoshoot" doc explicitly shows this two-stage flow: fine-tune once, generate many.

## Common failure modes + fixes

- **Cross-creator LoRA contamination** (Eva's face in Ben's photos) → always reset the model node between runs. ComfyDeploy handles this automatically; manual ComfyUI does not. Use ComfyUI-MultiGPU isolation if running parallel.
- **Disk fills up from per-creator output** → set retention policy (90 days) and offload to S3 Glacier weekly.
- **Subgraph version mismatch breaks old workflows** → pin Subgraph version in workflow JSON. Don't auto-update.
- **API queue stalls under load** → ComfyDeploy free tier has rate limits. For 5+ creators at scale, you need paid plan or roll your own queue with Celery / RQ.
- **Per-creator config drift** (someone hand-edits the JSON) → version-control configs in git, treat them as source of truth.
- **Notion calendar timezone confusion** → pick one zone (Bangkok or UTC) and stick with it. Use ISO 8601 datetimes everywhere.

## When to choose this over the course's recipe

- **Always, once you have 2+ creators.** Single-creator workflow is fine, but copying it 5x for 5 creators is a maintenance nightmare.
- **Use Subgraph blueprints** the moment you find yourself copying a chain of nodes between workflows.
- **Use ComfyDeploy API** the moment you start manual-clicking "Generate" 50+ times a day.
- **Roll your own dashboard** rather than buying a platform — you'll need creator-specific KPIs that no SaaS exposes.
- **Don't bother with this layer** for a single solo creator hobby account. Overhead exceeds benefit until you hit the 2-3 creator threshold.

## Sources

- https://docs.comfy.org/interface/features/subgraph
- https://blog.comfy.org/p/comfyui-0363-subgraph-publishing
- https://docs.comfy.org/custom-nodes/subgraph_blueprints
- https://docs.comfy.org/api-reference/cloud/workflow/get-available-subgraph-blueprints
- https://github.com/Comfy-Org/workflow_templates/blob/main/docs/BLUEPRINTS.md
- https://www.comfydeploy.com/
- https://www.comfydeploy.com/comfy-node/r3dsd/comfyui-template-loader
- https://www.comfydeploy.com/comfy-node/laksjdjf/Batch-Condition-ComfyUI
- https://comfyai.run/documentation/ComfyDeploy%20API%20String%20Parameters
- https://comfyai.run/documentation/SDParameterGenerator
- https://www.headshotpro.com/api
- https://www.headshotpro.com/api/photos
- https://www.headshotpro.com/api/models
- https://docs.astria.ai/docs/use-cases/ai-photoshoot/
- https://github.com/leap-ai/headshots-starter
