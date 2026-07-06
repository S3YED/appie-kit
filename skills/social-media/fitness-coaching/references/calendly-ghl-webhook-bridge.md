# Calendly → GoHighLevel Webhook Bridge

Deploy a Vercel serverless function that receives Calendly "invitee.created" webhooks and creates contacts (and optionally opportunities) in GoHighLevel.

## When to Use

- The client uses Calendly for booking strategy calls (not GHL's native calendar)
- The client wants booked calls to auto-create contacts in GHL without manual entry
- The client doesn't want to use Zapier/Make.com as a middleman

## Architecture

```
Calendly (booked call)
  ↓ POST webhook
Vercel serverless function (/api/calendly-webhook.js)
  ↓
POST /contacts/ → GoHighLevel (creates contact with tags "calendly-booking", "strategy-call")
POST /opportunities/ → GoHighLevel (optional — creates pipeline entry)
```

## Prerequisites

- Vercel project deployed (existing landing page project works)
- GHL Private Integration Token (`pit-...`) with contacts.write scope
- GHL Location ID
- (Optional) GHL Pipeline ID + Stage ID for opportunity creation
- (Optional) Calendly API token for programmatic webhook subscription

## Setup Steps

### 1. Deploy the webhook function

Create `/api/calendly-webhook.js`:

```javascript
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const payload = req.body;
    const invitee = payload?.payload?.invitee || {};
    const event = payload?.payload?.event || {};

    const firstName = invitee.first_name || invitee.name?.split(' ')[0] || 'Unknown';
    const lastName = invitee.last_name || invitee.name?.split(' ').slice(1).join(' ') || '';
    const email = invitee.email || '';
    const phone = invitee.phone || '';
    const scheduledTime = event.start_time ? new Date(event.start_time).toISOString() : '';

    let notes = `Booked via Calendly\nCall: ${event.name || 'Strategy Call'}\nScheduled: ${scheduledTime}\n`;
    if (invitee.questions_and_answers?.length) {
      invitee.questions_and_answers.forEach(qa => {
        notes += `${qa.question}: ${qa.answer}\n`;
      });
    }

    const ghlToken = process.env.GHL_TOKEN;
    const ghlLocation = process.env.GHL_LOCATION_ID;

    const contactPayload = {
      firstName, lastName, email, phone,
      locationId: ghlLocation,
      tags: ['calendly-booking', 'strategy-call'],
      notes
    };

    const contactResponse = await fetch('https://services.leadconnectorhq.com/contacts/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${ghlToken}`,
        'Content-Type': 'application/json',
        'Version': '2021-07-28'
      },
      body: JSON.stringify(contactPayload)
    });

    if (!contactResponse.ok) {
      const errText = await contactResponse.text();
      return res.status(500).json({ error: 'Contact creation failed', detail: errText });
    }

    const contactData = await contactResponse.json();

    // Optionally create opportunity
    const pipelineId = process.env.GHL_PIPELINE_ID;
    const stageId = process.env.GHL_STAGE_ID;
    const userId = process.env.GHL_USER_ID;

    if (contactData.contact?.id && pipelineId && stageId) {
      await fetch('https://services.leadconnectorhq.com/opportunities/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${ghlToken}`,
          'Content-Type': 'application/json',
          'Version': '2021-07-28'
        },
        body: JSON.stringify({
          contactId: contactData.contact.id,
          locationId: ghlLocation,
          pipelineId,
          pipelineStageId: stageId,
          name: `${firstName} ${lastName} - Strategy Call`,
          status: 'open',
          assignedTo: userId || ''
        })
      }).catch(() => {});
    }

    return res.status(200).json({ success: true, contactId: contactData.contact?.id });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
```

### 2. Add vercel.json for API routes

```json
{
  "functions": {
    "api/*.js": { "maxDuration": 10 }
  },
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/$1" },
    { "source": "/(.*)", "destination": "/$1" }
  ]
}
```

### 3. Set environment variables on Vercel

```
GHL_TOKEN       → pit-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
GHL_LOCATION_ID → location UUID (from GHL dashboard URL)
GHL_PIPELINE_ID → pipeline UUID (optional, for opportunities)
GHL_STAGE_ID    → stage UUID (optional)
GHL_USER_ID     → user UUID (optional, to assign the opportunity)
```

Deploy: `npx vercel --prod`

### 4. Connect Calendly webhook

**Via Calendly UI (recommended):**
1. Calendly → Account → Integrations → Webhooks
2. Add Webhook: `https://your-site.vercel.app/api/calendly-webhook`
3. Select event: "Invitee Created"
4. Save

**Via Calendly API (alternative):**
```bash
curl -s -X POST "https://api.calendly.com/webhook_subscriptions" \
  -H "Authorization: Bearer CALENDLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-site.vercel.app/api/calendly-webhook",
    "events": ["invitee.created"],
    "scope": "user",
    "organization": "https://api.calendly.com/organizations/ORG_UUID"
  }'
```

## Testing

```bash
curl -X POST "https://your-site.vercel.app/api/calendly-webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "payload": {
      "invitee": {
        "name": "Test User",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User"
      },
      "event": {
        "name": "Strategy Call",
        "start_time": "2026-07-01T10:00:00Z"
      }
    }
  }'
```

Check GHL dashboard → Contacts for the new entry.

## Pitfalls

- **Token masking in responses**: GHL tokens starting with `pit-` may be masked with `***` in agent response text, corrupting code. Store tokens in temp files and use `terminal()` not `execute_code()`.
- **GHL API 403 errors**: The token may have expired or been regenerated. Ask the user to check Settings → Private Integrations in GHL and generate a fresh one.
- **Vercel free tier:** 250 MB total limit for serverless functions and static assets combined. Keep the function lightweight (~5 KB).
- **Calendly test mode:** Calendly test bookings don't fire webhooks. Use the curl test above before going live.
- **Opportunity creation is optional**: If the pipeline endpoint returns 403 (common with sub-account level tokens), just skip it. Contact creation alone is still useful.
