---
name: appie-environment-maintenance
description: Daily healthcheck and low-risk cleanup workflow for Appie/Hermes environments. Use for routine self-maintenance runs that inspect /root/.hermes and /root/clawd, verify gateway/cron health, confirm canonical assets exist, and report only safe fixes.
---

# Appie Environment Maintenance

Use this skill for routine Appie-2 / Hermes self-maintenance runs and similar fleet health checks. The goal is to verify the environment first, clean only obvious clutter, and report anything riskier as a recommendation instead of acting on it.

## Triggers

- Daily cron self-maintenance runs
- Checks of `/root/.hermes` and `/root/clawd`
- Gateway health review
- Telegram service clues or polling warnings
- Disk, log, cache, and workspace hygiene review
- Verifying Appie asset files and scheduled jobs still exist

## Operating rules

1. **Read first, write later**
   - Inspect state before making any cleanup decision.
   - Prefer status files, process state, and logs over assumptions.

2. **Do not expose secrets**
   - Never print tokens, bot secrets, env contents, or private keys.
   - When logs include redacted auth material, keep it redacted.

3. **Keep cleanup minimal and obviously safe**
   - Remove only stale, clearly disposable temp artifacts when the owner and purpose are obvious.
   - Do not touch source, config, state databases, or live service directories unless there is an explicit, low-risk pattern to do so.

4. **Report, don’t guess**
   - If something looks off but you cannot prove it is safe to change, report it as a recommended next step.
   - Historical log errors do not automatically imply a current incident.

## Maintenance workflow

### 1. Verify gateway health
Check all of the following before concluding the gateway is healthy:
- `gateway_state.json` shows a running gateway and connected platforms
- gateway process exists in `ps`
- gateway logs are not showing a live crash loop
- Telegram clues are consistent with one active bot instance, not a current conflict
- in root-run cron contexts, prefer `hermes gateway status` plus `systemctl status hermes-gateway` (system scope). `systemctl --user` may fail without a user bus and is not, by itself, an outage signal

Useful sources:
- `/root/.hermes/gateway_state.json`
- `/root/.hermes/gateway.pid`
- `/root/.hermes/logs/gateway.log`
- `/root/.hermes/logs/errors.log`

### 2. Verify cron scheduler health
Confirm both the system scheduler and Hermes cron state:
- `cron` or `crond` is active
- `/root/.hermes/cron/jobs.json` exists and is readable
- scheduled jobs still show enabled/healthy state
- check per-job **last run** errors, not just whether jobs are active
- explicitly flag repeated multi-job signatures (for example `RuntimeError: 'NoneType' object is not iterable`) as scheduler/model health issues requiring follow-up
- the tick lock is not obviously stale

Useful sources:
- `systemctl is-active cron` or `systemctl is-active crond`
- `/root/.hermes/cron/jobs.json`
- `/root/.hermes/cron/.tick.lock`

### 3. Check disk and growth hotspots
- Use `df -h` for the root filesystem.
- Look for growth in:
  - `/root/.hermes/logs`
  - `/root/.hermes/cache`
  - `/root/.hermes/audio_cache`
  - `/root/.hermes/image_cache`
  - `/root/clawd/logs`
  - `/root/clawd/dashboard/.cache`
  - `/root/clawd/tmp`
- If cleanup is obvious and low-risk, remove only stale temporary folders or throwaway artifacts.
- Large media bundles under `tmp/` are often worth reporting rather than deleting unless the naming clearly marks them as disposable.

### 4. Check workspace integrity
In `/root/clawd`:
- run git status
- note whether the tree is clean, ahead, modified, or has untracked files
- avoid changing unrelated work

### 5. Confirm canonical Appie assets still exist
Verify the standard files and directories used by Appie are present, especially:
- `/root/clawd/assets/appie-profile-picture.png`
- `/root/clawd/projects/appie-character/appie-reference-locked.png`
- `/root/clawd/appies/appie-2/INSTANCE.md`
- `/root/clawd/appies/APPIE_BIBLE.md`
- any known cron/job setup files in `/root/.hermes/cron/`

### 6. Summarize with the required shape
Return a concise report with:
- Summary
- Issues found
- Actions taken
- Recommended next step

If nothing meaningful changed and no risk is present, say so plainly.

## Safe cleanup patterns

- Remove stale temp directories that are clearly detached from current work and have no live reference.
- Prefer deleting whole throwaway folders over pruning in-place unless the folder is obviously disposable.
- Recheck disk usage after cleanup.

## Avoid

- Editing config to silence logs without understanding the cause
- Touching secrets or credential files
- Deleting caches just because they are old if they may still be serving active workflows
- Concluding gateway or Telegram is broken based only on historical logs

## Pitfalls discovered

- When a scheduler or automation loads a skill by name, check for collisions first. If `skill_view` reports ambiguity, switch to a fully qualified category path instead of retrying the bare name.
- Historical Telegram warnings about missing media in `tmp/` do not by themselves mean the live gateway is unhealthy. Confirm the gateway process and state file before acting.
- Large temp-media bundles under `/root/clawd/tmp` are often safe cleanup candidates only when they are clearly detached from current work and not referenced by the workspace.

See `references/daily-maintenance-2026-05-23.md` for a compact run log and the skill-collision fix pattern.
See `references/daily-maintenance-2026-05-29-cron-root-context.md` for root-cron user-bus behavior and repeated cron last-run error detection.

## Verification checklist

- [ ] Gateway state file says running/connected
- [ ] Gateway process exists
- [ ] Cron service is active
- [ ] Job definitions exist and look sane
- [ ] Disk usage checked
- [ ] Workspace git status reviewed
- [ ] Canonical Appie files exist
- [ ] Any cleanup performed was obviously safe
- [ ] Final report includes the four requested sections

## Session reference

See `references/daily-maintenance-2026-05-22.md` for the maintenance run that informed this workflow, including the large temp-media hotspot pattern and the distinction between historical Telegram log noise and current gateway health.
