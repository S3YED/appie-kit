# SSH transport vs auth: Leona session note

Session lesson: an SSH port can be open while public-key auth is still rejected. Treat these as separate gates during remote provisioning.

## Symptom pattern
- `tailscale ping` succeeds
- `nc -z <host> 22` succeeds
- `ssh -o BatchMode=yes <user>@<host> 'whoami'` fails with `Permission denied (publickey,password,keyboard-interactive)`

## What to verify next
1. Confirm the remote user is correct.
2. Confirm the intended public key is present in `~/.ssh/authorized_keys` on the target.
3. Confirm the local client is offering the intended private key with `ssh -vvv`.
4. Re-run the deploy script after auth succeeds.

## Local key source used in this session
- `~/.ssh/id_ed25519.pub`
