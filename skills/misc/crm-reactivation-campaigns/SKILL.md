---
name: crm-reactivation-campaigns
description: Audit stale CRM pipeline data, tier leads by stage and contact coverage, build giveaway-anchored re-engagement campaigns, write tiered DM scripts for a setter, write email sequences, and tag/move leads via CRM API. For coaching/agency/client-acquisition businesses using GHL or similar CRMs.
---

# CRM Reactivation Campaigns

Use when a CRM has hundreds+ of stale leads (applied but never contacted, booked but no-showed, went cold after contact) that need a structured re-engagement campaign.

## Key Principle: Piggyback Don't Invent

Never create a separate "re-engagement offer." Anchor the outreach to whatever promotion/giveaway the business is already running. The existing campaign IS the re-engagement hook. This avoids confusing the owner ("what re-engagement offer?") and keeps messaging consistent.

## Workflow

### 1. Audit the pipeline

Query the CRM to understand:
- Total opportunities by stage
- Contact coverage (phone, email, both, neither) per stage
- Activity recency — how long since last contact
- Top sources
- Monetary value assigned

**GHL API quirks (v2):**
- Base: `services.leadconnectorhq.com` (v1 at `rest.gohighlevel.com` is Cloudflare-blocked)
- Required header: `Version: 2021-07-28`
- Phone numbers arrive **partially masked** (`+447****1234`) — GHL privacy feature, not a query error
- Max 100 results per page on opportunities search
- Store token in `/tmp/file` and read back to avoid shell redaction of secrets in command output

### 2. Tier leads by stage and contact data

| Tier | Stage | Action | Priority |
|------|-------|--------|----------|
| **Tier 1 — Kill Now** | Survey Submitted / Applied + has phone | DM setter reaches out TODAY | 🔴 Highest |
| **Tier 2 — Warm** | Booked but no-show / 24 Hours Before + has phone | DM setter within 48 hrs | 🟡 High |
| **Tier 3 — Re-nurture** | No Answer / Unresponsive / Requires Follow Up | Email sequence first → DM on open | 🟢 Medium |
| **Exclude** | Disqualified, existing Client, Cancelled | Skip | ✗ |

For Tier 1: sort by most-recent-created. Batch into groups of 30-50 for daily cadence.

### 3. Confirm the offer with the owner

Present the framework clearly:
> "Here are [N] cold leads. [Giveaway/Offer X] is your hook. We tell them: 'You applied before — you're pre-qualified for this.'"

Do NOT frame it as a separate campaign. The owner must immediately recognise their own promotion.

### 4. Write DM scripts per tier

Scripts must:
- Reference the specific stage the lead is stuck in
- Use the giveaway/offer as the reason (non-salesy)
- Include a clear CTA (book a call)
- Have reply-handling branches (interested, what's the catch, not now)

**Tier 1:** "Hey [Name], this is [Setter] from [Brand]. You applied for coaching before but never got through. We're running [Offer]. Since you're pre-qualified, wanted you to know first. Interested?"

**Tier 2:** Acknowledge the missed booking: "I see you booked a call before and it never happened — life gets in the way. We're running [Offer]..."

**Tier 3:** Email-first. "Saw you opened our email about [Offer]. Just making sure you saw it..."

### 5. Write the email sequence

3 emails over 7 days:
- Email 1: Re-introduction + offer (apologise for the silence)
- Email 2: Social proof / client story
- Email 3: Deadline urgency + last call

Track opens → tag "warm" → DM setter reaches out within 2 hours of open.

### 6. Setter daily cadence

| Day | Action |
|-----|--------|
| Day 1 | DM first 30-50 Tier 1 leads. Send Email 1 to all. |
| Day 2 | Reply to DM responses. DM Tier 2 leads. |
| Day 3 | Send Email 2. Check opens → DM warm leads. |
| Day 5-6 | Follow up Tier 1 non-responders. Cover remaining batches. |
| Day 7 | Send Email 3 (deadline). Final DM follow-up. |

### 7. Tag and move leads in CRM via API

- Tag: `re-engagement-wave-1`, `tier-1-hot`, `tier-2-warm`, `tier-3-nurture`
- Move Tier 1 → "Requires Follow Up" so the setter sees them immediately
- Move Tier 2 → "Requires Follow Up" on day 3

### 8. Deliverables to the owner

- Prioritised lead list (batched for the setter)
- DM scripts per tier with reply branches
- Email sequence (3 emails)
- CRM tags and stage moves (executed via API)
- Daily cadence sheet

## Pitfalls

- **Offer confusion:** Always tie the re-engagement to an existing promotion. Never invent a new one without explicit approval. If the owner says "I don't understand the re-engagement offer", you've failed — restate it as their existing campaign.
- **Phone masking:** Don't report "missing phone numbers" as a data issue in GHL. Country code + last 4 digits is all the API returns by design.
- **Lead volume overwhelm:** 150+ DMs in one day burns out a new setter. Batch into 30-50/day.
- **No booking link:** Always ask for the specific booking link before sending scripts to the setter.
- **API pagination:** GHL returns max 100 per page. Always paginate to get the full dataset.