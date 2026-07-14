---
name: ad-creative-generate-hooks
description: Generate 15 new headline hooks (3 each across 5 emotional angles) for a winning ad, with matching subheadlines. Optional step in the ad-creative-variations system, feeds only into ad-creative-new-angles (Prompt 2) — never into ad-creative-new-backgrounds (Prompt 3), which must keep the original text identical.
---

# Ad Creative — Generate Hooks (Step 3 / Hook Prompt)

Part of the `ad-creative-variations` family. Full context: `../ad-creative-variations/SKILL.md`.

## When to use

- Optional step, only relevant when the Prompt 2 route (new angles) is in play.
- Requires the brief from `ad-creative-analyze-winner` already produced.
- **Never** use this for the Prompt 3 / new-backgrounds route — that route keeps the existing headline 100% identical, a new hook never fits there.

## Prerequisites

- The full brief from `ad-creative-analyze-winner`, verbatim.
- The winning ad image again.
- The target market/language.

## Procedure

Run this prompt (adapt `[LANGUAGE/MARKET]`):

```text
Based on this winning ad brief:

[PASTE HERE: full output from Prompt 1]

I will upload the winning ad as a reference image.

Generate 15 new hooks for this ad that can replace the existing
headline while keeping the same winning format and visual DNA.

A hook replaces ONLY the headline. For each hook, also write one short
matching subheadline (1 line) so the ad text stays complete.

Deliver 3 hooks for each of these 5 angles:

Angle 1 - Problem Awareness
Hook directly into the pain point the target audience already
feels but hasn't named yet.

Angle 2 - Myth/Belief Breaker
Challenge a common assumption or mistake the target audience is making.

Angle 3 - Pure Proof
Show the result without selling it. A real before/after, a number,
a timeline. Let the proof speak — no commentary needed.

Angle 4 - Educational / Informational
Teach the audience something they didn't know. Position the product
as the logical conclusion of useful information.

Angle 5 - Direct Result / Transformation
Lead with the outcome. Bold, specific, no fluff.

Rules for every hook:
* All text in [LANGUAGE/MARKET]
* Maximum 8 words per hook
* Each hook must feel scroll-stopping on its own
* No hooks that sound similar to each other
* Match the tone and register of the winning ad
* Do not invent claims that weren't present or implied in the winning ad

Output format — for each hook deliver:
* The hook text
* The matching subheadline
* Which angle it uses
* One sentence on why it works for this specific audience
```

## After running

Pick a **maximum of 5 of the 15 hooks** and hand them to `ad-creative-new-angles` — that skill has a dedicated hook block matched one-per-variation-angle.

## Pitfalls

- Never route hooks into `ad-creative-new-backgrounds` (Prompt 3) — that route requires the text to be 100% identical to the original.
- Don't pick more than 5 hooks forward — `ad-creative-new-angles` generates exactly 5 variations, one per angle.
- Keep hooks distinct from each other even within the same angle; near-duplicates defeat the point of testing.
