---
name: ai-music-generation
description: Generate music and audio with AI — Suno, MusicGen, HeartMuLa, AudioCraft, and audio analysis via spectrograms.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [music, audio, generation, songwriting, suno, audiocraft, heartmula, spectrogram, creative]
    related_skills: []
---

# AI Music Generation

Generate music, songs, and audio using AI tools. This umbrella covers:

- **Songwriting craft & Suno prompts** — writing lyrics, structuring songs, engineering Suno music AI prompts
- **AudioCraft (MusicGen/AudioGen)** — Meta's text-to-music and text-to-sound models
- **HeartMuLa** — open-source music generation from lyrics + tags
- **SongSee** — audio spectrogram and feature visualization

## When to Use

Load this skill when the user asks to:
- Write a song, parody, or lyrics
- Generate music from text descriptions (Suno, MusicGen, HeartMuLa, etc.)
- Create sound effects from text
- Analyze or visualize audio (spectrograms, MFCCs, chroma features)
- Compare AI music generation tools

## Quick Reference

| Tool | Use Case | Format |
|------|----------|--------|
| Suno (via songwriting skill) | Full songs from lyrics + style tags + structure | Web UI via prompt engineering |
| AudioCraft / MusicGen | Text-to-music, melody conditioning, stereo | Python (audiocraft or transformers) |
| HeartMuLa | Open-source Suno alternative, lyrics+tags | Python (heartlib) |
| SongSee | Audio spectrogram visualization | CLI (Go binary) |

---

## 1. Songwriting & Suno AI Prompts

See `references/songwriting-and-ai-music.md` for the full craft guide. Key sections:

### Song Structure
Common forms: ABABCB (verse/chorus), AABA (jazz standard), ABAB (alternating), AAA (strophic).

### Suno Style Prompt Formula
```
Genre + Mood + Era + Instruments + Vocal Style + Production + Dynamics
```

Bad: `"sad rock song"`
Good: `"Cinematic orchestral spy thriller, 1960s Cold War era, smoky sultry female vocalist, big band jazz, brass section with trumpets and french horns, sweeping strings, minor key, vintage analog warmth"`

### Suno Metatags
Place `[bracketed tags]` in the lyrics field:
- **Structure**: `[Intro]` `[Verse]` `[Pre-Chorus]` `[Chorus]` `[Bridge]` `[Outro]`
- **Vocal**: `[Whispered]` `[Belted]` `[Falsetto]` `[Breathy]` `[Raspy]` `[Soulful]`
- **Dynamics**: `[High Energy]` `[Building Energy]` `[Explosive]` `[Emotional Climax]`
- **Atmosphere**: `[Melancholic]` `[Euphoric]` `[Nostalgic]` `[Aggressive]`

### Phonetic Tricks
Spell words as they sound: `"through"` → `"thru"`, `"Nous"` → `"Noose"`. Use ALL CAPS for emphasis, hyphens for sustained notes (`"lo-o-o-ove"`).

---

## 2. AudioCraft (MusicGen / AudioGen)

See `references/audiocraft-audio-generation.md` (quickstart + core usage) and `references/audiocraft-advanced.md` (fine-tuning, deployment, evaluation). `references/audiocraft-troubleshooting.md` covers common issues.

### Quick Start
```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained('facebook/musicgen-small')
model.set_generation_params(duration=8)
wav = model.generate(["upbeat electronic dance music with synths"])
torchaudio.save("output.wav", wav[0].cpu(), sample_rate=32000)
```

### Model Variants
| Model | Size | Use Case |
|-------|------|----------|
| `musicgen-small` | 300M | Quick generation |
| `musicgen-medium` | 1.5B | Balanced quality/speed |
| `musicgen-large` | 3.3B | Best quality |
| `musicgen-melody` | 1.5B | Melody-conditioned generation |
| `musicgen-stereo-medium` | 1.5B | Stereo output |
| `musicgen-style` | 1.5B | Style transfer |
| `audiogen-medium` | 1.5B | Sound effects |

### Generation Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `duration` | 8.0 | Length in seconds (1-120) |
| `top_k` | 250 | Top-k sampling |
| `top_p` | 0.0 | Nucleus sampling (0 = disabled) |
| `temperature` | 1.0 | Sampling temperature |
| `cfg_coef` | 3.0 | Classifier-free guidance |

---

## 3. HeartMuLa (Open-Source Music Generation)

See `references/heartmula.md` for full installation, patching, and usage.

HeartMuLa generates full songs from lyrics + tags. Requires Python 3.10 and a GPU (≥8GB VRAM).

### Key Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--max_audio_length_ms` | 240000 | Max length in ms |
| `--topk` | 50 | Top-k sampling |
| `--temperature` | 1.0 | Sampling temperature |
| `--cfg_scale` | 1.5 | Classifier-free guidance scale |
| `--lazy_load` | false | Load/unload models on demand |

### Known Pitfalls
- Do NOT use bf16 for HeartCodec (degrades quality)
- Tags may be ignored — lyrics dominate
- Dependency pin conflicts require manual upgrades (see reference)
- Triton not available on macOS

---

## 4. SongSee (Audio Visualization)

See `references/songsee.md` for full CLI usage.

Generate spectrograms and multi-panel audio feature visualizations.

### Quick Start
```bash
go install github.com/steipete/songsee/cmd/songsee@latest
songsee track.mp3 --viz spectrogram,mel,chroma,hpss --style magma -o analysis.png
```

### Visualization Types
| Type | Description |
|------|-------------|
| `spectrogram` | Standard frequency spectrogram |
| `mel` | Mel-scaled spectrogram |
| `chroma` | Pitch class distribution |
| `hpss` | Harmonic/percussive separation |
| `mfcc` | Mel-frequency cepstral coefficients |
| `tempogram` | Tempo estimation |

## Common Pitfalls

1. **Suno: NO artist names or trademarks** — describe the sound instead. "1960s Cold War spy thriller brass" not "James Bond style."
2. **Suno: Always use Custom Mode** — separate Style + Lyrics fields. Add structural tags or Suno defaults to flat verse/chorus.
3. **AudioCraft: pdb under pytest-xdist silently does nothing** — use `-p no:xdist`.
4. **AudioCraft: MusicGen outputs at 32kHz, AudioGen at 16kHz** — use the right sample rate when saving.
5. **HeartMuLa: Don't skip the source patches** — the dependency pins are outdated as of Feb 2026; the reference has exact patches.
6. **SongSee: WAV/MP3 decoded natively; other formats need ffmpeg.**
