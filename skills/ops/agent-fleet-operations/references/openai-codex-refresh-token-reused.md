# OpenAI Codex OAuth: `refresh_token_reused`

## When this applies

Hermes Agent is configured for `openai-codex`, often with a model such as `gpt-5.5`, but gateway replies fail with authentication errors, or the provider falls back unexpectedly.

## Evidence pattern

`~/.hermes/config.yaml` can already be correct:

```yaml
model:
  provider: openai-codex
  default: gpt-5.5
  base_url: https://chatgpt.com/backend-api/codex
```

But `~/.hermes/auth.json` contains:

```text
providers.openai-codex.last_auth_error.code = refresh_token_reused
providers.openai-codex.last_auth_error.message = Codex refresh token was already consumed by another client
providers.openai-codex.last_auth_error.relogin_required = true
```

Gateway logs may show:

```text
HTTP 429: The usage limit has been reached | provider=openai-codex model=gpt-5.5
Primary provider auth failed: No Codex credentials stored. Run `hermes auth` to authenticate.
```

Interpretation:

- Config/model may be fine.
- The OAuth token is stale or consumed by another Codex client, for example Codex CLI or VS Code extension.
- A human browser/device login may be required.

## Recovery commands

Run on the target machine that hosts Hermes:

```bash
codex
hermes auth
hermes gateway restart
```

During `hermes auth`, choose `openai-codex` if prompted.

## Communication pattern

Tell Seyed the blocker directly:

```text
Codex 5.5 is already configured. The blocker is OAuth, not config: auth.json shows refresh_token_reused. Please run codex, then hermes auth, choose openai-codex, then hermes gateway restart.
```

Do not paste tokens. Do not imply the model is unavailable unless model listing or API response proves that separately.
