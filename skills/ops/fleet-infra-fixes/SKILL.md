# fleet-infra-fixes Skill

## Purpose

Recurring operational fixes and credential patterns for the Appie fleet, so any agent can resolve them fast instead of re-deriving. Captured 2026-06-03.

## node / simdjson breakage (macOS)

Homebrew `node` (25.x/26.x) can break when simdjson upgrades the dylib (libsimdjson.29 missing), breaking codex/vercel/default-node. Symptom: dyld error or "Named export not found". Fix: `brew upgrade node` (-> 26) or use `node@22` at `/opt/homebrew/opt/node@22/bin`. Default to node@22 for Mission Control + Next builds.

## pnpm purge-without-TTY

`pnpm install` in a merged repo may abort: `ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY` (wants to purge node_modules). Do NOT run casual installs in Mission Control. If a dep is genuinely missing, install deliberately and restart the dev server when not in use. reagraph/three are already present; r3f/drei are not.

## Single-repo git access for a bot = SSH deploy key, NOT a token

Vercel/GitHub account tokens are scope-wide. To give a bot write access to ONLY one repo: generate an SSH deploy key ON the bot's machine (`ssh-keygen -t ed25519 -N "" -f ~/.ssh/<repo>_deploy`), add an ssh config alias (`Host github-<repo>` -> IdentityFile that key, IdentitiesOnly yes), and add the PUBLIC key in the repo Settings > Deploy keys (Allow write access). Private key never leaves the box, never goes in chat. Vercel single-project isolation needs a dedicated Vercel TEAM + team-scoped token (project-level RBAC is Enterprise only).

## Secrets discipline

Never echo secrets to Telegram or any chat (they are logged server-side). Secrets live in `~/.weblyfe-secrets/.env` or the agent's config. Tailscale serve cert/key must be gitignored (`*.ts.net.crt/.key`) and kept out of repos.

## Token re-auth (the common blocker)

When GitHub/Vercel ops fail with Bad credentials, the appie-1 tokens are expired (gh keyring + vault GH_TOKEN/GITHUB_TOKEN/VERCEL_TOKEN). SSH to github as S3YED works (key `appie-brain`). Fix needs the human: `gh auth login` + `vercel login`. Do not try to mint tokens; document and wait.

## Browser automation on modern Chrome

Chrome 148 app-bound cookie encryption defeats profile-copy session reuse; Chrome 136+ blocks CDP on the real profile. So you cannot reuse a logged-in GitHub session from a copied profile. For an authenticated headed render (e.g. screenshots of WebGL views), log in via the app's own API in the Playwright context, use `channel:'chrome'`, `headless:false`, `--use-gl=angle`.

## Tailscale serve (Mission Control)

Expose tailnet-only, NEVER funnel: `tailscale serve --bg 3000` -> `https://appie-1.tail61f54b.ts.net`. Disable: `tailscale serve --https=443 off`. The cert/key land in the cwd; move them to `~/.weblyfe-secrets/ts-certs/`.

## Local models

STT: faster-whisper (`small`, int8). Embeddings: ollama `bge-m3`. TTS: local Kokoro/Piper. Image gen: fal.ai Nano Banana. Heavy/bulk work dispatches to Spark Atlas or via `~/bin/dispatch-appie.sh`.
