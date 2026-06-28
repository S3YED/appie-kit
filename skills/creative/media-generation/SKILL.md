---
name: media-generation
title: AI Media Generation (Image/Video/Audio APIs)
description: Generate images, video, and talking-head animations via fal.ai and similar APIs. Covers sync-3 lipsync, cost estimation, async queue management, request recovery, and file delivery.
trigger: User asks to create a video from photo+audio, animate an image, generate talking-head content, use sync-lipsync, use fal.ai models, or any media generation workflow with paid APIs.
---

# AI Media Generation (fal.ai & Similar APIs)

## When to Use

- User wants to create a talking-head video from a photo + audio
- User asks for image-to-video, lipsync, or face animation
- Any paid API media generation task (fal.ai, etc.)
- Uploading/serving generated media files

## Principles

### Always Estimate Costs Before Running

**NEVER fire a paid API call without estimating the cost first.** This is the #1 rule from Seyed after the $16 fugu-sync3 incident.

```python
# Sync-3 v3 image-to-video: $0.1333 per output second
# 71s audio = 71 × $0.1333 = ~$9.46
```

Cost estimation checklist:
1. Look up the model's pricing (per-second, per-video, per-image)
2. Calculate: `duration × unit_price = estimated_cost`
3. Present to user with balance/remaining info
4. Only proceed after user confirms

### Bulletproof Async Workflow (fal.ai)

The **correct** sequence for long-running fal.ai jobs is:

```
1. submit() → get SyncRequestHandle
2. IMMEDIATELY save handle.request_id to disk ← CARDINAL RULE
3. Poll via REST API (GET) until Completed
4. Download result video
5. Compress if needed (Telegram 50MB limit)
6. Clean up temp files
```

**NEVER use `subscribe()`** — it blocks until completion with no request_id fallback. If the client disconnects mid-processing, the result is unrecoverable and credits are wasted.

### Request ID Recovery

Even with proper save, if the polling process dies:
- The saved request_id lets you recover via REST API
- Use GET on `https://queue.fal.run/fal-ai/{app}/requests/{request_id}`
- This returns the full result JSON including video URL
- The `from_request_id()` method in fal-client requires an `httpx.Client` instance (internal) — use raw REST API instead

## Supported Models & Pricing

### fal.ai — sync-3 Lipsync

| Model | Endpoint | Pricing | Notes |
|-------|----------|---------|-------|
| sync-3 image-to-video | `fal-ai/sync-lipsync/v3/image-to-video` | **$0.1333/sec** output | Photo + audio → talking video |
| sync-3 video-to-video | `fal-ai/sync-lipsync/v3` | ~$0.13/sec | Existing video + new audio |

**Input:** `{"image_url": "...", "audio_url": "..."}` (image-to-video variant needs `image_url`, NOT `face_image_url`)

**Output format:** MP4. Result lives at `https://v3b.fal.media/...` URLs valid ~14 days.

### Arbitrary fal.ai Models

All models follow the same queue/submit/workflow pattern. Generic workflow:

```python
from fal_client import submit

handle = submit("fal-ai/{owner}/{model}", arguments={...})
request_id = handle.request_id
# Save request_id immediately!
# Poll via GET https://queue.fal.run/fal-ai/{owner}/{model}/requests/{request_id}
```

## fal.ai File Upload

Use the `upload_file()` function from `fal_client`:

```python
from fal_client import upload_file
file_url = upload_file("/path/to/file.jpg")
# Returns: https://v3b.fal.media/files/...
```

The returned URL is immediately usable in model arguments.

## Polling Pattern

**Key learning:** the status endpoint returns 405 for GET and works with POST. But the result endpoint works with GET:

```bash
# Check status (POST)
curl -X POST "https://queue.fal.run/fal-ai/{app}/requests/{id}/status" \
  -H "Authorization: Key $FAL_KEY"

# Get completed result (GET)
curl "https://queue.fal.run/fal-ai/{app}/requests/{id}" \
  -H "Authorization: Key $FAL_KEY"
```

**Important:** The `{app}` in the queue URL may differ from the submit app name.
- Submit uses: `fal-ai/sync-lipsync/v3/image-to-video`
- Queue URL uses: `fal-ai/sync-lipsync` (without the `/v3/image-to-video` suffix)

Always check the `response_url`/`status_url` from the initial submit response to get the exact queue URL pattern.

## File Delivery

### Telegram Delivery

Telegram has a **50MB file size limit** for bots. Compress with ffmpeg:

```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -crf 28 -preset fast \
  -c:a aac -b:a 64k \
  -movflags +faststart \
  output-compressed.mp4
```

Typical compression: 136MB → ~5.8MB (CRF 28, 71s video). For Telegram delivery, use the MEDIA: prefix.

### Google Drive Upload

Requires OAuth setup (rclone or gdrive). The most direct alternative is giving the user the raw fal.ai storage URL (valid ~14 days).

## Scripts

### Reference: bulletproof-submit.py

A template script for bulletproof fal.ai job submission. Create and modify per task:

```python
import os, json, time
from fal_client import submit

RID_FILE = "/path/to/request-id.txt"

# Submit
handle = submit("fal-ai/{model}", arguments={...})
rid = handle.request_id
with open(RID_FILE, "w") as f: f.write(rid)
print(f"Request ID: {rid}")

# Poll via REST (more reliable than status())
REST_URL = f"https://queue.fal.run/fal-ai/{app}/requests/{rid}"
while True:
    # Use curl or requests here
    # Check if COMPLETED
    # If yes: download video, compress, deliver
    time.sleep(10)
```

## References

### Session Learnings (2026-06-23 fugu-sync3)

The fugu-sync3 session produced these verified facts:
- sync-3 v3 image-to-video expects `image_url` (NOT `face_image_url`) + `audio_url`
- The correct model path: `fal-ai/sync-lipsync/v3/image-to-video`
- Pricing is $0.1333 per output second, shown on the model page as "Your request will cost $X.XX per output second"
- A 71s video at 30fps generates ~136MB H.264 original, compressible to ~5.8MB at CRF 28
- Queue polling pattern: POST to status endpoint, GET to result endpoint
- The fal.ai SDK `from_request_id()` needs an httpx.Client instance (not a simple public method) — use REST API for recovery instead
- Video URLs from fal.ai storage are valid for ~14 days
- Request results expire after approximately 10+ minutes of inactivity — save the video URL immediately

## Pitfalls

- **$16 wasted on first attempt** — Using `subscribe()` without request_id fallback made the result unrecoverable when the client timed out.
- **405 errors on status endpoint** — The status endpoint uses POST, not GET. The result endpoint uses GET, not POST.
- **Queue URL vs Submit URL difference** — The queue URL may strip subpaths. Check response URLs from the submit call.
- **No charge for server errors** — fal.ai doesn't charge for 503/504/timeout errors during queue wait, but DOES charge for completed processing even if the client disconnects.
- **Request ID expiration** — Completed request results expire after some time (observed: a 10-minute-old request ID was gone). Save the result URL, not just the request ID.
- **Always save request_id to disk** before doing anything else. If the script crashes at any point, the request_id is the only way to recover the result.
