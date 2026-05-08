---
name: 07-nsfw-techniques
title: NSFW prompting and workflow techniques creators actually use
fills_gap: Course's NSFW recipe is YOLO V8 + Damn Pony Realistic + ComfyUI Impact Pack. Five months later there are sharper anatomy fixes, better realism finetunes, and clothing-swap workflows that the course doesn't teach.
course_module: ComfyUI Masterclass, Vault, Sugarlab AI Masterclass
date_researched: 2026-05-07
---

# NSFW prompting and workflow techniques creators actually use

## Why this lesson exists

Herman's NSFW pipeline, paraphrased from the course: "Generate with Damn Pony Realistic, run YOLO V8 person detection, send through ComfyUI Impact Pack to fix faces, manually inpaint nipples and groin if they look bad, upscale through CCSR." That's a 2024-vintage flow.

In May 2026 the consensus on r/comfyui, r/StableDiffusion, and the NSFW Civitai threads has moved to:

- **Z-Image base** (or NSFW MASTER FLUX LoRA on Flux base) replaces Damn Pony for photoreal NSFW.
- **FaceDetailer + ADetailer Nipples model** replaces ad-hoc YOLO + Impact Pack fixes.
- **Florence-2 auto-detect** replaces manual masking — point at any feature, get a segmentation mask, inpaint, done.
- **ComfyUI-Layered-Diffusion + cloth-swap workflows** replace manual outfit swaps in Photoshop.
- **Fluxed Up / UltraReal / CyberRealistic Flux** are the photoreal NSFW Flux finetunes that win on Civitai.

This lesson catalogs five concrete creator-tested techniques the course doesn't cover.

## What's the 2026 state of the art

### Five techniques that beat the course recipe

#### 1. Z-Image (or NSFW MASTER FLUX) replaces Damn Pony for photoreal NSFW

r/comfyui Q1 2026 consensus: Z-Image is the strongest open-weight NSFW base, with `NSFW MASTER FLUX - Z-Image Turbo V1` LoRA being the most-downloaded NSFW LoRA on Civitai (51k+). Damn Pony stays alive only for stylized work. https://civitai.com/models/667086/nsfw-master-flux · https://www.youtube.com/watch?v=qOIodnhOsys

#### 2. ADetailer Nipples + FaceDetailer chain replaces YOLO + Impact Pack

The CivArchive `ADetailer Nipples model` is purpose-trained for nipple-region inpainting. Chain it after FaceDetailer in the same workflow. Better masks, cleaner blends, fewer manual passes. Civitai article "Fix Face Distortion in ComfyUI (FaceDetailer Guide)" walks the entire flow. https://civitaiarchive.com/models/490259 · https://civitai.com/articles/24907/fix-face-distortion-in-comfyui-facedetailer-guide

#### 3. Florence-2 auto-segmentation kills manual masking

Florence-2-large-PromptGen v2.0 from MiaoshouAI does open-vocab segmentation. Workflow: feed image, prompt "groin region" or "left breast", get a clean mask, send to inpaint pass. ComfyUI-Florence2 by kijai exposes this as a native node. https://github.com/kijai/ComfyUI-Florence2 · https://comfyui.org/en/transforming-images-with-ai-flux-and-florence

Time saved per shot: ~3 minutes vs manual brush masking.

#### 4. ComfyUI clothing-swap workflow (Furkan Gozukara reference flow)

For "swap creator's outfit" without re-rendering the whole image. Pipeline: Florence-2 segments clothing → SAM 2 refines mask → IP-Adapter SD1.5 with reference outfit → in-paint at 0.6 denoise → CCSR upscale. Furkan Gozukara's "Transfer Any Clothing Into A New Person" tutorial is the canonical reference. https://huggingface.co/blog/MonsterMMORPG/transfer-any-clothing-into-a-new-person-comfyui · https://www.youtube.com/watch?v=pIR0oyafh-I

This is huge for Fanvue PPV: shoot once, swap outfits 20 times.

#### 5. Photoreal NSFW Flux finetunes (Fluxed Up, UltraReal, CyberRealistic)

These three Flux NSFW finetunes lead Civitai 2026:
- **Fluxed Up [Flux NSFW Checkpoint]** v5.1_FP16 — most popular, best general photoreal NSFW. https://civitai.com/models/847101
- **UltraReal Fine-Tune** v4 — sharpest skin texture, strongest "amateur iPhone" look. https://civitai.com/models/978314/ultrareal-fine-tune
- **CyberRealistic Flux** v2.5 — best for explicit + cinematic lighting. https://civitai.com/models/1799857/cyberrealistic-flux
- **Vision Realistic** v2 — alt option, smaller community. https://civitai.com/models/619656

LocalForge AI's "Best Flux NSFW Models on CivitAI (March 2026)" round-up confirms this exact ranking. https://offlinecreator.com/best-flux-nsfw-models-civitai

### Other techniques worth knowing

- **Mystic XXX** (NSFW LoRA, works across Flux, Wan 2.2, and Qwen-Image — same trigger across models). Good for unified-style multi-model output. https://civitai.com/models/1295758
- **Pony Realism v2.2** — refined Pony for SDXL-class NSFW with strong photoreal. Fallback if you're stuck on SDXL. https://civitai.com/models/938116/pony-realism-nsfw-photo-with-comfyui-upscale-workflow
- **RealCore_Pony** on Hugging Face — community-shared photoreal Pony refinement. https://huggingface.co/rityak/RealCore_Pony

## How to set it up on Spark

Build one canonical NSFW workflow that you reuse across creators:

```
[Load Image (reference)] → [InfiniteYou Loader] → [Apply InfuseNet (sim_stage1, 1.0)]
                                                       ↓
        [Load FLUX.2-dev OR Z-Image OR Fluxed Up Flux finetune (NSFW base)]
                                                       ↓
              [LoRA Loader: NSFW MASTER FLUX OR Mystic XXX]
                                                       ↓
              [LoRA Loader: UltraReal / iPhone Realism (style)]
                                                       ↓
                 [KSampler — 35 steps, CFG 4-5, Euler/dpmpp_2m]
                                                       ↓
                              [VAE Decode]
                                                       ↓
        [Florence-2 Segment "face"] → [FaceDetailer (face inpaint)]
                                                       ↓
        [Florence-2 Segment "nipples"] → [ADetailer Nipples (inpaint)]
                                                       ↓
        [Florence-2 Segment "hands"] → [HandDetailer (inpaint)]
                                                       ↓
                       [SUPIR or CCSR Upscale 2x]
                                                       ↓
                           [Save Image]
```

Custom nodes you'll want:
```bash
cd ~/.comfyui/custom_nodes
git clone https://github.com/kijai/ComfyUI-Florence2
git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack       # Face/Hand detailers
git clone https://github.com/kijai/ComfyUI-segment-anything-2   # SAM 2
git clone https://github.com/Acly/comfyui-tooling-nodes         # General masking
```

### Spark advantage

Spark lets you stack three LoRAs at full BF16 (Mystic XXX + UltraReal + character LoRA) without any quality compromise. 4090 users have to FP8-quantize and lose detail.

## Quality benchmarks

Civitai 2026 download leaderboard for Flux NSFW (LocalForge AI snapshot):

| Model | Type | Downloads (approx) | Strength |
|---|---|---|---|
| Fluxed Up v5.1 | Checkpoint | 200k+ | General photoreal NSFW |
| Mystic XXX (Flux) | LoRA | 80k+ | Multi-model unified style |
| NSFW MASTER FLUX (Z-Image) | LoRA | 51k+ | Photoreal on Z-Image base |
| UltraReal v4 | Checkpoint | 70k+ | Skin detail, amateur look |
| CyberRealistic Flux v2.5 | Checkpoint | 45k+ | Cinematic NSFW |

MyAIForce "Fix Plastic-Like Skin and Fake Details in ComfyUI" guide quote: "FaceDetailer + ADetailer for NSFW regions removes the 'AI-skin' shine that destroys believability. Skip this and your photos will read as AI within 2 seconds." https://myaiforce.com/fix-plastic-skin/

Civitai article "Refining Pony/Illustrious Models with SDXL/1.5 for Full Realism": "The two-pass approach — base in Pony, refine in SDXL realism — gives you Pony's NSFW competence and SDXL's skin detail. But moving to Flux NSFW finetunes obsoletes this for new builds." https://civitai.com/articles/6651

## Common failure modes + fixes

- **"AI-skin shine"** (the giveaway) → run FaceDetailer pass + iPhone Realism Qwen LoRA at 0.4 to break perfect symmetry. Add ImpurePores LoRA for skin texture.
- **Nipples look painted on / wrong color** → ADetailer Nipples pass at 0.5-0.6 denoise. Don't go higher or you re-roll the whole breast shape.
- **Hands deformed** → Florence-2 → HandDetailer at 0.7 denoise. Or run InfiniteYou at lower scale (0.7) so hands aren't over-conditioned.
- **Mystic XXX overpowers other LoRAs** → drop strength to 0.6 if stacking with realism LoRAs.
- **Damn Pony Realistic looks plastic in 2026** → switch base to Z-Image + NSFW MASTER LoRA, or to Fluxed Up v5.1.
- **Identity drift in NSFW finetunes** → InfiniteYou at sim_stage1 is more identity-preserving than PuLID with NSFW finetunes.

## When to choose this over the course's recipe

- **Always upgrade FaceDetailer + ADetailer Nipples** over the course's manual Impact Pack flow. Better, faster, fewer passes.
- **Use Florence-2 segmentation** any time you'd otherwise paint masks by hand. 3 minutes saved per shot, less inconsistent.
- **Move base from Damn Pony Realistic to Z-Image** as your NSFW default. Photoreal NSFW is its current job.
- **Adopt Fluxed Up / UltraReal / CyberRealistic** as your Flux NSFW finetunes; rotate based on shot type.
- **Use clothing-swap workflow** to multiply Fanvue PPV from a single base shoot.
- **Keep course recipe** only as a fallback for when Z-Image doesn't have a NSFW LoRA for your specific kink (Mystic XXX covers most).

## Sources

- https://civitai.com/models/847101/flux (Fluxed Up)
- https://civitai.com/models/978314/ultrareal-fine-tune
- https://civitai.com/models/1799857/cyberrealistic-flux
- https://civitai.com/models/619656 (Vision Realistic)
- https://civitai.com/models/667086/nsfw-master-flux (NSFW MASTER FLUX Z-Image)
- https://civitai.com/models/1295758 (Mystic XXX Flux/Wan 2.2/Qwen)
- https://offlinecreator.com/best-flux-nsfw-models-civitai
- https://huggingface.co/blog/MonsterMMORPG/transfer-any-clothing-into-a-new-person-comfyui
- https://github.com/FurkanGozukara/Stable-Diffusion/discussions/106
- https://www.youtube.com/watch?v=pIR0oyafh-I (1-Click Cloth Swap)
- https://github.com/kijai/ComfyUI-Florence2
- https://comfyui.org/en/transforming-images-with-ai-flux-and-florence
- https://civitaiarchive.com/models/490259 (ADetailer Nipples model)
- https://civitai.com/articles/24907/fix-face-distortion-in-comfyui-facedetailer-guide
- https://lilys.ai/en/notes/comfyui-20251214/comfyui-fix-faces-adetailer-alternative
- https://lilys.ai/en/notes/comfyui-20260221/comfyui-face-detailer-fix-faces
- https://www.youtube.com/watch?v=2JkTjbjRTEs (Fix Bad Faces ADetailer)
- https://civitai.com/models/938116/pony-realism-nsfw-photo-with-comfyui-upscale-workflow
- https://civitai.com/articles/6651 (Refining Pony with SDXL/1.5)
- https://huggingface.co/rityak/RealCore_Pony
- https://myaiforce.com/fix-plastic-skin/
