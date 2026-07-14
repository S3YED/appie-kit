# Ad Creative System — Winning Variations

Complete guide to all prompts · Version 2

Source: Seyed's Google Doc ("Ad Creative System — Winning variations, Complete guide to all prompts, Version 2, Schweizer Hochdeutsch · Swiss market"), converted to markdown 2026-07-14.

> Default market/language in this source doc is **Schweizer Hochdeutsch (Swiss Standard German, no ß — always "ss")**. Treat market + language as a parameter when reusing this system for a different client/market — see the skill files in this family for the parameterized versions.

## Quick reference

| Prompt | What it does | Requires | Output |
|---|---|---|---|
| Prompt 1 | Analyses the winning ad + gives recommendation + score | Ad image | Brief + recommendation + STRONG/WEAK score |
| Prompt 2 | 5 new angles, same DNA | Prompt 1 output (+ optional Top Pick / hooks) | 5 Higgsfield prompts |
| Prompt 3 | 5 new backgrounds, exact same text | Prompt 1 output — only if text is STRONG | 5 Higgsfield prompts |
| Text Angle Improvement | Diagnose + fix a weak text angle | Prompt 1 output + image | 5 stronger angles + Top Pick |
| Hook Prompt | 15 new hooks (for Prompt 2 only) | Prompt 1 output + image | 15 hooks + subheadlines |

**Always:** Step 0 → Prompt 1 → follow the recommendation → if WEAK, run Text Angle Improvement first → Prompt 2 and/or 3 → QC → save.

## How this document works

- Everything you need to fill in is a **[PASTE HERE: ...]** or **[FILL IN: ...]** placeholder.
- Everything in a fenced code block is copied word for word into the prompt (e.g. to Claude).
- Always follow the steps in order. Never skip a step.

## STEP 0 — Is this actually a winning ad?

An ad may only enter this system if it meets **both** requirements:

- Minimum spend: **[FILL IN: e.g. CHF 300]**
- ROAS above **[FILL IN: e.g. 2.5]** OR CPA below **[FILL IN: amount]**

**Doesn't meet these? → Stop.** This system is for proven winners only.

## The system in one picture

```
Winning ad
    |
STEP 1: Prompt 1 (analysis)  ->  recommendation: PROMPT 2, PROMPT 3, or BOTH
    |                             and: text angle STRONG or WEAK
    |
Text angle WEAK?  ->  STEP 2b: Text Angle Improvement  ->  take the Top Pick
    |
STEP 3 (optional): Hook Prompt  ->  for Prompt 2 only!
    |
STEP 4: Prompt 2 and/or Prompt 3  ->  5 Higgsfield prompts each
    |
STEP 5: Generate in Higgsfield + QC checklist
    |
STEP 6: Save with correct naming + go live
```

## STEP 1 — Analyse the winning ad (PROMPT 1)

1. Open a new chat.
2. Upload the winning ad as an image.
3. Copy Prompt 1 below and paste it in.
4. Save the output (see Step 6) — you need it for **all** following steps.

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
All ad copy in [LANGUAGE/MARKET, e.g. Schweizer Hochdeutsch — Swiss Standard
German, no ß, always "ss"].
```

- **RECOMMENDATION** → determines whether you go to Prompt 2, Prompt 3 or both.
- **TEXT ANGLE SCORE** → STRONG or WEAK. If WEAK, go to Step 2b FIRST.

## STEP 2 — Choose your route

| Claude says | What it means | What you do |
|---|---|---|
| USE PROMPT 3 | The TEXT is the winner | Keep text 100%, only refresh the background |
| USE PROMPT 2 | The FORMAT is the winner | Keep the format, 5 new text angles |
| USE BOTH | Both are strong | Run Prompt 2 AND Prompt 3 → 10 creatives, live simultaneously, equal budget per creative |
| TEXT ANGLE: WEAK | The text is too weak | Step 2b FIRST, only then Prompt 2. Prompt 3 is NOT allowed (you would be copying a weak text) |

**Remember:** WEAK + "USE PROMPT 3" cannot coexist. If the text is weak, the text is never the reason the ad wins. When in doubt: run Step 2b.

## STEP 2b — Only if the text angle is WEAK (TEXT ANGLE IMPROVEMENT)

1. Upload the winning ad again as an image.
2. Copy the prompt below and fill in the placeholder.
3. Save the **TOP PICK** from the output — you will paste it into Prompt 2.

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
* All text in [LANGUAGE/MARKET, e.g. Schweizer Hochdeutsch, no ß, always "ss"]
* Keep the same visual format and layout from the brief
* Do not invent claims not present or implied in the winning ad
* Each variation must feel scroll-stopping on its own
* Avoid angles that sound similar to each other

STEP 3 — TOP PICK
Recommend the single strongest variation and explain in 2 sentences
why it would outperform the original text angle for this specific audience.

Output each variation clearly numbered 1-5 before the top pick.
```

**Then:** take the headline, subheadline and trigger from the Top Pick into Prompt 2 (there is a dedicated spot for it).

## STEP 3 — Optional: generate new hooks (HOOK PROMPT)

**Note: hooks are ONLY for Prompt 2.** Prompt 3 keeps all text identical — a new hook never fits there.

1. Upload the winning ad again.
2. Copy the prompt below and fill in the placeholder.
3. Pick a maximum of 5 of the 15 hooks → paste them into the hook block of Prompt 2.

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
* All text in [LANGUAGE/MARKET, e.g. Schweizer Hochdeutsch, no ß, always "ss"]
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

## STEP 4A — PROMPT 2: New angles, same DNA

**Use when the recommendation says: USE PROMPT 2 or USE BOTH.**

1. Upload the winning ad again.
2. Copy the prompt below.
3. Fill in the placeholders: Prompt 1 output (always) · Top Pick from Step 2b (only if WEAK, otherwise delete the block) · hooks from Step 3 (only if created, otherwise delete the block).

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
* All text in [LANGUAGE/MARKET, e.g. Schweizer Hochdeutsch, no ß, always "ss"]
* Before/after format allowed and encouraged if it fits
* Only include brand name, logo and product if they were present
  in the original winning ad
* Use winning ad as reference for layout and style
* Target audience: same as winning ad brief
* Clean ad creative only
```

## STEP 4B — PROMPT 3: Same text, new background

**Use when the recommendation says: USE PROMPT 3 or USE BOTH. Never use if the text angle was WEAK.**

1. Upload the winning ad again.
2. Copy the prompt below and fill in the placeholder.

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
* All text in [LANGUAGE/MARKET, e.g. Schweizer Hochdeutsch, no ß, always "ss"]
* Only include brand name, logo and product if they were present
  in the original winning ad
* Stay relevant to the same target audience from the brief
* Each of the 5 images must feel distinctly different from each
  other and from the original
* Use winning ad as reference for text placement and style
* Clean ad creative only
```

## STEP 5 — Generate in Higgsfield + QC checklist

1. Copy each Higgsfield prompt one by one into Higgsfield (Nano Banana 2).
2. Generate the image.
3. Check EVERY image against this list before approving it:

| # | Check | YES/NO |
|---|---|---|
| 1 | All text is spelled correctly (compare letter by letter) | |
| 2 | No ß in the text if the market uses Swiss German — always "ss" | |
| 3 | Umlauts (ä, ö, ü) are rendered correctly, not garbled | |
| 4 | Text is clearly readable (contrast, not cut off) | |
| 5 | Logo/brand/product only present if in the original | |
| 6 | No claims that were not in the original ad | |
| 7 | For Prompt 3: text is 100% identical to the original | |

**One point NO?** → Regenerate or adjust the prompt. Never go live.

## STEP 6 — Saving and naming

**All outputs (briefs AND images) go to:** [FILL IN: exact folder path, e.g. Drive/Creatives/Product/AI-Iterations]

**Image naming:** `product_YYYY-MM-DD_P2orP3_variation1-5.png`
Example: `glowserum_2026-07-10_P2_3.png`

**Brief naming (Prompt 1 output):** `product_YYYY-MM-DD_brief.txt`

**For USE BOTH:** all 10 creatives live simultaneously in the same test campaign, equal budget per creative. After **[FILL IN: e.g. CHF 50]** spend per creative: winners continue, losers are turned off.

## The 5 most common mistakes

1. **Running Prompt 2/3/hooks without Prompt 1** → everything builds on the brief. No brief = generic output.
2. **Putting new hooks into Prompt 3** → Prompt 3 keeps text 100% identical. Hooks belong to Prompt 2 only.
3. **Running Prompt 3 when the text angle was WEAK** → you would be copying a weak text 5 times.
4. **Skipping QC** → AI garbles text more often than you think, especially umlauts.
5. **Not saving output with the naming convention** → nobody can find anything, everyone does double work.

Version 2 · converted 2026-07-14 by Appie-Opus from Seyed's source Google Doc.
