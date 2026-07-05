---
name: ai-music-generation
description: Generate music and audio with AI — AudioCraft (MusicGen/AudioGen from Meta) and HeartMuLa (open-source Suno-like lyrics+tags generation). Installation, model selection, prompt patterns, and hardware requirements.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [music, audio, generation, ai, audiocraft, heartmula, musicgen, text-to-music]
    related_skills: [songwriting-and-ai-music]
---

# AI Music Generation

## Overview

Two open-source AI music generation frameworks, each with different strengths:

| Framework | Best for | Output | License |
|-----------|----------|--------|---------|
| **AudioCraft (Meta)** | Text-to-music, text-to-sound, melody conditioning, audio codec | WAV/MP3, 32/16kHz | MIT |
| **HeartMuLa** | Lyrics+tags → full songs, Suno-like, multilingual | MP3, 48kHz stereo | Apache-2.0 |

**Decision:**
- **AudioCraft** when you need text prompts only, sound effects, melody conditioning, or stereo audio infrastructure
- **HeartMuLa** when you have specific lyrics and want a full song with tags (like Suno)

---

## Section A: AudioCraft (MusicGen / AudioGen / EnCodec)

### Quick Start

```bash
pip install audiocraft
# Or via HuggingFace transformers:
pip install transformers torch torchaudio
```

### Text-to-Music (MusicGen)

```python
import torchaudio
from audiocraft.models import MusicGen

model = MusicGen.get_pretrained('facebook/musicgen-medium')
model.set_generation_params(duration=8, top_k=250, temperature=1.0)

wav = model.generate(["happy upbeat electronic dance music"])
torchaudio.save("output.wav", wav[0].cpu(), sample_rate=32000)
```

Using HuggingFace Transformers:
```python
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to("cuda")

inputs = processor(text=["80s pop with bassy drums"], padding=True, return_tensors="pt").to("cuda")
audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=256)
scipy.io.wavfile.write("output.wav", rate=model.config.audio_encoder.sampling_rate, data=audio_values[0, 0].cpu().numpy())
```

### Model Variants

| Model | Size | Use Case |
|-------|------|----------|
| `musicgen-small` | 300M | Quick generation |
| `musicgen-medium` | 1.5B | Balanced quality/speed |
| `musicgen-large` | 3.3B | Best quality |
| `musicgen-melody` | 1.5B | Melody conditioning |
| `musicgen-stereo-*` | Varies | Stereo output |
| `musicgen-style` | 1.5B | Style transfer |
| `audiogen-medium` | 1.5B | Sound effects |

### Melody-Conditioned Generation

```python
model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=30)

melody, sr = torchaudio.load("melody.wav")
wav = model.generate_with_chroma(["acoustic guitar folk song"], melody, sr)
torchaudio.save("output.wav", wav[0].cpu(), sample_rate=32000)
```

### Text-to-Sound (AudioGen)

```python
from audiocraft.models import AudioGen
model = AudioGen.get_pretrained('facebook/audiogen-medium')
model.set_generation_params(duration=5)
wav = model.generate(["dog barking in park with birds chirping"])
torchaudio.save("sound.wav", wav[0].cpu(), sample_rate=16000)
```

### GPU Memory Requirements

| Model | FP32 | FP16 |
|-------|------|------|
| musicgen-small | ~4GB | ~2GB |
| musicgen-medium | ~8GB | ~4GB |
| musicgen-large | ~16GB | ~8GB |

---

## Section B: HeartMuLa

Hardware minimum: 8GB VRAM (`--lazy_load true`), recommended 16GB+.

### Installation

```bash
git clone https://github.com/HeartMuLa/heartlib.git
cd heartlib
uv venv --python 3.10 .venv
. .venv/bin/activate
uv pip install -e .

# Fix dependency conflicts
uv pip install --upgrade datasets transformers
```

### Patch Source Code

**Patch 1** — In `src/heartlib/heartmula/modeling_heartmula.py`, in `setup_caches`, add RoPE reinitialization after `reset_caches`:
```python
from torchtune.models.llama3_1._position_embeddings import Llama3ScaledRoPE
for module in self.modules():
    if isinstance(module, Llama3ScaledRoPE) and not module.is_cache_built:
        module.rope_init()
        module.to(device)
```

**Patch 2** — In `src/heartlib/pipelines/music_generation.py`, add `ignore_mismatched_sizes=True` to all `HeartCodec.from_pretrained()` calls.

### Download Checkpoints

```bash
cd heartlib
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B-happy-new-year'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss-20260123'
```

### Generate Music

```bash
. .venv/bin/activate
python ./examples/run_music_generation.py \
  --model_path=./ckpt --version="3B" \
  --lyrics="./assets/lyrics.txt" --tags="./assets/tags.txt" \
  --save_path="./assets/output.mp3" --lazy_load true
```

**Tags format:** comma-separated, no spaces: `piano,happy,wedding,synthesizer`
**Lyrics format:** use bracketed structural tags: `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]`

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--max_audio_length_ms` | 240000 | Max length in ms (240s = 4 min) |
| `--topk` | 50 | Top-k sampling |
| `--temperature` | 1.0 | Sampling temperature |
| `--cfg_scale` | 1.5 | Classifier-free guidance scale |
| `--lazy_load` | false | Load/unload models on demand |

### Pitfalls

1. Do NOT use bf16 for HeartCodec — degrades audio quality
2. Tags may be ignored — lyrics tend to dominate
3. Triton not available on macOS — Linux/CUDA only
4. No GPU → extremely slow on CPU (30-60+ min per song)
5. RTX 5080 incompatibility reported upstream

### Links

- Repo: https://github.com/HeartMuLa/heartlib
- Models: https://huggingface.co/HeartMuLa
- Paper: https://arxiv.org/abs/2601.10547