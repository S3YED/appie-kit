# Finding the live deploy for a Vercel-linked project

Use this when a local project is Vercel-linked but the requested custom domain may still point elsewhere.

## What to check

1. Inspect `.vercel/project.json` in the project root.
   - Captures `projectId` and `orgId` even when deploy URLs are missing from notes.
   - Confirms which Vercel project the local source is linked to.

2. Search deployment manifests and ship scripts.
   - Common locations in your workspace:
     - `<project>/deployment/manifests/*.yaml`
     - `<project>/scripts/ship-*.sh`
   - Look for intended domains, aliases, and project names.

3. Verify the custom domain by fetching the live HTML.
   - Do not assume the custom domain serves the latest Vercel build just because the manifest says it should.
   - Check for platform fingerprints: Shopify scripts, Webflow assets, Vercel/Next.js markers, old branding, or unexpected page structure.

4. If Vercel API/CLI access is available, query deployments and aliases.
   - Use token-authenticated `vercel`/API calls to recover generated deployment URLs.
   - If API access is unavailable or rejected, clearly separate:
     - known Vercel link from local files
     - intended live domain from manifests
     - actually live domain content from HTTP verification

## Reporting pattern

Return three distinct facts:

- Source location: local repo path and key files.
- Vercel link: project name plus `projectId`/`orgId` from `.vercel/project.json`.
- Public reality: what the custom domain currently serves, verified from live HTML.

If the custom domain still serves another platform, say so directly and name the evidence. Example: "`https://example.com` still serves the old Shopify site, not the new Next/Vercel build."
