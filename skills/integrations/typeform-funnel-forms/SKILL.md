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
