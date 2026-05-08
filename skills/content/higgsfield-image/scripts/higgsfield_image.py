#!/usr/bin/env python3
"""
Higgsfield Nano Banana Pro Image Generator
Wraps mcporter MCP calls for easy image generation

Usage:
    python3 higgsfield_image.py "prompt" [--ref URL] [--aspect 4:5] [--resolution 4k] [--out filename]
"""

import json
import os
import subprocess
import sys
import time
import uuid
import requests
from pathlib import Path

# Constants
MODEL = "nano_banana_2"
OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "media"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHARACTER_PHOTO_PROMPT = (
    "The image must look like it was captured with a high-end DSLR fashion camera "
    "using an 85mm lens, with natural depth of field, realistic light diffusion, and "
    "authentic photographic detail. The result must be extremely photorealistic, "
    "studio-quality fashion photography in ultra 4K resolution, indistinguishable from a "
    "real camera photograph, with no AI artifacts or synthetic appearance. Maintain "
    "true-to-life skin texture, natural wrinkles, pores, and realistic lighting reflections. "
    "No beauty filters, no artificial smoothing."
)


def run_mcporter(command: list) -> dict:
    """Run a mcporter command and return parsed JSON."""
    result = subprocess.run(
        ["mcporter"] + command,
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode != 0:
        raise Exception(f"mcporter error: {result.stderr}")
    return json.loads(result.stdout)


def generate(
    prompt: str,
    ref_url: str = None,
    aspect_ratio: str = "4:5",
    resolution: str = "4k",
    count: int = 1,
    wait: bool = True,
    poll_interval: int = 30,
    poll_timeout: int = 300,
) -> list:
    """
    Generate image(s) via Higgsfield Nano Banana Pro.

    Args:
        prompt: Image description
        ref_url: Optional reference image URL for character consistency
        aspect_ratio: Aspect ratio (1:1, 4:5, 2:3, etc.)
        resolution: 1k, 2k, or 4k
        count: Number of images to generate (1-4)
        wait: Whether to wait for completion
        poll_interval: Seconds between status checks
        poll_timeout: Max seconds to wait

    Returns:
        List of dicts with {id, status, url}
    """
    # Build medias array
    medias = []
    if ref_url:
        medias.append({"value": ref_url, "role": "image"})

    # Build params
    params = {
        "model": MODEL,
        "prompt": f"{CHARACTER_PHOTO_PROMPT}\n\n{prompt}",
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "count": count,
    }
    if medias:
        params["medias"] = medias

    # Submit generation
    args_json = json.dumps({"params": params})
    cmd = ["call", "higgsfield.generate_image", "--args", args_json]
    result = run_mcporter(cmd)
    
    jobs = result.get("results", [])
    print(f"Submitted {len(jobs)} job(s): {[j['id'] for j in jobs]}")

    if not wait:
        return jobs

    # Poll for completion
    completed = []
    start_time = time.time()
    
    while jobs:
        elapsed = time.time() - start_time
        if elapsed > poll_timeout:
            raise TimeoutError(f"Timeout after {poll_timeout}s waiting for generation")

        time.sleep(poll_interval)
        
        # Check status of our jobs
        gen_result = run_mcporter(["call", "higgsfield.show_generations", "type=image", "size=20"])
        items = gen_result.get("items", [])
        
        job_ids = {j["id"] for j in jobs if j["id"] not in [c["id"] for c in completed]}
        
        for item in items:
            if item["id"] in job_ids:
                status = item["status"]
                print(f"  Job {item['id'][:8]}: {status}")
                
                if status == "completed":
                    url = item.get("results", {}).get("rawUrl", "")
                    completed.append({"id": item["id"], "status": status, "url": url})
                    jobs = [j for j in jobs if j["id"] != item["id"]]
                elif status == "failed":
                    completed.append({"id": item["id"], "status": "failed", "error": "generation failed"})
                    jobs = [j for j in jobs if j["id"] != item["id"]]

    return completed


def download_image(url: str, output_path: str = None) -> str:
    """Download image from URL to file."""
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    
    if not output_path:
        ext = "png" if ".png" in url else "jpg"
        output_path = OUTPUT_DIR / f"hf_{uuid.uuid4().hex[:8]}.{ext}"
    else:
        output_path = Path(output_path)
    
    with open(output_path, "wb") as f:
        f.write(response.content)
    
    return str(output_path)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate images with Higgsfield Nano Banana Pro")
    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument("--ref", dest="ref_url", help="Reference image URL for character consistency")
    parser.add_argument("--aspect", default="4:5", help="Aspect ratio (default: 4:5)")
    parser.add_argument("--resolution", default="4k", help="Resolution: 1k, 2k, 4k (default: 4k)")
    parser.add_argument("--count", type=int, default=1, help="Number of images (1-4, default: 1)")
    parser.add_argument("--out", dest="output", help="Output filename")
    parser.add_argument("--no-wait", action="store_true", help="Don't wait for completion")
    parser.add_argument("--download", action="store_true", default=True, help="Download when complete (default: True)")
    
    args = parser.parse_args()

    print(f"🎨 Generating with {MODEL}...")
    if args.ref_url:
        print(f"   Reference: {args.ref_url}")
    print(f"   Aspect: {args.aspect} | Resolution: {args.resolution}")

    try:
        results = generate(
            prompt=args.prompt,
            ref_url=args.ref_url,
            aspect_ratio=args.aspect,
            resolution=args.resolution,
            count=args.count,
            wait=not args.no_wait,
        )
        
        print("\n✅ Results:")
        for r in results:
            print(f"  {r['id']}: {r['status']}")
            if r.get("url"):
                print(f"    URL: {r['url']}")
                
                if args.download:
                    path = download_image(r["url"], args.output)
                    print(f"    Saved: {path}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
