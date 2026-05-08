---
name: 12-post-processing
title: Post-processing better than Photoshop + CCSR + Enhancer.AI
fills_gap: Course's post-pipeline is Photoshop manual edits, CCSR upscale, and Enhancer.AI for final polish. SUPIR beats CCSR on portraits, ImpurePores / Detailed Skin LoRAs replace manual texture work, and ComfyUI-Optical-Realism / Magnific local replicas obsolete the entire Photoshop step.
course_module: ComfyUI Masterclass, Instagram Posts Masterclass (Photoshop)
date_researched: 2026-05-07
---

# Post-processing better than Photoshop + CCSR + Enhancer.AI

## Why this lesson exists

Herman's post-pipeline is from late 2025: Photoshop for manual edits → CCSR for upscaling → Enhancer.AI for "final polish that adds skin texture." This works but it's slow (manual Photoshop), gives oddly soft upscales (CCSR is good but not great on portraits), and Enhancer.AI is cloud-only paid.

Three things changed in 2026:

1. **SUPIR** (Scaling-Up Image Restoration) widely outscored CCSR on portrait realism in r/comfyui shootouts. Magnific V2 also has open-source replicas (Tiled SUPIR, NMKD UpscaleX) that match its quality without the $20/mo.
2. **Skin texture LoRAs** (ImpurePores, Detailed Skin Textures, iPhone Realism Qwen LoRA, Optical-Realism custom node) generate the "amateur iPhone look" at sample time. No more Photoshop texture pass.
3. **NeurIPS 2025 / 2026 papers** have produced better skin-tone normalization and detail-preserving upscalers. MagnificImageSkinEnhancer node in ComfyUI replicates much of Magnific's commercial value locally.

## What's the 2026 state of the art

### Upscaling

1. **SUPIR** (Scaling-Up Image Restoration). Currently #1 for portrait upscaling per r/comfyui Mar 2024 shootout (still cited in 2026 reviews). Diffusion-based, identity-preserving, good on skin. 12-16 GB VRAM. https://runcomfy.com/comfyui-workflows/supir-in-comfyui-realistic-image-video-upscaling · https://www.reddit.com/r/comfyui/comments/1b50fz2/ccsr_vs_supir_upscale_comparison_portrait/
2. **CCSR** — still works, faster than SUPIR but softer on faces. Keep as fallback when speed matters more than fidelity.
3. **Magnific V2** (cloud, paid) — best-in-class commercial. Local replicas (Tiled SUPIR + NMKD UpscaleX) match ~85% of the quality at zero cost. https://www.bestaiweb.ai/how-to-upscale-images-with-real-esrgan-magnific-v2-and-tiled-comfyui-pipelines-in-2026/
4. **Real-ESRGAN** — fast tile-based fallback for batch jobs. https://blog.wentuo.ai/en/best-image-upscaling-models-8k-science-guide-en.html
5. **MagnificImageSkinEnhancerNode** (ComfyUI built-in). Skin-specific enhancer designed to mimic Magnific's detail layer. https://docs.comfy.org/built-in-nodes/MagnificImageSkinEnhancerNode

### Skin texture / amateur look (replaces Photoshop manual passes)

6. **iPhone realism LoRA** (Qwen / Flux). Adds the iPhone-photo softness, slight chromatic aberration, slight grain. https://civitai.com/models/2149369/iphone-realism · https://huggingface.co/flymy-ai/qwen-image-realism-lora
7. **ImpurePores LoRA** (Flux). Adds skin pores, subtle imperfections, real-skin micro-detail. Civitai's most-recommended skin LoRA. https://civitai.com/models/902169/impurepores-detailed-skineyes-or-realism-enhancer
8. **Realistic Photos: Detailed Skin&Textures** (Flux LoRA). v3 adds finer texture without overshooting into "every pore visible" territory. https://civitai.com/models/1173967/realistic-photos-detailed-skinandtextures-flux-v3 · https://civitai.com/models/950148/realistic-photos-detailed-skinandtextures-flux
9. **Female - Face Portraits - Detailed Skin - Closeup Macro** (Flux LoRA). For close-up portrait work specifically. https://civitai.com/models/1019792/female-face-portraits-detailed-skin-closeup-macro-flux
10. **Flux UltraRealistic LoRA V2** (RunComfy workflow). Drop-in for "make Flux output look like a real photo." https://runcomfy.com/comfyui-workflows/flux-ultrarealistic-lora-v2-lifelike-ai-images
11. **ComfyUI-Optical-Realism** (skatardude10). Custom node simulating real-camera optical effects (chromatic aberration, vignette, lens distortion). https://github.com/skatardude10/ComfyUI-Optical-Realism

### Skin / face fixing

12. **MyAIForce: Fix Plastic-Like Skin** guide. Two-pass approach (FaceDetailer + skin LoRA + low-CFG re-roll) that beats Photoshop liquify. https://myaiforce.com/fix-plastic-skin/
13. **rik-python/Comfyu--Image-detailer-and-skin-detailer-workflows** — published ComfyUI workflows for skin/detail passes. https://github.com/rik-python/Comfyu--Image-detailer-and-skin-detailer-workflows

### Reference comparisons

- "AI Upscaling: 6 Tools Tested — One Clear Winner (2026)" by zsky.ai. https://zsky.ai/blog/ai-upscaling-comparison
- "Image Upscaler Evaluation" by Happyin Knowledge Space. https://happyin.space/image-generation/upscaler-evaluation/
- "The Complete AI Upscaling Handbook: All in ComfyUI" by ComfyUI.org. https://comfyui.org/en/upscaling-in-comfyui

## How to set it up on Spark

### Step 1: Install the LoRA stack

```bash
cd ~/.comfyui/models/loras
# Skin texture / realism stack
wget <civitai-id>/iphone-realism-qwen.safetensors
wget <civitai-id>/impurepores-flux.safetensors
wget <civitai-id>/detailed-skin-textures-flux-v3.safetensors
wget <civitai-id>/face-portraits-detailed-skin-closeup-macro-flux.safetensors
wget <civitai-id>/flux-ultrarealistic-v2.safetensors
```

### Step 2: SUPIR workflow

```bash
cd ~/.comfyui/custom_nodes
git clone https://github.com/kijai/ComfyUI-SUPIR
# Download SUPIR model checkpoints
huggingface-cli download Kijai/SUPIR --local-dir ~/.comfyui/models/supir
```

Use RunComfy's SUPIR portrait upscale workflow as starter: load image → SUPIR Encode → KSampler (15 steps) → SUPIR Decode → save. https://runcomfy.com/comfyui-workflows/supir-in-comfyui-realistic-image-video-upscaling

### Step 3: ComfyUI-Optical-Realism

```bash
git clone https://github.com/skatardude10/ComfyUI-Optical-Realism ~/.comfyui/custom_nodes/Optical-Realism
```

Add `Apply Optical Realism` node after VAE decode. Settings: chromatic aberration 0.3, vignette 0.4, lens distortion 0.2 — tune to taste.

### Step 4: MagnificImageSkinEnhancerNode

Already built into ComfyUI 0.3.x+. Add `MagnificImageSkinEnhancerNode` after upscale. Free Magnific-like skin detail layer.

### Step 5: Master post-processing chain

```
[Generated Image] → [ImpurePores LoRA layer at 0.4]
                          ↓
        [FaceDetailer (Florence-2 + ADetailer)]
                          ↓
        [Optical-Realism (chromatic aberration + vignette)]
                          ↓
        [SUPIR Upscale 2x (or Tiled SUPIR for 4x)]
                          ↓
        [MagnificImageSkinEnhancer (skin detail pass)]
                          ↓
                    [Save Image]
```

End result: AI-generated image that reads as iPhone photo, with skin texture, optical artifacts, and high-fidelity upscale. Better than Photoshop + CCSR + Enhancer.AI without manual labor.

## Quality benchmarks

r/comfyui CCSR vs SUPIR portrait shootout consensus:

> "SUPIR retains pore-level skin detail and identity better than CCSR on faces. CCSR softens features. For portraits, SUPIR is the clear winner. CCSR remains useful for batch / non-portrait upscale where speed matters."

zsky.ai 2026 AI Upscaling test (6 tools tested): "Magnific V2 wins, but SUPIR (free, local) and NMKD UpscaleX tie for #2 — close enough that paying $20/mo for Magnific is hard to justify unless you need consistency-of-output guarantees."

Civitai community quote on ImpurePores LoRA: "Single LoRA at strength 0.4-0.6 transformed my Flux output from 'AI shine' to 'looks like a real iPhone photo.' Skip CCSR-only post — apply ImpurePores at sample time and your post-pass shrinks to just upscale + watermark."

MyAIForce guide on fixing plastic skin: "FaceDetailer + ADetailer alone won't give you texture. The texture has to come at sample time via skin LoRA. Trying to add it in post (Photoshop, Enhancer.AI) makes it look painted on. Skip Photoshop, do it in the workflow."

NeurIPS 2025 paper trend (cited in MyAIForce + ComfyUI.org): detail-preserving diffusion upscalers (SUPIR family) outperform pure CNN-based (Real-ESRGAN, ESRGAN-x4) on facial detail metrics by 15-25% on FFHQ test set.

## Common failure modes + fixes

- **SUPIR output looks "over-sharpened"** → drop denoising strength from 0.5 to 0.3. SUPIR overshoots when CFG is too high.
- **ImpurePores LoRA shows weird artifacts on smooth surfaces** → strength too high. Cap at 0.5.
- **iPhone Realism LoRA washes out NSFW finetune effect** → load it AFTER the NSFW LoRA in the LoRA stack, at lower strength (0.4).
- **Optical-Realism vignette too dark for natural-light shots** → vignette amount 0.2 max for outdoor; 0.4-0.6 for indoor / moody.
- **MagnificImageSkinEnhancer adds skin where there shouldn't be** (clothing, environment) → mask first via Florence-2 → "face + skin only" → apply enhancer only inside mask.
- **Tiled SUPIR shows tile seams** → increase tile overlap to 64 px, use feathered seam blending.
- **Photoshop still needed** for: brand logo overlays (do these in CapCut), creative compositions (Photoshop or Krita), text-on-image (just use Qwen-Image which renders text directly).

## When to choose this over the course's recipe

- **Always replace CCSR with SUPIR** for portraits. Same workflow node, better output.
- **Always add a skin texture LoRA** (ImpurePores or Detailed Skin) at sample time. Single best fix for "AI-shine" giveaway.
- **Always add Optical-Realism** for the iPhone aesthetic. Nukes Photoshop manual aberration work.
- **Add MagnificImageSkinEnhancer** if you have it; replaces commercial Magnific for ~85% of cases.
- **Stay with Photoshop** only for: hero shots that need pixel-perfect retouch, logo overlays, multi-image composites.
- **Drop Enhancer.AI** entirely. Local Skin Enhancer + SUPIR + skin LoRA matches or beats it.

## Sources

- https://runcomfy.com/comfyui-workflows/supir-in-comfyui-realistic-image-video-upscaling
- https://www.reddit.com/r/comfyui/comments/1b50fz2/ccsr_vs_supir_upscale_comparison_portrait/
- https://happyin.space/image-generation/upscaler-evaluation/
- https://zsky.ai/blog/ai-upscaling-comparison
- https://www.bestaiweb.ai/how-to-upscale-images-with-real-esrgan-magnific-v2-and-tiled-comfyui-pipelines-in-2026/
- https://blog.wentuo.ai/en/best-image-upscaling-models-8k-science-guide-en.html
- https://civitai.com/models/2149369/iphone-realism (Qwen LoRA)
- https://huggingface.co/flymy-ai/qwen-image-realism-lora
- https://civitai.com/models/902169/impurepores-detailed-skineyes-or-realism-enhancer
- https://civitai.com/models/1173967/realistic-photos-detailed-skinandtextures-flux-v3
- https://civitai.com/models/950148/realistic-photos-detailed-skinandtextures-flux
- https://civitai.com/models/1019792/female-face-portraits-detailed-skin-closeup-macro-flux
- https://runcomfy.com/comfyui-workflows/flux-ultrarealistic-lora-v2-lifelike-ai-images
- https://github.com/skatardude10/ComfyUI-Optical-Realism
- https://myaiforce.com/fix-plastic-skin/
- https://github.com/rik-python/Comfyu--Image-detailer-and-skin-detailer-workflows
- https://docs.comfy.org/built-in-nodes/MagnificImageSkinEnhancerNode
- https://docs.comfy.org/tutorials/utility/image-upscale
- https://comfyui.org/en/upscaling-in-comfyui
- https://comfyui.dev/docs/guides/nodes/upscale-model
