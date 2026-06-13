# Legacy bridge decommission and fleet recovery

Use this when a Hermes/Appie host has old Telegram bridges, tmux sessions, or OpenClaw/ccgram services competing with the canonical Hermes gateway, especially during fleet outages.

## Read-only gateway shell caveat

A Telegram/gateway-triggered tool shell may run inside the `hermes-gateway.service` namespace. On hardened services, parts of the filesystem such as `/usr` or `/etc/systemd/system` can be read-only. In that context:

- It is still useful to inspect process/service state.
- `systemctl stop` and `systemctl disable` may work, depending on host policy.
- Full removal/masking of unit files may fail with `Read-only file system`.
- Finish destructive cleanup from a normal SSH shell or after stopping/restarting the gateway under operator control.

## Safe ccgram/tmux decommission sequence

1. Inspect before writing:
   ```bash
   ps -eo pid,ppid,user,stat,lstart,cmd --sort=cmd | grep -Ei 'ccgram|tmux' | grep -v grep || true
   tmux ls 2>&1 || true
   systemctl list-units --all --type=service --no-pager | grep -Ei 'ccgram|tmux|claude|codex' || true
   systemctl list-unit-files --no-pager | grep -Ei 'ccgram|tmux|claude|codex' || true
   (crontab -l 2>/dev/null || true) | grep -Ei 'ccgram|tmux|claude|codex' || true
   grep -RIE 'ccgram|tmux|claude|codex' /etc/cron* 2>/dev/null || true
   ```

2. Stop launcher first so it can shut down tmux cleanly:
   ```bash
   systemctl stop ccgram.service || true
   systemctl disable ccgram.service || true
   systemctl reset-failed ccgram.service || true
   systemctl daemon-reload
   ```

3. Kill leftovers only after graceful stop:
   ```bash
   pids=$(ps -eo pid=,cmd= | awk 'tolower($0) ~ /ccgram|tmux/ && $0 !~ /awk/ {print $1}' | tr '\n' ' ')
   [ -n "$pids" ] && kill $pids 2>/dev/null || true
   sleep 2
   left=$(ps -eo pid=,cmd= | awk 'tolower($0) ~ /ccgram|tmux/ && $0 !~ /awk/ {print $1}' | tr '\n' ' ')
   [ -n "$left" ] && kill -9 $left 2>/dev/null || true
   ```

4. Verify:
   ```bash
   ps -eo pid,ppid,user,stat,cmd | grep -Ei 'ccgram|tmux' | grep -v grep || true
   systemctl is-enabled ccgram.service 2>&1 || true
   systemctl is-active ccgram.service 2>&1 || true
   systemctl status ccgram.service --no-pager -l 2>&1 | sed -n '1,14p' || true
   ```

5. From a normal SSH shell, optionally archive and remove the launcher files:
   ```bash
   backup_dir="/root/decommissioned-services/ccgram-$(date -u +%Y%m%d-%H%M%S)"
   mkdir -p "$backup_dir"
   cp -a /etc/systemd/system/ccgram.service "$backup_dir/" 2>/dev/null || true
   cp -a /etc/systemd/system/ccgram.service.d "$backup_dir/" 2>/dev/null || true
   rm -f /etc/systemd/system/ccgram.service
   rm -rf /etc/systemd/system/ccgram.service.d
   rm -f /etc/systemd/system/multi-user.target.wants/ccgram.service
   systemctl daemon-reload
   ```

## Fleet outage triage

When multiple agents are suddenly down:

1. Stabilize the currently reachable agent first. Do not restart or update its Hermes gateway unless necessary.
2. Check local gateway, cron, and legacy bridge conflicts.
3. Check Tailscale peer state and SSH reachability for each agent.
4. Check known bot ownership. Do not reuse one Telegram bot token on two live gateways.
5. If the outage is due to shared host/dependency failure, recommend separate boxes for worker agents.
6. Save a short recovery plan under `~/.hermes/plans/` with hostnames, roles, bot handles, and smoke-test steps.

## Separate-box recommendation pattern

For resilient Appie-style fleets, prefer separate VPS instances for operationally distinct agents:

- Appie-2 style CMO/Herald: keep stable, avoid overloading with worker roles.
- Appie-3 style CTO/DevOps: dedicated VPS, at least 4 vCPU / 8 GB RAM, preferred 8 vCPU / 16 GB RAM for builds and infra checks.
- Appie-4 style worker/research/Ops: dedicated VPS, at least 2 vCPU / 4 GB RAM, preferred 4 vCPU / 8 GB RAM.

Provision clean Hermes installs, one Telegram bot token per gateway, Tailscale for private access, and watchdogs from a known-good agent.