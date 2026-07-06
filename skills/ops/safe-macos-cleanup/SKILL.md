---
name: safe-macos-cleanup
description: Evidence-first safe macOS storage cleanup. Use when freeing disk space, cleaning caches, clearing temp/log files, handling System Data/purgeable space, Time Machine local snapshots, developer caches, or recovering from a nearly full Mac disk without deleting source/projects or secrets.
---

# Safe macOS Cleanup

Use this skill to reclaim disk space without breaking projects, losing private data, or deleting credentials. Prefer evidence, dry-runs, and reversible actions. Do not use broad `rm -rf` over home, project, Library, or system directories.

## Safety rules

1. Diagnose before deleting: collect `df`, largest directories, and cache sizes first.
2. Delete only known regenerated caches, old logs, and temp files. Preserve source code, project data, downloads, model caches, backups, and credentials unless the user explicitly approves that exact target.
3. Prefer tool-native clean commands before file deletion: `npm cache clean --force`, `brew cleanup -s`, `uv cache prune`, `pip cache purge`, package-manager cache commands.
4. Use `trash` for user-owned non-cache files. Use direct deletion only for cache/temp/log paths that are explicitly safe to regenerate.
5. Never delete:
   - `~/.ssh`, `~/.gnupg`, `~/.1password`, keychains, `.env*`, credential/config directories.
   - active project folders, git repos, `node_modules` inside active repos without approval.
   - `~/Library/Messages`, `~/Library/Mail`, `~/Library/Application Support`, browser profiles, Photos libraries.
   - `/System`, `/usr`, `/bin`, `/sbin`, `/private/var/db`, `/Library/Keychains`.
6. For nearly full disks, keep scope small and verify after each batch.

## Evidence-first checklist

Run read-only checks first:

```bash
df -h /
du -sh ~/.cache ~/Library/Caches ~/Library/Logs ~/.hermes/cache ~/.hermes/tmp 2>/dev/null
```

Find top-level heavy areas without descending into every project:

```bash
du -xhd 1 ~ 2>/dev/null | sort -h | tail -30
du -xhd 1 ~/Library 2>/dev/null | sort -h | tail -30
```

If `System Data`/purgeable space seems wrong, inspect Time Machine snapshots:

```bash
tmutil listlocalsnapshots / 2>/dev/null || true
```

## Safe cleanup order

### 1. Package/tool caches

These are usually regenerated automatically:

```bash
npm cache clean --force 2>/dev/null || true
rm -rf ~/.npm/_npx 2>/dev/null || true
uv cache prune 2>/dev/null || true
pip cache purge 2>/dev/null || true
pnpm store prune 2>/dev/null || true
go clean -cache -modcache 2>/dev/null || true
brew cleanup -s 2>/dev/null || true
```

Notes:
- `brew cleanup -s` removes old downloads and stale versions, not installed current packages.
- `pnpm store prune` may make future installs slower but should not break checked-out source.
- `go clean -modcache` forces re-downloads later.

### 2. Browser/test automation caches

Safe when browsers can be reinstalled:

```bash
rm -rf ~/Library/Caches/ms-playwright 2>/dev/null || true
rm -rf ~/Library/Caches/puppeteer 2>/dev/null || true
rm -rf ~/Library/Caches/puppeteer-* 2>/dev/null || true
rm -rf ~/Library/Caches/camoufox 2>/dev/null || true
rm -rf ~/.cache/ms-playwright ~/.cache/puppeteer ~/.cache/camoufox 2>/dev/null || true
```

### 3. App/user caches and logs

Target old or obvious cache files. Avoid deleting whole app support directories.

```bash
find ~/Library/Logs -type f -mtime +14 -delete 2>/dev/null || true
find ~/.hermes/logs -type f -mtime +14 -delete 2>/dev/null || true
rm -rf ~/.hermes/tmp/* ~/.hermes/cache/* ~/.hermes/audio_cache/* 2>/dev/null || true
```

Only clear `~/Library/Caches/*` selectively when a specific cache is large and non-critical. Do not wipe the directory blindly while apps are running.

### 4. Time Machine local snapshots

Apple documents local snapshots as Time Machine restore points stored on the Mac and managed automatically. Treat manual pruning as optional and only use it when disk pressure persists after cache cleanup.

Read-only:

```bash
tmutil listlocalsnapshots /
```

Gentle thinning example, asks Time Machine to free about 20 GB with urgency 4:

```bash
sudo tmutil thinlocalsnapshots / 20000000000 4
```

Do not delete snapshots one by one unless the user explicitly accepts losing those local restore points.

## Verification

After cleanup:

```bash
df -h /
du -sh ~/.cache ~/Library/Caches ~/.hermes/cache ~/.hermes/tmp 2>/dev/null
```

Report:
- free space before and after
- exact categories cleaned
- anything intentionally skipped
- remaining big candidates that need approval

## Research basis

Exa search, 2026-06, surfaced these reliable points:
- Apple Support recommends checking Storage settings, using built-in storage recommendations, and deleting/moving known unneeded files.
- Apple Support describes Time Machine local snapshots as automatic local restore points; they are generally managed by macOS and should not be manually removed casually.
- macOS purgeable/System Data space can be tied to APFS/Time Machine snapshots; thinning is safer than wholesale deletion.
- Community and utility patterns converge on dry-run first, interactive confirmation, and limiting cleanup to regenerated caches: package manager caches, browser automation caches, old logs, temp files.
