#!/usr/bin/env python3
"""Memory search script for Hermes Agent.

Searches across all memory files (daily logs, topics, projects, decisions)
with ranked results based on relevance.

Usage:
    python3 search.py "query" [--limit 10] [--recent 7] [--files-only]
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

MEMORY_DIR = Path.home() / ".hermes" / "memory"
BRAIN_FILES = [
    Path.home() / ".hermes" / "MEMORY.md",
    Path.home() / ".hermes" / "USER.md",
    Path.home() / ".hermes" / "TOOLS.md",
    Path.home() / ".hermes" / "IDENTITY.md",
]


def search_file(filepath: Path, query: str, terms: list[str]) -> list[dict]:
    """Search a single file for query terms. Returns matches with context."""
    results = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")
    except Exception:
        return []

    query_lower = query.lower()
    # Score: exact phrase match > all terms present > partial matches
    content_lower = content.lower()

    if query_lower not in content_lower and not any(t in content_lower for t in terms):
        return []

    # Find matching lines with context
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(t in line_lower for t in terms):
            start = max(0, i - 2)
            end = min(len(lines), i + 3)
            context = "\n".join(lines[start:end])

            # Score calculation
            score = 0
            if query_lower in line_lower:
                score += 10  # exact phrase
            score += sum(2 for t in terms if t in line_lower)

            results.append({
                "file": str(filepath),
                "line": i + 1,
                "score": score,
                "context": context,
            })

    # Deduplicate overlapping contexts
    if results:
        deduped = [results[0]]
        for r in results[1:]:
            if r["line"] - deduped[-1]["line"] > 5:
                deduped.append(r)
            elif r["score"] > deduped[-1]["score"]:
                deduped[-1] = r
        results = deduped

    return results


def collect_files(recent_days: int = 0) -> list[Path]:
    """Collect all searchable memory files."""
    files = []

    # Brain files
    for bf in BRAIN_FILES:
        if bf.exists():
            files.append(bf)

    if not MEMORY_DIR.exists():
        return files

    # Walk memory directory
    cutoff = None
    if recent_days > 0:
        cutoff = datetime.now() - timedelta(days=recent_days)

    for root, dirs, filenames in os.walk(MEMORY_DIR):
        for fn in filenames:
            if not fn.endswith(".md") and not fn.endswith(".json"):
                continue
            fp = Path(root) / fn
            if cutoff:
                # Filter by date in filename if possible
                date_match = re.match(r"(\d{4}-\d{2}-\d{2})", fn)
                if date_match:
                    try:
                        file_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
                        if file_date < cutoff:
                            continue
                    except ValueError:
                        pass
            files.append(fp)

    return files


def main():
    parser = argparse.ArgumentParser(description="Search Appie brain memory files")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Max results to show")
    parser.add_argument("--recent", type=int, default=0, help="Only search last N days")
    parser.add_argument("--files-only", action="store_true", help="Only show matching filenames")
    args = parser.parse_args()

    terms = [t.lower() for t in args.query.split() if len(t) > 1]
    files = collect_files(args.recent)

    if not files:
        print("No memory files found.")
        sys.exit(1)

    all_results = []
    matching_files = set()

    for fp in files:
        matches = search_file(fp, args.query, terms)
        if matches:
            matching_files.add(str(fp))
            all_results.extend(matches)

    if args.files_only:
        for f in sorted(matching_files):
            rel = str(f).replace(str(Path.home()), "~")
            print(rel)
        print(f"\n{len(matching_files)} file(s) matched.")
        return

    # Sort by score descending
    all_results.sort(key=lambda x: x["score"], reverse=True)

    if not all_results:
        print(f"No results found for: {args.query}")
        print(f"Searched {len(files)} files.")
        sys.exit(0)

    print(f"Found {len(all_results)} match(es) in {len(matching_files)} file(s):\n")

    for r in all_results[: args.limit]:
        rel_path = str(r["file"]).replace(str(Path.home()), "~")
        print(f"--- {rel_path}:{r['line']} (score: {r['score']}) ---")
        print(r["context"])
        print()


if __name__ == "__main__":
    main()
