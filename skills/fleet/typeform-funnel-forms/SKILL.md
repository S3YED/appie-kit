---
name: typeform-funnel-forms
description: "Build qualification/delivery Typeforms for coaching funnels. Covers country/profession gates, logic jumps, thankyou screen refs, and embedding in landing pages."
version: 1.0.0
author: community
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  env_vars: [TYPEFORM_API_KEY]
---

# Typeform Funnel Forms

Build qualification forms for coaching funnels. Covers low-ticket, high-ticket, and giveaway variants. Uses the Typeform Create API.

## Setup

```bash
# Store API key
printf 'tfp_your_key_here' > /tmp/tf_token.txt

# Auth header for all calls
# Authorization: Bearer $(cat /tmp/tf_token.txt)
# Content-Type: application/json
```

## Common Form Structures

### Flow: Welcome → Qualification → Deep Questions → Contact → Thankyou

### 1. High-Ticket (£997+)
- Country gate → disqualify Asia/Africa/South America
- Profession → disqualify student/unemployed
- Budget/investment question
- Calendly scheduling block
- Contact info

### 2. Low-Ticket ($99/mo)
- No budget gate (everyone can afford it)
- "Does this look like you?" (Yes/No using multiple_choice, NOT yes_no)
- Yes → "Why now?" → Contact info → Thankyou
- No → "What's missing?" → Contact info → Redirect to high-ticket LP
- Contact info always required to deliver the programme

### 3. Giveaway
- Welcome screen with prize value ($5,000) and urgency (14 days)
- Deep motivation questions (situation, vision, why now)
- Commitment score (1-10 opinion_scale)
- Contact info
- Country gate + profession (optional — see "Lightweight Giveaway" below)
- "If you don't win, still interested?" (optional)

#### Lightweight Giveaway Variant (Proven — N4LbJCHT)
Ibrahim's live giveaway form uses a **5-field, 60-second version** that outperforms the full form. No country gate, no Instagram, no WhatsApp opt-in, no profession, no "still interested" question. Structure:

1. `statement` — Welcome with prize value + urgency
2. `multiple_choice` — "What's really made you want to enter?" (5 pre-written options about starting over, health struggles, etc.)
3. `long_text` — "In one line, what would transforming in 12 weeks do for you?"
4. `opinion_scale` — Commitment 1-10
5. `contact_info` — First name, last name, phone, email

**When to use the lightweight version:**
- Giveaway is promoted from Instagram stories (short attention span)
- Goal is lead volume over qualification depth
- You have a follow-up process (WhatsApp) to qualify later

**When to use the full version:**
- Giveaway is promoted via email/ads (higher-intent audience)
- Country geo-restrictions are critical
- You need Instagram handle for content repurposing

## Critical API Quirks

### Creating Forms (POST /forms)
```python
# CORRECT — create without logic first
form_data = {
    "title": "Form Title",
    "type": "quiz",  # required
    "settings": { ... },  # NO thankyou_screens here
    "fields": [...]  # all fields
}
POST /forms → get form_id
```

### Adding Logic (PUT /forms/{id})
```python
# After creation, GET the full form, add logic, PUT back
form = GET /forms/{id}   # get the complete object with auto-generated IDs
form["logic"] = [...]
PUT /forms/{id} with form  # sends complete updated form
```

### Key Restrictions

| Pattern | Do This | NOT This |
|---------|---------|----------|
| Yes/No questions | Use `type: "multiple_choice"` with explicit choice refs | `type: "yes_no"` — can't reference choices in logic via API |
| Opinion scale | `properties: {"steps": 10, "start_at_one": True}` | DO NOT include `shape` property |
| Thankyou screens | Use default `"default_tys"` ref in logic | Cannot create custom thankyou screens via API; must edit in Typeform UI |
| Contact info | `type: "contact_info"` with nested `fields[]` array | Flat properties (show_first_name, etc. are not allowed) |
| Language | Only in `settings.language`, NOT at top level | Top-level `"language"` key causes validation error |

### Logic Condition Format
```python
# IS (for multiple_choice):
{"op": "is", "vars": [
    {"type": "field", "value": "field_ref"},
    {"type": "choice", "value": "choice_ref"}
]}

# EQUAL (for short_text matching):
{"op": "equal", "vars": [
    {"type": "field", "value": "field_ref"},
    {"type": "constant", "value": "Exact string"}
]}

# ALWAYS (fallthrough):
{"op": "always", "vars": []}
```

### Default Thankyou Screen
Created automatically with every form. Ref is always `"default_tys"`. Use this in logic jumps:

```python
{"details": {"to": {"type": "thankyou", "value": "default_tys"}}}
```

## Embedding in Landing Pages

```html
<div
  data-tf-widget="FORM_ID"
  data-tf-medium="snippet"
  data-tf-iframe-props="title=Form Title"
  data-tf-inline-on-mobile="true"
  data-tf-hide-headers="true"
  data-tf-opacity="100"
  style="width:100%;height:700px;"
></div>
<script src="https://embed.typeform.com/next/embed.js"></script>
```

## Webhooks (Lead Capture Pipeline)

Every Typeform can send a real-time POST to any URL when a form is submitted. Use this for lead capture.

### Registering a webhook (PUT /forms/{id}/webhooks/{tag})

```python
import json, urllib.request

key = open('/tmp/tf_token.txt').read().strip()
form_id = "N4LbJCHT"  # your form ID
tag = "my-webhook"     # unique identifier for this webhook

data = json.dumps({
    "url": "https://your-endpoint.com/api/lead",
    "enabled": True,
    "verify_ssl": True
}).encode()

req = urllib.request.Request(
    f'https://api.typeform.com/forms/{form_id}/webhooks/{tag}',
    data=data,
    headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    },
    method='PUT')  # PUT creates or updates

resp = urllib.request.urlopen(req, timeout=10)
print('Webhook registered:', resp.status)
```

### Verifying webhooks (GET .../webhooks)

```python
req = urllib.request.Request(
    f'https://api.typeform.com/forms/{form_id}/webhooks',
    headers={'Authorization': f'Bearer {key}'})
resp = urllib.request.urlopen(req, timeout=10)
hooks = json.loads(resp.read())
for h in hooks.get('items', []):
    print(f'{h["tag"]}: {h["url"]} enabled={h["enabled"]}')
```

### Webhook payload format

Typeform sends a POST with this body:

```json
{
  "event_type": "form_response",
  "form_response": {
    "form_id": "N4LbJCHT",
    "submitted_at": "2026-07-02T10:00:00Z",
    "answers": [
      {"type": "choice", "field": {"ref": "q_situation"}, "choice": {"label": "..."}},
      {"type": "text", "field": {"ref": "q_vision"}, "text": "..."},
      {"type": "number", "field": {"ref": "q_commitment"}, "number": 8},
      {"type": "short_text", "field": {"ref": "UUID"}, "text": "First name"},
      {"type": "short_text", "field": {"ref": "UUID"}, "text": "Last name"},
      {"type": "phone_number", "field": {"ref": "UUID"}, "phone_number": "+44..."},
      {"type": "email", "field": {"ref": "UUID"}, "email": "user@example.com"}
    ]
  }
}
```

### Parsing responses — critical format detail

**`contact_info` fields are FLATTENED into separate answers in the response.** Each sub-field (first name, last name, phone, email) appears as its own answer object with a UUID ref. You CANNOT look up contact info fields by their `field.ref` — the UUIDs are generated per form and unpredictable.

**Correct detection approach — match by TYPE, not by ref:**

```javascript
// Node.js (Vercel serverless)
for (const a of answers) {
  const ref = a.field?.ref || "";
  const type = a.type;

  if (type === "email") {
    email = a.email || "";
  } else if (type === "phone_number") {
    phone = a.phone_number || "";
  } else if (type === "short_text") {
    // First short_text = first name, second = last name
    if (!firstName) firstName = a.text || "";
    else if (!lastName) lastName = a.text || "";
  }
  // Known refs for non-contact fields
  else if (ref === "q_situation") { ... }
  else if (ref === "q_vision") { ... }
  else if (ref === "q_commitment") { ... }
}
```

For known non-contact fields, use `field.ref` (they have stable human-readable refs like `q_situation`, `q_vision`, `q_commitment`).

### Storing leads (Vercel /tmp/ limitation)

Vercel serverless functions have **ephemeral /tmp/** — data written to `/tmp/leads.json` is lost between function instances. Do NOT rely on it as a persistent store.

**Vercel API route conflict:** If the Vercel project has `@vercel/static` in vercel.json builds, API functions (`api/*.js`) are silently ignored and return 404. Remove `@vercel/static` builds or add explicit `@vercel/node` build config for API routes.

**Webhook re-enabling:** When creating or updating a Typeform webhook, the response confirms the webhook is enabled. However, an existing webhook may remain disabled if the tag already exists. Always verify with GET /webhooks and explicitly set `"enabled": true` in the PUT body. The webhook endpoint URL must match the deployed Vercel URL exactly (including the project's production domain).

**Working architecture for lead capture without a CRM API:**

```
Typeform → Webhook → Vercel API (acknowledges receipt)
                        ↓
        Cron poller (GET /forms/{id}/responses every hour)
                        ↓
              Local JSON file (leads-database.json)
                        ↓
              Daily summary (Telegram/email)
```

The cron poller is the backbone — it queries Typeform's API directly for new responses and stores them on a persistent server. The webhook provides real-time acknowledgment so Typeform doesn't retry.

### Cron poller pattern (Python)

Store last poll time in `/root/.last_poll_time`. On each run, query `GET /forms/{id}/responses?since={last_time}&limit=100`. Deduplicate by `response_id` against the local database. Append new responses.

```python
import json, urllib.request, os
from datetime import datetime, timezone

key = open('/tmp/tf_token.txt').read().strip()
form_id = "N4LbJCHT"
last_file = "/root/.last_poll_time"
db_file = "/root/leads-database.json"

# Read last poll time
since = ""
if os.path.exists(last_file):
    since = open(last_file).read().strip()

# Fetch responses
since_param = f"&since={since}" if since else ""
url = f"https://api.typeform.com/forms/{form_id}/responses?limit=100{since_param}"
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {key}'})
data = json.loads(urllib.request.urlopen(req, timeout=15).read())

# Save new responses to database
db = json.load(open(db_file)) if os.path.exists(db_file) else []
existing_ids = {r.get('data', {}).get('_typeform_response_id') for r in db}

for item in data.get('items', []):
    rid = item.get('response_id', '')
    if rid in existing_ids:
        continue
    db.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": {
            "_typeform_response_id": rid,
            "_typeform_submitted_at": item.get('submitted_at', ''),
            # ...extract answers...
        }
    })

json.dump(db, open(db_file, 'w'), indent=2)

# Update last poll time
open(last_file, 'w').write(data['items'][0]['submitted_at'] if data.get('items') else since or datetime.now(timezone.utc).isoformat())
```

This pattern handles: deduplication, incremental polling, crash recovery (since stored in file), and works without any CRM API access.

### Registering the poller as a Hermes cron job

Once the poller script lives at `~/.hermes/scripts/poll-typeform.py`, register it as a no-agent cron job (the script runs directly without an LLM):

```
cronjob action=create
  name="Typeform Poller (Hourly Backup)"
  schedule="0 * * * *"
  script="poll-typeform.py"
  no_agent=true
  deliver="local"
```

Key constraints for Hermes cron jobs:
- **`no_agent=true`**: runs the Python script directly — no LLM overhead, instant execution.
- **`script` path must be RELATIVE** to `~/.hermes/scripts/`. Absolute paths fail with "Script path must be relative".
- **`deliver="local"`**: stdout goes to local cron logs, not to the user's Telegram/chat.
- The script must be **self-contained** — it reads its own token from `/tmp/tf_token.txt` and stores data in `/root/leads-database.json` and `/root/.last_poll_time`.
- Verify the cron works by running it once with `cronjob action=run job_id=<id>`, then check `cronjob action=list` to confirm `last_status: "ok"`.

### Data cleanup for lead databases

When converting from raw Typeform dumps to clean parsed leads, the contact_info sub-fields use UUID refs (generated per form). These UUIDs are NOT stable across sessions. Detect and extract them at cleanup time:

```python
# Known field UUIDs from the N4LbJCHT form (verify current UUIDs before running)
CN_FIRST = '33dfb589-3a48-443a-93b7-b1bacf5beb7e'
CN_LAST = '99021b03-5007-4e7a-98d5-6a2a99a123cf'
CN_PHONE = 'fdc60924-fd8b-4431-84a9-0430ef80039d'
CN_EMAIL = '8b3b086e-3df7-4320-812a-ce878af4f63b'

# Or detect dynamically: iterate through raw entries and find UUID-shaped keys
# that aren't in the known ref list (q_situation, q_vision, q_commitment)
```

This is a one-time cleanup task. Once clean, subsequent poller runs store in the clean format.

## Pitfalls

- **PUT requires the complete form** — always GET the full object first, modify, then PUT back. PUT without title/fields will fail.
- **yes_no type unusable with logic** via API — the yes/no choices have auto-generated refs not accessible to the API. Workaround: use `multiple_choice` with explicit refs like `choice_yes` and `choice_no`.
- **Thankyou screens cannot be created or modified via API** — you can only reference the default one in logic. To customise the thankyou screen (message, redirect, image), edit it in the Typeform UI at `admin.typeform.com/form/{form_id}/create`.
- **Statement/contact_info fields don't need validations** — for statement type, omit `validations: {"required": ...}` entirely.
- **Rate limit** — ~3 req/s. Add `time.sleep(2)` between POST and subsequent PUT.
- **403 from API key** — Usually means the key expired or was revoked. Generate a new one from Typeform admin.
