---
name: skill-library-sanitization
description: "Audit, sanitize, curate, and maintain AI agent skill libraries. Use when pulling external/community skills, updating installed skills, removing secrets/private info, quarantining unsafe material, deduplicating skills, or building a clean curated skill database for public or shared use."
origin: user
---

# Skill Library Sanitization

Use this when preparing, importing, updating, or publishing a skill library, agent kit, prompt/tool bundle, or exported knowledge base. The goal is to preserve reusable workflows while stripping secrets, private identity, client data, infrastructure details, copyrighted/raw paid material, NSFW material, local-machine assumptions, and stale duplicates.

## Core rule

Never import external skills directly into the live skill library. Pull into a staging area, scan, sanitize, curate, validate, then promote.

## Standard directory model

Use explicit zones:

- **Sources**: external repos, marketplace exports, local Hermes/OpenClaw/Claude skills, appie-brain skills.
- **Intake staging**: `~/.hermes/skill-intake/<source>/<timestamp>/` for raw pulled material.
- **Quarantine**: `~/.hermes/skill-quarantine/<timestamp>/` for private, unsafe, duplicate, or unlicensed material.
- **Clean database**: a user-approved repo or folder such as `<CLEAN_SKILLS_REPO>/skills/`.
- **Install target**: `~/.hermes/skills/` only after clean database validation passes.

Do not leave quarantine inside a public repo, even when `.gitignore` hides it.

## Workflow

### 1. Intake, never direct install

For a Git source:

```bash
mkdir -p ~/.hermes/skill-intake
cd ~/.hermes/skill-intake
git clone --depth 1 <REPO_URL> <source>-$(date -u +%Y%m%dT%H%M%SZ)
```

For local sources, copy into staging instead of editing originals:

```bash
rsync -a --exclude '.git' <SOURCE_SKILLS_DIR>/ ~/.hermes/skill-intake/<source>-$(date -u +%Y%m%dT%H%M%SZ)/
```

Record source URL/path, commit SHA if available, timestamp, and license before touching content.

### 2. Inventory and normalize

Count skills by `SKILL.md`, not just folders. Extract:

- skill name and description
- source path and source license
- linked resources under `references/`, `scripts/`, `templates/`, `assets/`
- duplicate names
- missing or malformed frontmatter
- support files outside allowed directories
- absolute paths, network calls, credential references, destructive commands

Use `scripts/scan_skill_library.py` from this skill for a masked inventory and leak scan.

### 3. Classify before editing

Classify every skill:

- **Keep**: generic, useful, low-risk, portable.
- **Sanitize**: useful workflow but contains private IDs, local paths, credentials, client references, internal hosts, or account names.
- **Merge**: narrow one-off that belongs in an umbrella skill.
- **Quarantine**: private/session-specific, NSFW/client-sensitive, raw paid-course/transcript material, unsafe automation, unclear license, or private memory.
- **Retire**: stale, broken, duplicate with no unique content.

Do not delete useful workflows just because they contain private IDs. Replace identifiers with placeholders and document required env vars.

### 4. Sanitize into portable placeholders

Replace concrete values with placeholders while keeping the procedure intact:

- API keys/tokens/cookies/auth headers -> `<API_KEY>`, `<TOKEN>`, env-var references, or `.env.example` keys.
- Notion database/data-source/page IDs -> `<NOTION_DATABASE_ID>`.
- Webflow site/collection IDs -> `<WEBFLOW_SITE_ID>`, `<WEBFLOW_COLLECTION_ID>`.
- Google Drive/docs/sheets IDs -> `<GOOGLE_FILE_ID>` / `<SPREADSHEET_ID>`.
- Tailscale/private IPs/internal domains -> `<PRIVATE_HOST>` / `<INTERNAL_DOMAIN>`.
- SSH hosts/key paths/usernames -> `<SSH_HOST>`, `<SSH_KEY_PATH>`, `<REMOTE_USER>`.
- Local absolute paths -> `$HOME/...` or `<PROJECT_PATH>`.
- Client/person/bot handles -> `<CLIENT_NAME>`, `<ACCOUNT_HANDLE>`, `<BOT_NAME>`.
- Signed URLs/query tokens -> strip query string or replace with `<SIGNED_URL>`.

### 5. Quarantine safely

Move unsafe files outside the clean database and keep a private manifest:

```bash
mkdir -p ~/.hermes/skill-quarantine/<timestamp>
mv <unsafe-path> ~/.hermes/skill-quarantine/<timestamp>/
```

The public report should say counts and categories only. Do not paste raw private snippets into chat or public reports.

### 6. Curate the clean database

For promoted skills:

- Keep one canonical skill per workflow, with umbrella skills preferred over narrow one-offs.
- Use lowercase hyphenated names and ensure global uniqueness.
- Keep `SKILL.md` concise; move long examples to `references/`.
- Keep support files only under `references/`, `scripts/`, `templates/`, or `assets/`.
- Replace environment-specific commands with variables and setup notes.
- Prefer deterministic scripts for repeatable scanning/conversion.
- Preserve attribution/license metadata in a private or public manifest when allowed.

### 7. Layered verification before promote/install

Run all gates before copying into the clean database or install target:

```bash
python3 <THIS_SKILL_DIR>/scripts/scan_skill_library.py <STAGED_OR_CLEAN_DIR> --json-out /tmp/skill-scan.json
# If available:
gitleaks detect --source <STAGED_OR_CLEAN_DIR> --no-git --redact
```

Also verify:

- Unique skill names equal total public skills.
- Missing frontmatter/description: 0.
- Duplicate names: 0.
- Broken links/support-file paths: 0.
- Secret/private-pattern findings: 0, except explicitly accepted false positives.
- Touched scripts pass syntax checks.
- Git diff contains no private report content.

### 8. Promote atomically

Promote only validated skills:

```bash
rsync -a --delete <CLEAN_CANDIDATE_DIR>/ <CLEAN_SKILLS_REPO>/skills/
```

Then install or sync from the clean database into `~/.hermes/skills/` if desired. Avoid editing installed skills directly when a clean source-of-truth repo exists.

### 9. Ongoing update loop

For updates:

1. Pull new upstream material into a fresh staging folder.
2. Compare against current clean database.
3. Re-run scan and classification.
4. Apply sanitization/merge decisions in staging.
5. Validate.
6. Promote with a reviewed diff.
7. Update indexes/manifests and this skill if the workflow changed.

## Reporting

Final reports should be terse and actionable:

- Source(s) inspected.
- Public/clean skill count.
- Kept, sanitized, merged, quarantined, retired counts.
- Duplicate skill count.
- Frontmatter/description validation result.
- Secret/private-pattern scan result.
- Generic scanner result.
- Syntax/index validation result.
- Quarantine path and file count.
- Clean database path and report paths.
- Reminder that intentional deletions need review before commit/push.

Never paste raw secrets or full private findings into chat. Mask them or reference the private quarantine path.

## Pitfalls

- Do not treat `gitleaks` alone as sufficient. It misses private identities, internal domains, client names, local paths, signed URLs, and operational details.
- Do not trust marketplace/community skills until read and scanned. Skills can contain destructive shell commands, exfiltration URLs, or hidden credential assumptions.
- Do not promote raw session transcripts, paid course transcripts, private memory, NSFW client-bot material, or client-specific docs into a shared kit.
- Do not rely on directory names for uniqueness. Read `name:` frontmatter.
- Do not create one skill per cleanup session. Fold recurring lessons into this skill and put run-specific patterns in `references/`.

## Support files

- `scripts/scan_skill_library.py`: masked inventory and leak scanner for skill trees.
- `references/curated-skill-database-workflow.md`: detailed intake, sanitize, curate, promote workflow.
- `references/appie-kit-cleanup-2026-06-14.md`: compact example of a completed public skill-kit cleanup, including validation checklist and reporting shape.
