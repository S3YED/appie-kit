# Typeform Recreation & API Integration

## Session-Specific Know-How (Updated June 2026)

### Two Approaches to Form Creation

**A) PUT on existing form (when form ID already exists):**
```python
# Build complete payload with ALL fields + logic + thankyou screens
form = {"title": "...", "type": "quiz", "settings": {...}, "fields": [...], "logic": [...], "thankyou_screens": [...]}
payload = json.dumps(form).encode('utf-8')
req = urllib.request.Request(f"https://api.typeform.com/forms/{FORM_ID}", data=payload,
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}, method="PUT")
resp = urllib.request.urlopen(req)
```
Works because the form already exists. You send everything in one shot with refs, not IDs.

**B) Two-step POST→PUT (new forms — use this for clean creation):**
```python
# Step 1: POST without calendly field
form = {...all fields EXCEPT calendly...}
req = urllib.request.Request("https://api.typeform.com/forms", data=payload, method="POST", ...)
result = json.loads(urllib.request.urlopen(req).read())
new_id = result['id']

# Step 2: PUT with calendly field added
result['fields'].append(calendly_field_with_full_application_block)
req = urllib.request.Request(f"https://api.typeform.com/forms/{new_id}", data=new_payload, method="PUT", ...)
```
**CRITICAL:** POST rejects `installation_id` in the calendly application block (`NOT_ALLOWED_PROPERTY`). But PUT accepts it. So: POST without calendly, then PUT to add it.

### Calendly Field Format (for PUT — works with installation_id)

```python
{
    "ref": "calendly_booking",
    "title": "Book your 1-1 strategy call.",
    "type": "calendly",
    "properties": {"description": ""},
    "application": {
        "id": "calendly",
        "application_block_id": "2a6026ef-da6f-4c64-ac4f-387700a4543b",
        "installation_id": "10cc3e10-0a85-4d5b-9f6f-97609640ed95",
        "iframe_url": "https://api.typeform.com/applications/calendly/installations/{install_id}/iframe/{block_id}",
        "inputs": [
            {"value": "{{field:first_name}}", "label": "Name", "ref": "name"},
            {"value": "{{field:email}}", "label": "Email", "ref": "email"}
        ]
    },
    "validations": {"required": True}
}
```

**Required on PUT:** `application_block_id`, `installation_id`, AND `iframe_url` — API rejects if `installation_id` is present without `iframe_url`.

**The Calendly connection must be set up ONCE through Typeform admin UI.** After that, the `installation_id` and `application_block_id` are stable and can be reused. You cannot CREATE a new Calendly block via API.

### CRITICAL: Settings Format

Exact key names — GET before you build, never guess:

```python
"settings": {
    "language": "en",
    "progress_bar": "proportion",
    "meta": {"allow_indexing": False},
    "hide_navigation": False,                # NOT "show_navigation"
    "is_public": True,
    "is_trial": False,
    "show_progress_bar": True,
    "show_typeform_branding": False,
    "are_uploads_public": False,             # NOT "are_uploads_enabled"
    "show_time_to_complete": True,
    "show_number_of_submissions": False,
    "show_cookie_consent": False,
    "show_question_number": False,           # NOT "show_question_numbers"
    "hide_required_indicator": False,
    "show_key_hint_on_choices": True,
    "autosave_progress": True,
    "free_form_navigation": False,
    "use_lead_qualification": False,
    "pro_subdomain_enabled": False,
    "auto_translate": True,
    "partial_responses_to_all_integrations": True
}
```

### contact_info Field Format

Must include `properties.fields` array with subfields:

```python
{
    "ref": "contact_details",
    "title": "Your contact details",
    "type": "contact_info",
    "properties": {
        "fields": [
            {"title": "Name", "ref": "first_name", "subfield_key": "first_name",
             "properties": {}, "validations": {"required": True}, "type": "short_text"},
            {"title": "Last name", "ref": "last_name", "subfield_key": "last_name",
             "properties": {}, "validations": {"required": True}, "type": "short_text"},
            {"title": "Phone", "ref": "phone", "subfield_key": "phone_number",
             "properties": {"default_country_code": "gb"},
             "validations": {"required": True}, "type": "phone_number"},
            {"title": "Email", "ref": "email", "subfield_key": "email",
             "properties": {}, "validations": {"required": True}, "type": "email"}
        ]
    },
    "validations": {}
}
```

**Pitfall:** Use `"type": "phone_number"` NOT `"type": "phone"` — `"phone"` is INVALID.

### Logic Rules: ALL Actions in ONE Group

For DQ logic on the same field, ALL actions go in ONE rule:

```python
form["logic"].append({
    "type": "field", "ref": "country",
    "actions": [
        {
            "action": "jump",
            "details": {"to": {"type": "thankyou", "value": "disqualified"}},
            "condition": {
                "op": "is",
                "vars": [
                    {"type": "field", "value": "country"},      # field ref
                    {"type": "choice", "value": "asia"}         # choice ref
                ]
            }
        },
        # ... more conditions ...
        {
            "action": "jump",
            "details": {"to": {"type": "field", "value": "next_field_ref"}},
            "condition": {"op": "always", "vars": []}     # empty vars REQUIRED
        }
    ]
})
```

**Pitfalls:**
- `op: "always"` MUST have `vars: []` — with items it returns `MAX_ITEMS: should NOT have more than 0 items`
- Use choice REFs (short strings you set, like `"asia"`), not auto-generated IDs
- Split rules into separate logic groups → API error. Always combine same-field rules into ONE group.
- **Statement fields reject `validations`.** A `"type": "statement"` field with a `validations` object returns `NOT_ALLOWED_PROPERTY`. Omit `validations` entirely for statements.

### Token Handling: Avoid the `***` Masking Trap

The system masks known token values with `***` in your response text. This corrupts ANY code that contains the token string when written via `write_file` or `execute_code` — the `***` becomes literal syntax.

**DO NOT:**
```python
# execute_code reads your response as source — token masking breaks it
TOKEN = "tfp_abc123..."   # ← becomes TOKEN = "tfp_***..." → SyntaxError

# write_file also corrupts — the token in your response gets masked
write_file(content="TOKEN=f.read...()")
# File ends up with TOKEN = f.read...strip() instead of TOKEN = f.read().strip()
```

**DO this instead:**
```bash
# Store token in a temp file via terminal()
printf '%s' 'tfp_abc123def456...' > /tmp/tf_token.txt
```

```python
# Read from file in Python — safe because file content is NOT your response text
with open("/tmp/tf_token.txt") as fd:
    TOKEN = fd.read().strip()
# Now use TOKEN in urllib.request calls
```

Run the Python script via `terminal("python3 /tmp/script.py")` NOT via `execute_code()`.

**Alternative for quick curl:** Use bash command substitution:
```bash
curl -s -H "Authorization: Bearer $(cat /tmp/tf_token.txt)" ...
```
But note: curl quoting can still break on special characters. Python `urllib.request` is more reliable.

### The Form-Not-Appearing Problem

If the client says the form doesn't appear in their Typeform dashboard:

1. **Verify the API token email matches their login email** — check via `GET https://api.typeform.com/me`
2. **The form IS there** — the API confirms it. The user is likely logged into a different Google account
3. **Workspace mismatch** — check if the form's workspace matches the default workspace. All forms created via the `tfp_` token go to the default workspace for that account
4. **Fix:** Tell them to log out of typeform.com and log back in with the correct Google account (the one matching `me.email`)

### Landing Page: Update Widget ID After Recreation

After creating/updating a Typeform, the landing page's `data-tf-widget="gipRb80u"` needs updating. Common pattern: the old form ID survives in the HTML. Always update + redeploy:

```bash
cd /root/ibrahim
cp creed-code-landing.html index.html
vercel --token "$VTOKEN" --prod --yes
```

### Confirmed: Text-Based Logic (`contains`) Does NOT Work on Field Logic

Multiple PUT attempts confirmed: `op: "contains"` with `{"type": "text"}` vars is rejected with 400 on field-level logic, even though the validation schema lists it as valid.

**Fix:** Convert the field to `multiple_choice` with preset options and use `op: "is"`.

**Fallback for truly free-text fields:** Handle disqualification in GHL/Slack via webhook — check the submission text server-side.

### Two-Step POST→PUT for Logic + Thankyou Screens (Generic Pattern)

When creating a NEW form from scratch (no Calendly needed), use this pattern:

```python
# Step 1: POST form WITHOUT logic or thankyou screens
form = {"title": "My Form", "type": "quiz", "settings": {...}, "fields": [...]}
req = urllib.request.Request("https://api.typeform.com/forms", data=json.dumps(form).encode(), headers=headers, method="POST")
result = json.loads(urllib.request.urlopen(req).read())
form_id = result["id"]

# Step 2: READ BACK to discover auto-generated thankyou screen ref
req2 = urllib.request.Request(f"https://api.typeform.com/forms/{form_id}", headers=headers)
form_data = json.loads(urllib.request.urlopen(req2).read())
thanks = form_data.get("thankyou_screens", [])
# Typically returns: [{"ref": "default_tys", "type": "thankyou_screen", "title": "All done! Thanks for your time."}]
default_tys_ref = thanks[0]["ref"]  # "default_tys"

# Step 3: PUT full form with logic referencing the discovered ref
form_data["logic"] = [
    {
        "type": "field", "ref": "country_field_ref",
        "actions": [
            {"action": "jump", "details": {"to": {"type": "thankyou", "value": default_tys_ref}},
             "condition": {"op": "is", "vars": [{"type": "field", "value": "country_field_ref"}, {"type": "choice", "value": "asia"}]}},
            {"action": "jump", "details": {"to": {"type": "field", "value": "next_field_ref"}},
             "condition": {"op": "always", "vars": []}}
        ]
    }
]
req3 = urllib.request.Request(f"https://api.typeform.com/forms/{form_id}", data=json.dumps(form_data).encode(), headers=headers, method="PUT")
urllib.request.urlopen(req3)
```

**CRITICAL:** The auto-generated thankyou ref is `"default_tys"`, NOT `"default"`. Using `"default"` returns `UNKNOWN_THANKYOU_REFERENCE`.

**Cannot set custom thankyou_screens via API.** The `thankyou_screens` property at the top level is rejected by POST (`NOT_ALLOWED_PROPERTY` in settings) and by PUT (`NOT_ALLOWED_PROPERTY` / `REQUIRED_PROPERTY type`). You must set custom thankyou screen text in the Typeform UI after creation.

**Logic must reference EXISTING thankyou screens.** You cannot reference thankyou screens that don't exist yet. The two-step pattern (create first → discover refs → add logic) is the only reliable approach.

### Form Without Logic (e.g. Low-Ticket No-Call Forms)

For offers that don't require a booked call (e.g. $99/mo group programme):

1. Omit the `calendly` field entirely
2. End with `contact_info` field
3. Logic: country disqualification + profession disqualification → default thankyou screen
4. No investment/budget question (price is fixed)
5. Goal field uses `multiple_choice` preset options (fat_loss, lean_muscle, performance, hybrid) instead of `long_text`
6. `multiple_choice` for goal allows cleaner data in GHL/CRM
7. `allow_multiple_selection: True` on "what held you back" for richer profiling

```python
# CRITICAL Pitfall: Profession DQ uses single "equal" check
{
    "action": "jump", "details": {"to": {"type": "thankyou", "value": "default_tys"}},
    "condition": {"op": "equal", "vars": [
        {"type": "field", "value": "q5_profession"},
        {"type": "constant", "value": "Student, unemployed, inbetween jobs"}
    ]}
}
```

The `op: "contains"` with text vars does NOT work via API (returns 400). Use exact `equal` match or convert to `multiple_choice`.

### Token: 403 "error code 1010" on GHL API

GHL returning 403 with `error code: 1010` means the API token is expired/revoked or doesn't have the correct scopes. Generate a new token at:
`GoHighLevel → Settings → Integrations → API Key`

This is a GHL-specific error code, not a generic HTTP 403. Neither location ID nor different base URLs fix it — the token itself needs rotating.

## Current Live Form (Creed Ignite Application: gipRb80u)

**Widget ID:** `gipRb80u`
**Link:** https://form.typeform.com/to/gipRb80u
**Account email:** ramzy@cali-creed.com

**Field order (11 fields):**

| # | Type | Title | Notes |
|---|------|-------|-------|
| 0 | statement | Achieve your best shape in 90 days with The Creed Code | No `validations` |
| 1 | multiple_choice | Which statement resonates most with where you are right now? | 5 opts |
| 2 | long_text | What is your ideal goal for the next 90 days? | Explain look + feel |
| 3 | multiple_choice | Current training level? | 3 opts |
| 4 | multiple_choice | What has held you back until now? | 5 opts |
| 5 | multiple_choice | What have you tried in the past? | 6 opts from longer form |
| 6 | multiple_choice | Tailored programs range from £1-3+k for 90 days | <£1k → DQ |
| 7 | multiple_choice | What do you do professionally? | Student/Unemployed → DQ |
| 8 | multiple_choice | Where are you based? | Asia/Africa/S.America → DQ |
| 9 | contact_info | Your contact details | Name, phone (gb), email |
| 10 | calendly | Book your 1-1 strategy call. | Calendly block via PUT step |

**Disqualification screens:**
1. `disqualified_investment` — "programs start from £1,000"
2. `disqualified_profession` — "best suited for working professionals"
3. `disqualified_country` — "reach out within 24 hours"
4. `default_tys` — "All done!"

**Calendly booking:** https://calendly.com/ramzy-cali-creed/30min

### Calendly Calendar Conflict Fix

When Calendly removes too many time slots (checking personal calendar with training/lunch blocks):
```
calendly.com → Account → Calendar Connections → Edit → Uncheck the 
calendar with personal blocks → Save
```

### Timer Gate: sessionStorage Fix

The 90s gate timer resets on page refresh. The user found this annoying. Fix:
```javascript
// On page load — check sessionStorage
if (sessionStorage.getItem('creed_gate_passed') === 'true') {
    unlockGate();  // Gate stays unlocked across refresh
}
// In unlockGate()
sessionStorage.setItem('creed_gate_passed', 'true');
```

This persists gate state within the same browser tab. Tab scope = intentional (resets on tab close).