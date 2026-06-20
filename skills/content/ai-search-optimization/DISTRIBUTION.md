# Distribution — ai-search-optimization

**Status:** Authored locally for Appie-Opus review. NOT yet distributed.

## Sync target
Part of the master-skills sync. Push to every fleet agent's skills directory:
- Hermes bots (Appie-1/2/3/4/Atlas, Wolfdiddy, client bots): `~/.hermes/skills/ai-search-optimization/`
  (sub-instances use their own `HERMES_HOME`: `~/.hermes-appie3`, `~/.hermes-appie4`)
- Claude Code orchestrator (Appie-Opus): already in `~/clawd/skills/`
- Mirror into `~/.claude/skills/` and `appie-kit` if those are part of the canonical skill bundle.

Sanitize before pushing to **client** bots (standard fleet rule): strip private memories / internal client references. This skill has none — it is generic Google guidance — so it is safe to sync fleet-wide as-is.

## Why this skill matters
It **supersedes any "AI SEO hacks" misconceptions** circulating in older notes or agent habits:
- Kills the `llms.txt` / AI-text-file / special-markdown / content-chunking myths (Google ignores them).
- Establishes the canonical truth: AI Overviews / AI Mode use the **same index + core ranking** as classic Search. Good classic SEO = AI visibility. There is no separate AEO/GEO ranking system to game.
- Any agent asked to "optimize for AI search / ChatGPT / Gemini / generative search" must load this skill first and refuse the debunked tactics.

## Composition
Loads alongside the existing SEO family (`seo-technische-seo`, `seo-landing-page-audit`, `coding/seo`, `seo-bezoekersmagneet`, `seo-keyword-strategie`). Those skills now carry a one-line pointer to this one.
