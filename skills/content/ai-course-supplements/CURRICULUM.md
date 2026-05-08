# Spark-Tier Curriculum — Combined `ai-course-transcripts` + `ai-course-supplements`

**Audience:** A creator (or agency operator) starting from zero, intending to build and run a spicy AI-influencer business in May 2026.
**Hardware:** DGX Spark Founders Edition (or equivalent: GB10 Blackwell, ARM, 120 GB unified memory).
**Outcome:** First Fanvue revenue within 90 days, 2-5 characters in production within 6 months, agency-grade tooling.
**Why this curriculum:** Herman Carter's "AI Model Factory" course is the ground truth for the playbook. The 12 supplement lessons fix what's outdated, missing, or wrong by 2026. Used together they form a complete operating manual.

---

## Reading order

This order interleaves Herman's modules (`T:` prefix, in `~/clawd/skills/ai-course-transcripts/`) with the supplement lessons (`S:` prefix, in `~/clawd/skills/ai-course-supplements/`).

### Phase A — Foundations (Week 1, ~10 hours)

1. `T: AIIC V2 Phase 0 Buckle up` — Foundation, mindset, what the course covers.
2. `T: AIIC V2 Phase 1 Know your Audience` — Niche selection, gooner-mindset thesis, scout influencers.
3. `T: AIIC V2 Phase 2 The Face of Your Empire I-II (ComfyUI vs SugarLab)` — branching path decision.
4. `S: 03-image-models.md` — REPLACE Herman's Flux Dev FP8 with FLUX.2-dev / Z-Image / Qwen-Image. Explains why this matters in May 2026.
5. `S: 08-spark-blackwell-opt.md` — Why Spark gives you 6.3× over the RunPod 4090 the course uses, what to install (NVFP4, SageAttention 2.2).

### Phase B — Character creation (Week 2, ~15 hours)

6. `T: ComfyUI Masterclass Phase 01 I-II` — Setup. Use the install steps but redirect Flux Dev → FLUX.2 per S:03.
7. `S: 01-character-consistency.md` — REPLACE Herman's "buy a Jack LoRA" with PuLID-FLUX2 or InfiniteYou. Faster, cheaper, more flexible.
8. `S: 02-lora-training.md` — When you DO need a custom LoRA (premium creators, brand-locked faces), train it yourself with ai-toolkit. Herman said this doesn't work; he was wrong about the hyperparameters.
9. `T: ComfyUI Masterclass Phase 02 I-III` — Master Workflow walkthrough, SFW + NSFW Pony branch.
10. `S: 07-nsfw-techniques.md` — REPLACE Damn Pony Realistic + YOLO V8 with Z-Image + ADetailer Nipples + Florence-2.
11. `T: SugarLab AI Masterclass` (full) — Optional no-code path. Skip if going Spark-only.

### Phase C — Visuals at quality (Week 3, ~10 hours)

12. `T: Instagram Posts Masterclass Phase 01-02` — Photoshop + CCSR + Enhancer.AI flow.
13. `S: 12-post-processing.md` — REPLACE CCSR with SUPIR. REPLACE Enhancer.AI with ImpurePores + Detailed Skin LoRAs (free, runs at sample-time on Spark).
14. `T: Vault — ComfyUI LoRA / Fanvue Likes` — Bonus content from Herman.

### Phase D — Reels + voice + lipsync (Week 4, ~15 hours)

15. `T: Instagram Reels Masterclass Phase 0-02` — 6 content formats, CapCut, Kling AI signup.
16. `S: 04-video-models.md` — REPLACE Kling AI (cloud) with Wan 2.2 / HunyuanVideo 1.5 / LTX-Video v2 (local on Spark).
17. `S: 05-lipsync.md` — ADD lipsync as a content format Herman skips entirely. MuseTalk 1.5 + Wan2.2-S2V open up talking-head Reels.
18. `S: 06-voice-cloning.md` — REPLACE ElevenLabs with F5-TTS / Voxtral. Free, no NSFW filter, runs on Spark.
19. `T: Reels Masterclass Phase 03-05 (Tips & Tricks, American Gooners)` — Advanced reel formats.

### Phase E — Auto-prompting + ops (Week 5, ~10 hours)

20. `S: 11-auto-prompting.md` — REPLACE manual ChatGPT-assisted wildcards with DSPy MIPROv2 + JoyCaption Two reverse-prompting + ComfyUI in-workflow LLM expansion.
21. `S: 13-spark-only-workflows.md` (deeper) — Workflows ONLY possible on Spark (multi-character batches, long-form HunyuanVideo, simultaneous voice+lipsync+video pipelines). This is the agency-mode unlock.

### Phase F — Instagram + Fanvue setup (Week 6-7, ~15 hours)

22. `T: AIIC V2 Phase 3 IG Setup Like a Pro` — Separate phone, new SIM, Apple ID, no VPN.
23. `S: 09-ig-fanvue-2026.md` — UPDATES on top of Herman's IG setup (Threads/Bluesky cross-post, Meta Verified, ManyChat funnel, 2026 shadowban patterns).
24. `T: Fanvue Masterclass Phase 01-02` — Setup, banner, content, verification.
25. `T: AIIC V2 Phase 4 Boosting` — Tinder Passport, Bouncy AI, Meta Ads, IG strategy.

### Phase G — Launch + content engine (Week 8-12, ~15 hours/week)

26. `S: 15-content-calendar-90-day.md`  — Day-by-day 90-day execution plan combining everything above.
27. `T: AIIC V2 Phase 5 Content That Prints` — Wildcard generation, "500 images, ~200 keepers" strategy.
28. `T: AIIC V2 Phase 6 Launch Day` — First post, first reel, first link-in-bio.
29. `S: 14-pricing-and-revenue-2026.md`  — What to charge, how to model revenue.

### Phase H — Scaling + agency mode (Month 4+)

30. `S: 10-multi-creator-scale.md` — Subgraph blueprints + ComfyDeploy + per-creator JSON config for 5-10 creators.
31. `S: 17-automation-and-orchestration.md`  — n8n + Hermes Atlas for end-to-end agency ops.
32. `S: 16-legal-rights-and-takedowns.md`  — TOS, DMCA, deepfake law, jurisdiction.

---

## Decision rules baked in

- **Image gen path:** Always FLUX.2 default. Z-Image when NSFW realism is critical. Qwen-Image for text/skin specifically. SDXL Pony only legacy / per-prompt edge cases. (S:03)
- **Character lock:** Try PuLID-FLUX2 first (fastest). Fall back to InfiniteYou for higher fidelity. Train a LoRA only when above-90% identity match is required AND you've validated the dataset (S:01, S:02).
- **Video path:** Wan 2.2 default for any cinematic / NSFW. LTX-Video v2 for fast preview iteration. Kling AI only when prompt has cloud-only feature (e.g. lip sync without local setup). (S:04)
- **Voice path:** F5-TTS for English / Western langs. OmniVoice for non-English / 600+ language tail. Voxtral for premium-feel cloning. ElevenLabs only legacy. (S:06)
- **Hardware path:** Always Spark first. Cloud (RunPod / Fal AI) only for spillover or for jobs that need a GPU type Spark lacks (e.g. multi-node training). (S:08)
- **Distribution path:** IG primary, Threads + Bluesky cross-post (free reach, S:09), Fanvue monetization (S:09 + T:Fanvue Masterclass).

---

## What this curriculum drops from Herman's flow

| Course element | Status | Reason |
|---|---|---|
| RunPod 4090 cloud setup | DROPPED | Spark replaces it (S:08, S:13) |
| Buy a Jack character LoRA | OPTIONAL | PuLID-FLUX2 / InfiniteYou skip this; LoRA still useful for premium characters |
| Damn Pony Realistic NSFW | DEPRECATED | Z-Image base + NSFW MASTER FLUX > Pony (S:03, S:07) |
| Kling AI for SFW Reels | OPTIONAL | Wan 2.2 + LTX-Video local replace it (S:04) |
| ElevenLabs voice | DEPRECATED | F5-TTS / Voxtral local (S:06) |
| Photoshop + CCSR + Enhancer.AI | OPTIONAL | SUPIR + LoRA-based skin alts (S:12) |
| Tinder Passport US-targeting | DEMOTED | Meta Verified + ManyChat funnel are bigger 2026 levers (S:09) |
| Bouncy AI link-in-bio | KEPT | Still the right call. Confirmed in S:09 |
| accessmarket.com aged accounts | KEPT | Still works in 2026 |
| Manual ChatGPT wildcards | DEPRECATED | DSPy MIPROv2 + JoyCaption Two (S:11) |

---

## What this curriculum adds beyond Herman's flow

| Capability | From | Why it matters |
|---|---|---|
| Local LoRA training | S:02 | Drops $100/character cost, full control, no Jack queue |
| PuLID-FLUX2 / InfiniteYou identity injection | S:01 | Skip training entirely for many characters |
| Multi-reference Flux.2 | S:01, S:03 | Natively understand 6 reference images, no LoRA |
| Talking-head Reels via lipsync | S:05 | Format Herman cannot produce (no lipsync taught) |
| Voice cloning local | S:06 | No ElevenLabs subscription, no NSFW filter |
| Long-form HunyuanVideo | S:04, S:13 | 2+ minute clips, course was capped at Kling's 10s |
| NVFP4 + SageAttention 2.2 | S:08 | 6.3× speed on Blackwell, course doesn't know about Spark |
| Multi-character batch generation | S:10, S:13 | Agency-mode capability (5-10 creators), course is single-creator |
| DSPy auto-prompt optimization | S:11 | 5-15% absolute lift over manual wildcards |
| n8n + Hermes Atlas orchestration | S:17 | End-to-end automation: gen → upload → notify → log |
| Threads + Bluesky cross-post | S:09 | Free incremental reach |
| Meta Verified + ManyChat funnel | S:09 | Higher leverage than Tinder Passport in 2026 |
| Spark-only privacy edge | S:13 | NSFW never leaves the box, regulatory + brand safety |

---

## How to use this curriculum

Sequential reading: Phase A → H, ~3-4 months total at part-time pace, 2 months full-time. Each phase has measurable end-of-phase deliverables (one character generated, one Reel posted, one Fanvue sub, etc.).

Reference reading: When stuck on a specific topic, look up the supplement lesson first (faster, more current), then check Herman's transcript for the strategic context.

Agent reading: This curriculum is RAG-friendly. Index both skills into the same vector store with `source: transcripts | supplements` metadata. A creator-facing agent can answer "how do I do X" by retrieving the supplement first, the transcript second.

---

## Update cadence

Per quarter:
- Refresh `S:03 image-models`, `S:04 video-models`, `S:05 lipsync`, `S:06 voice-cloning`. Frontier churns fast.
- Refresh `S:09 ig-fanvue-2026` after any Meta or Fanvue policy update.
- Re-validate `S:14 pricing` against latest creator-revenue surveys.

Per major release:
- New FLUX.X / Qwen-Image / Wan version → S:03/S:04 patches
- New Spark BIOS / DGX OS update → S:08 + spark-stability research

---

**This document is the single starting point. Everything else is referenced, not duplicated.**
