# Low-Ticket Group Coaching Funnel

Class-level architecture for fitness coaches running a low-ticket ($50-150/mo) group programme as a front-end to high-ticket one-on-one or premium coaching.

## Typical Offer Structure

| Component | What It Is | Delivery |
|---|---|---|
| **Core Training** | 3-5 day/week split tailored to goal (shred, build, hybrid, nomad, operator) | Everfit / App-based |
| **Nutrition** | AI-powered meal plans, recipes, supplement guidance | Custom GPT + PDF export |
| **Community** | Group chat (WhatsApp, Telegram) — daily motivation, accountability, support | VA-managed |
| **Live Call** | Monthly group coaching call — value, Q&A, community building | Zoom/Google Meet |
| **Education** | Training principles, recovery, mindset, lifestyle frameworks | Portal / Library / Vault |

## Funnel Flow

```
Ad → Typeform/Landing Page → Survey/Application → Low-Ticket Offer → Onboarding → Delivery → Upsell
```

1. **Lead capture** — Typeform or landing page collects: goals, fitness level, availability, equipment, country
2. **Survey qualifier** — Separates serious from tyre-kickers. GHL pipeline: "Survey Submitted" → "24H Before" → etc.
3. **DM/Warm outreach** — Appointment setter or VA contacts leads via WhatsApp (not IG DMs). Offer: free coaching prize (giveaway), $500 off (runner-up)
4. **Low-ticket sale** — $99/mo group programme. Cookie-cutter platform with tailored assignment (not 1:1 coaching)
5. **Onboarding** — Portal with video walkthrough, 3 pillar structure: Training / Nutrition / Education
6. **Delivery** — Everfit or similar app-based platform. VA monitors progress, manages group chat, handles escalations
7. **Upsell** — Monthly call + in-app nudges → upgrade to high-ticket premium coaching

## Key Insights

### Pricing Psychology
- $99/mo is impulse-buy territory for the ICP (career-successful professionals 25-45)
- Low enough to not need a sales call; high enough to filter freebie-seekers
- Main cost is delivery (VA time, platform fees) — needs volume to scale

### The Upsell Path
- Proven: 2 clients upgraded from $99/mo to high-ticket
- Trigger moments: client sees progress (4-8 weeks in), feels limited by group format, wants direct coach access
- Embed upsell CTA in monthly call + in-app milestone celebrations

### VA Leverage
- VA manages: group chat, programme assignment, progress monitoring, tech support
- Coach intervenes only on: escalations, programme modifications, monthly live call
- This decouples coach time from delivery — scales without burnout

### Common Pitfalls
- **No structured onboarding** → engagement cliff after week 1-2
- **Monthly call has no conversion trigger** → wasted upsell opportunity
- **Cookie-cutter feels impersonal** → need tailored assignment logic (form → programme match)
- **Over-delivery at low price** → 4 weeks tailored + AI nutrition + group + monthly call is a lot for $99. Watch margin.

## Landing Page Structure

The low-ticket landing page should follow this section order (copied from high-ticket page but reframed for low-barrier entry):

```
Hero → VSL → Timer Gate (90s) → What You Get → Pricing → Transformations → Testimonials → Community → FAQ → Typeform → Final CTA
```

### Section Details

| Section | Content |
|---------|---------|
| **Hero** | Label (brand name), subline (pain + price), headline (body + energy + confidence for $X/mo), social proof (stars + member count) |
| **VSL** | 6-minute video. Different energy from high-ticket — "entry point, no risk, start today" not "life-changing transformation" |
| **Timer Gate** | 90s locked content. sessionStorage persistence (key: `him_gate_passed` — must differ from high-ticket `creed_gate_passed` to avoid conflicts) |
| **What You Get** | 6 benefit cards in grid: Training, Nutrition, Community, Live Call, App Access, Mastery Library |
| **Pricing** | Single card: $99/month, cancel anytime. Feature list, CTA button |
| **Transformations** | Same client before/afters as high-ticket page (same result pool — the offer differs, not the proof) |
| **Testimonials** | Same video testimonials from high-ticket page |
| **Community** | 3-column feature grid (Daily Accountability, Motivation That Sticks, Direct Coach Access) |
| **FAQ** | 6 questions specific to low-ticket: what you get, beginner-friendly, schedule flexibility, nutrition personalisation, cancellation, how it differs from gym/app |
| **Typeform** | No investment question, no Calendly. Ends with contact_info |
| **Final CTA** | "Try it for a month. Cancel anytime." |

### Copy Shifts (High-Ticket → Low-Ticket)

| Element | High-Ticket | Low-Ticket |
|---------|-------------|------------|
| Offer | 90-day transformation | Monthly, ongoing |
| Price | £997+ | $99/mo |
| Commitment | Programme | Cancel anytime |
| Support | 1-on-1 coaching | Group + VA |
| Decision weight | "Life-changing investment" | "Try it, no risk" |
| FAQ tone | "We figure that out on the call" | Specific, transparent answers |

### Domain Setup (Vercel)

When deploying as a separate project (not a subpage):

```bash
# Remove existing Vercel project link
rm -rf .vercel

# Deploy as NEW project
vercel --prod --yes

# Add custom domain
vercel domain add healthinmotion.cali-creed.com
```

If the domain is managed externally (not on Vercel's DNS), the user must add a CNAME record:
```
Type: CNAME
Name: healthinmotion
Target: cname.vercel-dns.com
```

Do NOT re-use the same Vercel project — the high-ticket page and low-ticket page should be separate projects with separate domains to avoid deployment conflicts.

## Reference: "Health in Motion" (Ibrahim Ramzy)

A working example of this model:

**Offer:** "Health in Motion" — $99/month
**Pillars:** Engine Room (training), Fuel Station (nutrition GPT), Mastery Manor (education)
**Pipes:** GHL (428 leads, 155 survey submitted, 165 in 24H window)
**Setter:** Ishan (+91 78762 74614) — WhatsApp outreach
**Hook:** Giveaway (free coaching) + $500 off (2nd/3rd place)
**Migration:** Was Notion-based delivery → moved to Everfit for streamlined ops

## When to Use This Pattern

Use when:
- ICP is career-successful but time-poor (25-45, already fit, hitting plateaus)
- You have an existing lead list that never got a proper offer
- You want a scalable front-end that funds VA + platform costs
- You have a high-ticket offer this feeds into

Don't use when:
- Your ICP is beginners (they need more hands-on)
- You can't commit to monthly group delivery
- You don't have a VA to offload the daily operations