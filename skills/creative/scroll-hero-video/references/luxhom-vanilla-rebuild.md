# LuxHom Scroll Hero — Vanilla JS Rebuild

Source: `~/clawd/projects/luxhom-site/public/index.html`
Live: `luxhom-site.vercel.app`

## Video specs

- Source: `empty_to_finished_interior_transition_1920x1080.mp4` (7s, 1920x1080, 30fps)
- Scrub: 1280x720, 24fps, 5.8Mbps, 4.8MB
- Encode command:
  ```bash
  ffmpeg -y -i source.mp4 \
    -c:v libx264 -g 1 -crf 26 -preset medium \
    -pix_fmt yuv420p -movflags +faststart -an \
    -vf "scale=1280:720:flags=lanczos,fps=24" \
    scrub.mp4
  ```

## Key decisions vs Soleiman

| Decision | Soleiman | LuxHom |
|---|---|---|
| Lerp | 0.12 on time values (framer-motion) | Same, vanilla JS |
| Blob preload | No (browser handles 6MB fine) | Yes + `cache: force-cache` |
| Scroll reader | framer-motion `useScroll()` | `window.scrollY` in rAF |
| Safari prime | Not present in the component | `touchstart` → play+pause |
| CSS transitions | framer-motion `useTransform` | `.15s linear` CSS |
| `pointer-events` | Not set | `none` on overlay |
| `will-change` | Not set | `transform` on video + sticky |

## Complete vanilla JS

```javascript
(function() {
  const video = document.getElementById('heroVideo');
  const overlay = document.getElementById('heroOverlay');
  const hint = document.getElementById('heroHint');
  const progressBar = document.getElementById('progressBar');
  if (!video) return;

  // Detect constraints
  const isMobile = matchMedia('(max-width: 767px)').matches;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = navigator.connection?.saveData === true;

  if (isMobile || reduceMotion || saveData) {
    video.classList.add('mobile-fallback');
    video.loop = true;
    video.play().catch(() => {});
    return;
  }

  video.loop = false; video.pause();

  // Blob preload
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

  // Safari/iOS prime
  let primed = false;
  const prime = () => {
    if (primed) return; primed = true;
    video.play().then(() => video.pause()).catch(() => {});
    window.removeEventListener('touchstart', prime);
  };
  window.addEventListener('touchstart', prime, { passive: true });

  const PIN = 1.5;
  let cur = 0;
  let raf = 0;

  const tick = () => {
    raf = requestAnimationFrame(tick);

    const progress = Math.min(1, Math.max(0, window.scrollY / (window.innerHeight * PIN)));
    const target = progress * dur();

    cur += (target - cur) * 0.12;
    if (Math.abs(target - cur) < 0.004) cur = target;

    if (video.readyState >= 2 && Number.isFinite(cur) && duration > 0) {
      const seekTime = Math.min(cur, dur() - 0.05);
      if (Math.abs(video.currentTime - seekTime) > 0.01) {
        try { video.currentTime = seekTime; } catch (e) {}
      }
    }

    // Overlay fade: 5% -> 25% scroll
    const f = Math.max(0, Math.min(1, 1 - (progress - 0.05) / 0.20));
    overlay.style.opacity = f;

    // Hint fade: gone by 8%
    const h = Math.max(0, 1 - progress / 0.08);
    hint.style.opacity = h;
    hint.style.visibility = h <= 0 ? 'hidden' : 'visible';

    progressBar.style.width = (progress * 100) + '%';
  };

  raf = requestAnimationFrame(tick);
})();
```

## Research sources

- steveharrison/scroll-video: Blob preloading pattern
- pulkitxm/claude-directory/apex-scroll-hero: rAF-only scroll
- Soleiman ScrubHero: Fixed 0.12 lerp on time values, 0.004 threshold
- webperfclinic.com: CSS scroll-driven animations background
- Brad Holmes: "Everything on compositor" philosophy (will-change, GPU layers)