---
name: open-source-music-generation
description: "Open-source AI music generation tools — HeartMuLa (lyrics+tags) and AudioCraft/MusicGen (text-to-music, text-to-sound). Covers installation, generation parameters, model variants, and pitfalls for both ecosystems."
version: 1.0.0
author: Hermes Agent
tags: [music, audio, generation, ai, open-source, heartmula, audiocraft, musicgen, audiogen, encodec]
---

# Open-Source Music Generation

A unified guide to two major open-source music generation ecosystems: **HeartMuLa** and **AudioCraft (MusicGen/AudioGen)**. Both generate audio from text descriptions; HeartMuLa specializes in lyrics-conditioned song generation while AudioCraft offers broader text-to-music and text-to-sound capabilities with melody conditioning.

## Quick Comparison

| Feature | HeartMuLa | AudioCraft |
|---------|-----------|------------|
| Focus | Lyrics+tags song generation | Text-to-music, text-to-sound |
| Model sizes | 3B, 7B | 300M (small) to 3.3B (large) |
| Output | MP3 48kHz stereo | WAV 32kHz mono/stereo |
| VRAM (min) | ~6.2GB (3B lazy) | ~2GB (small fp16) to ~16GB (large) |
| Lyrics support | Core feature (required) | Not supported (text-only) |
| Melody conditioning | No | Yes (musicgen-melody) |
| License | Apache-2.0 | MIT |
| Setup complexity | Medium (patches needed) | Low (pip install) |

**When to use HeartMuLa:** You need to generate a full song with lyrics, multiple languages, or want the most open-source-capable Suno alternative.

**When to use AudioCraft:** You need text-to-music or text-to-sound effects, melody conditioning, stereo output, or style transfer.

---

## HeartMuLa — Lyrics-to-Song Generation

HeartMuLa generates full songs from lyrics + genre/style tags. Families of models: HeartMuLa (music language model), HeartCodec (12.5Hz audio codec), HeartTranscriptor (lyrics transcription), HeartCLAP (audio-text alignment).

### Hardware Requirements

- **Minimum**: 8GB VRAM with `--lazy_load true` (loads/unloads models sequentially, peaks ~6.2GB)
- **Recommended**: 16GB+ VRAM for single-GPU
- **Multi-GPU**: `--mula_device cuda:0 --codec_device cuda:1`
- **CPU mode**: Possible with `--mula_device cpu --codec_device cpu` but extremely slow (30-60 min per song)

### Installation

```bash
# 1. Clone
git clone https://github.com/HeartMuLa/heartlib.git
cd heartlib

# 2. Python 3.10 venv
uv venv --python 3.10 .venv
. .venv/bin/activate
uv pip install -e .

# 3. Fix dependency conflicts
uv pip install --upgrade datasets transformers

# 4. Download models (all in parallel)
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B-happy-new-year'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss-20260123'
```

### Source Patches Required

**Patch 1 — RoPE cache fix** in `src/heartlib/heartmula/modeling_heartmula.py`:
Add RoPE reinitialization in `setup_caches` after `reset_caches` and before `with device:`:
```python
from torchtune.models.llama3_1._position_embeddings import Llama3ScaledRoPE
for module in self.modules():
    if isinstance(module, Llama3ScaledRoPE) and not module.is_cache_built:
        module.rope_init()
        module.to(device)
```

**Patch 2 — HeartCodec loading fix** in `src/heartlib/pipelines/music_generation.py`:
Add `ignore_mismatched_sizes=True` to ALL `HeartCodec.from_pretrained()` calls.

### Usage

```bash
cd heartlib && . .venv/bin/activate
python ./examples/run_music_generation.py \
  --model_path=./ckpt \
  --version="3B" \
  --lyrics="./assets/lyrics.txt" \
  --tags="./assets/tags.txt" \
  --save_path="./assets/output.mp3" \
  --lazy_load true
```

**Tags** (comma-separated, no spaces): `piano,happy,wedding,synthesizer,romantic`
**Lyrics** use bracketed structural tags: `[Intro]`, `[Verse]`, `[Chorus]`, `[Bridge]`, `[Outro]`

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--max_audio_length_ms` | 240000 | Max length (240s = 4 min) |
| `--temperature` | 1.0 | Sampling temperature |
| `--cfg_scale` | 1.5 | Classifier-free guidance scale |
| `--lazy_load` | false | Load/unload models on demand |

**Pitfall:** Do NOT use bf16 for HeartCodec — degrades audio quality. Use fp32.

### Links
- Repo: https://github.com/HeartMuLa/heartlib
- Models: https://huggingface.co/HeartMuLa
- Paper: https://arxiv.org/abs/2601.10547
- License: Apache-2.0

---

## AudioCraft — Text-to-Music and Text-to-Sound

Meta's AudioCraft framework covers MusicGen (text-to-music), AudioGen (text-to-sound), and EnCodec (neural audio codec).

### Quick Start

```bash
pip install audiocraft
# Or for latest: pip install git+https://github.com/facebookresearch/audiocraft.git
```

### Model Variants

| Model | Size | Use Case |
|-------|------|----------|
| `musicgen-small` | 300M | Quick generation |
| `musicgen-medium` | 1.5B | Balanced quality/speed |
| `musicgen-large` | 3.3B | Best quality |
| `musicgen-melody` | 1.5B | Melody-conditioned generation |
| `musicgen-stereo-medium` | 1.5B | Stereo output |
| `musicgen-style` | 1.5B | Style transfer from reference audio |
| `audiogen-medium` | 1.5B | Sound effects generation |

### Basic Text-to-Music

```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained('facebook/musicgen-medium')
model.set_generation_params(duration=30, top_k=250, temperature=1.0, cfg_coef=3.0)
wav = model.generate(["upbeat electronic dance music with synths"])
torchaudio.save("output.wav", wav[0].cpu(), sample_rate=32000)
```

### Text-to-Sound (AudioGen)

```python
from audiocraft.models import AudioGen
model = AudioGen.get_pretrained('facebook/audiogen-medium')
model.set_generation_params(duration=5)
wav = model.generate(["dog barking in a park with birds chirping"])
torchaudio.save("sound.wav", wav[0].cpu(), sample_rate=16000)
```

### Melody Conditioning

```python
from audiocraft.models import MusicGen
model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=30)
melody, sr = torchaudio.load("melody.wav")
wav = model.generate_with_chroma(["acoustic guitar folk song"], melody, sr)
```

### Generation Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `duration` | 8.0 | Length in seconds (1-120) |
| `top_k` | 250 | Top-k sampling |
| `top_p` | 0.0 | Nucleus sampling |
| `temperature` | 1.0 | Sampling temperature |
| `cfg_coef` | 3.0 | Classifier-free guidance |

### Performance

| Model | FP32 VRAM | FP16 VRAM | Generation Time (30s) |
|-------|-----------|-----------|----------------------|
| musicgen-small | ~4GB | ~2GB | ~5s |
| musicgen-medium | ~8GB | ~4GB | ~15s |
| musicgen-large | ~16GB | ~8GB | ~30s |

### Advanced Usage

See `references/audiocraft-advanced-usage.md` for fine-tuning, MultiBand Diffusion, API server deployment, batch processing, LangChain integration, and evaluation.

### Troubleshooting

See `references/audiocraft-troubleshooting.md` for common installation, model loading, generation, memory, and format issues.

### Links
- GitHub: https://github.com/facebookresearch/audiocraft
- Paper (MusicGen): https://arxiv.org/abs/2306.05284
- Paper (AudioGen): https://arxiv.org/abs/2209.15352
- HuggingFace: https://huggingface.co/facebook/musicgen-small

