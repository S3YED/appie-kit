# Appie-1 recovery note: connectivity vs auth

Date: 2026-05-26

## Situation
- Host: `appie-1` / Appie-1 Mac mini
- Documented Tailscale IP: `100.101.29.56`
- Expected user/key from prior repair notes: `appie` + `/root/.ssh/id_ed25519`

## Live probes from Appie-2
- `ssh -o BatchMode=yes -o ConnectTimeout=8 -i /root/.ssh/id_ed25519 appie@100.101.29.56 'hostname; whoami; pwd'`
  - Result: `ssh: connect to host 100.101.29.56 port 22: Connection timed out`
- `tailscale ping -c 3 100.101.29.56`
  - Timed out repeatedly
- `ssh appie@mac.home`
  - `Could not resolve hostname mac.home: Name or service not known`
- `ssh -6 ... appie@fd7a:115c:a1e0::7032:1d38`
  - Timed out on port 22

## Conclusion
This was **not** an SSH-auth problem. The live symptom set matched a reachability issue, likely one of:
- Mac mini asleep or powered off
- Tailscale stopped on the Mac mini
- Local network path broken
- Port 22 blocked / host offline

## Useful lesson
Before using break-glass auth steps, prove the host is reachable on the live network:
1. Tailscale peer visible is not enough
2. SSH timeout indicates a connectivity problem, not an auth problem
3. Only proceed to password/key repair once a shell path exists
