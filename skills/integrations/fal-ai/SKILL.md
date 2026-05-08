# SKILL.md - fal.ai Content Creation

**Owner:** Appie-2 (CMO)
**Created:** 2026-04-07
**Purpose:** Access 600+ generative AI models for images, video, voice, and more — pay per use

---

## What is fal.ai?

A unified API gateway to 600+ generative AI models. No GPU management, no subscriptions, no idle costs. Pay per use.

**Website:** https://fal.ai
**Pricing:** Pay-per-use (no subscription required)

---

## Quick Start

```bash
# Install fal client
pip install fal-client

# Or use REST API directly
curl -X POST https://queue.fal.run/fal-ai/flux-pro/v1.1 \
  -H "Authorization: Key YOUR_FAL_KEY" \
  -d '{"prompt": "your prompt", "image_size": "landscape_16_9"}'
```

**Get your API key:** https://fal.ai/dashboard/api-keys

---

## Available Models

### Image Generation

| Model | Best For | Cost per Image |
|-------|----------|---------------|
| **FLUX Pro** | General purpose, high quality | ~$0.05-0.09 |
| **FLUX Realism** | Photorealistic images | ~$0.05-0.09 |
| **Stable Diffusion 3.5** | Versatile, creative | ~$0.003-0.02 |
| **Ideogram 3** | Text in images (logos, posters) | ~$0.01-0.05 |
| **Recraft V3** | Design-focused, illustrations | ~$0.01-0.03 |

**Sizes:** square (1:1), portrait (2:3), landscape (3:2), 9:16, 16:9, A4 portrait, A4 landscape

### Video Generation

| Model | Best For | Cost |
|-------|----------|------|
| **Hailuo MiniMax Video** | Text-to-video, motion | ~$0.26/5-sec 720p |
| **Vidu** | High quality video | ~$0.20-0.50/video |
| **Kling** | Motion control, camera movement | ~$0.30-0.60/video |
| **Wan 2.1** | Open source video | ~$0.10-0.30/video |

**Video with audio:** +$0.20-0.40 per clip

### Voice / TTS

| Model | Best For |
|-------|----------|
| **MiniMax Speech** | Voice cloning, natural TTS |
| **F5 TTS** | Fast, multilingual TTS |

---

## Python SDK Usage

```python
import fal_client

# Generate an image
result = fal_client.run("fal-ai/flux-pro/v1.1", arguments={
    "prompt": "Professional photo of a smartwatch on white marble surface, studio lighting",
    "image_size": "square_hd",
    "num_inference_steps": 28
})
image_url = result["images"][0]["url"]

# Generate video
result = fal_client.run("fal-ai/hailuo-minimax-video/v2", arguments={
    "prompt": "A robot walking through a neon-lit city at night",
    "duration": 5,
    "resolution": "720p"
})
video_url = result["video"]["url"]

# Image-to-video (animate an image)
result = fal_client.run("fal-ai/minimax-video-01-live", arguments={
    "image_url": "https://example.com/image.jpg",
    "prompt": "Cinematic zoom in, camera slowly moves forward"
})
```

---

## Integration with Appie

### Content Creation Workflow

1. **Appie writes prompt** using Content Genome framework
2. **fal.ai generates image/video** via API
3. **Appie post-processes** (add text overlay, brand colors)
4. **Schedules via Zernio** to 14 platforms

### Real Example: Instagram Post

```
You: "Create a promotional Instagram post for our new web design service"

Appie:
1. Writes caption using Content Genome (Hook + Authority + CTA)
2. Generates image: fal_client.run("fal-ai/flux-pro/v1.1", prompt="Modern web design dashboard on laptop, dark theme, teal accents")
3. Adds text overlay with service name
4. Formats for Instagram (1080x1080)
5. Schedules via Zernio for optimal posting time
6. Updates Notion content calendar

Cost: ~$0.05 | Time: ~2 minutes
```

---

## Cost Optimization

| Tip | Savings |
|-----|---------|
| Use SD 3.5 for drafts, FLUX Pro for final | 5-10x cheaper |
| Reuse prompts (iterate, don't regenerate) | ~50% savings |
| Batch generation (run 5 at once) | Faster, more efficient |
| Use Wan 2.1 (open source) for testing | Free |

---

## Weblyfe Use Cases

1. **Client presentations** — Generate custom thumbnails and hero images
2. **Social media** — Post-specific visuals for each platform
3. **Brand mockups** — Show clients designs in context
4. **Video content** — Generate video clips for Reels/Shorts
5. **Case studies** — Before/after visual comparisons

---

## Rate Limits

- Free tier: Limited requests/minute
- Paid: Higher limits based on tier
- Queue system handles overload automatically

---

## See Also

- **appie-video-production** skill — Appie character video pipeline
- **banner-design** skill — Social media banner creation
- **thumbnails** skill — YouTube thumbnail generation
- **Content Genome** framework — Content decomposition methodology

---

*Get started: https://fal.ai — No subscription needed, pay per use.*
