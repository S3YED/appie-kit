---
name: 03-image-models
title: Frontier image models beyond Flux Dev FP8
fills_gap: Course is locked to Flux Dev FP8 plus a paid character LoRA. Five months later there are at least three open-weight models that beat Flux Dev on realism, prompt-following, or NSFW, and Flux.2 itself supersedes Flux Dev for almost every creator workflow.
course_module: ComfyUI Masterclass, AIIC V2 Phase 3 (Character Creation)
date_researched: 2026-05-07
---

# Frontier image models beyond Flux Dev FP8

## Why this lesson exists

Herman's recipe is "Flux Dev FP8 + 5 paid LoRAs (Realism, iPhone Photo, NEEG, Age Slider, paid Character) plus Damn Pony Realistic for explicit NSFW." That stack was correct in late 2025. Since then BFL released Flux.2 (Nov 2025), Alibaba released Qwen-Image / Qwen-Image-Edit-2509, Tencent released HunyuanImage 3.0, ByteDance dropped Z-Image (currently the r/comfyui NSFW pick), and HiDream E1 stayed in the conversation for editing.

If you're still running Flux Dev FP8 in May 2026 you're producing visibly worse outputs than the field, and you're missing the multi-reference primitive in Flux.2 that obsoletes paid character LoRAs (see lesson `01-character-consistency.md`).

## What's the 2026 state of the art

### Tier 1: Frontier general-purpose image (use these as base)

1. **FLUX.2-dev** (BFL, Nov 2025). 9B parameters, MIT-style non-commercial license + commercial via API. Native multi-reference (up to 6 images). Beats FLUX.1-dev on prompt-following, hands, text rendering, and identity. NVFP4 quantization on Blackwell delivers 6.3x speedup over baseline (NVIDIA blog). https://bfl.ai/blog/flux-2 · https://bfl.ai/models/flux-2 · https://blogs.nvidia.com/blog/rtx-ai-garage-flux.2-comfyui/
2. **FLUX.2-klein** (BFL, Q1 2026). Smaller variant (4B) targeting interactive workflows. Same architecture. Native ComfyUI Klein nodes. http://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence
3. **Qwen-Image** + **Qwen-Image-Edit-2509** (Alibaba, mid-2025). Best open-weight for typography and structured edits. Edit version scores 7.69 average on OmniContext (vs OmniGen2's 7.95). Apache 2.0. ComfyUI native support. https://comfyanonymous.github.io/ComfyUI_examples/qwen_image/ · https://blog.comfy.org/p/qwen-image-edit-comfyui-support · https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit

### Tier 2: NSFW / realism specialists

4. **Z-Image (Z-Image Turbo)**, ByteDance, late 2025. Currently the r/comfyui consensus NSFW base — see "Uncensored Z Image in ComfyUI – Mind-Blowing Results!" community demo. Pairs with `NSFW MASTER FLUX - Z-Image Turbo V1` LoRA (51k+ downloads on Civitai). https://www.youtube.com/watch?v=qOIodnhOsys · https://civitai.com/models/667086/nsfw-master-flux
5. **HunyuanImage 3.0** (Tencent, autoregressive MoE, Sep 2025). 80B total, 13B active params per token. Trained on 5B image-text pairs. Strong on physics and complex compositions, weaker on speed (slow inference). Apache 2.0. ComfyUI support via `Comfy_HunyuanImage3` plugin. https://github.com/Tencent-Hunyuan/HunyuanImage-3.0 · https://github.com/EricRollei/Comfy_HunyuanImage3 · https://arxiv.org/abs/2509.23951
6. **HiDream E1.1** (HiDream, mid-2025). Editing-focused. Beats Flux Kontext Dev on some text-driven edits. https://adam.holter.com/hidream-e1-1-vs-flux-kontext-dev-which-open-source-ai-image-editor-should-you-use/

### Tier 3: Specialized editing (drop in alongside base)

7. **FLUX.1 Kontext [dev]**, BFL, mid-2025. In-context editing model — flow-matching for edits driven by reference + text. Open weights, similar usage rights to FLUX.1-dev. https://bfl.ai/blog/flux-1-kontext-dev · https://arxiv.org/html/2506.15742v2 · https://www.siliconflow.com/models/flux-1-kontext-dev

### Tier 4 (avoid as primary in 2026)

- **FLUX.1-dev FP8** (course default). Still works, no longer competitive on quality. Migrate to FLUX.2-dev or Klein. https://modelslab.com/blog/image-generation/flux1-vs-flux2-migration-guide-2026
- **SDXL / Pony / Damn Pony Realistic** for NSFW — superseded by Z-Image + Flux NSFW finetunes for realism. Pony still wins for stylized / anime. Course's "Damn Pony Realistic" path is now inferior.

## How to set it up on Spark

Install order on a fresh ComfyUI on Spark:

```bash
# FLUX.2-dev (primary base for AI-influencer)
cd ~/.comfyui/models/checkpoints
huggingface-cli download black-forest-labs/FLUX.2-dev --local-dir flux2-dev

# Z-Image (NSFW base)
huggingface-cli download tencent/Z-Image --local-dir z-image  # check current repo
# Or grab Z-Image Turbo LoRA from Civitai for use on Flux base
wget -O ~/.comfyui/models/loras/nsfw-master-flux-zimage.safetensors \
  https://civitai.com/api/download/models/<id>  # Civitai gating

# Qwen-Image-Edit-2509 (edit + character lock)
huggingface-cli download Qwen/Qwen-Image-Edit-2509 --local-dir qwen-image-edit

# HunyuanImage 3.0 (when you need physics-correct compositions, accept 4x slower inference)
git clone https://github.com/EricRollei/Comfy_HunyuanImage3 ~/.comfyui/custom_nodes/HunyuanImage3
```

Spark / Blackwell specific:
- Build PyTorch with `cu130` for NVFP4 acceleration on FLUX.2.
- Pull NVIDIA's `ComfyUI_Kitchen_nvfp4_Converter` to quantize FLUX.2 weights → NVFP4 → ~2x speedup over FP8/BF16. https://github.com/tritant/ComfyUI_Kitchen_nvfp4_Converter
- Async offloading and pinned memory are now ComfyUI defaults — you get 10-50% extra throughput automatically.

Workflow recipe per use case (on Spark):
- **Influencer photo (SFW)**: FLUX.2-dev + multi-ref (1-3 character images) + iPhone realism Qwen LoRA + 35-50 steps.
- **Influencer photo (NSFW)**: Z-Image base + NSFW MASTER FLUX LoRA + your trained character LoRA, 30 steps.
- **Edit existing photo (clothing swap, scene change)**: Qwen-Image-Edit-2509 OR FLUX.1 Kontext, depending on prompt complexity.
- **Multi-character / scene composition**: HunyuanImage 3.0.

## Quality benchmarks

From the FLUX.2 launch post (BFL benchmarks, image-text alignment + identity):

> "FLUX.2 demonstrates strong improvements over FLUX.1 in instruction following, multi-reference identity, photorealism, and complex compositions. Native multi-reference support enables consistency across up to 6 reference images in a single prompt."

NVIDIA NVFP4 + Blackwell B200 benchmark (NVIDIA dev blog, FLUX.2-dev):

| Optimization stack | Speedup vs baseline FLUX.2-dev BF16 |
|---|---|
| Baseline (BF16, no optim) | 1.0x |
| + torch.compile | ~1.2x |
| + CUDA Graphs | ~1.3x |
| + NVFP4 quantization | ~2.6x |
| + TeaCache | ~5.2x |
| **Full stack** | **6.3x** |

Modelslab migration guide quote: "FLUX.2 outperforms FLUX.1 across virtually every metric: prompt fidelity, hand rendering, text generation, and identity consistency. Migration is simply swapping the model node in most cases."

r/comfyui consensus on NSFW (via creator post compilations):
- Z-Image > Damn Pony Realistic for photoreal NSFW.
- Fluxed Up [Flux NSFW Checkpoint] v5.1_FP16 still leads for NSFW in pure Flux ecosystem (Civitai 200k+ downloads). https://civitai.com/models/847101
- Pony stays alive only for stylized art, not photoreal.

## Common failure modes + fixes

- **FLUX.2 OOM on 4090 / 24 GB** → use FLUX.2-klein (4B) or NVFP4-quantized FLUX.2-dev. Spark's 128 GB unified swallows full BF16.
- **Qwen-Image-Edit changes face when editing clothes** → drop guidance to 3.5, add InfiniteYou identity injection at 0.7 strength.
- **HunyuanImage 3.0 is glacially slow** → it is. Use only for hero shots; do bulk on FLUX.2.
- **Z-Image NSFW outputs are too cartoonish** → add iPhone Realism Qwen LoRA at 0.6, lower CFG to 4.
- **Mixed model stacks fight each other** → pick one base per workflow. Don't load FLUX.2 + Qwen-Image in the same KSampler.

## When to choose this over the course's recipe

- **Always migrate off FLUX.1-dev FP8** as soon as you have Spark's NVFP4 path working. You get faster + better outputs.
- **Use Qwen-Image-Edit** for any "change one thing" workflow — Photoshop replacement.
- **Use Z-Image base or NSFW MASTER LoRA on Flux** instead of Damn Pony for photoreal NSFW. Pony stays only for stylized.
- **Use HunyuanImage 3.0** only for the 5% of shots that need genuinely complex composition. It's not your bulk model.
- **Stick with course recipe** if you literally can't be bothered to update — but understand that you're shipping 2025-quality output.

## Sources

- https://bfl.ai/blog/flux-2
- https://bfl.ai/models/flux-2
- http://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence
- https://blogs.nvidia.com/blog/rtx-ai-garage-flux.2-comfyui/
- https://modelslab.com/blog/image-generation/flux1-vs-flux2-migration-guide-2026
- https://pixverse.blog/en/blog/flux-2-tech-review
- https://comfyanonymous.github.io/ComfyUI_examples/qwen_image/
- https://blog.comfy.org/p/qwen-image-edit-comfyui-support
- https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit
- https://www.youtube.com/watch?v=qOIodnhOsys (Z-Image NSFW)
- https://civitai.com/models/667086/nsfw-master-flux
- https://github.com/Tencent-Hunyuan/HunyuanImage-3.0
- https://github.com/EricRollei/Comfy_HunyuanImage3
- https://arxiv.org/abs/2509.23951 (HunyuanImage 3.0)
- https://bfl.ai/blog/flux-1-kontext-dev
- https://arxiv.org/html/2506.15742v2 (Kontext paper)
- https://adam.holter.com/hidream-e1-1-vs-flux-kontext-dev-which-open-source-ai-image-editor-should-you-use/
- https://aihaberleri.org/en/news/comprehensive-image-model-comparison-stable-diffusion-to-flux-2-20222026
- https://civitai.com/models/847101/flux (Fluxed Up)
- https://civitai.com/models/978314/ultrareal-fine-tune
- https://civitai.com/models/1799857/cyberrealistic-flux
