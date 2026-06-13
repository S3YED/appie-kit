# Remote host health/resource watchdog via Hermes cron

Use when the user wants periodic health checks for a machine reachable from the current Hermes host, especially a Mac mini reachable over SSH/Tailscale.

## Pattern

Create a small script under `~/.hermes/scripts/` and schedule it with Hermes cron using `no_agent=True`.

Why:
- A script-only cron job is cheaper and deterministic for threshold checks.
- Empty stdout means silent success. The user only receives alerts when something needs attention.
- The script can collect data over SSH without exposing raw secrets.

## Cron details

Hermes cron script paths must be relative to `~/.hermes/scripts/`.

Good:

```text
script="mac_mini_healthcheck.py"
```

Bad:

```text
script="/root/.hermes/scripts/mac_mini_healthcheck.py"
```

Use `no_agent=True` for watchdogs where the script itself prints the final message.

## macOS remote checks worth collecting

Read-only commands over SSH:

```bash
hostname
uname -a
uptime
df -h /
df -h /Users 2>/dev/null
vm_stat | head -20
memory_pressure 2>/dev/null | tail -20
sysctl vm.swapusage 2>/dev/null
ps -axo pid,pcpu,pmem,comm -r | head -12
ps -axo pid,pmem,pcpu,comm -m | head -12
launchctl print gui/$(id -u)/com.nousresearch.hermes-gateway 2>/dev/null | egrep 'state =|pid =|last exit code' || true
tmutil status 2>/dev/null | head -20 || true
```

## Network health extension

When the user asks for whole-network health, extend the same script rather than creating a second narrow watchdog. Keep it read-only and light:

```bash
route -n get default 2>/dev/null | egrep 'gateway|interface'
if=$(route -n get default 2>/dev/null | awk '/interface:/{print $2; exit}')
ipconfig getifaddr "$if" 2>/dev/null
scutil --dns 2>/dev/null | awk '/nameserver\[[0-9]+\]/{print $3}' | sort -u | head
ping -c 1 -W 1000 "$gateway"
python3 - <<'PY'
import socket
print(socket.gethostbyname('cloudflare.com'))
PY
```

Useful probes:
- Default gateway and active interface/local IP.
- Gateway ping, public IP ping, DNS resolve, and HTTPS probes to two stable endpoints.
- A light LAN ping sweep only on normal home-size subnets, for example `/24`; skip large networks to avoid noisy scanning.
- Tailscale status if installed, but do not alert merely because Tailscale is unavailable unless it is known to be required.

False-positive guard:
- Do not alert on a single ICMP failure when other evidence proves connectivity. Some routers or public endpoints rate-limit one-off pings.
- Treat gateway as reachable if the LAN sweep saw it even when the one-off gateway ping missed.
- Treat internet as healthy if DNS and at least one HTTPS probe succeeds even when `1.1.1.1` ping missed.

## Suggested thresholds

Keep routine alerts quiet and actionable:

- SSH failure: alert immediately.
- High load: alert when load is greater than `max(4.0, cpu_count * 1.5)`.
- Disk: alert at 85%+ by default. 80% is often too noisy for macOS data volumes.
- CPU drain: alert for a single process at 70%+ sustained in the sample.
- RAM drain: alert for a single process at 20%+ memory.
- Swap: alert only when multi-GB swap is actively used, for example 4GB+.
- Memory pressure: alert on macOS warning/critical indicators.

## Output rule

Print nothing when healthy. Print a concise alert with:

- Host
- Time
- Issues
- Snapshot: uptime/load, disk, top CPU, top RAM

This preserves Telegram signal-to-noise for periodic jobs.

## Pitfalls

- Do not judge Apple Silicon macOS health by a single short-lived Python process during the sampling run.
- macOS `/` and `/Users` can map to different APFS volumes. Check both if the task is about storage pressure.
- If the cron tool rejects the script path, move/use the file under `~/.hermes/scripts/` and pass only the filename.
- Prefer threshold tuning over noisy reports. A watchdog that messages on every run quickly becomes ignored.
