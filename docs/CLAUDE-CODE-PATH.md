# The Claude Code Path

Run your Appie's orchestrator brain on **Claude Code** (Anthropic's official agent CLI) in a persistent tmux session on your Mac. Reachable via Telegram through ccgram or the new Claude Channels. This is the third supported runtime in the Appie Kit alongside Hermes and OpenClaw.

Use this path when:
- You have a Claude Pro or Max subscription and want flat per-month cost on the brain.
- You want the latest Anthropic features (skills, plugins, Claude Channels) without juggling provider keys.
- Your orchestrator does deep reasoning all day and worker Appies handle bulk execution.

Stay on Hermes if you want OpenRouter routing, multi-instance setup on one machine, or the built-in Telegram pairing system.

---

## 10-minute setup

### 1. Install

```bash
# Install Node LTS if you don't already have it
brew install node                                  # macOS
# or: visit nodejs.org and install the LTS .pkg

npm install -g @anthropic-ai/claude-code
claude                                             # first launch, sign in via claude.ai
```

Pro is the floor. Max is recommended for long sessions (raises the daily message ceiling).

### 2. Add the two plugin marketplaces

Inside Claude Code's prompt:

```
/plugin marketplace add anthropics/claude-plugins-official
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
```

### 3. Install the 6 canonical plugins

```
/plugin install superpowers@claude-plugins-official
/plugin install frontend-design@claude-plugins-official
/plugin install claude-code-setup@claude-plugins-official
/plugin install code-review@claude-plugins-official
/plugin install skill-creator@claude-plugins-official
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

What each does:

| Plugin | What it does |
|---|---|
| `superpowers` | Workflow skills — brainstorming, writing-plans, verification, debugging, code-review process. Mandatory. |
| `frontend-design` | Anthropic's official frontend plugin. Distinctive UI instead of generic AI-template look. |
| `claude-code-setup` | Audits your project, suggests automations, helps with permissions and settings. |
| `code-review` | Multi-agent review pass at the end of a feature. Catches bugs a single agent misses. |
| `skill-creator` | Author your own recurring-workflow skill. Use this for anything you do 3+ times. |
| `ui-ux-pro-max` | 50 ready-made styles, 21 palettes, 50 font pairings, 9 tech stacks. Speed multiplier for landing pages. |

### 4. Drop in this minimal `CLAUDE.md`

This is a starter Appie-flavored `CLAUDE.md` (~50 lines, principle-based). Save to `~/.claude/CLAUDE.md` for global use, or to your project root for per-project rules.

```markdown
# Appie · Coding Behavior (default for all projects)

## Four Basic Rules
1. **Think Before Coding** — State assumptions, name unclear points, present tradeoffs. For exploratory questions: 2-3 sentences with recommendation + tradeoff, then wait for the user.
2. **Simplicity First** — Minimum code. No speculation, no unsolicited abstractions, no error handling for impossible cases.
3. **Surgical Changes** — Only touch what's necessary. No drive-by refactoring. Every change must be traceable back to the request.
4. **Goal-Driven Execution** — Define success criteria upfront. Multi-step tasks: short plan + verification check per step.

## UI Work — Mandatory Order
For every web, landing page, component, or frontend task:
1. `brainstorming` skill — clarify requirements (audience, tone, content).
2. `frontend-design` skill — commit to tone and typography BEFORE code.
3. `ui-ux-pro-max` skill — style plan, colors, fonts, component list.
4. Pull `shadcn/ui` components instead of inventing your own (`bunx shadcn@latest add ...`).
5. `verification-before-completion` skill — browser check before saying "done."

## Default Stack
- **Framework:** Next.js (App Router) + TypeScript
- **Styling:** Tailwind CSS v4 + shadcn/ui
- **Package Manager:** Bun (faster than npm for local dev)
- **Deploy:** Vercel

If I don't say otherwise, use this stack.

## Bias
Caution > speed. Trivial task (typo, one-liner) = judgment, not the full workflow.

## Language
Respond in the user's language. Code comments and variable names always in English.
```

### 5. Try it

```bash
mkdir ~/Desktop/my-first-appie-site && cd $_
claude
```

Inside Claude Code, paste:

> Let's build a landing page for {your audience}. Stack: Next.js + Tailwind + shadcn/ui. Before you start, brainstorm style and content with me.

What happens:

1. `brainstorming` triggers — Claude asks 5-7 focused questions (audience, tone, hero message, USP, CTA, sections).
2. You answer in bullet points.
3. `frontend-design` + `ui-ux-pro-max` load — Claude presents 2-3 style options with colors/fonts/vibe.
4. You pick one. Claude scaffolds the project.
5. Components pull via `shadcn/ui` instead of being invented.
6. At the end, `verification-before-completion` runs — Claude must `bun dev` and check the site in a browser before reporting "done."

---

## The workflow you stick to

```
Brainstorm  →  Style & Type  →  Components  →  Code  →  Verify  →  Review
    ↓              ↓                ↓             ↓        ↓          ↓
brainstorming  frontend-design   shadcn/ui    TDD     verification-  code-review
                + ui-ux-pro-max  add          flow    before-        plugin
                                              (don't  completion
                                              invent)
```

Six words. Six steps. The reader can recall them without re-reading. Stick to this and your output is light years better than a zero-shot "write me a landing page" prompt.

---

## The 10 skills you'll actually use

These trigger automatically when Claude recognizes the task. You don't start them by hand — but knowing them helps you steer.

**Before you build (mandatory 3):**
1. `brainstorming` — triggers when you say "let's build X".
2. `frontend-design` — triggers for UI tasks.
3. `ui-ux-pro-max` — triggers when you ask for a "landing page" or visual asset.

**While you build:**
4. `writing-plans` — multi-step tasks get a plan + per-step verification.
5. `test-driven-development` — test first, then code.
6. `subagent-driven-development` — splits large tasks across parallel subagents.

**When something goes wrong:**
7. `systematic-debugging` — hypothesis → test → fix instead of trial and error.

**Before saying "done":**
8. `verification-before-completion` — server started, tested, browser-checked. Not "it should work."
9. `requesting-code-review` — triggers the code-review plugin.
10. `finishing-a-development-branch` — clean diff, green tests, ready to merge.

If a skill doesn't trigger automatically, say it explicitly: *"Use the brainstorming skill"* or *"Verify before you say you're done."* Claude obeys.

---

## If something gets stuck

1. **Skill doesn't trigger** — explicitly say "Use the `<skill-name>` skill."
2. **`/plugin` command unresponsive** — restart `claude`, then `/plugin marketplace list` to confirm marketplaces loaded.
3. **Claude becomes too cautious** — bump reasoning effort with `/effort max` for one session.
4. **Claude becomes too fast** — back to `/effort` default.
5. **`/init` in an existing project** — generates a project-specific `CLAUDE.md` with the stack notes auto-detected.
6. **You don't believe a "done"** — ask: *"Did you use verification-before-completion? Did you open it in the browser?"* It will be honest.

---

## What NOT to do

- **Don't** download individual skills from random GitHub repos. Use plugins — they self-maintain via `/plugin update`.
- **Don't** zero-shot "write me the whole website" without brainstorming. The output will look like a stock template.
- **Don't** let Claude say "done" before a browser-check. Always require verification.
- **Don't** fill your `CLAUDE.md` with 500 rules. Keep it under ~50 lines or Claude overlooks the important ones.

---

## When this path makes sense vs Hermes / OpenClaw

| You should... | Reason |
|---|---|
| Stay on **Claude Code** (this path) | You want flat-rate Anthropic billing, latest plugin ecosystem, single-machine orchestrator. |
| Move to **Hermes** | You want OpenRouter routing, multiple Appie instances on one machine, built-in Telegram pairing. |
| Stay on **OpenClaw** | You have a stable system that works and don't need to migrate. |

The Appie philosophy: pick the runtime that matches the job. Don't migrate for novelty.

---

## Going further

- The full Appie guide (free preview + paid PDF): [weblyfe.ai/pdf](https://weblyfe.ai/pdf)
- The Appie persona templates: `workspace/SOUL.md`, `workspace/IDENTITY.md`, `workspace/USER.md`
- Multi-agent orchestration: see `docs/FLEET-GUIDE.md` in this kit
- Memory layer with mem0: Chapter 30 of the v4.5 PDF

---

*Authored after absorbing patterns from Felix's "Claude Code Setup for Web Builders" (2026-05-15). Felix's doc targets influencer-marketing-agency web builders specifically; this version generalizes to any Appie-style use case and pairs with the Hermes/OpenClaw paths in this kit.*
