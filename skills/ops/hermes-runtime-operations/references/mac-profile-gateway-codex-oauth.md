# Mac Hermes Profile Gateway + Codex OAuth Recovery

Session-derived reference for recovering a named Hermes profile on macOS when the config and OAuth credentials are valid but the agent appears offline.

## Symptoms

- `hermes profile show <profile>` reports the profile gateway as stopped.
- Default gateway checks can be misleading because named profiles use separate launchd labels and profile homes.
- Historical logs may point to old supervisor/script errors, but current `bash -n` or live status may be clean.
- Codex model smoke tests work in CLI, but the messaging agent is not reachable because the profile gateway service is not running.

## Known-good Codex OAuth profile config

```yaml
model:
  default: gpt-5.5
  provider: openai-codex
  base_url: https://chatgpt.com/backend-api/codex
  openai_runtime: auto
```

Use `openai_runtime: auto` for Hermes-managed OpenAI Codex OAuth. `codex_app_server` can be appropriate when the Codex CLI runtime is intentionally configured, but it depends on the `codex` executable and PATH being available to the service environment.

## Recovery commands

```bash
# Inspect the profile and credential pool
hermes profile show appie-1
hermes -p appie-1 auth list openai-codex
hermes -p appie-1 config show

# Ensure known-good Codex OAuth config
hermes -p appie-1 config set model.provider openai-codex
hermes -p appie-1 config set model.default gpt-5.5
hermes -p appie-1 config set model.base_url https://chatgpt.com/backend-api/codex
hermes -p appie-1 config set model.openai_runtime auto

# Start the profile-scoped gateway service on macOS launchd
hermes -p appie-1 gateway install
hermes -p appie-1 gateway start

# Verify live service state
hermes -p appie-1 gateway status
hermes gateway list
tail -120 ~/.hermes/profiles/appie-1/logs/gateway.log

# Non-secret provider smoke test
hermes -p appie-1 chat -Q -q 'Reply exactly: APPIE1_LIVE_CODEX_OK'
```

## Verification criteria

- `hermes -p <profile> gateway status` shows a loaded service with a live PID.
- `hermes gateway list` marks the named profile as running.
- Gateway logs show Telegram/Discord connected as expected.
- `hermes -p <profile> chat -Q` returns the exact smoke-test string.

## Pitfalls

- Do not rely on `hermes gateway status` alone. Without `-p <profile>`, it checks the default profile.
- Reproduce current failures before editing scripts. Old launchd/supervisor logs can contain stale syntax errors from previous versions.
- Profile-specific `.env`, config, sessions, and logs live under `~/.hermes/profiles/<profile>/`.
- Deprecated `.env` settings like `MESSAGING_CWD` are warnings if `terminal.cwd` is already set in config. Do not treat them as the outage unless live logs prove it.
