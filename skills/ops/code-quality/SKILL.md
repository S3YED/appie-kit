---
name: code-quality
description: "Code quality and verification: codebase metrics, post-implementation cleanup, and pre-commit verification pipeline."
version: 1.0.0
author: Hermes Agent Curator
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [code-quality, code-review, verification, metrics, static-analysis, linting, security, cleanup]
    related_skills: [test-driven-development, development-workflow, github-code-review]
---

# Code Quality & Verification

Three complementary tools for ensuring code quality at different stages of development:

| Mode | When | Tool | What it does |
|------|------|------|-------------|
| **Codebase Metrics** | Explore/adopt a repo | `pygount` | Analyze LOC, language breakdown, code-vs-comment ratios |
| **Simplify Code** | After implementing changes | 3 parallel subagents | Clean up recent changes for reuse, quality, efficiency |
| **Pre-Commit Verification** | Before `git commit` | Automated pipeline | Security scan, quality gates, independent reviewer, auto-fix |

---

## Section 1: Codebase Metrics (pygount)

Analyze repositories for lines of code, language breakdown, file counts, and code-vs-comment ratios.

### When to Use

- User asks for LOC (lines of code) count
- User wants a language breakdown of a repo
- User asks about codebase size or composition
- General "how big is this repo" questions

### Prerequisites

```bash
pip install --break-system-packages pygount 2>/dev/null || pip install pygount
```

### Basic Summary

```bash
cd /path/to/repo
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  .
```

**IMPORTANT:** Always use `--folders-to-skip` to exclude dependency/build directories, otherwise pygount will crawl them and hang.

### Common Folder Exclusions

```bash
# Python projects
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JavaScript/TypeScript projects
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"
```

### Filter by Language

```bash
# Only count Python files
pygount --suffix=py --format=summary .

# Only count Python and YAML
pygount --suffix=py,yaml,yml --format=summary .
```

### Output Formats

```bash
pygount --format=summary .        # Summary table
pygount --format=json .           # JSON for programmatic use
```

### Interpreting Results

The summary table columns: **Language**, **Files**, **Code** (executable lines), **Comment** (documentation lines), **%** (percentage of total).

Special pseudo-languages: `__empty__` (empty files), `__binary__` (binary), `__generated__` (auto-generated), `__duplicate__` (identical content), `__unknown__` (unrecognized types).

### Pitfalls

1. **Always exclude .git, node_modules, venv** — without `--folders-to-skip`, pygount crawls everything and may hang
2. **Markdown shows 0 code lines** — pygount classifies all Markdown as comments, not code (expected)
3. **JSON files show low code counts** — use `wc -l` for accurate JSON line counts
4. **Large monorepos** — use `--suffix` to target specific languages rather than scanning everything

---

## Section 2: Simplify Code — Parallel Review & Cleanup

Review recent code changes with three focused reviewers running in parallel, aggregate findings, and apply fixes.

**Core principle:** Three narrow reviewers beat one broad reviewer. Each deeply searches the codebase for a single class of problem.

### When to Use

- "simplify" / "simplify my changes" / "review my code"
- "/simplify" (Claude Code habit)

Optional modifiers: **Focus** (reuse/quality/efficiency), **Dry run** (report only), **Scope** (last commit / staged / specific file)

### Phase 1 — Identify Changes

```bash
# Default: uncommitted working-tree changes
git diff

# If empty, include staged
git diff HEAD

# Scoped variants:
git diff --staged              # staged changes
git diff HEAD~1                # last commit
git diff main...HEAD           # this branch/PR
git diff -- src/foo.py         # specific file
```

### Phase 2 — Launch Three Reviewers

Use `delegate_task` **batch mode** — pass all three tasks in one `tasks` array:

**Reviewer 1 — Code Reuse:** Search for code that duplicates existing functionality. Check utility modules, shared helpers, adjacent files for existing functions to reuse.

**Reviewer 2 — Code Quality:** Look for redundant state, parameter sprawl, copy-paste-with-variation, leaky abstractions, stringly-typed code.

**Reviewer 3 — Efficiency:** Look for unnecessary work, missed concurrency, hot-path bloat, TOCTOU anti-patterns, memory issues, overly broad reads.

Each gets the **complete diff** plus repo path and toolsets `[terminal, file, search]`.

### Phase 3 — Aggregate and Apply

1. Merge findings, dedup overlaps
2. Discard false positives
3. Resolve conflicts: **correctness > user's focus > readability > micro-perf**
4. Apply fixes with `patch`/`write_file` (or dry run)
5. Verify: run targeted tests + linter
6. Summarize what changed and what was skipped

### Pitfalls

- Don't fan out wider than ~3 reviewers
- Give the **WHOLE diff** to each reviewer
- Require `file:line` evidence from reviewers
- Keep edits scoped to what the diff touched
- Check AGENTS.md / CLAUDE.md for project conventions

---

## Section 3: Pre-Commit Verification

Automated verification pipeline before code lands. Static scans, baseline-aware quality gates, an independent reviewer subagent, and an auto-fix loop.

**Core principle:** No agent should verify its own work. Fresh context finds what you miss.

### When to Use

- After implementing a feature or bug fix, before `git commit` or `git push`
- When user says "commit", "push", "ship", "done", "verify", or "review before merge"
- After completing a task with 2+ file edits in a git repo

**Skip for:** documentation-only changes, pure config tweaks, or explicit "skip verification".

### Step 1 — Get the Diff

```bash
git diff --cached
```

If empty, try `git diff` then `git diff HEAD~1 HEAD`. If diff exceeds 15K chars, split by file.

### Step 2 — Static Security Scan

Scan added lines for hardcoded secrets, shell injection, dangerous eval/exec, unsafe deserialization, SQL injection:

```bash
git diff --cached | grep "^+" | grep -iE "(api_key|secret|password|token|passwd)\s*=\s*['\"][^'\"]{6,}['\"]"
git diff --cached | grep "^+" | grep -E "os\.system\(|subprocess.*shell=True"
git diff --cached | grep "^+" | grep -E "\beval\(|\bexec\("
git diff --cached | grep "^+" | grep -E "pickle\.loads?\("
git diff --cached | grep "^+" | grep -E "execute\(f\"|\.format\(.*SELECT|\.format\(.*INSERT"
```

### Step 3 — Baseline Tests and Linting

Detect the project language and run appropriate tools. Capture baseline BEFORE changes (stash changes, run, pop). Only NEW failures block commit.

**Test frameworks** (auto-detect):
```bash
python -m pytest --tb=no -q 2>&1 | tail -5
npm test -- --passWithNoTests 2>&1 | tail -5
cargo test 2>&1 | tail -5
go test ./... 2>&1 | tail -5
```
