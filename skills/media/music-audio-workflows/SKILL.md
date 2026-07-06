---
name: music-audio-workflows
description: "Umbrella workflow for songwriting, AI music generation, and audio feature visualization/analysis."
origin: user
---

# Music and Audio Workflows

Use this umbrella when creating songs, prompting AI music systems, generating Suno-like tracks, or analyzing audio with spectrogram/features.

## Choose the workflow

| Intent | Pattern |
|---|---|
| Write lyrics or improve a song | Songwriting craft: concept, structure, hook, imagery, prosody. |
| Generate a track from lyrics/tags | HeartMuLa-style AI music generation: prepare `lyrics`, `tags`, then render. |
| Inspect or visualize audio | Songsee-style spectrogram/features: mel, chroma, MFCC, waveform, beat cues. |

## Songwriting craft

Start with a clear premise, singer perspective, emotional turn, and form. Check hook memorability, stress patterns, rhyme density, concrete imagery, and whether each section advances the song.

## AI music prompt preparation

Separate the artistic brief from generation inputs:

- Lyrics: complete sections with labels like `[Verse]`, `[Chorus]`, `[Bridge]` when supported.
- Tags: genre, tempo, instrumentation, vocal style, mood, production era.
- Negative constraints: what to avoid, if the generator supports them.

Verify generated files exist and can be played before claiming success.

## Audio analysis

Use feature extraction when the user asks what is happening in audio, needs visual assets, or wants to compare mixes. Return both high-level interpretation and the artifact path when producing images/audio-derived files.
