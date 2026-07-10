---
name: productized-service-business
description: Validate, launch, and deliver productized service businesses, service-first SaaS wedges, managed marketplaces, and audit/retainer offers. Use when the user asks which business idea is worth doing, wants competitor or Dutch/NL market validation, wants a monetization ladder, wants to validate a service before building software, or wants delivery SOPs/templates for a first paid client offer such as Review-to-Revenue / Customer Voice Conversion Audits.
---

# Productized Service Business

Use this class-level skill to move from raw idea → market verdict → first paid offer → repeatable delivery. Prefer service-first validation over building SaaS until paid demand is proven.

## Default workflow

1. **Define the paid proposition before researching**
   - Who pays?
   - What painful job gets removed or improved?
   - What exact deliverable is produced?
   - What outcome is promised?
   - What is the narrow first wedge?

2. **Research competitors by category, not just exact names**
   - Direct exact competitors.
   - Adjacent service providers.
   - Software/tools that solve part of the problem.
   - Agencies/consultants with broader overlap.
   - Blogs/content that describe the method but do not sell it.
   - Enterprise versions that are too heavy for the target customer.

3. **Compare overlap with a fixed grid**
   For each found party, check whether it uses the same primary input, targets the same buyer, delivers the same artifact, promises the same outcome, has similar pricing/productization, and can expand into the wedge quickly.

4. **Score attackability 1-10**
   Judge pain intensity, buyer ability to pay, ease of first sale, competitor density, clarity of ROI, delivery simplicity, ability to productize into retainer/MRR, and copy risk from tools/agencies.

5. **Finish with the operator answer**
   Always include: hard verdict, sharp positioning sentence, first paid offer, free entry wedge, upsell/retainer path, biggest risk, and next 3 actions.

## Research lane

Load `exa-plus` for deep search when useful. If Exa fails because `EXA_API_KEY` is missing, continue with `web_search` + `web_extract` and mention the fallback. For Dutch checks, search both Dutch and English:

- `Nederland [problem] automatisering [buyer]`
- `site:.nl "[exact phrase]" "[industry]"`
- `"[method]" "webshop" "Nederland"`
- `"[problem]" "AI" "conversie" "Nederland"`
- `[global competitor category] Netherlands [industry]`

Absence of exact keywords is not proof of uniqueness; adjacent categories count.

## Service-first / managed-marketplace pattern

When the user asks for Airbnb/Uber-like ideas or simple people-to-people/service marketplaces, use a concierge MVP rather than recommending broad marketplaces.

- Avoid generic “Werkspot but with AI,” “Temper but better,” or broad leadgen/offerte sites.
- Look for narrow wedges where AI/automation improves intake, matching, trust, scheduling, pricing, payments, evidence photos, backup coverage, and follow-up.
- Start with landing page + Tally/Typeform + WhatsApp Business + Google Sheets/Airtable + Mollie/Stripe/Tikkie.
- Validate paid transactions manually before building software.
- Prefer recurring/high-frequency demand: short-stay turnovers, VvE maintenance, landlord repairs, office services, event staffing, practical care relief, subscriptions/memberships.
- Use `references/service-marketplace-ai-ideas-nl.md` for Dutch marketplace gaps, crowded categories, MVP stack, and current best bet.

## Productized audit/retainer pattern

When a validated wedge becomes client delivery, switch from research to SOP execution:

1. **Intake only what is needed**: URL, data source links/exports, priority pages or assets, business priority.
2. **Start with public data when safe**; do not block on perfect access if a free quick-win or sample audit can be produced.
3. **Turn evidence into exact artifacts**: page copy, FAQ answers, trust blocks, priority fixes, scorecards, checklists, or implementation-ready recommendations.
4. **Reject vague advice**. Replace “improve trust” / “optimize copy” / “make clearer” with exact text, exact placement, evidence, and expected impact.
5. **Sell a ladder**: free quick win → paid audit → done-for-you fix → managed retainer.

## Review-to-Revenue / Customer Voice Conversion Audits

Use this subsection when the business is Harry's Review-to-Revenue wedge or any client task that turns reviews/customer feedback into conversion fixes.

### Positioning

Do not position it as generic AI, CRO, review management, or a chatbot. Position as:

> We turn customer reviews into concrete websitecopy, FAQ answers, trust blocks, and page fixes that reduce buyer doubt and improve conversion.

Best first niche: Dutch webshops with 100+ reviews, products above roughly €30, visible product/category pages, and repeated doubt around sizing, quality, delivery, installation, compatibility, returns, or trust.

### Delivery ladder

1. **Free entry: 3 Review Revenue Leaks** — public review scan, 3 concrete leaks, each with review evidence → page problem → exact fix text.
2. **Paid entry: Review-to-Revenue Audit** — analyze 100-300 reviews and key pages; deliver top buying reasons, objections, complaints, return risks, 10 website fixes, 5 copy blocks, 5 FAQ answers, 3 trust snippets, and a priority plan.
3. **Upsell: Audit + Copy Fix** — implementation-ready copy for homepage, PDP, category, FAQ, checkout, return/shipping trust copy.
4. **Retainer: Managed Customer Voice Agent** — monthly review monitoring, new complaint/competitor patterns, and copy/FAQ update recommendations.

### Review source order

1. Client CSV/export from review platform.
2. Public review pages, copied or semi-automated.
3. Official API/feed if client provides access.
4. Browser/scraping only if allowed and necessary.

Platform notes: Trustpilot public reviews/export; WebwinkelKeur API ratings/product-review endpoints with client credentials; Kiyoh XML/API/feed with client access; Shopify/Judge.me/Loox exports through client admin/app; Google Business official access is cleanest, public samples are enough for quick wins.

### Labeling and page comparison

Tag meaningful reviews as buying reason, doubt/objection, complaint/friction, return risk, trust signal, missing product info, delivery/service, sizing/fit/compatibility, emotional trigger, competitor advantage, and FAQ candidate.

Compare at minimum homepage hero/USP, main category page, 3-5 product pages, FAQ/help, shipping/returns, and cart/checkout trust messaging if visible.

### Bundled resources

- `references/review-to-revenue-netherlands.md` — Dutch competitor-map and positioning notes.
- `references/review-to-revenue-delivery-kit.md` — SOP notes, platform blockers, delivery standards.
- `templates/quick-wins-template.md` — copyable 3 Review Revenue Leaks template.
- `templates/paid-audit-template.md` — copyable paid audit report structure.
- `templates/client-intake-message.md` — message to request client inputs.
- `scripts/review_csv_helper.py` — local CSV preprocessing helper for review text.

## Harry output style

For Harry, keep it caveman concise and direct: no academic report tone, no 20 vague options, use clear scores, say when a market is crowded, say when an idea only works with a narrower wedge, and prefer founder-led service validation over building SaaS first.

## Common pitfalls

- Do not confuse “nobody uses our name” with “no competition.” Category competitors matter.
- Do not recommend broad automation bots as a first wedge unless the buyer pain is already narrow and paid.
- Do not sell AI as the headline when the buyer cares about money, time, risk, or conversion.
- Do not let a service become “we optimize everything for everyone.” Narrow the beachhead.
- Do not overbuild. First sell an audit, pilot, or fixed-scope service; automate after proof.
- Do not wait for perfect data exports. Public data is enough for quick wins and proof-of-work.
