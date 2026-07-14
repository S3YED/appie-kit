---
name: ad-creative-new-angles
description: Generate 5 new Higgsfield (Nano Banana 2) prompts for a winning ad — same visual DNA and format, 5 different angles (problem awareness, myth-breaker, pure proof, educational, direct result). This is Prompt 2 of the ad-creative-variations system. Use when the analyze-winner recommendation was "USE PROMPT 2" or "USE BOTH".
---

# Ad Creative — New Angles, Same DNA (Prompt 2)

Part of the `ad-creative-variations` family. Full context: `../ad-creative-variations/SKILL.md`.

## When to use

- The brief from `ad-creative-analyze-winner` recommended "USE PROMPT 2" or "USE BOTH".
- If the text angle was WEAK, `ad-creative-fix-weak-angle` must run first — feed its Top Pick in here (see below), never the original weak headline.

## Prerequisites

- The full brief from `ad-creative-analyze-winner`, verbatim.
- If the text angle was WEAK: the Top Pick (headline, subheadline, emotional trigger) from `ad-creative-fix-weak-angle`.
- Optionally: up to 5 hooks from `ad-creative-generate-hooks`.
- The winning ad image again.
- The target market/language.

## Procedure

Assemble the prompt below. Include the "WEAK" block only if the text angle was weak; include the hooks block only if hooks were generated. Delete whichever blocks don't apply — do not leave placeholder text in the final prompt.

```text
Based on this winning ad brief:

[PASTE HERE: full output from Prompt 1]

--- ONLY FILL IN IF TEXT ANGLE WAS "WEAK" — otherwise delete this block ---
IMPORTANT: The original text angle was weak and has been replaced.
Ignore the original headline in the brief. Use this improved text angle
as the new baseline for tone, claim and direction of all 5 variations:
* New headline: [PASTE HERE: headline from Top Pick]
* New subheadline: [PASTE HERE: subheadline from Top Pick]
* Emotional trigger: [PASTE HERE: trigger from Top Pick]
--- END OF BLOCK ---

--- ONLY FILL IN IF YOU HAVE HOOKS FROM THE HOOK PROMPT — otherwise delete ---
Use these pre-approved hooks. Match each hook to the variation
with the same angle:
* Hook 1: [PASTE HERE: hook + subheadline]
* Hook 2: [PASTE HERE: hook + subheadline]
* Hook 3: [PASTE HERE: hook + subheadline]
* Hook 4: [PASTE HERE: hook + subheadline]
* Hook 5: [PASTE HERE: hook + subheadline]
--- END OF BLOCK ---

I will upload the winning ad as a reference image.

Create 5 Higgsfield (Nano Banana 2) prompts that:

1. Keep the exact winning visual DNA and format from the brief
2. Attack from a completely different angle each time:

   Variation 1: Problem awareness angle
   Variation 2: Myth/belief breaking angle
   Variation 3: Pure proof angle
   Variation 4: Educational/informational angle
   Variation 5: Direct/aggressive result angle

Rules for each prompt:
* Feel FRESH and scroll-stopping
* Never repeat the same hook or headline
* All text in [LANGUAGE/MARKET]
* Before/after format allowed and encouraged if it fits
* Only include brand name, logo and product if they were present
  in the original winning ad
* Use winning ad as reference for layout and style
* Target audience: same as winning ad brief
* Clean ad creative only
```

## After running

Generate each of the 5 resulting prompts via the Higgsfield skill (Nano Banana 2 model), one image per prompt. Then run the QC checklist from the parent skill before approving each one.

## Pitfalls

- Never carry the original weak headline forward if a Top Pick exists — it must be fully replaced, not blended.
- Keep the 5 variations genuinely distinct by angle; don't let two converge on the same emotional trigger.
- Don't add a brand/logo/product that wasn't in the original ad, even if it "would look better".
