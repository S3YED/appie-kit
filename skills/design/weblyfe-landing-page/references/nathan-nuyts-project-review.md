# Nathan Nuyts project review notes

Use as a compact example of how to inspect an existing Weblyfe client site before editing.

## Context found

- Repo: `~/clawd/projects/nathan-nuyts`
- Client deliverable: personal-brand / creator ecosystem site, not a plain service landing page.
- Stack: Next.js 15 App Router, React 19, TypeScript, Tailwind, Framer Motion.
- Vercel project linked via `.vercel/project.json`; production domain may differ from canonical metadata.
- Docs hierarchy discovered:
  - `HANDOFF.md`: most operationally important. Contains live URL, domain gotchas, deployment blockers, client caveats.
  - `docs/RESEARCH-BRIEF.md`: story spine, verified vs self-reported metrics, brand list, handles.
  - `docs/PRD-LIGHT-APPLE-GLASS-HOMEPAGE.md`: current homepage direction and exact section order.
  - `README.md`: useful but stale in parts. Treat older placeholder notes as lower authority than handoff and current code.

## Review pattern that worked

1. Read `HANDOFF.md` first for client/project state and non-obvious gotchas.
2. Read repo instructions and docs next: `AGENTS.md`, `README.md`, `docs/*.md`.
3. Inspect `package.json`, route tree, `app/page.tsx`, `app/layout.tsx`, key components, `public/brand`, and `.vercel/project.json`.
4. Compare docs against code rather than assuming docs are current.
5. Run targeted grep for durable risk markers: `TODO`, `picsum`, `placeholder`, canonical domains, `console.log`, `self-reported`, `reports`, `privacy`, `terms`.
6. Summarize current state, docs conflicts, route architecture, assets, deployment status, and concrete risks with file paths/line references.

## Durable Weblyfe pitfalls surfaced

- README can lag behind redesigns. In this repo it still mentioned placeholder `picsum.photos` even after most assets were replaced.
- A canonical production domain in metadata may not be the actual deliverable domain yet. Check handoff before repeating or deploying a domain.
- Personal-brand metrics need careful framing: distinguish verified reach from self-reported aggregate/revenue/deal numbers.
- Footer legal links often get added before pages exist. Verify `/privacy` and `/terms` routes before delivery.
- Form/booking route handlers that return success while only `console.log`ing are not production-ready lead capture.
- Template-origin components can survive after redesign. Search for old token classes and external placeholder images.