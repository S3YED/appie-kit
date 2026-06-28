---
name: github-operations
description: "Operate GitHub end to end with git, gh CLI, and REST: authentication, repository management, issues, pull requests, CI monitoring, code review, releases, labels, secrets, and project triage. Use for any GitHub workflow instead of loading narrow GitHub subskills separately."
---

# GitHub Operations

Use this umbrella for GitHub work. Prefer `gh` when authenticated and available; fall back to plain `git` plus REST API calls when `gh` is missing or the environment is headless.

## Start every workflow with discovery

```bash
git remote -v
gh auth status || true
gh repo view --json nameWithOwner,defaultBranchRef || true
```

Extract owner/repo from `origin` when `gh` is unavailable. Do not assume the current directory is the target repository.

## Authentication

Choose the least-friction method that fits the host:

1. Existing `gh` login: use `gh auth status` and `gh api`.
2. Headless `gh auth login --with-token` when the user provides a token.
3. Plain Git HTTPS with a credential helper or token-embedded remote when `gh` is unavailable.
4. SSH keys for persistent developer machines.

Reusable shell helpers from the old auth/code-review skills live in `scripts/gh-env.sh` when present.

## Repository management

Use for cloning, creating, forking, remotes, releases, secrets, settings, and repository metadata. See `references/github-api-cheatsheet.md` for REST endpoint patterns.

Common operations:

```bash
gh repo clone OWNER/REPO
gh repo create NAME --private --clone
gh repo fork OWNER/REPO --clone
gh release create v1.2.3 dist/* --notes "..."
```

## Issues

Use issues for bug reports, feature requests, triage, labels, milestones, and assignment.

```bash
gh issue list --state open
gh issue view 123 --comments
gh issue create --title "..." --body-file body.md
gh issue edit 123 --add-label bug --add-assignee @me
```

Templates are available under `templates/bug-report.md` and `templates/feature-request.md`.

## Pull request lifecycle

1. Sync default branch.
2. Create a focused branch.
3. Commit with a conventional message.
4. Push and open a PR with a clear body and test plan.
5. Monitor checks and fetch logs for failures.
6. Fix CI, update the branch, and merge only when policy allows.

Templates and references:

- `templates/pr-body-feature.md`
- `templates/pr-body-bugfix.md`
- `references/ci-troubleshooting.md`
- `references/conventional-commits.md`

## Code review

Review local diffs or GitHub PRs for correctness, regressions, security, tests, and maintainability. Load `references/review-output-template.md` for the preferred report shape.

```bash
gh pr view PR --json title,body,author,baseRefName,headRefName
gh pr diff PR
gh pr checkout PR
```

Verify every finding against code and tests before posting comments. Prefer one summary review over noisy inline comments unless line-specific context matters.

## Safety rules

- Ask before pushing, force-pushing, merging, deleting branches, changing repo settings, or posting public comments unless the user explicitly requested that action.
- Never print or store tokens in logs. Use env vars or `gh auth login --with-token`.
- For destructive repo operations, capture the target owner/repo and branch in the final confirmation.
