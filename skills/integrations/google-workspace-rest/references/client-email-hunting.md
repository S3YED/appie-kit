# Client Email Hunting

When you need a client's email but it's not in Google Contacts (token lacks `contacts.readonly` scope), fall through these sources in order:

## 1. Stripe API (Clark clients)

```python
import json, os, urllib.request, base64

# Load Stripe key
env = {}
with open(os.path.expanduser("~/.weblyfe-secrets/.env")) as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")

key = env.get("STRIPE_CLARK_LIVE_SECRET")
auth = base64.b64encode(f"{key}:".encode()).decode()

req = urllib.request.Request(
    "https://api.stripe.com/v1/customers?limit=50",
    headers={"Authorization": f"Basic {auth}"}
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    for c in data.get("data", []):
        print(c.get("email"), c.get("name"))
```

## 2. Gmail search (requires gmail.readonly scope)

```python
# Search for the person's name in From/To headers
params = urllib.parse.urlencode({"q": "from:Roslan OR to:Roslan", "maxResults": 5})
req = urllib.request.Request(f"{GM}?{params}", headers={"Authorization": f"Bearer {at}"})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    for m in data.get("messages", []):
        # Get headers to extract email from From field
        ...
```

## 3. Calendar attendee search

Search past events where the person might have been an attendee:

```python
params = urllib.parse.urlencode({"q": "Roslan", "timeMin": "2026-01-01T00:00:00Z", "maxResults": 10})
req = urllib.request.Request(f"{CAL}?{params}", headers={"Authorization": f"Bearer {at}"})
# Check attendees array in returned events for their email
```

## 4. Orgo API (Clark boxes)

```python
# POST to /computers/{uuid}/bash for hostname check
url = f"https://www.orgo.ai/api/computers/{uuid}/bash"
req = urllib.request.Request(url,
    data=json.dumps({"command": "hostname"}).encode(),
    headers={"Authorization": f"Bearer ***", "Content-Type": "application/json"})
```

## Priority Order
1. **Stripe** — fastest, always has email, works for all paid clients
2. **Gmail** — if you have the scope, search by name/persona
3. **Calendar** — search past event attendees
4. **Orgo** — box hostname confirms identity, but no email field

## Real Session Results (2026-07-14)
- Ibrahim Ramzy → `ramzy@cali-creed.com` (Stripe Clark Live)
- Roslan Bendenia → `rosscoaching@hotmail.com` (Gmail: "Fwd: Request for Review of Account Closure - ECOM KNOCKOUT ACADEMY")