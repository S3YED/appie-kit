---
name: instagram-download
description: "Download Instagram Reels and posts using browser-assisted extraction. Bypasses login requirement by extracting video URLs from the browser session's network performance entries."
version: 1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [ffmpeg, ffprobe]
metadata:
  hermes:
    tags: [instagram, social-media, download, reels]
    homepage: https://www.instagram.com
---

# Instagram Download — Browser-Assisted Extraction

Download Instagram Reels (and potentially posts) at highest quality without requiring login credentials. Instagram blocks `yt-dlp` and bare `curl` — the workaround is to load the page in the browser tool and extract video URLs from the network resource entries.

---

## When to Use

- User sends an Instagram Reel link and asks you to download it
- `yt-dlp` returns: `login required`, `rate-limit reached`, or `unable to extract shared data`
- You have browser tool access

---

## Workflow

### 1. Open the Reel in the Browser

```bash
browser_navigate(url="https://www.instagram.com/reel/REEL_ID/")
```

The page loads even without login — Instagram shows the content behind a signup prompt but the video elements and network resources are still accessible.

### 2. Extract Video URLs from Browser Network Performance Entries

```javascript
performance.getEntriesByType('resource').filter(r => r.name.includes('.mp4')).map(r => r.name)
```

This returns an array of MP4 URLs from Instagram's CDN. You'll typically see:

- **Video-only stream** — bitrate ~1 Mbps+, H.264, 720×1280 (the best quality)
- **Lower-bitrate video stream** — ~273 kbps
- **Audio-only stream** — AAC, ~12-87 kbps (look for "audio" or "vbr3_audio" in the `efg` URL parameter)

### 3. Download the Full Files

Instagram splits streams into byte-range chunks (`bytestart=N&byteend=M`). Use the **full URL without** `bytestart` and `byteend` parameters — this gives the complete file:

```bash
curl -sL -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -o reel_video.mp4 "VIDEO_URL_WITHOUT_BYTESTART_PARAMS"
curl -sL -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -o reel_audio.mp4 "AUDIO_URL_WITHOUT_BYTESTART_PARAMS"
```

### 4. Identify Which Stream Is Which

Not every URL has "audio" in its params. Use ffprobe to check:

```bash
ffprobe -v quiet -print_format json -show_streams file.mp4
```

- Video stream: `codec_type: "video"`, codec H.264, 720×1280
- Audio stream: `codec_type: "audio"`, codec AAC

### 5. Merge Audio + Video with ffmpeg

```bash
ffmpeg -i reel_video.mp4 -i reel_audio.mp4 \
  -c:v copy -c:a aac -b:a 128k \
  -map 0:v:0 -map 1:a:0 -shortest \
  -movflags +faststart reel_final.mp4 -y
```

- `-c:v copy` — copy video stream without re-encoding (lossless, fast)
- `-c:a aac -b:a 128k` — re-encode audio to a good bitrate (original is often very low ~12 kbps)
- `-map 0:v:0 -map 1:a:0` — take video from first file, audio from second
- `-movflags +faststart` — enables streaming-friendly moov atom at start
- `-y` — overwrite output

### 6. Deliver the Result

Send the file via `send_message` with `MEDIA:/path/to/reel_final.mp4`.

---

## Pitfalls

- **Don't use `yt-dlp` for Instagram** — it fails with login/rate-limit errors. The browser workaround is the reliable path.
- **Byte-range URLs are not full files** — URLs with `bytestart=N&byteend=M` params are chunks. Strip those params to get the complete file. If the base URL already includes them in a way you can't cleanly remove, download ALL byte chunks and concatenate them.
- **Audio stream may have very low bitrate** (~12 kbps). The ffmpeg command above upscales it to 128k AAC for acceptable quality.
- **Clean up temp files** — video/audio downloads and the final output are large. Delete them after sending.
- **Single video stream (no audio)** — sometimes the reel has no separate audio track. Check with ffprobe and skip the audio merge if there's no audio stream.
- **Cookie-based download** — if the user provides Instagram cookies (exported from Cookie-Editor extension as JSON), you can use them with `curl -b cookies.json` or `yt-dlp --cookies cookies.json` for a simpler download path. Ask for cookies before falling back to the browser method.

---

## References

For provider-specific details, error transcripts, and reproduction recipes, see `references/instagram-cdn-patterns.md`.