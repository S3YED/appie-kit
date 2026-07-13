---
name: vercel-deploy
description: Deploy projects to Vercel via CLI with token auth. Use when deploying Next.js, static sites, or any project to Vercel from the terminal.
version: 1.0.0
triggers:
  - deploy to Vercel
  - vercel deploy
  - push to Vercel
  - Vercel token
---

# Vercel Deploy

End-to-end Vercel deployment via CLI with token-based authentication.

## Prerequisites

- Vercel CLI installed (`npm install -g vercel` or `npx vercel`)
- A valid Vercel access token (from [vercel.com/account/tokens](https://vercel.com/account/tokens))
- Project ready to deploy (build passing)

## Token Management

### Where tokens live
- **Primary:** `~/.hermes/.env` as `VERCEL_TOKEN=vcp_...`
- **Legacy (from OpenClaw):** `~/clawd/.env.secrets` — update when refreshing tokens
- **Always update both** when a token changes to keep legacy and current paths in sync

### Token lifecycle
- Tokens expire — when you get `"The specified token is not valid"`, generate a fresh one
- Fresh token → update both `.env` files, then redeploy

## Deployment

### Standard deploy (linked project)
```bash
cd /path/to/project
npx vercel --prod --yes --token $VERCEL_TOKEN
```

This auto-detects Next.js settings, links the project, and deploys to production.

### First-time deploy (no `.vercel` directory)
The CLI auto-creates `.vercel/project.json` and links to the Vercel project. On first deploy it also auto-connects the GitHub repository.

### Deploy output
- **Inspect URL:** `https://vercel.com/<team>/<project>/<deploy-id>` — build logs
- **Production URL:** `https://<project>-<hash>-<team>.vercel.app`
- **Alias:** `https://<project>.vercel.app` (if configured)

## Verification
```bash
curl -s -o /dev/null -w "%{http_code}" https://<project>.vercel.app
# Expect: 200
```

A 200 only proves the site is up. When the question is whether a specific commit/design is live, compare local commit time/hash, remote branch state, Vercel production deploy timestamp, and live HTML/classes before answering. See `references/local-vs-live-deploy-verification.md`.

## Cross-Account .vercel.app Domain Ownership

A `.vercel.app` subdomain (e.g. `soleiman-advocatuur.vercel.app`) can be **owned by a different Vercel account** than the one you're deploying from. When this happens:

- `vercel alias set` returns `"The chosen alias is already in use"`
- `vercel domain add` returns `"domain_taken"` / `"Cannot add since it's aliased to another deployment on another account"`
- The API returns `409` with `domain_taken`
- The domain serves old content from the foreign account

**Fix:** The owner of the old account must delete the domain. Until then, use the project's auto-assigned URL (`<project>-<hash>-<team>.vercel.app`) or the Vercel-assigned alias (`<project>-azure.vercel.app` for new projects).

**Detection:** Check the domain's `Server` and `x-vercel-id` headers — they confirm it's served by Vercel but not which account. If `vercel domains ls` doesn't show it, it's owned elsewhere.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `The chosen alias is already in use` / `domain_taken` | `.vercel.app` domain owned by another Vercel account | See Cross-Account Domain Ownership section above — use auto-assigned URL or get owner to delete |
| `No existing credentials found` | No `.vercel` auth or `--token` missing | Pass `--token` flag |
| `option requires argument: --token` | Empty `--token` value | Ensure `$VERCEL_TOKEN` is set |
| `--prod false` not recognized | Vercel CLI 54+ changed flag syntax | Use `--yes` without `--prod` for preview (creates unique `.vercel.app` URL), or explicitly without `--prod` flag |
| Build fails with TypeScript errors | `as const` needed on ease arrays in Framer Motion | Add `as const` to cubic-bezier arrays |
| `Failed deployment` email from Vercel — `not a member of the team` | An external user (e.g. `priva@privanotify.com`) pushed to GitHub but is not on the Vercel team. Hobby plan limitation — only team members can deploy via GitHub integration | **First** check if the user can use the GitHub push + Vercel auto-deploy path (preferred by Seyed). The person who made the commit should push their code to the GitHub repo — Vercel's Git integration auto-deploys from main/master pushes. If they are not on the Vercel team, that is not the blocker — the blocker is they need push access to the GitHub repo. See `references/github-auto-deploy.md`. **Only if no repo/remote access exists**, consider adding as Vercel team member at `vercel.com/<team>/~/settings/members`, or upgrading to Pro |
| `files should NOT have more than 15000 items` | CLI upload includes too many files, often because `.next`, `node_modules`, or local artifacts are present | Retry with `--archive=tgz`, but also audit `.vercelignore` and local artifacts before claiming deploy success |
| Production deploy shows `status UNKNOWN` in `vercel inspect` | Vercel accepted a deployment record but did not finish/mark it Ready | Do not count it as published. Verify canonical alias with `vercel inspect <alias>` and live HTTP before reporting success |

## Large CLI Uploads and UNKNOWN Deploys

For projects with many local files, direct CLI deploy can hit Vercel's 15k file upload limit or create a production deployment record that remains `UNKNOWN`. In that case:

- First run the normal local app build (`npm run build`, `pnpm build`, etc.) to separate code correctness from Vercel packaging.
- Check `git status --short` and avoid uploading untracked helper files or build caches.
- Add or update `.vercelignore` for `.next`, `node_modules`, local reports, screenshots, and other non-source artifacts when appropriate.
- Retry direct deploy with `vercel deploy --prod --yes --archive=tgz --token "$VERCEL_TOKEN"` if the file count limit is the only blocker.
- If `vercel inspect <deployment-host>` reports `UNKNOWN`, do not call it published. Inspect the canonical alias (`vercel inspect <project>.vercel.app`) and `curl -I` the live URL.
- `vercel build` is not always equivalent to `npm run build` for App Router projects. If it fails while the normal build succeeds, treat it as a Vercel packaging path to debug, not as proof the app is broken.

See `references/large-cli-upload-and-unknown-deploy.md` for a concrete transcript pattern.

## API Route Triage

When a deployed page shows a JSON parse error like `Unexpected token 'A'...` or an invite page says `Invite Invalid`, check the runtime before assuming the frontend is broken.

- First confirm the route response with `curl -i https://<project>.vercel.app/api/<route>`.
- Then inspect logs with `vercel logs --project <project> --token "$VERCEL_TOKEN" --since 24h --expand --level error`.
- If logs show `FUNCTION_INVOCATION_FAILED` or `ERR_MODULE_NOT_FOUND`, fix the serverless function before touching the UI.
- Remember that a frontend `res.json()` call will fail if the API returns Vercel's plain-text error page instead of JSON.

See `references/api-function-triage.md` for a concrete reproduction and log pattern.

## SSO-protected preview aliases

If a production deploy succeeds but the generated `.vercel.app` URL returns a `302` redirect to `vercel.com/sso-api` (or `401` on older Vercel configs) with `_vercel_sso_nonce` cookie, check deployment protection before reporting the link. The symptom: `curl -sI` shows `HTTP/2 302` with `location: https://vercel.com/sso-api?...`.

Two strategies to make the site publicly accessible:

1. **Add a clean `.vercel.app` subdomain** (preferred — no SSO changes needed):  
   `vercel domain add <projectname>.vercel.app`  
   This works because SSO protection is set to `all_except_custom_domains`, and `.vercel.app` subdomains count as custom domains.

2. **Disable SSO protection** (use when no custom domain is acceptable):  
   `vercel project protection disable <project-name>` or PATCH the project via REST API with `ssoProtection: None`.

Verify with `curl -s -o /dev/null -w "%{http_code}" https://<projectname>.vercel.app` — expect `200`, not a redirect to a login page.

When the CLI approach fails (token masked in terminal, interactive prompts, `--scope` confusion), use the REST API directly. See `references/api-disable-sso.md` for the Python script pattern.

See `references/sso-protected-vercel-previews.md`.

## Creating a Separate / Standalone Vercel Project

When the user asks for a "separate vercel.app deploy" (not a preview of the existing project), they want a **brand new Vercel project** with its own `https://<new-project>.vercel.app` URL.

### The problem: same-name auto-link

Running `vercel deploy --prod --yes` from a directory whose `package.json` `name` field matches an existing Vercel project causes Vercel to **auto-link to the existing project**. This:

- Overwrites the production alias (the custom domain gets reassigned to the new deployment)
- Creates preview-looking URLs that are actually production deploys of the wrong project
- Requires manual alias cleanup to restore the original

### The fix: fresh checkout + auto-create

```bash
# 1. Create a new GitHub repo (private)
gh repo create <org>/<project-name-suffix> --private --push --source=<src-dir>

# 2. Clone fresh into a separate directory
git clone <new-repo-url> <separate-dir>
cd <separate-dir>
npm install

# 3. Deploy with --yes so Vercel auto-creates a new project
# The absence of .vercel/ means Vercel creates a brand-new project
vercel deploy --prod --yes --scope <team>
```

This produces `https://<new-project-name>-<hash>-<team>.vercel.app` as an independent project.

**Never** deploy from the same directory as the original project when the user wants a separate project. Always clone fresh.

## SSL Cert / Alias Re-Assignment Pitfall

When you run `vercel alias rm <domain>` followed by `vercel alias set <deploy-url> <domain>` within a short window (< 5 min), Vercel/Lets Encrypt may return `Error: Response Error` during cert generation. This happens even when the alias was actually set successfully.

**Behavior:** The `vercel inspect <deployment>` output WILL still show the domain under "Aliases" despite the error. The domain resolves correctly after DNS propagation.

**Rule of thumb:** If `vercel alias rm` succeeded and `vercel alias set` returned `Error: Response Error`, check `vercel inspect <deployment>` for the alias list before assuming failure. The cert is likely still being issued asynchronously.

## Finding the Live Deploy

When asked to find the live deploy for a project, separate local intent from public reality:

- Check `.vercel/project.json` for `projectId` and `orgId`.
- Check deployment manifests and ship scripts for intended domains and aliases.
- Fetch the custom domain's live HTML to verify what platform/content it actually serves.
- If Vercel API access is unavailable, report the verified domain state and label any generated Vercel URL as unconfirmed.

See `references/find-live-deploy.md` for the full lookup pattern.

### Token-only Direct Deploys

When working from Telegram or another constrained non-interactive runner, use `vercel deploy --prod --token "$VERCEL_TOKEN" --yes --no-color`, then query the Vercel deployments API from `.vercel/project.json` if the CLI suppresses the URL. Do not claim the custom domain changed until you independently verify the public domain content.

If token loading involves legacy `.env.secrets`, prefer extracting `VERCEL_TOKEN` by key instead of shell-sourcing the whole file. Legacy secrets files can contain unquoted characters or multiline values that make `source` emit unrelated command errors while still leaving deploy state ambiguous.

After a successful production deploy, inspect or verify the intended alias separately. A pretty alias such as `<project>.vercel.app` can still point at the previous deployment even when the new production URL is Ready. If needed, run `vercel alias set <new-deployment-url> <desired-alias> --token "$VERCEL_TOKEN"`, then verify the alias with cache-busted live HTML for a unique marker from the new build.

See `references/token-direct-deploy.md` for the command sequence and pitfalls. See `references/vercel-alias-verification.md` for the alias-staleness verification pattern and safe token extraction snippet. If direct Vercel API inspection is forbidden but GitHub integration created deployment records, use `references/github-deployment-record-vs-alias.md` to distinguish "commit deployed" from "public alias serving the new build".

## GitHub Integration

When `gh` CLI is authenticated and a repo exists, Vercel auto-connects the GitHub repository on first deploy. This enables:
- Auto-deploy on push (if configured in Vercel dashboard)
- Preview deployments for PRs
- Build cache reuse across deployments

Once `.vercel/project.json` exists, subsequent deploys reuse the link — no login needed, just `--token`.

### GitHub push auto-deploy fallback

If direct Vercel CLI deploy is blocked and the user points out that GitHub push should trigger Vercel, switch to the GitHub path immediately:
- Check `git remote -v` before blaming deploy tooling. No remote means there is nothing to push yet.
- Check `gh auth status`, but prefer an existing SSH remote/key for Weblyfe projects when possible.
- Commit only build-relevant files, exclude bulky local artifacts, then push the branch that Vercel watches.
- Treat `Could not resolve host: github.com` as network/DNS permission trouble, not a Vercel or repo diagnosis.
- After push, verify the Vercel deployment or live domain before saying it deployed.

See `references/github-auto-deploy.md` for the full fallback sequence and reporting pattern.

### Deploy without interactive login (token-only)
```bash
# Works even without `vercel login` — token flag handles auth
npx vercel --prod --yes --token $VERCEL_TOKEN
```
The `.vercel` directory persists between deploys. First deploy creates it (auto-links project), subsequent deploys are instant uploads.

## Full Workflow Example
```bash
# 1. Build and verify locally
cd ~/weblyfe/my-project && npm run build

# 2. Deploy to production
npx vercel --prod --yes --token $VERCEL_TOKEN

# 3. Verify
curl -s -o /dev/null -w "%{http_code}" https://my-project.vercel.app
```