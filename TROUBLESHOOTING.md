# Troubleshooting

Symptoms-first. Find your symptom, follow the fix.

---

## Gateway won't start

**Symptom:** Running `hermes start` or `openclaw gateway start` exits immediately, or you get "address in use" / "EADDRINUSE".

**Likely cause:** A previous gateway process is still running, or the port (default: 3000) is in use by another application.

**Fix:**
```bash
# Kill any existing agent processes
pkill -f "hermes start" || true
pkill -f "openclaw gateway" || true

# Wait 2 seconds, then try again
hermes start

# If port 3000 is taken by another app:
lsof -i :3000 # find what's using it
# Change gateway port in your config (gateway.yaml or hermes.config.json)
```

If the gateway still won't start, check the log file directly:
```bash
# Hermes
tail -50 ~/.hermes/logs/gateway.log

# OpenClaw
tail -50 ~/.openclaw/logs/gateway.log
```

---

## Model timeouts / no response

**Symptom:** You send a message to the agent and nothing comes back. Or responses arrive but take 60+ seconds.

**Likely cause:** The model API is slow or rate-limited, or your API key is invalid.

**Fix:**
1. Test your OpenRouter key directly:
 ```bash
 curl https://openrouter.ai/api/v1/models \
 -H "Authorization: Bearer $OPENROUTER_API_KEY" | head -20
 ```
 A 200 response means the key works. A 401 means it doesn't.

2. Check your model fallback chain in TOOLS.md. If the primary model is rate-limited, the agent should fall back automatically if configured.

3. Try a different model to isolate whether the issue is the key or a specific model.

4. If you see responses but they're very slow: MiniMax M2.7 is fast by default. Slowness usually means you've switched to a heavier model (Opus, GPT-4) or the provider is under load.

---

## Telegram bot is silent

**Symptom:** You message your bot on Telegram and nothing happens. The agent appears to be running.

**Likely cause (in order):** Access not configured, wrong bot token, gateway not reachable from the Telegram polling loop.

**Fix:**
1. Verify the bot token is set:
 ```bash
 grep TELEGRAM .env.secrets
 # Should show TELEGRAM_BOT_TOKEN=<your_token>
 ```

2. Check the access list. By default, bots ignore messages from unrecognized users. Find the access config:
 ```bash
 cat ~/.hermes/access.json # Hermes
 cat ~/.openclaw/access.json # OpenClaw
 ```
 Your Telegram user ID should be listed. Get your ID by messaging @userinfobot on Telegram.

3. Check that the gateway is running and the Telegram connector is active:
 ```bash
 tools/health-check.sh
 curl -s http://localhost:3000/status | python3 -m json.tool
 ```

4. Send `/start` to the bot. Some setups require an initial handshake.

---

## OAuth expired (Google Workspace)

**Symptom:** Google-related skills (Gmail, Calendar, Drive) return 401 or "token expired" errors. Works fine after re-auth but breaks again in 7 days.

**Likely cause:** You're using a test OAuth app. Google expires tokens for test apps unless users re-authorize regularly.

**Fix:**
For permanent tokens, you need an Internal OAuth app (available if your Google account is part of a Google Workspace organization):

1. In Google Cloud Console, go to APIs and Services > OAuth consent screen.
2. Set "User type" to Internal (not External).
3. Internal apps get permanent refresh tokens that don't expire.

If you're using a personal Google account (not Workspace), the 7-day expiry is a Google limitation. You can work around it by scheduling an automatic token refresh:
```bash
# Add to crontab: refresh token daily at 9am
0 9 * * * cd /path/to/workspace && ./tools/refresh-google-token.sh
```

---

## Skill not detected / not loading

**Symptom:** You installed a skill but the agent doesn't seem to know about it. Or you get "skill not found" errors.

**Likely cause:** Wrong directory location, YAML frontmatter syntax error, or missing `name` field.

**Fix:**
1. Verify the skill is in the right place:
 ```bash
 ls ~/.hermes/skills/your-skill-name/SKILL.md # Hermes
 ls ~/.openclaw/skills/your-skill-name/SKILL.md # OpenClaw
 ```

2. Check the frontmatter for syntax errors. The YAML block must be at the very top of the file:
 ```yaml
 ---
 name: your-skill
 description: What it does.
 version: 1.0.0
 ---
 ```
 Indentation errors in YAML silently fail. Use a YAML linter: `python3 -c "import yaml; yaml.safe_load(open('SKILL.md'))"`.

3. Reload skills without restarting the agent:
 ```bash
 hermes skills reload # Hermes
 # OpenClaw requires gateway restart
 openclaw gateway restart
 ```

4. Check logs for load errors:
 ```bash
 grep -i "skill" ~/.hermes/logs/gateway.log | tail -20
 ```

---

## Hermes vs OpenClaw mismatch

**Symptom:** Skills that work on one platform silently fail on the other. The agent loads but doesn't use the skill correctly.

**Likely cause:** Some skills are written specifically for OpenClaw's plugin system and reference `openclaw`-specific tool names. Others use Hermes-specific routing via the `hermes:` metadata block.

**Fix:**
- Check the skill's frontmatter. If it has `"openclaw": { ... }` in the metadata, it was written for OpenClaw. If it has `"hermes": { ... }`, it targets Hermes.
- For cross-platform use, skills should use generic tool names (`terminal`, `web_extract`, `browser_navigate`) rather than platform-specific ones.
- If you're on Hermes and a skill references OpenClaw-specific tools, edit the SKILL.md to use Hermes equivalents. The skills in this kit have been audited for Hermes compatibility.

---

## MiniMax via OpenRouter setup

**Symptom:** You configured MiniMax M2.7 but the agent uses a different model, or MiniMax returns errors.

**Fix:**
Verify the model ID is correct. OpenRouter uses the format `provider/model-name`:
```
minimax/minimax-m2.7
```

Not `minimax-m2.7` or `m2.7`. Common mistake: copy-pasting the display name instead of the model slug. Check openrouter.ai/models to confirm the current slug.

Test the model directly:
```bash
curl https://openrouter.ai/api/v1/chat/completions \
 -H "Authorization: Bearer $OPENROUTER_API_KEY" \
 -H "Content-Type: application/json" \
 -d '{"model": "minimax/minimax-m2.7", "messages": [{"role": "user", "content": "hello"}]}'
```

---

## fal.ai key issues

**Symptom:** Image/video generation skills return 401 or "unauthorized".

**Fix:**
1. Get a key at fal.ai/dashboard.
2. Store it in `.env.secrets`:
 ```
 FAL_KEY=your-key-here
 ```
3. Verify the variable name exactly. fal.ai's SDK expects `FAL_KEY` (not `FAL_API_KEY` or `FALAI_KEY`).

Test:
```bash
source .env.secrets
curl "https://queue.fal.run/fal-ai/nano-banana" \
 -H "Authorization: Key $FAL_KEY" \
 -H "Content-Type: application/json" \
 -d '{"prompt": "a test image"}' | head -3
```

---

## Rate limits

**Symptom:** Sporadic HTTP 429 errors from OpenRouter, Airtable, or other APIs. Agent retries but eventually fails.

**Fix:**
Each API has its own limit. Key ones:
- OpenRouter: varies by model and plan. Free tier is limited; paid tier scales.
- Airtable: 5 requests/second per base. Never fire requests faster than this.
- Google APIs: 100 requests/100 seconds per user (most endpoints).

For persistent rate limiting on OpenRouter, check your account tier at openrouter.ai/settings/credits.

To reduce rate limit pressure: configure the agent to use smaller, faster models for simple tasks (Haiku, Mistral 7B) and reserve heavier models for complex work.

---

## Disk space

**Symptom:** Agent crashes or behaves strangely. Logs contain "ENOSPC" or "no space left on device".

**Fix:**
```bash
df -h # check overall disk usage
du -sh ~/.hermes/logs/ # check log size
du -sh ~/.openclaw/logs/ # same

# Rotate logs (keeps last 7 days)
find ~/.hermes/logs/ -mtime +7 -delete
```

For agents doing heavy file processing (transcription, image generation), temp files accumulate. Run `tools/session-cleanup.sh` to clear stale session files.

---

## Log locations

| Component | Log path |
|-----------|----------|
| Hermes gateway | `~/.hermes/logs/gateway.log` |
| OpenClaw gateway | `~/.openclaw/logs/gateway.log` |
| Session logs | `~/.hermes/logs/sessions/` |
| Skill errors | `~/.hermes/logs/skills.log` |
| Health check output | Check stdout when running `tools/health-check.sh` |

---

## Debug mode

For more verbose output during troubleshooting:

```bash
# Hermes
HERMES_LOG_LEVEL=debug hermes start

# OpenClaw
OPENCLAW_DEBUG=1 openclaw gateway start
```

Debug mode logs every tool call, model request, and skill invocation. Turn it off in production, it generates a large volume of output.

---

## Still stuck?

1. Run `tools/health-check.sh` and paste the output in your GitHub issue.
2. Include your OS, agent version (`hermes --version`), and Node.js version (`node -v`).
3. Sanitize any API keys before posting (the security scan tool helps: `tools/security-scan.sh`).
