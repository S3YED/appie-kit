# GHL Inbound Webhook — Typeform Field Mapping

Typeform webhooks → GHL "Create/Update Contact" action requires manual field mapping inside the GHL workflow. The user found this non-obvious — here's the exact process.

## Prerequisites

- A GHL workflow exists with **Inbound Webhook** as the trigger
- The webhook URL is registered in Typeform (as a `PUT /forms/{id}/webhooks/{tag}` webhook)
- At least one test form submission has been sent through Typeform

## Step-by-Step

### 1. Create the workflow trigger
- GHL → Automations → Workflows → Create Workflow
- Trigger: Inbound Webhook
- GHL generates a URL — copy and send it to the developer to register in Typeform
- **Do not proceed until the webhook is registered and enabled** (check via `GET /forms/{id}/webhooks`)

### 2. Add the "Create/Update Contact" action
- Inside the workflow, add an action: **Create/Update Contact**
- The Action Name field is just a label — leave as "Create Contact" unless you have multiple

### 3. Add fields to the action
- Click **"+ Add field"** for each field you want captured
- **Required fields:** Email, First Name, Last Name, Phone
- **Optional but useful:** Tags (manually type `Giveaway Lead` as the value)
- **Ignore:** Business Name, City, Country, Date of Birth, Contact Type, Contact Source — Typeform doesn't send these

### 4. Map the incoming data (the confusing part)
- Click on the field you just added (e.g. "Email")
- A side panel opens showing the incoming webhook payload from the test submission
- Click the corresponding value in the payload to map it — e.g. click `email` from the Typeform contact_info to fill the GHL Email field
- **Common pitfall:** If the side panel shows NO data, the test submission hasn't hit GHL yet. Submit another test entry and refresh.

### 5. GHL auto-mapping
- GHL may auto-map `contact.name`, `contact.email`, and `contact.phone` from the webhook — these appear automatically in the action summary
- If they appear auto-mapped, you don't need to manually add those fields
- You still need to add **Tags** manually (type the value, don't map from webhook)

## KNOWN ISSUE: Field Dropdown Shows Wrong Options

Multiple users have reported that when clicking `"+ Add Field"` in the Create Contact action, the dropdown only shows:

- Business Name, City, Contact Source, Contact Type, Country, Date of Birth

**Email, First Name, Last Name, Phone are NOT in this list.** This is not a bug — these are core contact fields that GHL handles differently. They may already be auto-mapped (check the action summary for `{{contact.name}}`, `{{contact.email}}`, `{{contact.phone}}`). If they are NOT auto-mapped, the Inbound Webhook trigger may need a fresh test submission to populate the sample data panel.

**Fix:**
1. Delete the workflow and create a fresh one
2. Send a test submission to the new webhook URL BEFORE adding any fields
3. When the sample data appears in the trigger settings, add the Create Contact action — GHL should auto-map the core fields
4. If auto-mapping still fails, use **GHL Native Forms** instead of Typeform + webhook

## Fallback: GHL Native Forms (Skip Workflow Entirely)

If the inbound webhook field mapping continues to fail, switch to GHL's native form builder:

1. GHL → Marketing → Surveys & Forms → Create Form
2. Add fields: First Name, Last Name, Email, Phone + your custom questions
3. Publish → get the form URL or embed code
4. Replace the Typeform embed on your landing page with the GHL form

**Advantages:** Every submission creates a contact in GHL automatically. Zero workflow configuration, zero field mapping, zero API keys. Works every time.

**Disadvantage:** Lose Typeform's analytics and existing form data (can export CSV and import to GHL).

### 6. Save and enable
- Save the workflow
- Toggle it to **Active**
- Submit a third test entry and verify the contact appears in GHL Contacts

## Common Issues

| Problem | Fix |
|---------|-----|
| Webhook registered but "AUTHENTICATION_FAILED" | Token expired — get a new one from the user |
| Test submission shows nothing in GHL | The webhook URL might point to a deleted workflow. Create a new workflow, copy the new URL, update Typeform webhook |
| "Create Contact" action has no data panel | The action runs with "contactless execution" (inbound webhook). It needs at least one test submission to show sample data |
| GHL shows "Contact type" dropdown instead of data fields | You're looking at the field type selector, not the data mapper. Click the field VALUE (the empty space next to the field name) to open the data panel |

## Typeform Payload Structure

Typeform's contact_info field sends nested data:

```json
{
  "form_response": {
    "answers": [
      {
        "field": {"ref": "2332382b-5762-409e-be79-16220636b064"},
        "type": "contact_info",
        "contact_info": {
          "first_name": "Ahmed",
          "last_name": "Khan",
          "email": "ahmed@example.com",
          "phone_number": "+971501234567"
        }
      }
    ]
  }
}
```

GHL parses this automatically — you don't need to write any extraction logic. The data panel shows `first_name`, `last_name`, `email`, `phone_number` as mappable fields.