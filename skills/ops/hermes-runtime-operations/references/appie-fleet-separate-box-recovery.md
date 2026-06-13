# Appie fleet separate-box recovery pattern

Use this reference when several Appie agents are down, a user reports fleet fragility, or a legacy OpenClaw/ccgram bridge may be competing with Hermes gateways.

## Durable lesson

When multiple agents go down, treat it as a fleet resilience problem, not only a single service restart.

Preferred architecture:

- Appie-2 stays stable as CMO/Herald on its current VPS.
- Appie-3 CTO/DevOps should run on a dedicated VPS.
- Appie-4 Worker/Research/Ops should run on a separate dedicated VPS.
- Do not pile critical agents onto one host unless it is explicitly a temporary recovery bridge.

## Scan pattern

1. Check live process/service owners for legacy bridges:

```bash
ps aux | grep -Ei 'openclaw|ccgram|tmux|telegram|hermes' | grep -v grep || true
systemctl list-units --all --type=service --no-pager | grep -Ei 'openclaw|ccgram|hermes|telegram' || true
systemctl --user list-units --all --type=service --no-pager | grep -Ei 'openclaw|ccgram|hermes|telegram' || true
```

2. Check Tailscale reachability:

```bash
tailscale status
tailscale ping --timeout=3s --c 2 <tailnet-name-or-ip>
```

3. Check Hermes state:

```bash
hermes --version
hermes gateway status
hermes gateway list
hermes profile list
hermes cron list
```

4. Check machine capacity:

```bash
uptime
free -h
df -hT /
ps -eo pid,user,pcpu,pmem,rss,cmd --sort=-pmem | head
```

## Legacy bridge cleanup

If `ccgram` or `openclaw-gateway` owns a bot token that should move to Hermes, stop and disable it before configuring Hermes with that token.

```bash
systemctl stop ccgram.service 2>/dev/null || true
systemctl disable ccgram.service 2>/dev/null || true
systemctl --user stop openclaw-gateway 2>/dev/null || true
systemctl --user disable openclaw-gateway 2>/dev/null || true
ps aux | grep -Ei 'openclaw|ccgram|tmux' | grep -v grep || true
```

If running from a Telegram/gateway-triggered Hermes tool shell, system paths such as `/etc/systemd/system` may be read-only because of gateway hardening. In that case, stop/disable what you can, then do full unit-file removal later from normal SSH.

## New-box build order

1. Keep Appie-2 stable.
2. Rebuild Appie-3 first, because DevOps capability speeds up recovery.
3. Rebuild Appie-4 second.
4. Add watchdogs from Appie-2 to the new boxes.
5. Update shared brain/fleet docs.

## Recommended specs

Appie-3 CTO/DevOps:

- Minimum: 4 vCPU, 8 GB RAM, 80 GB disk, Ubuntu 24.04 LTS
- Preferred: 8 vCPU, 16 GB RAM, 160 GB disk

Appie-4 Worker/Research/Ops:

- Minimum: 2 vCPU, 4 GB RAM, 60 GB disk, Ubuntu 24.04 LTS
- Preferred: 4 vCPU, 8 GB RAM, 80 GB disk

## Documentation sync pattern

If appie-brain is dirty or heavily diverged, do not pull into it directly. Use a fresh clone, write the cookbook/recovery docs there, review for secrets, commit, push, then verify `HEAD == origin/master`.

Current class-level docs created from this pattern in appie-brain:

- `appies/HERMES_APPIE_COOKBOOK.md`
- `appies/recovery/2026-06-12-appie-3-4-separate-boxes-recovery.md`

## User expectation

Seyed feels fleet outages acutely and expects practical, direct recovery work with concrete verification, not generic reassurance. Report what was checked, what changed, what remains blocked, and the next operational move.
