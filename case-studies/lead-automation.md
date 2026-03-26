# Case Study: Lead Capture Automation

## The Problem

Every time someone filled out a waitlist form on weblyfe.ai, someone had to:
1. Check the form submission (email notification)
2. Copy the data into Airtable CRM
3. Add them to the Brevo email list
4. Send a confirmation email
5. Tag them for follow-up sequences

**Time per lead:** ~3 minutes manual work
**At 10 leads/day:** 30 minutes of pure data entry

## The Solution

One API route (`/api/waitlist`) that does everything in < 2 seconds:

```
User fills form on weblyfe.ai/openclaw
  → Airtable: Lead created (name, email, phone, status, heat, source)
  → Brevo: Added to waitlist list (#18)
  → Brevo: Confirmation email sent (template #21)
  → User sees: "You're on the list! ✅"
```

### The Stack

| Component | Service | Cost |
|-----------|---------|------|
| Form frontend | Next.js on Vercel | Free |
| CRM | Airtable (free tier) | $0 |
| Email list | Brevo (free: 300/day) | $0 |
| Confirmation email | Brevo transactional | $0 |
| Hosting | Vercel (hobby) | $0 |

**Total cost: $0/month** for unlimited lead capture.

### What Appie Does

Appie monitors the system and handles edge cases:
- **Duplicate detection:** Checks if lead already exists before creating
- **Error recovery:** If Brevo fails, lead still saves to Airtable (non-blocking)
- **Template management:** Appie can update email templates via API
- **DNS management:** Set up email authentication (SPF, DKIM) via Namecheap API
- **Analytics:** Can query Airtable for lead counts, conversion rates

### Key Technical Decisions

1. **All API calls are non-blocking.** If Brevo is down, the lead still saves to Airtable. The user still sees success.
2. **Vercel env vars must be `plain` type.** We learned the hard way that `encrypted` type corrupts API tokens (Airtable keys, Brevo keys).
3. **16px font minimum on all inputs.** Prevents iOS Safari from zooming in on focus.
4. **44px minimum touch targets.** Mobile users shouldn't have to precision-tap.

### The Confirmation Email

Professional, on-brand, dark-mode compatible:
- Weblyfe logo header
- Personalized greeting (uses first name)
- 3-step "what happens next" section
- CTA button linking back to the product page
- Table-based layout (works in Outlook, Gmail, Apple Mail)
- SPF + DKIM authenticated (no spam folder)

### Results

| Metric | Before | After |
|--------|--------|-------|
| Lead capture time | 3 min manual | < 2 seconds |
| Missed leads | ~15% (forgot to check) | 0% |
| Confirmation email | Manual, often forgot | Instant, every time |
| Data accuracy | Typos from copy-paste | Clean, validated |
| Cost | Staff time | $0 |
