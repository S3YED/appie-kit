---
name: ad-creative-analyze-winner
description: Analyze a proven-winning ad image and produce a structured creative brief with a PROMPT 2/PROMPT 3/BOTH recommendation and a STRONG/WEAK text-angle score. This is always the first step of the ad-creative-variations system (see that skill for the full pipeline) — every later step depends on this brief verbatim.
---

# Ad Creative — Analyze Winner (Prompt 1)

Part of the `ad-creative-variations` family. Full context: `../ad-creative-variations/SKILL.md` and `../ad-creative-variations/references/ad-creative-system-source.md`.

## When to use

- First step whenever asked to scale/vary a winning ad.
- Never skip this even if the user only wants "just the new angles" — every downstream prompt (new angles, new backgrounds, hook generation, weak-angle fix) needs this brief verbatim.

## Prerequisites

- The winning ad, as an image.
- Confirm the ad actually qualifies as a winner first (Step 0 in the parent skill: minimum spend + ROAS/CPA threshold the user has set). If unproven, stop and say so.
- Know the target market/language (ask if unclear — do not assume Swiss German).

## Procedure

1. Load the winning ad image.
2. Run this analysis (adapt `[LANGUAGE/MARKET]` to the actual target, e.g. "Schweizer Hochdeutsch — Swiss Standard German, no ß, always 'ss'", or "German (Germany)", "Dutch", etc.):

```text
Analyse this winning ad and extract the following elements.

START your answer with two clear labels:

A) RECOMMENDATION: "USE PROMPT 2" or "USE PROMPT 3" or "USE BOTH"
   + one sentence why.
B) TEXT ANGLE SCORE: "STRONG" or "WEAK" + a score from 1-10
   + one sentence why. Score 6 or lower = WEAK.

Then extract:

1. VISUAL STYLE: How is the image composed?
   (close-up, lifestyle, product shot, before/after etc.)

2. FORMAT: What is the ad format?
   (split screen, single image, text overlay, two-zone with bottom strip etc.)
   List every layout element that is actually present. Do not assume elements
   that are not visible.

3. HOOK STYLE: What emotional trigger does the headline use?
   (curiosity, fear, social proof, problem-aware, authority etc.)

4. CORE MESSAGE: What is the main promise or benefit?

5. TEXT ELEMENTS: List all text visible in the ad exactly as written.

6. PRODUCT PLACEMENT: Where and how is the product shown?
   If no product is visible, say so.

7. MAIN SUBJECT: Is there a person in the image? If yes: age, gender,
   expression, pose. If no: describe the main subject (product, scene, object).

8. TARGET AUDIENCE: Who is this ad clearly targeting?

9. WINNING DNA: Summarize in 2-3 sentences what makes this ad work
   and what must be preserved in all variations.

Recommendation logic you must follow:
* USE PROMPT 3 if the TEXT is the main reason this ad wins.
  The text must stay exactly as is; only the background image gets refreshed.
* USE PROMPT 2 if the VISUAL FORMAT is the main reason this ad wins.
  The format stays; the text angle can be varied.
* USE BOTH if text AND format are both clearly strong.

Output this as a structured brief I can use to brief an AI image generator.
All ad copy in [LANGUAGE/MARKET].
```

3. Present the RECOMMENDATION and TEXT ANGLE SCORE up front, clearly, before the rest of the brief.
4. Save the full brief output verbatim (see naming convention in the parent skill) — hand it to whichever step runs next.

## Recommendation logic (must follow exactly)

- **USE PROMPT 3** if the TEXT is the main reason the ad wins — text stays exactly as is, only the background refreshes.
- **USE PROMPT 2** if the VISUAL FORMAT is the main reason the ad wins — format stays, text angle can vary.
- **USE BOTH** if text AND format are both clearly strong.

## Pitfalls

- Do not soften a WEAK score to avoid an extra step — a 6-or-lower text angle score is WEAK, full stop, and routes to `ad-creative-fix-weak-angle` before anything else.
- Do not invent layout elements that are not actually visible in the ad.
- Do not skip straight to generating variations without this brief — every later prompt is built "based on this winning ad brief".
