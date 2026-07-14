# Typeform response extraction for Cognify KG

## Problem
Typeform contact blocks store sub-fields (name, email, phone) as nested field objects
with UUID refs, not as top-level titled fields. A flat form definition parse misses them.

## Solution
Recursively traverse `properties.fields` in the form definition to build a complete
ref→label map:

```python
ref_map = {}
def extract_fields(fields):
    for field in fields:
        ref = field.get('ref', '')
        title = field.get('title', '')
        if ref and title:
            ref_map[ref] = title
        props = field.get('properties', {})
        if 'fields' in props:
            extract_fields(props['fields'])

extract_fields(form['fields'])
```

## Example
Contact block `2332382b-5762-409e-be79-16220636b064` contains:
- `33dfb589-3a48-443a-93b7-b1bacf5beb7e` → "First name"
- `99021b03-5007-4e7a-98d5-6a2a99a123cf` → "Last name"
- `fdc60924-fd8b-4431-84a9-0430ef80039d` → "Phone number"
- `8b3b086e-3df7-4320-812a-ce878af4f63b` → "Email"

## Active forms
- `N4LbJCHT` — The Creed Challenge (giveaway intake, 65+ responses)
- API key at `/root/.hermes/.env` (Typeform token stored separately)