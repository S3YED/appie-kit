---
name: development-workflow
description: "Development lifecycle methodologies: TDD, debugging, code review, simplification, and spike prototyping."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [development, methodology, tdd, debugging, code-review, spike, simplification, workflow]
    related_skills: [plan, subagent-driven-development, external-coding-agents]
---

# Development Workflow Methodologies

A collection of proven development workflows covering the full lifecycle: from exploration (spikes) through implementation (TDD), verification (code review), cleanup (simplify), and debugging (systematic debugging).

## Workflow Sequence

```
Spike ──→ TDD ──→ Code Review ──→ Simplify ──→ Deploy
  │                                          ↑
  └──→ Bug Found? ──→ Systematic Debugging ──┘
```

Each phase has an independent skill reference with exact commands, iron laws, and anti-pattern tables:

### 1. Spike — Throwaway Experiments
When to use: Validating feasibility before committing to a real build.
- **references/spike.md** for the full workflow

### 2. Test-Driven Development (TDD)
When to use: ANY code change — features, bug fixes, refactoring.
- RED: Write failing test first, watch it fail
- GREEN: Write minimal code to pass
- REFACTOR: Clean up while keeping tests green
- **references/test-driven-development.md** for the full TDD cycle

### 3. Pre-Commit Code Review
When to use: Before every commit after 2+ file edits.
- Static security scan (secrets, injections, unsafe patterns)
- Baseline-aware quality gates (tests, linting)
- Independent reviewer subagent (fail-closed JSON verdict)
- Auto-fix loop (max 2 cycles)
- **references/github-code-review.md** for the full pipeline

### 4. Simplify Code — Parallel Cleanup
When to use: When the user says "simplify" or "clean up my changes".
- Three parallel reviewers: Reuse, Quality, Efficiency
- Aggregates findings, applies fixes, verifies with tests
- **references/simplify-code.md** for the full process

### 5. Systematic Debugging
When to use: ANY technical bug or test failure.
- 4 phases: Root Cause Investigation → Pattern Analysis → Hypothesis Testing → Implementation
- The Rule of Three: stop after 3 failed fixes, question the architecture
- **references/systematic-debugging.md** for the full methodology

## Common Patterns Across All Workflows

### The Iron Law
Each methodology has a non-negotiable first principle:
- TDD: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"
- Debugging: "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"
- Code Review: "No agent should verify its own work"

### Rationalizations vs Reality
All five skills include a table of common excuses and their counters.

### Red Flags
Each skill lists patterns that indicate you're skipping the process.

### When NOT to Use Each
- **Spike:** Skip when the answer is already known or the work is production path
- **TDD:** Skip only for throwaway prototypes, generated code, or config files (ask the user first)
- **Code Review:** Skip for docs-only or config-only changes
- **Simplify:** Skip unless the user explicitly asks (it's token-heavy)
- **Debugging:** Never skip — even simple bugs have root causes

## Hermes Tool Integration

All workflows use the same Hermes tool primitives:

```
terminal("git diff")              # Get changes
terminal("pytest ...")            # Run tests
terminal("ruff check .")          # Lint
terminal("git log --oneline")     # Check history
search_files("error_string")      # Find errors
read_file("src/problematic.py")   # Read code
```