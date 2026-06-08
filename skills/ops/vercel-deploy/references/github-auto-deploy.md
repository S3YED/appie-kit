# GitHub auto-deploy fallback for Vercel

Use this when the user wants Vercel deploys to happen through GitHub pushes instead of direct `vercel --prod` CLI deploys.

## Pattern

1. Verify the project is linked to Vercel:
   ```bash
   test -f .vercel/project.json && sed -n '1,120p' .vercel/project.json
   ```
   Capture `projectId`, `orgId`, and `projectName`. This only proves local Vercel linkage, not GitHub linkage.

2. Check Git state before trying to push:
   ```bash
   git branch --show-current
   git remote -v
   git status --short
   git log --oneline -5
   ```

3. If no remote exists, do not pretend GitHub auto-deploy can work yet. Add or create a repo first:
   ```bash
   git remote add origin git@github.com:<owner>/<repo>.git
   # or https://github.com/<owner>/<repo>.git if HTTPS creds are known-good
   ```

4. Prefer SSH remotes for Weblyfe/Vercel projects when available. Seyed's Vercel setup often expects commits pushed via the SSH key connected to the GitHub integration. HTTPS/expired `gh` credentials can block despite the repo being otherwise deployable.

5. Keep deploy commits clean:
   - Stage only build-relevant source, config, and docs needed for the deploy.
   - Exclude local artifacts such as generated analysis output, logs, screenshots, and bulky scratch directories.
   - Add artifact directories to `.gitignore` before committing if they are likely to be picked up accidentally.

6. Build before push when the project has a build script:
   ```bash
   npm run build
   git add <explicit files>
   git commit -m "feat: <deploy summary>"
   git push -u origin <branch>
   ```

7. If push fails, distinguish the blocker precisely:
   - `Could not resolve host: github.com`: network/DNS/tool sandbox issue, not a repo or Vercel problem.
   - `gh auth status` invalid token: GitHub CLI needs re-auth, but SSH push may still work.
   - auth denied on HTTPS: switch to SSH or refresh GitHub token.
   - remote missing or wrong owner/name: fix `origin` before retrying.

8. After push, verify the auto-deploy instead of assuming it:
   - Check Vercel deployment page/API if available.
   - Fetch the production/custom domain and confirm the new content is live.

## Reporting to Seyed

Be direct. Say exactly what is already done and what the real blocker is:
- local build status
- commit hash
- configured remote
- push result
- whether Vercel auto-deploy was verified

Avoid framing GitHub push as impossible when the concrete issue is just missing remote, expired `gh`, or sandbox network permission.