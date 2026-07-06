# Curated skill database workflow

This reference describes the clean-database workflow for skill libraries. Use it when importing, updating, or publishing skills.

## Principles

- Raw imports are never trusted.
- The clean database is the source of truth.
- Installed skills are deployment artifacts, not the place to curate.
- Private findings live in private reports, not chat or public repos.
- Curation preserves reusable workflows and removes local/private details.

## Suggested layout

```text
clean-skills/
├── skills/
│   ├── security/skill-library-sanitization/SKILL.md
│   └── ...
├── manifests/
│   ├── sources.json
│   ├── quarantine-manifest.json
│   └── scan-results.json
└── README.md
```

Private staging/quarantine stay outside this repo:

```text
~/.hermes/skill-intake/
~/.hermes/skill-quarantine/
```

## Intake checklist

For each source:

- Source URL/path:
- Commit SHA or version:
- License:
- Pull timestamp UTC:
- Intended destination:
- Explicit exclusions:

Use shallow clones for external repos. Avoid running scripts from intake until scanned.

## Review checklist

- Read `SKILL.md` frontmatter and first-pass body.
- Search scripts for network calls, destructive commands, credential reads, and shell curl pipes.
- Search references/templates for private IDs, names, client details, and hardcoded local paths.
- Check license and attribution requirements.
- Decide: keep, sanitize, merge, quarantine, retire.

## Sanitization checklist

Replace or remove:

- secrets, tokens, cookies, private keys
- private hostnames, Tailscale/IP addresses, SSH users/keys
- local absolute paths and personal usernames
- client/person names unless intentionally public and approved
- bot handles and account identifiers
- Notion/Webflow/Google IDs
- signed URLs and auth query strings
- raw private chat logs, transcripts, paid content, NSFW material

Preserve:

- generic workflow steps
- CLI command shape with placeholders
- validation gates
- reusable scripts after safety review
- attribution when license permits

## Promotion gate

A candidate is promotable only if:

- `scan_skill_library.py` reports no high-severity findings.
- Generic secret scanner passes or findings are accepted false positives.
- Skill names are globally unique.
- Every skill has valid `name` and `description` frontmatter.
- Support files live under allowed directories.
- The git diff has been reviewed for accidental private output.

## Update cadence

- Small update: scan changed skills only, then promote.
- Large import: full inventory and classification.
- Before public release: full scan plus gitleaks plus manual diff review.
- After any leak found: patch sanitizer patterns, rescan whole clean database, rotate exposed secret if real.

## Final report template

```text
Sources inspected: N
Clean skills: N
Kept/sanitized/merged/quarantined/retired: A/B/C/D/E
Validation: PASS/FAIL
Secret scan: PASS/FAIL
Quarantine: <private path>, N files
Reports: <paths>
Next action: review diff, then commit/push or install
```
