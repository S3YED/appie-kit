---
name: brevo-campaign
description: Build and execute segmented email campaigns via Brevo API. Use when creating email strategies, managing Brevo contact lists, importing segmented contacts, extracting branding from live sites for email templates, or running multi-list outreach campaigns. Covers Brevo API (lists, contacts, import), list segmentation strategy, per-segment email copywriting in brand voice, and HTML email styling.
---

# Brevo Campaign

End-to-end Brevo email campaign pipeline: audit existing data, categorize contacts into clean segments, extract live-site branding, write segment-specific email sequences, import into Brevo lists.

## When to Activate

- User wants to create an email campaign from their existing Brevo contacts
- User asks to "clean up Brevo lists" or "categorize leads"
- User wants email copy matched to a specific product/website
- User asks to import contacts into Brevo
- User says "email campaign", "newsletter strategy", "Brevo lijsten"

## Trigger phrases

- "verzamel leads en maak brevo lijsten"
- "email strategie / campagne"
- "analyseer leads in brevo"
- "maak strakke categorieën"

---

## Pipeline

```
1. AUDIT        → Fetch ALL Brevo contacts + lists via API
2. COLLECT      → Gather external sources (CSV, Notion, Google, etc.)
3. CATEGORIZE   → Smart segmentation into clean tiers (3-6 lists max)
4. BRAND        → Extract exact design system from live website
5. WRITE        → Segment-specific email sequences in brand voice
6. REVIEW       → Present everything to user BEFORE any sends
7. IMPORT       → Create lists + import contacts via Brevo API
8. SEND         → Only after explicit user approval
```

---

## Stage 1: Brevo API Audit

```python
# Fetch all contacts (paginated)
GET /v3/contacts?limit=500&offset={offset}&sort=desc

# Fetch all lists
GET /v3/contacts/lists?limit=50
```

Key data points per contact:
- email, listIds, attributes (FIRSTNAME, TAG, COMPANY)
- createdAt date
- Email domain (gmail vs business)

Pitfall: Brevo API returns max 500 per page. Loop until empty array.

---

## Stage 2: External Sources

Check for contact data outside Brevo:
- CSV client databases (most common)
- Notion CRM (API or filesystem sync at `~/clawd/tools/fleet-memory/stage-knowledge/notion/`)
- Google Contacts (via gog CLI — may need auth)
- WhatsApp contacts (via wacli — may need auth)
- Google Sheets

Cross-reference by email to avoid duplicates.

---

## Stage 3: Smart Categorization

Rule: **6 lists max.** The current default chaos (18+ overlapping lists) is what we're fixing.

### Tier structure

| Tier | List | Who |
|---|---|---|
| 🔥 | Clients | Paying customers from CSV/CRM |
| 🟢 | Buyers | Purchased a product/training |
| 🟡 | Warm Leads | Showed interest, waitlist, engaged |
| 🔵 | Cold Leads | Bulk contacts, non-buyers, unknown |
| ⚪ | Newsletter | Value letter, ads subs |
| 🗄️ | Archive | Lost, no-show, bounced |

### Dedup rule

Each contact goes into exactly **one primary** list (highest tier they qualify for). Plus one "All Contacts" master list.

### Overlap detection

Count contacts in multiple lists — this reveals the cleanup needed:
```python
from collections import Counter
overlap = Counter()
if len(lids) > 1:
    key = '+'.join(sorted(str(l) for l in lids))
    overlap[key] += 1
```

---

## Stage 4: Brand Extraction

**Reference:** `references/clark-branding.md` — complete Clark (getclark.app) design system: exact CSS vars, typography, shadows, voice.
**Reference:** `references/svg-icon-email-template.md` — SVG icon email pattern: inline icons, feature cards, color assignments, email client compatibility.

### Standard extraction process

Extract the EXACT design system from the product's live website.

### Via browser console (preferred)

```javascript
// Get all CSS custom properties
getComputedStyle(document.documentElement)

// Key vars to extract:
// --primary, --ink, --ink-2, --ink-3, --canvas, --container
// --surface, --line, --font, --display
// --shadow, --shadow-lg, --r (border radius), --s1-s7 (spacing)
```

Also capture with `browser_vision` for visual confirmation: colors, typography, button styles, hero layout.

### Via Figma API

If Figma token is available:
```python
GET https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}
Headers: X-Figma-Token: {token}
```

Pitfall: Figma tokens expire. Test with `GET /v1/me` first. Official Figma MCP server (`https://mcp.figma.com/mcp`) requires OAuth, not PAT.

### What to extract

- Colors: primary, ink, canvas, surface, line, glass, success, danger
- Typography: font families (headings + body), sizes, weights
- Spacing scale
- Border radius scale
- Shadows
- Button styles (primary + secondary)
- Tone and voice from site copy

---

## Stage 5: Email Sequences

### Per-segment cadence

| Segment | Emails | Timing | Tone |
|---|---|---|---|
| Clients | 3 | days 0, 4, 8 | Personal — "you know me from [project]" |
| Buyers | 3 | days 0, 4, 8 | "You bought X, now here's the next level" |
| Warm | 3 | days 0, 5, 9 | "You were on the list, now it's live" |
| Cold | 3 | days 0, 5, 9 | Introduction → social proof → urgency |
| Newsletter | 2 | days 0, 7 | Personal founder story |
| Archive | 1 | day 0 | One-shot announcement |

### Email structure

Each email:
1. **Personalized greeting** — use [NAAM] from Brevo attributes
2. **Context hook** — reference their specific experience with your brand
3. **The story** — what you built and why (connect their experience to the new thing)
4. **The offer** — price, scarcity, what they get
5. **CTA** — branded button/link, always to the product URL
6. **Social proof** — "this site? built by [product]. this email? also [product]."

### Copy rules

- Match the extracted brand voice exactly
- No em dashes (—). Period, comma, colon, or hyphen instead
- No "Excited to share", "I'd love to", "Great question"
- Direct, declarative sentences
- Claims backed by numbers (15 deployed, 61K items, etc.)
- Uppercase section labels match brand convention
- CTA: "[CLAIM JE SEAT →]" or "[BEKIJK [PRODUCT] →]"

---

## Stage 6: Review Gate

**CRITICAL: Never send without explicit approval.**

Present to user:
1. List structure with counts
2. Sample emails per segment
3. Total campaign reach
4. "Akkoord?" before any import or send

User may say "akkoord op lijsten maar nog niet versturen" — lists can be created but contacts not imported until both steps are approved.

---

## Stage 7: Brevo Import

### Create lists
```python
POST /v3/contacts/lists
Body: {"name": "🔥 Clients", "folderId": 8}
```

### Import contacts
```python
POST /v3/contacts/import
Body: {
  "listIds": [list_id],
  "updateExistingContacts": True,
  "jsonBody": [{"email": "...", "attributes": {"FIRSTNAME": "..."}}]
}
```

Pitfall: Import endpoint is async — returns `createdCount`/`updatedCount`/`errorCount`. Verify after import.

---

## Stage 8: Send

Only after explicit approval. Brevo supports transactional + campaign sends. For campaign sends, create a campaign via Brevo dashboard or API.

### Send pattern (transactional, Python)

```bash
source ~/.weblyfe-secrets/.env && python3 << 'PYEOF'
import os, requests, json
key = os.environ['BREVO_API_KEY']  # NEVER interpolate directly
html = open('/path/to/email.html').read()

resp = requests.post(
    'https://api.brevo.com/v3/smtp/email',
    headers={'api-key': key, 'Content-Type': 'application/json'},
    json={
        'sender': {'name': 'Clark', 'email': 'seyed@weblyfe.nl'},
        'to': [{'email': email, 'name': name}],
        'subject': 'Subject line',
        'htmlContent': html
    }
)
# Status 201 = sent. 401 = key issue.
PYEOF
```

### Batch send to multiple recipients

Loop over the recipients list inside the same `<< 'PYEOF'` block, calling `requests.post` for each. Brevo's transactional endpoint sends one email per call — no bulk endpoint. Each call returns its own messageId.

### 8. Import
- **Client consolidation hierarchy:** When gathering a client list, cross-reference:
    1. **Stripe** (charges) for paying status and billing names.
    2. **Orgo/Mission Control** for provisioned agent status (Appie-6, Appie-7, etc.).
    3. **WhatsApp (wacli)** for missing phone numbers and direct conversational JIDs.
    4. **Notion** (Website Leads) for form-entry attributes (WhatsApp number, qualification answers).
- **Import rule:** Do not import partial profiles. Gather name + email + phone (WHATSAPP attribute) before batching into Brevo lists.

---

## Pitfalls

1. **Brevo Key format:** API keys are `xkeysib-` prefixed. Redactor may mask them as `***`, so use the `source ~/.weblyfe-secrets/.env && curl ... -H "api-key: $BREVO_API_KEY"` pattern in Python or shell to avoid corruption.
2. **Contact search by name:** `wacli chats list --query "Name"` is better for finding numbers than searching message history.
3. **Brevo list Subscriber count:** Subscriber counts in the API can lag or show 0 if contacts haven't been assigned to the list ID specifically.

1. **Figma token expires silently** — returns 403. Test `/v1/me` first. Ask user for new token if needed.
2. **Brevo lists are chaotic by default** — most accounts have 15-20 overlapping lists. The audit step reveals this. Don't add to the chaos — create clean new lists and migrate.
3. **Contacts in 5+ lists** — this is the norm, not an anomaly. Dedup is the core value of this workflow.
4. **User wants review before action** — always gate on approval. "Akkoord op lijsten maar nog niet sturen" is a valid state.
5. **Google Contacts / WhatsApp may be unreachable** — auth issues are common. Don't block the campaign on these. Note the gap and proceed.
6. **API key in shell heredocs** — `source ~/.weblyfe-secrets/.env && python3 << 'PYEOF'` sets the env but the single-quoted `'PYEOF'` delimiter blocks shell variable expansion. `$BREVO_API_KEY` inside the heredoc will NOT be interpolated. Even when it IS interpolated (no quotes around PYEOF), the key can produce a silent 401 "Key not found" from Brevo. Always use `os.environ['BREVO_API_KEY']` inside Python: `key = os.environ['BREVO_API_KEY']`. Never write the raw key into the script string.
7. **@wa.tmp emails are dead** — contacts imported from WhatsApp via wacli get `@wa.tmp` placeholder emails. These cannot receive email. Always cross-reference Stripe, Notion, or Google Contacts for real email addresses before sending. Never send to a @wa.tmp address.
8. **SVG icons render poorly in email** — inline SVGs fail or render inconsistently across email clients (Outlook especially). The roadmap email V3 showed this: icons appeared broken for Gmail users. Fix: either (a) generate real images via Higgsfield/FAL and use `<img>` tags, or (b) use pure CSS geometric visuals (gradients, borders, shadows) that degrade gracefully. Do not ship production emails with inline SVG as the only visual element.

---

## Verification

- Lists created and verified via `GET /v3/contacts/lists`
- Import confirmed with created/updated counts
- Strategy document saved as artifact (in project dir)
- Branding extracted and documented
- User approved before any sends
