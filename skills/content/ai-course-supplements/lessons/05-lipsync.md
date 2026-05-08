---
name: 05-lipsync
title: Lipsync and talking-head video
fills_gap: Course doesn't teach lipsync at all. Three open-source models now produce real-time, identity-preserving talking-head video from photo + audio, opening up an entire content format (Reels with the creator "speaking") that the course's pipeline can't reach.
course_module: (new topic) — adjacent to AIIC V2 Phase 5 (Content), Reels Masterclass
date_researched: 2026-05-07
---

# Lipsync and talking-head video

## Why this lesson exists

Herman's course never covers lipsync. The closest he gets is "use ElevenLabs for voicenotes" and "post audio over a still image." Result: every "talking" creator clip in the course is a still image with a voiceover. Real talking-head video — where the AI creator's mouth actually moves to a TTS audio track — is a meta-format that's been blowing up on Reels and TikTok since late 2025, especially for "creator answers questions" / "creator reads thirst trap text" formats.

Three open-source models now do this well, all in May 2026:

- **MuseTalk 1.5** (Tencent Lyra): real-time, lip-sync via spatio-temporal sampling.
- **LatentSync** (ByteDance): latent-space diffusion lipsync, often visually best on long clips.
- **Wan2.2-S2V-14B** (Alibaba): full body + face audio-driven cinematic video, beats MultiTalk/InfiniteTalk per creator threads.

All three run on Spark / single 4090. None of them are in the course.

## What's the 2026 state of the art

Ranked by use case:

1. **MuseTalk 1.5** (Tencent / Lyralab). Real-time inference (30+ fps). Best for short clips, fastest. Trained for high-fidelity lipsync via latent-space inpainting. https://github.com/TMElyralab/MuseTalk · https://arxiv.org/html/2410.10122v3 · https://huggingface.co/marcosremar2/MuseTalk
2. **LatentSync** (ByteDance, NeurIPS 2024 / 2025-2026 updates). Audio-conditioned latent diffusion. Generally produces highest visual quality but is slower than MuseTalk. https://github.com/Latentsync/LatentSync · https://arxiv.org/abs/2412.09262v1
3. **Wan2.2-S2V-14B** (Alibaba). Full cinematic shot from image + audio, including body motion and head pose. Beats MultiTalk and InfiniteTalk per creator reports. Best for "talking head with body language." https://huggingface.co/Wan-AI/Wan2.2-S2V-14B · https://docs.comfy.org/tutorials/video/wan/wan2-2-s2v
4. **Wav2Lip 2026 / LPIPS-AttnWav2Lip** (academic, Feb 2026). Generic audio-driven lipsync improvement. Available via lipsync.com tooling for comparison. https://arxiv.org/abs/2602.00189
5. **SadTalker / EMO / Hallo3** — older or closed; mostly superseded by the three above.

## How to set it up on Spark

### MuseTalk 1.5 (recommended default)

```bash
git clone https://github.com/TMElyralab/MuseTalk ~/musetalk
cd ~/musetalk
pip install -r requirements.txt
# Download checkpoints
huggingface-cli download TMElyralab/MuseTalk --local-dir models/musetalkV15
# Plus dependency: download whisper checkpoints for audio encoding
```

Run inference:
```bash
python -m scripts.inference \
  --inference_config configs/inference/test.yaml \
  --result_dir output/ \
  --whisper_dir models/whisper/ \
  --audio_path inputs/voicenote.wav \
  --video_path inputs/creator_idle_loop.mp4
```

Key tip: feed it a 5-10 second idle loop of the creator (already generated via Wan 2.2 Animate) instead of a single photo. Lipsync stays cleaner across longer audio.

### LatentSync (best quality, slower)

```bash
git clone https://github.com/Latentsync/LatentSync ~/latentsync
cd ~/latentsync
pip install -r requirements.txt
# Download checkpoints (~5 GB)
huggingface-cli download bytedance-research/LatentSync --local-dir checkpoints/

python -m scripts.inference \
  --unet_config_path configs/unet/second_stage.yaml \
  --inference_ckpt_path checkpoints/latentsync_unet.pt \
  --video_path inputs/creator_clip.mp4 \
  --audio_path inputs/voicenote.wav \
  --video_out_path output/synced.mp4
```

### Wan2.2-S2V-14B (cinematic full-body talking head)

ComfyUI native workflow at https://docs.comfy.org/tutorials/video/wan/wan2-2-s2v. Inputs: single reference image + audio file. Outputs: full cinematic clip with synced lipsync, head movement, body breathing.

```bash
# Already covered in lesson 04 setup; pull the workflow JSON
```

### Spark / VRAM

- MuseTalk 1.5: ~8 GB VRAM peak. Works on every Spark / 4090 / 5090.
- LatentSync: ~12-16 GB. Spark fine.
- Wan2.2-S2V-14B: 65-80 GB at 720p like other Wan 14B variants. Spark unified memory handles it; consumer GPUs need GGUF Q5 (~12 GB).

## Quality benchmarks

From the Hypereal AI Aug 2025 shootout (LatentSync vs Wav2Lip vs MuseTalk):

| Model | Lipsync acc | Visual quality | Speed | Best for |
|---|---|---|---|---|
| Wav2Lip | High | Low (mouth-only patch, blurry seams) | Fast | Quick patch on existing video |
| MuseTalk 1.5 | Very high | High (full-frame, identity preserved) | Real-time | Production short clips |
| LatentSync | Highest | Highest (cleanest face, no seams) | Slow (1x realtime) | Hero clips, long-form |
| Wan2.2-S2V-14B | Highest | Highest + body motion | Slow | Full-body cinematic talking head |

MuseTalk paper claim: "MuseTalk modifies an unseen face according to input audio, with a face region size of 256 × 256, supports multiple languages, real-time inference at 30fps+ on V100, and is positioned for high-fidelity lipsync via spatio-temporal sampling."

LatentSync paper (arXiv 2412.09262): emphasis on "end-to-end framework based on audio conditioned latent diffusion models without any intermediate motion representation" — meaning fewer artifacts than two-stage Wav2Lip pipelines.

Wan2.2-S2V-14B creator review (from deepbeepmeep/Wan2GP Issue #1266): "It's better than multytalk and infinite talk. And it can do good lipsink for singing characters."

## Common failure modes + fixes

- **Mouth shape stays static / barely moves** → audio amplitude too low or codec mismatch. Convert audio to 16kHz mono WAV before feeding in.
- **Identity drifts mid-clip** → use MuseTalk's `--identity_preservation` flag (1.5 release) or chain output through PuLID-FLUX2 frame-by-frame for rescue.
- **Visible seam around mouth** (Wav2Lip-style) → switch to LatentSync or MuseTalk 1.5; both are full-frame.
- **Tongue, teeth, inner-mouth artifacts** → MuseTalk 1.5 handles these much better than 1.0 thanks to spatio-temporal sampling. Update if you've been on 1.0.
- **Sync drifts on long clips (>30s)** → split the audio into ~10s chunks, run each through MuseTalk, concatenate with crossfade in ffmpeg.
- **Wan2.2-S2V freezes on dual-GPU** → known issue with diffusers split. Run on single GPU or single Spark.

## When to choose this over the course's recipe

- **You're producing Reels where the creator "speaks"** — entire content format the course can't make. Mandatory: pick MuseTalk for default, LatentSync for hero clips, Wan2.2-S2V for full-body cinematic.
- **You want talking-head DM previews on Fanvue** — MuseTalk + 5s creator idle loop + ElevenLabs / F5-TTS voicenote. Course doesn't get past audio-only voicenotes.
- **You want viral "creator reacts" Reels** — LatentSync + ElevenLabs voice → 15s reaction-style content with synced face.
- **Skip lipsync entirely** only if your strategy is purely photo-based (rare in 2026).

## Sources

- https://github.com/TMElyralab/MuseTalk
- https://github.com/tmelyralab/musetalk
- https://arxiv.org/html/2410.10122v3 (MuseTalk paper)
- https://huggingface.co/marcosremar2/MuseTalk
- https://www.themoonlight.io/review/musetalk-real-time-high-quality-lip-synchronization-with-latent-space-inpainting
- https://github.com/Latentsync/LatentSync
- https://arxiv.org/abs/2412.09262v1 (LatentSync paper)
- https://lipsync.com/compare/wav2lip-vs-latentsync
- https://hypereal.tech/a/latentsync-vs-wav2lip-vs-musetalk-which-lip-sync-ai-is-best
- https://huggingface.co/Wan-AI/Wan2.2-S2V-14B
- https://docs.comfy.org/tutorials/video/wan/wan2-2-s2v
- https://wan-s2v.net/
- https://github.com/deepbeepmeep/Wan2GP/issues/1266
- https://arxiv.org/abs/2602.00189 (LPIPS-AttnWav2Lip)
