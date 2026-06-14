# Cross-machine provisioning note

Session lesson: a Tailscale ping can succeed while SSH is still refused. For remote agent deploys, treat network reachability and shell reachability as separate gates.

## Preflight order
1. Verify Tailnet reachability.
2. Verify SSH port reachability with `nc` or `ssh -o BatchMode=yes`.
3. Run the deploy script in `--dry-run` mode.
4. Only then do the rsync / install / persona writes.

## Why this matters
- Tailnet reachability only proves the node is visible on the overlay network.
- SSH may still be disabled, blocked, or not yet configured on the remote host.
- VNC / screen sharing can fail independently too, so check each service explicitly if the target depends on it.

## Remote Mac examples
```bash
tailscale ping -c 3 100.126.237.96
nc -z -G 3 100.126.237.96 22
nc -z -G 3 100.126.237.96 5900
```

If SSH is refused, fix Remote Login on the target before retrying the deploy. Do not assume Tailscale connectivity implies SSH readiness.
