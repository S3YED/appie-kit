# Case Study: AI Content Pipeline

## The Problem

Creating one Instagram Reel used to take 4+ hours:
1. Script writing (30 min)
2. Video recording or stock footage (1-2 hours)
3. Editing in Premiere/CapCut (1 hour)
4. Voiceover recording (30 min)
5. Thumbnail + captions (30 min)
6. Upload + scheduling (15 min)

**At 3 reels/week:** 12+ hours of content work.

## The AI Pipeline

### Video Generation: fal.ai + Kling 3.0 Pro

**Why Kling 3.0 Pro:**
- $3-4 per 10-second clip (vs $6-7 for Veo 3)
- Element Binding = character consistency across scenes
- 4K native resolution
- Image-to-video (your reference image → animated video)

**Process:**
1. Generate character reference image (Flux Dev, $0.03)
2. Write scene prompt with character description
3. Submit to Kling 3.0 Pro via fal.ai API
4. Receive 1440x1440 10-second clip in 3-4 minutes

### Voice: ElevenLabs

**Selected voice:** Liam (TX3LPaxmHKxFdv7VOQHJ)
- Persona: Energetic Social Media Creator
- Natural, not robotic
- Consistent across all content

**Process:**
1. Write script (or let Appie write it)
2. Submit to ElevenLabs v3 Creative API
3. Receive natural voiceover in seconds

### Assembly: FFmpeg

Appie combines everything:
```bash
# Merge video + voiceover + background music
ffmpeg -i scene.mp4 -i voice.mp3 -i music.mp3 \
  -filter_complex "[1:a][2:a]amerge=inputs=2[a]" \
  -map 0:v -map "[a]" -shortest output.mp4
```

### Scheduling: n8n + Buffer

- n8n workflow triggers content generation
- Buffer handles multi-platform scheduling
- Google Sheets as content calendar

## Cost Comparison

| Component | Per Reel | Monthly (12 reels) |
|-----------|----------|-------------------|
| Kling 3.0 Pro (3 scenes) | $9-12 | $108-144 |
| ElevenLabs voice | ~$2 | ~$22/mo flat |
| fal.ai images | $0.09 | ~$1 |
| n8n (self-hosted) | $0 | $0 |
| **Total** | **~$12/reel** | **~$150/mo** |

**Compare:** Freelance video editor: $200-500/reel. Agency: $500-2,000/reel.

## Model Comparison (2026)

| Model | Quality | Cost/10s | Character Lock | Best For |
|-------|---------|----------|---|---|
| **Kling 3.0 Pro** | Professional | $3-4 | Element Binding | Mascot content |
| Veo 3 | Cinematic | $6-7 | Workarounds | One-shot cinematic |
| Sora 2 Pro | Photorealistic | Expensive | Limited | Realistic scenarios |
| Wan 2.2 5B | Low quality | $0.06 | No | Prototyping only |

## Key Learnings

1. **Character consistency is everything** for brand content. Kling's Element Binding is a game-changer.
2. **Voice selection matters more than you think.** Test 5+ voices before committing.
3. **Batch generation saves money.** Generate all scenes for a month in one session.
4. **Keep a reference image library.** Same character, same outfit, different poses.
5. **Native audio from video models is bad.** Always replace with ElevenLabs.
