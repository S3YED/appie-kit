---
name: ad-creative-new-backgrounds
description: Generate 5 new Higgsfield (Nano Banana 2) prompts for a winning ad that keep the exact same text and layout, only refreshing the background/scene. This is Prompt 3 of the ad-creative-variations system. Use when the analyze-winner recommendation was "USE PROMPT 3" or "USE BOTH" and the text angle was STRONG. Never use on a WEAK text angle.
---

# Ad Creative — Same Text, New Background (Prompt 3)

Part of the `ad-creative-variations` family. Full context: `../ad-creative-variations/SKILL.md`.

## When to use

- The brief from `ad-creative-analyze-winner` recommended "USE PROMPT 3" or "USE BOTH" **and** the text angle was STRONG.
- **Never** use this if the text angle was WEAK — that would copy a weak text 5 times. Run `ad-creative-fix-weak-angle` instead and route to `ad-creative-new-angles` only.
- Never route fresh hooks (from `ad-creative-generate-hooks`) into this skill — the text here must stay 100% identical to the original.

## Prerequisites

- The full brief from `ad-creative-analyze-winner`, verbatim, with a STRONG text angle score.
- The winning ad image again.
- The target market/language (must match the brief — the text isn't changing, but rules should still be stated explicitly).

## Procedure

```text
Based on this winning ad brief:

[PASTE HERE: full output from Prompt 1]

I will upload the winning ad as a reference image.

Keep the EXACT same text and layout as the winning ad:
* Same headline text, same font style, same position
* Keep ALL layout and text elements exactly as listed in the brief
  under TEXT ELEMENTS and FORMAT
* Do NOT add layout elements that are not in the brief, and do NOT
  remove elements that are in the brief

Create 5 Higgsfield (Nano Banana 2) prompts that ONLY change
the background image/scene behind the exact same text.

Each prompt must describe:
* The main subject: if the brief says there is a person, describe age,
  gender, expression and pose. If the brief says there is no person,
  describe the product/scene/object instead. Follow the MAIN SUBJECT
  section of the brief.
* The setting/background
* The lighting and mood
* How it differs from the original while staying relevant
  to the same target audience

Rules for each prompt:
* Keep all text elements 100% identical to the winning ad
* All text in [LANGUAGE/MARKET]
* Only include brand name, logo and product if they were present
  in the original winning ad
* Stay relevant to the same target audience from the brief
* Each of the 5 images must feel distinctly different from each
  other and from the original
* Use winning ad as reference for text placement and style
* Clean ad creative only
```

## After running

Generate each of the 5 resulting prompts via the Higgsfield skill (Nano Banana 2 model), one image per prompt. Then run the QC checklist from the parent skill before approving each one — pay special attention to check #7 (text 100% identical to the original) since that is this route's entire point.

## Pitfalls

- Do not let the background generation drift the text, font, or layout at all — any deviation fails QC.
- Do not run this route on a WEAK text angle under any circumstance.
- Keep all 5 backgrounds meaningfully different from each other, not just palette swaps.
