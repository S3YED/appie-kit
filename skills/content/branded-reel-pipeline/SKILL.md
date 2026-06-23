---
name: branded-reel-pipeline
description: "Use when producing a PREMIUM short-form BRAND reel end to end with real on-brand visuals and (optionally) live dashboard/analytics data baked in — e.g. 'make a branded reel', 'cut a premium reel for <brand>', 'turn this dashboard into a reel', 'make an analytics reel', 'reel from the Content Factory brief', 'show our real numbers in a 9:16'. The reusable framework + presets + scripts: script → Higgsfield visuals + music → ElevenLabs VO → Playwright live-data capture → Remotion brand-preset assembly → MP4 + ffprobe verify. Runs gated (human approves script, then assets, before final render) or auto. This is the premium-reel LAYER on top of short-form-video-production; do not duplicate that skill — cross-reference it for ideation/hook/retention craft."
allowed-tools: Bash, Read, Write, Edit
---

# Branded Reel Pipeline

Reusable framework that produces a premium short-form brand reel end to end. It is the
**premium layer** on top of `media/short-form-video-production` (ideation, hook,
retention, captions craft).
Use those for the *creative* craft; use this for the *premium branded assembly* with real
on-brand visuals and live data.

## The proven stack (do not deviate without reason)

1. **Script** — hook-first, retention-structured. Borrow craft from `content-creation`
   (Hook→Tension→Payload→CTA) and `short-form-video-production`. Beat table: `t | OST | VO`.
2. **Visuals + music** — `higgsfield-generate` skill. GPT Image 2 for hero frames (9:16,
   2k, brand palette), `sonilo_music` for the bespoke bed. Frames are premium connective
   tissue; live screens carry conversion.
3. **Voiceover** — ElevenLabs `eleven_v3`, stability `0.30`, default voice id
   `cjVigY5qzO86Huf0OWal` ("Eric"). Key from environment. Calm-operator delivery.
4. **Live-data capture** — `reference/live-data-capture.py` (Playwright). Parameterized:
   URL + auth method + selector / API path. The differentiator: real dashboards, real
   numbers count up on screen.
5. **Assembly** — Remotion with brand-preset tokens (`templates/remotion-template/`).
   Parameterized by aspect ratio. Count-ups, curve-draws, glass device frames, the
   audio-reactive orb. 1080x1920 @ 30fps for 9:16.
6. **Render + verify** — `remotion render` → `ffprobe` confirms duration/resolution/codec.

## Input: the brief

A reel is driven by a brief object:

```json
{
  "subject": "Our AI agent that posts daily and tracks every number",
  "brand_preset": "my-brand",
  "format": "9:16",
  "mode": "gated",
  "live_data_source": {
    "url": "https://your-dashboard.example.com/api/analytics?days=30",
    "auth": { "method": "session_token", "mint": "node scripts/mint-session-token.js" },
    "capture": "json",
    "selector": null
  },
  "script": null
}
```

- `subject` (required): what the reel is about.
- `brand_preset` (required): a dir under `presets/` matching your brand.
- `format`: `9:16` (default) | `1:1` | `16:9`.
- `mode`: `gated` (default) | `auto`.
- `live_data_source` (optional): `{ url, auth, capture: json|screenshot, selector }`.
- `script` (optional): pre-written beat table; if null the pipeline writes one in Stage 1.

A brief can originate from a **Notion Content Factory** database that `appie-content-intelligence` feeds: pull a row (subject + angle + target), map it onto this schema, run the pipeline.

## Staged workflow (default mode: gated)

A run lives in a workspace dir `projects/reels/<brief-hash>/` (or
`projects/<name>-reel/` for a one-off). Cache keyed by brief hash (see Token optimization).

### STAGE 1 — Script + assets plan
1. Hash the brief → workspace dir. If cache hit on script, reuse.
2. Resolve the brand preset (`presets/<name>/preset.json` + prompt fragments).
3. If `script` not supplied, write the beat table (`script.md`): `t | OST | VO` rows,
   target 18-24s, hook in first 1.5-3s, abrupt end. Pull retention craft from
   `short-form-video-production`. Honour brand voice rules.
4. Write the **shot list / assets plan** (`assets-plan.md`): which beats are generated
   hero frames vs live-screen proof; the Higgsfield prompts (brand palette baked in);
   the music brief; the VO script.
5. Confirm the live-data source is reachable (dry probe), but do NOT generate paid assets yet.

   **GATE 1 (gated mode): stop. Present `script.md` + `assets-plan.md` for approval.**
   In `auto` mode, continue without pausing.

### STAGE 2 — Generate assets + capture live data
6. Generate hero frames via `higgsfield-generate` (one prompt per generated beat, brand
   palette + 9:16). Cache by `(brief-hash, beat-id, prompt-hash)` so re-runs reuse.
7. Generate the music bed via `sonilo_music` (brand music brief). Cache.
8. Generate VO via ElevenLabs (`reference/elevenlabs-vo.sh`). Cache by VO-text hash.
9. Capture live data via `reference/live-data-capture.py` (URL + auth + capture).
   Output `live-data.json` and/or `capture.png`. Crop screenshots if needed.
10. Place all assets into `remotion/public/`.

    **GATE 2 (gated mode): stop. Present the hero frames, the captured data/screens, the
    VO file, and the music for approval before the (compute-heavy) render.**
    In `auto` mode, continue.

### STAGE 3 — Assemble + render + verify
11. Copy `templates/remotion-template/` into the workspace `remotion/` (if not present),
    wire the preset theme + brief data (beats, KPIs, captured json) into `src/`.
12. `npm i` (first run) then `npm run render` → MP4 (preset-driven aspect/fps).
13. `ffprobe` verify: duration within target, resolution matches format, h264/aac.
14. Emit `RUN-REPORT.md`: assets used, cache hits, token budget, ffprobe output, MP4 path.
    Reel is delivered for posting (posting is a separate runtime step — never auto-post).

### Flipping to auto
Set `"mode": "auto"` in the brief (or pass `--mode auto`). The two gates become
no-ops and the pipeline runs Stage 1→3 unattended. Flip this once a brand preset
has produced a clean reel 1-2x. Quality floor still applies: if Stage 3 verify fails,
stop and report, never ship a broken MP4.

## Token optimization (priority)

Documented budget per run, and the levers that keep re-runs near-free:

- **Brief-hash cache.** Everything generated (script, each hero frame, music, VO) is
  cached under `cache/<brief-hash>/` keyed by content hash. A re-run with an unchanged
  brief regenerates **nothing** — it re-assembles from cache. Editing one beat only
  invalidates that beat's frame + that VO line.
- **Reuse hero frames across formats.** 1:1 and 16:9 re-use the same 2k hero frames; only
  the Remotion composition re-renders. No new Higgsfield calls for a format change.
- **Cheapest competent tier for non-creative steps.** Brief parsing, hashing, cache
  lookups, ffprobe checks, JSON reshaping → plain shell / python, no model.
  Script writing is the only step that wants a strong model; route the rest cheap.
- **Single-pass generation.** One Higgsfield prompt per generated beat (no iterate-loops
  unless a gate rejects). One VO pass. One music pass.
- **Reference, don't inline.** Pass asset paths between stages, not asset bytes.

**Token budget per run (design target):**

| Step | Tokens (orchestrator) | Cost driver | Cached re-run |
|------|----------------------|-------------|---------------|
| Brief parse + hash | ~0 (shell) | — | ~0 |
| Script write | 1-3k | model (1 pass) | 0 (cache) |
| Higgsfield frames (N~5) | ~0 orchestration | Higgsfield credits (~1/frame) | 0 (cache) |
| Music (sonilo) | ~0 | Higgsfield credits | 0 (cache) |
| VO (ElevenLabs) | ~0 | EL chars | 0 (cache) |
| Live-data capture | ~0 (script) | — | re-run if data stale |
| Remotion render | ~0 (shell) | local CPU | re-render only on edit |
| Verify (ffprobe) | ~0 (shell) | — | ~0 |

Net: a fresh reel costs ~1-3k orchestrator tokens + Higgsfield/EL credits. A re-run after
an approval tweak costs only the changed beat. A format add (1:1/16:9) costs **zero**
generation credits.

## Brand presets

Each preset is a dir under `presets/<name>/`:
- `preset.json` — the tokens (colors, fonts, easing, motion language, music brief, VO
  voice id + settings, default format) consumed by the Remotion theme.
- `higgsfield.md` — the visual-prompt fragment (palette + style) prepended to every hero
  prompt so all frames are on-brand.
- (optional) `notes.md` — brand voice / do-not rules.

### Add a brand preset
1. `cp -r presets/example presets/<your-brand>`
2. Edit `preset.json`: colors, fonts (`@remotion/google-fonts` names), easing, music
   brief, VO voice id, default format.
3. Edit `higgsfield.md`: the palette + style sentence for hero prompts.
4. (optional) `notes.md` for brand voice rules.
5. Reference it in a brief: `"brand_preset": "<your-brand>"`. No code changes.

## Add a live-data source
`reference/live-data-capture.py` is parameterized. In the brief's `live_data_source`:
- `url`: the page or API endpoint.
- `auth.method`: `none` | `session_token` | `cookie` | `header`. For `session_token`,
  set `auth.mint` to a command that prints the token.
- `capture`: `json` (fetch + parse an API response) | `screenshot` (render + crop a live
  dashboard into a glass device frame).
- `selector`: CSS selector to wait for / crop to (screenshot mode).

The captured `live-data.json` is wired into the Remotion composition as count-up KPIs and
per-channel tiles; `capture.png` drops in as an `<Img>`/`<OffthreadVideo>` proof layer.

## Invocation examples

```bash
# 1. From a brief file (gated — default; pauses at GATE 1 and GATE 2)
python3 reference/run-pipeline.py --brief templates/brief.example.json

# 2. Auto mode (no gates) once a preset is proven
python3 reference/run-pipeline.py --brief my-brief.json --mode auto

# 3. Add a 16:9 cut of an already-rendered reel (zero new generation)
python3 reference/run-pipeline.py --brief my-brief.json --format 16:9 --reuse-assets
```

The orchestrator reads this SKILL, resolves the brief, and runs the stages: it calls
`higgsfield-generate` for visuals/music, `elevenlabs-vo.sh` for VO, `live-data-capture.py`
for data, and the Remotion template for assembly — pausing at the two gates in gated mode.
`run-pipeline.py` is the deterministic skeleton (hash, cache, dirs, gate prompts, render,
verify); the creative calls are delegated to the existing skills.

## Verification checklist
- [ ] Brief validates against schema; brand_preset exists
- [ ] Script: hook in first 1.5-3s, abrupt end, brand voice
- [ ] Hero frames are native 9:16 (or target aspect), on-brand palette
- [ ] Live data captured is REAL (not fabricated); KPIs match the source
- [ ] Gates respected in gated mode; skipped cleanly in auto mode
- [ ] ffprobe: duration in target window, resolution = format, codecs h264/aac
- [ ] Cache populated so re-runs reuse; format-add uses zero generation credits
- [ ] RUN-REPORT.md written with token budget + asset manifest

## Cross-references
- `media/short-form-video-production/SKILL.md` — ideation, hook, retention, caption craft.
- `higgsfield-generate` skill — image/video/music generation (GPT Image 2, sonilo_music).
- `creative/appie-content-intelligence` — feeds the Content Factory; benchmarking.
