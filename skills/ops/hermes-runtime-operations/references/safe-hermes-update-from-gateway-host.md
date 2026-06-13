# Safe Hermes update from a gateway-hosted agent session

Use this reference when planning a Hermes update on a machine where the active agent is running through the Hermes gateway/systemd service.

## Durable lesson

A gateway-triggered/tool-executed shell may inherit systemd hardening from `hermes-gateway.service`. If the service uses `ProtectSystem=full`, paths under `/usr` can appear read-only inside the gateway process namespace even when the host filesystem itself is writable from a normal SSH shell.

Symptom during update preflight:

```text
hermes update --check
error: cannot open '.git/FETCH_HEAD': Read-only file system
```

This is not necessarily a broken repo or disk. It can mean the check is running from the gateway sandbox.

## Safe workflow

1. Scan first, do not update from Telegram/chat immediately:
   - `hermes --version`
   - `git status --short --branch`
   - `git diff --stat`
   - `hermes gateway status`
   - `hermes cron list`
   - `hermes doctor`
2. Clone or fetch a fresh upstream copy into a neutral path such as `/root/hermes-update-scan/hermes-agent-latest`.
3. Compare current codebase to latest, especially local dirty files and files touched upstream.
4. Back up before update:
   - source patch: `git diff > /root/hermes-update-backups/hermes-local-source-adjustments-$(date +%Y%m%d-%H%M%S).patch`
   - Hermes home tarball, excluding bulky regenerated caches/logs
   - gateway service unit: `systemctl cat hermes-gateway > ...`
   - pre-update HEAD: `git rev-parse HEAD > ...`
5. Stash source-tree local changes before updating:
   - `git stash push --include-untracked -m "pre-hermes-update-local-changes-$(date +%Y%m%d-%H%M%S)"`
6. Run the real update from a normal SSH shell, not from the gateway tool context:
   - `cd /usr/local/lib/hermes-agent && hermes update --backup`
7. If the update asks whether to restore local changes, default to **no** when the local patch overlaps with upstream changes. Reapply only after validating that upstream did not solve the issue.
8. Post-update validation:
   - `hermes --version`
   - `hermes doctor`
   - `hermes gateway status`
   - `hermes cron list`
   - `git status --short --branch`
   - smoke test the messaging platform and one tool-backed request.

## Rollback pattern

If code update breaks the install but git still works:

```bash
cd /usr/local/lib/hermes-agent
git reset --hard $(cat /root/hermes-update-backups/hermes-pre-update-head.txt)
/usr/local/lib/hermes-agent/venv/bin/python -m pip install -e '.[all]'
systemctl restart hermes-gateway
```

If Hermes home data is damaged, restore the pre-update Hermes-home tarball and restart the gateway.

## Pitfall

Do not encode this as "Hermes update is broken" or "git cannot write to /usr". The durable rule is contextual: update from outside the hardened gateway namespace, or stop/restart the gateway around the update if necessary.
