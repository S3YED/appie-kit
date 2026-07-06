---
name: scroll-hero-video
description: Build Apple-style scroll-driven video hero sections. A full-screen video scrubs frame-by-frame as the user scrolls, with text overlay fade, mobile fallback, and buttery-smooth rAF lerp.
tags:
  - scroll
  - video
  - hero
  - scrub
  - animation
---

# Scroll Hero Video

Build a scroll-driven video hero where a full-screen video scrubs in sync with scroll position — the Apple product page effect.

## When to use

- Landing page hero needs a premium, interactive feel
- You have a short video (5–10s) that tells a story (before/after, product reveal, transformation)
- Desktop-first: mobile gets autoplay loop fallback

## Requirements

- Short video (5–10s, 720p recommended)
- ffmpeg for encoding
- No JS dependencies needed (vanilla JS)

---

## Step 1: Encode the video

The video MUST have every frame as a keyframe (`-g 1`) so seeking is instant. Use Soleiman/LuxHom proven specs:

```bash
ffmpeg -i source.mp4 \
  -c:v libx264 \
  -g 1 \
  -crf 26 \
  -preset medium \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -an \
  -vf "scale=1280:720:flags=lanczos,fps=24" \
  scrub.mp4
```

**Key params:**
| Param | Why |
|---|---|
| `-g 1` | Every frame is a keyframe — enables instant seeking to any position |
| `-crf 26` | Balance quality/file size (28 = smaller/lower, 24 = larger/better) |
| `scale=1280:720` | 720p is plenty for background video — 1080p adds 3-4x weight |
| `fps=24` | Lower FPS = fewer frames to seek = smoother scrub |
| `-an` | No audio needed for scrub |
| Target: **~5-6MB** for a 7s video at 5.8 Mbps |

**Soleiman reference**: 1280x714, 24fps, 6Mbps, 6MB for 8s video.

## Step 2: HTML structure

```html
<section class="hero" id="hero">
  <div class="hero-sticky">
    <video id="heroVideo" muted playsInline preload="auto" poster="poster.jpg">
      <source src="videos/scrub.mp4" type="video/mp4">
    </video>
    <div class="hero-overlay" id="heroOverlay">
      <!-- Your hero content: pre-title, heading, tagline, CTAs -->
    </div>
    <div class="hero-scroll-hint" id="scrollHint">
      <span>Scroll voor de transformatie</span>
    </div>
  </div>
</section>
```

**Key:**
- Section height: `250vh` (scrubs over ~1.5 viewports)
- Inner div: `position: sticky; top: 0; height: 100vh` — pins video
- Video: `position: absolute; inset: 0; object-fit: cover`

## Step 3: CSS

```css
.hero { position: relative; width: 100%; height: 250vh; background: #000; }
.hero-sticky { position: sticky; top: 0; height: 100vh; overflow: hidden; will-change: transform; }
.hero video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; will-change: transform; }
.hero video.mobile-fallback { will-change: auto; }
.hero-overlay {
  position: absolute; inset: 0; z-index: 5;
  display: flex; flex-direction: column; justify-content: center;
  align-items: center; text-align: center; pointer-events: none;
  transition: opacity .15s linear;
}
.hero-scroll-hint {
  position: absolute; bottom: 2.5rem; left: 50%; transform: translateX(-50%); z-index: 10;
  display: flex; flex-direction: column; align-items: center; gap: .75rem;
  color: rgba(255,255,255,.35); font-size: .7rem; letter-spacing: .15em; text-transform: uppercase;
  transition: opacity .15s linear, visibility .15s linear;
}
```

**CSS tips:**
- `will-change: transform` on sticky + video hints GPU acceleration — the compositor knows these layers are animated
- `pointer-events: none` on overlay so clicks pass through to nav/CTAs underneath
- `.15s linear` transitions feel snappier than `1s ease` — the rAF loop updates every frame anyway, the CSS transition is just a safety net

## Step 4: JavaScript (Soleiman-exact)

```javascript
(function() {
  const video = document.getElementById('heroVideo');
  const overlay = document.getElementById('heroOverlay');
  const hint = document.getElementById('scrollHint');
  const progressBar = document.getElementById('progressBar');
  if (!video) return;

  // Mobile / reduced motion / save-data → autoplay loop
  const isMobile = window.matchMedia('(max-width: 767px)').matches;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = navigator.connection?.saveData === true;
  if (isMobile || reduceMotion || saveData) {
    video.classList.add('mobile-fallback');
    video.loop = true;
    video.play().catch(() => {});
    return;
  }

  video.loop = false; video.pause();

  // ─── BLOB PRELOAD: fetch entire video into memory ───
  const src = video.querySelector('source')?.src;
  if (src) {
    fetch(src, { cache: 'force-cache' })
      .then(r => r.blob())
      .then(blob => {
        const url = URL.createObjectURL(blob);
        video.src = url;
        const old = video.querySelector('source');
        if (old) old.remove();
        const s = document.createElement('source');
        s.src = url; s.type = 'video/mp4';
        video.appendChild(s);
        video.load();
      })
      .catch(() => {});
  }

  let duration = 7;
  const dur = () => video.duration || duration;
  video.addEventListener('loadedmetadata', () => { duration = video.duration || 7; });
  if (video.readyState >= 1) duration = video.duration || 7;

  // Safari/iOS: prime with play+pause for seeking
  let primed = false;
  const prime = () => {
    if (primed) return; primed = true;
    video.play().then(() => video.pause()).catch(() => {});
    window.removeEventListener('touchstart', prime);
  };
  window.addEventListener('touchstart', prime, { passive: true });

  const PIN = 1.5; // viewport heights to scrub through
  let cur = 0; // smoothed TIME value (Soleiman-exact)
  let raf = 0;

  const tick = () => {
    raf = requestAnimationFrame(tick);

    // Read scrollY directly in rAF — NO scroll event listener needed
    const progress = Math.min(1, Math.max(0, window.scrollY / (window.innerHeight * PIN)));
    const target = progress * dur();

    // Soleiman-exact lerp: fixed 0.12 factor, 0.004 threshold
    cur += (target - cur) * 0.12;
    if (Math.abs(target - cur) < 0.004) cur = target;

    // Seek — only when video has data
    if (video.readyState >= 2 && Number.isFinite(cur) && duration > 0) {
      const seekTime = Math.min(cur, dur() - 0.05);
      if (Math.abs(video.currentTime - seekTime) > 0.01) {
        try { video.currentTime = seekTime; } catch (e) {}
      }
    }

    // Overlay fade — Soleiman-exact: fades between 5% and 25% scroll
    const f = Math.max(0, Math.min(1, 1 - (progress - 0.05) / 0.20));
    if (overlay) overlay.style.opacity = f;

    // Scroll hint fade — gone by 8% scroll
    if (hint) {
      const h = Math.max(0, 1 - progress / 0.08);
      hint.style.opacity = h;
      hint.style.visibility = h <= 0 ? 'hidden' : 'visible';
    }

    // Progress bar
    if (progressBar) progressBar.style.width = (progress * 100) + '%';
  };

  raf = requestAnimationFrame(tick);
})();
```

### Key techniques explained

| Technique | Why |
|---|---|
| **Blob preload** (`cache: force-cache`) | Whole video in memory. Browsers may ignore `preload=auto` for large files. Blob = guaranteed instant seeking. Cache hint avoids re-download. |
| **rAF-only scroll** | Read `window.scrollY` directly in rAF. No separate scroll event listener = no layout thrashing, no dual-update bugs. |
| **Fixed 0.12 lerp on time values** | Soleiman-exact. Lerp on `currentTime` (not 0-1 progress), fixed factor. Prevents the "catching up" feel of adaptive lerps. |
| **0.004 threshold** | Snaps to exact position when close enough — prevents micro-jitter when user stops scrolling. |
| **Safari prime** | iOS/Safari won't decode frames for a video that has never played. A play()+pause() on first interaction unlocks seeking. |
| **`dur()` helper** | Readable pattern: `const dur = () => video.duration || duration` — returns live duration or cached fallback. |

## Mobile fallback

On small screens (`<768px`), prefers-reduced-motion, or save-data: the video autoplays in a loop instead of scrubbing. The text overlay stays visible. This avoids wasting bandwidth on a scroll effect that doesn't work well on touch.

## Reference implementations

| Site | Video specs | Notes |
|---|---|---|
| **Soleiman Advocatuur** (`soleiman-advocatuur.vercel.app`) | 1280x714, 24fps, 6Mbps, 6MB (8s) | Production reference. Uses blob preload + rAF-only scroll + fixed 0.12 lerp. React/framer-motion but vanilla JS equivalent works identically. |
| **LuxHom** (`luxhom-site.vercel.app`) | 1280x720, 24fps, 5.8Mbps, 4.8MB (7s) | Vanilla HTML/JS rebuild. Soleiman-exact lerp, no scroll listener, blob preload with `cache: force-cache`. |

## Pitfalls

- **Don't skip blob preload.** Without it, seeking depends on browser's buffering state. `preload=auto` is not reliable for large files.
- **Don't use a scroll event listener.** Read `window.scrollY` directly in rAF. A separate scroll handler + rAF creates dual-update bugs and unnecessary overhead.
- **Don't use canvas.** Drawing video frames to canvas with `drawImage` adds compositing overhead. Direct `<video>` with `object-fit: cover` is GPU-accelerated and smoother.
- **Don't use 1080p.** 720p looks identical at full-screen on most devices and is 3-4x smaller.
- **Don't use 30fps.** 24fps is the sweet spot — fewer frames to seek, smoother feel.
- **Don't use adaptive lerp on progress.** Soleiman-exact: lerp on `currentTime` (time value) with a fixed 0.12 factor. This feels more consistent than adaptive approaches.
- **Don't add `transform: translate(-50%, -50%)`** on the video element for centering — use `object-fit: cover` with `inset: 0`. The translate approach breaks the sticky positioning.
- **Don't forget the Safari prime.** Without it, iOS Safari shows a black/blank video until the user interacts. Only `touchstart` is needed (not scroll).
- **Don't use `1s ease` on overlay transitions.** Use `.15s linear` — the rAF loop updates every frame anyway, the CSS transition is just a safety net for missed frames.
- **Don't forget `pointer-events: none`** on the overlay div — otherwise clicks on the hero area won't reach the navigation or CTA buttons underneath.
- **Don't set `width: 100%` on sticky element when not needed.** `position: sticky` naturally fills width. Redundant `width: 100%` can cause horizontal scroll issues on some browsers.
