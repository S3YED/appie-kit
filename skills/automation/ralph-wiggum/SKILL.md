# Ralph Wiggum Skill

**Purpose:** Autonomous coding loop technique for complex build tasks.

**What it does:** Runs an AI coding agent (Claude Code, Codex, etc.) in iterative loops — each iteration picks ONE spec/task, implements it, verifies, commits, and loops until done.

**Based on:** Geoffrey Huntley's Ralph Wiggum technique — fresh context each loop, persistent state via git/files.

## Setup

Already installed at: `~/.openclaw/skills/ralph-wiggum/`

Structure:
```
ralph-wiggum/
├── SKILL.md
├── scripts/
│   ├── ralph-loop.sh      # Claude Code loop
│   └── ralph-loop-codex.sh # OpenAI Codex loop
└── specs/                 # Spec files (you create these)
```

Ralph Wiggum commit: `d205125cc33745116cce22d883417461174dcde5`

## How to Use

### 1. Create a Spec

Write a spec file in `specs/` with:
- What to build
- Clear acceptance criteria
- Completion signal

### 2. Start the Loop

```bash
# Claude Code (recommended)
~/.openclaw/skills/ralph-wiggum/scripts/ralph-loop.sh

# Or OpenAI Codex
~/.openclaw/skills/ralph-wiggum/scripts/ralph-loop-codex.sh

# Limit iterations
~/.openclaw/skills/ralph-wiggum/scripts/ralph-loop.sh 20
```

### 3. How the Loop Works

```
Each iteration:
1. Ralph reads specs/ and picks highest priority incomplete spec
2. AI implements it completely
3. AI verifies acceptance criteria + runs tests
4. AI outputs "DONE" only if criteria pass
5. Bash loop checks for DONE → next iteration
6. Context cleared, fresh start
```

### 4. Exit Signals

- `<promise>DONE</promise>` → spec complete, next iteration
- `<promise>ALL_DONE</promise>` → all specs complete, loop exits
- Bash checks for DONE phrase in output

## Key Concepts

**Specs:** Markdown files in `specs/` with acceptance criteria. Lower number = higher priority.

**Context Reset:** Each iteration starts fresh — no accumulated confusion.

**State Persistence:** Progress stored in git commits + files.

**Completion Verification:** AI only outputs DONE when ALL criteria verified + tests pass.

## For Wolfie (OpenClaw) Integration

Ralph Wiggum is useful for:
- Complex multi-step builds (creative pipeline, store cloning)
- Tasks too large for single AI call
- Autonomous iteration on specifications

To use with OpenClaw: spawn a subagent with `sessions_spawn` and run ralph-loop.sh inside it.

## Links

- Main repo: https://github.com/fstandhartinger/ralph-wiggum
- Official CLI: https://github.com/wiggumdev/ralph
- Website: https://wiggum.dev