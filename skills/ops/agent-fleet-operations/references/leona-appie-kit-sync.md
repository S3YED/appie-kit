# Leona Appie-kit sync notes

Session lesson: the Leona Mac Studio was reachable on Tailnet and had SSH port 22 open, but the deploy script still failed until the SSH user was corrected.

## What mattered
- Tailnet reachability and SSH shell access are separate checks.
- The host accepted `zahedi@100.126.237.96`, not the script's original `S3YED` default.
- The deploy script succeeded once run with `LEONA_USER=zahedi`.

## Useful verification sequence
```bash
tailscale ping -c 1 100.126.237.96
nc -z -G 3 100.126.237.96 22
ssh -o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=10 zahedi@100.126.237.96 'whoami && hostname'
LEONA_USER=zahedi ~/bin/leona-appie-kit-deploy.sh
```

## Practical rule
For remote Mac deployments, do not trust the script's default login until a successful `ssh ... 'whoami'` proves the username.
