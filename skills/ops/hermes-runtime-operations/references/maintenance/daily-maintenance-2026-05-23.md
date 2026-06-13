# Daily maintenance run notes - 2026-05-23

## What mattered
- Gateway state was healthy and Telegram showed `connected`.
- Cron service was active and `/root/.hermes/cron/jobs.json` existed with 5 enabled jobs.
- Canonical Appie assets still existed under `/root/clawd`.
- `git status` in `/root/clawd` was not clean, but the changes were unrelated to maintenance.

## Important pitfall discovered
- Cron attempted to load `appie-self-maintenance` and `hermes-agent` by bare skill name, but both names collide with multiple local/external skill definitions.
- The job was skipped because `skill_view` refused to guess.
- Fix pattern: use fully qualified skill paths when a name is ambiguous, or rename/merge the colliding skill entries so the scheduler has a unique target.

## Safe cleanup performed
Removed obvious disposable temp-media directories from `/root/clawd/tmp`:
- `loom_amalia`
- `amalia_review`
- `amalia_thumbs`

This reduced `/root/clawd/tmp` from a large media hotspot to a small directory.

## Verification snippets
- `systemctl is-active cron` -> active
- `df -h /` -> ~21% used after cleanup
- `git -C /root/clawd status --short --branch` -> ahead 57, plus unrelated modified/untracked files
