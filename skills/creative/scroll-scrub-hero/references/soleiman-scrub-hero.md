# Soleiman ScrubHero — Reference Implementation

This is the exact ScrubHero component from soleiman-advocatuur.vercel.app, the reference site the user pointed to.

## Full Component (Next.js, framer-motion)

```tsx
"use client";

import { useEffect, useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { ArrowRight, ChevronDown, Phone } from "lucide-react";

export function ScrubHero() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const { scrollY } = useScroll();
  const [vh, setVh] = useState(800);
  const [scrub, setScrub] = useState(false);

  // Determine viewport + whether to enable scroll-scrubbing (desktop, motion allowed)
  useEffect(() => {
    let raf = 0;
    const sync = () => {
      const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      const big = window.matchMedia("(min-width: 768px)").matches;
      const saveData =
        (navigator as Navigator & { connection?: { saveData?: boolean } })
          .connection?.saveData === true;
      setVh(window.innerHeight);
      setScrub(big && !reduce && !saveData);
    };
    const schedule = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(sync);
    };
    schedule();
    window.addEventListener("resize", schedule);
    return () => { cancelAnimationFrame(raf); window.removeEventListener("resize", schedule); };
  }, []);

  // Scroll -> video.currentTime, rAF-throttled with easing for smooth scrubbing
  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;
    if (!scrub) {
      v.loop = true;
      v.play().catch(() => {});
      return;
    }
    v.pause();
    v.loop = false;
    let raf = 0;
    let cur = 0;
    const loop = () => {
      const dur = v.duration || 8;
      const pin = vh * 1.5;
      const p = Math.min(1, Math.max(0, scrollY.get() / pin));
      const target = p * dur;
      cur += (target - cur) * 0.12;
      if (Math.abs(target - cur) < 0.004) cur = target;
      if (v.readyState >= 2 && Number.isFinite(cur)) {
        try { v.currentTime = cur; } catch { /* seeking not ready */ }
      }
      raf = requestAnimationFrame(loop);
    };
    const start = () => { raf = requestAnimationFrame(loop); };
    if (v.readyState >= 1) start();
    else v.addEventListener("loadedmetadata", start, { once: true });
    return () => cancelAnimationFrame(raf);
  }, [scrub, vh, scrollY]);

  const introY = useTransform(scrollY, [0, vh * 0.9], [0, -18]);
  const cueOpacity = useTransform(scrollY, [0, vh * 0.18], [1, 0]);

  return (
    <section className="relative h-[250vh] bg-[#071522]">
      <div className="sticky top-0 h-screen w-full overflow-hidden">
        <video
          ref={videoRef}
          className="absolute inset-0 h-full w-full object-cover"
          muted playsInline preload="auto"
          poster="/images/lady-justice-poster.jpg"
        >
          <source src="/video/lady-justice-scrub.mp4" type="video/mp4" />
        </video>

        {/* Dark gradient overlays */}
        <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(7,21,34,0.92)_0%,rgba(7,21,34,0.72)_38%,rgba(7,21,34,0.34)_70%,rgba(7,21,34,0.2)_100%)]" />
        <div className="absolute inset-x-0 bottom-0 h-56 bg-gradient-to-t from-[#071522] via-[#071522]/55 to-transparent" />

        {/* Content overlay */}
        <motion.div style={{ y: introY }} className="absolute inset-0 flex items-center">
          <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl text-white">
              <h1 className="font-serif text-[2.5rem] font-semibold leading-[0.98] sm:text-6xl md:text-7xl xl:text-[5rem]">
                Advocatuur op hoog niveau in Rotterdam.
              </h1>
              <p className="mt-6 max-w-2xl font-serif text-xl italic leading-snug text-[#d9bd8a] sm:text-2xl">
                Letselschade, arbeidsrecht, bestuursrecht en contractrecht.
              </p>
              {/* CTA buttons */}
              <div className="mt-9 flex flex-col gap-3 sm:flex-row sm:items-center">
                <a href="#contact" className="group inline-flex items-center justify-center rounded-[4px] bg-[#f5efe6] px-7 py-4 text-sm font-bold text-[#0f2644] transition hover:bg-white">
                  Plan een vertrouwelijke kennismaking
                  <ArrowRight className="ml-3 h-4 w-4 transition group-hover:translate-x-1" />
                </a>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Scroll hint */}
        <motion.div style={{ opacity: cueOpacity }} className="absolute bottom-7 left-1/2 -translate-x-1/2 text-white/65">
          <span className="flex flex-col items-center gap-2 text-[10px] font-bold uppercase tracking-[0.3em]">
            Scroll
            <ChevronDown className="h-4 w-4 animate-bounce" />
          </span>
        </motion.div>
      </div>
    </section>
  );
}
```

## Key Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Video source | `/video/lady-justice-scrub.mp4` | Encoded with `-g 1` |
| Video duration | 8s (fallback) | Read from `loadedmetadata` |
| Scroll distance (PIN) | `vh * 1.5` | 1.5 viewport heights |
| Lerp factor | `0.12` | Slower than apex (0.14) — smoother but more laggy |
| Scroll runway | `250vh` | 1.5x pin + buffer |
| Overlay fade start | 5% | First content fades quickly |
| Overlay fade end | ~20% | Full opacity → hidden |
| Scroll hint fade | 18% | `cueOpacity` transform |
| Mobile breakpoint | 768px | Below: autoplay loop fallback |

## LuxHom Adaptation (Static HTML)

The Soleiman pattern was adapted for a static HTML site (luxhom-site.vercel.app). Key differences:
- No framer-motion: used vanilla JS with direct `requestAnimationFrame`
- No React: used `document.getElementById` and `element.style`
- Video: `empty_to_finished_interior_transition_1920x1080.mp4` → re-encoded to `scrub.mp4`
- Full pattern includes progress bar synced to scroll