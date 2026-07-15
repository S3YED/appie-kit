---
name: scroll-scrub-hero
title: Scroll-Scrub Video Hero
description: Build a hero section where a video scrubs frame-by-frame driven by scroll position — Apple-product-page style. Covers video encoding, rAF lerp loop, mobile fallback, and Safari/iOS priming.
bundle: user
---

# Scroll-Scrub Video Hero

Build a hero section where a video scrubs frame-by-frame driven by the user's scroll position — Apple-product-page style. The video plays forward (and rewinds) exactly as fast as you scroll.

**Trigger conditions:**
- User wants a "scroll scrub video", "scroll-driven animation", "Apple-style hero", or "sticky video hero"
- User wants a before/after transformation revealed by scrolling
- User asks to fix a "janky" or "not smooth" scroll video
- User points to a reference (Soleiman Advocatuur, Apple product pages, Apex scroll hero)

## Architecture

```
<section.hero>       ← 250vh tall (the scroll runway)
  <div.hero-sticky>  ← position: sticky; top: 0; height: 100vh (the viewport-pinned stage)
    <video>          ← positioned absolute, inset 0, object-fit: cover
    .hero-overlay    ← text/CTAs that fade out during scrub
    .scroll-hint     ← "Scroll" indicator that fades early
```

## The Core Loop (rAF + Lerp)

The critical piece — a `requestAnimationFrame` loop that smoothly interpolates between the current scroll position and `video.currentTime`. This is what makes it smooth.

```js
let duration = 0;
video.addEventListener('loadedmetadata', () => { duration = video.duration; });
if (video.readyState >= 1) duration = video.duration;

let cur = 0;
const LERP = 0.12;          // Soleiman uses 0.12, apex uses 0.14
const PIN = 1.5;            // viewport heights to scrub over

function tick() {
  requestAnimationFrame(tick);

  const p = Math.min(1, Math.max(0, window.scrollY / (window.innerHeight * PIN)));
  const target = p * duration;

  cur += (target - cur) * LERP;
  if (Math.abs(target - cur) < 0.004) cur = target;

  if (video.readyState >= 2 && Number.isFinite(cur) && duration > 0) {
    const t = Math.min(cur, duration - 0.05);
    if (Math.abs(video.currentTime - t) > 0.01) {
      video.currentTime = t;
    }
  }

  // Overlay + hint fade
  overlay.style.opacity = Math.max(0, 1 - Math.max(0, p - 0.05) / 0.2);
  hint.style.opacity = Math.max(0, 1 - p / 0.08);
}
```

## Video Preparation (CRITICAL)

Scroll scrubbing seeks to **arbitrary** positions — the video must be encoded so every frame is a keyframe:

```bash
ffmpeg -i source.mp4 -c:v libx264 -g 1 -crf 20 -pix_fmt yuv420p -movflags +faststart -an scrub.mp4
```

| Flag | Why |
|------|-----|
| `-g 1` | **Every frame is a keyframe** — enables instant seeking to any position |
| `-crf 20` | Quality (18-23 range; lower = better, 20 is good balance) |
| `-movflags +faststart` | Web-optimized (moov atom at front — faster initial load) |
| `-an` | Strip audio (not needed for scrub) |

**File size:** Expect 2-3x larger than normal video. A 7s 1080p video at `-g 1` is ~18-25MB. This is expected — every frame needs to be a seek point.

## Safari / iOS Priming

Safari won't decode video frames until a `play()` has been called. Prime on first interaction:

```js
let primed = false;
function prime() {
  if (primed) return;
  primed = true;
  video.play().then(() => video.pause()).catch(() => {});
  window.removeEventListener('touchstart', prime);
  window.removeEventListener('scroll', prime);
}
window.addEventListener('touchstart', prime, { passive: true });
window.addEventListener('scroll', prime, { passive: true });
```

## Mobile Fallback

On small screens, reduced motion, or save-data mode, fall back to autoplay loop instead of scrub:

```js
if (isMobile || reduceMotion || saveData) {
  video.loop = true;
  video.muted = true;
  video.playsInline = true;
  video.play().catch(() => {});
  return; // skip all scrub logic
}
```

Detect mobile: `window.matchMedia('(max-width: 767px)').matches`
Detect reduced motion: `window.matchMedia('(prefers-reduced-motion: reduce)').matches`
Detect save-data: `navigator.connection?.saveData === true`

## Reference Implementations

See `references/soleiman-scrub-hero.md` for the full Soleiman ScrubHero component (Next.js + framer-motion) and the LuxHom static HTML adaptation — both are verified, production-deployed implementations of this pattern.

## Pitfalls

- **Canvas is slow:** Never render video through canvas (`drawImage`) for scroll-scrub. The canvas compositing step adds CPU/GPU overhead and drops frames. Use a direct `<video>` element with `object-fit: cover`.
- **No `currentTime` in cleanup:** If the rAF loop uses `video.currentTime` and the component unmounts, cancel the rAF. Leaving it running leaks resources.
- **Scroll event vs rAF:** Setting `video.currentTime` directly inside a `scroll` event listener causes jank because scroll events fire at variable rates and don't sync to display refresh. Always use rAF with lerp.
- **Duration = 0 on slow loads:** The first `requestAnimationFrame` may fire before `loadedmetadata`. Check `duration > 0` in the loop or pause the rAF until metadata loads.
- **Seeking past end:** Some browsers throw if `currentTime > duration - small_delta`. Always clamp to `Math.min(cur, duration - 0.05)`.
- **React re-renders:** Never use React state for values that change every rAF tick. Use refs and direct DOM manipulation — React reconciliation kills frame rate.

## Verification

- Video scrubs forward when scrolling down, backward when scrolling up
- No visible keyframe-snapping — movement should be continuous
- Text fades out cleanly during first ~20% of scrub
- Works on mobile: shows autoplay loop, not frozen frame
- Works on Safari (test iOS specifically — Safari's seeking has unique quirks)
- Loading from cache is instant (21MB @ 7s = ~210 frames, all keyframes)===ME:scroll-scrub-hero