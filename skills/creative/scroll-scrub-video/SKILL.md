---
name: scroll-scrub-video
description: Build scroll-driven video hero sections where a video scrubs frame-by-frame as the user scrolls. Covers video encoding, blob preloading, rAF-driven playback, mobile fallback, and the two common modes (fast Soleiman-style vs. full-section chronological).
trigger:
  - 'User asks for a scroll-scrubbing video hero, Apple-style product page animation, or scroll-driven video section.'
  - 'User reports a scrub video is choppy, janky, or playing at the wrong speed.'
  - 'Task involves encoding a video for frame-accurate seeking (keyframe=1).'
  - 'User asks to match the scrub behavior of an existing site (e.g., soleiman-advocatuur.vercel.app).'
---

# Scroll Scrub Video Hero

Build a scroll-driven video section where `video.currentTime` is driven by the user's scroll position. This is the technique Apple uses on product pages and is used on [soleiman-advocatuur.vercel.app](https://soleiman-advocatuur.vercel.app/).

## Two Modes (critical to get right)

### Mode A: Fast scrub with overlay fade (Soleiman-style)
- Video finishes scrubbing after **1.5 viewport heights** of scroll
- Content overlay/text fades out (5–25% scroll)
- Remaining scroll in the hero section shows the last video frame
- Used for: storytelling where the video is a backdrop that transitions to content below
- **Hero height**: 250vh | **Scrub distance**: 150vh | **Fade**: yes

### Mode B: Chronological full-section scrub
- Video scrubs from start to end across the **entire hero section** (e.g., 240vh)
- Content overlay stays visible throughout
- When the user finishes scrolling the hero, the video is at the final frame
- Used for: product transformations, "before → after" reveals, where the video IS the content
- **Hero height**: 340vh | **Scrub distance**: 240vh | **Fade**: no

Always confirm with the user which mode they want before building. Default to Mode B for transformation/reveal content.

## Video Encoding

The video MUST be encoded with every frame as a keyframe (`-g 1`) for instant seeking. Standard video files have keyframes every ~250 frames, causing visible stutter when scrubbing.

```bash
# Production scrub video — 720p, 24fps, every frame a keyframe
ffmpeg -i source.mp4 \
  -c:v libx264 -g 1 -crf 26 -preset medium \
  -pix_fmt yuv420p -movflags +faststart -an \
  -vf "scale=1280:720:flags=lanczos,fps=24" \
  scrub.mp4
```

**Video spec (proven):**
- Resolution: 1280x720
- Framerate: 24fps
- Codec: H.264, `-g 1` (every frame keyframe)
- Bitrate: ~6 Mbps
- File size: ~5 MB for 7 seconds
- No audio (`-an`)

**Why these specs:** The Soleiman reference video (lady-justice-scrub.mp4) is 1280x714 @ 24fps, 6MB. Higher resolution or FPS increases file size without visible benefit (the video is a background element). 24fps = fewer frames to seek through = smoother scrub.

## Implementation

### HTML Structure
```html
<section class="hero" style="height: 340vh">
  <div class="hero-sticky" style="position: sticky; top: 0; height: 100vh; overflow: hidden">
    <video id="heroVideo" muted playsInline preload="auto" poster="poster.jpg">
      <source src="videos/scrub.mp4" type="video/mp4">
    </video>
    <div class="hero-overlay">
      <!-- overlay content stays visible or fades per mode -->
    </div>
  </div>
</section>
```

### CSS
```css
.hero { position: relative; width: 100%; height: 340vh; background: #000; }
.hero-sticky { position: sticky; top: 0; height: 100vh; overflow: hidden; will-change: transform; }
.hero video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; will-change: transform; }
.hero video.mobile-fallback { will-change: auto; }
```

### JavaScript (rAF-only, no scroll event listener)

```javascript
(function() {
  const video = document.getElementById('heroVideo');
  const hint = document.getElementById('heroHint');
  const progressBar = document.getElementById('progressBar');
  if (!video) return;

  // Detect constraints
  const isMobile = window.matchMedia('(max-width: 767px)').matches;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = navigator.connection?.saveData === true;

  // Mobile fallback: autoplay loop
  if (isMobile || reduceMotion || saveData) {
    video.classList.add('mobile-fallback');
    video.loop = true;
    video.play().catch(() => {});
    return;
  }

  video.loop = false;
  video.pause();

  // Blob preload: fetch entire video into memory for instant seeking
  const src = video.querySelector('source')?.src || video.currentSrc;
  if (src) {
    fetch(src, { cache: 'force-cache' })
      .then(r => r.blob())
      .then(blob => {
        const url = URL.createObjectURL(blob);
        video.src = url;
        const old = video.querySelector('source');
        if (old) old.remove();
        const s = document.createElement('source');
        s.src = url;
        s.type = 'video/mp4';
        video.appendChild(s);
        video.load();
      })
      .catch(() => {});
  }

  // Read duration
  let duration = 7;
  video.addEventListener('loadedmetadata', () => { duration = video.duration || 7; });
  if (video.readyState >= 1) duration = video.duration || 7;

  // Safari prime: muted play+pause on first interaction to unlock seeking
  let primed = false;
  const prime = () => {
    if (primed) return;
    primed = true;
    video.play().then(() => video.pause()).catch(() => {});
    window.removeEventListener('touchstart', prime);
  };
  window.addEventListener('touchstart', prime, { passive: true });

  // rAF loop — read scrollY directly, no scroll event listener
  const hero = document.getElementById('hero');
  let cur = 0;
  let raf = 0;

  const tick = () => {
    raf = requestAnimationFrame(tick);

    const scrollable = hero.offsetHeight - window.innerHeight;
    const scrolled = Math.max(0, window.scrollY);
    const progress = Math.min(1, scrolled / scrollable);

    const target = progress * duration;

    // Smooth lerp — prevents jitter from individual scroll wheel ticks
    cur += (target - cur) * 0.12;
    if (Math.abs(target - cur) < 0.004) cur = target;

    // Frame-accurate seek
    if (video.readyState >= 2 && Number.isFinite(cur) && duration > 0) {
      const seekTime = Math.min(cur, duration - 0.05);
      if (Math.abs(video.currentTime - seekTime) > 0.01) {
        try { video.currentTime = seekTime; } catch (e) {}
      }
    }

    // Scroll hint fade (only at very start)
    if (hint) {
      const h = Math.max(0, 1 - progress / 0.05);
      hint.style.opacity = h;
      hint.style.visibility = h <= 0 ? 'hidden' : 'visible';
    }

    // Progress bar
    if (progressBar) progressBar.style.width = (progress * 100) + '%';
  };

  raf = requestAnimationFrame(tick);
})();
```

### Key Implementation Details

**Blob preloading:** Standard `<video preload="auto">` does NOT guarantee the browser has buffered the entire file. `fetch()` + `URL.createObjectURL()` puts the full video in memory, eliminating disk I/O and network latency during seeking.

**rAF-only scroll reading:** Do NOT attach a scroll event listener. Read `window.scrollY` directly inside `requestAnimationFrame`. This avoids the overhead of a separate event handler and eliminates synchronization issues.

**Lerp factor (0.12):** Smooths individual scroll wheel ticks into a fluid motion. Higher values = more responsive but potentially jittery. Lower values = smoother but laggy. 0.12 is proven across multiple production implementations.

**Mobile fallback:** On screens <768px, prefers-reduced-motion, or save-data connections, fall back to a standard autoplay loop. Don't force scroll scrubbing on mobile.

**Safari/iOS:** iOS Safari will NOT decode video frames for seeking unless the video has been played at least once. The "prime" pattern (muted play + pause on first touch/scroll interaction) unlocks seeking.

## Pitfalls

- **Overlay fade surprises:** The Soleiman-style fade at 5–25% scroll looks like the video is "fading to an end screen." For transformation/reveal content, keep the overlay visible (Mode B).
- **Wrong scrub distance:** Using `PIN = 1.5` (150vh) when the user expects full-section scrub (240vh) makes the video complete too fast. Always confirm the scrub distance.
- **Video too large:** A 21MB 1080p30 video vs a 5MB 720p24 video makes a dramatic difference in scrub smoothness. Encode at 720p24 with `-g 1`.
- **No Safari prime:** Without the play+pause priming, the video stays black on iOS Safari because seeking doesn't decode frames.
- **Canvas overhead:** Don't render video frames onto a `<canvas>` via `drawImage`. Use a direct `<video>` element with `object-fit: cover`. Canvas adds a compositing bottleneck.
- **Overlay pointer-events:** Set `pointer-events: none` on overlays so clicks pass through to navigation/buttons beneath.

## Verification

1. Open the page and scroll down — video should progress frame-by-frame
2. Scroll back up — video should reverse smoothly
3. Test on Safari/iOS — video should play, not stay black
4. Check blob loading via DevTools Network tab — video should load once, then show `blob:` URL in video element
5. Open on mobile (<768px) — should autoplay in a loop, not scrub===ME:scroll-scrub-video