"""Spark Atlas image-generation client.

Standard-library-only HTTP client for the spark-api FastAPI wrapper around ComfyUI.
Tailnet-only: requires routing to 100.69.197.43 and an X-API-Key in SPARK_API_KEY.

Example:
    from spark_client import spark_generate

    urls = spark_generate(
        prompt="luxury portrait of a confident woman, premium editorial",
        model="sdxl",
        style="cinematic",
    )
    print(urls[0])

Functions:
    spark_health()                          → dict   (no auth)
    spark_models()                          → dict   (no auth)
    spark_styles()                          → dict   (no auth)
    spark_generate(prompt, **kw)            → [str]  (X-API-Key required)
    spark_img2img(prompt, image_url, **kw)  → [str]  (X-API-Key required)
    spark_upscale(image_url, **kw)          → [str]  (X-API-Key required)
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

SPARK_BASE = os.environ.get("SPARK_BASE", "http://100.69.197.43:8190")
SPARK_API_KEY = os.environ.get("SPARK_API_KEY", "")
DEFAULT_POLL_INTERVAL = 2.0
DEFAULT_POLL_TIMEOUT = 300.0


class SparkError(Exception):
    """Spark API rejected the call or returned a non-2xx."""


class SparkTimeout(SparkError):
    """Job didn't reach a terminal state in time."""


def _http_json(method: str, path: str, *, body: dict | None = None, timeout: float = 30.0) -> dict[str, Any]:
    url = f"{SPARK_BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"} if body is not None else {}
    if SPARK_API_KEY:
        headers["X-API-Key"] = SPARK_API_KEY
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise SparkError(f"HTTP {e.code} on {method} {path}: {detail[:300]}") from None
    except urllib.error.URLError as e:
        raise SparkError(f"Network error on {method} {path}: {e.reason}") from None


# ---------------------------------------------------------------------------
# Read-only endpoints (no auth)
# ---------------------------------------------------------------------------


def spark_health(timeout: float = 5.0) -> dict[str, Any]:
    """Liveness + ComfyUI/connected status. Returns the raw /health payload."""
    return _http_json("GET", "/health", timeout=timeout)


def spark_system(timeout: float = 5.0) -> dict[str, Any]:
    """Diagnostics: uptime, output dir, available_models, total_generated."""
    return _http_json("GET", "/system", timeout=timeout)


def spark_models(timeout: float = 5.0) -> dict[str, Any]:
    """List installed checkpoints + the model_map aliases."""
    return _http_json("GET", "/models", timeout=timeout)


def spark_styles(timeout: float = 5.0) -> dict[str, Any]:
    """List the style presets."""
    return _http_json("GET", "/styles", timeout=timeout)


def spark_status(job_id: str, timeout: float = 5.0) -> dict[str, Any]:
    """Poll job status. Terminal states: completed, failed, error."""
    return _http_json("GET", f"/status/{job_id}", timeout=timeout)


def spark_output_url(stored_filename: str) -> str:
    """Absolute URL for downloading an output image."""
    return f"{SPARK_BASE}/output/{urllib.parse.quote(stored_filename)}"


# ---------------------------------------------------------------------------
# Mutating endpoints (require X-API-Key)
# ---------------------------------------------------------------------------


def _submit_and_wait(
    path: str,
    body: dict[str, Any],
    *,
    poll_interval: float = DEFAULT_POLL_INTERVAL,
    poll_timeout: float = DEFAULT_POLL_TIMEOUT,
) -> list[str]:
    """Submit a job, poll until terminal, return absolute image URLs.

    Raises SparkError on submission failure or terminal failure.
    Raises SparkTimeout if poll_timeout elapses without a terminal state.
    """
    if not SPARK_API_KEY:
        raise SparkError("SPARK_API_KEY env var is not set — cannot call mutating endpoints")

    job = _http_json("POST", path, body=body)
    job_id = job.get("job_id")
    if not job_id:
        raise SparkError(f"submit returned no job_id: {job!r}")

    deadline = time.monotonic() + poll_timeout
    while time.monotonic() < deadline:
        time.sleep(poll_interval)
        status = spark_status(job_id)
        state = status.get("status")
        if state == "completed":
            return [f"{SPARK_BASE}{u}" for u in status.get("image_urls", [])]
        if state in ("failed", "error"):
            raise SparkError(f"job {job_id} {state}: {status}")
    raise SparkTimeout(f"job {job_id} did not reach terminal state within {poll_timeout}s")


def spark_generate(
    prompt: str,
    *,
    model: str = "sdxl",
    style: str = "cinematic",
    negative_prompt: str = "",
    width: int = 1024,
    height: int = 1024,
    steps: int | None = None,
    cfg: float | None = None,
    sampler: str = "euler",
    scheduler: str = "normal",
    seed: int | None = None,
    poll_interval: float = DEFAULT_POLL_INTERVAL,
    poll_timeout: float = DEFAULT_POLL_TIMEOUT,
    **extra: Any,
) -> list[str]:
    """Text-to-image. Returns absolute image URLs.

    Model-aware defaults if steps/cfg unset:
      - flux_schnell: steps=4, cfg=1.0
      - sdxl:         steps=24, cfg=5.0
    """
    if steps is None:
        steps = 4 if model == "flux_schnell" else 24
    if cfg is None:
        cfg = 1.0 if model == "flux_schnell" else 5.0
    body: dict[str, Any] = {
        "prompt": prompt,
        "model": model,
        "style": style,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg": cfg,
        "sampler": sampler,
        "scheduler": scheduler,
    }
    if seed is not None:
        body["seed"] = seed
    body.update(extra)
    return _submit_and_wait("/generate", body, poll_interval=poll_interval, poll_timeout=poll_timeout)


def spark_img2img(
    prompt: str,
    image_url: str,
    *,
    model: str = "sdxl",
    style: str = "cinematic",
    denoise: float = 0.7,
    **kw: Any,
) -> list[str]:
    """Image-to-image. `image_url` is an existing /output/... URL or absolute URL Spark can fetch."""
    body: dict[str, Any] = {
        "prompt": prompt,
        "model": model,
        "style": style,
        "init_image": image_url,
        "denoise": denoise,
    }
    body.update(kw)
    poll_interval = kw.pop("poll_interval", DEFAULT_POLL_INTERVAL)
    poll_timeout = kw.pop("poll_timeout", DEFAULT_POLL_TIMEOUT)
    return _submit_and_wait("/img2img", body, poll_interval=poll_interval, poll_timeout=poll_timeout)


def spark_upscale(image_url: str, *, factor: float = 2.0, **kw: Any) -> list[str]:
    """Upscale an existing image."""
    body: dict[str, Any] = {"init_image": image_url, "factor": factor}
    body.update(kw)
    poll_interval = kw.pop("poll_interval", DEFAULT_POLL_INTERVAL)
    poll_timeout = kw.pop("poll_timeout", DEFAULT_POLL_TIMEOUT)
    return _submit_and_wait("/upscale", body, poll_interval=poll_interval, poll_timeout=poll_timeout)


# ---------------------------------------------------------------------------
# CLI for quick sanity checks
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Spark Atlas image generation client")
    p.add_argument("--health", action="store_true", help="ping /health and exit")
    p.add_argument("--models", action="store_true", help="list /models and exit")
    p.add_argument("--prompt", help="prompt to render")
    p.add_argument("--model", default="sdxl", choices=["sdxl", "flux_schnell"])
    p.add_argument("--style", default="cinematic")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--out", help="local path to download the result")
    args = p.parse_args()

    if args.health:
        print(json.dumps(spark_health(), indent=2))
        raise SystemExit(0)
    if args.models:
        print(json.dumps(spark_models(), indent=2))
        raise SystemExit(0)
    if args.prompt:
        urls = spark_generate(args.prompt, model=args.model, style=args.style, seed=args.seed)
        for u in urls:
            print(u)
        if args.out and urls:
            with urllib.request.urlopen(urls[0], timeout=60) as r, open(args.out, "wb") as f:
                f.write(r.read())
            print(f"saved → {args.out}")
        raise SystemExit(0)
    p.print_help()
