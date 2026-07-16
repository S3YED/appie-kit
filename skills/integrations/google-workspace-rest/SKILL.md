---
name: google-workspace-rest
description: Direct Google Calendar + Gmail + Contacts REST API access via Python. Use when gws CLI is broken (token cache decrypt failure) or google_api.py wrapper is unreliable. Companion to the bundled google-workspace skill.
version: 1.0.0
tags: [google, calendar, gmail, contacts, oauth, rest]
---

# Google Workspace — Direct REST API

Fallback when `gws` or `google_api.py` fail. Uses Python + `urllib.request` directly against the Google REST APIs with the token from `~/.hermes/google_token.json`. Handles token refresh automatically.

## Quick Start

```python
import json, os, urllib.request, urllib.parse

# Load and refresh token
token_path = os.path.expanduser("~/.hermes/google_token.json")
with open(token_path) as f:
    td = json.load(f)

# Refresh if needed
refresh_data = urllib.parse.urlencode({
    "client_id": td["client_id"],
    "client_secret": td["client_secret"],
    "refresh_token": td["refresh_token"],
    "grant_type": "refresh_token",
}).encode()
req = urllib.request.Request("https://oauth2.googleapis.com/token", data=refresh_data,
    headers={"Content-Type": "application/x-www-form-urlencoded"})
with urllib.request.urlopen(req, timeout=10) as resp:
    at = json.loads(resp.read().decode())["access_token"]
```

## Calendar

### List Events
```python
CAL = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
params = urllib.parse.urlencode({
    "timeMin": "2026-07-14T00:00:00+07:00",
    "timeMax": "2026-07-14T23:59:59+07:00",
    "singleEvents": "true",
    "orderBy": "startTime",
    "q": "optional search query"
})
req = urllib.request.Request(f"{CAL}?{params}", headers={"Authorization": f"Bearer {at}"})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    for e in data.get("items", []):
        print(e.get("summary"), e["start"].get("dateTime"))
```

### Get Single Event
```python
event_id = "a565ick0dvt1ahtcc3f1r86v6s"
req = urllib.request.Request(f"{CAL}/{event_id}", headers={"Authorization": f"Bearer {at}"})
with urllib.request.urlopen(req) as resp:
    event = json.loads(resp.read().decode())
```

### Add Attendees (PATCH)
```python
event = ...  # from get
current = event.get("attendees", [])
all_att = current + [{"email": "new@example.com"}]
update = json.dumps({"attendees": all_att}).encode()
req = urllib.request.Request(
    f"{CAL}/{event_id}?sendUpdates=all",
    data=update,
    headers={"Authorization": f"Bearer {at}", "Content-Type": "application/json"},
    method="PATCH"
)
with urllib.request.urlopen(req) as resp:
    updated = json.loads(resp.read().decode())
```

## Gmail

### Search Messages
```python
GM = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
params = urllib.parse.urlencode({"q": "Roslan OR Bendenia", "maxResults": 5})
req = urllib.request.Request(f"{GM}?{params}", headers={"Authorization": f"Bearer {at}"})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    for m in data.get("messages", []):
        mid = m["id"]
        # Get details
        req2 = urllib.request.Request(
            f"{GM}/{mid}?format=metadata&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Subject",
            headers={"Authorization": f"Bearer {at}"})
        with urllib.request.urlopen(req2) as resp2:
            msg = json.loads(resp2.read().decode())
        hd = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(hd.get("From"), hd.get("Subject"))
```

## Contacts

Contacts API requires the `contacts.readonly` scope. If the token lacks this scope, use Gmail search or Stripe instead to find client emails (see references/client-email-hunting.md).
```

## Pitfalls

- **Token scope matters.** Calendar works with the `calendar` scope. Gmail needs `gmail.readonly`. Contacts needs `contacts.readonly`. If an API returns 401/403, check what scopes the token has — re-authenticate with broader scopes if needed.
- **Refresh before every session.** The access token expires after ~1 hour. Always run the refresh flow before making API calls.
- **Gmail search syntax.** Use `from:`, `to:`, `OR`, quoted phrases. See Gmail search operators for full syntax.
- **Calendar timezones.** Always include timezone offset (e.g. `+07:00`) — Google Calendar stores in event's local time.
- **sendUpdates=all.** When modifying events (PATCH), always include `?sendUpdates=all` so attendees get email notifications.

## References

- `references/client-email-hunting.md` — How to find client emails across Stripe, Gmail, and Calendar when contacts API is unavailable.