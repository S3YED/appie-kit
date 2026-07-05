---
name: typeform-api
description: "Typeform REST API — create, update, and manage forms with fields, logic, thankyou screens, and contact_info. Covers API quirks and field-type gotchas discovered through real usage."
version: 1.0.0
author: hermes
tags: [typeform, forms, api, quizzes, lead-generation]
---

# Typeform API

Create and manage Typeform forms programmatically via the REST API.

## Authentication

API key (Bearer token) in `Authorization` header. Stored at `/tmp/tf_token.txt`.

## Form Creation — Two-Step Pattern

**Do NOT try to create a form with everything in one POST.** Typeform's API rejects forms that reference thankyou screens or logic that don't exist yet. Always use this two-step pattern:

### Step 1: POST (create bare form)
```python
POST https://api.typeform.com/forms
{
  "title": "Form Title",
  "type": "quiz",
  "settings": { ... },
  "fields": [ ... ]
  # NO thankyou_screens
  # NO logic
}
```

### Step 2: GET (fetch form, get auto-generated IDs)
```python
GET https://api.typeform.com/forms/{form_id}
```
This returns the form with auto-generated `thankyou_screens` (default ref: `default_tys`) and field IDs.

### Step 3: PUT (add logic and thankyou screens)
```python
PUT https://api.typeform.com/forms/{form_id}
# Send the FULL form object from GET + your additions
form["logic"] = [...]
form["thankyou_screens"] = [...]
```

## Key Gotchas

### thankyou_screens
- Must be at the **top level** of the JSON, NOT inside `settings`
- **If setting custom thankyou screens is complex or fails, fall back to the default.** Most funnels can just use the single default screen and let the logic reference `default_tys`.
- The default thankyou screen ref is always `default_tys` — safe to use in logic jumps.
- Custom thankyou screens with `show_button`, `button_text`, `button_mode` inside `properties` may be **rejected** by the API. If you need custom screens with specific messaging, create them in the Typeform UI instead.
- When using `PUT` to add logic, make sure the thankyou_screens array from the GET response is preserved — stripping it out causes "UNKNOWN_THANKYOU_REFERENCE" errors in the logic.

### Logic (field jumps)
- `condition` is at the **action level**, NOT inside `details`
- Correct structure:
```json
{
  "type": "field",
  "ref": "field_ref",
  "actions": [
    {
      "action": "jump",
      "details": {"to": {"type": "thankyou", "value": "thankyou_ref"}},
      "condition": {"op": "is", "vars": [
        {"type": "field", "value": "field_ref"},
        {"type": "choice", "value": "choice_ref"}
      ]}
    },
    {
      "action": "jump",
      "details": {"to": {"type": "field", "value": "next_field_ref"}},
      "condition": {"op": "always", "vars": []}
    }
  ]
}
```

### Yes/No field type
- `yes_no` type has **auto-generated choice refs** that cannot be predicted or set
- You CANNOT reference "Yes" or "No" as choice refs in logic
- **Workaround:** Use `multiple_choice` with explicit refs instead:
```json
{
  "ref": "q_question",
  "title": "Question?",
  "type": "multiple_choice",
  "properties": {
    "choices": [
      {"ref": "choice_yes", "label": "Yes"},
      {"ref": "choice_no", "label": "No"}
    ]
  }
}
```

### contact_info field
Requires nested `fields` array, NOT flat properties:
```json
{
  "ref": "contact",
  "title": "Your details",
  "type": "contact_info",
  "properties": {
    "fields": [
      {"ref": "first_name", "title": "Name", "subfield_key": "first_name", "type": "short_text", "properties": {}, "validations": {"required": true}},
      {"ref": "last_name", "title": "Last name", "subfield_key": "last_name", "type": "short_text", "properties": {}, "validations": {"required": true}},
      {"ref": "phone", "title": "Phone", "subfield_key": "phone_number", "type": "phone_number", "properties": {"default_country_code": "gb"}, "validations": {"required": true}},
      {"ref": "email", "title": "Email", "subfield_key": "email", "type": "email", "properties": {}, "validations": {"required": true}}
    ]
  }
}
```

### opinion_scale
- `shape` property is NOT accepted during creation (removed from API)
- Simple format:
```json
{
  "type": "opinion_scale",
  "properties": {
    "steps": 10,
    "start_at_one": true
  }
}
```

### statement field
- Does NOT support `validations` (remove `validations` or omit)
```json
{
  "ref": "welcome",
  "title": "Welcome",
  "type": "statement",
  "properties": {
    "description": "Text here",
    "button_text": "Start",
    "hide_marks": false
  }
}
```

### PUT endpoint quirks
- PUT on an existing form requires sending the **entire form object** including `title` at top level
- Removing `thankyou_screens` from the PUT payload can cause "UNKNOWN_THANKYOU_REFERENCE" validation errors
- After PUT, always verify the form by GETing it again — the API may silently drop fields it doesn't recognise

### Form cleanup
- After creating multiple test/abandoned forms, clean them up. There's no DELETE endpoint, but you can unpublish them via the UI or leave them unused. Keep track of the active form ID in `/tmp/`.

## Qualification Patterns

### Profession gate (short_text + exact match)
```json
{
  "type": "field",
  "ref": "q_profession",
  "actions": [
    {
      "action": "jump",
      "details": {"to": {"type": "thankyou", "value": "default_tys"}},
      "condition": {"op": "equal", "vars": [
        {"type": "field", "value": "q_profession"},
        {"type": "constant", "value": "Student, unemployed, inbetween jobs"}
      ]}
    },
    {
      "action": "jump",
      "details": {"to": {"type": "field", "value": "next_field_ref"}},
      "condition": {"op": "always", "vars": []}
    }
  ]
}
```
Note: The `equal` operator does exact string matching. Use a single value that captures the variations you want to block.

### Country gate (multiple_choice + choice refs)
```json
{
  "type": "field",
  "ref": "q_country",
  "actions": [
    {"action": "jump", "details": {"to": {"type": "thankyou", "value": "default_tys"}}, "condition": {"op": "is", "vars": [{"type": "field", "value": "q_country"}, {"type": "choice", "value": "asia"}]}},
    {"action": "jump", "details": {"to": {"type": "thankyou", "value": "default_tys"}}, "condition": {"op": "is", "vars": [{"type": "field", "value": "q_country"}, {"type": "choice", "value": "africa"}]}},
    {"action": "jump", "details": {"to": {"type": "field", "value": "next_field"}}, "condition": {"op": "always", "vars": []}}
  ]
}
```
The last action with `op: "always"` acts as the default/fallthrough path.

## Settings (recommended defaults)
```json
{
  "progress_bar": "proportion",
  "meta": {"allow_indexing": false},
  "hide_navigation": false,
  "is_public": true,
  "show_progress_bar": true,
  "show_typeform_branding": false,
  "show_time_to_complete": false,
  "show_number_of_submissions": false,
  "show_cookie_consent": false,
  "show_question_number": false,
  "hide_required_indicator": false,
  "free_form_navigation": false,
  "use_lead_qualification": false,
  "partial_responses_to_all_integrations": true
}
```

## Field Types Reference

See `references/field-types.md` for the exact API format of all field types encountered in real usage.

## Ibrahim's Form Patterns

See `references/ibrahim-form-patterns.md` for the three funnel-specific Typeform templates (giveaway, low-ticket, high-ticket) and asset hosting details.