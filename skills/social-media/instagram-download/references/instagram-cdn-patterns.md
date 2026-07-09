# Instagram CDN URL Patterns & Session Reference

## URL Structure

Instagram Reels use `scontent-*.cdninstagram.com` CDN URLs with the following structure:

```
https://scontent-{REGION}{NUMBER}.cdninstagram.com/o1/v/t2/f2/m86/{BASE64_HASH}.mp4
  ?_nc_cat={CATEGORY_ID}
  &_nc_sid=9ca052
  &_nc_ht=scontent-{REGION}{NUMBER}.cdninstagram.com
  &_nc_ohc={HASH}
  &efg={BASE64_JSON_METADATA}
  &ccb=17-1
  &_nc_gid={SESSION_ID}
  &_nc_ss={SOME_ID}
  &_nc_zt=28
  &oh={AUTH_HASH}
  &oe={EXPIRY_TIMESTAMP}
  &bytestart={START_BYTE}
  &byteend={END_BYTE}
```

## efg Parameter Decoding

The `efg` parameter is base64-encoded JSON. Decoded example:

```json
{
  "encode_tag": "ig-xpvds.clips.igwww-C3.dash_baseline_1_v1",
  "video_id": null,
  "oil_urlgen_app_id": 936619743392459,
  "client_name": "ig",
  "xpv_asset_id": 783471260859568,
  "asset_age_days": 313,
  "vi_usecase_id": 10099,
  "duration_s": 15,
  "bitrate": 1055523,
  "urlgen_source": "www"
}
```

Key fields to identify stream type:
- **`encode_tag` containing `audio` or `vbr3_audio`** → audio-only stream
- **`encode_tag` containing `baseline_1_v1`** → highest-quality video stream
- **`encode_tag` containing `baseline_3_v1`** → lower-quality video stream
- **`bitrate`** — higher = better quality (video: ~1 Mbps+, audio: ~12-87 kbps)

## Typical Stream Set for a Reel

| Stream | Bitrate | Resolution | Codec | Duration |
|--------|---------|------------|-------|----------|
| Video (best) | ~1,055 kbps | 720×1280 | H.264 High | ~15.5s |
| Video (low) | ~274 kbps | (lower) | H.264 | ~15.5s |
| Audio | ~12-88 kbps | — | AAC HE-AAC | ~15.5s |

## Full URL Without Byte-Range (example format)

Strip `&bytestart=N&byteend=M` from the URL to get the complete file:

```
https://scontent-{REGION}{NUMBER}.cdninstagram.com/o1/v/t2/f2/m86/{HASH}.mp4
  ?_nc_cat={ID}
  &_nc_sid=9ca052
  &_nc_ht=scontent-{REGION}{NUMBER}.cdninstagram.com
  &_nc_ohc={HASH}
  &efg={BASE64}
  &ccb=17-1
  &_nc_gid={SESSION}
  &_nc_ss={ID}
  &_nc_zt=28
  &oh={AUTH}
  &oe={EXPIRY}
```

## Session Transcript (2026-07-08)

**Reel ID:** DN8lBOnjh2M  
**Poster:** gymking  
**Mentioned:** nathannuyts  
**Date:** August 29, 2025  
**Duration:** 15.47s video, 15.49s audio  
**Final output:** 2.25 MB (2250kB), 720×1280, 30fps, AAC 128k audio

### Steps Taken
1. `yt-dlp` attempted first → failed with "login required or rate-limit reached"
2. `browser_navigate` to `https://www.instagram.com/reel/DN8lBOnjh2M/` → loaded successfully with content visible
3. `browser_console` with `performance.getEntriesByType('resource').filter(r => r.name.includes('.mp4')).map(r => r.name)` → returned 12+ URL entries (byte-range chunks)
4. Identified the two distinct base URLs (video + audio) from the first entries
5. Stripped `bytestart/byteend` params, downloaded via `curl` with browser User-Agent
6. `ffprobe` confirmed: video file had H.264 video stream only (no audio), audio file had AAC HE-AAC only
7. ffmpeg merge with `-c:v copy -c:a aac -b:a 128k -movflags +faststart`
8. Final output sent via `send_message` with `MEDIA:` path

### What Worked
- Browser tool loads Instagram without any login or proxy setup
- Performance API exposes all network resources including HLS/DASH fragments
- Full URL (without byte-range params) downloads the complete file