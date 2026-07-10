---
name: award-caliber-websites
description: Create, critique, or upgrade websites using an award-caliber framework that combines concept, narrative, interaction, usability, accessibility, performance, and visual craft.
version: 1.0.0
author: Appie
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web-design, design, ux, storytelling, motion, awards, awwwards, webby, creative-direction]
    related_skills: [claude-design, popular-web-designs, design-md, p5js, hyperframes, dogfood, adversarial-ux-test]
---

# Award-Caliber Websites

Use this skill when the user asks for:

- an award-winning website, Awwwards/Webby-level redesign, or standout landing page
- creative direction for a premium site
- critique of whether a site feels generic, memorable, usable, or award-caliber
- an art-directed website with storytelling, scroll rhythm, motion, or interaction
- a bridge between visual design skills and actual judged website quality

This is a class-level framework. Pair it with implementation skills:

- `claude-design` for artifact process and anti-slop execution
- `popular-web-designs` for real design-system references
- `design-md` for persistent tokens and WCAG validation
- `p5js`, `hyperframes`, or `manim-video` for motion and visual storytelling
- `dogfood` or `adversarial-ux-test` for browser-based verification and UX friction testing

## Core thesis

Award-caliber sites are not prettier generic sites. They have a clear idea, a memorable point of view, excellent usability, technical polish, and interaction that serves the story.

A site should be judged across seven dimensions:

1. **Concept**: What is the site trying to make the visitor feel, believe, or do?
2. **Narrative**: Does the scroll unfold like chapters instead of stacked sections?
3. **Visual system**: Are color, type, spacing, imagery, and components distinctive and controlled?
4. **Interaction**: Does motion reveal state, guide attention, or create tactility?
5. **Usability**: Can a real visitor understand, navigate, and act without friction?
6. **Execution**: Is it responsive, performant, accessible, and free of obvious technical defects?
7. **Content**: Is the copy specific, useful, and emotionally aligned with the brand?

## Workflow

### 1. Define the creative premise

Before designing sections, answer:

- Who is this for?
- What is the one-sentence idea of the site?
- What should the visitor remember 24 hours later?
- What is the brand allowed to be: calm, sharp, playful, cinematic, luxurious, weird, editorial, technical?
- What is explicitly off-brand?

If the premise is weak, do not compensate with gradients, glass, blobs, or animation.

### 2. Build the page as a story

Map the site into narrative beats, not generic sections.

Common arcs:

- **Problem to transformation**: pain, consequence, new mechanism, proof, invitation
- **Discovery**: hook, intuition, reveal, implications, action
- **Product cinema**: object, behavior, proof, ecosystem, CTA
- **Editorial authority**: thesis, evidence, cases, principles, contact
- **World-building**: atmosphere, beliefs, artifacts, rituals, conversion

Every section gets one job. If a section tries to explain everything, split it or delete it.

### 3. Choose a visual posture

Decide the posture before writing CSS:

- **Minimal premium**: strict type, negative space, one accent, product/image as hero
- **Cinematic dark**: scene-like scroll, controlled contrast, large display type, slow reveals
- **Editorial**: rich typographic hierarchy, essay-like rhythm, images as evidence
- **Playful craft**: tactile components, named color palette, delightful but legible interactions
- **Developer precision**: mono accents, code/product artifacts, restrained surfaces
- **Luxury restraint**: fewer weights, slower pacing, material detail, no loud UI patterns

Use `popular-web-designs` as reference material, but transform principles instead of cloning brand surfaces.

### 4. Design hero frames first

For each major section, define the hero frame: the moment when the most important visual idea is clearest.

Then implement:

1. static layout first
2. hierarchy and contrast next
3. responsive behavior
4. interaction and motion last

Do not add animation to rescue weak composition.

### 5. Motion rules

Good website motion:

- reveals relationships
- gives controls tactility
- makes scrolling feel like progression
- focuses attention on the current idea
- is respectful of `prefers-reduced-motion`

Bad website motion:

- loops without purpose
- delays access to content
- hides poor hierarchy
- turns every section into the same fade-up pattern
- causes layout instability or scroll jank

Use fewer motion motifs and repeat them consistently.

### 6. Award-style review pass

Score the site before calling it done:

- Design: visual system, typography, composition, art direction
- Usability: navigation, readability, CTA clarity, mobile flow
- Creativity: concept, interaction, memorability, surprise
- Content: specificity, proof, voice, narrative economy
- Technical execution: console health, responsiveness, performance, accessibility

A beautiful site with confusing navigation is not award-caliber. A usable site with no idea is not award-caliber either.

## Anti-patterns

Avoid:

- generic SaaS card grids as the default page structure
- fake dashboards, fake metrics, or fake testimonials
- decorative icons that do not improve scanning
- gradients, glassmorphism, or blobs without a brand reason
- every section using the same centered heading plus three cards
- motion added before the static design works
- copying distinctive branded layouts from references without rights
- accessibility as a final afterthought

## Verification checklist

Before final delivery:

- [ ] One-sentence creative premise is clear
- [ ] Each section has exactly one job
- [ ] Typography creates hierarchy before boxes or icons do
- [ ] Visual references were transformed, not cloned
- [ ] Motion has a purpose and reduced-motion fallback
- [ ] Mobile flow was considered, not just desktop
- [ ] Browser console checked if implemented
- [ ] Visual inspection performed with screenshot or browser vision when available
- [ ] Content avoids fake claims and generic filler
- [ ] CTA and navigation remain usable throughout

## References

- `references/criteria-and-method.md`: condensed notes on award criteria and the Weblyfe/Appie site-making method captured from prior design review work.
- `references/legal-website-competitive-research.md`: workflow and heuristics for deep research on award-winning or competitor lawyer/law-firm websites, including source-list extraction, original-site crawling, conversion/SEO analysis, and report artifacts.
