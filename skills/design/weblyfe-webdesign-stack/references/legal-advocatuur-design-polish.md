# Legal / Advocatuur Design Polish Reference

Class-level workflow for refining Dutch legal/advocatuur websites to a premium standard. Use for Soleiman-like boutique law firm projects.

## Design Principles
- **Empathy + Authority**: warmth toward the client, sharpness toward the adversary
- **Dark sophistication**: deep navy/ink + champagne-gold accents
- **Typography**: editorial serif for display, clean sans for body
- **Sharp corners (2-4px radius)**, no `rounded-full` on buttons/cards
- **No gavels/scales** stock imagery; prefer real office context, desaturated photography

## Refined Color System
- Navy `#0f2644` → buttons, headings, brand
- Deep ink `#06111f` → hero, footer, dark sections
- Ivory `#f5efe6` → backgrounds, light cards
- Champagne `#c9a76b` → accents, thin rules, gold details
- Charcoal `#1a232e` → body text

## Revision Workflow

### A. Classic Sharp Polish (default for Soleiman-style boutique firms)
...
1. **Research** via Exa AI: PaperStreet, Clio, Dan Gilroy, PxlPeak (intl) + Onwaarts, iO Digital, Legalista (NL)
2. **Visual audit** — load live site in browser (Chrome DevTools MCP), take screenshot, use `vision_analyze` with a specific prompt: "Describe the current design for a Harvey Specter / Suits style premium legal look. Focus on: typography, spacing, color usage, header, hero, card styling, layout hierarchy, motion." The vision output gives concrete improvement directions.
3. **PRD first** — document before/after, tokens, plan
4. **CSS tokens first** — update globals.css
5. **Bulk replace** via subagent, NOT manual patches — define ALL find/replace pairs in a structured list (color codes, radius tokens, button styles, shadow values), then dispatch a `delegate_task` with the file path and list. The subagent runs every replacement. Verify with `search_files` afterward. Saves ~15-20 manual patch calls on a full-page redesign.
6. **Also update component files**: SiteHeader, ScrubHero, SiteFooter, TeamSection — these often have separate inline styles that the home page bulk replace missed.
7. **Build** (`npm run build`) then preview deploy (`vercel --yes`, NOT `--prod`). If linking fails with a stale `.vercel`, remove and re-link.
8. **Client review** — confirm the preview URL visually. Let the client approve before production push.
9. **Production push** — TWO options depending on client setup:
   - GitHub auto-deploy: `git add <path> && git commit -m "msg" && git push origin master` → Vercel picks it up
   - Manual: `vercel --prod --yes` → note that team scope may differ from the domain owner
10. **Verify production URL** with `curl` and optionally a screenshot — build pass !== correct domain deployed

## Common find/replace patterns for legal polish
| Pattern | From | To |
|---------|------|-----|
| Navy | `#102b4e` | `#0f2644` |
| Ink | `#071522` | `#06111f` |
| Champagne | `#b9945d` | `#c9a76b` |
| Ivory | `#f7f2ea` | `#f5efe6` |
| Button radius | `rounded-full` on buttons | `rounded-[4px]` |
| Card radius | `rounded-[5px]` | `rounded-[4px]` |
| Legal blue | `#184a78` | `#1a5276` |
| Muted text | `#43505b` | `#3a4753` |
| Text muted | `#5c6873` | `#4f5d6a` |

## Research reference
Full Exa search results with URLs in `references/legal-design-exa-research-2026-06.md`