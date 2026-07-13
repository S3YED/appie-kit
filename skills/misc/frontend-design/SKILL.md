---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

## Landing Page Conversion Patterns

### Minimal first viewport, conversion below the fold
When refining a personal brand or creator landing page and the user asks for a more minimal homepage, strip the hero down aggressively:
- First viewport should carry identity + one powerful headline + one subtle scroll CTA only.
- Avoid putting multiple conversion CTAs, stat strips, social proof pills, or long explanations in the hero unless explicitly requested.
- Route the hero CTA to the next section with an in-page anchor (`#intro`, `#story`, etc.), not straight to a sales page.
- Start conversion pressure below the fold. CTAs in proof/intro/brand sections should guide users toward the primary choice section, commonly a three-path selector (`#paths`).
- Give the selector section a stable `id` and `scroll-mt-*` offset so mobile and sticky nav jumps land cleanly.

## Workflow Guardrails

### Working inside an already-modified frontend
When a repo has many uncommitted changes, treat the current state as someone else's active design pass:
- Inspect `git status` before editing.
- Read the page composition and the specific components in play before changing code.
- Do not rewrite broad sections just because the aesthetic could be improved. Patch only concrete mismatches, build failures, or explicit user-requested gaps.
- If legacy/unused components contain old classes or placeholders, note them separately instead of touching them unless they are imported by the target page.
- Verify with a production build first. Then run a local visual/browser check if a server can bind. If the environment blocks local server binding, report that limitation without encoding it as a durable tool failure.

## Stack-Specific Pitfalls

### Next.js 16 + Framer Motion + TypeScript
Framer Motion `Variants` objects with custom parameters need `as const` on `ease` tuples:
```tsx
// ❌ TypeScript error: 'number[]' not assignable to 'Easing'
const fadeUp = {
  visible: (i: number) => ({
    transition: { duration: 0.7, ease: [0.25, 0.46, 0.45, 0.94] },
  }),
};

// ✅ Use `as const`
const fadeUp = {
  visible: (i: number) => ({
    transition: { duration: 0.7, ease: [0.25, 0.46, 0.45, 0.94] as const },
  }),
};
```

### Tailwind CSS v4
Next.js 16 uses Tailwind v4 with `@import "tailwindcss"` instead of the old `@tailwind base/components/utilities` directives. Config lives in CSS, not `tailwind.config.ts`.

### Deployment
Vercel CLI tokens expire. Check `~/.vercel/auth.json` or `~/.config/vercel` before deploying. If expired, run `vercel login` interactively or create a new token at vercel.com/account/tokens.

When the user asks to publish and send a live link, do not treat a green local build as completion. Run the deploy, capture the explicit deployment URL from the CLI output, and verify it with a browser or HTTP fetch before reporting success. If `vercel deploy --prod --yes` hangs at `Retrieving project…`, exits without a URL, or produces spinner-only output, do not infer success from exit code. Retry with explicit linked project context if available (`.vercel/project.json`), then report the deployment as blocked unless a concrete Vercel URL is obtained and verified.

### Website Modernization Pipeline
For the complete "analyze existing site → SEO/design audit → rebuild → deploy" workflow, see `references/website-modernization.md`.

### Image-led visual refreshes
When improving a page with client-provided Drive/assets, do not choose images by filename or dump every asset into the repo. First create a candidate inventory, exclude unrelated folders the user warned about, make contact sheets, visually select images by website role, then copy only the chosen assets into `public/`. For the full workflow, see `references/image-led-visual-refresh.md`.

For image-led heroes, make gradients support the photo instead of hiding it: lower the readability gradient, reduce broad washes, and use local side/bottom overlays plus subtle text shadow. If the user says the hero image was better before, restore the original image first and preserve only non-image improvements like lighter gradients or typography refinements.

When the user asks to use images from the current/public client site, follow `references/public-site-image-refresh.md`: inventory public assets, classify stock vs real company imagery, avoid implying stock portraits are real people, select images by slot, and run responsive visual QA after import. For professional-services sites without verified portrait photography, explicitly state that the concept uses symbolic/editorial imagery for now and reserve personal bio/attorney sections for a real portrait instead of using stock people as representatives.

If the logo/nav sits on a transparent photo hero, the transparent state must be internally consistent: logo, wordmark, nav links, secondary links, CTA, and mobile menu icon should all use the same light/white treatment. Once the scrolled blurred/solid navbar appears, invert the whole system back to dark styling together. Avoid mixed states where only the logo is light but links/buttons stay dark.

For card-based visual sections, avoid duplicate image usage across adjacent homepage slots. Give key cards their own images, then move intro, gallery, and closing CTA to separate assets or subtle textures so the page feels curated instead of recycled.
