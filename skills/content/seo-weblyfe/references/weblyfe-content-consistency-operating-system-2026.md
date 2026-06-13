# Weblyfe content consistency operating system, June 2026

## Purpose
Keep Weblyfe, Seyed, and Appie publishing consistently without depending on random inspiration bursts.

## Core cadence
- Publish or prepare **2 Weblyfe blog articles per week**.
- Produce **5 to 7 LinkedIn drafts per week** for Seyed/Weblyfe/Appie.
- Generate **2 to 4 repurposing angles per week** for reels, carousels, or short-form clips.
- Run **1 weekly review** of planned vs drafted vs approved vs published.

## Weekly rhythm

### Monday: editorial direction
Pick two blog topics for the week. Each topic needs:
- Primary keyword.
- Search intent.
- Cluster role.
- Target Weblyfe service page or internal link destination.
- LinkedIn angle.

### Tuesday: blog 1 draft pack
Create:
- Full draft.
- SEO title and meta description.
- Source/backlink list.
- Internal links.
- Cover image direction or prompt.
- LinkedIn derivative.

### Wednesday: blog 1 finalization and blog 2 brief
- Anti-AI voice pass.
- No corporate filler, no em dashes.
- CMS-ready formatting.
- Blog 2 brief using the Monday criteria.

### Thursday: blog 2 draft pack
Create the second full blog pack with the same fields as blog 1.

### Friday: publishing preparation
Prepare publish-ready assets and QA:
- CMS formatting.
- Cover image check.
- Internal links.
- SEO metadata.
- LinkedIn variants.

Do not auto-publish public content unless Seyed explicitly approves. Drafting and preparation can run automatically.

### Sunday: consistency review
Report:
- What was planned.
- What was drafted.
- What was approved.
- What was published.
- What was blocked.
- Best next-week angles.

## Content pillars
1. **Story-driven websites**: conversion, narrative, founder-led positioning.
2. **Webflow and platform decisions**: Webflow vs WordPress, no-code, iteration speed.
3. **AI workflows and agents**: Appie, automation, client workflows, agency AI systems.
4. **Founder/operator lessons**: real client lessons, building Weblyfe/Appie, agency systems.

## Quality gates
A Weblyfe blog is not done until it has:
- Clear primary keyword.
- Search intent match.
- Strong title and intro.
- No generic AI filler.
- No em dashes.
- Useful sources or backlinks when relevant.
- Internal links to Weblyfe service/content pages.
- Branded cover image direction or asset.
- CMS-ready formatting.
- LinkedIn repurpose draft.

A LinkedIn draft is not done until it has:
- One strong hook.
- One clear point.
- Concrete founder/operator detail.
- Natural, direct voice.
- No corporate filler.
- Optional CTA only if useful.
- 3 to 5 hashtags max when needed.

## Automation design
Recommended recurring jobs:
- `weblyfe-weekly-editorial-brief`: Monday 08:00 NL.
- `weblyfe-blog-1-draft-pack`: Tuesday 08:00 NL.
- `weblyfe-blog-2-draft-pack`: Thursday 08:00 NL.
- `weblyfe-weekly-publishing-prep`: Friday 08:00 NL.
- `weblyfe-weekly-consistency-review`: Sunday 11:00 NL.

Use fully qualified skill paths in cron jobs where possible to avoid ambiguous skill load failures.
