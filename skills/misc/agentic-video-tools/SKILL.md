---
name: agentic-video-tools
description: "Compare and integrate agentic short-form video editing SaaS tools and OSS alternatives for the Weblyfe Content Factory pipeline. Use when Appie-2 needs to automate: raw clip → Reel/Short/TikTok with captions/SFX/music/transitions → publish to IG/TikTok/YT with zero human editor in the loop. Covers automation depth ranking, API integration recipes, OSS alternatives, and anti-patterns."
---

# Agentic Video Tools — Weblyfe Content Factory

## Purpose

Equip Appie-2 to choose and drive the right tool for fully automated short-form video production. The decision axis is **automation depth**, not feature richness for human editors. A tool with 50 manual effects but no API is useless. A tool with 3 endpoints and a webhook is gold.

Goal pipeline: `raw clip URL → API call → captions + reframe + music → finished 9:16 MP4 → publish to IG/TikTok/YT`. Human reviews the output, does not produce it.

---

## Sources

| Source | What it gave |
|--------|-------------|
| opus.pro/api + help.opus.pro/api-reference/overview | OpusClip API endpoints, rate limits, webhook spec |
| docs.submagic.co/introduction | Submagic REST API, auth, rate limits |
| docs.vizard.ai/docs/quickstart | Vizard API endpoints, webhook config, sample curl |
| docs.klap.app/pricing | Klap API per-operation costs |
| docs.descriptapi.com | Descript API endpoints, agent automation, callback URLs |
| veed.io/api | VEED Fabric API, fal.ai endpoints, per-second pricing |
| captions.ai/pricing | Captions pricing tiers, no public API found |
| quso.ai/pricing | Quso.ai (formerly Vidyo.ai) pricing, no API listed |
| munchstudio.com | Munch (now Munch Studio), no API found |
| heyeddie.ai | Eddie AI — desktop app, no API |
| tammy.ai reviews | Tammy.ai — summarizer, no clip extraction API |
| Trustpilot/G2/Reddit reviews 2025-2026 | Real creator pain points for OpusClip, Submagic, Klap |
| github.com/harry0703/MoneyPrinterTurbo | 56.7k stars OSS, FastAPI backend, MIT |
| github.com/SamurAIGPT/AI-Youtube-Shorts-Generator | 3.4k stars OSS, Python, MIT |
| github.com/mutonby/openshorts | 1.7k stars OSS, self-hosted, MIT |

---

## Quick Reference

**Automation tier (API > webhook > CLI > Playwright > manual UI):**

| Rank | Tool | Tier | One-line verdict |
|------|------|------|-----------------|
| 1 | **Vizard.ai** | REST API + webhook | Best automation depth for clip generation; docs public, webhook native |
| 2 | **Submagic** | REST API + webhook | Best for captions-only pipelines; public API docs, 100 req/hr export |
| 3 | **Descript** | REST API + callback | Full Underlord agent via API; best for script-based editing at scale |
| 4 | **Klap** | REST API (usage-based) | Clean per-operation pricing; Pro+ required for API access |
| 5 | **OpusClip** | REST API (closed beta) | API exists but gated; virality scores unreliable per creator reviews |
| 6 | **VEED Fabric** | REST API via fal.ai | Image/video generation APIs only; not a clip extractor |
| 7 | **Quso.ai (Vidyo.ai)** | No API | Rebranded Vidyo.ai; web UI only; no automation surface |
| 8 | **Captions.ai** | No public API | Mobile-first; Scale tier may have limited API but not documented |
| 9 | **Munch Studio** | No API | Rebranded GetMunch; no developer surface found |
| 10 | **Eddie AI** | No API | Desktop app (Mac/Win); NLE integration only; not automatable |
| 11 | **Tammy.ai** | No clip API | YouTube summarizer only; not a clip extractor |
| 12 | **Decipher** | N/A | Not a standalone product; generic term; no dedicated tool found |

---

## Comparison Matrix

| Tool | Hook detect | Auto-captions | B-roll | SFX/music | Multi-format export | Brand templates | Voice clone | API/webhook | REST API? | Per-video cost @100/mo | Free tier |
|------|-------------|---------------|--------|-----------|---------------------|-----------------|-------------|-------------|-----------|------------------------|-----------|
| **Vizard.ai** | Yes (LLM virality) | Yes (30+ lang) | No | No | 9:16, 1:1, 16:9 | Yes | No | REST + webhook | Yes (paid plans) | ~$0.20–$0.50 (credit-based, ~$15–20/mo tier) | 60 credits/mo |
| **Submagic** | Yes (magic clips) | Yes (100+ lang, 95-98% acc) | Yes (AI B-roll) | Yes (music sync) | 9:16, 1:1, 16:9 | Yes (unlimited on Business) | No | REST + webhook | Yes (Business $69/mo) | $0.69/video at Business tier | None |
| **Descript** | Via Underlord AI | Yes (transcript-based) | No native | No | Export via publish API | No | Yes (Overdub) | REST + callback | Yes (all paying users, free during beta) | 60 min/mo |
| **Klap** | Yes (LLM) | Yes | No | No | 9:16 primary | Yes | No | REST API | Yes (Pro+ $151/mo) | ~$1.24/video API ($0.32+0.44+0.48 per video) | No |
| **OpusClip** | Yes (virality score) | Yes | Yes (AI B-roll, buggy) | No | 9:16, 1:1, 16:9 | Yes (2 templates Pro) | No | REST + webhook | Business tier only (closed beta, annual) | Custom (Business, contact sales) | 60 min/mo |
| **VEED Fabric** | No (gen only) | No (separate sub API) | No | No | MP4 output | No | No | REST via fal.ai | Yes (pay-per-use) | $4.80/60s video at 720p | Pay-per-use |
| **Quso.ai** | Yes | Yes | No | No | 9:16, 1:1, 16:9 | Yes (Growth tier) | No | None | No | $0.49/video (Growth $49/mo, 100 clips) | 75 credits/mo |
| **Captions.ai** | Yes | Yes (100+ lang) | Yes | Yes | 9:16, 1:1, 16:9 | Yes | Yes (AI voice) | None documented | Not public | ~$0.70–1.40/video (Scale tiers) | No |
| **Munch Studio** | Yes | Yes | No | No | 9:16, 1:1, 16:9 | No | No | None | No | $0.49/video (Elite ~$116/mo, 500 min ≈ ~50 vids) | No |
| **Eddie AI** | No (manual) | Yes | Yes (B-roll log) | No | Via NLE export | No | No | None | No | N/A (desktop app) | No |
| **Tammy.ai** | No | Summaries only | No | No | No video output | No | No | None | No | N/A (summarizer) | Yes |
| **Decipher** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

---

## Automation Tier Ranking

### Tier 1 — REST API + Webhook (fully drivable by Appie-2)

**Vizard.ai**
- `POST /open-api/v1/project/create` → returns `projectId`
- `GET /open-api/v1/project/query/{projectId}` → poll or wait for webhook
- Webhook: configure URL in workspace settings; API POSTs clip metadata when ready
- `POST /open-api/v1/project/publish-video` → direct social publish
- Rate: 10 req/min (Business), 60/hr
- Auth: `VIZARDAI_API_KEY` header

**Submagic**
- `POST https://api.submagic.co/v1/projects` → submit video URL
- Webhook callback on completion
- Rate: 50 export ops/hr, 500 retrieval ops/hr
- Auth: `x-api-key: sk-...` header
- Note: Business tier ($69/mo) required for API; 100 min/month included, extra at $0.10–0.15/min

**Descript**
- `POST /jobs/import/project_media` → import + transcribe
- `POST /jobs/agent` → natural language edit commands (remove fillers, add captions, create clips, translate)
- `POST /jobs/publish` → export shareable link
- Callback via `callback_url` param on any job
- Auth: Bearer token
- Rate: 429 + Retry-After headers; `X-RateLimit-Remaining` exposed
- Status: Free for all paying users during beta (no extra cost)

### Tier 2 — REST API, no native webhook (poll-based)

**Klap**
- API docs at docs.klap.app; three endpoint groups: Tasks, Projects, Exports
- Usage-based: $0.32 generate + $0.44 video input + $0.48 export = **$1.24/video** on pure API
- Pro+ ($151/mo) required for API access; includes 100 uploads + 1,000 exports/mo
- At 100 videos/mo on Pro+: $1.51/video (subscription) or $1.24 pure API

**OpusClip**
- `POST /clip-projects` (video URL submission)
- Query clips, share project, social posting, webhook endpoints documented
- Rate: 30 req/min, 50 concurrent projects
- Auth: API key from dashboard
- BLOCKED: API is closed beta. Requires annual Business plan with 20+ packs/year. Contact sales. No self-serve access.

### Tier 3 — No API / UI-only (Playwright or manual)

Quso.ai, Captions.ai, Munch Studio, Eddie AI, Tammy.ai — all require human to drive the web UI or desktop app. Can be wrapped in Playwright if cost of scripted browser is acceptable, but fragile.

---

## Recommended Stack

### Primary: Vizard.ai + Submagic (layered)

**Vizard** handles the long-to-short intelligence: hook detection, face-tracked reframe, 9:16 output. **Submagic** adds the polished caption layer: animated word-level captions, music sync, B-roll, brand template.

**Why this stack:**
- Both have documented REST APIs with webhooks — zero manual UI touches
- Vizard: ~$0.20–0.50/video; Submagic Business: $0.69/video → combined ~$0.89–1.19/video at 100/mo
- Submagic accuracy 95-98%, real creator-tested; Vizard has n8n template published by the tool itself
- Vizard already has a Claude Skills integration (they published the zip)

**Pipeline flow:**
```
raw clip URL
  → Vizard API (create project, poll/webhook)
  → download 9:16 MP4 from Vizard clip URL
  → Submagic API (submit clip, get captioned output, webhook)
  → finished MP4 with captions + music
  → publish via Vizard publish endpoint OR native IG/TikTok/YT API
```

### Fallback / Script-first option: Descript

For content where Appie-2 has the transcript in advance (podcast, interview), Descript's Underlord API is the most powerful: one `POST /jobs/agent` with a natural language instruction handles filler removal, captions, clips, and translation. Free for all paying users during beta. Use when the clip editing needs script-level precision, not just hook detection.

---

## Integration Recipe

### Vizard.ai

**Auth:** `VIZARDAI_API_KEY` in request header (generate from workspace settings)

**Submit video:**
```bash
curl -X POST https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/create \
  -H "Content-Type: application/json" \
  -H "VIZARDAI_API_KEY: $VIZARD_KEY" \
  -d '{
    "lang": "en",
    "preferLength": [30, 60],
    "videoUrl": "https://your-s3-or-yt-url.mp4",
    "videoType": 2
  }'
# Returns: { "projectId": "abc123", "status": "processing" }
```

**Webhook config:** Set webhook URL once in Vizard workspace settings → Vizard POSTs clip metadata (URLs, timestamps, scores) when ready.

**Poll fallback:**
```bash
curl -X GET https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/query/abc123 \
  -H "VIZARDAI_API_KEY: $VIZARD_KEY"
# Returns: clips array with download URLs when status = "done"
```

**Publish to social:**
```bash
curl -X POST https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/publish-video \
  -H "Content-Type: application/json" \
  -H "VIZARDAI_API_KEY: $VIZARD_KEY" \
  -d '{ "projectId": "abc123", "clipId": "clip456", "platform": "instagram" }'
```

**Full docs:** https://docs.vizard.ai/docs/quickstart

---

### Submagic

**Auth:** `x-api-key: sk-your-key` header (generate from app.submagic.co/account)

**Submit video for captioning:**
```bash
curl -X POST https://api.submagic.co/v1/projects \
  -H "Content-Type: application/json" \
  -H "x-api-key: $SUBMAGIC_KEY" \
  -d '{
    "videoUrl": "https://cdn.your-storage.com/clip.mp4",
    "language": "en",
    "template": "your-brand-template-id",
    "webhookUrl": "https://your-appie-endpoint.com/submagic-done"
  }'
```

**Webhook payload:** On completion Submagic POSTs project metadata including export download URL.

**Rate limits:** 50 export ops/hr, 500 project ops/hr, 1000 meta ops/hr

**Full docs:** https://docs.submagic.co/introduction

---

### Descript (bonus — script-aware editing)

**Auth:** `Authorization: Bearer <token>` (from Descript workspace)

**Import + transcribe:**
```bash
curl -X POST https://api.descript.com/v1/jobs/import/project_media \
  -H "Authorization: Bearer $DESCRIPT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mediaUrl": "https://cdn.your-storage.com/raw.mp4",
    "callbackUrl": "https://appie-endpoint.com/descript-done"
  }'
```

**Run Underlord agent edit:**
```bash
curl -X POST https://api.descript.com/v1/jobs/agent \
  -H "Authorization: Bearer $DESCRIPT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "proj_abc",
    "prompt": "Remove all filler words. Add captions. Create 3 highlight clips of 30-60 seconds each.",
    "callbackUrl": "https://appie-endpoint.com/descript-edit-done"
  }'
```

**Full docs:** https://docs.descriptapi.com/

---

### Tools with no API — Playwright fallback note

Quso.ai, Captions.ai, Munch Studio: use Playwright + a headless Chromium session if forced. Cost: ~30-90 seconds per video, brittle to UI changes, no SLA. Tag these as `MANUAL_OR_PLAYWRIGHT` in pipeline config. Not recommended for Appie-2 primary path.

---

## Output Flexibility

| Tool | SRT export | EDL export | Asset separation | Finished MP4 only |
|------|-----------|-----------|-----------------|-------------------|
| Vizard.ai | Yes (via clip metadata) | No | No | MP4 + metadata JSON |
| Submagic | Yes | No | No | MP4 + SRT |
| Descript | Yes | Yes (Premiere XML) | Audio/video tracks | All formats via publish |
| Klap | No (UI only) | No | No | MP4 only |
| OpusClip | Yes (SRT) | No | No | MP4 + SRT |
| VEED Fabric | No | No | No | MP4 URL |

For full asset separation (SRT + video tracks + EDL), **Descript is the only tool** in this list that comes close. All others output finished MP4s only.

---

## Open-Source Alternatives

### 1. MoneyPrinterTurbo
- **Repo:** https://github.com/harry0703/MoneyPrinterTurbo
- **Stars:** 56,700+ | **Last commit:** Apr 2026 | **License:** MIT
- **What it does:** Text prompt → script → B-roll footage → TTS voiceover → subtitles → HD short (9:16 or 16:9). Full pipeline in one tool. FastAPI backend with Swagger UI at `:8080/docs`. Docker-ready.
- **Tech:** Python, FastAPI, MoviePy, Streamlit, Whisper, multiple LLM/TTS providers
- **Good for:** Faceless content automation (no raw clip needed — generates from scratch)
- **Lacks:** No input-clip-to-short conversion. Takes a topic keyword, not an existing video. Not a replacement for Vizard/Klap.

### 2. AI-Youtube-Shorts-Generator (SamurAIGPT)
- **Repo:** https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator
- **Stars:** 3,400 | **Last commit:** 2025 | **License:** MIT
- **What it does:** YouTube URL → Whisper transcription → GPT-4o-mini highlight detection → face-tracked vertical crop → 9:16 MP4 clips. Direct OSS replacement for OpusClip/Vidyo.ai/Klap.
- **Tech:** Python, yt-dlp, faster-whisper, OpenCV, ffmpeg, OpenAI API
- **Good for:** Batch processing existing YouTube content with no SaaS cost. Self-hostable. API cost only (OpenAI).
- **Lacks:** No captions layer, no brand templates, no direct social publish, no REST API wrapper. Requires engineering work to embed in Appie-2 pipeline.

### 3. OpenShorts (mutonby)
- **Repo:** https://github.com/mutonby/openshorts
- **Stars:** 1,700 | **Last commit:** May 2026 (active) | **License:** MIT
- **What it does:** Self-hosted platform with three modes: (1) clip generator — viral moment detection from long video using Gemini, faster-whisper, YOLOv8 face tracking, FFmpeg; (2) AI Shorts with synthetic actors via ElevenLabs + fal.ai; (3) YouTube Studio for thumbnails/titles. Docker Compose, React + FastAPI + AWS S3.
- **Tech:** Python 3.11, FastAPI, React, Vite, YOLOv8, MediaPipe, Google Gemini, fal.ai, ElevenLabs, Docker
- **Good for:** The most complete OSS alternative to a full SaaS stack. Self-hosted = no per-video fee. Clip gen + captions + social features in one repo.
- **Lacks:** No published REST API (internal only); no built-in social publisher; requires infra management; ElevenLabs and fal.ai API costs still apply.

**OSS recommendation for Weblyfe:** Run **AI-Youtube-Shorts-Generator** for clip extraction + **Submagic API** for captions as a cost-optimised hybrid. OSS handles the expensive clip generation; Submagic adds the polished caption layer at $0.69/video. Total cost drops to ~$0.20/video (OpenAI Whisper + GPT-4o-mini per clip) + $0.69 Submagic = ~$0.89/video, minus any SaaS subscription base cost.

---

## Anti-Patterns

These tools market themselves as AI-automated but require human review at every clip:

**OpusClip (review loop anti-pattern)**
- The web UI defaults to a "review and pick clips" workflow. The API exists but is closed beta (annual Business, 20+ packs/year, contact sales). Most creators using OpusClip are in the manual UI loop. Creator reviews: "I end up spending more time correcting the AI than just editing." Virality scores confirmed unreliable. The "AI Video Compilation Maker" feature advertised on the marketing page does not exist per creator reports.

**Captions.ai (mobile-first, no automation surface)**
- Explicitly a mobile app. Web version exists but is secondary. No documented REST API. "Scale" tier may expose limited API but no public docs found. One-tap workflows are UI buttons, not API calls. Auto-export times reported as "an hour or more" on Trustpilot. Do not include in Appie-2 automated pipeline.

**Munch Studio (approval-gate UI)**
- The platform explicitly states users "choose posts you love and post with just one click." This is a human-review-required model. No API. Rebranded from GetMunch (itself rebranded), suggesting instability. Avoid.

**Quso.ai / Vidyo.ai (no API, rebranded)**
- Formerly Vidyo.ai (redirects to quso.ai). No API. Scheduling features exist but posting still requires manual approval. The rebrand from Vidyo.ai to Quso.ai mid-2024 means existing integrations and documentation are unreliable.

**Tammy.ai (summarizer, not clip extractor)**
- Produces text summaries and timestamps, not video clips. No video output. Not relevant for this pipeline. Included in original brief but is a different category of tool.

**Eddie AI (desktop NLE assistant, not cloud)**
- Native Mac/Win app. Connects to Premiere, DaVinci, Final Cut. Excellent for human editors. Zero automation surface for agents. Not relevant for Appie-2.

**Klap (API exists but expensive for pure API path)**
- $1.24/video on pure API usage pricing ($0.32 generate + $0.44 input + $0.48 export). At 100 videos/month that's $124/mo in API fees alone, plus the Pro+ subscription ($151/mo). Total: ~$275/mo vs Vizard at ~$20/mo. Use Klap only if Vizard quality is insufficient and API access is the priority.

---

## How to Apply

### Appie-2 content factory pipeline (recommended)

```
1. Receive raw clip (S3 URL or YouTube URL) from content briefing
2. POST to Vizard API → wait for webhook → download 9:16 clips JSON
3. For each clip:
   a. Download clip MP4 from Vizard URL
   b. POST to Submagic API with clip URL + brand template ID
   c. Wait for Submagic webhook → download captioned MP4
4. POST to IG/TikTok/YT via their native publish APIs
   (OR use Vizard publish endpoint for supported platforms)
5. Log output URLs to Notion task + Telegram report to Seyed
```

### For script-based content (podcast/interview processing)

```
1. Upload raw recording to Descript API (import endpoint)
2. Run Underlord agent: "Remove fillers, add captions, extract 3 highlights 30-60s"
3. Receive callback → download export
4. Post-process captions with Submagic if brand template needed
5. Publish
```

### For cost-optimised high-volume (self-hosted hybrid)

```
1. Run AI-Youtube-Shorts-Generator locally (or on Appie-3 Hetzner)
2. Pass output clips to Submagic API for captions
3. Publish via native APIs
Cost: ~$0.10-0.20 (OpenAI) + $0.69 (Submagic) = ~$0.89/video
```

---

## Core Principles

1. **Webhook over polling.** Always configure a webhook endpoint. Polling burns credits and adds latency.
2. **API key per environment.** Never share dev/prod API keys. Store in `~/.openclaw/openclaw.json` → `env.vars`.
3. **Validate output before publishing.** Even automated pipelines should run a sanity check (duration > 5s, file size > 100KB) before the publish step. One bad clip posted is a brand problem.
4. **Don't pay for virality scores.** Creator consensus: OpusClip's virality score and Munch's "trending" signals are unreliable. Use them as tie-breakers only, never as primary selectors.
5. **Layer tools, don't consolidate.** Vizard (clip extraction) + Submagic (captions) beats any single all-in-one tool on both quality and automation depth.
6. **OSS for clip extraction, SaaS for captions.** The clip extraction step (long→short) is well-solved in OSS. The polished caption layer (animated, brand-templated, word-level) is not. Split accordingly.
7. **Respect rate limits.** Submagic: 50 export ops/hr. Vizard Business: 60 req/hr. Queue jobs; never burst.

---

## Examples

### Submit a YouTube clip to Vizard + receive webhook (Python)
```python
import httpx, os

VIZARD_KEY = os.environ["VIZARD_KEY"]
WEBHOOK_URL = "https://appie.weblyfe.nl/hooks/vizard"

resp = httpx.post(
    "https://elb-api.vizard.ai/hvizard-server-front/open-api/v1/project/create",
    headers={"VIZARDAI_API_KEY": VIZARD_KEY, "Content-Type": "application/json"},
    json={
        "lang": "en",
        "preferLength": [30, 60],
        "videoUrl": "https://youtube.com/watch?v=XXXX",
        "videoType": 2,
        "webhookUrl": WEBHOOK_URL,
    },
    timeout=30,
)
project_id = resp.json()["projectId"]
print(f"Submitted: {project_id}")
```

### Submit clip to Submagic for captioning (Python)
```python
import httpx, os

SUBMAGIC_KEY = os.environ["SUBMAGIC_KEY"]

resp = httpx.post(
    "https://api.submagic.co/v1/projects",
    headers={"x-api-key": SUBMAGIC_KEY, "Content-Type": "application/json"},
    json={
        "videoUrl": "https://cdn.weblyfe.nl/clips/clip_001.mp4",
        "language": "en",
        "template": "weblyfe-brand-v1",
        "webhookUrl": "https://appie.weblyfe.nl/hooks/submagic",
    },
    timeout=30,
)
print(resp.json())
```

---

## Cross-Skill References

- `video-editing-pro` — cut decisions, silence thresholds, pause tables; use for reviewing Vizard/Submagic output quality
- `viral-shorts-course` — hook formulas, retention benchmarks, platform-specific structure; use to evaluate which Vizard clips to publish
- `seo-pack` — once video is published, apply SEO to title/description/hashtags
- `fal-ai` — for custom B-roll generation (Nano Banana) to feed into the pipeline before Submagic
- Future: `content-factory-pipeline` — orchestration skill that stitches this skill + `viral-shorts-course` + `fal-ai` + IG/TikTok/YT publish APIs into one Appie-2 runbook

---

## Pricing Summary at 100 Videos/Month

| Stack | Monthly cost | Per-video cost | Notes |
|-------|-------------|---------------|-------|
| **Vizard Business + Submagic Business** | ~$85–90/mo | ~$0.89/video | Recommended. Both have APIs + webhooks. |
| **Vizard alone** | ~$20/mo | ~$0.20/video | No captions layer. Output needs Submagic or OSS captions. |
| **Submagic Business alone** | $69/mo | $0.69/video | Captions + music + B-roll. No clip extraction. |
| **Klap Pro+** | $151/mo | $1.51/video | API access included. More expensive. |
| **OSS (AI-YT-Shorts-Gen) + Submagic** | ~$69 + ~$10 API | ~$0.89/video | Self-hosted extraction. Requires Appie-3 infra. |
| **Descript Creator** | $24/mo | $0.24/video | Script-based only. No clip extraction. Best for podcast/interview. |
| **OpusClip Business** | Custom (contact sales) | Unknown | API closed beta. Avoid until open. |

**Bottom line:** Vizard + Submagic at ~$85–90/mo is the first integration. Run 30 days, measure quality vs the OSS hybrid. If output is good, scale. If cost matters more than convenience, migrate clip extraction to AI-Youtube-Shorts-Generator on Appie-3.
