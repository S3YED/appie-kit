# Large CLI Uploads and UNKNOWN Deploys

Use this when a Vercel CLI production deploy is authenticated and linked, but publishing is not cleanly confirmed.

## Symptom pattern

- Project is linked via `.vercel/project.json` and `vercel whoami --token "$VERCEL_TOKEN"` succeeds.
- Local app build succeeds, e.g. `npm run build` passes for a Next.js App Router project.
- `vercel deploy --prod --yes --token "$VERCEL_TOKEN"` fails with:

```text
Invalid request: `files` should NOT have more than 15000 items, received <n>.
Try using `--archive=tgz` to limit the amount of files you upload.
```

- Retrying with `--archive=tgz` can create a Vercel production deployment URL, but `vercel inspect <deployment-host>` may show:

```text
status UNKNOWN
target production
Builds: . [0ms]
```

- The unique deployment URL may return 401 because of Vercel Deployment Protection. That alone does not prove failure, but `UNKNOWN` also does not prove success.

## Safe workflow

1. Verify auth and project link:

```bash
vercel whoami --token "$VERCEL_TOKEN"
cat .vercel/project.json
```

2. Verify the app itself:

```bash
export PATH="/opt/homebrew/opt/node@22/bin:$PATH"  # if project requires node@22
npm run build
```

3. Check local noise before uploading:

```bash
git status --short
```

Do not upload untracked helper files, `.next`, `node_modules`, screenshots, reports, or temporary artifacts if they are not needed.

4. If direct deploy hits the file-count limit, retry with archive mode:

```bash
vercel deploy --prod --yes --archive=tgz --token "$VERCEL_TOKEN"
```

5. Verify the result with the canonical alias, not just the generated deployment URL:

```bash
vercel inspect <project>.vercel.app --token "$VERCEL_TOKEN"
curl -I -L https://<project>.vercel.app
```

Report success only if the alias maps to a `Ready` deployment and HTTP/content checks match the intended version.

## What not to do

- Do not report "published" when `vercel inspect` says `UNKNOWN`.
- Do not confuse a protected unique deployment URL returning 401 with the public canonical alias status.
- Do not conclude the app is broken just because `vercel build` fails while `npm run build` succeeds. Debug the Vercel packaging path separately.
- Do not delete `.next` destructively while debugging. Move it to `/private/tmp/...` if you need a clean local state, then rebuild normally before leaving the project.

## Durable fix options

- Add a project `.vercelignore` excluding `.next`, `node_modules`, local reports, screenshots, and tool outputs.
- Prefer GitHub auto-deploy for Vercel-linked projects when a remote exists and Vercel watches the branch. It avoids bulky CLI uploads and usually gives better build logs.
- Keep deploy claims precise: "local build green, auth works, live alias is still previous Ready deploy" is better than overstating success.