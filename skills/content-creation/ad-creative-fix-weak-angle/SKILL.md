---
name: ad-creative-fix-weak-angle
description: Diagnose why a winning ad's text angle scored WEAK and rewrite it into 5 stronger variations with a recommended Top Pick. Runs after ad-creative-analyze-winner when the TEXT ANGLE SCORE was WEAK, and before generating any new angle variations (ad-creative-new-angles). Never use to touch Prompt 3 / same-background variations.
---

# Ad Creative — Fix Weak Text Angle (Step 2b)

Part of the `ad-creative-variations` family. Full context: `../ad-creative-variations/SKILL.md`.

## When to use

- Only after `ad-creative-analyze-winner` produced a TEXT ANGLE SCORE of WEAK (6 or lower).
- Never run this as a standalone step without that brief — it needs the full brief output verbatim.
- The output (Top Pick) feeds into `ad-creative-new-angles`. It never feeds into `ad-creative-new-backgrounds` (Prompt 3) — a weak text angle is never the reason to copy, only to fix.

## Prerequisites

- The full brief from `ad-creative-analyze-winner`, verbatim.
- The winning ad image again.
- The target market/language (same one used in the brief).

## Procedure

Run this prompt (adapt `[LANGUAGE/MARKET]`):

```text
Based on this winning ad brief:

[PASTE HERE: full output from Prompt 1]

I will upload the winning ad as a reference image.

The current text angle is WEAK. Analyse why and fix it.

STEP 1 — DIAGNOSE THE WEAKNESS
Identify in 2-3 sentences exactly why the current text angle is not working:
* Is it too generic? Too product-focused instead of problem-focused?
* Does it lack emotional pull or specificity?
* Is the hook too weak to stop the scroll?

STEP 2 — REWRITE THE TEXT ANGLE
Create 5 stronger text angle variations that fix the diagnosed weakness.

Each variation must include:
* New headline (max 8 words, [LANGUAGE/MARKET])
* New subheadline or body copy (1-2 lines)
* Which emotional trigger it uses
  (curiosity / fear / social proof / authority / transformation)
* One sentence explaining why it is stronger than the original

Rules:
* All text in [LANGUAGE/MARKET]
* Keep the same visual format and layout from the brief
* Do not invent claims not present or implied in the winning ad
* Each variation must feel scroll-stopping on its own
* Avoid angles that sound similar to each other

STEP 3 — TOP PICK
Recommend the single strongest variation and explain in 2 sentences
why it would outperform the original text angle for this specific audience.

Output each variation clearly numbered 1-5 before the top pick.
```

## After running

Take the headline, subheadline, and emotional trigger from the **Top Pick** forward into `ad-creative-new-angles` — that skill has a dedicated block for it. Discard the other 4 variations unless the user wants to keep them as extra options.

## Pitfalls

- Do not run this on a STRONG text angle — nothing to fix, go straight to `ad-creative-new-angles` and/or `ad-creative-new-backgrounds`.
- Do not invent product claims that weren't in the original ad, even to make a headline punchier.
- Do not let variations sound like rephrasings of each other — each must attack the diagnosed weakness from a genuinely different emotional trigger.
