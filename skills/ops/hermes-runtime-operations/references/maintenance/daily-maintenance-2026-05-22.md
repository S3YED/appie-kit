# Daily maintenance run, 2026-05-22

This note captures the concrete observations that shaped the maintenance workflow.

## What to inspect each run

- `/root/.hermes`
- `/root/clawd`
- `systemctl is-active cron` or `crond`
- `/root/.hermes/cron/jobs.json`
- `/root/.hermes/gateway_state.json`
- `/root/.hermes/logs/gateway.log`
- `/root/.hermes/logs/errors.log`
- `/root/clawd/logs/gateway.log`
- `git -C /root/clawd status --short --branch`

## Observed healthy baseline

- Cron service was active.
- Gateway process was present.
- `gateway_state.json` showed the Hermes gateway running and Telegram connected.
- Disk usage on `/` was low, around 22% used.
- Appie canonical files were still present:
  - `/root/clawd/assets/appie-profile-picture.png`
  - `/root/clawd/projects/appie-character/appie-reference-locked.png`
  - `/root/clawd/appies/appie-2/INSTANCE.md`
  - `/root/clawd/appies/APPIE_BIBLE.md`

## Observed maintenance findings

- Historical gateway logs contained old Telegram polling conflicts and model/context errors.
- Those logs were not evidence of a live incident once current state files and process checks were healthy.
- `/root/clawd/tmp` can accumulate large media bundles.
- A safe cleanup win was removing clearly stale storyboard directories when they were detached from current work.

## Cleanup pattern that was safe here

- Remove only old, obviously disposable temp folders.
- Recheck `df -h` after cleanup.
- Leave caches and media bundles in place if their purpose is unclear or they may still be in use.

## Reporting pattern

A good maintenance note should separate:

1. Summary
2. Issues found
3. Actions taken
4. Recommended next step

That shape makes cron output easier to scan later.
