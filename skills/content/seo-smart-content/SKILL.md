---
name: seo-smart-content
description: "Plan SEO content networks and internal-link architectures that compound authority across Weblyfe client sites."
version: 1.0.0
category: content
---

# SEO Smart Content Skill

## Purpose
Plan and architect a content network that compounds in SEO value over time. Use this when building a new site's content strategy, when a site has isolated pages that do not link to each other, or when planning a content calendar for a Weblyfe client. The core idea: every piece of content should link into a web, not exist as an island.

## Source
"Smart Content" PDF from Seyed's Weblyfe University SEO course (downloaded from Drive 2026-05-03).

## Quick reference
| Task | Action |
|------|--------|
| Map internal links | Draw a hub-and-spoke diagram: one pillar page, multiple supporting articles all linking back |
| Retarget content readers | Facebook Pixel on content pages + retargeting campaign |
| Convert content readers | Add conversiepixel / conversiecode on thank-you pages |
| Track content performance | Google Search Console impressions + GA4 engagement rate |
| Find content gaps | Exa research on competitor content clusters |

## Core principles
1. Content does not work in isolation. The PDF shows a web of interconnected pages where every node links to related nodes. Isolated pages accumulate no authority.
2. Internal linking distributes PageRank within the site. A strong internal network means externally earned backlinks benefit the whole site, not just one page.
3. Content is a retargeting asset. Blog readers who do not convert can be re-engaged via Facebook Retargeting using the Facebook Pixel - they have already shown topical interest.
4. The Facebook Retargeting stappenplan from the PDF: (1) place Pixel, (2) build audience from page visitors, (3) run ads to that warm audience. Cost per acquisition is significantly lower than cold traffic.
5. Conversiepixel / conversiecode tracks which ads and which content led to actual purchases or sign-ups.
6. Content clusters beat single articles. A pillar page + 10 supporting articles collectively rank for far more variations than one long article.
7. Smart content serves both SEO (organic discovery) and paid (retargeting fuel). It is not just an SEO tactic.
8. Update existing content regularly. Actualiteit is one of Google's 6 ranking signals (from Bezoekersmagneet module).

## How to apply (for any new Weblyfe site)
- Identify 3-5 pillar topics for the site. Each pillar gets a long-form hub page.
- Plan 5-10 supporting articles per pillar. Each supporting article links to the pillar and to at least 2 other supporting articles in the same cluster.
- Install Facebook Pixel on all content pages on day one (even before the first article is published).
- Set up a custom audience in Facebook Ads Manager: "visitors of /blog/* in the last 30 days."
- Add conversiecode to the order confirmation or lead thank-you page to enable conversion tracking.
- Create an internal linking map as a spreadsheet: columns = source page, target page, anchor text. Update on every new publish.
- Audit internal links quarterly: identify orphan pages (no inbound internal links) and fix them.
- Repurpose high-traffic articles into video or infographic to earn additional backlinks.

## Anti-patterns (what the PDF says NOT to do)
- Publishing content without internal links to related pages. Orphan content earns no internal PageRank.
- Running retargeting without a Pixel. You cannot retarget visitors you have not tracked.
- Treating blog content as separate from the commercial site. Content and conversion funnels should be connected.
- Ignoring existing content. A well-updated older article outperforms a new one on the same topic.

## Examples and templates
Content web pattern (from PDF slide 2 and 3):
A central hub article surrounded by 20-30 satellite articles, all connected with dashed link lines. The hub has the highest internal link authority. Satellite articles reinforce each other laterally.

Facebook Retargeting stappenplan (from PDF slide 4):
"Facebook Retargeting is een perfecte manier om specifiek te adverteren aan mensen die jouw website al kennen, dus een bijzonder hebben. Deze mensen vormen een zeer relevante doelgroep en je zult zien dat je hiermee bijvoorbeeld je opties en verkopen tegen lage kosten flink kunt opvoeren."

Steps: (1) Retargeting pixel aanmaken in Facebook Ads account, (2) specify conversion events, (3) launch campaign to warm audience.

## Cross-skill references
- `seo-keyword-strategie`: content clusters are built around keyword families, not random topics
- `seo-backlinks`: pillar pages are the primary targets for earned external backlinks
- `seo-technische-seo`: site must be crawlable for the internal link network to work
- `seo-checklist`: each article in the cluster must pass the on-page checklist before publishing
