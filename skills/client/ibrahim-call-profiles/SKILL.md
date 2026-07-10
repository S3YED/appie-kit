---
name: ibrahim-call-profiles
description: Transcribe triage calls, extract lead profile (pain points, goals, objections, commitment level), and prep strategy for Ibrahim's second "next steps" call.
version: 1.0.0
author: Ibrahim's Assistant
tags: [ibrahim, calls, triage, lead-profile, sales]
---

# Ibrahim Call Profile Builder

## When to Use

Use when a triage call recording is uploaded or Ibrahim says he finished a call and shares notes. This builds a structured profile for the second call.

## Pipeline

1. Get the recording or notes
2. Transcribe (if audio) using OpenAI Whisper or similar
3. Extract structured profile
4. Store in Cognee for future recall
5. Deliver profile to Ibrahim as prep for second call

## Profile Structure

Extract these fields from every triage call:

**Lead Info:**
- Name, location, age range
- Gender (for "brother/sister" usage)
- How they found Ibrahim

**Pain Points:**
- Primary physical pain point (what's wrong with their body)
- Secondary pain point
- Emotional driver (why this matters to them deep down)
- Quote their own words here

**Current Routine:**
- Training frequency and type
- Diet/nutrition approach
- Sleep and recovery
- Biggest struggle area

**Commitment Signals:**
- Red flags (excuses, vague answers, not ready)
- Green flags (specific goals, past success, ready to act)
- Overall readiness score: Low/Medium/High

**The Angle for Call 2:**
- What specific transformation would mean most to them
- What objection to overcome
- The hook that will get them to say yes

## Second Call Strategy

The second call is framed as "next steps" — never as a sales pitch.

**Opening:** "You did the work. I saw your [specific progress/reference]. Let's talk about where you go from here."

**The Offer Frame:** Present coaching as the natural next step, not a hard sell. Use their own words from the triage call about what they want.

**Close:** "I have a spot opening on [day]. If you're ready to make this happen, I can take you on. Think about it and let me know by [timeframe]."

## Storage

After building the profile, save it to Cognify:
```bash
cd /root/cognify && source .venv/bin/activate && set -a && . ./.env && set +a
echo "$JSON_SUMMARY" | cognify --tenant ibrahim ingest -
```

## Delivery to Ibrahim

Send the profile as a structured message to Ibrahim on Telegram/WhatsApp with:
- Key insights (3 bullet points max)
- Recommended approach for Call 2
- Suggested timing for the follow-up