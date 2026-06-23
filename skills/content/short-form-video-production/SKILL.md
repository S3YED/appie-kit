---
name: short-form-video-production
description: "Use when producing short-form video end to end: idea selection, hook and retention structure, sentence-level edit decisions, captions, thumbnails/first-frame communication, Remotion or FFmpeg implementation, and Appie/Weblyfe production workflows."
---

# Short-Form Video Production

Umbrella skill for Reels, Shorts, and TikTok production. Prefer this over separate micro-skills for ideation, editing, thumbnails, Remotion notes, or one project-specific production pass.

## End-to-end workflow
1. Choose the concept and the audience-specific promise.
2. Design the first frame and hook before polishing the middle.
3. Build an open loop and delay the payoff.
4. Cut at the sentence level for clarity, novelty, and energy.
5. Add captions, visual changes, and audio transitions.
6. Verify the first frame, the 3-second hook, and the abrupt ending.
7. Export, review muted, and deliver the correct file format.

## Core sections
### Ideation and retention
- Hook first, payoff later.
- Use clear audience targeting and 5th-grade readability when scripting.
- Structure around hook -> foreshadow -> tension -> payoff -> abrupt end.

### Editing decisions
- Keep only sentences that advance the story, prove the claim, or deliver payoff.
- Trim transitional filler and long dead pauses.
- Preserve emphasis pauses that carry meaning.
- Ensure a visual change at least every 5-8 seconds.

### Captions and motion
- Highlight one meaning-bearing word per phrase.
- Verify word timing tightly.
- Use motion as emphasis, not constant noise.

### Thumbnails and first-frame design
- First frame must communicate the concept on mute.
- Face, contrast, and 3-5 word text are usually enough.
- Design for mobile legibility and safe zones.
- For vertical reels, compose natively in 9:16 from the start.
- When the opener is the main hook, generate or revise the opener before polishing downstream scenes.

### Tooling and implementation
- FFmpeg for extraction, normalization, stitching, muxing, and quick probes.
- Remotion for programmable compositions, caption animation, and reusable branded systems.
- HyperFrames for HTML-native, agent-friendly editing pipelines for deterministic social-video renders.
- Submagic API for polished captions, hook titles, AI B-roll, and Magic Clips.
- Vizard API for clip/edit automation and multi-format outputs.
- Use commercial APIs first for speed and reliability. Use OSS tools only after secure vetting.

### Verification checklist
- [ ] First frame communicates the concept without sound
- [ ] Hook lands in the first 1.5-3 seconds
- [ ] Payoff is delayed, then delivered cleanly
- [ ] No obvious dead pauses or redundant sentences remain
- [ ] Captions and export format match the delivery platform
- [ ] Final MP4 is stored outside /tmp or copied to a persistent path before delivery
- [ ] If likeness matters, the opener matches the user's provided photo/reference
- [ ] If the user asked for oversight, a review bundle was delivered before continuing to animation
- [ ] Sound design / narration plan is included when the task is a reel or short-form video