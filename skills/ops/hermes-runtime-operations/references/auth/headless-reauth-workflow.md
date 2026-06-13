# Codex OAuth Re-Auth from Messaging Platforms

When Hermes runs as a gateway (Telegram/Discord/Slack), the standard `hermes auth add` blocks the agent because it polls for up to 15 minutes waiting for user authorization. This doc captures the workflow used on 2026-05-28 for re-authenticating openai-codex from Telegram.

## The Problem

The `hermes auth add openai-codex --type oauth` command calls `_codex_device_code_login()` which:
1. Requests a device code (fast)
2. Prints URL + code for the user
3. Polls `deviceauth/token` every 5s until user authorizes (can take minutes)
4. Exchanges authorization code for tokens

Step 3 blocks the calling process. From a messaging platform, this means the agent's terminal is blocked for up to 15 minutes.

## The Solution: Manual Script with Background Polling

### Phase 1: Request device code + show user

```bash
python3 -c "
import httpx
r = httpx.post('https://auth.openai.com/api/accounts/deviceauth/usercode',
    json={'client_id':'app_EMoamEEZ73f0CkXaXp7hrann'},
    headers={'Content-Type':'application/json'}, timeout=10)
d = r.json()
print(f'CODE:{d[\"user_code\"]}')
print(f'ID:{d[\"device_auth_id\"]}')
"
```

Tell the user: "Open **https://auth.openai.com/codex/device** and enter code **`XXXX-XXXXX`**"

### Phase 2: Start background poll

Write the device_auth_id and user_code into `references/codex-oauth-refresh.py`, then:

```
terminal(background=True, notify_on_complete=True, timeout=900,
         command="python3 -u /path/to/codex-oauth-refresh.py")
```

The `notify_on_complete=True` means you get alerted when the poll succeeds or times out - no need to manually poll the process.

### Phase 3: Restart gateway

After the background process completes with `OK:<entry_id>`:

```bash
hermes gateway restart
```

### Lessons Learned

- **`--no-browser --manual-paste` is wrong** for messaging platforms - it waits for stdin paste
- **`--no-browser` alone** uses the standard device code print-and-poll flow and is correct, but blocks the agent
- **Background polling** via `terminal(background=True, notify_on_complete=True)` is the right approach
- **Always verify endpoint reachability first** with a quick `curl` to `auth.openai.com`
- **Each device code is single-use** - if you kill and restart the poller, request a fresh code
- **Update both auth.json layers** - `providers.openai-codex` AND `credential_pool.openai-codex[]`

## Error: `TypeError: 'NoneType' object is not iterable`

This is the signature of a dead Codex OAuth token. The refresh mechanism (`refresh_codex_oauth_pure`) returns None or the HTTP response parsing fails, and the credential pool wraps it in TypeError.

**Diagnosis:**
```bash
grep "NoneType.*iterable\|API call failed.*codex" ~/.hermes/logs/errors.log | tail -5
```

**Fix:** Full re-auth as described above.