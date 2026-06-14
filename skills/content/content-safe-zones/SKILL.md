---
name: content-safe-zones
description: "Place text, captions, CTAs, and overlays safely for Instagram Reels, TikTok, and YouTube Shorts vertical-video layouts."
version: 1.0.0
category: content
---

# Content Safe Zones — Instagram Reels, TikTok, YouTube Shorts

Reference guide for placing text, captions, CTAs, and overlays on 9:16 vertical video (1080x1920).

## Platform-Specific Safe Zones

### Instagram Reels (1080x1920)
```
┌─────────────────────────┐ 0px
│  ❌ Status bar / time    │
├─────────────────────────┤ ~100px
│  ⚠️ Username / follow    │
├─────────────────────────┤ ~200px
│                         │
│                         │
│  ✅ SAFE ZONE            │ 200–1250px
│  Best for captions,     │
│  titles, key visuals    │
│                         │
│  🎯 SWEET SPOT:          │ 670–1250px
│  (center-lower frame)   │
│                         │
├─────────────────────────┤ ~1250px
│  ⚠️ Caption preview area │ 1250–1520px
├─────────────────────────┤ ~1520px
│  ❌ Like/Comment/Share   │ 1520–1700px
│  ❌ Music + description  │ 1700–1920px
└─────────────────────────┘ 1920px

Right edge (980–1080px): ❌ Action buttons (heart, comment, share, remix)
Left 0-100px: ⚠️ May overlap with username on some devices
```

### TikTok (1080x1920)
```
┌─────────────────────────┐ 0px
│  ❌ Status bar            │
├─────────────────────────┤ ~120px
│  ⚠️ "Following/For You"  │
├─────────────────────────┤ ~200px
│                         │
│  ✅ SAFE ZONE            │ 200–1200px
│                         │
│  🎯 SWEET SPOT:          │ 640–1200px
│                         │
├─────────────────────────┤ ~1200px
│  ⚠️ Username + caption   │ 1200–1500px
├─────────────────────────┤ ~1500px
│  ❌ Like/Comment/Share   │ 1500–1700px
│  ❌ Music ticker          │ 1700–1920px
└─────────────────────────┘ 1920px

Right edge (960–1080px): ❌ Action buttons (slightly wider than IG)
```

### YouTube Shorts (1080x1920)
```
┌─────────────────────────┐ 0px
│  ❌ Status bar            │
├─────────────────────────┤ ~100px
│  ⚠️ Channel name         │
├─────────────────────────┤ ~180px
│                         │
│  ✅ SAFE ZONE            │ 180–1300px
│                         │
│  🎯 SWEET SPOT:          │ 650–1300px
│                         │
├─────────────────────────┤ ~1300px
│  ⚠️ Title / description  │ 1300–1550px
├─────────────────────────┤ ~1550px
│  ❌ Like/Dislike/Comment │ 1550–1750px
│  ❌ Subscribe button      │ 1750–1920px
└─────────────────────────┘ 1920px

Right edge (970–1080px): ❌ Action buttons
```

## Universal Safe Zone (works on ALL platforms)

**For maximum cross-platform compatibility, use:**

| Zone | Y range (px) | Y range (%) | Use for |
|------|-------------|-------------|---------|
| **Caption zone** | 670–1200px | 35–62% | Captions, subtitles |
| **Title zone** | 300–600px | 16–31% | Headlines, hooks |
| **CTA zone** | 1000–1200px | 52–62% | Call to action text |
| **Full safe** | 200–1200px | 10–62% | Any text/overlay |

**Horizontal margins:** Keep text within x=100–980px (leave 100px on each side)

## Caption Best Practices

- **Font size:** 42–56px for body captions, 60–72px for headlines
- **Max width:** ~880px (100px margin each side)
- **Line height:** 1.3–1.5x font size
- **Max lines visible:** 2–3 lines at a time
- **Background:** Semi-transparent dark box OR text shadow/outline
- **Shadow recommended:** `shadowcolor=black@0.7:shadowx=3:shadowy=3` (ffmpeg)
- **Animation:** Word-by-word or sentence pop preferred over static

## FFmpeg Reference

```bash
# Caption in sweet spot (y=62% = 1190px)
drawtext=fontfile=FONT:text='Your text':fontcolor=white:fontsize=48:\
x=(w-text_w)/2:y=h*0.62:shadowcolor=black@0.7:shadowx=3:shadowy=3

# With background box
drawtext=fontfile=FONT:text='Your text':fontcolor=white:fontsize=48:\
x=(w-text_w)/2:y=h*0.62:box=1:boxcolor=black@0.5:boxborderw=12
```

## Platform Comparison Summary

| Feature | IG Reels | TikTok | YT Shorts |
|---------|----------|--------|-----------|
| Bottom dead zone | 1520px+ | 1500px+ | 1550px+ |
| Right dead zone | 980px+ | 960px+ | 970px+ |
| Top dead zone | 0–200px | 0–200px | 0–180px |
| Safe text area | 200–1250px | 200–1200px | 180–1300px |
| Sweet spot | 670–1250px | 640–1200px | 650–1300px |
| Universal sweet | **670–1200px** | **670–1200px** | **670–1200px** |
