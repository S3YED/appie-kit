# Orgo Bot Operational Learnings

Collected 2026-07-08 from the fleet of Orgo-hosted client bots (Ferdows/Soleiman, Bakkali/Clark, Ramzy/Ibrahim).

## Bakkali's AGENTS.md Patterns (translated from Dutch)

### Honesty Rule
- Never confirm prior work is done unless verified in the current session.
- MEMORY.md and daily notes describe things from past sessions — you can't remember executing them.
- When asked "did you do X?": "Memory says X was done, but I haven't verified it this session."
- When in doubt: verify, do not assume.

### Context Engineering (8GB disk constraint)
1. Load files JIT (just in time) — only read a topic file when that topic becomes relevant.
2. MEMORY.md is an index pointing to topic files — read on demand, not all upfront.
3. Keep workspace files lean — archive resolved items promptly.
4. Smallest viable context — load only what you need for the current task.

### Task Execution Protocol
- Ask which project when context is ambiguous.
- Checkpoint after first major file write — confirm direction before continuing.
- Pause between tool call batches — let user see progress.
- Outline first for multi-file changes.
- Break large tasks into confirmable chunks.

### Session Startup
1. Read SOUL.md — who you are.
2. Read USER.md — who you're helping.
3. Read memory/YYYY-MM-DD.md (today + yesterday) for recent context.
4. If main session (direct chat): also read MEMORY.md.
- Do not ask permission. Just do it.

### Smart File Handling (8GB disk)
- Never store large media locally. Upload to Google Drive and share the link.
- After processing any file, delete the local temp copy immediately.
- On disk/space error: run ~/disk-guard.sh, then retry.

### Self-Improvement Loop
```
Error -> Diagnose -> Fix -> Update tool/skill/doc -> Test -> Document -> System stronger
```
- Every bug reveals a gap in the system.
- Document learnings immediately, not "later".
- Track recurring issues — they point to systemic problems.

## Ramzy's Orgo Onboarding Pattern

### 3-Part Client Onboarding
1. **Tools setup**: Get GitHub token (PAT, not device flow — device flow blocks on Orgo), Vercel token, Exa API key. Confirm each one works before proceeding.
2. **Business understanding**: Ask what client does daily, biggest obstacle, what they want to delegate. Reflect back.
3. **Data connection (most important)**: Connect existing tools: email, calendar, Instagram, social, funnels, CRM, payments. Without data, the bot is empty.

### Technical Do's and Don'ts for Orgo
- NEVER run interactive auth (`gh auth login`, device-flow) on the terminal. It blocks on timeout.
- For GitHub: ask client for Personal Access Token (classic, scope repo). Use `gh auth login --with-token` via stdin, or set GH_TOKEN.
- For Vercel/Exa: have client paste the token, save and test locally. No browser flows on the box.
- Keep messages short. Do 1 thing per call and wait for response. No long blocking commands.

## Ferdows' Clean Output Pattern

### Client Communication Mode
- Reply with the answer only. One clear, natural-language message.
- Keep full capability. All tools/skills/knowledge remain available — only the display changes.
- Hide process, not results. No tool narration, reasoning, logs, JSON, IDs, or file paths.
- If task takes time: at most one short line ("One moment, working on it.") then the result.
- Write like a calm, competent human assistant. Short sentences. Plain words. Mirror client's language.
- No em dashes. No corporate filler. No "as an AI" framing.
- If you can't do something: say it plainly in one sentence and offer the next best step.

## Fleet Scripts

Located in `references/orgo-bot-artifacts/`:
- `hermes-clean-output.py` — Applies clean output config + SOUL block to any Hermes bot (idempotent)
- `keepalive.sh` — Persistent supervisor: clock sync, gateway respawn, auto-pair claim, disk guard
- `disk-guard.sh` — Aggressive disk cleanup for 8GB Orgo VMs (80% threshold)
- `disk-guard-loop.sh` — Wraps disk-guard.sh in a loop (every 20 min)
- `fix-prov.sh` — Installs xz-utils and reruns provisioning (dependency fix for Orgo)