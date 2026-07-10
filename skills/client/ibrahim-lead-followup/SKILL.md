---
name: ibrahim-lead-followup
description: Draft personalized WhatsApp follow-up messages for Ibrahim Ramzy's leads at each funnel stage — giveaway entered, triage call booked, call completed, no-show/reactivation. Matches Ibrahim's brand voice.
version: 1.0.0
author: Ibrahim's Assistant
tags: [ibrahim, whatsapp, lead-followup, funnel, messaging]
---

# Ibrahim Lead WhatsApp Follow-up

## When to Use

Use this skill when Ibrahim asks you to send follow-ups, drafts, or outreach messages to leads in his coaching pipeline. Automatically personalized per funnel stage.

## Brand Voice Rules (non-negotiable)

1. **No em dashes** — ever. Use periods or commas instead.
2. **No metaphors or flowery language.** Short, direct sentences.
3. **Sound human, not AI slop.** No corporate filler.
4. **Must hit emotional pain/drive** — not surface level. Reference their specific situation.
5. **Structure:** `[Name], was thinking about what you said about [specific thing]. Here's one thing you can do today: [one actionable step]. Let me know how it helps.`
6. **Aspiration over shame** — never "I've let myself go." Always "unlocked potential."
7. **Use brother/sister** for gender respect. Never "guys" — use "everyone."
8. **Transformation photos prominent** if sending media.

## Funnel Stage Templates

### Stage 1: Just Entered Giveaway (Welcome)
Goal: Make them feel seen, explain next step, get them to save contact.
Template: "Brother/Sister [Name], saw your entry. I read through your answers. [Reference one specific thing they wrote]. The challenge starts [date]. First thing: [one small win they can get today]. Make sure you save my number so we stay connected."

### Stage 2: Triage Call Booked (Confirmation)
Goal: Confirm, build anticipation, reduce no-show rate.
Template: "Brother/Sister [Name], got you down for [day/time]. This call is for me to understand where you're at and what you really want. No pitch, no pressure. Just come ready to be honest about where you're stuck."

### Stage 3: Post-Triage Call (Value Follow-up)
Goal: Deliver value, build trust, move toward second call.
Template: "Brother/Sister [Name], was thinking about what you said about [specific pain point from call]. Here's one thing you can do today that changes everything: [specific actionable step based on their situation]. Let me know how it feels tomorrow."

### Stage 4: No-Show / Unresponsive (Reactivation)
Goal: Gentle re-engagement with hook, no guilt.
Template: "Brother/Sister [Name], I had a slot open for you and didn't see you there. No worries — life happens. I'm still here when you're ready. The giveaway prize is still on the table. One message and we reschedule."

### Stage 5: Second Call (Sales Progression)
Goal: Frame as progression, not sales.
Template: "Brother/Sister [Name], you've put in the work. I think you're ready to take this further. Let's book a 15 minute call to talk about what that looks like. No pressure, just options. When works for you?"

## Personalization Rules
1. Always reference something specific the lead said/did. Never generic.
- Use Cognify recall to check past interactions with this lead.
3. Dubai/UAE leads: reference "golden cage" pain point (Talabat, long hours, Botox over longevity).
4. Woman = "sister", man = "brother".
5. Never send without Ibrahim's explicit approval. ALWAYS draft first, get green light, then send.

## Sending via WhatsApp
```bash
wacli send text --to "+<number>" --message "<message>"
```

## Verification Checklist
- [ ] Personalized with specific reference?
- [ ] No em dashes?
- [ ] Short, direct sentences?
- [ ] Aspiration over shame?
- [ ] Uses brother/sister correctly?
- [ ] Got Ibrahim's approval before sending?