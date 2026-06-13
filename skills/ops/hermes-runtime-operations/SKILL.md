---
name: hermes-runtime-operations
description: Operate and troubleshoot Hermes runtime health in production-like environments. Use for routine environment maintenance (gateway/cron/disk/workspace checks) and auth incident response (OAuth/API-key failures, refresh-token issues, headless device-code recovery).
---

# Hermes Runtime Operations

Class-level runbook for keeping Hermes healthy and recoverable.

## Update safety on gateway hosts

When planning or performing a Hermes update on a live gateway host, use the preflight, backup, stash, validation, and rollback pattern in `references/safe-hermes-update-from-gateway-host.md`. Important pitfall: a Telegram/gateway-triggered tool shell may run inside the `hermes-gateway.service` systemd namespace. If the service has `ProtectSystem=full`, `/usr` can be read-only in that namespace and `git fetch`/`hermes update --check` may fail on `.git/FETCH_HEAD`; run the real update from a normal SSH shell or stop/restart the gateway around the update.

Use this skill when the task is either:
1. **Routine maintenance** (preventive checks and low-risk cleanup), or
2. **Auth troubleshooting** (provider auth failures, token refresh breakage, re-auth flows).

## Operating model

- **Read before write**: gather evidence first.
- **Minimal-risk changes only**: perform only clearly safe actions; escalate risky actions as recommendations.
- **No secret exposure**: never output tokens/keys/raw env secrets.
- **Verify after change**: restart/recheck services when applicable.

## Workflow A - Routine maintenance (daily/periodic)

1. Validate gateway health from state + process + logs (avoid judging by stale historical errors alone).
2. Validate scheduler/cron health, job definitions, and most recent per-job failures.
3. Check disk usage and hotspot directories (`~/.hermes/logs`, caches, temp/work dirs).
4. Check workspace integrity (git status) without mutating unrelated work.
5. Confirm canonical required assets/job files exist.
6. Apply only obvious low-risk cleanup; otherwise report recommendations.

Output shape:
- Summary
- Issues found
- Actions taken
- Recommended next step

## Workflow B - Auth incident response

1. Inspect auth state (`hermes auth list`) and recent auth/provider failures in logs.
2. Confirm active provider/model config and identify failing credential source.
3. Validate auth store layers (`providers.*` and `credential_pool.*`) and stale entries.
4. For headless OAuth/device-code failures, run manual device-code flow and persist refreshed credentials.
5. Restart gateway and verify the provider path is healthy.

Common patterns:
- `401/403`, silent empty provider output, refresh loops, `invalid_grant`, reused refresh tokens.
- Device-code polling on headless systems should run in background with completion notification.

## Absorbed modules (labeled)

### From `appie-environment-maintenance`
- Daily healthcheck flow for gateway + cron + disk + workspace integrity.
- Root-cron/systemd user-bus caveat (`systemctl --user` false negatives in root cron contexts).
- Distinction between historical log noise and live outages.
- Conservative cleanup policy for temp media and caches.

### From `hermes-auth-troubleshooting`
- Cross-provider auth failure triage (OAuth and API-key paths).
- Dual-layer auth store model (`providers.*` + `credential_pool.*`).
- Headless device-code recovery workflow and gateway restart requirement.
- Refresh-token reuse and stale credential-pool reseeding pitfalls.

## Workflow C - Safe Hermes update with local adjustments

1. Inspect install method, version, git branch/remotes, dirty source files, stashes, profiles, and cron jobs before updating.
2. For a self-scan/audit request, clone the current upstream repo into a separate audit directory and compare it to the live checkout before mutating production.
3. Back up user-owned runtime state under the active Hermes home (`config.yaml`, `.env`, `auth.json`, `cron/jobs.json`, `scripts/`, `skills/`, `memories/`, `state.db`, `sessions/`) while excluding bulky caches/logs.
4. If the Hermes source checkout is dirty, save `git diff` as a patch and separately copy important untracked files before running the updater.
5. Prefer `hermes update --backup` from SSH for production gateways instead of casual chat `/update` when local source changes exist.
6. If the updater auto-stashes local source changes and asks whether to restore, default to *not* restoring old workarounds immediately when the install is far behind or the modified file is likely to have changed upstream. Update cleanly, then inspect and port the patch deliberately if still needed.
7. Verify post-update with version, doctor, gateway status, cron list, git status, and stash list.

Detailed commands: `references/hermes-safe-update-preserve-local-adjustments.md`

## Workflow D - Legacy bridge decommission and fleet recovery

Use `references/legacy-bridge-decommission-and-fleet-recovery.md` when old OpenClaw/ccgram/tmux bridges compete with Hermes gateway ownership or when multiple Appie agents go down at once. Inspect first, stop launchers before killing child tmux processes, verify no bot-token conflicts, and prefer separate VPS boxes for operationally distinct agents.

## Playbooks and deep references

- Environment maintenance references: `references/maintenance/`
- Remote host watchdog pattern: `references/maintenance/remote-host-watchdog.md`
- Auth troubleshooting references/scripts: `references/auth/`
- Safe update preserving local adjustments: `references/hermes-safe-update-preserve-local-adjustments.md`
- Safe update preserving local adjustments: `references/hermes-safe-update-preserve-local-adjustments.md`
- Safe update preserving local adjustments: `references/hermes-safe-update-preserve-local-adjustments.md`
- Secret ingestion + local scrub pattern: `references/secret-ingestion-and-local-scrub.md`
- Mac Hermes profile gateway + Codex OAuth recovery: `references/mac-profile-gateway-codex-oauth.md`
- Legacy source skill snapshots (for historical context): `references/legacy/`

## Profile gateway recovery pattern

When a named Hermes profile is configured correctly but appears offline, verify the profile service itself before editing scripts or credentials:

1. Check the profile: `hermes profile show <profile>`.
2. Check profile gateway status: `hermes -p <profile> gateway status`.
3. If stopped, install/start the profile-scoped launchd/system service: `hermes -p <profile> gateway install` then `hermes -p <profile> gateway start`.
4. Verify fleet state: `hermes gateway list` and profile logs under the profile home, for example `~/.hermes/profiles/<profile>/logs/gateway.log`.
5. Confirm provider path with a non-secret smoke test: `hermes -p <profile> chat -Q -q 'Reply exactly: OK'`.

For OpenAI Codex OAuth on Hermes, `model.provider: openai-codex`, `model.default: gpt-5.5`, `model.base_url: https://chatgpt.com/backend-api/codex`, and `model.openai_runtime: auto` are a known-good profile configuration when using Hermes-managed OAuth credentials.

## Pitfalls

- Ambiguous skill names can break automation; use fully qualified skill paths in cron/automation contexts.
- Historical Telegram/gateway warnings are not proof of current outage; verify live state.
- Stale supervisor or script logs can mislead incident response; reproduce current syntax/status (`bash -n`, service status, live process list) before patching files.
- A default Hermes gateway and a named-profile gateway are separate services; `hermes gateway status` may show default stopped while `hermes -p <profile> gateway status` is healthy.
- Token changes typically require gateway restart to become effective.
- Single-use refresh/device tokens can be invalidated by concurrent consumers.
