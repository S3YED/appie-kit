---
name: webflow-seo-audit
description: Run a comprehensive SEO audit on Webflow sites via API + live browser crawling. Checks meta tags, alt text, headings, schema, sitemap, technical SEO, and backlink opportunities.
trigger: User asks to audit, analyse, or SEO-check a Webflow site.
---

# Webflow SEO Audit

Run a comprehensive SEO audit on Webflow sites via API + live browser crawling.

## Workflow

### Phase 1: Install & Connect
1. Test the API token via Webflow v2 API:
   `curl -sH "Authorization: Bearer <token>" -H "Accept-Version: 1.0.0" https://api.webflow.com/v2/sites`
2. Identify Site ID, save to project env file
3. Create project dir with README.md

### Phase 2: Live Crawl (browser_navigate + browser_console)

**Use browser_console JavaScript DOM extraction, NOT curl regex.** Webflow's compiled HTML is minified/injected and curl-based regex misses meta tags, OG tags, and canonical links.

**Crawl sequence:** Extract metadata BEFORE navigating away — the previous page's DOM is gone after navigation.

**Pages to crawl:**
- `/` (homepage), Main nav pages, `/privacy`, `/terms`
- CMS template pages (`/video/[slug]`, `/faq/[slug]`)
- Suspicious pages in sitemap (`/quiz`, `/call`, `/order`)

**Browser console script for each page:**
```js
JSON.stringify({
  title: document.title,
  metaDesc: document.querySelector('meta[name="description"]')?.getAttribute('content') || 'MISSING',
  ogTitle: document.querySelector('meta[property="og:title"]')?.getAttribute('content') || 'MISSING',
  ogDesc: document.querySelector('meta[property="og:description"]')?.getAttribute('content') || 'MISSING',
  ogImage: document.querySelector('meta[property="og:image"]')?.getAttribute('content') || 'MISSING',
  canonical: document.querySelector('link[rel="canonical"]')?.getAttribute('href') || 'MISSING',
  h1count: document.querySelectorAll('h1').length,
  h2count: document.querySelectorAll('h2').length,
  images: document.querySelectorAll('img').length,
  imgsWithAlt: Array.from(document.querySelectorAll('img')).filter(i => i.alt && i.alt.trim()).length,
});
```

### Phase 3: Technical Checks (terminal)
- `curl -sI https://<domain>` — HTTP headers, HSTS
- `curl -s https://<domain>/sitemap.xml` — sitemap
- `curl -s https://<domain>/robots.txt` — robots.txt
- `dig +short <domain>` — DNS
- Check sitemap URLs for orphaned/empty pages

### Phase 4: CMS Data (Webflow API)
- Fetch collections: `GET /v2/sites/{id}/collections`
- Fetch items: `GET /v2/collections/{id}/items`
- Note CMS items with slugs but no dedicated page URL

### Phase 5: Scoring & Report

**Priority levels:**
- **P0 / Critical** — Multiple H1 tags, >50% alt text missing, sitemap issues, empty indexed pages, wrong titles
- **P1 / High** — No internal linking, FAQ without pages, schema gaps, broken social share
- **P2 / Medium** — Breadcrumbs missing, weak titles, hreflang, duplicate pages
- **P3 / Low** — Nice-to-haves

**Common Webflow SEO bugs (check first):**
1. Slider/lightbox sections rendered as `<h1>` instead of `<h2>`
2. Images have `alt=""` by default in Webflow CMS
3. Privacy/Terms pages get default titles
4. CMS items have slugs but no dedicated page template
5. Social share buttons link to `#`

### Phase 6: Backlink Strategy
Suggest linkable assets based on content found: industry partnerships, scientific citations, local SEO, founder profile optimization.

### Phase 7: Remediation
Most Webflow SEO fixes require **Designer access** — the API cannot change page settings, H1 tags, custom code, or page titles. Create tasks for the designer.

**Webflow API limitations (Designer-only fixes):**
- Page SEO settings (title, meta desc, OG tags, canonical)
- Custom Code
- H1/H2 tag changes
- Image alt text
- Page creation
- Breadcrumb components

**What you CAN do via API:**
- Read site info, collections, CMS items
- List pages in sitemap
- Token test

### Phase 8: Report
Save report to project directory with date-stamped filename.

## Reference Files
- `references/webflow-api.md` — Webflow v2 API endpoints, auth format, collection querying
- `references/common-seo-bugs.md` — Common Webflow SEO pitfalls and fixes