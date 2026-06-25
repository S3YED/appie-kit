---
name: fleet-self-review
description: Daily fleet self-review — audit the Appie fleet for safety, errors/fabrications, and improvement opportunities; propose fixes and author custom skills capturing the learning. Read-only on systems; only writes reports + skills. Use when running the daily self-review routine (cron) or on demand.
---

# Fleet Self-Review (daily)

Goal: keep the fleet **safe**, **minimise repeated errors**, **improve**, and **capture learnings as custom skills** — without taking any risky action itself.

## Hard safety rules (non-negotiable)
- READ-ONLY on all systems. NO git push, NO deploys, NO `rm`/`trash` of anything you did not create this run, NO edits to code/config outside the two write targets below.
- WRITE TARGETS (the only places you may create/modify files):
  1. `~/clawd/reports/fleet-self-review/` — the dated report.
  2. `~/clawd/skills/` — new or improved custom skills (additive; never delete an existing skill).
- NO sending to third parties. The ONLY outbound message is the end-of-run Telegram summary to Seyed (the runner script handles it).
- NO secret access beyond reading config you already have; NEVER print secrets into the report or the summary.
- If a proposed fix is destructive or outward-facing, DO NOT do it — write it as a recommendation for Seyed to approve.
- Token discipline: reference paths/IDs, no state dumps. Keep the report tight.

## Inputs to review (gather, read-only)
1. **Recent memory + observations** — `~/clawd/memory/` (today + last 2 days), `~/clawd/MEMORY.md` index, and claude-mem if available.
2. **Errors & fabrications** — scan recent session memory/logs for: fabricated output (claims of success not backed by real tool output), stale-shell/cache symptoms, retractions, repeated failures. This is the top priority (see the fabrication incidents on 2026-06-02).
3. **Missed / stalled tasks** — Notion "Task List" (canonical), any `tasks.json`, open obligations in daily notes.
4. **Cron / automation health** — `~/Library/LaunchAgents/com.weblyfe.*`, recent `~/clawd/logs/**`, which jobs are disabled or failing. Check for 0-byte cron output files (`ls -la ~/clawd/logs/security-scan-*.log` etc.) — a 0-byte file means a job fires but produces no output, which is a silent failure, not a clean pass. Also verify pipeline last-success timestamps: if `invoice-pipeline.jsonl` or `sync-status.json` show no entry in >48h, the pipeline is broken even if the cron job "ran".
5. **Fleet reachability** — `tailscale status` (which nodes online/offline). Read-only; do NOT ssh-mutate.
6. **Repo hygiene** — `git status` in active repos (uncommitted/secret risks); flag, don't fix.

## What to produce
Write `~/clawd/reports/fleet-self-review/<YYYY-MM-DD>.md` with:
- **Safety** — any red lines crossed or at risk (fabrication, secret exposure, public exposure, destructive risk). Most important section.
- **Errors to minimise** — concrete recurring errors with root cause + the cheapest durable fix.
- **Improvements** — prioritised, concrete, each with the file/command to apply (for Seyed or a future run to action).
- **Custom skills authored/updated this run** — list them with one-line purpose. Author a skill ONLY when a learning is reusable and durable (e.g. a recurring-error guard). Follow the skills format; keep skills small and specific.
- **Open obligations** — dated follow-ups, flags, gates.
- Keep it scannable. Cite real paths/IDs. No fabrication — if you didn't verify something, say "unverified".

## Authoring custom skills (the improvement loop)
When you find a recurring, durable failure or a reusable best-practice, write a skill under `~/clawd/skills/<kebab-name>/SKILL.md` with proper frontmatter (`name`, `description`). Prefer guard-rail skills that prevent the errors you found (e.g. "verify-before-claiming-success", "never-relay-uncaptured-output"). Do not duplicate an existing skill — improve it in place instead.

## Self-check before finishing
"Did I change anything outside reports/ and skills/? Did I claim anything I didn't verify? Did I leak a secret?" If yes to any, undo/redact before writing the summary.
