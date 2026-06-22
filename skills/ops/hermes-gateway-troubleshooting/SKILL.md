---
name: hermes-gateway-troubleshooting
description: "Troubleshoot Hermes Agent gateway/runtime issues: messaging sessions, model/provider switches, auth, logs, and state.db consistency."
version: 1.1.0
author: Appie-3
license: MIT
platforms: [linux, macos, windows]
---

# Hermes Gateway Troubleshooting

Use this skill when Hermes behaves differently in Telegram/Discord/Slack/etc. than in the CLI, especially after model/provider changes, OAuth refreshes, `/model` switches, gateway restarts, or session resumes.

## Triggers

- User says a selected model "doesn't work", "switches back", "falls back", or shows wrong runtime metadata.
- Gateway responds from a different model/provider than `hermes config` says.
- CLI test works, but Telegram/gateway session appears stale.
- Logs mention polling conflicts, stale sessions, stream watchdogs, provider/auth errors, or config migration.
- Session rows in `state.db` disagree with runtime logs.

## Investigation sequence

1. **Check current config and auth first.**
   - `hermes status --all` — per-provider auth health report (`✗ not logged in`, `No <provider> credentials stored`, or `✓` with key hint)
   - `hermes auth list` — credential pools per provider; empty arrays mean no stored credentials despite provider being selected
   - `hermes config check`
   - Inspect `~/.hermes/config.yaml` model block: `model.default`, `model.provider`, `model.base_url`, `fallback_providers`, auxiliary provider settings.

2. **When status shows a provider as "not logged in" or the user says "OAuth is shady", dig into credential health.**
   - `cat ~/.hermes/auth.json` via terminal (read_file redacts this file) — check `credential_pool[<provider>]`: empty array = no stored credentials.
   - Check `active_provider` field — is it pointing at a provider with empty credentials? This causes silent fallback or auth failure every turn.
   - Look for stale backup files: `ls ~/.hermes/auth.json.bak-*` — previous broken auth attempts.
   - If switching from a broken OAuth provider to a working API-key provider, follow `references/oauth-to-apikey-provider-switch.md`.

3. **Read gateway and agent logs with timestamps.**
   - Gateway ingress and delivery: `~/.hermes/logs/gateway.log`
   - Model/runtime/tool calls: `~/.hermes/logs/agent.log`
   - Warnings/errors: `~/.hermes/logs/errors.log`
   
4. **Differentiate runtime truth from metadata truth.**
   - Runtime truth: `agent.turn_context`, `OpenAI client created`, and `API call #... model=... provider=...` in `agent.log`.
   - Metadata truth: `sessions` table row (`model`, `billing_provider`, `billing_base_url`, `model_config`) and `~/.hermes/sessions/sessions.json` current session mapping.

5. **Reproduce with a minimal CLI call using the same default config.**
   - Example: `hermes chat -q 'Reply exactly: ok' --toolsets safe -Q`
   - For provider-specific checks: add `--provider <provider> --model <model>`.
   - A CLI success proves auth and provider wiring; a gateway-only failure usually points to session state, stale process config, or messaging/gateway lifecycle.

6. **Check the active gateway process.**
   - Confirm only one gateway owns the bot token/polling stream.
   - Polling conflicts (`terminated by other getUpdates request`) mean multiple bot instances or recently-stopped polling sessions. Resolve process/service duplication before diagnosing model behavior.

## Model/provider switch checklist

When a model switch seems half-applied:

- Verify config: selected `model.default`, `model.provider`, and `model.base_url`.
- Verify auth: provider credential exists and is healthy.
- Verify runtime logs: actual API calls use the intended provider/model.
- Verify session DB: current gateway session row matches intended provider/model.
- Verify fallback chain: remove or reorder fallbacks if they silently mask provider failures.
- Restart gateway only after config changes that are read at process startup; do not assume a running gateway rereads every setting.
- If a session row is stale but runtime is correct, repair or reset the session so future resume/metadata uses the correct model.

## Safe remediation patterns

- Run `hermes doctor --fix` for config migrations and harmless install/link repairs.
- Prefer `/reset` or a fresh session when the issue is session-scoped and no durable state must be preserved.
- If preserving the chat matters, update only the current session's row and confirm via read-back. Include `model_config` with `model`, `provider`, `base_url`, reasoning config, and iteration/token settings when applicable.
- Disable unintended fallbacks only when the desired behavior is strict provider use. Otherwise, document the fallback as intentional.
- After changes, run a minimal model call and verify both runtime output and session metadata.

## Pitfalls

- Do not conclude "auth works" from config alone. Make a real minimal call.
- Do not conclude "the model is wrong" from `sessions.model` alone. Compare with `agent.log` API-call lines.
- Do not leave a stale fallback provider that points at the previous model if the user explicitly wants to know when the selected provider fails.
- Do not save transient missing-package or local setup errors as durable rules. Capture the remediation pattern, not the one-off failure.
- Avoid dumping huge logs into context. Search for targeted timestamps, model names, provider names, session IDs, and error classes.

## Verification

A fix is not done until:

- `hermes config check` is clean enough for the intended provider.
- `hermes auth list` shows the selected provider credential.
- A minimal `hermes chat -q ...` returns the expected text from the selected provider/model.
- The active gateway session row, if relevant, reflects the same provider/model.
- The user-facing summary separates actual runtime behavior from stale metadata or fallback behavior.

## References

- `references/model-switch-metadata-fallback.md` — session-derived pattern for Codex/GPT-5.5 switch issues where runtime was correct but session metadata and fallbacks were stale.
- `references/oauth-to-apikey-provider-switch.md` — diagnosing and fixing a broken OAuth provider (empty credential pool) by switching to a working API-key provider, with exact commands and auth.json cleanup.