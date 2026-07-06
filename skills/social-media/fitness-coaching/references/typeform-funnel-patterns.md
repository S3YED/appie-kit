# Typeform Funnel Patterns for Fitness Coaching

Concise reference for the Typeform patterns used in Ibrahim's coaching funnels. These are specific to his qualification logic, country gates, and question ordering preferences.

## Funnel Types

### 1. High-Ticket Qualification (Creed Ignite — £997)
- 12 questions + Calendly booking
- Investment question tiers: exploring / £1-1.5K / £1.5-2K / £3K+
- Country DQ: Asia/Africa/South America → "We'll reach out" screen
- Profession DQ: "Student, unemployed, inbetween jobs"
- Ends with Calendly redirect

### 2. Low-Ticket Entry (Health in Motion — $99/mo)
- No investment question (fixed price)
- No Calendly booking
- "Does this look right?" Yes/No gate:
  - Yes → "Why now?" → contact → payment
  - No → "What's missing?" → contact → high-ticket redirect
- Country DQ still active (but collect contact info anyway)

### 3. Giveaway/Challenge (Lead Gen)
- Emotional buy-in FIRST, contact info AFTER:
  1. Welcome (prize value + deadline)
  2. Current situation (long text)
  3. 12-week vision (long text)
  4. Why now / cost of staying same (long text)
  5. Commitment score 1-10 (opinion_scale)
  6. Contact info (name, email, phone)
  7. Instagram handle
  8. WhatsApp opt-in (yes_no)
  9. Profession
  10. Country with DQ (collect info even on DQ)
  11. "Still interested at discount?" (yes_no) — pre-qualifies for sales
- Winner selection: based on commitment score + story depth, not random draw

## API Patterns

### Two-Step Creation
```python
# Step 1: Create without logic
POST /forms {title, settings, fields}  # NO logic, NO thankyou_screens

# Step 2: Get IDs
GET /forms/{id}  # captures auto-generated field/thankyou IDs

# Step 3: Add logic
PUT /forms/{id} { ...logic, thankyou_screens }  # must include ALL fields
```

### Logic Format
```python
{
    "type": "field",
    "ref": "q_field_ref",
    "actions": [
        {
            "action": "jump",
            "details": {"to": {"type": "thankyou", "value": "default_tys"}},
            "condition": {
                "op": "is",
                "vars": [
                    {"type": "field", "value": "q_field_ref"},
                    {"type": "choice", "value": "choice_ref"}
                ]
            }
        },
        {
            "action": "jump",
            "details": {"to": {"type": "field", "value": "next_field_ref"}},
            "condition": {"op": "always", "vars": []}
        }
    ]
}
```

### Key Field Structures

**contact_info:**
```python
{
    "ref": "contact",
    "title": "Your contact details",
    "type": "contact_info",
    "properties": {
        "fields": [
            {"ref": "first_name", "title": "Name", "subfield_key": "first_name", "type": "short_text", ...},
            {"ref": "last_name", "title": "Last name", "subfield_key": "last_name", "type": "short_text", ...},
            {"ref": "phone", "title": "Phone", "subfield_key": "phone_number", "type": "phone_number", "properties": {"default_country_code": "gb"}, ...},
            {"ref": "email", "title": "Email", "subfield_key": "email", "type": "email", ...}
        ]
    }
}
```

**Country DQ logic:** Uses `op: "is"` with choice refs. Three DQ choices (asia, africa, sa) jump to thankyou. An `op: "always"` catch-all jumps to the next field.

**Profession DQ logic:** Uses `op: "equal"` with a constant value matching exactly: `"Student, unemployed, inbetween jobs"`.

### opinion_scale
```python
{
    "type": "opinion_scale",
    "properties": {"steps": 10, "start_at_one": True}
}
```
Note: `shape` property is NOT allowed in POST. Set in the UI after creation.

### yes_no Alternative
For branch logic, use `multiple_choice` with explicit refs instead of `yes_no`:
```python
{
    "type": "multiple_choice",
    "properties": {
        "choices": [
            {"ref": "choice_yes", "label": "Yes — ..."},
            {"ref": "choice_no", "label": "No — ..."}
        ]
    }
}
```
This avoids the `yes_no` choice ref problem where auto-generated refs are unknown at creation time.

### Common Errors & Fixes
| Error | Cause | Fix |
|-------|-------|-----|
| `language` NOT_ALLOWED | language at top level | Move inside `settings` |
| `validations/required` on statement | statements can't be required | Remove `validations` from statement fields |
| `UNKNOWN_THANKYOU_REFERENCE` | logic references thankyou that doesn't exist yet | Create form first, GET to find ref, then PUT with logic |
| `UNKNOWN_CHOICE_REFERENCE` | wrong choice ref in logic | Must match exactly what Typeform generated |
| `show_first_name` on contact_info | flat properties not allowed | Use nested `fields[]` array instead |
| `thankyou_screens` in settings | wrong nesting | Move to top level of form JSON |
