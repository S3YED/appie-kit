---
name: ad-creative-variations
description: Turn one proven-winning ad into a batch of new Higgsfield ad-creative variations (new angles, new backgrounds, fixed weak text, fresh hooks) using a fixed, gated 6-step system. Use when asked to "make variations of this winning ad", "scale this ad", "generate new creatives from this winner", or similar ad-creative scaling requests.
---

# Ad Creative Variations System

Turns one proven-winning ad into a batch of Higgsfield-ready creative variations, using a strict, gated pipeline so every variation preserves what actually makes the ad win instead of guessing from scratch.

Full source spec (Seyed's canonical doc, Version 2): `references/ad-creative-system-source.md`. Read it once for the complete rationale; this file is the operating summary.

## When to use

- The user shares a winning ad (image) and asks for variations, new angles, or scaled creative.
- The user asks to generate Higgsfield prompts from a proven ad.
- The user asks to fix a weak ad angle or generate new hooks for an existing winner.

## Hard gate — Step 0

Only proceed if the ad meets the winner bar the user has set (minimum spend AND a ROAS/CPA threshold). Ask for these numbers if not given — do not run the system on unproven ads. If the ad doesn't qualify, say so and stop.

## The pipeline

```
Winning ad
    |
Prompt 1 (analyze) -> ad-creative-analyze-winner
    |                  recommendation: PROMPT 2 / PROMPT 3 / BOTH
    |                  text angle: STRONG or WEAK
    |
WEAK? -> ad-creative-fix-weak-angle -> take the Top Pick
    |
optional -> ad-creative-generate-hooks (Prompt 2 only, max 5 of 15 hooks)
    |
ad-creative-new-angles (Prompt 2)  and/or  ad-creative-new-backgrounds (Prompt 3)
    |
Generate each resulting prompt in Higgsfield (Nano Banana 2)
    |
QC checklist (below) on every image
    |
Save with the naming convention (below) and hand off for review/go-live
```

Always run in this order. Never skip Prompt 1 — every later step depends on its brief.

## Step-by-step

1. **Analyze** — use skill `ad-creative-analyze-winner` on the winning ad image. Get RECOMMENDATION (PROMPT 2 / PROMPT 3 / BOTH) and TEXT ANGLE SCORE (STRONG/WEAK). Keep the full brief output — every later step needs it verbatim.
2. **Route:**
   - TEXT ANGLE is WEAK → run `ad-creative-fix-weak-angle` first. Prompt 3 is not allowed on a weak text angle (never copy a weak text 5 times). Take the Top Pick forward into step 4.
   - RECOMMENDATION is PROMPT 3 or BOTH, and text angle is STRONG → Prompt 3 is in play.
   - RECOMMENDATION is PROMPT 2 or BOTH → Prompt 2 is in play.
3. **Optional hooks** — if the user wants fresh headline hooks (Prompt 2 route only), run `ad-creative-generate-hooks`, then pick at most 5 of the 15 to feed into Prompt 2.
4. **Generate variations:**
   - Prompt 2 in play → run `ad-creative-new-angles` (5 new angles, same visual DNA, format from the brief; use the Top Pick or hooks if produced in steps 2-3).
   - Prompt 3 in play → run `ad-creative-new-backgrounds` (5 new backgrounds, text 100% identical to the brief).
   - Both in play → run both; treat the result as 10 creatives that go live simultaneously with equal budget per creative.
5. **Render** each resulting Higgsfield prompt via the Higgsfield skill/CLI (Nano Banana 2 model). One image per prompt.
6. **QC every image** against the checklist below before approving. One NO = regenerate or adjust the prompt; never ship an unchecked image.
7. **Save + hand off** using the naming convention below, and tell the user what to review before it goes live.

## QC checklist (every generated image)

- [ ] All text is spelled correctly (compare letter by letter)
- [ ] No ß in the text if the market uses Swiss German — always "ss"
- [ ] Umlauts (ä, ö, ü) render correctly, not garbled
- [ ] Text is clearly readable (contrast, not cut off)
- [ ] Logo/brand/product present only if it was in the original
- [ ] No claims beyond what was in the original ad
- [ ] For Prompt 3 output: text is 100% identical to the original

## Naming convention

- Image: `product_YYYY-MM-DD_P2orP3_variation1-5.png` (e.g. `glowserum_2026-07-10_P2_3.png`)
- Brief (Prompt 1 output): `product_YYYY-MM-DD_brief.txt`
- Ask the user for the destination folder if not already known.

## Market / language parameter

The source doc defaults to Schweizer Hochdeutsch (Swiss Standard German, no ß, always "ss"). Every sub-skill takes market/language as a parameter — ask the user which market this ad is for (or infer from context: existing client market, ad's own language) before running Prompt 1, and use that language consistently across every subsequent step. Do not silently default to Swiss German for a client whose market is different.

## The 5 most common mistakes (from the source doc)

1. Running Prompt 2/3/hooks without Prompt 1 first — everything builds on the brief.
2. Putting new hooks into Prompt 3 — Prompt 3 keeps text 100% identical, hooks are Prompt-2-only.
3. Running Prompt 3 when the text angle was WEAK — that copies a weak text 5 times.
4. Skipping QC — AI garbles text more often than expected, especially umlauts/diacritics.
5. Not saving with the naming convention — nobody can find anything, work gets duplicated.

## Sub-skills in this family

- `ad-creative-analyze-winner` — Prompt 1
- `ad-creative-fix-weak-angle` — Step 2b
- `ad-creative-generate-hooks` — Step 3 (hook prompt)
- `ad-creative-new-angles` — Prompt 2
- `ad-creative-new-backgrounds` — Prompt 3
