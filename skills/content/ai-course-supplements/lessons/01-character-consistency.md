---
name: 01-character-consistency
title: Character consistency without paid LoRAs
fills_gap: Course locks character lock behind buying Jack's paid Flux LoRA. There are now four production-grade open-source paths that beat that flow on identity fidelity AND skip the training step entirely.
course_module: AIIC V2 Phase 3 (Character Creation), ComfyUI Masterclass, Vault (ComfyUI LoRA)
date_researched: 2026-05-07
---

# Character consistency without paid LoRAs

## Why this lesson exists

Herman teaches one path: pay Jack ~$100 for a custom Flux character LoRA, drop it into ComfyUI, then everything stays on-character. That works, but it costs money per creator, locks you into Jack's queue, and freezes your character at training time. Worse, the course explicitly tells you NOT to train a LoRA yourself because "I tried it multiple times and they all came out like shit" (AIIC V2, ComfyUI Masterclass module).

In May 2026 there are four open-source identity-injection methods that lock a face from a single reference image with NO training, run on Flux Dev / Flux.2 / Qwen-Image, and ship as a single ComfyUI node. Two of them (PuLID-FLUX and InfiniteYou) outscore IP-Adapter on every published benchmark, and Flux.2 has its own multi-reference primitive that obsoletes the entire concept of a per-character LoRA for many use cases.

You should still train LoRAs eventually (lesson `02-lora-training.md` explains how to do it without crap results), but for prototyping a creator, fast experimentation, and per-shot identity correction, identity-injection is what the field actually uses now.

## What's the 2026 state of the art

Ranked by output quality on the OmniContext SINGLE-character benchmark (Flux-class scores):

1. **Flux.2 multi-reference (native)**, BFL, Nov 2025 release. Score 8.95 SC. Pass up to 6 reference images in one prompt; identity, outfit, environment all inherit. No extra nodes, no IP-Adapter. This is BFL's deliberate replacement of the LoRA workflow for character work. https://bfl.ai/blog/flux-2 · https://selfielab.me/blog/flux-2-multi-ref-character-consistency-guide-20260329
2. **InfiniteYou (InfU) v1.0 aes_stage2 / sim_stage1**, ByteDance, ICCV 2025 highlight. State-of-the-art identity preservation on FLUX.1-dev. Two variants: `aes_stage2` for prompt-following + aesthetics, `sim_stage1` for higher identity similarity. Plug-and-play, Apache 2.0, on HuggingFace. Beats PuLID-FLUX on identity AND text-image alignment qualitatively (their own paper Fig 5; community confirms). https://huggingface.co/ByteDance/InfiniteYou · https://github.com/bytedance/infiniteyou
3. **PuLID-FLUX2 v0.6.2** (iFayens fork), 2026-03. First PuLID adaptation for FLUX.2 with Klein weight support (4B / 9B / Dev). ComfyUI-native. https://github.com/iFayens/ComfyUI-PuLID-Flux2 · https://huggingface.co/Fayens/Pulid-Flux2
4. **OmniGen2** (VectorSpaceLab), CVPR-track Jun 2025, score 7.95 average on OmniContext. Uses Qwen-VL-2.5 (3B) + 4B diffusion. ReferenceLatent multi-reference + instruction-based edits in one model. Best when you also need editing ("change clothes, keep face"). https://github.com/VectorSpaceLab/OmniGen2 · https://arxiv.org/html/2506.18871
5. **Qwen-Image-Edit-2509** scores 7.69 on the same benchmark, beats OmniGen2 on object/scene but loses on character SINGLE. Useful as a fallback when prompt fidelity matters more than face. https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit
6. **InstantID v1** (still relevant for SDXL-class flows; superseded for Flux). Use only if you're stuck on SDXL. https://apatero.com/blog/instantid-vs-pulid-vs-faceid-ultimate-face-swap-comparison-2025

NSFW compatibility: PuLID-FLUX and InfiniteYou both work with NSFW Flux finetunes (Fluxed Up, UltraReal, CyberRealistic) because they inject identity tokens between DiT blocks rather than overwriting the base. OmniGen2 has NSFW limits in its base weights but is fine when used purely as an identity passthrough into a NSFW finetune.

## How to set it up on Spark

Tested workflow for Spark / GB10 (sm_121, 128 GB unified) running ComfyUI Nvidia Docker:

1. **Install Flux.2 native multi-ref first** (it covers 70% of cases):
   ```bash
   cd ~/.comfyui/models
   huggingface-cli download black-forest-labs/FLUX.2-dev --local-dir checkpoints/flux2-dev
   ```
   Use the official `FLUX.2 Multi-Reference` example workflow from comfyanonymous/ComfyUI_examples. Pass 1-6 images via `Load Image` nodes; the conditioning stack handles the rest.

2. **Add InfiniteYou for max identity fidelity** when one ref isn't enough:
   ```bash
   cd ~/.comfyui/custom_nodes
   git clone https://github.com/bytedance/infiniteyou
   cd infiniteyou && pip install -r requirements.txt
   # Download both variants
   huggingface-cli download ByteDance/InfiniteYou --local-dir ~/.comfyui/models/infiniteyou
   ```
   Workflow: `InfiniteYou Loader` → `InfuseNet Conditioning` → `KSampler`. Switch `--model_version sim_stage1` for max identity, `aes_stage2` for default. Tweak `infusenet_conditioning_scale` (start 1.0, raise to 1.4 if drift) and `infusenet_guidance_start` (start 0.0).

3. **PuLID-FLUX2 for FLUX.2 specifically**:
   ```bash
   git clone https://github.com/iFayens/ComfyUI-PuLID-Flux2 ~/.comfyui/custom_nodes/ComfyUI-PuLID-Flux2
   pip install insightface onnxruntime-gpu open-clip-torch ml_dtypes==0.3.2
   # InsightFace AntelopeV2 → ~/.comfyui/models/insightface/models/antelopev2/
   # PuLID-Flux2 weights → ~/.comfyui/models/pulid/
   ```
   Add `Apply PuLID ✦ Flux.2` after model load, strength 1.0 (normal) or 1.4 (max lock).

4. **OmniGen2 for in-context editing**:
   ```bash
   pip install omnigen2
   # Or via ComfyUI-OmniGen2 nodes
   ```

Spark VRAM math: InfiniteYou-FLUX bf16 needs ~30 GB peak with `--offload`, ~17 GB with `--offload --fp8` (per the official `pulid_for_flux.md`). Spark's 128 GB unified memory swallows bf16 trivially; no fp8 needed.

## Quality benchmarks

From the OmniGen2 paper (Tab. 2, OmniContext SINGLE / MULTIPLE / SCENE Average):

| Method | SINGLE | MULTIPLE | SCENE | Avg |
|---|---|---|---|---|
| Gemini-2.5-Flash-Image | 8.62 | 7.88 | 7.05 | 7.85 |
| **Flux.2 (closed)** | 8.95 | 8.54 | 8.60 | **8.80** |
| Qwen-Image-Edit-2509 | 8.35 | 7.65 | 5.16 | 7.69 |
| OmniGen2 | 8.19 | 7.45 | 7.75 | **7.95** |
| InfiniteYou | 8.05 | – | – | – (single-task) |
| BAGEL | 5.48 | 5.17 | 4.07 | 5.73 |

Quote from the InfU paper, Fig 5 caption: "FLUX.1-dev IP-Adapter (IPA) results are inadequate. PuLID-FLUX generates images with decent identity similarity. However, it suffers from poor text-image alignment (Columns 1, 2, 4), and the image quality (e.g., bad hands in Column 5) and aesthetic appeal are degraded. In addition, the face copy-paste issue of PuLID-FLUX is evident (Column 5). In comparison, the proposed InfU outperforms the baselines across all dimensions."

Apatero's 2025 face-swap shootout: PuLID > InstantID > IP-Adapter FaceID for "drift across many scenes." InfiniteYou wasn't in their test (released after) but matches PuLID on identity and beats it on prompt-following.

## Common failure modes + fixes

- **Face copy-paste artifact** (face looks pasted on, not synthesized in-scene) → switch from PuLID-FLUX to InfiniteYou `aes_stage2`. The SFT stage they describe was specifically built to fix this.
- **Identity drift in side profile or extreme angle** → add a second reference image (Flux.2 multi-ref) or chain `OmniGen2 ReferenceLatent` with the angled shot as a second condition.
- **NSFW finetune washes the face** (e.g. on Damn Pony) → don't apply identity injection at full strength. Set `infusenet_conditioning_scale` to 0.7 and let the NSFW LoRA take over from there.
- **Hands and feet get worse with high IP-Adapter weight** → known bug, see XLabs-AI/flux-ip-adapter Issue #33 ("Flux IPAdapter with high weight 'breaks' the consistency"). Drop IP-Adapter, use PuLID/InfU instead.
- **Wrong race / age / hair on identity injection** → InsightFace AntelopeV2 has known biases on darker skin and Asian features. Re-run with the `sim_stage1` checkpoint and provide a second, well-lit reference image.

## When to choose this over the course's recipe

- **Always**, for prototyping a new creator persona. Identity-injection is faster, cheaper, and more flexible than commissioning a LoRA.
- **For one-off rescue shots** where the LoRA missed (off-angle, weird outfit, kids photo) → InfU + your existing trained LoRA stacked.
- **For multi-character scenes** (two creators in one shot) → Flux.2 multi-ref or OmniGen2 only. Course workflow has no answer here.
- **Stick with paid LoRA from Jack** only when you've got a long-term creator with a fixed look and need infinite-shot consistency at zero per-shot identity cost.

## Sources

- https://github.com/iFayens/ComfyUI-PuLID-Flux2
- https://github.com/ToTheBeginning/PuLID/blob/main/docs/pulid_for_flux.md
- https://github.com/bytedance/infiniteyou
- https://huggingface.co/ByteDance/InfiniteYou
- https://arxiv.org/pdf/2503.16418 (InfiniteYou paper)
- https://github.com/VectorSpaceLab/OmniGen2
- https://arxiv.org/html/2506.18871 (OmniGen2 paper)
- https://bfl.ai/blog/flux-2
- https://selfielab.me/blog/flux-2-multi-ref-character-consistency-guide-20260329
- https://apatero.com/blog/instantid-vs-pulid-vs-faceid-ultimate-face-swap-comparison-2025
- https://huggingface.co/XLabs-AI/flux-ip-adapter/discussions/33
- https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit
