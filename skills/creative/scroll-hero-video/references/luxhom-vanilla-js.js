// LuxHom — vanilla JS scroll hero with blob preloading (no framework)
// Deployed at: https://luxhom-site.vercel.app/
// Video: 1280x720, 24fps, 4.8MB, empty_to_finished_interior transition
// Key difference from Soleiman: blob preloading + adaptive lerp + seek queue management

/* ─── HTML ───
<section class="hero" id="hero">
  <div class="hero-sticky">
    <video id="heroVideo" muted playsInline preload="auto" poster="images/photo_01.jpg">
      <source src="videos/scrub.mp4" type="video/mp4">
    </video>
    <div class="hero-overlay" id="heroOverlay">...</div>
    <div class="hero-scroll-hint" id="scrollHint">...</div>
  </div>
</section>
─── */

/* ─── CSS ───
.hero{position:relative;width:100%;height:250vh;background:#0d0a08}
.hero-sticky{position:sticky;top:0;width:100%;height:100vh;overflow:hidden}
.hero video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
─── */

// ─── JS (key sections) ───

// 1. BLOB PRELOAD — fetch entire video into memory
const src = video.querySelector('source')?.src || video.src;
if (src) {
  fetch(src)
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
    .catch(() => {});  // fallback: original src works
}

// 2. SCROLL HANDLER (passive: only stores target)
const onScroll = () => {
  const vh = window.innerHeight;
  target = Math.min(1, Math.max(0, window.scrollY / (vh * PIN_HEIGHT)));
};
window.addEventListener('scroll', onScroll, { passive: true });

// 3. rAF TICK — adaptive lerp + seek queue management
let lastSeek = 0;
const tick = () => {
  raf = requestAnimationFrame(tick);
  const vh = window.innerHeight;
  target = Math.min(1, Math.max(0, window.scrollY / (vh * PIN_HEIGHT)));

  // Adaptive lerp: faster when far behind
  const diff = Math.abs(target - cur);
  const factor = diff > 0.1 ? 0.35 : diff > 0.05 ? 0.25 : 0.12;
  cur += (target - cur) * factor;
  if (diff < 0.002) cur = target;

  if (video.readyState >= 2 && Number.isFinite(cur) && duration > 0) {
    const t = Math.min(cur * duration, duration - 0.05);
    const now = performance.now();
    // Skip intermediate seeks when behind — jump to latest
    if (now - lastSeek > 8 || Math.abs(t - video.currentTime) > 0.15) {
      lastSeek = now;
      try { video.currentTime = t; } catch (e) {}
    }
  }
};
raf = requestAnimationFrame(tick);