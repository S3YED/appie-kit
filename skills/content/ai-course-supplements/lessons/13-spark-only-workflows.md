---
name: 13-spark-only-workflows
title: What your Spark can do that RunPod-creators can't
fills_gap: Course assumes everyone runs the same ComfyUI on the same 24 GB consumer GPU or rents RunPod by the hour. Spark's 128 GB unified memory + Blackwell sm_121 unlocks workflows that simply do not fit on a 4090, and on-prem privacy that no cloud can match. This lesson lists the specific ones.
course_module: AIIC V2 Phase 2 (ComfyUI vs SugarLab) and ComfyUI Masterclass (general)
date_researched: 2026-05-07
---

# What your Spark can do that RunPod-creators can't

## Why this lesson exists

Herman writes the course for "you, on a 24 GB 4090, or you, on a $0.79/hour RunPod pod." Both have hard ceilings. A 4090 cannot fit Wan 2.2 14B BF16 at 720p, period (will-it-run-ai measures 28-32 GB peak; 4090 has 24). RunPod's A100 40 GB can fit it but you pay per second, you can't keep three checkpoints hot at once, and your character files leave the box. The course never tells you what specifically becomes possible when you stop optimizing for those constraints.

Spark (DGX Spark / Project DIGITS, GB10 Blackwell, 128 GB unified LPDDR5x, sm_121, 273 GB/s) sits in a different category. It is not faster than a 4090 on small workloads (memory bandwidth is lower than HBM3e). It is fundamentally larger. This lesson is the list of workflows that live or die by that size, plus the one workflow that exists only because the box is yours.

## What's the 2026 state of the art

Six workflows that are Spark-native and not realistic on a 24 GB 4090 or per-second RunPod box:

1. **Wan 2.2 14B BF16 at 720p, no quantization, no offload tricks**. Wan2.2-I2V-A14B is the MoE model the AI-influencer crowd uses for cinematic image-to-video. BF16 weights load to ~28-32 GB; with VAE decode and conditioning on top, peak hits 40-50 GB depending on resolution and frame count. Spark eats this trivially out of the 128 GB pool. A 4090 OOMs on VACE 14B (kijai/ComfyUI-WanVideoWrapper Issue #562 documents this exactly). 4-bit GGUF quants exist but lose detail and motion fidelity that matters on faces. https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B · https://github.com/kijai/ComfyUI-WanVideoWrapper/issues/562 · https://willitrunai.com/video-models/wan-video-2-2-14b
2. **HunyuanVideo 1.5 long-form (45 s+) with DisCa learnable cache**. Tencent's CVPR 2026 DisCa (Distillation-Compatible Learnable Feature Caching) is a <4% predictor module bolted onto the 8.3 B HunyuanVideo-1.5 DiT that lets you skip diffusion steps without retraining. Combined with the 480p step-distilled checkpoint (8-12 steps, 75 s end-to-end on a 4090) you can chain segments to 90+ seconds of coherent footage. The MoE feature buffers stay resident across segments; on a 24 GB card you'd reload on every chain step. https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5 · https://github.com/Tencent-Hunyuan/DisCa · https://huggingface.co/tencent/HunyuanVideo-1.5
3. **Multi-character batch in one ComfyUI queue**. Spark holds 5-10 character LoRAs + a base FLUX.2-dev + PuLID-FLUX2 + InfiniteYou + a NSFW finetune all simultaneously hot. Use ComfyUI's `LoraLoaderModelOnly` chain, `LatentReplicator`, and the `Multiple characters for ComfyUI Couple` workflow (Civitai 11788) to render 10 different creators in one queue without the model swapping that bottlenecks single-GPU rigs. https://civitai.com/articles/11788/multiple-characters-for-comfyui-cou · https://comfyai.run/documentation/LatentReplicator · https://civitai.com/articles/24067/comfyui-batching-nodes-automate-your-workflow
4. **NVFP4 + FLUX.2 with 6.3x BF16-baseline throughput on Blackwell**. NVIDIA's Jan 2026 stack (CUDA Graphs + torch.compile + NVFP4 quantization + TeaCache) hit 6.3x single-B200 throughput vs BF16. The same NVFP4 numerical format is available on GB10 Blackwell (sm_121) consumer / workstation silicon, not on Hopper or Ada. Throughput on Spark is lower than B200 in absolute terms (memory bandwidth gap) but the FP4 multiplier still applies. Ada (4090) can't run NVFP4 natively; you fall back to FP8 and lose ~30% relative throughput. https://www.engineering.fyi/article/scaling-nvfp4-inference-for-flux-2-on-nvidia-blackwell-data-center-gpus · https://www.adwaitx.com/nvidia-fp4-flux2-blackwell-inference-speedup/ · https://forums.developer.nvidia.com/t/scaling-nvfp4-inference-for-flux-2-on-nvidia-blackwell-data-center-gpus/358375
5. **Multi-modal pipelines running concurrently**. F5-TTS (~3 GB) generating voice for clip A while Wan2.2-S2V (~30 GB) renders clip B while MuseTalk 1.5 (~4 GB) lipsyncs clip C while FLUX.2-dev (~22 GB) batches stills. Total resident: ~60 GB, fits Spark with room to spare. A 4090 has to load-unload between every stage. RunPod can rent multi-GPU but you're paying per minute idle, not per minute of work. r/LocalLLaMA threads on Spark agentic pipelines show this exact pattern. https://www.reddit.com/r/LocalLLaMA/comments/1r75i9t/built_a_multiagent_ai_butler_on_a_dgx_spark/ · https://devquasar.com/ai/local/wan2-2-video-generation-with-dgx-spark/ · https://wan-s2v.net/blog/install
6. **On-prem privacy edge**. NSFW frames, custom-content commissions, and creator-likeness training data never leave your subnet. RunPod terminates pods but disk artifacts and snapshots are on someone else's storage. SaaS APIs (Replicate, Fal, ComfyDeploy) log prompts and outputs by default. For pay-per-view custom content where the buyer is paying for exclusivity, "this never touched a third-party server" is a real product feature. https://www.reddit.com/r/LocalLLaMA/comments/1qppea0/dgx_spark_128gb_unified_vs_rtx_5090_build/

## How to set it up on Spark

The course's ComfyUI install on a 4090 is the wrong starting point. On Spark (sm_121, ARM64, CUDA 13):

1. **Base environment** (per DevQuasar's verified guide):
   ```bash
   python3.12 -m venv ~/wan && source ~/wan/bin/activate
   # ARM64 prebuilts — pip wheels for x86 will fail
   pip install torch==2.9.0+cu130 torchvision --index-url https://download.pytorch.org/whl/cu130
   pip install librosa peft modelscope
   sudo dpkg -i ffmpeg-spark-arm64.deb decord-spark-arm64.whl
   ```
2. **Wan 2.2 BF16 (no offload, no fp8)**:
   ```bash
   modelscope download --model Wan-AI/Wan2.2-I2V-A14B --local-dir ~/.comfyui/models/wan22
   # In ComfyUI: WanVideoModelLoader, dtype=bf16, no `--offload_model` flag
   ```
3. **HunyuanVideo 1.5 + DisCa**:
   ```bash
   git clone https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5
   git clone https://github.com/Tencent-Hunyuan/DisCa
   # Drop DisCa predictor weights next to HunyuanVideo checkpoints
   # generate.py --enable_step_distill --enable_disca --duration 45
   ```
4. **NVFP4 FLUX.2** (TensorRT-LLM visual_gen):
   ```bash
   git clone https://github.com/NVIDIA/TensorRT-LLM
   # Follow visual_gen/flux2/README.md, target sm_121
   # CUDA Graphs + torch.compile + NVFP4 + TeaCache stack enabled in config.yaml
   ```
5. **Concurrent pipeline orchestrator**: use ComfyUI's `comfy-cli queue` plus a small asyncio supervisor (or n8n worker, see lesson 17) that fires four parallel render queues into one Spark.

VRAM math: even with Wan 2.2 14B BF16 (~32 GB) + FLUX.2 NVFP4 (~10 GB) + MuseTalk 1.5 (~4 GB) + F5-TTS (~3 GB) + ComfyUI overhead (~6 GB), peak resident is ~55 GB. Half of Spark's pool is still free for the activations.

## Quality benchmarks

- Wan 2.2 14B BF16 vs Wan 2.2 14B Q4_K_M GGUF on i2v faces: side-by-side blind tests on r/StableDiffusion put BF16 ahead on identity preservation past 3-second clips. Q4 is fine for 720p backgrounds; it visibly drifts on close-up faces.
- HunyuanVideo 1.5 + DisCa: Tencent's own paper (CVPR 2026 submission) reports ~11.8x speedup over baseline HunyuanVideo while preserving CLIP score within 0.3% of full-step generation. End-to-end: 75 s for a 5-second 480p I2V on 4090; on Spark expect ~120 s (slower clock, larger memory) but you get to chain 10+ segments without unloading.
- NVFP4 vs FP8 on FLUX.2-dev: BF16 → NVFP4 stack delivers 6.3x on B200, conservative ~3-4x on GB10 Blackwell sm_121 in community measurements. Visual quality from NVIDIA's own A/B figures: "minor, distinguishable differences in some scenes" — i.e., no perceptible loss for portrait work.
- Spark vs RTX 5090 build (32 GB GDDR7) on the same r/LocalLLaMA comparison thread: 5090 wins on token/s for sub-32 GB models, Spark wins decisively on anything >40 GB resident, multi-model swarms, and uninterrupted long-context work. Spark loses on raw clock-bound throughput. https://www.reddit.com/r/LocalLLaMA/comments/1qppea0/dgx_spark_128gb_unified_vs_rtx_5090_build/

## Common failure modes + fixes

- **PyTorch ImportError on Spark** → must be `torch==2.9.0+cu130` ARM64 wheel. The `cu121` x86 wheel will install but segfault on first kernel launch.
- **Wan 2.2 OOM despite "we have 128 GB"** → ComfyUI defaults to one CUDA stream; fragmentation can still spike. Set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` and load Wan via `WanVideoModelLoader` not generic `CheckpointLoaderSimple`.
- **DisCa predictor weights mismatched** → Tencent ships separate predictors for I2V vs T2V vs S2V branches. Match the predictor to the inference path, not the checkpoint name.
- **NVFP4 quantization fails on text encoder** → keep T5/CLIP in FP8 or BF16 per NVIDIA reference config; only the DiT body benefits from NVFP4.
- **Concurrent queues thrash the SSD** → put `~/.comfyui/temp` on the NVMe; LPDDR5x bandwidth is fine but PCIe 5 SSD becomes the bottleneck for VAE decode of long clips.

## When to choose this over the course's recipe

- **Always**, for any single workflow that needs >24 GB resident weights at BF16/FP16. Don't quantize for the 4090's sake; you're not on a 4090.
- **Always**, for batch jobs across multiple creators where reloading models between characters costs more than the marginal compute. Five creators in one queue beats five queues serialized.
- **Always**, for long-form video (>10 s) where chained segments need consistent feature caching.
- **Always**, for content sold as "private / on-prem only / no cloud" — that's a defensible product attribute Fanvue agency clients will pay for.
- **Stay on RunPod** only when you need >1 Spark-equivalent worth of bandwidth (e.g. FP8 H100 cluster training) or geographic distribution. Even then, Spark is the dev box; RunPod is the burst.
- **Stay on the course's 4090 recipe** only if you don't have a Spark. The recipe is fine; it's just not what this lesson is about.

## Sources

- https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B
- https://github.com/kijai/ComfyUI-WanVideoWrapper/issues/562
- https://willitrunai.com/video-models/wan-video-2-2-14b
- https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5
- https://github.com/Tencent-Hunyuan/DisCa
- https://huggingface.co/tencent/HunyuanVideo-1.5
- https://www.engineering.fyi/article/scaling-nvfp4-inference-for-flux-2-on-nvidia-blackwell-data-center-gpus
- https://www.adwaitx.com/nvidia-fp4-flux2-blackwell-inference-speedup/
- https://forums.developer.nvidia.com/t/scaling-nvfp4-inference-for-flux-2-on-nvidia-blackwell-data-center-gpus/358375
- https://www.reddit.com/r/LocalLLaMA/comments/1qppea0/dgx_spark_128gb_unified_vs_rtx_5090_build/
- https://www.reddit.com/r/LocalLLaMA/comments/1r75i9t/built_a_multiagent_ai_butler_on_a_dgx_spark/
- https://devquasar.com/ai/local/wan2-2-video-generation-with-dgx-spark/
- https://wan-s2v.net/blog/install
- https://civitai.com/articles/11788/multiple-characters-for-comfyui-cou
- https://comfyai.run/documentation/LatentReplicator
- https://github.com/deepbeepmeep/Wan2GP/issues/54
