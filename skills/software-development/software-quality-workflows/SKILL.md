---
name: software-quality-workflows
description: "Umbrella workflow for TDD, debugging, code simplification, spikes, pre-commit review, and debugger-assisted investigation."
origin: user
---

# Software Quality Workflows

Use this umbrella for implementation-quality loops: test-first work, systematic debugging, short spikes, simplification passes, debugger sessions, and pre-commit review.

## Pick the mode

| Situation | Mode |
|---|---|
| New behavior or bug fix with clear expected output | TDD: RED → GREEN → REFACTOR. |
| Unknown root cause | Systematic debugging: reproduce, localize, hypothesize, fix, verify. |
| Uncertain approach or API | Spike: time-boxed throwaway experiment before production changes. |
| Recent change is too complex | Simplify-code: parallel or focused cleanup with behavior preserved. |
| Ready to hand off/commit | Requesting code review: security scan, quality gates, auto-fix only when safe. |
| Runtime behavior is opaque | Debugger-assisted investigation via `pdb`/`debugpy` or Node inspector. |

## TDD loop

1. Write or identify a failing test that captures the requirement.
2. Run only the relevant test to see RED.
3. Implement the smallest fix.
4. Run focused then broader tests.
5. Refactor while tests stay GREEN.

## Systematic debugging loop

1. Reproduce with exact command/input.
2. Observe logs, state, failing assertions, and environment.
3. Narrow the fault with instrumentation or debugger probes.
4. Fix the root cause, not the symptom.
5. Verify the original failure and a regression test.

## Spikes

Create disposable experiments under a clearly temporary path. Do not mix spike code into production without reimplementation or review. End with a decision: adopt, reject, or investigate further.

## Simplification and review

Before committing, inspect diff shape, remove incidental complexity, check security-sensitive paths, and run project gates. If using subagents for cleanup/review, independently verify their claims.

## Debugger notes

- Python: use `pdb` for local stepping and `debugpy` when a DAP/remote attach flow is needed.
- Node: start with `node --inspect`/`--inspect-brk` and inspect through Chrome DevTools Protocol when logs are insufficient.
