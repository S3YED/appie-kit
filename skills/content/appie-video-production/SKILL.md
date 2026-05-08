# SKILL.md - Appie Video & Audio Production

**Owner:** All Appies (1/2/3)
**Created:** 2026-03-31
**Purpose:** Complete reference for producing Appie character videos, voiceovers, audio design, image generation, and content delivery. Includes every tool, API, preference, mistake, and lesson learned.

---

## 1. Character Design (LOCKED)

**Full spec:** `/root/clawd/projects/appie-character/CHARACTER-LOCK.md`

### Quick Reference
- **Name:** Appie
- **Style:** 3D Pixar/high-end mobile game quality
- **Skin:** Warm brown (olive-tan)
- **Beard:** BLACK (NOT grey, NOT silver, NOT white) — LOCKED
- **Outfit:** Dark teal robes + wizard hat (tilted), gold circuit-line accents
- **Palette:** Teal #0D4F4F, Gold #D4A843, Skin #8B6914
- **Energy:** Confident but kind. Genie/wizard who already knows the answer.
- **Reference image:** `/root/clawd/tmp/appie-nb-pro-c2.png`

### ⚠️ DO NOT CHANGE without Seyed's approval:
- Beard color (BLACK)
- Skin tone (warm brown)
- Teal + gold palette
- 3D animated style
- Confident but kind energy

---

## 2. Image Generation

### Primary: Gemini 3 Pro Image (BEST quality)
```bash
NANO_BANANA_API_KEY=$(grep '^NANO_BANANA_API_KEY=' /root/clawd/.env.secrets | cut -d= -f2)

curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=${NANO_BANANA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "YOUR PROMPT HERE"}]}],
    "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
  }'
```
- **Response:** `candidates[0].content.parts[].inlineData.data` (base64)
- **Use for:** Character design, hero visuals, key frames, any quality-critical image
- **Key name in .env.secrets:** `NANO_BANANA_API_KEY`

### Secondary: Gemini 2.5 Flash Image (fast, decent quality)
- Same API key, model: `gemini-2.5-flash-image`
- Use for: Quick iterations, drafts, non-hero images

### Alternative: fal.ai (Flux, Recraft, Ideogram)
```bash
FAL_KEY=$(grep '^FAL_KEY=' /root/clawd/.env.secrets | cut -d= -f2)
```
- Flux Dev: mediocre for characters
- Flux Pro: better, use for bulk parallel generation
- Use for: Scene backgrounds, non-character elements, parallel queue jobs

### 🔴 Image Generation Lessons
1. **Gemini 3 Pro Image is king** for Appie character consistency. Other models drift.
2. **Always include the FULL character description** in every prompt (beard=BLACK, skin=warm brown, teal robes, gold circuits). Models forget between generations.
3. **9:16 vertical composition needs EXPLICIT instructions:** "strict 9:16 vertical portrait, subject fills 50-70% of frame height, stack elements vertically, no wide shots, tight framing waist-up or chest-up"
4. **Style consistency across scenes:** Include a unified style block in every prompt. See `regen-frames-v4.js` for the exact STYLE + PROTAG + WIZARD blocks.
5. **Iteration is normal:** Expect 3-5 versions per key frame before it's right. v1 → v2 → v3 → v4 was our actual journey.

---

## 3. Video Generation (Scene Animation)

### Primary: Kling 2.1 Pro via fal.ai
```bash
FAL_KEY=$(grep '^FAL_KEY=' /root/clawd/.env.secrets | cut -d= -f2)

# Submit (returns request_id for polling)
curl -s -X POST "https://queue.fal.run/fal-ai/kling-video/v2.1/pro/image-to-video" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "ANIMATION PROMPT",
    "image_url": "DATA_URL_OR_HTTP_URL",
    "duration": "5",
    "aspect_ratio": "9:16"
  }'

# Poll status
curl -s "https://queue.fal.run/fal-ai/kling-video/v2.1/pro/image-to-video/requests/${REQUEST_ID}/status" \
  -H "Authorization: Key $FAL_KEY"

# Fetch result when COMPLETED
curl -s "https://queue.fal.run/fal-ai/kling-video/v2.1/pro/image-to-video/requests/${REQUEST_ID}" \
  -H "Authorization: Key $FAL_KEY"
# Video URL: .video.url
```

- **Cost:** ~$0.07/second
- **Duration:** 5 seconds per scene
- **Queue time:** 2-5 minutes per scene
- **Aspect ratios:** `9:16`, `16:9`, `1:1`

### Alternative Video Models
- **MiniMax Hailuo Video 01 Live** — good motion, cheaper
- **Wan Pro** — $0.16/video, 5 clips at a time (budget option)

### 🔴 Video Generation Lessons
1. **Image-to-video needs the STARTING FRAME to be perfect.** Bad frame in = bad video out. Invest time in key frames first.
2. **Normalize ALL scene outputs** before stitching: `ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1" -r 24 -c:v libx264 output.mp4`
3. **5 seconds per scene is the sweet spot.** Shorter feels rushed, longer and motion degrades.
4. **Animation prompts should describe MOTION, not just appearance.** "Slow push-in", "camera drifts forward", "hand raises deliberately" — be specific about movement.
5. **v4 frames >> v1 frames.** The vertical composition instructions made a huge difference. Always include explicit 9:16 framing rules in prompts.
6. **Kling can return inconsistent resolutions.** ALWAYS normalize before stitching.

### Full Pipeline Script
**Location:** `/root/clawd/projects/appie-character/launch-video/full-pipeline-v4.js`
- Handles: frame generation, video rendering, normalization, stitching, text overlays
- Run: `node full-pipeline-v4.js`

### Scene Generation Script (individual scenes)
**Location:** `/root/clawd/projects/appie-character/launch-video/generate-scene.sh`
- Run: `./generate-scene.sh <1-6>`

---

## 4. Video Stitching & Compositing

### FFmpeg Crossfade Stitch (6 scenes, 5s each)
```bash
ffmpeg -y \
  -i scene1.mp4 -i scene2.mp4 -i scene3.mp4 -i scene4.mp4 -i scene5.mp4 -i scene6.mp4 \
  -filter_complex "
    [0:v][1:v]xfade=transition=fadeblack:duration=0.5:offset=4.5[v01];
    [v01][2:v]xfade=transition=fadeblack:duration=0.5:offset=9.0[v012];
    [v012][3:v]xfade=transition=fadeblack:duration=0.5:offset=13.5[v0123];
    [v0123][4:v]xfade=transition=fadeblack:duration=0.5:offset=18.0[v01234];
    [v01234][5:v]xfade=transition=fadeblack:duration=0.5:offset=22.5[vfinal]
  " \
  -map "[vfinal]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart -an stitched.mp4
```
- **Duration:** ~27.5s (6x5s minus 5x0.5s overlaps)
- **Transition:** `fadeblack` with 0.5s duration
- **Quality:** CRF 18 (high quality), preset slow

### Text Overlays
```bash
ffmpeg -y -i stitched.mp4 -vf "
  drawtext=fontfile=/root/.local/share/fonts/Hauora-Bold.otf:text='Your business runs.':fontcolor=white:fontsize=52:x=(w-text_w)/2:y=h*0.82:enable='between(t,19.0,21.5)',
  drawtext=fontfile=/root/.local/share/fonts/Hauora-Bold.otf:text='Your turn.':fontcolor=white:fontsize=68:x=(w-text_w)/2:y=h*0.76:enable='between(t,25.5,27.5)'
" -c:v libx264 -preset slow -crf 18 final.mp4
```

### Available Fonts
- `/root/.local/share/fonts/Hauora-Bold.otf` — Primary (headings, overlays)
- `/root/.local/share/fonts/Hauora-Medium.otf` — Secondary (subtitles)
- `/root/.local/share/fonts/Hauora-Regular.otf`
- `/root/.local/share/fonts/Hauora-Light.ttf`
- `/root/.local/share/fonts/CostaStd-Bold.otf`
- `/root/.local/share/fonts/CostaStd-Regular.otf`

### HQ Export (for sending via Telegram as document)
```bash
ffmpeg -y -i final.mp4 -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart final-hq.mp4
```

### 🔴 Stitching Lessons
1. **Normalize ALL inputs first.** Different scenes from Kling can have different framerates/resolutions. Normalize to 1080x1920 @ 24fps before stitching.
2. **CRF 18 is the quality sweet spot.** Lower = bigger file, minimal visual gain. Higher = visible compression.
3. **Always add `-movflags +faststart`** — enables streaming playback and Telegram previews.
4. **`-an` flag** to strip audio from video-only exports (add audio separately for cleaner workflow).
5. **Text overlay timing needs manual tuning.** Use `enable='between(t,START,END)'` and `alpha` expressions for fade in/out.

---

## 5. Voiceover (ElevenLabs TTS)

### API
```bash
ELEVEN_KEY=$(grep '^ELEVENLABS_API_KEY=' /root/clawd/.env.secrets | cut -d= -f2)

curl -s "https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}" \
  -H "xi-api-key: ${ELEVEN_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text here",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.65,
      "similarity_boost": 0.75,
      "style": 0.4,
      "use_speaker_boost": true
    }
  }' -o output.mp3
```

### Tested Voices (for Appie narrator)

| Voice | ID | Style | Notes |
|-------|----|-------|-------|
| **Charlie** | `IKne3meq5aSn9XLyUdCD` | Deep, Confident, Energetic | Good wizard energy. Latest pick. |
| **George** | `JBFqnCBsd6RMkjVDRZzb` | Warm, Captivating Storyteller | Tested multiple times. Good but softer. |
| Adam | (OpenAI TTS, not ElevenLabs) | Clean, neutral | Mixed into vo-adam-mixed.mp3 |
| Bill | (OpenAI TTS) | Warm, older | Mixed into vo-bill-mixed.mp3 |
| Brian | (OpenAI TTS) | Professional | Mixed into vo-brian-mixed.mp3 |

### Voice Settings Guide
- **stability:** 0.60-0.75 (lower = more expressive, higher = more consistent)
- **similarity_boost:** 0.75-0.85
- **style:** 0.3-0.6 (lower = more neutral, higher = more dramatic)
- **use_speaker_boost:** always true

### Seyed's Preference (TBD)
- Sent Charlie and George versions for comparison
- Waiting for final voice pick
- Script v2 preferred: lead with pain, proof over story

### 🔴 Voice Lessons
1. **Generate each VO line SEPARATELY** for precise scene-sync timing. Don't generate one big block.
2. **Line duration varies wildly.** A 5-word line can be 0.8s or 2.5s depending on pacing. Always check with `ffprobe`.
3. **"eleven_multilingual_v2"** is the best model for English narration. Don't use v1.
4. **Style parameter matters:** 0.3 for "Your turn." (calm, authoritative), 0.5 for dramatic lines.

---

## 6. Audio Design & Mixing

### Music/Score
- **Existing score:** `/root/clawd/projects/appie-character/launch-video/score-cinematic-v1.mp3` (30s, cinematic)
- **Style:** Epic cinematic buildup, quiet tension to triumphant release

### Mixing VO Lines Over Score (Precise Timing)
```bash
ffmpeg -y \
  -i line1.mp3 -i line2.mp3 -i line3.mp3 -i line4.mp3 -i line5.mp3 -i line6.mp3 \
  -i score-cinematic-v1.mp3 \
  -filter_complex "
    [0]adelay=500|500,volume=1.8[v1];
    [1]adelay=5500|5500,volume=1.8[v2];
    [2]adelay=10000|10000,volume=1.8[v3];
    [3]adelay=14500|14500,volume=1.8[v4];
    [4]adelay=19000|19000,volume=1.8[v5];
    [5]adelay=25000|25000,volume=1.8[v6];
    [6]volume=0.35[music];
    [v1][v2][v3][v4][v5][v6][music]amix=inputs=7:duration=longest:dropout_transition=2[out]
  " \
  -map "[out]" -ac 2 -ar 44100 -b:a 192k mixed.mp3
```

### Muxing Audio onto Video
```bash
ffmpeg -y \
  -i final-hq.mp4 \
  -i mixed.mp3 \
  -t 27.75 \
  -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  final-with-audio.mp4
```

### Scene Timing Map (6 scenes, ~4.6s each after crossfade)
| Scene | Time | VO Delay (ms) | Line |
|-------|------|---------------|------|
| 1 - Grind | 0:00-0:04.5 | 500 | "Three AM... Another night buried in emails." |
| 2 - Spark | 0:04.5-0:09.0 | 5500 | "Until one night... something woke up." |
| 3 - Summoning | 0:09.0-0:13.5 | 10000 | "Meet Appie... Your AI employee." |
| 4 - Cleanup | 0:13.5-0:18.0 | 14500 | "Emails. Calendar. Proposals. Handled." |
| 5 - Freedom | 0:18.0-0:22.5 | 19000 | "You built your business for freedom." |
| 6 - Invite | 0:22.5-0:27.75 | 25000 | "Your turn." |

### 🔴 Audio Lessons
1. **VO volume at 1.8x, music at 0.35x** — voice must sit clearly above music. Adjust if voice is quiet.
2. **`adelay` values are in milliseconds** and need BOTH channels specified (e.g., `adelay=5500|5500`).
3. **`amix` with `dropout_transition=2`** prevents volume drops when streams end.
4. **`-shortest` flag** when muxing to prevent audio running past video end.
5. **AAC at 192k** is the sweet spot for quality vs file size on mobile.
6. **Always trim audio to exact video duration** with `-t` flag.

---

## 7. Delivery via Telegram

### Send as Document (preserves quality)
```bash
BOT_TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' /root/clawd/.env.secrets | cut -d= -f2)
CHAT_ID="1817919454"  # Seyed

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendDocument" \
  -F "chat_id=${CHAT_ID}" \
  -F "document=@/path/to/video.mp4" \
  -F "caption=Description here"
```

### Send as Video (compressed, in-chat preview)
```bash
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendVideo" \
  -F "chat_id=${CHAT_ID}" \
  -F "video=@/path/to/video.mp4" \
  -F "caption=Description" \
  -F "width=1080" -F "height=1920"
```

### Send Photo
```bash
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto" \
  -F "chat_id=${CHAT_ID}" \
  -F "photo=@/path/to/image.png" \
  -F "caption=Description"
```

### 🔴 Telegram Delivery Lessons
1. **ALWAYS send final videos as DOCUMENT, not video.** Telegram's video player compresses and can display 9:16 vertical as square/distorted. Document preserves the original file.
2. **Send BOTH:** Document (for quality) + Video (for quick preview) if wanted.
3. **For review/comparison:** Send individual scenes as videos (quick preview OK), final as document.
4. **Max file size:** 50MB for bots. Our finals are ~26MB, well within limit.
5. **Include width/height** when sending as video to help Telegram display correctly.
6. **Captions** have a 1024 char limit.

---

## 8. Whisper Transcription (Voice Messages)

### For transcribing Seyed's voice feedback:
```bash
/root/clawd/tmp/faster-whisper/transcribe.sh /path/to/audio.ogg
```
- **Model:** large-v3 (default, best accuracy)
- **Fast mode:** `--model base` (for quick transcription when accuracy isn't critical)
- **Input:** .ogg, .mp3, .wav, .m4a
- **⚠️ large-v3 can take 30-60s to load on first run.** Use `base` model for speed when iterating.

---

## 9. Script Templates

### Launch Video Script (Current)
**Location:** `/root/clawd/projects/appie-character/launch-video/PRODUCTION-BIBLE.md`

### Talking Head Scripts
- **v1:** `/root/clawd/projects/appie-character/talking-head-script-v1.md` (story-driven, "I'm not real" hook)
- **v2:** `/root/clawd/projects/appie-character/talking-head-script-v2.md` (pain-driven, proof-first — PREFERRED)

### Seyed's Script Preferences
1. **Lead with the pain point**, not the identity reveal
2. **Acknowledge AI openly** ("Obviously I'm not real") but as a throwaway, not the feature
3. **Proof over story:** Real numbers, real clients, real results
4. **Case studies:** Dubai Property, Seyed's own transformation (14hr days → gym mornings)
5. **CTA:** "Comment 'Minion'" (playful, on-brand wizard/minion dynamic)
6. **Tone:** No hype-bro energy. Warm, confident, direct. Like a knowledgeable friend.
7. **No corporate fluff.** Authentic, direct voice.

---

## 10. File Map

### Project Root
```
/root/clawd/projects/appie-character/
├── CHARACTER-LOCK.md          # Locked character spec (DO NOT MODIFY)
├── talking-head-script-v1.md  # Script v1 (story hook)
├── talking-head-script-v2.md  # Script v2 (pain hook — PREFERRED)
└── launch-video/
    ├── PRODUCTION-BIBLE.md    # Full storyboard + specs
    ├── full-pipeline-v4.js    # Complete render pipeline (Node.js)
    ├── generate-scene.sh      # Individual scene generator
    ├── regen-frames-v4.js     # Key frame regenerator with unified style
    ├── score-cinematic-v1.mp3 # Background music (30s)
    ├── vo-lines/              # Individual VO lines (Charlie voice)
    │   ├── line1.mp3 ... line6.mp3
    ├── vo-lines-george/       # Individual VO lines (George voice)
    ├── vo-scored-charlie-v1.mp3  # Mixed VO + score (Charlie)
    ├── vo-scored-george-v1.mp3   # Mixed VO + score (George)
    ├── 9x16-v4/               # Latest key frames (v4)
    ├── videos-v4/             # Latest rendered scenes + finals
    │   ├── scene1-6.mp4       # Individual scenes
    │   ├── final-hq.mp4       # Stitched video (no audio)
    │   ├── final-with-audio.mp4       # Charlie VO + score
    │   └── final-with-audio-george.mp4 # George VO + score
    └── renders/               # Legacy renders
```

### Assets
```
/root/clawd/assets/
├── seyed-photos/              # Seyed's actual photos (for thumbnails/content)
│   └── seyed-closeup-resized.jpg  # Best for close-ups
└── thumbnail-templates/       # HTML templates for YouTube thumbnails
```

### Reference Images
- Approved character: `/root/clawd/tmp/appie-nb-pro-c2.png`

---

## 11. API Keys Summary

| Service | Key Name in .env.secrets | Used For |
|---------|--------------------------|----------|
| Gemini (image gen) | `NANO_BANANA_API_KEY` | Character images, key frames |
| fal.ai (video gen) | `FAL_KEY` | Kling video, Flux images |
| ElevenLabs (TTS) | `ELEVENLABS_API_KEY` | Voiceovers |
| Telegram Bot | `TELEGRAM_BOT_TOKEN` | Sending files to Seyed |

---

## 12. Complete Production Workflow (Checklist)

### Phase 1: Key Frames
- [ ] Write scene descriptions in PRODUCTION-BIBLE.md
- [ ] Generate key frames with Gemini 3 Pro Image
- [ ] Include FULL character spec + vertical composition rules in every prompt
- [ ] Review, iterate (expect 3-5 versions per frame)
- [ ] Get Seyed's approval on all frames

### Phase 2: Animation
- [ ] Render each scene via Kling 2.1 Pro (fal.ai)
- [ ] Write animation prompts describing MOTION specifically
- [ ] Normalize all outputs to 1080x1920 @ 24fps
- [ ] Review each scene individually

### Phase 3: Stitch & Overlay
- [ ] Stitch with crossfade transitions (0.5s)
- [ ] Add text overlays with precise timing
- [ ] Export HQ version (CRF 16-18)

### Phase 4: Audio
- [ ] Write VO script (short punchy lines, one per scene)
- [ ] Generate each line separately via ElevenLabs
- [ ] Check each line's duration with ffprobe
- [ ] Mix VO lines at precise timestamps over score
- [ ] Set VO volume ~1.8x, music ~0.35x
- [ ] Mux audio onto video

### Phase 5: Delivery
- [ ] Send as Telegram DOCUMENT (not video!) for quality
- [ ] Send comparison versions if testing voices/edits
- [ ] Wait for Seyed's feedback before finalizing

---

## 13. Known Issues & Gotchas

1. **Telegram squishes 9:16 video** — always send as document for review
2. **Kling returns inconsistent resolutions** — always normalize before stitching
3. **Whisper large-v3 is slow to cold-start** — use `base` for quick transcription
4. **Gemini 3 Pro sometimes generates grey/silver beards** — always specify "BLACK beard, NOT grey"
5. **fal.ai queue can back up** — during peak times, expect 5-10 min per scene instead of 2-5
6. **ffmpeg `amix` reduces volume** when streams overlap — use `volume` filter to compensate
7. **GitHub tokens on both Appie-2 and Appie-3 are EXPIRED** — need new PAT from Seyed
8. **Text overlay escaping in ffmpeg** — backslash-escape commas and colons in drawtext
9. **`-shortest` flag is essential** when muxing — prevents audio overrun
10. **CTA text changed:** Was "Comment AI Magic" → now "Comment MINION" (per script v2)
