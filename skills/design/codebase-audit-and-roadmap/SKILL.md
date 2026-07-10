---
name: codebase-audit-and-roadmap
description: "Audit a codebase from a user reference and produce a structured feature inventory, gap analysis, and build-plan PRD."
version: 1.0.0
author: Appie-2
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [codebase-audit, feature-inventory, gap-analysis, prd, planning]
    related_skills: [writing-plans, codebase-inspection]
---

# Codebase Audit & Roadmap

When a user names a project and asks "what's in it" / "what's next" / "make a PRD" / "audit this" — this skill covers the full discovery-to-plan workflow.

## When to Use

- User says "check this repo" or "audit this project"
- User names a project and asks for a feature summary or to "make a PRD"
- User asks for a gap analysis before a launch/rebuild
- User references a project you haven't encountered before and needs structured analysis

## Workflow

### Phase 1 — Locate the Project

1. **Ask / clarify what they mean** — get a name, repo URL, or GitHub handle
2. **Search locally**: `find ~ -maxdepth 4 -name ".git" -type d`
3. **Search GitHub**: use web_search with `site:github.com <handle>` patterns. Try known handles (S3YED, weblyfe, etc.)
4. **Try multi-case variations** — the exact case matters on GitHub. If user says "wai", search `S3YED/wai`, `s3yed/WAI`, etc.
5. **Clone private repos via SSH** if SSH key is configured (`ssh -T git@github.com` to verify)
6. **Fallback**: ask for the exact URL if web search fails

### Phase 2 — Codebase Analysis (Systematic)

Read in this order, top to bottom:

1. **README.md** — overall purpose, features, stack, setup
2. **AGENTS.md / CLAUDE.md / SKILL.md** — project-specific instructions for agents
3. **package.json** — dependencies, build scripts, test commands (run `npm ls 2>/dev/null | head`)
4. **Git log** — `git log --oneline -10 --all` — recent activity, branch structure
5. **Project structure** — `find src -maxdepth 2 -type d | sort`, or list top-level files
6. **Key feature files** — read every component/API/hook file systematically:
   - `api/*.ts` — serverless endpoints (feature surface)
   - `components/*.tsx` — UI screens (feature surface)
   - `utils/*.ts` — shared logic
   - `hooks/*.ts` — custom hooks
   - `migrations/*.sql` — DB schema
7. **Types/interfaces** — the data model tells you the domain
8. **Tests** — `npm test` or `vitest run` — test coverage is a health signal
9. **Docs/ directory** — PRDs, architecture docs, integration guides
10. **Existing PRDs** (`docs/*PRD*.md`, `docs/*PLAN*.md`) — read first to compare intent vs reality

### Phase 3 — Deployment Audit (SaaS projects)

For Vercel-deployed apps:

1. `cd <project> && vercel link --yes` to link the local clone to Vercel
2. Read `.vercel/project.json` for projectId + orgId
3. Check deployments: `vercel list --prod` or `vercel list`
4. Check env vars: `vercel env ls`
5. If CLI is limited, use Vercel REST API:
   ```
   curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
     "https://api.vercel.com/v1/projects/<projectId>/env?teamId=<orgId>"
   ```
   (Write response to file, parse with python3 to avoid shell quoting issues)

For Supabase projects:
- Look for `SUPABASE_URL` in env files or Vercel env
- Check if `migrations/000_base_schema.sql` has been run

### Phase 4 — Feature Inventory + Gap Analysis

For every feature found, classify:

| Status | Meaning |
|---|---|
| ✅ Complete | Fully implemented, tested, wired |
| 🟡 Partial | Code exists but not wired (e.g. UI component with no trigger, API without route) |
| 🔴 Missing | Referenced in PRD/docs but no code found |
| ❌ Broken | Code exists but has known issues (e.g. always-`[]` state, in-memory-only) |

Build a table with: Feature | Status | File(s) | Notes

### Phase 5 — Produce PRD / Build Plan

Structure the output PRD as a markdown document in `docs/`:

```markdown
# [Project Name] — [Launch Name] Build Plan

## 1. Current State Assessment

[Feature table from Phase 4]

## 2. [Phase Name — e.g. P2: Voice Notes]

### What already exists
[Code that exists but may not be wired]

### What to build
[Items with file paths, clear deliverables]

## 3. Build Order

Use a priority system:
- **[Phase 1 — Launch-ready]**: P0 items that must work for go-live
- **[Phase 2 — Production Hardening]**: P1 items for reliability/security
- **[Phase 3 — Scale]**: P2 items for multi-tenant scale
- **[Phase 4 — Polish]**: P3 nice-to-haves

## 4. One-Command Vision

[If applicable: describe the ideal provisioning flow]

## 5. Decisions Needed

[Questions for the user/operator]
```

Save to `docs/<PROJECT>-LAUNCH-PLAN.md` and present a concise summary in the reply.

## Pitfalls

1. **Don't assume features work just because the code exists.** A component may be dead code (no import/trigger). An API may exist but the state that feeds it may never be populated. Always trace the data flow: where is the state set, where is it consumed.
2. **Demo-mode == broken, not working.** If an app silently falls back to fake data when env vars are missing, call it a stability bug, not a feature.
3. **Rate limiting on serverless is always in-memory until proven otherwise.** Vercel cold starts reset in-memory Maps.
4. **Feature-rich does not mean deployed.** A project can have massive feature surface but zero deployments on Vercel.
5. **Private repos won't show in web search.** Try cloning with `git@github.com:<handle>/<repo>.git` after verifying SSH auth.
6. **Shell quoting with env vars containing special chars is fragile.** Write Python scripts to files for complex API calls; avoid interpolating env vars directly in shell commands.
7. **Verbal feature names may not match repo names.** "WAI" = WhatsApp Intelligence, not a tool called "wai". Ask for clarification.