---
name: seo-technische-seo
description: "Audit and fix technical SEO for Weblyfe sites, including crawling, indexing, structured data, speed, and launch readiness."
version: 1.0.0
category: content
---

# SEO Technische SEO Skill

## Purpose
Ensure Google can crawl, index, and correctly interpret any Weblyfe site. Use this at site launch (prerequisite before any on-page or off-page work), when a site is not appearing in search results, or when rankings drop unexpectedly. Also covers rich markup (structured data) which unlocks enhanced SERP features.

## Source
"Technische SEO" PDF from the source SEO course (downloaded from Drive 2026-05-03).

## Quick reference
| Task | Action |
|------|--------|
| Submit sitemap | Google Search Console > Sitemaps > add sitemap.xml URL |
| Find crawl errors | Google Search Console > Coverage > Errors |
| Check mobile rendering | Google Mobile-Friendly Test + manual device check |
| Add local business schema | Add `LocalBusiness` JSON-LD to homepage |
| Add product schema | Add `Product` JSON-LD with price, availability, reviews |
| Add review schema | Add `AggregateRating` JSON-LD |
| Speed check | Google PageSpeed Insights (mobile score is primary) |
| Validate structured data | Google Rich Results Test (search.google.com/test/rich-results) |

## Core principles
1. Schone code is the foundation. Google's crawler reads your HTML directly. Dirty, bloated, or broken code slows crawling and reduces indexing quality.
2. Sitemaps tell Google what pages exist and which to prioritise. Submit XML sitemap via Search Console.
3. Errors (4xx, 5xx) waste crawl budget and signal poor site health. Monitor and fix via Search Console > Coverage.
4. Slechte software and poorly coded plugins add bloat, JavaScript errors, and slow load times. Each plugin is a liability.
5. Mobile-first indexing is the current Google standard. The mobile version of a page is what Google indexes and ranks.
6. Rich markup (structured data / schema.org) makes a site "semantisch" - Google understands entities, not just text. This unlocks rich snippets in SERPs.
7. Rich markup types available for Weblyfe clients: Locatie (LocalBusiness), Producten (Product), Recepten (Recipe), Reviews (AggregateRating), Events, Vacatures (JobPosting), Website elementen (WebSite with Sitelinks search box).
8. Fast indexing = competitive advantage for fresh content (news, events, pricing). Submit URLs via Search Console > URL Inspection > Request Indexing for time-sensitive pages.

## How to apply (for any new Weblyfe site)
- Verify sitemap.xml exists and is accessible at `/sitemap.xml`. Submit to Google Search Console.
- Check Search Console Coverage report: zero errors target at launch.
- Audit installed plugins/apps: remove any that add functionality not used. Each unused plugin is technical debt.
- Run Google Mobile-Friendly Test. Fix any failing elements before launch.
- Run PageSpeed Insights on homepage and top landing page. Target 80+ on mobile.
- Identify the most relevant schema types for the client: most Weblyfe clients need at minimum `LocalBusiness` or `Organization` + `WebSite`.
- Implement JSON-LD structured data in the `<head>` or at end of `<body>`. Do not use Microdata (more error-prone).
- Validate schema with Rich Results Test before publishing.
- Set up Search Console email alerts for coverage errors and manual actions.
- Ensure canonical tags are set correctly to prevent duplicate content issues.

## Anti-patterns (what the PDF says NOT to do)
- Installing many plugins without auditing them. Each plugin can add render-blocking scripts, database queries, or security vulnerabilities.
- Ignoring mobile. Google uses the mobile version for indexing; a desktop-only optimisation is wasted effort.
- Skipping the sitemap submission. Google will eventually find pages, but submission speeds up initial indexing significantly.
- Not monitoring errors. A single 404 on a high-value page costs ranking over time.
- Using generic or keyword-free URLs. `/pagina-1/` tells Google nothing. `/seo-tips-voor-mkb/` does.

## Examples and templates
Rich markup types from PDF (with primary use case for Weblyfe clients):

| Schema type | When to use |
|-------------|-------------|
| LocalBusiness | Any client with a physical address or service area |
| Product | Webshop or SaaS with clear pricing |
| AggregateRating | Any site with customer reviews |
| Event | Clients running workshops, events, webinars |
| JobPosting | Clients actively recruiting |
| WebSite | Every site - enables Sitelinks search box |

Minimal `WebSite` JSON-LD:
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Bedrijfsnaam",
  "url": "https://www.domein.nl"
}
```

## Cross-skill references
- `seo-checklist`: technical items (sitemap, canonical, mobile) are in the pre-launch checklist
- `seo-bezoekersmagneet`: technical SEO enables the 6 quality signals Google checks
- `seo-smart-content`: internal link network only works if Google can crawl all pages
- `ai-search-optimization`: indexability/crawlability/schema here is also what makes pages eligible for AI Overviews & AI Mode (same index + ranking)
