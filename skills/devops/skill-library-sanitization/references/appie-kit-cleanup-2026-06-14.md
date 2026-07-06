# Appie Kit cleanup example, 2026-06-14

This reference captures the reusable pattern from a public skill-library cleanup. It is intentionally compact and excludes raw private findings.

## Scope

- Public tree: an agent skill library intended for release.
- Private material: client-specific skills, internal bot references, local infrastructure details, NSFW-related bot material, paid-course/raw transcript imports, stale duplicates.
- Quarantine: moved outside the repo under a timestamped private path.

## Sanitization replacements used

- Concrete Notion database/data-source IDs -> `<NOTION_DATABASE_ID>` or env-var references.
- Webflow site/collection IDs -> `<WEBFLOW_SITE_ID>`, `<WEBFLOW_COLLECTION_ID>`.
- Private/Tailscale IPs and internal domains -> `<PRIVATE_HOST>` / `<INTERNAL_DOMAIN>`.
- Bot handles and personal account handles -> generic placeholders.
- SSH key paths -> `<SSH_KEY_PATH>`.
- Local absolute paths -> portable `$HOME/...` examples or `<PROJECT_PATH>`.
- Signed URL query tokens -> stripped from public docs.
- Hardcoded-looking API keys -> safe placeholders and `.env.example` entries.

## Verification checklist

- Public skill count recorded.
- Unique skill names equal public skill count.
- Duplicate skill names: 0.
- Missing frontmatter/description: 0.
- Index/link validation: PASS.
- Custom private-pattern scan: PASS with 0 findings.
- Generic scanner, e.g. `gitleaks detect --source . --no-git --redact`: PASS with 0 findings.
- Syntax checks for touched Python/Node scripts: PASS.
- Git diff reviewed for accidental private report content.

## Final response shape

Keep the user-facing summary clean:

- What changed.
- Verification results.
- Quarantine path and count.
- Report paths.
- Warning that large deletions are intentional but should be reviewed before commit/push.

Do not paste raw private identifiers or detailed leak snippets into chat.
