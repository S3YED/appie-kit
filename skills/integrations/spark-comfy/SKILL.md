---
name: spark-comfy
description: Generate images via Spark Atlas's ComfyUI inference API. SDXL + FLUX schnell, style presets, queue + status polling, Tailnet-only access with X-API-Key auth.
version: 1.0.0
author: appie-opus
license: MIT
prerequisites:
  env_vars: [SPARK_API_KEY]
  commands: [curl, python3]
metadata:
  hermes:
    tags: [image-generation, ComfyUI, SparkAtlas, FLUX, SDXL, GPU]
    homepage: https://github.com/S3YED/appie-kit
---

# Spark Atlas — Fleet Image Generation

Spark Atlas is the Weblyfe fleet's on-prem DGX Spark inference box (Tailscale-only endpoint set by `SPARK_BASE`). It runs ComfyUI behind a FastAPI wrapper called `spark-api` on port `8190`. Any Appie on the tailnet can render images by hitting it.

This skill is the client side: a thin Python helper and copy-paste curl examples.

## Prerequisites

1. Be on the same Tailnet as Spark Atlas. Test with:
   ```bash
   curl -s $SPARK_BASE/health | jq .
   ```
   Should return `{"status": "healthy", "comfyui": "connected", ...}`.

2. Have an API key. Set it in your `~/.hermes/.env` (or your shell env):
   ```
   SPARK_API_KEY=spark_<your-handle>_<hex>
   ```
   Seyed provisions keys via Spark's `~/.hermes/.env` `SPARK_API_KEYS` list. Ask if you don't have one.

3. The Python helper imports the standard library only (`urllib`, `json`, `time`, `os`). No extra installs needed.

## Quick reference

| Endpoint | Method | Auth | Purpose |
|---|---|---|---|
| `/health` | GET | none | Quick liveness check |
| `/system` | GET | none | Diagnostics (uptime, output dir, model count) |
| `/models` | GET | none | List checkpoints + which models are downloaded |
| `/styles` | GET | none | List style presets (cinematic, luxury, ...) |
| `/generate` | POST | **X-API-Key** | Text-to-image |
| `/img2img` | POST | **X-API-Key** | Image-to-image |
| `/upscale` | POST | **X-API-Key** | Upscale an existing image |
| `/workflow` | POST | **X-API-Key** | Raw ComfyUI workflow |
| `/status/{job_id}` | GET | none | Job status |
| `/jobs` | GET | none | Active job list |
| `/output/{path}` | GET | none | Fetch a generated image file |
| `/docs` | GET | none | Swagger UI |

`max_concurrent = 2`. Submit a third while two are running → `429 Max concurrent jobs reached`.

## Quick start (curl)

```bash
# Health
curl -s $SPARK_BASE/health | jq .

# Generate with SDXL
JOB=$(curl -s -X POST $SPARK_BASE/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $SPARK_API_KEY" \
  -d '{
    "prompt": "luxury portrait of a confident woman, premium editorial",
    "model": "sdxl",
    "style": "cinematic"
  }' | jq -r .job_id)

# Poll until done
while true; do
  STATUS=$(curl -s "$SPARK_BASE/status/$JOB" | jq -r .status)
  echo "$STATUS"
  [[ "$STATUS" == "completed" || "$STATUS" == "failed" ]] && break
  sleep 3
done

# Get the image URL
curl -s "$SPARK_BASE/status/$JOB" | jq -r '.image_urls[0]'
# → /output/job_xxx_SparkAtlas_..._00001.png

# Download it
curl -s -o out.png "$SPARK_BASE/output/job_xxx_..._00001.png"
```

## Quick start (Python)

```python
from spark_client import spark_generate

urls = spark_generate(
    prompt="luxury Dubai penthouse balcony at golden hour, panoramic city view",
    model="flux_schnell",  # or "sdxl"
    style="luxury",
)
print(urls[0])
```

The `spark_client.py` helper lives next to this SKILL.md. Copy it into your skill's tools dir or import directly.

## Available models

| Alias | Filename | Recommended params |
|---|---|---|
| `sdxl` | sd_xl_base_1.0.safetensors | steps=24-30, cfg=5.0-7.0, euler/normal |
| `flux_schnell` | flux_schnell_fp8.safetensors | steps=4, cfg=1.0, euler/simple |

Call `/models` to see the live list — new models added on Spark show up there automatically.

## Style presets

The `style` field appends a style tag block to your prompt. Available:

`cinematic` · `natural` · `studio` · `fashion` · `luxury` · `vintage` · `minimalist` · (and more — call `/styles`).

Set `style: ""` to skip preset and pass tags inline.

## Generate request schema

```json
{
  "prompt": "subject + scene description",
  "negative_prompt": "low quality, blurry, deformed",
  "model": "sdxl",
  "style": "cinematic",
  "width": 1024,
  "height": 1024,
  "steps": 24,
  "cfg": 5.0,
  "sampler": "euler",
  "scheduler": "normal",
  "seed": 42,
  "return_url": true
}
```

Only `prompt` is required.

## Operating rules

1. **Read `/system` first when something feels off.** Tells you `active_jobs`, `available_models`, `total_generated`.
2. **Cap to 2 concurrent jobs.** Spark's `max_concurrent = 2`. Queue locally above that.
3. **One render → review → iterate.** Don't blast 20 variants in parallel — wastes GPU minutes.
4. **Right model for the job.** `flux_schnell` for fast iteration; `sdxl` for the final delivery.
5. **Save winners.** Persist `prompt + seed + model` together. Reproducible.

## Error reference

| HTTP | Cause | Fix |
|---|---|---|
| `401 Invalid or missing X-API-Key` | Header missing on mutating call | Add `-H "X-API-Key: $SPARK_API_KEY"` |
| `429 Max concurrent jobs reached (2)` | Queue full | Wait, or check `/jobs` for active work |
| `503 ComfyUI not reachable` | ComfyUI process down on Spark | Page Seyed; check `/health` |
| `422 validation error` | Bad request body | Check `/docs` for exact schema |
| timeout >30s on `/health` | Network/Tailscale issue | `tailscale ping <spark-tailscale-ip>` |

## Files in this skill

- `SKILL.md` — this file
- `spark_client.py` — Python helper (stdlib only)
- `examples/` — sample prompts + workflows (TBD)

## See also

- `docs/CLAUDE-CODE-PATH.md` in the appie-kit for general Claude Code orchestrator setup.
- `$SPARK_DOCS_DIR/spark-api-instructions.md` on the Spark host.
- Operator discipline doc: `$SPARK_DOCS_DIR/operator-discipline.md`.
