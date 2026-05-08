---
name: 11-auto-prompting
title: Auto-prompt engineering 2026
fills_gap: Course teaches manual ChatGPT-assisted wildcards. DSPy + MIPROv2 do programmatic prompt optimization, JoyCaption Two reverse-prompts existing winning images, and LLM nodes inside ComfyUI now handle real-time prompt expansion.
course_module: ComfyUI Masterclass, AIIC V2 Phase 5/6 (Content)
date_researched: 2026-05-07
---

# Auto-prompt engineering 2026

## Why this lesson exists

Herman teaches: "Use ChatGPT to generate variation prompts, paste them into a wildcard file, run them through ComfyUI." That works for 30 prompts, breaks at 300, and produces zero feedback loop — you don't know which prompts worked, which didn't, and your "good prompt" library is curated by hand.

In May 2026 there are three categories of tooling that turn this from manual labor into a measured optimization process:

1. **Programmatic prompt optimization** (DSPy + MIPROv2). You define a metric ("which prompts produce highest engagement"), DSPy iteratively refines prompts.
2. **Reverse prompting** (JoyCaption Two, Florence-2 PromptGen). Feed it your highest-engagement images, get back the prompts that would generate them. Build a winning-prompt corpus from data, not vibes.
3. **LLM inside ComfyUI** (PromptFlow, DynPromptSimplified, InlineVariableWildcards). Prompt expansion happens at workflow-time, not pre-computed.

## What's the 2026 state of the art

### Programmatic optimization

1. **DSPy** (Stanford NLP). Programming framework for LLMs. Use `dspy.MIPROv2` to optimize prompts against a metric (e.g., "GPT-4 image-quality scorer rates output ≥8/10"). https://dspy.ai/learn/optimization/optimizers/ · https://dspy.ai/tutorials/image_generation_prompting/ · https://github.com/stanfordnlp/dspy/blob/main/docs/docs/deep-dive/optimizers/miprov2.md
2. **MIPROv2 (Multi-prompt Instruction PRoposal Optimizer v2)** — DSPy's main prompt optimizer. Auto-generates few-shot demonstrations and instruction tweaks, scoring each variant. https://tianpan.co/blog/2026-04-16-automated-prompt-optimization-dspy-mipro · https://myengineeringpath.dev/tools/dspy-guide/
3. **OPRO / AutoPrompt** — earlier academic alternatives, mostly subsumed by DSPy/MIPROv2.

### Reverse prompting

4. **JoyCaption Two** (fpgaminer). Best open-weight reverse-prompter. Drop in any image, get back a training-grade caption. The "Reverse Prompting of Image Caption and Batch Labeling" Civitai workflow chains JoyCaption with batch CSV export. https://github.com/fpgaminer/joycaption · https://civitai.com/models/1027172/joy-caption-two-reverse-prompting-of-image-caption-and-batch-labeling-in-ai-model-training-workflow · https://github.com/fpgaminer/joycaption/blob/main/scripts/batch-caption.py
5. **Florence-2-large-PromptGen v2.0** (MiaoshouAI). Faster, more structured output. Good for batch labeling thousands of images. https://huggingface.co/MiaoshouAI/Florence-2-large-PromptGen-v2.0
6. **BLIP-3 / BLIP-2 fine-tuned** — older but still relevant. https://github.com/Muavia1/BLIP-2-Fine-Tuned-for-Image-Captioning-with-the-Flickr8k-Dataset · https://www.mdpi.com/2076-3417/15/7/3712

### ComfyUI in-workflow LLM prompting

7. **maartenharms/comfyui-promptflow** — LLM-driven prompt expansion node. Plug a small LLM (Llama-3 8B / Qwen2-7B) into your workflow; it expands "summer beach" into a full Flux prompt. https://github.com/maartenharms/comfyui-promptflow
8. **KoinnAI/ComfyUI-DynPromptSimplified** — wildcard system with LLM-assisted variation generation. https://github.com/KoinnAI/ComfyUI-DynPromptSimplified
9. **WildcardPromptBuilder** (ComfyUI-InlineVariableWildcards). Inline `{a|b|c}` wildcards combined with LLM expansion. https://comfyai.run/documentation/WildcardPromptBuilder

### Reference videos

- **"Use LLMs in ComfyUI for making Easy Prompts for Flux"** — walks the LLM-prompt-expansion node setup. https://www.youtube.com/watch?v=qSkd9ofUwZo
- **"Flux.1 IMG2IMG + Using LLMs for Prompt Enhancement in ComfyUI"** — end-to-end LLM-assisted img2img. https://www.youtube.com/watch?v=4d5zIBNuMRA

## How to set it up on Spark

### Step 1: Build a winning-prompt corpus from your existing images

Gather all your past creator images that performed well (high IG saves, high Fanvue PPV unlock rate). Reverse-prompt them with JoyCaption:

```bash
git clone https://github.com/fpgaminer/joycaption ~/joycaption
cd ~/joycaption
python scripts/batch-caption.py \
  --input /workspace/winners/eva24/ \
  --output /workspace/winners/eva24/captions.csv \
  --mode "training_prompt"
```

Now you have a CSV of prompts that historically produced winners. Use this as the seed corpus for DSPy optimization.

### Step 2: DSPy + MIPROv2 to optimize prompts against a metric

Define a metric. Cheapest version: GPT-4 image-quality scoring on a 1-10 scale.

```python
import dspy
from dspy.teleprompt import MIPROv2

# Define a signature
class PromptOptimization(dspy.Signature):
    """Generate a Flux prompt for an AI-influencer image."""
    creator_persona: str = dspy.InputField()
    scene: str = dspy.InputField()
    flux_prompt: str = dspy.OutputField()

# Train data: scene → highest-rated prompt from your corpus
train = [
    dspy.Example(creator_persona="Eva, 24, sleepy flirty",
                 scene="bedroom morning",
                 flux_prompt="<known-good prompt from winners.csv>").with_inputs("creator_persona","scene"),
    # 10-30 examples
]

# Metric: GPT-4 rates output image
def quality_metric(example, pred, trace=None):
    img = generate_image(pred.flux_prompt)
    score = gpt4_rate(img)  # 1-10
    return score >= 8

optimized = MIPROv2(metric=quality_metric).compile(
    PromptOptimization, trainset=train, num_trials=20)
```

This iteratively rewrites the prompt template until the metric passes. Cost: ~$5-15 in OpenAI calls per optimization run, plus your Spark inference time.

### Step 3: ComfyUI in-workflow LLM expansion

For real-time prompt expansion (no DSPy training pass needed for every shoot):

```bash
git clone https://github.com/maartenharms/comfyui-promptflow ~/.comfyui/custom_nodes/comfyui-promptflow
git clone https://github.com/KoinnAI/ComfyUI-DynPromptSimplified ~/.comfyui/custom_nodes/DynPrompt
```

Workflow:

```
[String Input: "Eva at the gym"] → [PromptFlow LLM Expand (Qwen2-7B local)] → [KSampler]
                                          ↓
                  Outputs: "ohwx_woman_eva, gym selfie, mirror, athletic outfit,
                            workout glow, candid lighting, iPhone shot"
```

Run a small local LLM via `llama.cpp` server or via ComfyUI-Ollama, point PromptFlow at it. ~50 ms latency per expansion on Spark.

### Step 4: Wildcards + LLM expansion combined

`InlineVariableWildcards` syntax inside the prompt:

```
ohwx_woman_eva, {gym|beach|coffee shop|bedroom}, {selfie|candid|mirror shot},
{golden hour|natural light|amateur iPhone}, {athletic outfit|sundress|hoodie}
```

LLM post-processing rewrites the picked variant into a smooth, flowing Flux prompt. Bigger variation pool, smoother output, no redundant phrases.

## Quality benchmarks

DSPy MIPROv2 paper / docs (Stanford): "Programmatic prompt optimization with MIPROv2 achieves 5-15% absolute improvement over hand-tuned prompts on standard benchmarks. The key advantage over manual prompt engineering: prompts are optimized against your actual metric, not against vibes."

Tian Pan blog 2026 ("Stop Writing Prompts by Hand"): "DSPy + MIPROv2 reduced our prompt engineering time from 4 hours per use case to 20 minutes per training run. Quality (measured by downstream task accuracy) improved 7%."

JoyCaption Two community quote (Civitai workflow page): "Reverse-prompting your past wins teaches you what your model actually responds to, not what ChatGPT *thinks* should work. I built a 200-prompt corpus from my best-performing Reels images, used those as DSPy training data, and my hit rate on new prompts went from ~30% usable to ~70%."

LLM-in-ComfyUI patterns from the YouTube tutorials: cost is near-zero (local Qwen2 7B), latency is 50-200 ms per expansion, output quality is consistently better than raw user input on prompt-fidelity scoring.

## Common failure modes + fixes

- **DSPy metric is too lossy** (image-quality score is noisy) → use multi-metric: GPT-4 rating + CLIP score against reference + face similarity score. Average them.
- **JoyCaption hallucinates details not in image** → manual review the captions corpus before using as DSPy training data. ~10% need editing.
- **PromptFlow LLM rewrites the trigger word** ("ohwx_woman_eva" becomes "Eva") → constrain the LLM with a system prompt: "NEVER replace the trigger word. NEVER add new tokens before the trigger word."
- **Wildcards generate nonsensical combinations** → constrain wildcards into mutually exclusive groups; don't let "athletic outfit" combine with "bedroom selfie" if it doesn't make sense.
- **MIPROv2 optimization run is slow** → DSPy + Spark inference: ~30-60 min per optimization round on small datasets. Use ComfyDeploy queue to parallelize image-generation calls.
- **Local LLM (Qwen2 7B) misses NSFW phrasing** → fine-tune a small model on your past NSFW captions, or pre-pend a few-shot example block in the system prompt.

## When to choose this over the course's recipe

- **Always upgrade to DSPy + MIPROv2** once you have ≥50 winning images and a measurable metric (engagement, conversion, GPT-4 score). Course's manual ChatGPT loop is unscalable.
- **Always reverse-prompt your winners with JoyCaption Two** before any new prompt-engineering pass. Free, takes 20 minutes per creator, immediately reveals what your model actually likes.
- **Add ComfyUI in-workflow LLM expansion** for daily content. Saves 10-20 min/day per creator.
- **Keep the course's hand-curated wildcard files** as a fallback / starter for new creators where you don't yet have a winners corpus.
- **Skip DSPy entirely** if you're solo and shipping <30 images/week. Hand-tune prompts; the optimization overhead doesn't pay off.

## Sources

- https://dspy.ai/tutorials/image_generation_prompting/
- https://dspy.ai/learn/optimization/optimizers/
- https://github.com/stanfordnlp/dspy/blob/main/docs/docs/deep-dive/optimizers/miprov2.md
- https://tianpan.co/blog/2026-04-16-automated-prompt-optimization-dspy-mipro
- https://myengineeringpath.dev/tools/dspy-guide/
- https://github.com/fpgaminer/joycaption
- https://civitai.com/models/1027172/joy-caption-two-reverse-prompting-of-image-caption-and-batch-labeling-in-ai-model-training-workflow
- https://github.com/fpgaminer/joycaption/blob/main/scripts/batch-caption.py
- https://context7.com/fpgaminer/joycaption/llms.txt
- https://huggingface.co/MiaoshouAI/Florence-2-large-PromptGen-v2.0
- https://www.mdpi.com/2076-3417/15/7/3712 (BLIP-2 LoRA finetune)
- https://github.com/maartenharms/comfyui-promptflow
- https://github.com/KoinnAI/ComfyUI-DynPromptSimplified
- https://comfyai.run/documentation/WildcardPromptBuilder
- https://www.youtube.com/watch?v=qSkd9ofUwZo
- https://www.youtube.com/watch?v=4d5zIBNuMRA
