---
name: content-production-workflow
description: End-to-end workflow for creative review gates, content drafting, and publishing to blogs, Notion, and social channels with explicit approval checkpoints.
---

# Content Production Workflow

Use this skill for content work that needs both a clear approval gate and a reliable publishing path. It covers short-form creative review packs, blog/article drafting, and platform-specific publishing checks.

## When to use
- The user wants a review pack before final production or publication.
- You are drafting, refining, or publishing content for a brand or publication.
- The work needs a pause point for human curation before expensive downstream steps.
- You need to keep approved anchors stable while iterating on nearby details.

## Core workflow
1. **Clarify the content target.**
   - Identify the format, audience, channel, and success criterion.
   - Separate locked canon from flexible draft material.

2. **Build a reviewable draft first.**
   - For creative assets: script, beat list, keyframes, CTA notes.
   - For articles: outline, thesis, draft body, sources, and distribution variants.

3. **Make the approval boundary explicit.**
   - Say what is locked.
   - Say what the user can change.
   - Say what will not proceed until approval arrives.

4. **Pause at the gate.**
   - Do not continue into animation, bulk generation, final packaging, or publishing until the approved state is clear.

5. **Resume from the approved state only.**
   - If the user changes one part, adjust the smallest adjacent pieces and re-present the updated pack or draft.

6. **Publish with verification.**
   - Sanity-check links, titles, formatting, and destination state.
   - After publishing, verify the page or post actually exists and matches the intended content.

## Review-gate subsection
Use this when producing reels, ads, storyboards, or other assets that need user curation before final production.

### Review pack contents
- Clear title and goal
- Short script or narration draft
- Frame list with IDs and one-line purpose
- Aspect-ratio callout when relevant
- Canonical design constraints
- CTA or end-card direction
- Direct question to the user about what to change, keep, or approve

### Review-gate pitfalls
- Do not silently continue after the user asked for curation.
- Do not bury the approval request in a long explanation.
- Do not regenerate everything when only one frame or line needs review.
- Do not mix draft, approved, and pending assets without labels.

## Publishing subsection
Use this when creating blog posts, updating editorial content, or publishing into a CMS or knowledge base.

### Publishing workflow
- Prefer concrete market signals, internal learnings, and practical value over filler.
- Draft in the brand voice requested by the user.
- Add sources, backlinks, or citations when they strengthen trust.
- Verify title, formatting, and destination content after publishing.

### Weblyfe-specific notes
- Write in English unless the user explicitly asks for another language.
- Avoid em dashes.
- Keep tone human, specific, and useful.
- For LinkedIn derivatives, keep the structure compact: hook, concrete founder/operator details, one clear thesis, simple CTA if needed, and 3-5 hashtags.
- When Seyed says to prevent AI speech, run an explicit anti-AI pass: remove common AI words and structures such as "delve into", "at its core", "pivotal", "underscore", "harness", "realm", "that being said", "to put it simply", generic significance language, corporate filler, over-tidy transitions, rule-of-three padding, and robotic upbeat endings. Prefer direct wording, lived details, varied rhythm, and Seyed's natural founder/operator voice.
- For Weblyfe blog publication checks and LinkedIn publishing with generated images, use `references/weblyfe-linkedin-and-blog-publishing-checks.md`.
- For premium launch films or carousel-to-video work, use `references/premium-launch-film-styleframes.md`: styleframe gate first, one metaphor, readable proof modules, mascot integrated not pasted.
- Sanitize markdown links before sending rich-text blocks to Notion.
- After publishing, verify the page title, the page existence, and that child blocks were appended successfully.
- If a social post is created, verify the returned URL and published status.
- For status checks and asset handoffs, use `references/status-and-asset-handoff.md`: verify state before answering, separate script-ready / asset-ready / scheduled / published, and include preview/zip paths without implying publication.
- For short-term autonomous posting trials through Zernio, use `references/zernio-social-posting-trial.md`: verify connected accounts, publish primarily to LinkedIn, poll for `platformPostUrl`, and notify Seyed daily with the exact public link and text posted.

## Pitfalls
- Do not force a pre-made content calendar if the user wants reactive, evidence-based ideas.
- Do not write generic filler that is disconnected from actual work.
- Do not leave the final asset in a local draft state if the task includes publishing.
- Do not assume markdown links survive rich-text conversion unchanged.

## Support-file guidance
- Put reusable review-pack examples, checklists, or brand-specific publishing notes in `references/`.
- Put copyable starter drafts in `templates/`.
- Put repeatable validation or publishing probes in `scripts/`.
