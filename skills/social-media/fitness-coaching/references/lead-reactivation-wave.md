# Cold Lead Reactivation — Giveaway Re-Engagement Wave

Use when a coaching business has hundreds of stale leads in GHL that need a structured re-engagement campaign. The giveaway gives a non-salesy reason to reach out.

## The Core Insight

Most leads go cold because nobody follows up, not because they weren't interested. A pipeline audit almost always reveals 3x-5x more leads than the founder thinks exist.

**The hook:** A giveaway (free coaching prize) piggybacks on existing interest — "You applied before. We're running a Founders Giveaway. Since you're pre-qualified, wanted you to know first."

## Pipeline Audit

### GHL v2 API Audit

Base URL: `https://services.leadconnectorhq.com` (NOT `rest.gohighlevel.com/v1/`)

Required headers:
```
Authorization: Bearer <pit-token>
Version: 2021-07-28
Content-Type: application/json
User-Agent: Mozilla/5.0
```

Key queries:
1. List pipelines: `GET /opportunities/pipelines/?location_id={locationId}`
2. Search opportunities: `POST /opportunities/search/` with body `{"pipeline_id":"...","location_id":"..."}`
3. Get contact: `GET /contacts/{contactId}`

**Phone masking:** GHL partially masks phone numbers in API responses (e.g., `+447****1234`). Country code + last 4 digits are visible. This is a privacy feature, not an API error.

**Pipeline stage mapping:** Build a stage-ID-to-name map by cross-referencing the opportunity's `pipelineStageId` with the contact's stage name (extracted from the opportunity's source or by matching against the pipeline's stage list).

### Tiering Logic

| Stage | Tier | Action |
|-------|------|--------|
| Survey Submitted | **Tier 1 (Hot)** | DM within 24 hours. These people qualified themselves and never heard back. |
| 24 Hours Before | **Tier 2 (Warm)** | DM within 48 hours. They booked a call that never happened. |
| No Answer 1/2, Unresponsive, Requires Follow Up | **Tier 3 (Re-nurture)** | Email sequence first. DM only if they engage with email. |
| Client | **Skip** | Already paying. Leave alone. |
| Disqualified | **Skip** | Already ruled out. |

## DM Scripts

### Lead Preferences

**Ibrahim prefers:** IG DMs as the founder account (not WhatsApp from a setter's number). The founder's name in the inbox lands harder. The DM setter monitors the founder's IG inbox and responds using the scripts.

### Tier 1 — Survey Submitted

**Primary script:**
> Hey [Name], this is Ishan from The Creed with Ibrahim Ramzy.
>
> You applied for coaching with us but never got through to the next step. We're running a Founders Giveaway: free coaching for 1st place, $500 off for 2nd & 3rd.
>
> Since you're already pre-qualified, wanted you to know first. You interested in entering?

**If they respond:**
> Simple. Two steps:
> 1. Book a quick call with Ibrahim to confirm fit
> 2. You're automatically in the draw
>
> No purchase needed to enter or win. Worst case? You get $500 off if you don't win the free spot.
>
> Want the link?

**If they say "what's the catch":**
> No catch. Ibrahim wants to find the most committed person for this intake. You're pre-qualified from your application. One 15-min call to confirm fit and you're entered.

**If "not interested":**
> No worries. If things change, offer's open for the next [X] days.

### Tier 2 — 24 Hours Before

> Hey [Name], Ishan here from The Creed.
>
> I see you booked a call with Ibrahim before but it never happened — life gets in the way, I get it.
>
> We're doing a Founders Giveaway and since you were already in the pipeline, wanted to flag it. Free coaching for 1 winner, $500 off for 2nd & 3rd.
>
> Want me to send you a link to rebook? If you're a fit, you're automatically entered.

### Tier 3 — No Answer / Unresponsive

Email-first approach. DM script (triggered by email open):
> Hey [Name], saw you opened our email about the Founders Giveaway. You're already pre-qualified from when you applied. All you need is a 15-min call to confirm fit, and you're in the draw.
>
> Want the link?

## Email Sequence (3 emails)

**From:** Founder's work email
**Audience:** All 460+ contacts with emails

### Email 1 — Re-introduction (Day 1)
Subject: We dropped the ball. Making it right.

Opens with apology for not following up. Announces the giveaway: free coaching for 1st, $500 off for 2nd & 3rd. CTA to book a call. "No purchase needed to enter or win."

### Email 2 — Social Proof (Day 4)
Subject: She was you 12 weeks ago

Client story (e.g., Pangina -20kg). "She didn't have more time. She had a system." Remind them the giveaway is still open. Urgency: "If you don't book by [deadline], your pre-qualified spot goes to someone else."

### Email 3 — Deadline Close (Day 7)
Subject: Final reminder — giveaway closes tomorrow

"Closing the Founders Giveaway tomorrow." Clear CTA to book the call. "If you've been thinking about this, book the call. 15 minutes. That's all."

## Lead List Review Process

When the founder wants to exclude certain contacts:

1. Export the full pipeline leads list (sorted: Survey Submitted first, then 24 Hours Before, then rest)
2. Founder reviews and flags names to exclude
3. **Fuzzy matching is critical** — names in GHL are often entered by the lead themselves and may be:
   - Misspelled (e.g., "Basirah" vs "Basira", "Ashraf Sadek" vs "Ashraf Sadeq")
   - Different ordering (e.g., "Nisreen Lloyd" listed as two separate names)
   - Different first names with same surname
   - Arabic characters
4. Search the full pipeline for partial name matches and email matches
5. Present close matches to the founder for confirmation
6. Remove confirmed exclusions from the list
7. Tag excluded contacts in GHL as "excluded"

## DM Setter Cadence

| Day | Action |
|-----|--------|
| Day 1 | DM Tier 1 leads (30-40/day batch). Send Email 1 to all. |
| Day 2 | Follow up on replies. DM Tier 2 leads. |
| Day 3 | Send Email 2. Check for email opens → hot DM follow-up within 2 hours. |
| Day 5 | DM follow-up to Tier 1 non-responders. |
| Day 7 | Send Email 3. Final DM push. |

**Goal:** 30-40 DMs per day from the setter. Respond to all replies within 2 hours.

## GHL Tags

Use the API to tag opportunities and move stages:
- `re-engagement-wave-1` — everyone in the wave
- `tier-1-hot` — Survey Submitted priority
- `tier-2-warm` — 24 Hours Before
- `tier-3-cold` — No Answer / Unresponsive
- `excluded` — founder opted out
- `warm-email-open` — opened an email (triggers DM follow-up)
- `hot-click` — clicked the booking link (triggers priority DM)
