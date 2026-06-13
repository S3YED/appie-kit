# Hermes safe update: preserve local adjustments

Use when updating a production-like Hermes install that may have user-owned config, cron jobs, skills, memory, or local source patches.

## Discovery checklist

Before updating, inspect both the source checkout and Hermes home:

```bash
cd /usr/local/lib/hermes-agent  # or the detected project root
hermes --version
hermes config path
hermes config env-path
git status --short --branch
git diff --stat
git remote -v
git stash list --format='%gd %H %s'
hermes profile list
hermes cron list
```

When the user asks to "self scan", "download the new repo", or "compare before updating", create a separate clean upstream checkout instead of pulling into the live repo:

```bash
mkdir -p /root/hermes-update-audit
cd /root/hermes-update-audit
rm -rf hermes-agent-upstream
git clone --depth 1 git@github.com:NousResearch/hermes-agent.git hermes-agent-upstream

cd /usr/local/lib/hermes-agent
git rev-parse HEAD
git rev-parse --abbrev-ref HEAD
git status --short --branch
git diff --name-status
git diff > /root/hermes-update-audit/local-source-adjustments.patch

# Compare changed local files against upstream versions without mutating production.
for f in $(git diff --name-only); do
  [ -f "/root/hermes-update-audit/hermes-agent-upstream/$f" ] && \
    diff -u "$f" "/root/hermes-update-audit/hermes-agent-upstream/$f" \
      > "/root/hermes-update-audit/compare-${f//\//__}.diff" || true
done
```

Use the clean checkout only for inspection, code comparison, and planning. Do not run the gateway from the audit checkout, and do not copy files over the live checkout blindly.

Key persistent state usually lives under `~/.hermes` or the active profile home, not in the git checkout:

- `config.yaml`
- `.env`
- `auth.json`
- `gateway_state.json`
- `channel_directory.json`
- `cron/jobs.json`
- `scripts/`
- `skills/`
- `memories/`
- `state.db`
- `sessions/`

## Backup pattern

Use Hermes' own pre-update backup and also save source patches explicitly when the git tree is dirty:

```bash
mkdir -p ~/hermes-update-backups

# Persistent runtime data, excluding bulky/generated caches and logs.
tar --exclude="$HOME/.hermes/cache" \
    --exclude="$HOME/.hermes/audio_cache" \
    --exclude="$HOME/.hermes/logs" \
    -czf ~/hermes-update-backups/hermes-home-$(date +%Y%m%d-%H%M%S).tar.gz \
    -C "$HOME" .hermes

# Local source modifications.
cd /usr/local/lib/hermes-agent
git diff > ~/hermes-update-backups/hermes-local-source-adjustments-$(date +%Y%m%d-%H%M%S).patch
```

Copy any untracked local files that matter, because a patch only covers tracked-file diffs:

```bash
git ls-files --others --exclude-standard
# then cp -a the needed files into ~/hermes-update-backups/
```

## Update command

Prefer an interactive SSH session for production gateways with local source changes:

```bash
hermes update --backup
```

`hermes update --backup` creates a full pre-update Hermes-home backup when possible, then updates code, dependencies, skills, config defaults, and restarts gateways.

## Local source change pitfall

Hermes update auto-stashes dirty git trees, including untracked files. If the install is far behind or the modified file is on a hot path, do not blindly restore the stash during update. When prompted:

```text
Restore local changes now? [Y/n]
```

Default to `n` if the local patch is a workaround or old source adjustment. First update cleanly, then inspect whether the workaround is still needed and port it deliberately.

Post-update inspection:

```bash
hermes --version
hermes doctor
hermes gateway status
hermes cron list
git status --short
git stash list --format='%gd %H %s'
```

If needed, inspect the saved stash or patch before applying:

```bash
git stash show -p stash@{0} -- path/to/file.py
# or review ~/hermes-update-backups/*.patch
```

## Communication pattern

When advising the user, separate:

1. What Hermes update preserves automatically (`~/.hermes` runtime state, skills sync keeping user-modified skills).
2. What can conflict (`/usr/local/lib/hermes-agent` local source modifications).
3. Exact commands for backup, update, and post-update verification.
4. Which prompt response is safest for the detected situation.
