# Hermes Log Warning Patterns

Common warnings found in ~/.hermes/logs/ — what they mean and when to act.

## Vision Provider Issues

### `unknown provider 'openai'`
```
WARNING agent.auxiliary_client: resolve_provider_client: unknown provider 'openai'
WARNING agent.auxiliary_client: Vision provider openai unavailable, falling back to auto vision backends
```
**Meaning:** config.yaml specifies `openai` as the vision provider but OpenAI isn't configured in the providers list.
**Impact:** Falls back to main provider for vision. If main provider also doesn't support vision → silent failure or 404.
**Fix:** Either add OpenAI credentials or switch vision provider to `anthropic`.

### `No endpoints found that support image input` (404)
```
openai.NotFoundError: Error code: 404 - {'error': {'message': 'No endpoints found that support image input', 'code': 404}}
```
**Meaning:** The model being used (e.g. `deepseek/deepseek-v4-pro`) cannot handle image inputs. DeepSeek models do NOT support multimodal.
**Impact:** All vision analysis tools fail.
**Fix:** Switch to a vision-capable model like `anthropic/claude-opus-4-6`.

## Network Issues

### Telegram connection failure
```
WARNING gateway.platforms.telegram_network: [Telegram] Primary api.telegram.org connection failed
WARNING gateway.platforms.telegram_network: [Telegram] Fallback IP 149.154.167.220 failed
WARNING gateway.platforms.telegram: [Telegram] Telegram network error (attempt 1/10), reconnecting in 5s
```
**Meaning:** Internet connectivity loss — ISP issue, DNS failure, or firewall blocking Telegram's API.
**Impact:** Cannot send/receive Telegram messages until connectivity restored.
**Recovery:** Automatic — gateway retries up to 10 times with exponential backoff. If it persists >10 min, check internet connection.

### Discord session RESUMED
```
INFO discord.gateway: Shard ID None has successfully RESUMED session b2fed473081e2469b9c25cb2502da64d
```
**Meaning:** Discord WebSocket connection dropped and re-established with session resume (no event loss).
**Impact:** Normal if occasional. If every 2-3 hours consistently, gateway may be under resource pressure.
**Watch for:** If accompanied by `RECONNECT` or `IDENTIFY` instead of `RESUME`, events may have been lost.

## Gateway Lifecycle

### Shutdown diagnostic
```
WARNING gateway.run: Shutdown diagnostic — other hermes processes running
```
**Meaning:** A `launchctl kickstart` was triggered on the gateway, restarting it via the launch agent.
**Impact:** Brief downtime (~5-10s) while gateway restarts.
**Check:** `launchctl list | grep hermes` to see if launch agent is causing frequent restarts.

### Agent cache idle eviction
```
INFO gateway.run: Agent cache idle-TTL evict: session=agent:main:telegram:dm:1817919454 (idle=3676s)
```
**Meaning:** Normal — agent sessions idle for >1 hour are evicted from memory.
**Impact:** None. Next message creates fresh session.
