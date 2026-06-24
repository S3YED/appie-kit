---
name: seo-landing-page-audit
description: Audit and improve landing pages using SEO fundamentals from the Tornado/IMU PDFs: bezoekersmagneet, zoekwoorden, backlinks, smart content, technische SEO, and on-page checklist.
---

# SEO Landing Page Audit

Use this for landing pages, event pages, campaign pages and SEO conversion pages. The goal is to make the page a better visitor magnet: relevant, specific, unique, readable, technically clean, and trusted.

## Source Principles

From the SEO PDFs:

1. **Bezoekersmagneet**
   - SEO is for attracting visitors and managing reputation.
   - Google remains durable while social channels come and go.
   - On/off-page signals: relevance, popularity, uniqueness, actuality, quality, readability.

2. **Scoren op zoekwoorden**
   - Words closer to the front carry more weight.
   - Be specific. Long-tail intent often converts better than broad keywords.
   - Monster content wins when it includes images, video, length/depth, outgoing links, interaction, backlinks and internal links.

3. **Backlinks**
   - Authority matters.
   - Relevant links are more valuable than irrelevant links.
   - Earn links through useful content, guest/blog references, owned properties and relevant profiles.

4. **Smart content**
   - Content should match visitor intent and be useful, not filler.
   - Add sections that answer real questions and guide next action.

5. **Technische SEO**
   - Clean code, sitemap, errors, readable code, minimal bad plugins/software.
   - Rich markup/schema helps semantic search: location, products/services, reviews, events, vacancies, website elements.

6. **On-page checklist**
   - Unique title and meta description.
   - One clear H1.
   - Logical H2/H3 hierarchy.
   - Keyword in title, meta, H1/intro, headings and body naturally.
   - Descriptive image alt text.
   - Internal/external links where useful.
   - Fast, mobile-friendly, no broken links/images.

## Audit Checklist

### Keyword and intent
- Identify primary keyword and 3-6 secondary/long-tail keywords.
- Put primary keyword early in `<title>`, meta description, H1 or hero intro.
- Avoid keyword stuffing. Specific beats broad.

### Content quality
- Does the hero answer: what is this, for whom, why now, why trust us, what next?
- Add concrete proof: years, cases, numbers, expertise, location, date.
- Add FAQ for objections and semantic coverage.
- Add media that supports the claim, not decorative filler.

### Technical SEO
- Verify title/meta/canonical/hreflang/robots/sitemap.
- Add JSON-LD where relevant: `Event`, `Organization`, `FAQPage`, `Product`, `Service`, `BreadcrumbList`.
- Check broken images/links and HTTP status.
- Check mobile viewport and readable text.
- Keep HTML clean and accessible.

### Conversion SEO
- CTA above the fold and repeated after proof.
- Match CTA text to intent: “Uitnodiging aanvragen” beats vague “Aanvragen”.
- Remove friction, but qualify where needed.
- Use scarcity honestly.

### Brand and readability
- Content must feel human, specific and credible.
- Replace houterige punctuation or AI-like copy.
- Respect user copy rules, e.g. for Seyed: no em-dashes in copywriting.

## AI features (AI Overviews / AI Mode)
For visibility in generative search, also run the `ai-search-optimization` skill: AI features use the same index + core ranking, so this page must be indexed, crawlable, snippet-eligible, and offer a unique POV (not a commodity summary). Skip the debunked tactics (llms.txt, content chunking).

## Verification Commands

Use Playwright or equivalent to verify:

- HTTP 200 on key URLs.
- `document.title` and meta description.
- Count `script[type="application/ld+json"]`.
- Broken images count is 0.
- Body text has no forbidden terms.
- Mobile screenshot/readability check.

Example:

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={'width': 1440, 'height': 1000})
    page.goto('https://example.com', wait_until='networkidle')
    text = page.locator('body').inner_text()
    print({
      'title': page.title(),
      'jsonld': page.locator('script[type="application/ld+json"]').count(),
      'broken_images': page.evaluate('Array.from(document.images).filter(i=>!i.complete||i.naturalWidth===0).length'),
    })
    b.close()
```
