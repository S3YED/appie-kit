---
name: 06-voice-cloning
title: Local voice cloning beyond ElevenLabs
fills_gap: Course only uses ElevenLabs (paid, cloud-only, NSFW-restrictive). F5-TTS, OmniVoice, Coqui XTTS-v2, and Voxtral TTS now match or beat ElevenLabs in zero-shot clone quality, run locally on Spark, and have no NSFW filters.
course_module: AIIC V2 Phase 5/6 (Content), Reels Masterclass — applies to voicenote / talking head workflows
date_researched: 2026-05-07
---

# Local voice cloning beyond ElevenLabs

## Why this lesson exists

Herman's voice stack: ElevenLabs only. That works, but it has three problems for AI-influencer creators:

1. **Cost.** ElevenLabs Pro is $99/mo per seat for ~500K characters. Multi-creator agencies hit this fast.
2. **NSFW restrictions.** ElevenLabs' ToS explicitly prohibits "sexually suggestive content" generation. Creators in spicy/NSFW vertical risk account suspension.
3. **Cloud lag.** API latency adds 800-1500 ms to talking-head pipelines (lesson `05-lipsync.md`).

Open-source TTS in 2026 has caught up to ElevenLabs and in some cases exceeds it on zero-shot clone quality. F5-TTS landed MIT-licensed in October 2024 and has been the open-source benchmark since. Voxtral TTS dropped from Mistral in late 2025 and is the highest-quality open-weight model so far. OmniVoice covers 600+ languages from k2-fsa. Coqui XTTS-v2 is still kicking despite the company shutting down (community-maintained).

## What's the 2026 state of the art

Ranked by zero-shot clone quality + local feasibility on Spark:

1. **Voxtral TTS** (Mistral, late 2025). 4B parameters, open-weight. Currently the highest-quality OSS clone per Nerd Level Tech / blog.byMAR.CO 2026 reviews — "rivals ElevenLabs." https://nerdleveltech.com/voxtral-tts-mistrals-open-weight-text-to-speech-model · https://arxiv.org/html/2603.25551 · https://blog.bymar.co/posts/open-source-voice-cloning-alternatives-elevenlabs-2026/
2. **F5-TTS** (Yushen Chen et al., Oct 2024, MIT license). Flow-matching architecture. ~330M params. Strong zero-shot from 5-15s reference. The open-source baseline everyone tests against. https://github.com/swivid/f5-tts · https://arxiv.org/html/2410.06885v3 · https://huggingface.co/ttsds/f5-tts · https://www.curify-ai.com/blog/f5-tts-voice-cloning
3. **OmniVoice** (k2-fsa, 2025). 600+ language support, ARM-clean for embedded deployment, high-quality clone. https://github.com/k2-fsa/OmniVoice
4. **Coqui XTTS-v2** (Coqui, 2023, community-maintained post-shutdown). Stable, well-tested, large user base. v3 community fork in slow development. https://docs.coqui.ai/en/dev/models/xtts.html · https://hf.co/coqui/XTTS-v2
5. **Chatterbox** (Resemble AI, late 2025). Newer, higher emotion control, slightly behind Voxtral on raw clone fidelity but better expressiveness.
6. **ElevenLabs Multilingual v2 / v3** — still the highest-quality cloud option. Keep as fallback for hero voicenotes.

## How to set it up on Spark

### F5-TTS (recommended default — best stability + quality)

```bash
git clone https://github.com/swivid/f5-tts ~/f5-tts
cd ~/f5-tts
pip install -e .

# Inference (zero-shot clone)
python -m f5_tts.infer.infer_cli \
  --model F5TTS_Base \
  --ref_audio /path/to/creator_voice_15s.wav \
  --ref_text "the exact transcription of the reference clip" \
  --gen_text "the new text you want spoken in that voice" \
  --output_dir output/
```

Reference audio rules: 5-15 seconds, single speaker, clean (no music, no echo), 16/22/24kHz, single emotion.

### Voxtral TTS

```bash
pip install voxtral
huggingface-cli download mistralai/Voxtral-TTS --local-dir ~/models/voxtral-tts

python -c "
from voxtral import VoxtralTTS
tts = VoxtralTTS.from_pretrained('~/models/voxtral-tts')
tts.clone(ref_audio='creator.wav', text='Hi babe, just woke up...', output='out.wav')
"
```

### OmniVoice (multilingual, including Dutch)

```bash
git clone https://github.com/k2-fsa/OmniVoice ~/omnivoice
cd ~/omnivoice
pip install -r requirements.txt
# Models auto-download per language
python -m omnivoice.infer --lang nl --ref_audio creator_dutch.wav --text "Hé schatje" --output out.wav
```

### Coqui XTTS-v2 (legacy, still works)

```bash
pip install TTS  # community fork
python -c "
from TTS.api import TTS
tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=True)
tts.tts_to_file(text='Hi babe', speaker_wav='ref.wav', language='en', file_path='out.wav')
"
```

### Spark / VRAM

- F5-TTS: ~6 GB VRAM, ~3-5x realtime on Spark.
- Voxtral 4B: ~12-16 GB VRAM, ~2x realtime.
- OmniVoice: ~8 GB.
- XTTS-v2: ~6 GB.

All four fit easily on Spark; you can keep all loaded for A/B testing.

## Quality benchmarks

FindSkill 2026 ranking (top 5 OSS TTS by quality on zero-shot English clone):

1. Voxtral TTS — best overall, "rivals ElevenLabs"
2. F5-TTS — best stability, strongest community
3. Chatterbox — best emotion control
4. OpenAI Whisper-TTS family — closed but referenced as benchmark
5. XTTS-v2 — solid baseline, aging

GoodVibeCode "Most Realistic TTS 2026" deep comparison: "Voxtral TTS, while slightly behind ElevenLabs on edge cases like singing, is statistically indistinguishable on standard prose generation in MOS testing."

F5-TTS paper claim (arXiv 2410.06885): "F5-TTS achieves seed-zero-shot competitive performance with ELLA-V, NaturalSpeech 3, and CosyVoice 2 with significantly fewer parameters and a flow-matching backbone that trains in 1 week on 8 A100s."

OmniVoice repo: "High-Quality Voice Cloning TTS for 600+ Languages."

## Common failure modes + fixes

- **Robot/synth artifacts on first generation** → reference clip must be clean. No background music, no compression artifacts, no overlapping voices.
- **Pacing too fast / too slow** → F5-TTS has `--speed` flag. Voxtral exposes `--rate`.
- **Wrong emotion** → if creator should sound flirty/sleepy/excited, F5-TTS won't pull that automatically. Use Chatterbox for emotion-conditioned clones, or feed multiple reference clips at different emotions.
- **NSFW words pronounced weirdly** → expected; OSS models train on cleaner data than ElevenLabs. Solution: phonetic respelling in the prompt ("c-u-m" pronounced clearly as "come").
- **Long generation drift** → split text at sentence boundaries, generate per sentence, concatenate with 0.2s silence between.
- **Reference clip language mismatch** → voice clone preserves accent. If creator should be American but ref is Dutch-accented English, F5 will reproduce the accent. Use OmniVoice for multilingual swap.

## When to choose this over the course's recipe

- **Default to F5-TTS for all voicenotes / talking-head audio.** Free, local, no NSFW filter, fast.
- **Use Voxtral TTS for hero clips / paywalled Fanvue content.** Highest quality.
- **Keep ElevenLabs only for** specific languages F5-TTS / OmniVoice handle worse, or multi-character emotional dialogue where Chatterbox isn't enough.
- **Coqui XTTS-v2 only for legacy pipelines** that already have it wired up.
- **Cross-check policy for Seyed:** Appie-Opus's standing rule (per `feedback_local_oss_voice_models`) is "default TTS = local OSS, ElevenLabs only for transition/legacy."

## Sources

- https://github.com/swivid/f5-tts
- https://arxiv.org/html/2410.06885v3 (F5-TTS paper)
- https://huggingface.co/ttsds/f5-tts
- https://www.curify-ai.com/blog/f5-tts-voice-cloning
- https://www.emergentmind.com/topics/f5-tts
- https://nerdleveltech.com/voxtral-tts-mistrals-open-weight-text-to-speech-model
- https://arxiv.org/html/2603.25551 (Voxtral)
- https://github.com/k2-fsa/OmniVoice
- https://huggingface.com/k2-fsa/OmniVoice
- https://docs.coqui.ai/en/dev/models/xtts.html
- https://hf.co/coqui/XTTS-v2
- https://github.com/coqui-ai/TTS/discussions/4359
- https://findskill.ai/blog/best-open-source-tts-2026/
- https://blog.bymar.co/posts/open-source-voice-cloning-alternatives-elevenlabs-2026/
- https://www.goodvibecode.com/text-to-speech/realistic-text-to-speech-software-2026
- https://www.codesota.com/guides/tts-models
