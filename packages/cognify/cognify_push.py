#!/usr/bin/env python3
"""
cognify_push — universal, dependency-free auto-ingest client for fleet agents.

Stdlib only (urllib + json + hashlib): runs on ANY box with python3, no pip
install. Walks an agent's workspace, and for every new/changed document POSTs it
to the shared Cognify brain over Tailscale. Heavy lifting (chunk + LLM extraction
+ embed + graph) happens on the endpoint, so agent boxes stay light.

Each agent's data lands under its own namespace (workspace:<agent>) in the shared
fleet graph, so it connects to everything else but stays attributable.

Usage (cron-friendly):
  cognify_push.py --agent appie-2 --workspace ~/.hermes/memory \
                  --endpoint http://100.101.29.56:8765

Run every N minutes from cron / a Hermes scheduled task to auto-ingest new data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

CACHE = Path(os.path.expanduser("~/.cognify/push-cache.json"))


def _load_cache() -> dict:
    try:
        return json.loads(CACHE.read_text())
    except Exception:
        return {}


def _save_cache(c: dict) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(c))


def _post(endpoint: str, payload: dict, timeout: int = 120) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(endpoint.rstrip("/") + "/cognify/ingest", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True)
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--endpoint", default="http://100.101.29.56:8765")
    ap.add_argument("--glob", default="**/*.md")
    ap.add_argument("--min-chars", type=int, default=200)
    ap.add_argument("--max-files", type=int, default=0)
    a = ap.parse_args()

    ws = Path(os.path.expanduser(a.workspace))
    if not ws.exists():
        print(f"workspace not found: {ws}", file=sys.stderr)
        sys.exit(1)
    ns = f"workspace:{a.agent}"
    cache = _load_cache()
    files = sorted(p for p in ws.glob(a.glob) if p.is_file())
    if a.max_files:
        files = files[: a.max_files]

    pushed = skipped = failed = 0
    for p in files:
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        if len(text) < a.min_chars:
            continue
        key = str(p)
        h = hashlib.sha256(text.encode()).hexdigest()
        if cache.get(key) == h:
            skipped += 1
            continue
        try:
            _post(a.endpoint, {"text": text, "title": p.name, "tenant": "fleet",
                               "namespace": ns, "agent": a.agent})
            cache[key] = h
            _save_cache(cache)  # persist per-file so interruptions keep progress
            pushed += 1
        except Exception as e:
            failed += 1
            print(f"  [FAIL] {p.name}: {str(e)[:80]}", file=sys.stderr)

    print(json.dumps({"agent": a.agent, "namespace": ns, "pushed": pushed,
                      "skipped": skipped, "failed": failed, "files": len(files)}))


if __name__ == "__main__":
    main()
