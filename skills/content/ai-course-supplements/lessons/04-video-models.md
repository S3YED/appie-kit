---
name: 04-video-models
title: Frontier video generation beyond WAN 2.1 + Kling
fills_gap: Course uses WAN 2.1 (NSFW) and Kling AI (cloud SFW). Wan 2.2 and Wan 2.2 Animate are now drop-in upgrades, HunyuanVideo 1.5 ships an 11.8x speedup over Wan via DisCa cache, and LTX-Video v2 generates 5-second 24fps clips in under 10 seconds on a 4090.
course_module: AIIC V2 Phase 5/6 (Content & Reels), Reels Masterclass, ComfyUI Masterclass
date_researched: 2026-05-07
---

# Frontier video generation beyond WAN 2.1 + Kling

## Why this lesson exists

Herman teaches WAN 2.1 for NSFW video (locally on RunPod 4090) and Kling AI for cinematic SFW reels (paid cloud). Both choices were correct in late 2025. Eight months later:

- Wan 2.2 (Alibaba, July 2025) is a true MoE-architecture upgrade with cinematic camera control. Wan2.2-Animate-14B and Wan2.2-S2V-14B add identity-preserving character animation and audio-driven talking head from a single reference image — both ComfyUI-native, both open weights, both NSFW-capable through community LoRAs.
- HunyuanVideo 1.5 (Tencent, Nov 2025, accepted CVPR 2026) ships DisCa distillation cache delivering up to 11.8x speedup over baseline.
- LTX-Video v2 / LTX-2 (Lightricks, late 2025) generates faster than real-time on a 4090 — useful for prompt iteration even if final output goes through Wan.
- The whole "you need RunPod for video" frame breaks on Spark's 128 GB unified memory.

## What's the 2026 state of the art

### Tier 1: NSFW video (replaces course's WAN 2.1)

1. **Wan 2.2 T2V-A14B** (Alibaba, July 2025). 2-expert MoE. Better motion, better stability, cinematic camera control. 65-80 GB VRAM at 720p 14B, 8-12 GB at GGUF Q5. Drop-in weight swap from Wan 2.1. https://wan2.video/wan2.2-vs-wan2.1 · https://docs.comfy.org/tutorials/video/wan/wan2_2 · https://wanvideogenerator.com/zh/blog/wan-21-vs-wan-22-comparison-guide
2. **Wan 2.2 VACE Fun** — community-maintained NSFW-trained variant of Wan 2.2 VACE, distributed via NSFWcode and the NSFW-API/Wan-VACE GitHub repo. Native NSFW without prompt jailbreaking. https://github.com/NSFW-API/Wan-VACE · https://www.nsfwcode.com/viewforum.php?f=47 · https://www.youtube.com/watch?v=hTZfTj5wIiY
3. **Wan2.2-Animate-14B** — character animation from single reference image + driving pose video. SAM 2 + ViTPose pose extraction, identity-preserving. RunComfy `Wan-2-2-Animate-V2` workflow is the production-grade reference. https://docs.comfy.org/tutorials/video/wan/wan2-2-animate · https://www.runcomfy.com/comfyui-workflows/wan-2-2-animate-v2-in-comfyui-pose-driven-animation-workflow · https://wanimate.net/how-to-animate-wan-22-in-comfyui

### Tier 2: SFW cinematic (replaces Kling AI)

4. **HunyuanVideo 1.5** (Tencent, Nov 2025, CVPR 2026). DisCa distillation cache: 11.8x speedup over baseline at near-identical quality. ~13B params. Runs locally. https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5 · https://arxiv.org/html/2511.18870v1 · https://www.aibase.com/news/27187 (DisCa announcement)
5. **LTX-Video v2 / LTX-2** (Lightricks, late 2025). Fastest open video model: 5-second clip at 24fps in under 10s on a 4090. 4K spatial upscaler. NVFP4/NVFP8 announced at CES 2026 to triple speed again. Limited to 5s clips, no character consistency built-in. Best for prompt iteration. https://apatero.com/blog/text-to-video-open-source-models-compared-2026 · https://insiderllm.com/guides/local-ai-video-generation/
6. **Kling 2.0 / 2.5** — still best closed-cloud quality for cinematic. Worth keeping as escape hatch for hero shots.

### Tier 3: Talking head / lip-synced video (NEW capability the course doesn't address)

7. **Wan2.2-S2V-14B** — audio-driven cinematic video from a single image. Beats MultiTalk and InfiniteTalk on lipsync quality, including singing characters. https://huggingface.co/Wan-AI/Wan2.2-S2V-14B · https://docs.comfy.org/tutorials/video/wan/wan2-2-s2v · https://github.com/deepbeepmeep/Wan2GP/issues/1266
8. (See lesson `05-lipsync.md` for the full lipsync stack including MuseTalk 1.5 and LatentSync.)

### Tier 4: Other models worth knowing (don't make these primary)

- **CogVideoX-5B** — strong ecosystem, still kicking, lots of community LoRAs.
- **Mochi** — high quality but resource-hungry.
- **Helios** — newer entrant per AGENTVSAI Feb 2026 ranking. https://www.agentvsai.com/best-open-source-text-to-video-generators-feb-2026/

## How to set it up on Spark

Spark's 128 GB unified memory means you can run Wan 2.2 14B at 720p without GGUF compression, which is impossible on any consumer GPU including the 5090 (per Spheron's deploy guide: "Wan 2.1/2.2 14B at 720p needs 65-80 GB VRAM, rules out every consumer GPU including the RTX 5090").

```bash
# Wan 2.2 (T2V + I2V + Animate + S2V — all checkpoints from one repo)
cd ~/.comfyui/models/diffusion_models
huggingface-cli download Wan-AI/Wan2.2-T2V-A14B --local-dir wan2.2-t2v
huggingface-cli download Wan-AI/Wan2.2-Animate-14B --local-dir wan2.2-animate
huggingface-cli download Wan-AI/Wan2.2-S2V-14B --local-dir wan2.2-s2v

# ComfyUI native workflows (already shipped, no extra nodes needed for T2V)
# For Animate V2:
git clone https://github.com/kijai/ComfyUI-WanVideoWrapper ~/.comfyui/custom_nodes/WanVideoWrapper

# HunyuanVideo 1.5 with DisCa
git clone https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5
git clone https://github.com/Tencent-Hunyuan/DisCa  # 11.8x distillation cache
# Plus DisCa ComfyUI integration node (community)

# LTX-Video v2 (for fast prompt iteration)
huggingface-cli download Lightricks/LTX-Video-2 --local-dir ltx-v2
```

Workflow recipe per shot:

| Shot type | Model | Settings |
|---|---|---|
| 5s NSFW reel from text | Wan 2.2 T2V-A14B + NSFW LoRA | 720p, 50 steps, Wan 2.2 native ComfyUI workflow |
| Character dance/walk from photo | Wan2.2-Animate-14B | Reference image + driving pose video, SAM 2 mask, 720p |
| Talking head from photo + voice | Wan2.2-S2V-14B | Image + audio (your TTS output, see lesson `06-voice-cloning.md`) |
| Cinematic SFW b-roll | HunyuanVideo 1.5 + DisCa | Cuts inference 11.8x; lets you batch 30+ clips overnight |
| Prompt iteration | LTX-Video v2 | <10s per generation; once you find prompt, re-render in Wan |

## Quality benchmarks

Wan 2.1 vs 2.2 (from wan2.video comparison):

| Feature | Wan 2.1 (T2V-14B) | Wan 2.2 (T2V-A14B) |
|---|---|---|
| Architecture | Dense Diffusion Transformer | 2-expert MoE Diffusion Transformer |
| Motion quality | Good | Substantially better (more stable temporal flow) |
| Camera control | Limited | Cinematic primitives built in |
| Prompt fidelity | Solid | Better, especially complex scenes |
| VRAM (14B 720p) | 65-80 GB | 65-80 GB (MoE doesn't reduce peak) |
| GGUF Q5 (8 GB VRAM) | Available | Available |
| NSFW community LoRA | Mature | Mature, faster-moving |

LTX-Video v2 speed (Apatero / InsiderLLM benchmarks): "5-second clips at 24fps in under 10 seconds—fastest on this list by a wide margin... 700M parameters, deployable as a microservice on a single consumer GPU." Trade-off: 512×320 native, no character consistency. Use for iteration not final.

HunyuanVideo 1.5 DisCa quote (Tencent / aibase.com announcement): "DisCa accelerates video diffusion transformers by 11.8x via distillation cache while preserving quality, accepted at CVPR 2026."

Wan2.2-S2V-14B creator quote (Wan2GP Issue #1266): "Wan 2.2 S2V model needed, it's better than multytalk and infinite talk. And it can do good lipsink for singing characters."

## Common failure modes + fixes

- **Wan 2.2 14B OOM at 720p on consumer GPU** → use GGUF Q5 (8-12 GB) or downgrade to 480p, or move to Spark.
- **Animate-14B drops identity in fast motion** → preprocess driving video to slow it 0.7x, then time-stretch in CapCut. Or chain Wan2.2-Animate output through PuLID-FLUX2 for shot-by-shot rescue.
- **S2V lipsync drift on long clips** → Wan2.2-S2V is best under 6s. For longer talking head, use MuseTalk 1.5 or LatentSync (lesson `05-lipsync.md`).
- **NSFW Wan 2.2 outputs face wash** → use NSFW-API/Wan-VACE NSFW-trained variant; don't try to jailbreak base Wan with prompts.
- **HunyuanVideo 1.5 too slow without DisCa** → DisCa is the unlock. Don't run 1.5 baseline.
- **LTX-Video output looks soft** → it is by design. Always re-render final in Wan or HunyuanVideo.

## When to choose this over the course's recipe

- **Replace WAN 2.1 with Wan 2.2 immediately.** Drop-in weight swap. Better motion, same VRAM.
- **Replace Kling AI with HunyuanVideo 1.5 + DisCa** for SFW cinematic reels. You go from $0.10/clip on Kling to free at scale, with comparable quality.
- **Add Wan2.2-Animate** when you need a creator to dance, walk, or do a specific pose from a real-life reference video. Not in course at all.
- **Add Wan2.2-S2V** when you want a creator to "speak" a TTS voicenote on camera. Not in course.
- **Keep Kling** as a fallback for hero shots where you want zero variance.

## Sources

- https://wan2.video/wan2.2-vs-wan2.1
- https://docs.comfy.org/tutorials/video/wan/wan2_2
- https://docs.comfy.org/tutorials/video/wan/wan2-2-animate
- https://docs.comfy.org/tutorials/video/wan/wan2-2-s2v
- https://huggingface.co/Wan-AI/Wan2.2-Animate-14B
- https://huggingface.co/Wan-AI/Wan2.2-S2V-14B
- https://www.runcomfy.com/comfyui-workflows/wan-2-2-animate-v2-in-comfyui-pose-driven-animation-workflow
- https://wanimate.net/how-to-animate-wan-22-in-comfyui
- https://wanimate.net/wan-animate-talking-ai-characters
- https://www.spheron.network/blog/deploy-wan-2-1-ai-video-generation-gpu-setup/
- https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5
- https://github.com/Tencent-Hunyuan/DisCa
- https://arxiv.org/html/2511.18870v1
- https://www.aibase.com/news/27187
- https://apatero.com/blog/text-to-video-open-source-models-compared-2026
- https://www.agentvsai.com/best-open-source-text-to-video-generators-feb-2026/
- https://insiderllm.com/guides/local-ai-video-generation/
- https://github.com/NSFW-API/Wan-VACE
- https://www.nsfwcode.com/viewforum.php?f=47
- https://www.youtube.com/watch?v=hTZfTj5wIiY (Wan 2.2 VACE Fun)
- https://github.com/deepbeepmeep/Wan2GP/issues/1266
