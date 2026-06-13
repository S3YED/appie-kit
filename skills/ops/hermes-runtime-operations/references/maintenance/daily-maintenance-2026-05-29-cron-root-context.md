# Daily maintenance note - 2026-05-29 (root cron context)

## What was new
- `hermes-gateway.service` (system scope) was healthy and running.
- `systemctl --user status hermes-gateway` failed with `Failed to connect to bus: No medium found` in cron/root context.
- Appie-2 maintenance and two content cron jobs reported recent last-run failures with the same signature:
  - `RuntimeError: 'NoneType' object is not iterable`
- Legacy port `18789` was not listening, while gateway health remained good (expected compatibility signal behavior).

## Durable handling pattern
1. In cron/root runs, treat `systemctl --user` failure as context-related unless other gateway checks fail.
2. Use `hermes gateway status` + system service state + `gateway_state.json` as primary liveness signals.
3. In cron checks, always inspect per-job `last run` errors and look for repeated signatures across jobs.
4. Report repeated signatures as priority follow-up even when scheduler itself is active.

## Why this matters
A run can look healthy at the service/scheduler layer while workload execution is degraded. The maintenance report should distinguish:
- infrastructure healthy (gateway/scheduler up), and
- job execution quality degraded (repeating runtime errors).
