---
name: fal-ai-media
title: Fal.ai Media Generation (Sync Lipsync, Image-to-Video)
description: Generate talking-head videos, lipsync animations, and image-to-video media via fal.ai models. Covers file upload, model selection, and common pitfalls.
trigger: User asks to create a talking head video, animate a photo with audio, sync lips to audio, generate a video from an image, use fal.ai for media generation, or 'make this photo speak'.
---

# Fal.ai Media Generation

Fal.ai provides GPU-backed AI inference for generative media. This skill covers the **Sync Lipsync (sync-3)** image-to-video and video-to-video pipelines, and the general fal.ai upload + run pattern.

## Authentication

```bash
# Store in ~/.hermes/.env
export FAL_KEY="<your-api-key>"

# Format: a 36-char UUID, colon, then a 32-hex-char secret
# Example: 5136e6b5-aa91-4b0f-b77c-5ba08944bc48:0d30a9ba4385b238d52f9185deac29e7
```

Install the Python client:

```bash
pip install fal-client
```

## Upload Files to Fal Storage

Fal has built-in file storage. Upload before running any model:

```python
from fal_client import upload_file

image_url = upload_file("/path/to/image.jpg")
audio_url = upload_file("/path/to/audio.mp3")
```

Files get a `https://v3b.fal.media/files/...` URL that is accessible to fal models for ~24 hours.

## Sync-3 Image-to-Video (Photo + Audio → Talking Head)

Best model for turning a static photo with a face into a talking video with lip-sync.

**Model ID:** `fal-ai/sync-lipsync/v3/image-to-video`

**Required inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `image_url` | string | URL of photo with a face (JPEG, PNG, WebP) |
| `audio_url` | string | URL of audio for lip-sync |

**NOT** `face_image_url` (that's for the video-to-video variant). Use `image_url`.

### Python (synchronous):

```python
from fal_client import run
import os

os.environ['FAL_KEY'] = '***'

result = run(
    "fal-ai/sync-lipsync/v3/image-to-video",
    arguments={
        "image_url": "https://...",
        "audio_url": "https://..."
    },
    timeout=300  # 71s audio can take 5-10 min
)

video_url = result.get('video', {}).get('url', '')
```

### Python (with progress updates):

```python
from fal_client import subscribe
import time

start = time.time()

def on_queue_update(update):
    status = type(update).__name__
    pos = getattr(update, 'position', '')
    elapsed = time.time() - start
    print(f"[{elapsed:.0f}s] {status}" + (f" — positie {pos}" if pos else ""))

result = subscribe(
    "fal-ai/sync-lipsync/v3/image-to-video",
    arguments={
        "image_url": img_url,
        "audio_url": audio_url
    },
    on_queue_update=on_queue_update
)
```

### Via curl:

```bash
curl -X POST https://fal.run/fal-ai/sync-lipsync/v3/image-to-video \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://...",
    "audio_url": "https://..."
  }'
```

## Sync-3 Video-to-Video (Existing Video + New Audio → Re-sync)

When you already have a video but want to re-sync the lips to different audio.

**Model ID:** `fal-ai/sync-lipsync/v3` (or `fal-ai/sync-lipsync` for v2)

**Required inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `video_url` | string | URL of input video with a talking face |
| `audio_url` | string | URL of new audio to sync to |

## Response Shape

The response is a dict. The video URL is typically nested:

```python
video_url = result.get('video', {}).get('url', '')
# Or sometimes:
video_url = result.get('url', '') or result.get('video_url', '')
```

## Processing Times

| Audio Length | Approx. Processing |
|-------------|-------------------|
| 10-30s | 1-3 min |
| 60-90s | 5-10+ min |

Long audio can time out synchronous calls. For audio >30s, use `subscribe()` with a progress callback or run asynchronously.

## Pitfalls

- **`image_url` vs `face_image_url`** — The image-to-video variant uses `image_url`. Using `face_image_url` (the video-to-video param name) returns a 422 validation error.
- **Timeout on long audio** — The default CLI timeout (180s) is too short for 60s+ audio. Set `timeout=600` or use `subscribe()`.
- **The photo needs a visible face** — If the image has no clear face or is heavily stylized, the model may hang in InProgress indefinitely or produce a garbled result.
- **fal.ai website is Next.js** — The `fal.ai/storage` URL is a web page, not an upload API. Use the Python client's `upload_file()` instead.
- **Result URL is nested** — Don't assume `result['url']`. Check `result['video']['url']` first.
- **403 on first run** — You need credits on your account. Check credits at `https://fal.ai/dashboard`.

## Related Models on Fal

| Model | ID | Use Case |
|-------|-----|----------|
| sync-3 image-to-video | `fal-ai/sync-lipsync/v3/image-to-video` | Photo + audio → talking head |
| sync-3 video-to-video | `fal-ai/sync-lipsync/v3` | Video + new audio → re-sync |
| sync v2 video-to-video | `fal-ai/sync-lipsync` | Older version, smaller context |
| Kling | `fal-ai/kling*` | General text/image-to-video |
| LivePortrait | `fal-ai/live-portrait*` | Face animation from driving video |
