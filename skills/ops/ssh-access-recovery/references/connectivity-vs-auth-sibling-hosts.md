# Connectivity vs Auth: Sibling Host Relay Check

Session takeaway:
- A Tailscale peer can appear in `tailscale status` yet still be unusable as a relay if it is not actually reachable on port 22.
- In this session, both the target Mac mini and a candidate sibling Mac mini timed out over SSH and Tailscale ping.
- Lesson: do not treat a sibling Mac as a recovery path until you have verified *that* host is online and SSH-reachable.

Practical decision rule:
1. Check the target host.
2. If target times out, check whether a known sibling or jump host is reachable.
3. If the sibling also times out, stop auth-recovery work and classify the issue as network/power-state/out-of-band access required.

Useful probes:
- `tailscale status --json` to confirm live peer identity
- `tailscale ping <ip-or-host>` to check tailnet reachability
- `ssh -o BatchMode=yes -o ConnectTimeout=8 user@host 'hostname; whoami; pwd'` to distinguish transport from auth

Do not confuse:
- peer visibility in Tailscale status
- with actual SSH availability

This is a recovery classification aid, not a guarantee that the machine is down.
