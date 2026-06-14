#!/usr/bin/env python3
"""Validate the public Appie Kit skill tree before publishing.

Checks:
- production SKILL.md count and per-category counts
- unique frontmatter names
- non-empty frontmatter descriptions
- suspicious private operational patterns

This is intentionally conservative. If it flags a false positive, either
replace the text with a placeholder or add a narrow, documented exception in
this script.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
SKIP_PARTS = {"references", "scripts", "assets", "node_modules", "_quarantine", ".git"}
EXPECTED_CATEGORIES = {
    "automation",
    "communication",
    "content",
    "ecc",
    "integrations",
    "knowledge",
    "meta",
    "ops",
    "personal",
}

PRIVATE_PATTERNS = [
    ("tailscale_ip", re.compile(r"\b100\.(?:\d{1,3}\.){2}\d{1,3}\b")),
    ("tailscale_magic_dns", re.compile(r"\btail[0-9a-z]+\.ts\.net\b", re.I)),
    ("absolute_private_home", re.compile(r"/(?:Users|home)/appie\b")),
    ("telegram_token", re.compile(r"\b\d{6,}:[A-Za-z0-9_-]{20,}\b")),
    ("openai_like_secret", re.compile(r"\bsk-(?!xxx|no-|bod)[A-Za-z0-9][A-Za-z0-9_\-]{16,}\b")),
    ("github_secret", re.compile(r"\b(?:ghp|gho|github_pat)_[A-Za-z0-9_]{16,}\b")),
    ("slack_secret", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{16,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
]

ALLOWLIST_SUBSTRINGS = {
    "configs/fleet-access.example.yml",  # public placeholder template for private fleet access
    "docs/FLEET-ACCESS.md",              # public placeholder guide for private fleet access
}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def is_production_skill(path: Path) -> bool:
    rel_parts = path.relative_to(ROOT).parts
    return not any(part in SKIP_PARTS for part in rel_parts)


def main() -> int:
    skill_files = sorted(p for p in SKILLS.rglob("SKILL.md") if is_production_skill(p))
    category_counts: Counter[str] = Counter()
    names: defaultdict[str, list[str]] = defaultdict(list)
    missing: list[str] = []

    for skill_file in skill_files:
        rel = skill_file.relative_to(ROOT)
        parts = rel.parts
        if len(parts) < 4:
            missing.append(f"{rel}: expected skills/<category>/<skill>/SKILL.md")
            continue
        category_counts[parts[1]] += 1
        fm = parse_frontmatter(skill_file.read_text(errors="ignore"))
        name = fm.get("name", "").strip()
        desc = fm.get("description", "").strip()
        if not name or not desc:
            missing.append(f"{rel}: missing name or description")
        names[name or f"<missing:{rel}>"].append(str(rel))

    duplicates = {name: paths for name, paths in names.items() if len(paths) > 1}
    unknown_categories = set(category_counts) - EXPECTED_CATEGORIES
    missing_categories = EXPECTED_CATEGORIES - set(category_counts)

    findings: list[dict[str, str]] = []
    scan_paths = [
        p
        for p in ROOT.rglob("*")
        if p.is_file() and ".git" not in p.parts and "mailing" not in p.parts and "memory" not in p.parts
    ]
    for path in scan_paths:
        rel = str(path.relative_to(ROOT))
        if any(rel.startswith(prefix) for prefix in ALLOWLIST_SUBSTRINGS):
            continue
        if (
            path.suffix.lower()
            not in {".md", ".yml", ".yaml", ".json", ".js", ".ts", ".py", ".sh", ".txt", ".example"}
            and path.name != ".env.example"
        ):
            continue
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        for label, pattern in PRIVATE_PATTERNS:
            for match in pattern.finditer(text):
                value = match.group(0)
                if "<" in value or "your" in value.lower():
                    continue
                findings.append({"file": rel, "type": label, "match": value[:80]})

    result = {
        "production_skill_files": len(skill_files),
        "category_counts": dict(sorted(category_counts.items())),
        "unique_skill_names": len(names),
        "duplicate_skill_names": duplicates,
        "missing_frontmatter_or_description": missing,
        "unknown_categories": sorted(unknown_categories),
        "missing_categories": sorted(missing_categories),
        "private_pattern_findings": findings,
    }
    print(json.dumps(result, indent=2, sort_keys=True))

    failed = bool(duplicates or missing or unknown_categories or missing_categories or findings)
    if failed:
        print("FAIL: public skill validation found issues", file=sys.stderr)
        return 1
    print("PASS: public skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
