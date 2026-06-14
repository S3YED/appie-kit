# Fleet Access for Appie Kit

Use this guide when adding missing worker or client-bot hosts to a sanitized Appie Kit workflow. It is intentionally placeholder-only so the public repo stays safe.

## Goal

Give the local Appie Kit maintainer enough access to inventory skills from approved hosts such as:

- an external bot or worker host
- a GPU/media worker host
- an approved client-bot host

The goal is **skill inventory and curation**, not credential sharing. Never copy API keys, bot tokens, private memory, direct messages, client assets, or explicit/private content into Appie Kit.

## 1. Create a private access file

Copy the public template and fill it in privately:

```bash
cp configs/fleet-access.example.yml fleet-access.local.yml
chmod 600 fleet-access.local.yml
```

`fleet-access.local.yml` is ignored by git. Keep real hostnames, Tailscale IPs, usernames, bot handles, and SSH key paths out of public commits.

## 2. Add the maintainer public SSH key on each host

On each approved host, add the maintainer's public key to the target user's `authorized_keys`:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
printf '%s\n' 'ssh-ed25519 <public-key> <agent-comment>' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Use a public key only. Never copy private keys between machines.

## 3. Enable secure transport

### macOS hosts

```bash
sudo systemsetup -setremotelogin on
tailscale status
```

### Linux hosts

```bash
sudo systemctl enable --now ssh || sudo systemctl enable --now sshd
tailscale status
```

If a firewall is enabled, allow SSH on the Tailscale interface only. Do not expose SSH publicly.

## 4. Add private SSH aliases locally

Add aliases to your private `~/.ssh/config`, not to this repo:

```sshconfig
Host external-worker
    HostName <external-worker-tailscale-name-or-ip>
    User <external-worker-ssh-user>
    IdentityFile ~/.ssh/<private-key-name>
    IdentitiesOnly yes

Host gpu-worker
    HostName <gpu-worker-tailscale-name-or-ip>
    User <gpu-worker-ssh-user>
    IdentityFile ~/.ssh/<private-key-name>
    IdentitiesOnly yes

Host client-bot-host
    HostName <client-bot-host-tailscale-name-or-ip>
    User <client-bot-host-ssh-user>
    IdentityFile ~/.ssh/<private-key-name>
    IdentitiesOnly yes
```

## 5. Prove access before pulling anything

Run each gate separately:

```bash
tailscale ping -c 3 <host>
nc -z -G 3 <host> 22
ssh -o BatchMode=yes -o ConnectTimeout=10 <host> 'whoami && hostname'
```

Do not run sync or copy commands until `whoami && hostname` proves the intended user and machine.

## 6. Pull manifests first, not files

Start with a remote manifest. This avoids copying private material just to discover what exists.

```bash
ssh <host> 'python3 - <<"PY"
from pathlib import Path
import hashlib, json, re
roots = [Path.home()/".hermes/skills", Path.home()/".openclaw/skills"]
rows = []
for root in roots:
    if not root.exists():
        continue
    for skill in root.rglob("SKILL.md"):
        text = skill.read_text(errors="ignore")
        name = None
        desc = None
        m = re.match(r"^---\n(.*?)\n---", text, re.S)
        if m:
            for line in m.group(1).splitlines():
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip("\"'")
                if line.startswith("description:"):
                    desc = line.split(":", 1)[1].strip().strip("\"'")
        rows.append({
            "root": str(root),
            "path": str(skill.parent.relative_to(root)),
            "name": name or skill.parent.name,
            "description": desc or "",
            "sha256": hashlib.sha256(text.encode()).hexdigest(),
        })
print(json.dumps(rows, indent=2))
PY' > manifests/<host>-skills.json
```

Create `manifests/` locally as a private working directory unless the manifest has been reviewed and sanitized.

## 7. Curate before importing

For each candidate skill:

1. Compare name and SHA-256 against existing Appie Kit skills and stock Hermes skills.
2. Skip exact duplicates.
3. Quarantine questionable skills outside the repo.
4. Exclude private, client-specific, explicit, paid-course, or credentials-related content.
5. Convert reusable operational knowledge into a generic skill with placeholders.
6. Re-run the public validation and leak scans before committing.

## Host-specific rules

### External worker hosts

Treat external worker hosts as inventory sources first. Pull manifests first, then import only reusable, public-safe skills. Replace names, hostnames, project paths, and bot handles with placeholders.

### GPU/media worker hosts

Treat GPU/media worker hosts as specialized workers. Before any operational work, run the host's private health or hardening checklist if one exists. Appie Kit may include generic GPU/media workflows, but never publish private model caches, prompts, generated client assets, credentials, or Tailscale endpoints.

### Client-bot hosts

Treat client-bot hosts as inventory sources only unless the owner explicitly approves sync-back. Do not publish direct-message context, client data, explicit/NSFW content, bot tokens, private memory, or raw client-bot logs. If unsure, leave the material on the origin host and document only a sanitized count.

## Publish gate

Before pushing Appie Kit to GitHub:

```bash
python3 tools/validate-public-skills.py
gitleaks detect --source . --no-git --redact
```

The publish gate must show:

- unique skill names
- no missing frontmatter descriptions
- no hardcoded secrets
- no private hostnames, Tailscale IPs, bot handles, user home paths, or client identifiers
- no quarantine directory inside the repo
