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
- Store `VERCEL_TOKEN=vcp_...` in your `.env` or secrets file (e.g. `~/.env.secrets`, `.env.local`)
- Keep a single source of truth; update it whenever a token is rotated

### Token lifecycle
- Tokens expire — when you get `"The specified token is not valid"`, generate a fresh one
- Fresh token → update your env file, then redeploy

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

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `The specified token is not valid` | Token expired | Generate new token at vercel.com/account/tokens |
| `No existing credentials found` | No `.vercel` auth or `--token` missing | Pass `--token` flag |
| `option requires argument: --token` | Empty `--token` value | Ensure `$VERCEL_TOKEN` is set |
| Build fails with TypeScript errors | `as const` needed on ease arrays in Framer Motion | Add `as const` to cubic-bezier arrays |
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

## Finding the Live Deploy

When asked to find the live deploy for a project, separate local intent from public reality:

- Check `.vercel/project.json` for `projectId` and `orgId`.
- Check deployment manifests and ship scripts for intended domains and aliases.
- Fetch the custom domain's live HTML to verify what platform/content it actually serves.
- If Vercel API access is unavailable, report the verified domain state and label any generated Vercel URL as unconfirmed.

See `references/find-live-deploy.md` for the full lookup pattern.

## Token-only Direct Deploys

When working from a non-interactive runner (CI, cron, remote shell), use `vercel deploy --prod --token "$VERCEL_TOKEN" --yes --no-color`, then query the Vercel deployments API from `.vercel/project.json` if the CLI suppresses the URL. Do not claim the custom domain changed until you independently verify the public domain content.

See `references/token-direct-deploy.md` for the command sequence and pitfalls.

## GitHub Integration

When `gh` CLI is authenticated and a repo exists, Vercel auto-connects the GitHub repository on first deploy. This enables:
- Auto-deploy on push (if configured in Vercel dashboard)
- Preview deployments for PRs
- Build cache reuse across deployments

Once `.vercel/project.json` exists, subsequent deploys reuse the link — no login needed, just `--token`.

### GitHub push auto-deploy fallback

If direct Vercel CLI deploy is blocked and the user points out that GitHub push should trigger Vercel, switch to the GitHub path immediately:
- Check `git remote -v` before blaming deploy tooling. No remote means there is nothing to push yet.
- Check `gh auth status`, but prefer an existing SSH remote/key for your project when possible.
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
cd /path/to/my-project && npm run build

# 2. Deploy to production
npx vercel --prod --yes --token $VERCEL_TOKEN

# 3. Verify
curl -s -o /dev/null -w "%{http_code}" https://my-project.vercel.app
```
