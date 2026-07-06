# VSL + Timer Gate Funnel Architecture

For fitness coaches who want a **commitment-filtered** landing page that pre-qualifies leads before they reach the booking CTA. Uses a 2-min VSL with a 90-second timer gate that unlocks the rest of the page. Created for Ibrahim Ramzy / The Creed Code.

## Core Logic

Watching 90 seconds of a VSL is a stronger signal of intent than clicking an ad. Someone who watches the full hook has mentally committed before booking. This drives higher show rates and warmer calls.

## Page Structure (Top to Bottom)

- **HERO:** Headline matching ad hook + subheadline (1-line value prop)
- **VSL EMBED (2 min):** Click-to-play or auto-play. Overlay covers content below.
- **TIMER GATE:** 90s countdown. Content below is BLOCKED by a translucent overlay until timer hits 0. Timer pauses if video pauses. NOT an anti-bot measure — it's a commitment filter. Anyone who waits 90s has shown intent.
- **FREE TRAINING (Short):** Valuable content given freely before any ask — 3-5 min video or written guide. Creates reciprocity. Do NOT gate this behind email capture — breaks the reciprocity loop.
- **TESTIMONIALS:** Grid of video clips (30-60s) + screenshot carousel. Real names/jobs/results. Mix of video testimonials already shot + screenshot proof.
- **OBJECTION-BUSTER VIDEOS:** 1-2 min each, created by the coach. Cover the top objections from the ICP doc. Common ones: consistency, time, tried-before-failed, cost/value. Arrange in order of objection frequency.
- **FINAL CTA:** "Book Your Free Strategy Call" — one button, one destination. No secondary CTA, no social links, no email signup below it.

## The Timer Gate

- VSL starts → translucent overlay covers page below → 90s countdown → overlay fades → content unlocked
- VSL can keep playing past 90s; gate only requires 90 minimum watch
- Timer pauses if video pauses (JS event tracking on video player)
- NOT an anti-bot measure — users can DevTools-remove it. It's an honesty filter.

**Why 90s:** Covers Hook + Dream Outcome (0-20s) + Us vs Them/Proof (20-50s) + Mechanism/Guarantee (50-80s) + Bridge start (80-90s). By 90s they've absorbed the full promise.

## CTA Placement

Right below objection-busting videos. No secondary CTA, no social links, no email signup. One path: book the call. Links to Calendly/GoHighLevel booking.

## When to Use vs Standard Landing Page

| Scenario | Standard LP | VSL+Timer Gate |
|---|---|---|
| Cold traffic from ads | ✅ Best | ❌ Too much friction |
| Retargeting (know you) | ❌ | ✅ Best |
| Warm audience (followers) | ❌ | ✅ Best |
| Client wants quality over volume | ❌ | ✅ Timer filters |
| Client wants maximum volume | ✅ | ❌ Gate reduces volume |

## GHL Integration

- VSL: YouTube unlisted or Vimeo
- Timer gate: JavaScript on page (standalone, no GHL needed)
- CTA → GHL calendar booking link
- Lead capture: booking creates GHL contact + triggers email workflow
- Tracking: Meta Pixel for video progress (25%/50%/75%/100%) + timer complete + CTA click + booking

## Pitfalls

- Mobile-first: timer gate must work on touch events, not hover. Test on real phone.
- Autoplay restrictions: many mobile browsers block autoplay with sound. Design for muted autoplay + tap-to-unmute.
- VSL must be under 2:30. Longer loses them before CTA.
- Don't gate the training behind email — breaks the reciprocity loop.
- One CTA only. Multiple CTAs create choice paralysis.
