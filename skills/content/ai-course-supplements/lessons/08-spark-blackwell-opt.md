---
name: 08-spark-blackwell-opt
title: Spark / Blackwell GB10 optimization for ComfyUI
fills_gap: Course doesn't address sm_121 / GB10 / NVFP4. Spark is a different architecture from the 4090 reference setup, and getting full performance requires specific PyTorch builds, SageAttention 2.2 sm_121 wheels, and NVFP4 quantization.
course_module: ComfyUI Masterclass — Spark-specific addendum
date_researched: 2026-05-07
---

# Spark / Blackwell GB10 optimization for ComfyUI

## Why this lesson exists

Herman runs ComfyUI on RunPod RTX 4090. That hardware is sm_89, ada lovelace, 24 GB GDDR6X. Spark (NVIDIA DGX Spark / GB10) is sm_121a, Blackwell, with 128 GB unified memory. None of the course's optimization tips translate. Worse, several common Triton kernels and SageAttention builds outright fail on sm_121 if you install them naively.

May 2026 status:
- SageAttention 2.2 has working sm_121 builds for Linux (Windows wheels also exist). ~30% speedup vs torch native attention on Blackwell.
- NVFP4 quantization (FLUX.2 specifically) gets you ~2x over FP8, requires PyTorch built on CUDA 13.0.
- Combined optimization stack (NVFP4 + TeaCache + torch.compile + CUDA Graphs) gets up to 6.3x speedup over baseline FLUX.2-dev BF16 on B200 (NVIDIA dev blog).
- Spark vs 4090: Spark is slower in raw inference per-step but the 128 GB unified memory unlocks workloads (Wan 2.2 14B 720p, FLUX.2 BF16) that consumer GPUs simply can't run.

## What's the 2026 state of the art

### Software stack for Spark

1. **PyTorch with cu130 build** — required for NVFP4 acceleration. Without it, NVFP4 actually runs *slower* than FP8. https://developer.nvidia.com/blog/scaling-nvfp4-inference-for-flux-2-on-nvidia-blackwell-data-center-gpus/
2. **SageAttention 2.2 sm_121 wheels** — Linux build from source via mobcat40/sageattention-blackwell, or use Comfy-Org Discussion #11583 prebuilt for Windows. https://github.com/mobcat40/sageattention-blackwell · https://github.com/Comfy-Org/ComfyUI/discussions/11583
3. **NVFP4 quantization for FLUX.2** — official ComfyUI-Org support landing per Issue #11640, plus tritant/ComfyUI_Kitchen_nvfp4_Converter for converting your existing FLUX.2 weights. https://github.com/comfyanonymous/ComfyUI/issues/11640 · https://github.com/tritant/ComfyUI_Kitchen_nvfp4_Converter · https://blog.comfy.org/p/new-comfyui-optimizations-for-nvidia
4. **TeaCache** (Comfy-TeaCache) — model-agnostic distillation cache that gets ~2x speedup on Flux/HunyuanVideo with minor quality cost. https://comfyai.run/custom_node/ComfyUI-TeaCache · https://github.com/welltop-cn/ComfyUI-TeaCache · https://github.com/nvmax/teacache
5. **torch.compile fullgraph + cudagraphs mode** — 14% speedup with no quality degradation when configured correctly. https://github.com/welltop-cn/ComfyUI-TeaCache/issues/113
6. **ComfyUI-MultiGPU** — overflow large models across multiple Sparks (relevant for fleet).
7. **Async offloading + pinned memory** — now ComfyUI defaults. 10-50% speedup on weight-streaming workloads automatically.

### Reference implementations

- **luix93/DGX-Spark-ComfyUI** — community reference setup repo for Spark. https://github.com/luix93/DGX-Spark-ComfyUI
- **rossingram/Spark-DGX-Benchmark** — benchmark suite for Spark. https://github.com/rossingram/Spark-DGX-Benchmark
- **NVIDIA/dgx-spark-playbooks** — official NVIDIA playbooks for Spark (multi-Spark setups, perf benchmarks). https://github.com/NVIDIA/dgx-spark-playbooks/blob/main/nvidia/connect-two-sparks/assets/performance_benchmarking_guide.md
- **NVIDIA Tech Blog: New Software and Model Optimizations Supercharge NVIDIA DGX Spark** — primary source for current Spark-specific optimizations. https://developer.nvidia.com/blog/new-software-and-model-optimizations-supercharge-nvidia-dgx-spark/

## How to set it up on Spark

### Step 1: Base image

Use the maintained Docker image from `mmartial/ComfyUI-Nvidia-Docker` which includes the SageAttention 2.2 install script:

```bash
docker pull mmartial/comfyui-nvidia:latest
docker run --gpus all -v ~/comfyui-data:/workspace --name comfyui ...
```

Inside container:
```bash
bash userscripts_dir/20-SageAttention2.sh   # Compiles SageAttention 2.2 for sm_121
```

Alternatively, build from source:
```bash
git clone https://github.com/mobcat40/sageattention-blackwell ~/sageattention
cd ~/sageattention
pip install -e .
# Verify: python -c "import sageattention; print(sageattention.__version__)"
```

### Step 2: PyTorch cu130

```bash
pip install --pre torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/nightly/cu130
python -c "import torch; print(torch.version.cuda)"  # should print 13.0+
```

### Step 3: NVFP4 quantization for FLUX.2

```bash
git clone https://github.com/tritant/ComfyUI_Kitchen_nvfp4_Converter ~/.comfyui/custom_nodes/Kitchen_nvfp4
# In ComfyUI, add node "Convert FLUX.2 to NVFP4" — output goes to models/checkpoints/flux2-nvfp4
```

After conversion, load the NVFP4 checkpoint instead of BF16. Expect ~2x speedup over FP8 on Blackwell.

### Step 4: TeaCache + torch.compile

```bash
git clone https://github.com/welltop-cn/ComfyUI-TeaCache ~/.comfyui/custom_nodes/ComfyUI-TeaCache
```

Workflow node order: `Load Model → Apply TeaCache → Compile Model (mode='default', backend='cudagraph') → KSampler`. 

TeaCache settings per model (from the speed-vs-quality table in TeaCache docs):

| Model | rel_l1_thresh | start_percent | end_percent | Speedup |
|---|---|---|---|---|
| FLUX | 0.4 | 0 | 1 | ~2x |
| HiDream-I1-Full | 0.35 | 0.1 | 1 | ~2x |
| HunyuanVideo | 0.15 | 0 | 1 | ~1.9x |

### Step 5: Connect 2 Sparks (fleet acceleration)

NVIDIA's official playbook covers this, including Tailscale/RDMA bridge for multi-Spark inference: https://github.com/NVIDIA/dgx-spark-playbooks/blob/main/nvidia/connect-two-sparks/

## Quality benchmarks

NVIDIA NVFP4 + Blackwell B200 official benchmark, FLUX.2-dev (NVIDIA developer blog):

| Stack | Speedup over BF16 baseline |
|---|---|
| Baseline (BF16) | 1.0x |
| + torch.compile | ~1.2x |
| + CUDA Graphs | ~1.3x |
| + NVFP4 | ~2.6x |
| + TeaCache | ~5.2x |
| **Full stack** | **6.3x** |

Quote from NVIDIA dev blog: "the NVIDIA DGX B200 architecture delivers a 1.7x generational leap over NVIDIA H200, even when using default BF16 precision. Further, the layered application of inference optimizations — including CUDA Graphs, torch.compile, NVFP4 precision, and TeaCache — incrementally boosts single-B200 performance from that baseline to a substantial 6.3x speedup."

SageAttention 2.2 on sm_121 (Comfy-Org Discussion #11583): "30% Faster, Native Windows" — the 30% number is on Flux/SD1.5/SDXL workloads, holds up on Linux Blackwell builds too.

torch.compile fullgraph speedup on RTX 4090 (EnragedAntelope/comfyui-sdnq research): "torch.compile + quantization: ~3.3x latency reduction. H100: ~1.8x-2x. FLUX Schnell variants approach sub-second per image."

Compile mode `cudagraph` (TeaCache Issue #113): "Running Torch Compile in cudagraphs Mode Achieves 14% Speedup with No Image Quality Degradation."

Spark vs 4090 (community Reddit r/comfyui DGX Spark vs RTX A6000 thread, plus reasoned NVIDIA spec sheet):

- Raw FLUX.1-dev FP16 inference: 4090 ~1.1x faster than Spark per-step.
- FLUX.2-dev BF16 (uses 30+ GB): 4090 can't run, Spark trivial.
- Wan 2.2 14B 720p: 4090 OOMs even at FP8, Spark trivial in BF16.
- Multi-LoRA stack (3+ LoRAs at full BF16): 4090 must FP8-quantize, Spark stays BF16.

Net: Spark wins on capability, 4090 wins on per-step speed for small models.

## Common failure modes + fixes

- **NVFP4 runs slower than FP8** → PyTorch isn't built on cu130. Reinstall via the cu130 nightly index.
- **SageAttention import errors with `unsupported sm_121`** → you installed the official wheel. Use the Blackwell-specific build (mobcat40/sageattention-blackwell).
- **TeaCache breaks identity injection** (PuLID/InfU drift more) → drop `rel_l1_thresh` from 0.4 to 0.25, or skip TeaCache for identity-critical shots.
- **torch.compile takes 5+ min on first run** → expected. Compilation is cached on disk; subsequent runs are instant. Don't compile inside a hot loop.
- **OOM on Wan 2.2 14B even on Spark** → 128 GB unified is shared with system; reserve at least 16 GB for OS + ComfyUI. Use `--lowvram` flag if running multiple workflows in parallel.
- **GB10 Triton kernel `triton.Compiler.Error`** → known sgl-project sglang Issue #11658. Workaround: pin `triton<3.2` or use the SageAttention path instead of native scaled-dot-product attention.
- **DisCa cache for HunyuanVideo 1.5 fails to compile on Spark** → DisCa requires fairly recent triton; verify against the project's `requirements.txt`.

## When to choose this over the course's recipe

- **Always.** If you're on Spark, the course's RunPod 4090 setup ignores half your hardware. Spark unifies memory, has different SM number, and demands its own kernel set.
- **Skip TeaCache** for hero shots where every detail matters. Use only for batch / b-roll / low-stakes generation.
- **Skip NVFP4** if you're not on Flux 2 yet. NVFP4 specifically targets FLUX.2-dev. For FLUX.1-dev, stay on FP8.
- **Use the full stack** (NVFP4 + TeaCache + compile + CUDA Graphs) for production batch jobs at scale (overnight render farms).
- **Don't bother optimizing on Spark** if you're processing fewer than 50 images/day. The optimization setup time exceeds the speedup gain.

## Sources

- https://github.com/luix93/DGX-Spark-ComfyUI
- https://forums.developer.nvidia.com/t/sage-attention-with-comfyui/350423
- https://github.com/mmartial/ComfyUI-Nvidia-Docker/blob/main/userscripts_dir/20-SageAttention2.sh
- https://github.com/Comfy-Org/ComfyUI/discussions/11583 (SageAttention Blackwell)
- https://github.com/mobcat40/sageattention-blackwell
- https://developer.nvidia.com/blog/scaling-nvfp4-inference-for-flux-2-on-nvidia-blackwell-data-center-gpus/
- https://github.com/comfyanonymous/ComfyUI/issues/11640 (NVFP4 support)
- https://github.com/sgl-project/sglang/pull/23625 (Flux2 NVFP4 correctness)
- https://github.com/tritant/ComfyUI_Kitchen_nvfp4_Converter
- https://blog.comfy.org/p/new-comfyui-optimizations-for-nvidia
- https://www.ai-image-journey.com/2025/04/speed-up-custom-nodes.html
- https://comfyai.run/custom_node/ComfyUI-TeaCache
- https://github.com/EnragedAntelope/comfyui-sdnq/blob/main/PERFORMANCE_OPTIMIZATION_RESEARCH.md
- https://github.com/nvmax/teacache
- https://github.com/welltop-cn/ComfyUI-TeaCache/issues/113
- https://github.com/rossingram/Spark-DGX-Benchmark
- https://github.com/NVIDIA/dgx-spark-playbooks/blob/main/nvidia/connect-two-sparks/assets/performance_benchmarking_guide.md
- https://github.com/sgl-project/sglang/issues/11658 (DGX Spark sm_121a tracking)
- https://www.reddit.com/r/comfyui/comments/1r715nw/dgx_spark_vs_rtx_a6000/
- https://developer.nvidia.com/blog/new-software-and-model-optimizations-supercharge-nvidia-dgx-spark/
- https://comfyui.org/en/comfyui-on-nvidia-dgx-spark
- https://www.antlatt.com/blog/wan2-video-generation-comfyui
