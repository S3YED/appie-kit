---
name: ssh-access-recovery
description: Restore SSH access when the host is reachable but authentication fails. Diagnose the real failure mode, use the smallest safe break-glass path, convert back to key-based auth, and verify from the source machine.
---

# SSH Access Recovery

Use this when a machine is online and reachable, but `ssh` login fails due to username drift, key mismatch, missing trust, or stale local config.

## Triggers

- `Permission denied (publickey...)` on a host that is otherwise reachable
- Tailscale node is online, ping works, but shell access fails
- Historical docs disagree about hostname, username, or identity file
- You have a temporary password or console path and want to convert back to SSH keys immediately

## Goal

Recover the smallest working SSH path without leaving secrets behind, then make the result easy to reuse.

## Workflow

1. **Confirm network reachability first**
   - Verify the node is online and addressable.
   - For Tailscale hosts, confirm the live tailnet name and IP.
   - Separate **network failure** from **auth failure** before changing anything.
   - If SSH times out or Tailscale ping times out, stop the auth-recovery path and classify it as a connectivity or power-state problem first.
   - If you are considering a sibling machine as a relay or jump host, verify *that* host is itself online and SSH-reachable before depending on it. A healthy-looking tailnet peer that also times out cannot serve as a recovery path.

2. **Inspect local SSH assumptions**
   - Read `~/.ssh/config`.
   - Check host alias expansion with `ssh -G <host>`.
   - Identify candidate users and identity files already present locally.
   - Do not assume docs are current if live tests disagree.

3. **Prove the failure mode with non-interactive tests**
   - Test likely user/key combinations with `BatchMode=yes` and short timeouts.
   - Prefer explicit tests over guessing.
   - Record whether failure is:
     - unreachable host
     - wrong hostname
     - wrong username
     - wrong key selection
     - server-side key trust missing

4. **Use the smallest safe break-glass path**
   - If the host still allows password auth and the user provides credentials, use them transiently.
   - Do **not** save passwords to memory, notes, or skills.
   - Treat password login as a one-time repair path only.

5. **Convert immediately back to key-based auth**
   - On the remote host:
     - create `~/.ssh` if needed
     - set `chmod 700 ~/.ssh`
     - create or update `~/.ssh/authorized_keys`
     - set `chmod 600 ~/.ssh/authorized_keys`
   - Append the required public key(s) idempotently.
   - Prefer `grep -qxF ... || printf '%s\n' ... >> ~/.ssh/authorized_keys` to avoid duplicates.

6. **Verify from the source host, not just inside the remote shell**
   - Exit or ignore the interactive repair session.
   - Run fresh non-interactive SSH from the originating machine.
   - Verify with:
     - `hostname`
     - `whoami`
     - `pwd`
   - Test both:
     - explicit `user@host`
     - the intended alias, if one should exist

7. **Repair local usability after remote auth works**
   - If needed, add or fix the local `~/.ssh/config` host entry.
   - Keep the entry minimal:
     - `HostName`
     - `User`
     - `IdentityFile`
     - `IdentitiesOnly yes`
     - `StrictHostKeyChecking no` only if that is already the local convention
   - Back up protected config files before rewriting them.

8. **Document the working path without secrets**
   - Save:
     - working hostname/IP
     - working username
     - working identity file
     - verification result
   - Do not store passwords.

## Recommended command patterns

### Check alias expansion
```bash
ssh -G appie-1 | egrep '^(hostname|user|identityfile|identitiesonly|stricthostkeychecking) '
```

### Test non-interactive SSH
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 appie@appie-1 'hostname; whoami; pwd'
```

### Idempotently add a key remotely
```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
 touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
 grep -qxF 'ssh-ed25519 AAAA... comment' ~/.ssh/authorized_keys || \
   printf '%s\n' 'ssh-ed25519 AAAA... comment' >> ~/.ssh/authorized_keys
```

## Pitfalls

- **Do not confuse reachability with access.** Ping/Tailscale success does not mean SSH trust is correct.
- **Do not trust stale docs over live host facts.** Hostnames, Tailscale names, and users drift.
- **Do not stop after entering with a password.** The real finish line is restored key-based login from the source machine.
- **Do not save transient credentials** in memory, plaintext notes, or skills.
- **Do not only verify inside the remote shell.** Always run a fresh outbound SSH after the fix.
- **Do not overwrite SSH config blindly.** Back it up first and keep edits minimal.

## Verification checklist

- [ ] Host is reachable on the network/tailnet
- [ ] Correct remote username identified
- [ ] Required public key exists in remote `authorized_keys`
- [ ] Permissions on `~/.ssh` and `authorized_keys` are correct
- [ ] Fresh non-interactive SSH works from the source host
- [ ] Local alias works if one is expected
- [ ] No password was stored in notes, memory, or skill files

## Session-specific reference

See:
- `references/appie1-recovery-2026-05-11.md` for a concrete Tailscale + macOS recovery example where a transient password was used only once to restore Appie-2 key trust and then discarded.
- `references/appie1-connectivity-vs-auth.md` for a later case where SSH and Tailscale both timed out, showing this skill must stop at connectivity classification when no shell path exists.
