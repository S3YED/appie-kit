---
name: ai-search-optimization
description: Use when building or auditing a site for SEO visibility in AI Overviews, AI Mode, or generative search (AEO / GEO / answer-engine optimization), or when someone asks how to "optimize for ChatGPT/Gemini/AI search", whether to add llms.txt or AI text files, how grounding / query fan-out / RAG pick pages, indexability and snippet-eligibility for AI features, structured data for AI, or agentic/UCP commerce readiness. Codifies Google's official AI-optimization guidance and debunks AI-SEO myths.
---

# AI Search Optimization (AEO / GEO)

Google's AI features (AI Overviews, AI Mode) use the **same crawl, index, and core ranking** as classic Search, plus grounding (RAG) and **query fan-out** (the model generates related sub-queries and pulls pages for each). There is **no separate AI ranking system**. Good classic SEO IS AI visibility. Source: developers.google.com/search/docs/fundamentals/ai-optimization-guide.

## Eligibility checklist (same as Search eligibility)
A page can only surface in AI features if it is:
- [ ] **Indexed** — not blocked by `noindex`, in the index, not a duplicate canonicalized away
- [ ] **Crawlable** — `robots.txt` allows it; JS unblocked so rendered content is visible
- [ ] **Publicly accessible** — no login/paywall wall on the content that should rank
- [ ] **Snippet-eligible** — no `nosnippet` / `max-snippet:0` / `data-nosnippet` on the content you want quoted
- [ ] Meets Search **technical requirements** + **spam policies** (no cloaking, scaled-content abuse)

Note: meeting every requirement does **not** guarantee crawl, index, or serving.

## Content: people-first + unique POV
- Write for humans. Offer a **unique point of view, first-hand experience, original data, or expertise** the model can't synthesize from everyone else.
- Avoid commodity summaries an LLM could generate itself — those don't earn citation.
- Avoid **scaled content abuse** (mass keyword/location variations to manipulate).
- No ideal length. Clear headings, sections, short paragraphs. Self-contained answers near the top help, but do **not** chunk content into tiny fragments.

## DEBUNKED — do NOT waste effort on these
| Myth | Reality |
|------|---------|
| `llms.txt` / AI text files / `ai.txt` | Google Search ignores them. Zero benefit. |
| Special markdown / "machine-readable AI" copies | Not used. Serve normal HTML. |
| "Chunk" content into micro-pieces for the LLM | No benefit; harms readability. |
| Write copy *specifically for* generative AI | Write for people; ranking follows. |
| Chase inauthentic "mentions" / brand name-drops | Not a ranking signal; can be spam. |
| Separate "AEO/GEO ranking system" to game | Doesn't exist. Same index + ranking. |

## Structured data
Not required for AI features, but **still recommended** — it powers overall SEO and rich-result eligibility. Use valid schema.org JSON-LD: `Organization`/`LocalBusiness`, `Product`, `FAQPage`, `Article`, `BreadcrumbList`. (See `seo-technische-seo`.)

## Multimodal
High-quality, relevant images/video create **more opportunities** to appear in AI responses. Follow image/video SEO best practices (descriptive alt text, captions, structured data, fast delivery).

## Local / ecommerce
- **Google Business Profile** feeds local info into AI responses (hours, location, reviews).
- **Merchant Center** product feeds power product details in AI shopping answers.
- **Business Agent** enables conversational experiences over your data.

## Technical / crawlability
Unblock JS, use semantic human-readable HTML (imperfect HTML is fine), reduce duplicate content, fast + mobile page experience, clear separation of main content vs chrome/nav.

## Agentic / UCP (emerging)
AI agents read sites via DOM, accessibility tree, and screenshots. Keep markup accessible and agent-friendly. The **Universal Commerce Protocol (UCP)** for agentic checkout is emerging — track it for ecommerce clients.

## Example — commodity vs unique-POV (the difference that earns a citation)

```text
COMMODITY (won't get cited — LLM already knows this):
  H1: What is SEO?
  "SEO is the practice of optimizing a website to rank higher
   in search engines. It includes keywords, backlinks, and
   technical optimization."

UNIQUE POV (citable — first-hand, specific, original):
  H1: SEO results timeline: what 40 Dutch MKB sites taught us
  "Across 40 client sites we launched in 2025, position-1
   rankings took a median of 4.5 months. The fastest (6 weeks)
   all shared one trait: a LocalBusiness schema + 15+ Google
   reviews live at launch. Here is the month-by-month data..."
```

## Quick audit snippet (indexability)
```bash
curl -sI https://example.com/page | grep -i 'x-robots-tag'         # nosnippet/noindex?
curl -s https://example.com/page | grep -i '<meta name="robots"'    # page-level robots
curl -s https://example.com/robots.txt | grep -i 'disallow'         # crawl blocks
# Then: Search Console > URL Inspection — confirm "Indexed" + rendered content visible.
```

## Cross-skill references
- `seo-technische-seo` — crawl/index/schema foundation (prerequisite)
- `seo-landing-page-audit` — apply this on landing/conversion pages
- `coding/seo` — umbrella; this is the AI-features layer
- `seo-bezoekersmagneet` / `seo-keyword-strategie` — the same signals AI ranking uses
