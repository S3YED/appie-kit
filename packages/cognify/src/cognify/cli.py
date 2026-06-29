"""Cognify CLI: ingest documents and run hybrid recall from the terminal."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import cognify
from cognify import config


def _cache_path(tenant: str) -> Path:
    import re
    d = config.DATA_DIR / "cache"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"ingest-{re.sub(r'[^a-zA-Z0-9_.-]', '_', tenant)}.json"


def cmd_ingest(a):
    be = cognify.get_backend(a.backend)
    text = sys.stdin.read() if a.path == "-" else a.path
    r = cognify.ingest(be, text, tenant=a.tenant, namespace=a.namespace, agent=a.agent,
                       is_path=(a.path != "-"), do_extract=not a.no_extract)
    print(json.dumps(r.__dict__, indent=2)); be.close()


def cmd_ingest_dir(a):
    be = cognify.get_backend(a.backend)
    files = sorted(p for p in Path(a.path).expanduser().glob(a.glob) if p.is_file())
    if a.limit:
        files = files[:a.limit]
    cache, cpath = {}, _cache_path(a.tenant)
    if a.cache and cpath.exists():
        try:
            cache = json.loads(cpath.read_text())
        except Exception:
            cache = {}
    print(f"ingesting {len(files)} files -> tenant={a.tenant} ns={a.namespace} "
          f"extract={not a.no_extract} cache={a.cache}", flush=True)
    tot = {"docs": 0, "chunks": 0, "entities": 0, "relations": 0, "failed": 0, "skipped": 0}
    t0 = time.time()
    for i, p in enumerate(files):
        if a.cache:
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            if cache.get(str(p)) == h:
                tot["skipped"] += 1
                continue
        try:
            r = cognify.ingest(be, str(p), tenant=a.tenant, namespace=a.namespace, agent=a.agent,
                               is_path=True, do_extract=not a.no_extract)
            tot["docs"] += 1; tot["chunks"] += r.chunks
            tot["entities"] += r.entities; tot["relations"] += r.relations
            if a.cache:
                cache[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
        except Exception as e:
            tot["failed"] += 1
            print(f"  [FAIL] {p.name}: {e}", flush=True)
        if (i + 1) % 10 == 0:
            print(f"  {i+1}/{len(files)} | {tot['chunks']}c {tot['entities']}e "
                  f"{tot['relations']}r ({time.time()-t0:.0f}s)", flush=True)
    if a.cache:
        cpath.write_text(json.dumps(cache, indent=2))
    tot["seconds"] = round(time.time() - t0, 1)
    print("DONE:", json.dumps(tot, indent=2)); be.close()


def cmd_recall(a):
    be = cognify.get_backend(a.backend)
    res = cognify.recall(be, a.query, tenant=a.tenant, namespace=a.namespace, k=a.k)
    print(json.dumps({
        "query": res.query, "tenant": res.tenant,
        "chunks": [{"score": c["score"], "heading": c.get("heading"), "text": c["text"][:200]}
                   for c in res.chunks],
        "entities": [f"{e['name']} ({e['etype']})" for e in res.entities],
        "relations": [f"{r['subject']} -{r['predicate']}-> {r['object']}" for r in res.relations],
    }, indent=2, ensure_ascii=False)); be.close()


def cmd_stats(a):
    be = cognify.get_backend(a.backend)
    print(json.dumps(be.stats(tenant=a.tenant), indent=2)); be.close()


def main():
    p = argparse.ArgumentParser(prog="cognify")
    p.add_argument("--backend", default=None, choices=["neo4j", "local"])
    p.add_argument("--tenant", default="default")
    p.add_argument("--namespace", default="default")
    p.add_argument("--agent", default="agent")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("ingest"); s.add_argument("path"); s.add_argument("--no-extract", action="store_true"); s.set_defaults(fn=cmd_ingest)
    s = sub.add_parser("ingest-dir"); s.add_argument("path"); s.add_argument("--glob", default="**/*.md"); s.add_argument("--limit", type=int, default=0); s.add_argument("--no-extract", action="store_true"); s.add_argument("--cache", action="store_true"); s.set_defaults(fn=cmd_ingest_dir)
    s = sub.add_parser("recall"); s.add_argument("query"); s.add_argument("-k", type=int, default=8); s.set_defaults(fn=cmd_recall)
    s = sub.add_parser("stats"); s.set_defaults(fn=cmd_stats)
    a = p.parse_args(); a.fn(a)


if __name__ == "__main__":
    main()
