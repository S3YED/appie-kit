# Appie-1 recovery example - 2026-05-11

## Scenario

Source host: Appie-2
Target host: Appie-1 over Tailscale

Symptoms:
- `appie-1` online on tailnet
- network path healthy
- SSH failed with `Permission denied (publickey,password,keyboard-interactive)`
- historical docs disagreed on hostname and username

## Live facts that mattered

- Working target: `appie-1`
- Tailscale IP: `100.101.29.56`
- Working remote user: `appie`
- Working source key: `/root/.ssh/id_ed25519`
- Verified remote identity after repair:
  - `hostname` → `mac.home`
  - `whoami` → `appie`
  - `pwd` → `/Users/appie`

## Minimal repair used

1. Confirmed host reachability and auth failure separately.
2. Used a transient password login for `appie@appie-1`.
3. Appended these public keys to `/Users/appie/.ssh/authorized_keys` idempotently:
   - `Appie-2@appie-brain`
   - `appie-2@weblyfe.nl`
4. Enforced permissions:
   - `chmod 700 ~/.ssh`
   - `chmod 600 ~/.ssh/authorized_keys`
5. Verified fresh outbound SSH from Appie-2 succeeded.
6. Repaired local `/root/.ssh/config` so plain `ssh appie-1` worked again.

## Key lesson

When Tailscale reachability is good but every tested key is rejected, the most efficient safe recovery is:
- use password auth once if the server still allows it
- restore `authorized_keys`
- verify a brand-new non-interactive SSH session from the source machine
- discard the password and do not store it
