---
name: 02-lora-training
title: Local LoRA training that actually works
fills_gap: Course tells you not to train LoRAs because Herman's attempts "all came out like shit." The 2026 toolkits + correct hyperparameters get you a usable Flux LoRA from 15-30 images on a single 4090/5090/Spark in 30-90 min.
course_module: ComfyUI Masterclass, Vault (ComfyUI LoRA), AIIC V2 Phase 3 (Character Creation)
date_researched: 2026-05-07
---

# Local LoRA training that actually works

## Why this lesson exists

Herman explicitly outsources LoRA training to Jack: "I tried it multiple times and they all came out like shit so I just have Jack do it." This blocks every creator from owning their character pipeline, costs ~$100/character, and makes you queue behind Jack. The training-bad-results problem in Herman's pipeline is a tooling and dataset issue, not a fundamental skill gap. With the May 2026 stack, a 15-30 image set can be turned into a high-fidelity Flux character LoRA in under 2 hours on a 4090 / 5090 / Spark.

Three open-source toolkits dominate Flux LoRA training right now: ostris/ai-toolkit (the de-facto standard, used by BFL itself for FLUX.2 LoRA training tutorials), kohya-ss/sd-scripts (battle-tested SD1.5/SDXL with mature Flux support), and cocktailpeanut/fluxgym (zero-config GUI wrapper around sd-scripts; runs at 8 GB VRAM). All three converge on similar settings if you know what you're doing.

## What's the 2026 state of the art

Toolkits, ranked by what most creators actually use:

1. **ostris/ai-toolkit** (latest commits weekly, FLUX.2 dev support landed Q1 2026). Written by ostris, sponsored by GLIF and BFL. Single yaml config, runs on 24 GB VRAM (RTX 4090 reference config). Official BFL FLUX.2 LoRA tutorial uses it. https://github.com/ostris/ai-toolkit · https://www.youtube.com/watch?v=qWDpPos6vrI · https://www.runcomfy.com/comfyui-nodes/trainer/ai-toolkit/flux-2-dev-lora-training
2. **kohya-ss/sd-scripts** with `flux_train_network.py`. Most flexible, widest hyperparameter knobs, oldest community. https://github.com/kohya-ss/sd-scripts/blob/main/docs/flux_train_network.md · https://deepwiki.com/kohya-ss/sd-scripts/6.3-flux-lora-training
3. **cocktailpeanut/fluxgym** — Gradio frontend on top of sd-scripts, zero-config presets for 8/12/16/20/24 GB. Best if you hate yaml. https://github.com/cocktailpeanut/fluxgym · https://deepwiki.com/cocktailpeanut/fluxgym

Image captioner (the second piece Herman skips):

- **JoyCaption Beta One** by fpgaminer — current SOTA for verbose, training-grade Flux/SDXL captions. Replaced BLIP-2 and old WD14 taggers in most creator pipelines. Free, runs locally. https://github.com/fpgaminer/joycaption · https://civitai.com/models/1027172/joy-caption-two-reverse-prompting
- **Florence-2-large-PromptGen v2.0** by MiaoshouAI — fast, structured. Good for batch tagging full datasets in minutes. https://huggingface.co/MiaoshouAI/Florence-2-large-PromptGen-v2.0
- **MieMieeeee/ComfyUI-CaptionThis** wraps both inside ComfyUI for one-click batch captioning before training. https://github.com/MieMieeeee/ComfyUI-CaptionThis

## How to set it up on Spark

### Step 1: Dataset prep (the part Herman gets wrong)

15-30 images is the sweet spot. Specifically:
- 8-10 head/face shots, varied lighting and angle (front, 3/4, profile, looking up/down).
- 6-8 medium shots (waist up).
- 4-6 full-body shots.
- 2-4 expression / emotion variation (smile, neutral, serious).
- Strict rule: no two images at same angle + same outfit. Variety = generalization.
- 1024x1024 minimum. Don't upscale low-res Bouncy AI / SugarLab outputs; they'll teach the LoRA to be soft.

Throw out anything with multiple people, watermarks, heavy duplicate compression, or obvious AI artifacts (extra fingers, melted accessories).

### Step 2: Caption with JoyCaption

```bash
git clone https://github.com/fpgaminer/joycaption ~/joycaption
cd ~/joycaption
pip install -r requirements.txt
# Batch caption all images in dataset/
python scripts/batch-caption.py --input dataset/ --output dataset/ --mode "training_prompt" --trigger "ohwx_woman"
```

`ohwx_woman` (or any rare token) is your activation phrase. Every caption gets this prefix prepended. Edit any captions that are wrong (JoyCaption reverse-engineers ~95% correctly; you handle the 5%).

### Step 3: Train with ai-toolkit (Flux Dev, RTX 4090 / Spark)

```bash
git clone https://github.com/ostris/ai-toolkit ~/ai-toolkit
cd ~/ai-toolkit
pip install -r requirements.txt
huggingface-cli login  # need access to FLUX.1-dev gated repo
cp config/examples/train_lora_flux_24gb.yaml config/myproject.yaml
```

Edit `config/myproject.yaml`. Key settings (the ones that matter):

```yaml
process:
  - type: 'sd_trainer'
    training_folder: "/workspace/output"
    network:
      type: "lora"
      linear: 32           # rank — 32 for character, 64 if face is complex
      linear_alpha: 32     # match rank
    save:
      dtype: float16
      save_every: 250
    datasets:
      - folder_path: "/workspace/dataset"
        caption_ext: "txt"
        resolution: [512, 768, 1024]  # multi-res bucketing
        cache_latents_to_disk: true
    train:
      batch_size: 1
      steps: 2000           # 1500-3000 typical for 20 imgs
      gradient_accumulation_steps: 1
      train_unet: true
      train_text_encoder: false  # Flux: never train T5
      gradient_checkpointing: true
      noise_scheduler: "flowmatch"
      optimizer: "adamw8bit"
      lr: 1e-4
      ema_config:
        use_ema: true
        ema_decay: 0.99
    model:
      name_or_path: "black-forest-labs/FLUX.1-dev"
      is_flux: true
      quantize: true        # 8-bit quantize during training
    sample:
      sampler: "flowmatch"
      sample_every: 250
      width: 1024
      height: 1024
      prompts:
        - "ohwx_woman, in a coffee shop, natural light, candid"
        - "ohwx_woman, gym selfie, mirror, athletic outfit"
```

Run:
```bash
python run.py config/myproject.yaml
```

Spark training time: ~45-75 min for 2000 steps at batch 1. Save every 250 steps; pick the checkpoint that looks best in the sample previews (almost always one of 1500/1750/2000 — 2500+ overfits and burns in pose/outfit).

### Step 4: For FLUX.2

Use ai-toolkit's `train_lora_flux2_24gb.yaml` template. Same dataset works. Pin `is_flux2: true` in model section. Training time ~60% longer due to 9B parameter count. https://www.runcomfy.com/comfyui-nodes/trainer/ai-toolkit/flux-2-dev-lora-training

### Step 5: Spark / Blackwell extras

- Build PyTorch with CUDA 13.0 (cu130) so NVFP4 inference on the trained LoRA actually accelerates.
- SageAttention 2.2 sm_121 wheels skip the Triton kernel issue on GB10 — install before training. (Lesson `08-spark-blackwell-opt.md`.)
- 128 GB unified memory means you can train at rank 64 with `quantize: false` if you want max fidelity at 2x training time.

## Quality benchmarks

From kohya-ss/sd-scripts FLUX wiki and creator threads:

| Setting | Result |
|---|---|
| 15 images, rank 16, 1500 steps | Soft, generalizes well, slight identity drift |
| 20-30 images, rank 32, 2000 steps | **Sweet spot.** Sharp face, clean prompt-following |
| 40+ images, rank 32, 3000 steps | Tighter face but starts overfitting outfits/pose |
| 20 images, rank 64, 2000 steps | Sharper face details, slightly less prompt-flex |
| LR 1e-4 + adamw8bit | Standard. Stable. |
| LR 5e-5 + prodigy | Slower convergence, slightly higher peak quality |
| LR 1e-3 + lion | Fast, prone to bad-image collapse on small datasets (kohya Issue #1846: "Black images generated while training Lora with Flux") |

Quote from a top FluxGym creator review (DeepWiki Training Configuration page): "8 GB VRAM at rank 4 takes 6 hours and the result is mush. 16 GB at rank 16 with 20 images and 1500 steps got me a usable LoRA in 90 minutes that I happily use in production." — this is the threshold the course never communicates.

Failure mode catalog from kohya-ss Issue #1822 ("Bad Flux lora training result"): the #1 cause was T5 fine-tuning enabled (always disable for Flux), #2 was wrong noise scheduler (use `flowmatch`, not `ddpm`), #3 was overfit from too many similar images.

## Common failure modes + fixes

- **Black images on first sample step** → kohya Issue #1846. Cause: training in fp16 without scaling. Fix: switch optimizer to `adamw8bit` and enable `gradient_checkpointing`. Or use ai-toolkit which sets these correctly by default.
- **Face is "mush" or doesn't match** → either dataset is too small (under 12 imgs) or rank is too low (rank 4-8). Bump rank to 32 and add 5 more images.
- **LoRA burns in the outfit / pose** → too many steps, dataset too uniform. Cap at 2000 steps, force outfit variety in dataset.
- **Trigger word doesn't work** → rare token must actually be rare. `ohwx`, `zkz`, `tk2`, or made-up phrases like `eva24creator` work. Don't use real names ("emily") — Flux already knows them.
- **Multi-res bucket OOM on Spark** → Spark has 128 GB unified, won't OOM. On 4090 (24 GB), drop `resolution: [512, 768]` and skip 1024.
- **LoRA overfits to background** → add 2-3 segmented background-removed images to the dataset, or caption every image with the explicit background.

## When to choose this over the course's recipe

- **You want to own your creators.** Ship 5+ creators without per-character vendor cost.
- **You want iteration.** Re-train in 90 min when the look needs tweaking instead of waiting for Jack's queue.
- **You're on Spark.** 128 GB unified is overkill for Jack's setup; you can train at rank 64 quality he can't easily ship.
- **Stick with Jack** only if your single creator is locked-in long-term and you genuinely don't want to learn the toolkit. But even then, train your own as an A/B and compare.

## Sources

- https://github.com/ostris/ai-toolkit
- https://github.com/ostris/ai-toolkit/blob/main/config/examples/train_lora_flux_24gb.yaml
- https://www.runcomfy.com/comfyui-nodes/trainer/ai-toolkit/flux-2-dev-lora-training
- https://www.youtube.com/watch?v=qWDpPos6vrI (BFL FLUX.2 LoRA tutorial)
- https://github.com/kohya-ss/sd-scripts/blob/main/docs/flux_train_network.md
- https://github.com/kohya-ss/sd-scripts/issues/1846 (Black images bug)
- https://github.com/kohya-ss/sd-scripts/issues/1822 (Bad result diagnosis)
- https://deepwiki.com/kohya-ss/sd-scripts/6.3-flux-lora-training
- https://github.com/cocktailpeanut/fluxgym
- https://deepwiki.com/cocktailpeanut/fluxgym/3.3-training-configuration
- https://github.com/fpgaminer/joycaption
- https://huggingface.co/MiaoshouAI/Florence-2-large-PromptGen-v2.0
- https://github.com/MieMieeeee/ComfyUI-CaptionThis
- https://neurocanvas.net/blog/ai-toolkit-guide/
