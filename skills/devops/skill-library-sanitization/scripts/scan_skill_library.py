#!/usr/bin/env python3
"""Scan a skill library for inventory, duplicate names, and likely leaks.

This scanner is intentionally conservative and masks findings. It is not a
replacement for gitleaks/trufflehog, but catches private operational details
that generic secret scanners often miss.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

ALLOWED_SUPPORT_DIRS = {"references", "scripts", "templates", "assets"}
TEXT_EXTS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".py", ".sh", ".bash",
    ".js", ".ts", ".tsx", ".jsx", ".env", ".example", ".csv", ".xml", ".html", ".css"
}
SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__", ".next", "dist", "build"}

PATTERNS: list[tuple[str, str, str]] = [
    ("private_key", "critical", r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |)?PRIVATE KEY-----"),
    ("openai_like_key", "critical", r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    ("github_token", "critical", r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    ("aws_access_key", "critical", r"\bAKIA[0-9A-Z]{16}\b"),
    ("google_api_key", "critical", r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    ("slack_token", "critical", r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    ("generic_secret_assignment", "high", r"(?i)\b(api[_-]?key|secret|token|password|cookie|authorization)\b\s*[:=]\s*['\"]?[A-Za-z0-9_./+=:-]{16,}"),
    ("bearer_token", "high", r"(?i)Authorization:\s*Bearer\s+[A-Za-z0-9_./+=:-]{16,}"),
    ("signed_url", "high", r"https?://[^\s)\]>'\"]+[?&](?:X-Amz-Signature|sig|signature|token|access_token)=[^\s)\]>'\"]+"),
    ("notion_id", "medium", r"\b[0-9a-f]{32}\b"),
    ("uuid", "low", r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    ("private_ip", "medium", r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[0-1])|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7]))\.\d{1,3}\.\d{1,3}\b"),
    ("local_absolute_path", "medium", r"(?:/Users|/home|/root)/[A-Za-z0-9._-]+/[A-Za-z0-9._~/-]+"),
    ("ssh_private_path", "high", r"(?:/Users|/home|/root)/[A-Za-z0-9._-]+/\.ssh/[A-Za-z0-9._-]+"),
    ("destructive_command", "medium", r"\b(?:rm\s+-rf\s+(?:/|~|\$HOME|\*)|git\s+reset\s+--hard|git\s+push\s+--force|docker\s+system\s+prune\s+-a)\b"),
]


def is_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTS or path.name in {"SKILL.md", ".env.example"}:
        return True
    try:
        data = path.read_bytes()[:4096]
    except OSError:
        return False
    return b"\0" not in data


def mask(s: str) -> str:
    s = s.strip().replace("\n", " ")
    if len(s) <= 12:
        return "<redacted>"
    digest = hashlib.sha256(s.encode()).hexdigest()[:8]
    return f"{s[:4]}...{s[-4:]}#{digest}"


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            p = Path(dirpath) / filename
            yield p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", help="Skill tree or repo root to scan")
    ap.add_argument("--json-out", help="Write full JSON report to path")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    skill_files = sorted(root.rglob("SKILL.md"))
    skills: list[dict[str, Any]] = []
    name_to_paths: dict[str, list[str]] = {}

    for sf in skill_files:
        text = sf.read_text(errors="replace")
        fm = parse_frontmatter(text)
        name = fm.get("name", "")
        desc = fm.get("description", "")
        rel = str(sf.relative_to(root))
        skills.append({"path": rel, "name": name, "description_present": bool(desc)})
        if name:
            name_to_paths.setdefault(name, []).append(rel)

    findings: list[dict[str, Any]] = []
    support_issues: list[dict[str, str]] = []
    regexes = [(name, sev, re.compile(pattern)) for name, sev, pattern in PATTERNS]

    for p in iter_files(root):
        if not p.is_file() or not is_text(p):
            continue
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        rel = str(p.relative_to(root))
        for line_no, line in enumerate(text.splitlines(), 1):
            for kind, severity, rx in regexes:
                for m in rx.finditer(line):
                    findings.append({
                        "file": rel,
                        "line": line_no,
                        "kind": kind,
                        "severity": severity,
                        "match": mask(m.group(0)),
                    })

    for sf in skill_files:
        skill_dir = sf.parent
        for child in skill_dir.iterdir():
            if child.name == "SKILL.md" or child.name.startswith("."):
                continue
            if child.is_dir() and child.name not in ALLOWED_SUPPORT_DIRS:
                support_issues.append({"skill": str(sf.relative_to(root)), "path": str(child.relative_to(root)), "issue": "unsupported support directory"})
            elif child.is_file():
                support_issues.append({"skill": str(sf.relative_to(root)), "path": str(child.relative_to(root)), "issue": "support file outside allowed dirs"})

    duplicates = {n: ps for n, ps in name_to_paths.items() if len(ps) > 1}
    missing_frontmatter = [s for s in skills if not s["name"] or not s["description_present"]]
    high_findings = [f for f in findings if f["severity"] in {"critical", "high"}]

    report = {
        "root": str(root),
        "skill_count": len(skills),
        "duplicate_names": duplicates,
        "missing_frontmatter_or_description": missing_frontmatter,
        "support_issues": support_issues,
        "finding_count": len(findings),
        "high_or_critical_count": len(high_findings),
        "findings": findings,
    }

    if args.json_out:
        Path(args.json_out).expanduser().write_text(json.dumps(report, indent=2))

    print(f"root: {root}")
    print(f"skills: {len(skills)}")
    print(f"duplicate_names: {len(duplicates)}")
    print(f"missing_frontmatter_or_description: {len(missing_frontmatter)}")
    print(f"support_issues: {len(support_issues)}")
    print(f"findings: {len(findings)}")
    print(f"high_or_critical_findings: {len(high_findings)}")
    if findings:
        print("sample_findings_masked:")
        for f in findings[:25]:
            print(f"- {f['severity']} {f['kind']} {f['file']}:{f['line']} {f['match']}")
    return 2 if high_findings or duplicates or missing_frontmatter else 0


if __name__ == "__main__":
    raise SystemExit(main())
