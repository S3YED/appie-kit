# 1-Week Minimum Viable Funnel Build

For fitness coaches who want to run paid ads this month. Builds a working funnel from scratch in 5-7 days.

## Core Principle: Work Backwards

Start at the end goal (sale) and work backwards to the ad creative. Every element exists to move the prospect one step closer.

```
AD CLICK → LANDING PAGE → BOOK CALL → CLOSE ON OFFER
```

## Default Offer to Lead With

**Creed Ignite (£997-£1,497)** — cash cow, ads-friendly, group coaching cohort.

Why: Lowest price point means lowest ad friction. Cold traffic won't buy £3.5k-£5k offers from an ad. The call converts them into the higher tiers if they're a fit.

## Day-by-Day Build

### Day 1-2: Shoot Ad Creatives

**3 video angles (15-30s, vertical 9:16):**

| Angle | Hook Example | When to Use |
|-------|-------------|-------------|
| Struggle | "You've tried everything and still can't stay consistent" | Broad cold audience |
| Aspirational | "What if 90 days could change your entire relationship with your body?" | Lookalike of past clients |
| Credibility | "I've coached 300+ men. Here's the #1 thing they all get wrong." | Retargeting + skeptics |

**Production rules:**
- Phone camera is fine. Good lighting + clear audio are non-negotiable.
- Text overlays for the first 3 seconds (silent autoplay on Facebook/IG)
- CTA in last 5 seconds: "Book your free call" + on-screen button text
- No branding in the first 10 seconds (Meta flags early branding as low quality)

### Day 2-3: Landing Page (Critical Path)

**Structure (top to bottom):**

1. **Hero section**
   - Headline: matches the ad hook EXACTLY. Prospect should feel like the ad brought them to the right place.
   - Subheadline: 1-2 sentences of the specific transformation (not features)
   - CTA button: "Book Your Free Strategy Call" — Royal Blue (#004CC8)
   - Background image/video: you coaching or a transformation shot

2. **Quick wins / proof of concept**
   - 3 bullet points of what they'll get in the first 2 weeks
   - "Not another generic plan" — differentiation from free info online

3. **Social proof (CRITICAL for skeptical ICP)**
   - 3-5 before/after transformations with name + job + location + timeframe
   - Star rating or testimonial quote
   - Avoid: fake-sounding testimonials. Real results from real people.

4. **How it works**
   - 3 simple steps. Keep it easy to scan.
   - Step 1: Book your call
   - Step 2: We build your plan
   - Step 3: We execute together

5. **Objection killers**
   - "What if I can't stay consistent?" → Answer with the accountability system
   - "What if I've tried before?" → Answer with the REP method
   - "What if I don't have time?" → Answer with efficiency

6. **Final CTA**
   - Same button as the hero. No new choices.

**Technical specs:**
- Mobile-first. >70% of ad clicks happen on mobile.
- Load time <3s. Compress images, minimal JS.
- Meta Pixel installed: events for ViewContent, Lead, Schedule
- UTM params on all links

### Day 3: Booking + Tracking

**Booking system:** Calendly or GoHighLevel
- One link. No steps before booking (name + email + phone is enough)
- Auto-confirmation email with calendar link
- Reminder 24h and 1h before

**Tracking setup:**
- Meta Pixel (pixel_id from Facebook Business Manager)
- Events: PageView, ViewContent, Lead (when they book), Schedule
- UTM tags on ad → landing page link: `utm_source=facebook&utm_medium=paid&utm_campaign=ignite_launch`

### Day 4: Email Follow-up

Sequence for booked calls (auto-triggered by booking system):

| # | Trigger | Subject | Content |
|---|---------|---------|---------|
| 1 | Immediate | "See you on [date] — here's what to expect" | Thank them, prep questions, what the call covers |
| 2 | +48h no-show | "Still interested? Here's what [client] achieved" | One strong testimonial + result. One more chance to rebook. |
| 3 | +96h no-show | "Your spot won't be here forever" | Scarcity. Last chance. If they don't respond by now, move on. |

### Day 5: Launch

**Budget:**
- Start: £20-30/day per creative (3 creatives = £60-90/day total)
- This is a TEST budget. You're looking for signal, not sales yet.

**Kill/Scale rules:**
- Kill if CTR < 0.8% by day 3 (ad not resonating)
- Kill if CPA > offer price / 3 (e.g. £997 ÷ 3 = £332 max CPA)
- Scale winner: double budget every 48h while CPA stays healthy
- Max budget: whatever you can handle on calls (each ~10 leads = 1 booked call)

## Client-Specific: Ibrahim Ramzy / The Creed Code

**Brand:**
- Background: Dark Navy (#072A42)
- Primary: Silver (#B4B4BC)
- Accent: Navy (#0F2D55)
- CTAs: Royal Blue (#004CC8)
- No neon greens. Client rejected off-brand colours previously.

**Offer to lead with:** Creed Ignite (£997 group, 3 months)

**Call to actions:** "Book Your Free Strategy Call" — direct booking. No lead magnet step.

**Ad creative style:** You talking to camera. No actors. Your credibility sells.

## Pitfalls

- **Building the landing page before the ad is approved.** The headline MUST match the ad hook. If the ad creative gets rejected or changed, the page needs to change too. Do them in parallel or ad first.
- **Skipping the booking system.** A "Book Call" CTA converts better than "Buy Now" on cold traffic. The call is where the money is made.
- **Too many CTAs.** One CTA per page. Confusion kills conversion.
- **Not testing the full flow yourself.** Click your own ad → land on page → book a call → check the email. Do it start to finish before spending a penny.
- **No retargeting.** Set up a retargeting audience (people who landed but didn't book) and show them a different ad: social proof or scarcity angle. This is where most sales come from.