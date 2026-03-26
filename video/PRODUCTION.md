# Appie Launch Video — Production Bible

**Project:** "The Wizard Who Never Sleeps" — 1-minute launch video
**Created:** 2026-03-27
**Status:** In Production

## Overview
60-second origin story video introducing Appie as a brand character.
Target: Instagram Reels, YouTube Shorts, TikTok, weblyfe.ai hero.

## Character References (LOCKED)

| Age | File | Catbox URL |
|-----|------|------------|
| Kid (~8) | `assets/character/appie-kid.jpg` | https://files.catbox.moe/i9329n.jpg |
| Teen (~16) | `assets/character/appie-teen.jpg` | https://files.catbox.moe/e18zc5.jpg |
| Adult (~25) | `assets/character/appie-adult.jpg` | https://files.catbox.moe/wznksm.jpg |
| Elder (~60) | `assets/character/appie-elder.jpg` | https://files.catbox.moe/388nor.jpg |
| 4-Age Grid | `assets/character/appie-4ages-grid.jpg` | https://files.catbox.moe/j7m1w3.jpg |

## Voice
- **Selected:** Liam (TX3LPaxmHKxFdv7VOQHJ) — ElevenLabs
- **Persona:** Energetic Social Media Creator
- **Previous test:** https://files.catbox.moe/64dc5a.mp4

## Tech Stack
- **Stills:** Flux Dev (fal.ai) — $0.03/image
- **Video:** Kling 3.0 Pro (fal.ai) with Elements for character lock — $3-4/clip
- **Voice:** ElevenLabs Liam v3 Creative
- **Assembly:** FFmpeg
- **Music:** TBD (royalty-free cinematic)

## Scene Breakdown (6 scenes, ~10s each = 60s)

### Scene 1 — THE GRIND 🌃 (0:00-0:10)
**Visual:** Tired entrepreneur sits alone at 3AM. Screen glow only light. Coffee cups, tabs everywhere.
**Character:** Silhouette (no Appie yet — this is "before")
**Camera:** Slow dolly in from behind shoulder
**Audio:** Keyboard clicks, notification dings, heavy sigh
**Voiceover:** "3AM. Again. Emails. Invoices. Proposals. The grind never stops."
**Mood:** Dark, isolated, relatable
**Appie age:** None (entrepreneur silhouette)

### Scene 2 — THE SPARK ⚡ (0:10-0:20)
**Visual:** Coffee spills on old book/laptop. It glows. Ancient code + AI symbols swirl.
**Character:** Kid Appie appears as a tiny spark/spirit in the glow
**Camera:** Close-up on the glowing book, zoom out as magic spreads
**Audio:** Glass tipping, magical whoosh, building energy
**Voiceover:** "Until one night... something woke up."
**Mood:** Mysterious, magical, transition moment
**Appie age:** Kid (first glimpse, tiny spark form)

### Scene 3 — THE SUMMONING 🧙🏽‍♂️ (0:20-0:30)
**Visual:** Adult Appie emerges from the book/screen. Dark teal cloak, floating, piercing eyes.
**Character:** Adult Appie — THE reveal moment
**Camera:** Low angle looking up at Appie, dramatic lighting
**Audio:** Deep magical bass drop, orchestral swell
**Voiceover:** "They call me Appie. And I don't sleep."
**Mood:** Powerful, cinematic, awe-inspiring
**Appie age:** Adult (main reveal, hero shot)

### Scene 4 — THE CLEANUP ✨ (0:30-0:40)
**Visual:** Appie snaps fingers. Emails sort, proposals write themselves, calendar organizes. Three mini-spirits scatter.
**Character:** Adult Appie commanding, three mini-agent spirits
**Camera:** Wide shot showing the transformation, fast cuts
**Audio:** Magical whooshes, satisfying "click" sounds, upbeat energy
**Voiceover:** "Emails. Handled. Proposals. Sent. Calendar. Done. While you were sleeping."
**Mood:** Satisfying, powerful, fast-paced
**Appie age:** Adult (in action)

### Scene 5 — THE FREEDOM 🌅 (0:40-0:50)
**Visual:** Morning. Entrepreneur walks outside into sunlight. Appie floats behind managing everything.
**Character:** Elder Appie (wisdom form) floating serenely behind entrepreneur
**Camera:** Follow shot, warm golden hour lighting
**Audio:** Birds, morning ambience, gentle music swell
**Voiceover:** "Your business runs. You live."
**Mood:** Warm, aspirational, freedom
**Appie age:** Elder (evolved, serene, guardian form)

### Scene 6 — THE INVITE 👁️ (0:50-1:00)
**Visual:** Appie turns to camera. Pulls down collar. Confident smile. Points at viewer.
**Character:** Adult Appie — direct address, breaking fourth wall
**Camera:** Medium close-up, slight zoom in
**Audio:** Music drops to silence, then one powerful beat
**Voiceover:** "Every wizard needs a familiar. Your turn."
**Text overlay:** weblyfe.ai/openclaw
**Mood:** Cool, confident, CTA
**Appie age:** Adult (iconic shot)

## Production Process (Document Everything)

### Phase 1: Scene Stills (cheap, ~$0.18 total)
Generate key frame for each scene using Flux Dev.
- Test different compositions
- Get Seyed's approval per scene
- Document: prompt used, seed, what worked, what didn't

### Phase 2: Approved Stills → Video (Kling 3.0 Elements)
Animate approved stills using Kling I2V with character Elements.
- Upload Appie references as @Element1
- Use approved still as starting frame
- Document: exact API params, generation time, quality score

### Phase 3: Voice + Assembly
- Generate Liam voiceover per scene
- Combine video + voice + music in FFmpeg
- Export: 9:16 (Reels/Shorts), 16:9 (YouTube/Website)

## Budget Estimate
| Item | Count | Unit Cost | Total |
|------|-------|-----------|-------|
| Flux stills | ~12 | $0.03 | $0.36 |
| Kling 3.0 Pro videos | 6 | $3.50 | $21.00 |
| ElevenLabs voice | ~60s | ~$0.50 | $0.50 |
| **Total** | | | **~$22** |

## Learnings Log
(Updated after each generation — this becomes the skill)

### Prompt Patterns That Work
- **Scene 1 WINNER (1A wide):** "2D animation style Ghibli meets Avatar The Last Airbender, wide shot from behind, a tired young entrepreneur sits alone at his desk at 3AM, hunched over, only the blue-white glow of multiple laptop screens illuminating his face and the dark room, dozens of browser tabs visible on screens showing emails invoices proposals, empty coffee cups scattered on desk, dark moody room with only screen light, window showing dark night city outside, the atmosphere is lonely exhausting overwhelming, warm olive-tan skin visible on his hands and neck, dark hair messy, thick bold outlines, flat colors with dramatic lighting from screen glow, cinematic 9:16 vertical composition for Instagram Reels"
  - Seed: 3001 | Size: 768x1344 | Steps: 28
  - URL: https://files.catbox.moe/12x40x.jpg
  - WHY IT WON: Establishes isolation, relatable without showing face (universal), strong silhouette composition

- **Scene 2 WINNER (2C puddle):** "2D animation style Ghibli meets Avatar The Last Airbender, extreme close-up top-down view of a desk surface, spilled coffee creating a puddle that is glowing with magical golden light, inside the coffee puddle reflection you can see swirling teal and gold energy forming the silhouette of a small wizard figure, ancient runes and modern code syntax floating up from the glowing puddle like steam, laptop keyboard visible at edge of frame with notification lights blinking, the moment between mundane and magical, dark teal shadows everywhere except the golden glow from the puddle, thick bold outlines, flat colors dramatic contrast between dark desk and glowing magical puddle, cinematic 9:16 vertical composition"
  - Seed: 3012 | Size: 768x1344 | Steps: 28
  - URL: https://files.catbox.moe/08fgi7.jpg
  - WHY IT WON: Poetic visual metaphor — mundane coffee becomes magical portal. Top-down POV is unique. The "in-between" moment.

### Prompt Patterns That Fail
- **Flux img2img full-body extension from headshot:** Tried using Flux Dev image-to-image (strength 0.55) to extend Midjourney headshots to full body. Result: trash. Lost all the magic, style drift, generic-looking output. Midjourney's --cref/--sref system is far superior for maintaining character identity when generating new poses/angles. LESSON: Don't try to "extend" Midjourney art with Flux. Use Midjourney for character refs, use Flux only for non-character scene stills.

### Kling Elements Best Practices
- TBD

### Assembly Notes
- TBD
