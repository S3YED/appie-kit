# video-editing-pro Skill

## Purpose

Decision-level framework for cutting talking-head short-form video (Reels/Shorts/TikTok). Not tool instructions — cut decisions: which sentences survive, where to end them, how to pick the hook, how to pace energy, and how to know when you got it wrong. Codified from auto-editor source defaults, production-audio practitioner interviews, platform retention data, and analysis of the 2026-05-03 Weblyfe Content Factory clips.

---

## Source

Every entry consumed directly, not cited generically:

| Source | URL | What it gave |
|--------|-----|-------------|
| auto-editor reference | https://auto-editor.com/ref/edit | Exact defaults: threshold=0.04 (normalized amplitude), margin=0.2s padding, smooth=0.2s,0.1s |
| auto-editor options | https://auto-editor.com/options | `--margin 0.2s` default, `--smooth 0.2s,0.1s` (mincut 0.2s, minclip 0.1s) |
| auto-editor blog: threshold removal | https://auto-editor.com/blog/silent-threshold | Why 0.04 is the amplitude default, not dB |
| Production Expert: René Coronado interview edit | https://www.production-expert.com/production-expert-1/2020/7/29/editing-audio-interviews-what-choices-do-we-make-and-why | "My goal is NOT to get from 14s to 6s" — clarity-of-thought frame vs duration-reduction frame |
| podmuse.com: pro podcast edit workflow | https://www.podmuse.com/post/edit-audio-for-podcast | Selective filler removal rule: cut fillers that block clarity or stack awkwardly, leave ones that "sound human and disappear in context" |
| Recut silence removal docs | https://getrecut.com/remove-silence-from-video-automatically | Padding 0.4–0.5s sounds natural; 0s creates rapid-fire effect |
| Aibrify: YouTube Shorts retention curve playbook 2026 | https://aibrify.com/blog/youtube-shorts-retention-curve-playbook | Pacing target 1.5–2s per visual change; below 1.2s = noise, above 2.5s = dip; 55–70% retention for talking-head |
| TikTok editing guide | https://edicionvideopro.com/en/editing-for-platforms-video-marketing/tiktok-video-editing-guide/ | "Every pause between sentences, every transitional phrase should be cut"; drop-off graph as diagnostic |
| Postigniter: hook formulas | https://postigniter.com/blog/high-performance-hooks-writing-scroll-stopping-intros-for-short-form-video | Optimal hook 1.5–3s; 0.1–0.3s cuts for dynamism in hook window |
| go-viral.app: first 3 seconds | https://www.go-viral.app/blog/hook-first-3-seconds/ | <50% retention at 3s = hook failing; >70% = strong; target >70% |
| autoshorts.app: hooks 2026 | https://www.autoshorts.app/blog/instagram-reels-hooks-2026 | 3+ cuts in first 3s boost watch time 58%; each cut creates "change signal" |
| VlogLikePro: energy management | http://vloglikepro.com/editing-styles-that-drive-watch-time-beyond-basics | Energy curve; cut every 4s→3s→2s building to reveal; 10–15s micro-hook cadence |
| We Design Motion: attention without faster cuts | https://wedesignmotion.com/blog/design/video-content-that-earns-attention-without-faster-cuts/ | 5-layer attention model: promise→clarity→progression→contrast→craft |
| socialync.io: hook-body-payoff structure | https://www.socialync.io/blog/short-form-video-structure-guide-2026 | "8 seconds without visual change = viewer exit"; tension > rush to resolution |
| Ascynd: Hormozi captions breakdown | https://ascynd.io/en/blog/hormozi-captions | One keyword per phrase; noun or verb carrying meaning; yellow #FFD93D; 200–500ms per word timing |
| reelwords.ai: caption retention | https://reelwords.ai/blog/how-to-add-captions-to-short-form-video | Highlight: promise words, contrast words, specificity (numbers/outcomes), stakes words; never highlight "the", "and", "like" |
| Film Editing Pro: reviewing your own cuts | https://filmeditingpro.com/3-editing-tips-for-reviewing-your-own-cuts | Audio-off test; black-and-white test; Hitchcock rule; first-reaction markers |
| joelv.ca: post-edit fresh-eyes technique | https://joelv.ca/blog/best-way-to-edit-better | Watch with someone beside you = best fresh-eyes; Joe Walker (Dune) black-and-white review trick |
| autocut.com: finding viral moments | https://autocut.com/en/blogs/viral-moment/ | Three criteria for clip viability: hook (curiosity), clarity (standalone), emotion (tension/surprise/reaction) |

---

## Quick Reference

### Cut-decision flowchart (per sentence)

```
Is this sentence the strongest opener (action verb, bold claim, contrast)?
  YES → Hook candidate. Check: does it land in ≤3s? Does it open a loop?
  NO  → continue

Does this sentence ADVANCE the story, prove a claim, or deliver payoff?
  YES → KEEP
  NO (transition / re-statement / filler connector) → CUT

Is this sentence a list item where the list has 3+ members?
  KEEP only the 2 strongest. Cut the weakest.

Does this sentence repeat information already established?
  CUT (restatements are dead weight in <60s formats)

After cutting, does the sentence before and after still connect logically?
  YES → done
  NO  → keep a bridge, or reorder to make it work without the cut sentence
```

### Pause decision table

| Gap duration | Action |
|---|---|
| < 100ms | Leave untouched — any cut here clips consonants |
| 100–150ms | Cut if it's between two sentences with no breath | 
| 150–300ms | Cut between sentences; leave within a sentence if it's a natural emphasis pause |
| 300–500ms | Cut in fast-paced segments; consider leaving in slow/emotional segments as breathing room |
| > 500ms | Cut. Always. This is where auto-editor's 0.4–0.5s padding target is your floor |
| Inter-segment join | Add ~200ms of ambient room tone between segments — hard joins feel robotic |

Auto-editor defaults for reference:
- `threshold=0.04` (normalized amplitude, not dB — roughly equivalent to -28dB)
- `--margin 0.2s` (200ms padding added each side of every kept segment)
- `--smooth 0.2s,0.1s` (mincut=200ms, minclip=100ms — no cut shorter than 200ms, no clip shorter than 100ms)

### Sentence scoring rubric (for a multi-sentence take)

Score each sentence 0–3 on each axis, keep the top scorers:

| Axis | 0 | 1 | 2 | 3 |
|------|---|---|---|---|
| New information | Repeats | Filler | Adds context | Standalone proof |
| Energy | Flat | Mild | Active | Peak moment |
| Clarity | Confusing | Needs context | Clear | Instantly clear |
| Memorability | Forgettable | Decent | Quotable | Single sharp claim |

Cut sentences scoring ≤4 total when length forces a choice.

---

## Core Principles

### A. Pause length thresholds

**1. The 200ms floor rule (auto-editor verified)**
Auto-editor's default margin is 200ms. This is not arbitrary — it is the minimum time the brain needs to register a cut without perceiving it as a clip. Cutting tighter than 200ms between speech segments produces the "machine-gun" effect. The practical rule: never trim a pause to less than 100ms of leading silence before the next word. The safe trim target is 150–200ms preserved.

Source: auto-editor `--margin 0.2s` default + Recut "0.4–0.5s sounds pretty natural" (0.4s is a comfortable listener-pace padding).

**2. The 300ms breath preservation rule**
A pause that follows a sentence-final vowel (ends with rising or falling intonation) signals meaning. "It's currently happening." followed by 300ms is not sloppiness — it is the speaker marking emphasis. Cut that breath and the claim loses weight. Preserve pauses that follow strong claims.

Source: René Coronado (Production Expert): "we leave in...pauses that actually help convey the context of the thought."

### B. Sentence selection

**3. The clarity-of-thought frame (not duration-reduction frame)**
The wrong mental model: "I need to get from 36s to under 30s." The right mental model: "What is the single sharpest version of this person's thought?" Duration drops as a consequence, not as a goal. This matters because duration-reduction thinking produces mechanical cuts that remove good content to hit a number.

Source: René Coronado: "My goal is NOT to get from 14 seconds to 6 seconds."

**4. Cut when the sentence restates**
If a sentence says the same thing as the previous sentence in different words, cut it. In the Weblyfe clip-02, "Thank you page, checkout page, you name it, all of it" (15.74–18.9s) restates what the Monday funnel sentence already established. It got cut in v1 — correctly. "Even the screenshots and the mockups are all made by my AI" (19.0–21.76s) adds new information (AI-made mockups) but was also cut — that may have been an error (see clip analysis below).

**5. The "does it earn its place" test**
From TikTok editing doctrine: every pause between sentences, every transitional phrase, every breath that does not add rhythm should be cut. Transitional connectors ("And then...", "So basically...", "You know what I mean?") are the first to go.

**6. Keep list items only if there are ≤2 or if you can name them as a number**
Three proof items in a row (WhatsApp system, full funnel, screenshots) exhausts short-form attention. Either cut to the 2 strongest, or reframe as "I built 3 systems in a few hours" (numerical frame) and cut the enumeration.

### C. Filler word policy

**7. The selective removal rule**
Not all fillers are equal:
- "um" / "uh" mid-sentence: cut always — they add no rhythm
- "you know" / "I mean" at start of sentence: cut — these are delay tactics, not meaning
- "like" used as a hedge mid-sentence ("I was like, building this thing"): cut the "like" only if it does not change the tone; sometimes "like" is character
- "so" at sentence start as a connector: leave it if the sentence that follows is strong; cut it if the sentence is weak anyway (cutting the sentence solves the problem)
- Repeated words / stutters ("I—I was building"): cut to the clean take of the word

Source: podmuse.com — "Cut fillers that block clarity, stack up awkwardly, or interrupt momentum. Leave the ones that sound human and disappear in context."

**8. Over-cleaning destroys naturalness**
If you remove every "um", breath, and restart, the speech sounds "assembled instead of spoken." For a personal brand creator (not a news anchor), some raw edges are trust signals. The test: does the filler make the speaker sound more like a real person, or does it make them sound nervous and unprepared? Keep the former, cut the latter.

### D. Hook precision

**9. The hook is not the first sentence — it is the strongest action-or-contrast moment**
Do not default to the first complete sentence. Find the sentence with the sharpest verb or the most surprising contrast. Scan the full transcript and score each sentence on: does this sentence make me want to know what happens next? The one that scores highest is the hook, even if it originally appeared at second 22 of the take.

**10. The 1.5–3 second hook window**
The hook must land and deliver its core signal within 1.5–3 seconds. If the strongest sentence takes 5 seconds to deliver, trim it to its core claim. "Watch this." (0.5s) combined with a visual action beats a 4-second explanation of what is about to happen.

Platform benchmarks:
- >70% retention at 3s = strong hook, optimize the rest
- 50–70% at 3s = hook is partial, needs faster delivery or stronger first word
- <50% at 3s = hook is failing, re-cut or re-shoot

**11. The open-loop requirement**
A strong hook does not deliver the payoff — it promises one. "Oh, but say it, how is AI gonna make your work easier? Watch this." is an open loop: the viewer must keep watching to get the answer. A closed statement ("AI makes work easier by automating tasks") delivers the payoff before the viewer is committed — they can leave. Structure: hook = question or claim, payoff = later in video.

### E. Energy curve

**12. Build → Peak → Release, not flat**
The wrong edit: same pacing throughout, viewer drifts. The correct structure:
- Seconds 0–3: HIGH (fast cut, strong claim, open loop)
- Seconds 3–15: MEDIUM-HIGH (proof, evidence, one new fact every 3–5s)
- Seconds 15–30: HIGHEST (demo reveal, strongest proof, surprising outcome)
- Seconds 30–end: MEDIUM (vision/implication + CTA)

Cut frequency mirrors energy: 1 cut per 4s in setup → 1 per 3s in middle → 1 per 2s approaching peak. Do not apply uniform cut pacing.

Source: VlogLikePro energy curve + Aibrify pacing target 1.5–2s per visual change.

**13. The 8-second stagnation rule**
More than 8 seconds without a visual change causes viewer drop. In a talking-head without B-roll, visual changes come from: cuts to a new take angle, zoom/crop change, text overlay appearing, caption emphasis, or transition to screen recording. Plan one of these every 5–8 seconds minimum.

Source: socialync.io: "8 seconds without a visual change = viewer exit."

**14. The energy valley before the peak**
The Dune editor Joe Walker's principle: the moment before the peak should be slightly lower energy — a deliberate pause or slowdown — so the peak lands with contrast. Monotonically building energy without a valley feels like shouting. One 300–500ms beat of relative quiet before the reveal makes the reveal feel bigger.

### F. J-cuts and L-cuts in talking head

**15. J-cut and L-cut offset: 200ms–1s**
Start with 1 second overlap (as recommended by Artlist) and trim toward 200ms if the audio track permits. In a talking-head monologue, L-cuts are more useful than J-cuts: let the voice continue while cutting to a screen recording or B-roll. The audio must be mid-sentence — cutting on the last word of a sentence before the visual cut creates a false ending that kills pacing.

Source: edicionvideopro.com J-cut/L-cut guide — "start with a one-second overlap and move from there."

**16. Cut on the consonant, not the vowel**
When trimming within a sentence, cut on the leading consonant of the next word, not on the trailing vowel of the previous word. The consonant is a natural attention reset. Cutting on a trailing vowel ("eeeasy...") sounds spliced; cutting on "Watch" or "Build" sounds intentional.

### G. Caption decisions

**17. One keyword per phrase, not per sentence**
Highlight the single noun or verb that carries the semantic weight of each 3–6 word phrase. Not the adjective, not the connector word. If the phrase is "I built a full WhatsApp system," highlight "WhatsApp" or "built" — not "full" or "system" alone.

Source: Ascynd/Hormozi captions analysis — "one word per phrase is the rule."

**18. What to highlight**
- Promise words: "free", "fast", "10X", "in minutes"
- Contrast words: "but", "instead", "here's the trick"
- Specificity: numbers, outcomes, proper nouns (product names, platform names)
- Stakes: "wasting", "losing", "never"

What NOT to highlight: "the", "and", "like", "just", "really", function words, repeated emphasis on every line (defeats the purpose).

**19. Caption timing precision: 100ms word-level accuracy required**
Word-level timestamps must be accurate within 100ms. Words appearing before they are spoken destroy the karaoke effect and look amateur. Verify this in the export by watching at 0.5x speed in the first 5 seconds.

Source: canvasub.com — "Word-level timestamps need to be accurate within 100ms."

### H. Self-edit critique technique

**20. The audio-off test (primary diagnostic)**
Export the cut. Mute your speakers. Watch it. Can you follow the story purely from the visuals and captions? If not, the edit is leaning on audio to compensate for weak visual sequencing. Hitchcock's test: "If it's a good cut, the sound could go off, and the audience would still have a perfectly clear idea of what was going on."

Source: Film Editing Pro — this is the "granddaddy" technique.

**21. The black-and-white test (energy diagnostic)**
Remove color (apply a desaturation effect in your editor). Watch again. Does the energy structure still feel like it builds and peaks? If everything feels equally dull in B&W, the edit has no visual energy hierarchy. The highest-energy segment should feel visually busiest even without color.

Source: Joe Walker (Dune editor) via joelv.ca.

**22. The 3-view rule (stale-eyes detection)**
If on the third full viewing a segment feels less compelling than it did the first time, cut it. Your audience sees it once, with fresh eyes. If repeated viewing degrades your own enthusiasm, it will fail to hold a stranger.

Source: Rachel Corbett podcast editing guide: "if on the third time something isn't as compelling as it was when you listened to it the first time, cut it out."

**23. The stranger test**
Watch your cut with someone who has not seen the raw material. Do not tell them what to look for. Watch their face, not the screen. The moments they zone out, check their phone, or stop reacting are your re-cut targets. This is more valuable than any analytics you can collect before publishing.

Source: joelv.ca — "Watching the cut with someone else beside you is watching the cut with fresh eyes."

---

## How to Apply

### Pre-cut prep checklist

- [ ] Read the full transcript of all clips. Do not start cutting without reading first.
- [ ] Score each sentence: New info (0–3) + Energy (0–3) + Clarity (0–3) + Memorability (0–3)
- [ ] Mark the highest-scoring sentence across all clips — that is your hook candidate
- [ ] Mark the highest-energy moment — that is your peak candidate (usually a demo reveal or surprising outcome)
- [ ] Check: does the hook open a loop that the peak closes? If not, restructure.
- [ ] Decide target duration before touching the timeline: 20–35s for maximum platform performance, 45s absolute max

### During-cut checklist

- [ ] Place hook first even if it appeared in the middle of a take
- [ ] Trim all pauses between sentences to 150–200ms maximum
- [ ] Cut every sentence that only restates (does not advance)
- [ ] Cut every "um", "uh", and sentence-opening "so" or "you know" that adds nothing
- [ ] Check energy curve: count seconds between each cut point — should decrease as you approach the peak
- [ ] Ensure no segment runs >8s without a visual change (cut, zoom, text overlay, B-roll)
- [ ] L-cut into screen recordings: let the voice start ~500ms before the visual cut
- [ ] Check join between segments: add ~200ms room tone if the cut sounds robotic

### Post-cut review checklist

- [ ] Watch 1: full play with audio — note any moment of boredom (timestamp it)
- [ ] Watch 2: audio off — can you follow the story from visuals + captions alone?
- [ ] Watch 3: black and white — does energy structure still read?
- [ ] Fix any segment that failed the stale-eyes test (see principle 22)
- [ ] Verify captions: word-level timing accurate within 100ms in first 5s
- [ ] Verify highlight keywords: one per phrase, semantic-weight words only
- [ ] Check retention curve targets: hook sentence delivered by 1.5s, peak no later than 25s in a 35s cut

---

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Cutting to hit a duration target | Produces mechanical removal of good content. Duration is an outcome, not a goal. |
| Cutting all pauses uniformly | Destroys emphasis. Some pauses convey meaning. Cutting the breath after "It's currently happening" removes the speaker's belief signal. |
| Leaving all restatements because "it might add context" | Restatements are retention killers. The viewer already has the information. Restating it insults their attention. |
| Starting with the first sentence as the hook | The best sentence is almost never the first one. Scan the full transcript first. |
| Using the same cut frequency throughout | Flat pacing = no energy curve = no peak = no rewatches. The algorithm optimizes for completion; completion requires a peak to push toward. |
| Removing all fillers to sound "professional" | Over-cleaned dialogue sounds assembled, not spoken. Trust signals in personal brand video include some natural speech texture. |
| Highlighting every third word in captions | Highlighting everything = highlighting nothing. One keyword per phrase is the rule. |
| Never watching with fresh eyes | You have seen the raw material 20 times. Your audience sees it once. Post-edit, you cannot judge pacing without the audio-off or stranger test. |
| Hard cuts between segments with no room tone | Produces audible pops and robotic joins. 200ms of ambient tone between segments makes cuts invisible. |
| Applying a 3-second delay before the hook lands | If the first sentence is "so today I want to talk about..." the viewer is gone. The hook must land in the first frame of speech. |

---

## Clip Analysis: Weblyfe 2026-05-03

### What happened in v1

**Total cut: 49.6 seconds across 6 segments from 5 source clips (70.4s raw total used).**

The source clips had:
- clip-01 (4.2s): 2 sentences, both kept as hook
- clip-02 (36.0s): 8 sentences; 4 kept, 4 cut
- clip-03 (11.3s): 5 sentences; all 5 kept as one segment
- clip-04 (10.9s): 4 sentences; all 4 kept as CTA
- clip-05 (9.0s): 3 sentences; all 3 kept as vision

### Cut-point evaluation

**Hook (seg-01, 3.6s):**
"Oh, but say it, how is AI gonna make your work easier? Watch this."
CORRECT hook structure. Opens a loop ("Watch this"), delivers in ≤3.6s, strong action verb. One issue: "Oh, but say it" is a mid-conversation connector — the "Oh" sounds mid-stream. Better hook trim: start at "How is AI gonna make your work easier? Watch this." — 2.3s, cleaner entry.

**seg-02 proof (0.0–8.7s of clip-02, 8.7s):**
Kept: "In just a few hours talking to my AI agents I'm able to build several different systems. One including a full WhatsApp messaging system using the Facebook API and whatnot."
CORRECT: establishes scope and gives a concrete proof item. The word "whatnot" is a filler ending — could trim the last 0.3s.

**What v1 cut from clip-02 (sentences 3–5, 12.6s):**
- "A full funnel including making the leads appear inside of the Monday system" (9.1–15.7s, 6.6s) — CUT
- "Thank you page, checkout page, you name it, all of it" (15.7–18.9s, 3.2s) — CUT  
- "Even the screenshots and the mockups are all made by my AI" (19.0–21.8s, 2.8s) — CUT

The Monday funnel sentence and the "thank you page / checkout page" sentence are list enumeration that restates the same idea (AI built the funnel). Correct cut. However: "Even the screenshots and mockups are all made by my AI" (19–21.8s) is NEW information — AI doing design work is a separate, surprising claim. This was the strongest proof item and it was discarded. This is a v1 error.

**seg-03 (cherry on top / translate, 9.1s):**
Jumped directly to "And the cherry on top, the weblife.ai website..." This is a structural cut from 8.7s to 22.2s — a 13.5s gap in the original timeline. The result: the "cherry on top" framing lands correctly as an escalation, but the audience lost the screenshots/mockups proof that would have built momentum into it. The energy plateau in the middle of the final video corresponds to this gap.

**seg-04 (demo, clip-03, 10.1s):**
Kept all 5 sentences of clip-03, including: "The instant Appies are coming soon" (2.46–4.0s, 1.5s) which is a product announcement with no completed payoff for the viewer, and "But here you will see a little bit more" (4.08–5.46s) which is a low-information connector. These two sentences (3.0s combined) could be cut, tightening seg-04 to 7.1s.

**seg-05 (vision, clip-05, 8.1s):**
"I think AI employees for 10X your productivity is not the future talk anymore. It's currently happening. And the sooner you get into it, the more..."
The 200ms pause between "happening." and "And" (correctly left in) is good — it is an emphasis pause. But the segment cuts mid-sentence at "the more..." — the audience is left hanging on an incomplete thought. The CTA (seg-06) follows from a completely different clip in Dutch, making this a language-switch non-sequitur. The vision statement should either be completed ("the more advantages you'll see" from clip-05's transcript) or the CTA segment should bridge the language switch.

**seg-06 (CTA, clip-04, 10.1s):**
Dutch CTA following English content. The language switch here is jarring because there is no bridging visual or text explaining the switch. Additionally, the 0.94s gap in words.json between "well" (41.87s) and "and" (42.81s) was left in — that is a 940ms pause that should have been cut to 150–200ms. This is the clearest timing error in the v1 edit.

### Prescribed re-cuts

1. **Hook**: trim opening "Oh, but say it," — start at "How is AI gonna make your work easier?" — saves 1.3s, sharpens entry
2. **Restore the screenshots/mockups sentence** (clip-02 19.0–21.8s) — this is new information and the strongest visual proof of AI design capability
3. **Cut seg-04 first two sentences**: "The instant Appies are coming soon" + "But here you will see a little bit more" — remove 3s of low-information content
4. **Complete the vision sentence** in seg-05: add "the more advantages you see" to close the hanging "the more..."
5. **Cut the 940ms gap in seg-06** between "well" and "and" — trim to 150ms

These 5 changes would reduce total runtime from 49.6s → ~44s and fix the two most retention-damaging moments: the incomplete vision sentence and the 940ms dead pause in the CTA.

---

## Cross-skill references

- `appie-video-production`: production workflow, shot setup, normalization commands
- `thumbnails`: thumbnail selection criteria (strongest frame, not prettiest frame)
- `social-media`: per-platform duration norms and caption format requirements
- `seo-bezoekersmagneet`: same "first impressions compound" principle applies to hook optimization

---

## Motion Graphics with Remotion

Codified 2026-05-03. Brand: Weblyfe — Rethink Sans, #DFB771 gold, #247459 teal, #031D16 dark, #F6FEFC light.

### A. Repos to study

| Repo | URL | What to steal |
|---|---|---|
| remotion-dev/template-tiktok | https://github.com/remotion-dev/template-tiktok | `@remotion/install-whisper-cpp` pipeline: `transcribe()` → `toCaptions()` → JSON; `SubtitlePage.tsx` spring entry pattern (damping 200, durationInFrames 5) |
| reactvideoeditor/remotion-templates | https://github.com/reactvideoeditor/remotion-templates | 81 components MIT-licensed; steal: ScalePop (text entrance), WordHighlighting, CameraShake, KenBurns, WhipPan, ZoomPulse |
| gyoridavid/short-video-maker | https://github.com/gyoridavid/short-video-maker | Remotion v4.0.286 scaffold, MCP interface, working `@remotion/captions` + `@remotion/transitions` integration |
| dojocodinglabs/remotion-superpowers | https://github.com/dojocodinglabs/remotion-superpowers | `@remotion/light-leaks` + film grain + vignette patterns; `@remotion/three` for 3D intro if needed |
| ahgsql/remotion-subtitles | https://github.com/ahgsql/remotion-subtitles | SRT import → animated subtitle component (fallback if whisper pipeline not set up yet) |

---

### B. Visual hook recipe — Scale-punch with mask reveal (0–2.3s)

Chosen pattern: text SCALE-PUNCH + background color flash + word appears from below. Best for Weblyfe: brand-aligned, no VFX software, pure CSS/spring.

```tsx
// src/components/Hook.tsx
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const Hook: React.FC<{ line: string }> = ({ line }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Flash: dark bg → brand gold in first 4 frames
  const bgOpacity = interpolate(frame, [0, 4, 8], [1, 0.6, 0], { extrapolateRight: 'clamp' });

  // Text entrance: springs up from translateY(40px) + scale 0.82 → 1
  const enter = spring({ frame, fps, config: { damping: 14, mass: 0.6 }, durationInFrames: 18 });
  const scale  = interpolate(enter, [0, 1], [0.82, 1]);
  const translateY = interpolate(enter, [0, 1], [40, 0]);

  // Overshoot punch: peak scale 1.08 at frame 10, settles to 1
  const punch = spring({ frame: frame - 10, fps, config: { damping: 8, mass: 0.4 }, durationInFrames: 12 });
  const punchScale = frame >= 10 ? interpolate(punch, [0, 1], [1.08, 1]) : 1;

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', backgroundColor: '#031D16' }}>
      {/* Flash overlay */}
      <AbsoluteFill style={{ backgroundColor: '#DFB771', opacity: bgOpacity }} />
      <div style={{
        transform: `translateY(${translateY}px) scale(${scale * punchScale})`,
        fontFamily: 'Rethink Sans',
        fontWeight: 900,
        fontSize: 108,
        color: '#F6FEFC',
        textAlign: 'center',
        textTransform: 'uppercase',
        lineHeight: 1.05,
        letterSpacing: '-2px',
        padding: '0 60px',
      }}>
        {line}
      </div>
    </AbsoluteFill>
  );
};
```

---

### C. Caption animation — Hormozi word-pop with brand highlight

```tsx
// src/components/CaptionLine.tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface Token { text: string; fromMs: number; toMs: number; }

export const CaptionLine: React.FC<{ tokens: Token[]; timeMs: number; isKeyword: (t: string) => boolean }> = ({
  tokens, timeMs, isKeyword
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{
      display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 10px',
      fontFamily: 'Rethink Sans', fontWeight: 700, fontSize: 88,
      textAlign: 'center', padding: '0 60px',
    }}>
      {tokens.map((token, i) => {
        const isActive = timeMs >= token.fromMs && timeMs < token.toMs;
        const framesSinceActive = Math.max(0, frame - Math.round((token.fromMs / 1000) * fps));

        // Bounce entrance when word becomes active
        const bounce = spring({
          frame: isActive ? framesSinceActive : 0,
          fps,
          config: { damping: 10, mass: 0.5 }, // snappy TikTok feel
          durationInFrames: 8,
        });
        const wordScale = isActive ? interpolate(bounce, [0, 1], [0.85, 1]) : 1;

        const highlight = isKeyword(token.text);

        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              transform: `scale(${wordScale})`,
              transformOrigin: 'bottom center',
              color: isActive && highlight ? '#DFB771'   // brand gold for active keyword
                   : isActive             ? '#F6FEFC'   // white for active non-keyword
                   : '#F6FEFC99',                        // dimmed for inactive
              textShadow: isActive && highlight
                ? '0 0 20px #DFB77180'
                : 'none',
              textTransform: 'uppercase',
              lineHeight: 1.1,
              // Karaoke fill: teal underline on active
              borderBottom: isActive ? '6px solid #247459' : '6px solid transparent',
              paddingBottom: '4px',
            }}
          >
            {token.text}
          </span>
        );
      })}
    </div>
  );
};

// Keyword detection — pass into isKeyword prop:
// const KEYWORDS = new Set(['AI','WhatsApp','FREE','built','10X','funnel','seconds','minutes']);
// isKeyword={(t) => KEYWORDS.has(t.toUpperCase())}
```

Spring config summary:
- Active word entrance: `damping: 10, mass: 0.5` — snappy, Captions.ai feel
- Hook text entrance: `damping: 14, mass: 0.6` — slightly slower, more weight
- Page-level entrance (from template-tiktok): `damping: 200, durationInFrames: 5` — near-instant snap

---

### D. Font + color stack

Load via `@remotion/google-fonts`:

```tsx
import { loadFont } from '@remotion/google-fonts/RethinkSans';

const { fontFamily } = loadFont('normal', {
  weights: ['400', '700', '900'],
  subsets: ['latin'],
});
// fontFamily → 'Rethink Sans' — use in all style objects
```

| Element | Weight | Size (1080×1920) | Color |
|---|---|---|---|
| Hook line (0-2s) | 900 Black | 108px | #F6FEFC |
| Active caption word | 700 Bold | 88px | #F6FEFC / #DFB771 highlight |
| Inactive caption word | 700 Bold | 88px | #F6FEFC at 60% opacity |
| Keyword callout (solo) | 900 Black | 110px | #DFB771 |
| Body sub-caption | 700 Bold | 72px | #F6FEFC |
| Trust micro-copy / CTA | 400 Regular | 52px | #247459 or #F6FEFC80 |
| Lower third label | 700 Bold | 44px | #DFB771 |

Safe zones: 150px top, 170px bottom, 60px sides minimum.

Colors:
```
GOLD    #DFB771   keyword highlight, logo, CTA button
TEAL    #247459   underline, micro-copy, accent
DARK    #031D16   background, behind captions
LIGHT   #F6FEFC   primary text
```

---

### E. SFX library

**Pick: Mixkit** — https://mixkit.co/free-sound-effects/
No signup, royalty-free commercial use, WAV+MP3 direct download.

| Event | Sound type | Mixkit category path |
|---|---|---|
| Hook text appears (0s) | Impact/whoosh | /free-sound-effects/transition/ → "Whoosh" |
| Caption word active | Pop/click | /free-sound-effects/misc/ → "Pop" |
| Soft riser under hook | Riser/atmosphere | /free-sound-effects/transition/ → "Swoosh" (slow) |
| CTA reveal (drop) | Impact sting | /free-sound-effects/technology/ → "Ding" or "Notification" |
| UI tick/blip | Click | /free-sound-effects/technology/ → "Click" |

Download batch:
```bash
# Mixkit direct-download (replace slug with exact filename from site):
curl -L "https://cdn.mixkit.co/sfx/download/mixkit-fast-small-sweep-transition-166.wav" -o sfx/whoosh-1.wav
curl -L "https://cdn.mixkit.co/sfx/download/mixkit-pop-up-notification-221.wav" -o sfx/pop-word.wav
curl -L "https://cdn.mixkit.co/sfx/download/mixkit-long-pop-2358.wav" -o sfx/cta-drop.wav
```

No npm package for SFX is needed — `<Audio src={staticFile('sfx/whoosh-1.wav')} />` in Remotion is sufficient. Place all files in `public/sfx/`.

Audio mixing in Remotion:
```tsx
// Duck voice track when SFX fires
<Audio src={staticFile('voice.mp3')} volume={(f) =>
  interpolate(f, [hookFrame, hookFrame+8], [1, 0.4], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
} />
<Audio src={staticFile('sfx/whoosh-1.wav')} startFrom={hookFrame} volume={0.7} />
```

---

### F. Composition structure — 6-beat 50-60s reel

At 30fps. Adjust beat offsets to match actual clip durations.

```tsx
// src/compositions/Reel.tsx
import { Composition, Sequence } from 'remotion';

// Beat timing (frames at 30fps):
const BEATS = {
  hook:    { from: 0,   dur: 69  }, // 0–2.3s  — Hook component
  proof1:  { from: 69,  dur: 120 }, // 2.3–6.3s — caption + B-roll 1
  proof2:  { from: 189, dur: 120 }, // 6.3–10.3s — caption + B-roll 2
  demo:    { from: 309, dur: 300 }, // 10.3–20.3s — screen recording / OffthreadVideo
  vision:  { from: 609, dur: 180 }, // 20.3–26.3s — talking head + caption
  cta:     { from: 789, dur: 210 }, // 26.3–33.3s — CTA overlay + SFX drop
};
// Total: ~1050 frames / 35s (scale up proportionally for 50-60s)

export const Reel = () => (
  <>
    <Sequence from={BEATS.hook.from} durationInFrames={BEATS.hook.dur}>
      <Hook line="HOW IS AI GONNA MAKE YOUR WORK EASIER?" />
      <Audio src={staticFile('sfx/whoosh-1.wav')} volume={0.65} />
    </Sequence>

    <Sequence from={BEATS.proof1.from} durationInFrames={BEATS.proof1.dur}>
      <OffthreadVideo src={staticFile('clips/clip-02-proof.mp4')} />
      <AbsoluteFill style={{ justifyContent: 'flex-end', paddingBottom: 170 }}>
        <CaptionLine tokens={proof1Tokens} timeMs={...} isKeyword={isKeyword} />
      </AbsoluteFill>
    </Sequence>

    {/* demo beat */}
    <Sequence from={BEATS.demo.from} durationInFrames={BEATS.demo.dur}>
      <OffthreadVideo src={staticFile('clips/clip-03-demo.mp4')} />
      <AbsoluteFill style={{ bottom: 170, position: 'absolute' }}>
        <CaptionLine tokens={demoTokens} timeMs={...} isKeyword={isKeyword} />
      </AbsoluteFill>
    </Sequence>

    {/* CTA drop SFX */}
    <Sequence from={BEATS.cta.from} durationInFrames={BEATS.cta.dur}>
      <CTAOverlay />
      <Audio src={staticFile('sfx/cta-drop.wav')} volume={0.8} />
    </Sequence>

    {/* Background voice track — always present, ducked at SFX moments */}
    <Audio src={staticFile('voice-mixed.mp3')}
      volume={(f) => interpolate(f, [0, 5, BEATS.hook.dur, BEATS.hook.dur+8], [0, 1, 1, 0.5],
        { extrapolateRight: 'clamp' })}
    />
  </>
);
```

`<OffthreadVideo>` notes:
- Input: H.264 MP4 at source fps is fine. No ProRes needed for input.
- If source fps != composition fps (30), pre-convert: `ffmpeg -i input.mp4 -r 30 -c:v libx264 -crf 18 output.mp4`
- OffthreadVideo has a built-in frame cache (default = 50% system RAM). For a Mac Mini M2 16GB, that is ~8GB — enough for a 60s reel.

---

### G. Render command

```bash
# Caption generation (run once per voice track):
node scripts/transcribe.mjs  # uses @remotion/install-whisper-cpp, outputs captions.json

# Render — Mac Mini M2, 1080x1920, 30fps, 50-60s:
npx remotion render src/index.ts Reel out/reel-v2.mp4 \
  --codec h264 \
  --crf 16 \
  --concurrency 10 \
  --pixel-format yuv420p \
  --image-format jpeg \
  --jpeg-quality 95

# Benchmark first to find optimal concurrency:
npx remotion benchmark src/index.ts Reel --concurrency-levels 4,8,10,12
# M2 has 8 performance cores; 10 is empirically fast without starving the system
```

Expected render time at `--concurrency 10`, CRF 16, JPEG frames: ~3-4 min for 60s at 1080x1920 on M2.

---

### H. Anti-patterns (what makes a Remotion reel look cheap)

| Anti-pattern | Fix |
|---|---|
| CSS `transition:` or `animation:` properties | Forbidden — silently fails to render. Use `interpolate()` + `spring()` only. |
| Default Inter/system font | Always load brand font via `@remotion/google-fonts` before any component renders. |
| All words same size throughout caption | Only active word gets scale bounce; inactive words stay at 1. Over-animating every word = visual noise. |
| `easeInOutCubic` on text entrances | Too smooth → looks like a slideshow. Use spring with damping 10-14 for organic bounce. |
| Simultaneous animations on 3+ layers | Stagger by 3-6 frames minimum between text, background, and icon entrances. |
| Caption text near edges | Minimum 60px side margin, 170px bottom margin. Sub-60px font looks unreadable on phone. |
| Hard audio cuts (no ducking) | Always volume-curve `<Audio>` — ramp in over 5 frames, never start at full volume on frame 0. |
| No safe-zone padding | All text within 150px top, 170px bottom, 60px sides — platform UI covers edges. |
| Over-highlighting captions | Max 1 keyword per phrase. Never highlight "the", "and", connectors. |
| Rendering to VP8/VP9 | Very slow encoder, no benefit for deliverables. Use H.264 CRF 16. |

---

### I. Captions pipeline (whisper → Remotion tokens)

```bash
# Install once:
npx @remotion/install-whisper-cpp install --version 1.5.5
npx @remotion/install-whisper-cpp download-model medium.en
```

```ts
// scripts/transcribe.mjs
import { transcribe, toCaptions } from '@remotion/install-whisper-cpp';
import { writeFileSync } from 'fs';

const { transcription } = await transcribe({
  model: 'medium.en',
  whisperPath: '.whisper-cpp',
  whisperCppVersion: '1.5.5',
  inputPath: 'public/voice-mixed.wav',  // must be WAV
  tokenLevelTimestamps: true,
});

const captions = toCaptions({ transcription });
writeFileSync('src/captions.json', JSON.stringify(captions, null, 2));
```

Then in the component, import `captions.json` and use `createTikTokStyleCaptions()` from `@remotion/captions` to group tokens into pages with `combineTokensWithinMilliseconds: 300` (one page every ~300ms, 2-4 words per page).
