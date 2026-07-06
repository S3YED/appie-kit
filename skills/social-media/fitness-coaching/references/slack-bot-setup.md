# Slack Bot Setup for Agent Access

## Scopes Needed
- `channels:join` — join all channels
- `groups:write` — join private channels
- `chat:write` — send messages
- `channels:read` — list channels
- `channels:history` — read messages
- `groups:read` — read private channels
- `users:read` — look up members
- `reactions:write` — react to messages
- `im:write` — DM users

## Setup Steps
1. Go to https://api.slack.com/apps → Create New App → From scratch → Name it → Pick workspace
2. OAuth & Permissions → Add OAuth Scopes (list above) → Install to Workspace → Allow
3. Copy Bot User OAuth Token (starts with `xoxb-`)

## Token Handling
The `xoxb-` token breaks in shell variables. Store it:
```bash
echo -n 'xoxb-...' > /tmp/slack_token.txt
```
Read via Python:
```python
token = open('/tmp/slack_token.txt').read().strip()
```

## API Endpoints
- `auth.test` — verify token, get bot/user/team IDs
- `conversations.list` — list all channels
- `conversations.join` — join a channel
- `chat.postMessage` — send a message
- `conversations.invite` — invite to private channels (if join fails)

## Notes
- `send_message` tool needs `channels.slack` config in Hermes — bot token alone won't enable it
- For direct API: use Python `urllib.request` with `Authorization: Bearer {token}`
- Token stored at `/tmp/slack_token.txt` — clears between sessions, save in memory