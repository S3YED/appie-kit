# SEO Backlinks Skill

## Purpose
Build, evaluate, and audit the external link profile of any Weblyfe client site. Use this when a site has good on-page SEO but is not breaking into the top 5 (authority gap), when planning a content or outreach campaign, or when a client asks why a competitor outranks them despite similar content.

## Source
"Backlinks" PDF from Seyed's Weblyfe University SEO course (downloaded from Drive 2026-05-03).

## Quick reference
| Task | Action |
|------|--------|
| Check existing backlinks | Ubersuggest > Backlink Checker OR Google Search Console > Links |
| Find competitor backlinks | Ubersuggest > enter competitor domain |
| Evaluate a link source | Check: high autoriteit + relevant onderwerp = waardevol |
| Check follow vs nofollow | Inspect link HTML: `rel="nofollow"` = no PageRank passed |
| Outreach for guest posts | Find relevant NL/BE blogs in the niche, pitch a gastblog |

## Core principles
1. Google was originally called "Backrub" - the PageRank algorithm was built on the idea that links are votes. This has not fundamentally changed.
2. Quantity of backlinks matters less than quality. One link from a high-authority site beats 100 links from low-authority sites.
3. Two quality axes: autoriteit (domain strength) AND relevantie (topical match). A link from Marketingtips.nl to IMU.nl is relevant. A link from Tuintips.nl to IMU.nl is not.
4. Follow links pass PageRank (link juice). Nofollow links do not pass juice - shown in PDF as a glass that spills rather than pours.
5. The more sites link to B compared to A, the more PageRank B accumulates. The winner in any niche is typically the one with the strongest backlink network.
6. Anchor text matters: "Online marketing" as anchor text is relevant and carries signal. "Klik hier" carries almost no topical signal.
7. Earned links (links verdienen) are the safest and most durable acquisition method.
8. Guest blogging (gastbloggen) is the primary active outreach strategy named in the PDF.

## How to apply (for any new Weblyfe site)
- Run Ubersuggest backlink audit on the client domain and top 3 competitors on day one.
- Identify authoritative and relevant Dutch/Belgian domains in the client's niche.
- Build immediate quick wins: add the site to the client's own other web properties, social media profiles (LinkedIn company page, Facebook, etc.).
- Plan one guest post per month on a relevant NL/BE blog with a follow link back.
- Earn links by publishing linkable assets: original research, tools, checklists, or definitive guides (monsterartikelen).
- When acquiring or building affiliate partnerships, ensure affiliate links are follow where possible.
- Audit nofollow vs follow ratio quarterly via Ubersuggest or Search Console.
- Avoid link schemes (link farms, paid links without nofollow). Google's spam detection is sophisticated.

## Anti-patterns (what the PDF says NOT to do)
- Link farms: mass low-quality link networks. Google detects and penalises these.
- Linkruilen (reciprocal linking) at scale. A few natural reciprocal links are fine; a systematic exchange is a red flag.
- Buying backlinks without nofollow tags. Violates Google's guidelines.
- Accepting links from irrelevant sites regardless of their authority (Tuintips.nl linking to an online marketing site adds almost no value).
- Using "klik hier" or generic anchor text. Always negotiate for keyword-rich anchor text when possible.

## Examples and templates
Quality evaluation matrix from PDF:

| Source autoriteit | Relevantie | Verdict |
|------------------|-----------|---------|
| Hoog | Ja | Waardevol |
| Laag | Ja | Beperkte waarde |
| Hoog | Nee | Niet waardevol |
| Laag | Nee | Schadelijk risk |

Linkbuilding sources ranked by safety (from PDF):
1. Eigen websites (safest)
2. Social media profielen
3. Affiliates
4. Gastbloggen
5. Links verdienen (best long-term)
6. Website overnames
7. Linkruilen (risky at scale)
8. Link farms (avoid)
9. Backlinks kopen (avoid)

## Cross-skill references
- `seo-bezoekersmagneet`: autoriteit is one of Google's 6 ranking factors (Populariteit)
- `seo-keyword-strategie`: monsterartikelen earn links naturally; create them first
- `seo-smart-content`: a strong internal link network distributes the PageRank you earn externally
