---
name: cron-env-isolation-guard
description: Guard-rail for debugging launchd cron failures caused by env isolation. Use when a launchd job works interactively but fails headless (missing keys, no TTY, MCP hangs).
---

# Cron Env Isolation Guard

## Why this exists

macOS launchd strips most shell environment from launched jobs. Variables available in an interactive terminal are NOT inherited. Common silent failures:
- API key env var missing → CLI crashes immediately
- OAuth keyring prompt has no TTY → deadlock
- MCP plugins init on claude startup → hang → SIGKILL after watchdog timeout

## Diagnostic checklist (run in order)

1. **Check exit code**: `launchctl list | grep <label>` — column 2 is last exit code. `-1` / `1` = crash; `-15` = SIGTERM (watchdog?).
2. **Check log size**: if stdout log = 0 or ~90 bytes, job started but didn't produce output → silent crash or early hang.
3. **Read the log**: check stderr path from the plist. Look for:
   - `no TTY available for keyring file backend password prompt` → add the keyring password to plist EnvironmentVariables.
   - `invalid_grant` / `Bad Request` → OAuth token expired; need interactive re-auth.
   - `aes.KeyUnwrap(): integrity check failed` → encrypted token corrupted; need re-auth.
   - Python traceback / CLI crash → missing API key in env.
   - MCP plugin startup messages followed by silence + SIGKILL → add `--no-mcp` to `claude -p` invocation.
4. **Read the plist**: confirm which EnvironmentVariables are set. Compare against what the script needs interactively.
5. **Run the script manually** with the same PATH the plist specifies: `PATH=<plist-PATH> <command>`. Compare output.

## Common fixes

| Symptom | Fix |
|---------|-----|
| Keyring/password prompt has no TTY | Add password env var to plist `EnvironmentVariables` dict |
| OAuth expired (invalid_grant) | Re-auth interactively, then reload launchd job |
| CLI crash (no API key) | Add API key to plist env |
| `claude -p` hangs on MCP init | Add `--no-mcp` flag to the claude invocation |
| Any env var missing | Add to plist EnvironmentVariables OR source a `.env` file at script start |

## Applying plist fixes

```bash
# Edit the plist to add env vars, then reload:
launchctl unload ~/Library/LaunchAgents/<label>.plist
launchctl load ~/Library/LaunchAgents/<label>.plist

# Verify:
launchctl list | grep <label>
```

## Hard rule: never add secrets inline to plist

Plists are readable by all processes under the same user. For API keys:
- Preferred: source a secrets file at script start (e.g. `source ~/.secrets/.env`).
- Acceptable: add to plist EnvironmentVariables if the key is already accessible to the user account.
- Never: hardcode secret values directly in a plist tracked in git.
