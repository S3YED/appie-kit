# Local vs live Vercel verification

Use this when the user asks whether a design/change has been pushed or deployed.

## Goal
Separate three different states that often get conflated:

1. Local commit exists.
2. Commit is pushed to GitHub/remote.
3. Vercel production is serving that commit.

Do not answer "yes" unless all relevant states are verified.

## Verification sequence

```bash
cd /path/to/project

# 1. Local state
git status --short
git log --oneline --decorate -8
git show --stat --oneline --decorate HEAD
git show -s --format='%H%n%ci%n%s' HEAD

# 2. Remote state
git remote -v
git ls-remote origin refs/heads/$(git branch --show-current)

# 3. Vercel project link
cat .vercel/project.json

# 4. Live production status
curl -I -L https://<project>.vercel.app
vercel inspect https://<project>.vercel.app --token "$VERCEL_TOKEN"

# 5. Live content check
curl -L https://<project>.vercel.app | head -c 20000
```

## Interpretation

- Local commit exists, but `git ls-remote` fails with `Repository not found`: say the change is local only, or at least not verifiably pushed to that origin.
- Vercel inspect shows a production deploy older than the local commit timestamp: production cannot contain that local commit unless there was a later alias switch or another deployment source. Verify live HTML before claiming it is deployed.
- Live HTML/classes still match the old design, while local files match the new design: report "local ready, live not updated".
- `curl -I` returning `200` only proves the site is up. It does not prove the latest commit or design is live.

## Reporting pattern

Keep it crisp:

- Local: commit/hash and build status.
- GitHub/remote: pushed or not verifiable, with exact remote problem.
- Vercel: production deploy timestamp/status and whether live HTML matches the expected change.
- Next action: ask before public deploy if not already authorized.

Example:

> Lokaal staat de light/glass commit en build slaagt. GitHub push is niet bevestigd: origin geeft `Repository not found`. Vercel production is Ready, maar de deploy is ouder dan de commit en live HTML gebruikt nog de oude dark classes. Conclusie: lokaal klaar, niet live gedeployed.
