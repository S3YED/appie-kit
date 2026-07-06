# Session Reference: LuxHom Scroll Scrub Hero

## Source Videos

| Property | Original | Encoded for Scrub |
|----------|----------|-------------------|
| Resolution | 1920x1080 | 1280x720 |
| Framerate | 30fps | 24fps |
| Bitrate | ~8 Mbps | ~6 Mbps |
| Size | 7.1 MB | 4.8 MB |
| Keyframes | default (~250) | every frame (`-g 1`) |

## Soleiman Reference (soleiman-advocatuur.vercel.app)

| Property | Value |
|----------|-------|
| Video | lady-justice-scrub.mp4 |
| Resolution | 1280x714 |
| Framerate | 24fps |
| Bitrate | 6 Mbps |
| Size | 6 MB |
| Duration | 8.04s |
| Mode | Fast scrub (150vh) + overlay fade |

## Encoding Commands Used

```bash
# Initial attempt (too large — 21MB)
ffmpeg -i input.mp4 -c:v libx264 -g 1 -crf 20 -pix_fmt yuv420p -movflags +faststart -an scrub.mp4

# Final (Soleiman-matching — 4.8MB)
ffmpeg -i input.mp4 \
  -c:v libx264 -g 1 -crf 26 -preset medium \
  -pix_fmt yuv420p -movflags +faststart -an \
  -vf "scale=1280:720:flags=lanczos,fps=24" \
  scrub.mp4
```

## Key Lesson: Two Modes of Scroll Scrub

The user wanted **Mode B** (chronological) but I initially built **Mode A** (Soleiman-style). This caused:
- Video completed scrubbing in 150vh instead of 240vh
- Overlay faded out, looking like an "end screen"
- The transformation effect was lost because the video finished too early

Always ask: "Do you want the video to scrub through the full section, or complete quickly and fade to content below?"