---
name: webflow-seo-audit
description: Run a comprehensive SEO audit on Webflow sites via API + live browser crawling. Checks meta tags, alt text, headings, schema, sitemap, technische SEO, en backlink opportunities.
trigger: User asks to audit, analyse, or SEO-check a Webflow site, or asks for 'volledige analyse' van een site.
---

# Webflow SEO Audit

## Workflow

### Phase 1: Install & Connect
1. Check if there's an existing project dir in `~/clawd/projects/<client>/`
2. Test the API token via Webflow v2 API:
   `curl -sH "Authorization: Bearer $TOKEN" -H "Accept-Version: 1.0.0" https://api.webflow.com/v2/sites`
3. Identify Site ID, save to `.weblyfe-secrets/<client>.env`
4. Create project dir with `README.md` and `wf.sh` helper

### Phase 2: Live Crawl (browser_navigate + browser_console)

**ALWAYS use browser_console JavaScript DOM extraction, NOT curl regex.** Webflow's compiled HTML is minified/injected and curl-based regex (even with re.DOTALL) consistently misses meta tags, OG tags, and canonical links that the browser DOM can access.

**Crawl sequence (critical — browser_console is session-bound):**
1. `browser_navigate(url=PAGE_A)` → `browser_console(expression=META_SCRIPT)` → save results
2. `browser_navigate(url=PAGE_B)` → `browser_console(expression=META_SCRIPT)` → save results
3. Repeat for each page. **Extract metadata BEFORE navigating away** — the previous page's DOM is gone after navigation.

**Pages to crawl:**
- `/` (homepage)
- Main nav pages (about, family, performance, contact)
- `/privacy`, `/terms`
- Any CMS template pages (e.g. `/video/[slug]`, `/faq/[slug]`)
- Any suspicious pages found in sitemap (`/quiz`, `/call`, `/order`, etc.)

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

**Alternative for bulk check without browser:** If the site is on Cloudflare (check `server: cloudflare` header), you can also use `curl -sL` to GET the HTML. But the regex approach remains fragile — use the browser for canonical results.

### Phase 3: Technical Checks (terminal)
- `curl -sI https://<domein>` — check HTTP headers, Cloudflare, HSTS
- `curl -s https://<domein>/sitemap.xml` — check sitemap contents
- `curl -s https://<domein>/robots.txt` — check robots.txt
- `dig +short <domein>` — check DNS
- `curl -s https://<domein> | grep -o 'application/ld+json'` — check schema presence
- Check sitemap URLs — look for orphaned/empty pages (/quiz, /call, /order)

### Phase 4: CMS Data (Webflow API)
- Fetch collections: `GET /v2/sites/{id}/collections`
- Fetch items per collection: `GET /v2/collections/{id}/items`
- Check FAQ items, video pages, testimonials, content blocks
- Note any CMS items that have slugs but no dedicated page URL

### Phase 5: Scoring & Report

**Priority levels:**
- **P0 / Critical** — Multiple H1 tags, alt text crisis (>50% missing), sitemap issues, empty pages indexed, wrong titles
- **P1 / High** — No internal linking, FAQ without pages, schema gaps (Organization, FAQPage, Author), broken social share, wrong email domains
- **P2 / Medium** — Breadcrumbs missing, weak titles, hreflang, duplicate pages
- **P3 / Low** — Nice-to-haves

**Common Webflow SEO bugs (check these first):**
1. Slider/lightbox sections rendered as `<h1>` instead of `<h2>` — very common Webflow pattern
2. All images have `alt=""` by default in Webflow CMS — must be manually filled
3. Privacy/Terms pages often get default titles "Privacy" / "Terms"
4. CMS items have slugs but no dedicated page template
5. Social share buttons link to `#` — never wired up

### Phase 6: Backlink Strategy
Suggest linkable assets based on content found:
- Enagic dealer/partner listings
- PubMed/study citations → guest posts
- Blue Zones / longevity angle
- Local SEO (Google Business, location data)
- Sports/athlete partnerships from testimonials
- LinkedIn founder profile optimization

### Phase 7: Notion Task Creation (voor team-uitvoering)
Most Webflow SEO fixes require **Designer access** — the API cannot change page settings, H1 tags, custom code, or page titles. For these, create a Notion task for the designer:

1. Create task in the **Task List** database (database_id: `538bdf7b-a506-4c9c-b451-5d2f78b4d544`)
2. Use `Person: people` property to assign to workspace user (Seyed = `379c630c-9c29-46f1-9dc7-68de28d8f25c`)
3. Add detailed checklist as `to_do` blocks under the page
4. Label with `Webflow`, `SEO`, `<client-name>` multi-selects
5. If the assignee (Danial) is not a Notion workspace user, put their name in the task title

**Notion API notes for this:**
- `NOTION_API_KEY` is in `~/clawd/.env`
- Task List database: use `database_id` for `parent`, `data_source_id` for querying
- Python's `urllib.request` works more reliably than curl for multi-block page creation

**Webflow API limitation — Designer-only fixes (NOT possible via API):**
- Page SEO settings (title, meta desc, OG tags, canonical)
- Custom Code (requires Designer → Project Settings → Custom Code tab)
- H1/H2 tag changes (Designer → element tag selector)
- Image alt text (CMS field or Designer)
- Page creation (FAQ detail pages, etc.)
- Breadcrumb components

**What you CAN do via Webflow API:**
- Read site info, collections, CMS items
- List pages in sitemap
- Token test with `GET /v2/sites`

If the client provides Designer access, log in via browser to execute fixes. Otherwise, hand off to the designer via Notion task.

### Phase 8: Report
Save report to `~/clawd/projects/<client>/seo-audit-<date>.md`

---

## Reference Files

- `references/webflow-api.md` — Webflow v2 API endpoints, auth format, collection querying
- `references/common-seo-bugs.md` — Common Webflow SEO pitfalls and fixes