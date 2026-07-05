---
name: ai-music
description: "AI music generation and audio tools: HeartMuLa lyrics-to-music generation, songwriting craft (+ Suno prompts), and audio spectrogram/feature visualization."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [music, audio, generation, ai, songwriting, lyrics, suno, spectrogram, heartmula]
    related_skills: [humanizer]
---

# AI Music & Audio Tools

Umbrella covering music generation, songwriting, and audio analysis. Each area has a dedicated reference file for detailed commands.

## Contents

1. [HeartMuLa — Music Generation from Lyrics + Tags](#1-heartmula--music-generation-from-lyrics--tags)
2. [Songwriting & AI Music Prompts (Suno)](#2-songwriting--ai-music-prompts)
3. [Audio Spectrogram & Feature Visualization](#3-audio-spectrogram--feature-visualization)

---

## 1. HeartMuLa — Music Generation (Lyrics + Tags)

**Full reference:** `references/heartmula.md`

HeartMuLa is an open-source (Apache-2.0) music foundation model family that generates songs from lyrics and style tags. Comparable to Suno for open-source.

### Prerequisites

```bash
git clone https://huggingface.co/heartmula/HeartMuLa-3B
# Or use via HuggingFace Inference API
```

### Quick Start

```python
from heartmula import HeartMuLa
model = HeartMuLa.from_pretrained("heartmula/HeartMuLa-3B")
audio = model.generate(lyrics="Verse 1...", tags="pop, upbeat, female vocals")
```

### Supported Tags

- Genre: pop, rock, jazz, classical, electronic, hip-hop, r&b, folk, metal, blues, country, latin, ambient, lo-fi
- Mood: happy, sad, energetic, calm, dark, uplifting, dreamy, aggressive, romantic, nostalgic
- Instrument: piano, guitar, drums, strings, synth, saxophone, flute, organ, bass, orchestra
- Vocal: male, female, duet, choir, rap, spoken, falsetto, harmonies, acapella
- Tempo: slow, medium, fast, bpm:120

---

## 2. Songwriting & AI Music Prompts

**Full reference:** `references/songwriting.md`

### Crafting Lyrics

**Golden rules:**
- Show, don't tell — use concrete imagery instead of abstract emotion
- Syllable count matters more than rhyme
- A strong hook repeats 3-4 times
- Write like you talk, then polish

### Song Structure

```
Intro (4-8 bars) → Verse (16 bars) → Chorus (8 bars) → Verse → Chorus → Bridge (8 bars) → Chorus (×2) → Outro
```

### Suno Prompt Patterns

| Style | Tags | Structure |
|-------|------|-----------|
| Pop | `pop, female vocals, upbeat, synth, 120bpm` | Verse-Chorus-Verse-Chorus-Bridge-Chorus |
| Rock | `rock, electric guitar, powerful male vocals, 140bpm` | Intro-Verse-Chorus-Verse-Solo-Chorus-Outro |
| Lo-fi | `lo-fi, chill, hip-hop beat, piano, 85bpm, vinyl crackle` | Verse-Chorus-Verse-Chorus-Outro |

### Parody & Adaptation

- Match syllable count and stress pattern of the original
- Keep the original rhyme scheme
- Use phonetic tricks for rhymes

---

## 3. Audio Spectrogram & Feature Visualization

**Full reference:** `references/songsee.md`

Use `songsee` CLI to generate spectrograms and audio feature visualizations from audio files.

### Quick Start

```bash
# Install
pip install songsee

# Generate mel spectrogram
songsee spectrogram input.mp3 -o output.png

# Features
songsee features input.mp3 --chroma --mfcc --tempogram
```

### Supported Visualizations

- **Mel spectrogram** — frequency content over time
- **Chroma** — pitch class distribution
- **MFCC** — timbral features (speech/music recognition)
- **Tempogram** — tempo and rhythmic patterns
- **Spectral features** — centroid, bandwidth, rolloff, flatness

### Use Cases

- Analyzing song structure (verse/chorus boundaries from spectral changes)
- Debugging audio processing pipelines
- Visual documentation for music production
- Comparing original vs generated audio quality