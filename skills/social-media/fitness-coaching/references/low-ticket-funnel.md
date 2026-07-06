# Low-Ticket Funnel: Landing Page & Typeform Workflow

For personal trainers and fitness coaches building a $99/mo offer alongside a high-ticket £500+ programme.

## When to qualify vs when not to

| Price Point | Qualification | Rationale |
|-------------|---------------|-----------|
| High-ticket (£500+) | Country, profession, budget, commitment | Protects coach time, justifies price |
| Low-ticket ($99/mo) | **None** beyond contact info | Barrier too low to disqualify; everyone should get through |
| Mid-tier | Goal + training level (route to variant) | Light routing only |

## Low-ticket Typeform (proven pattern)

1. **Gate question:** "Does this look like what you're looking for?" (multiple_choice with refs `choice_yes`, `choice_no`)
2. **If Yes:** "Why now?" (short text — commitment check)
3. **If No:** "What's missing?" (short text — captures objections, redirects to high-ticket page)
4. **Contact info:** name, email, phone (always required — need to deliver the programme)

Both paths collect contact info. The "No" path then redirects to the high-ticket landing page.

## Typeform API: two-step logic pattern

Typeform forms with logic jumps MUST be created in two steps:

```python
# Step 1: POST form without logic
POST /forms { fields: [...] }

# Step 2: GET the form to discover thankyou_screen refs
GET /forms/{id}
# thankyou_screens[0].ref is typically "default_tys"

# Step 3: PUT the full form with logic referencing thankyou refs
PUT /forms/{id} { fields: [...], logic: [...] }
```

Attempting to include logic in the initial POST fails with `UNKNOWN_THANKYOU_REFERENCE` because thankyou screens don't exist at creation time.

## yes_no field in Typeform API

Typeform's `yes_no` field does NOT export its choice refs via the API. Logic jumps using `"type": "choice"` with values "Yes"/"No" fail with `UNKNOWN_CHOICE_REFERENCE`.

**Fix:** Use `multiple_choice` with explicit choices:

```json
{
  "ref": "q1_look_right",
  "title": "Does this look like what you're looking for?",
  "type": "multiple_choice",
  "properties": {
    "choices": [
      {"ref": "choice_yes", "label": "Yes — this is exactly what I need"},
      {"ref": "choice_no", "label": "No — I need something more"}
    ]
  }
}
```

Then reference them in logic as `{"type": "choice", "value": "choice_yes"}`.

## Copy tone shifts

| Element | High-ticket (£500+) | Low-ticket ($99/mo) |
|---------|-------------------|-------------------|
| Hero headline | "Build the best body of your life in 90 days" | "Get the body, energy, and confidence you deserve — for $99/month" |
| VSL length | 2 minutes | Up to 6 minutes |
| Promise | Transformation | Entry point, start today |
| Commitment | "Reserve my spot" | "Try it for a month, cancel anytime" |
| FAQ tone | "What makes this different?" | "Is this for me if I'm a beginner?" |
| Social proof | "Real transformations" | "Join 50+ members" |

## Landing page duplication

When duplicating an existing landing page for a new offer:

1. `cp -r /root/project /root/project-copy` (full copy, don't rebuild)
2. Rewrite: hero headline, brand name, price, offer description, FAQ, typeform ID
3. Keep: testimonials, layout, timer gate, visual assets
4. `rm -rf .vercel/` in the copy (prevents deploying to the old project)
5. Deploy with `npx vercel --prod --yes --token $TOKEN` (creates new Vercel project)
6. Verify: `curl -s -o /dev/null -w "%{http_code}" https://project.vercel.app`