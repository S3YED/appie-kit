# GoHighLevel API — Private Integration Token Setup

For connecting a GHL sub-account to a coding agent. Uses the newer Private Integration token format (starts with `pit-`). The old `rest.gohighlevel.com` API key system is deprecated — all new integrations use Private Integrations.

## Token Format

New format: `pit-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` (starts with `pit-`, UUID-style)
Old format (deprecated, V1): `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` (no prefix)

## How to Generate

**Agency level** (accesses all sub-accounts):
1. Agency settings → Integrations → Private Integrations
2. "Create new Integration" → name it → select scopes → copy token

**Location/Sub-account level** (scoped to one location):
1. Settings (gear icon) → Integrations → Private Integrations
2. "Create new Integration" → name it → copy token

Available under both Starter/Unlimited and Agency Pro plans.

The location ID is ~20 alphanumeric chars. Visible in the browser URL:

```
# GHL UI (both v1 and v2):
https://app.gohighlevel.com/v2/location/<LOCATION_ID>/settings/...
https://app.gohighlevel.com/location/<LOCATION_ID>/dashboard
```

NOT `rest.gohighlevel.com` (old V1) — that returns "Unauthorized, Switch to the new API token."

## Required Headers

```
Authorization: Bearer <pit-token>
Version: 2021-07-28
Content-Type: application/json
User-Agent: Mozilla/5.0
```

The `Version` header is mandatory. Without it: `"version header was not found."` (401)
The `User-Agent` header is needed for Python/curl — Cloudflare returns Error 1010 / 403 without it.

## Making API Calls (Python Preferred, NOT bash curl)

The token contains hyphens and UUID characters that break bash quoting/escaping in `curl`. Use Python's `urllib.request` instead:

```python
import urllib.request, json

req = urllib.request.Request(
    f"https://services.leadconnectorhq.com/contacts/?locationId={LOCATION_ID}&limit=5",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Version": "2021-07-28",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
```

Do NOT use shell `curl` with the token in `-H "Authorization: Bearer $TOKEN"` — shell string splitting will corrupt the token value.

## Finding the Location ID

The location ID is ~20 alphanumeric chars. Visible in the browser URL:

```
# GHL UI (both v1 and v2):
https://app.gohighlevel.com/v2/location/<LOCATION_ID>/settings/...
https://app.gohighlevel.com/location/<LOCATION_ID>/dashboard
```

The location ID is ~20 alphanumeric chars.

For agency-level tokens, list locations via:
```
GET /locations/
```
(returns 404 for location-level tokens)

## Common Endpoints

| Purpose | Method | URL | Notes |
|---|---|---|---|
| Get location | GET | `/locations/{locationId}` | Requires location ID |
| List contacts | GET | `/contacts/?locationId={locationId}` | |
| Create contact | POST | `/contacts/` | With `locationId` in body |
| Get calendars | GET | `/calendars/?locationId={locationId}` | |
| Create opportunity | POST | `/pipelines/opportunities/` | |
| Send email | POST | `/conversations/messages/email` | |
| Send SMS | POST | `/conversations/messages/sms` | |

Full docs: https://marketplace.gohighlevel.com/docs/

## V1 Deprecation (Critical — discovered July 2026)

GHL officially deprecated the V1 REST API on **31 December 2025**:

- `rest.gohighlevel.com/v1/` — no longer operational
- `pit-` prefix API keys generated from Settings → Company Settings → API Keys are **V1 keys only**. Even freshly generated, they return 401 `{"msg":"Api key is invalid."}` because the V1 endpoint is dead
- **This is NOT a token expiry problem** — V1 is simply shut down. Generating new keys in the same place produces the same result

### V2 Authentication Problem

V2 uses `services.leadconnectorhq.com` and requires JWT tokens (OAuth 2.0 or Private Integration access tokens). The `pit-` prefix keys from Company Settings → API Keys **do not work** with V2 either — they return `{"statusCode":401,"message":"Invalid JWT"}`.

### Reliable Workaround — Inbound Webhook

The only reliable way to push leads into GHL programmatically (as of July 2026) is the **Inbound Webhook** trigger:

1. GHL → Automations → Workflows → Create Workflow → Trigger: **Inbound Webhook**
2. GHL generates a URL like `https://services.leadconnectorhq.com/hooks/{locId}/webhook-trigger/{uuid}`
3. Register that URL as a Typeform webhook via `PUT /forms/{id}/webhooks/{tag}`
4. In the workflow, add a **Create/Update Contact** action
5. Submit a test entry through Typeform, then map the fields in GHL

This uses GHL's internal routing — no API key required. The webhook URL is the authentication mechanism.

### Alternative — GHL Native Forms

Skip API entirely. Build the form in GHL's Surveys & Forms (Marketing section). Every submission creates a contact automatically with zero workflow configuration. Replace the Typeform embed on the landing page with the GHL form embed or a link to the GHL form URL.

## Error Reference

| Error | Meaning | Fix |
|---|---|---|
| "Unauthorized, Switch to the new API token." | Using V1 endpoint with V2 token | Use `services.leadconnectorhq.com` |
| "version header was not found." | Missing Version header | Add `Version: 2021-07-28` |
| "The token does not have access to this location." | Wrong location ID for token scope | Use the correct location ID |
| "Invalid Private Integration token" | Token malformed or expired | Regenerate in GHL settings |
| `{"msg":"Api key is invalid."}` (401 on `rest.gohighlevel.com`) | **V1 API deprecated since 31 Dec 2025** | Use inbound webhook instead |
| `{"statusCode":401,"message":"Invalid JWT"}` (401 on `services.leadconnectorhq.com`) | pit- token not accepted as JWT on V2 | Use inbound webhook instead |
| 200 with empty body | Endpoint doesn't exist at path | Double-check URL path |