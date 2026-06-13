# Review to Revenue Delivery Kit Notes

Condensed from the Review to Revenue setup session.

## Business context

Harry is building `Review to Revenue` as a service-first business. The assistant should eventually execute client delivery while Harry monitors, sells, and approves external/paid/public actions.

Core offer:
- Free: 3 Review Revenue Leaks
- Paid audit: Review-to-Revenue Audit, intro €950
- Upsell: Audit + Copy Fix, €2.500-€5.000
- Retainer: Managed Customer Voice Agent, €750-€2.000 p/m

Core promise:
> Zet klantreviews om in websitecopy die meer omzet oplevert.

## Dutch competitor/positioning insight

Exact Dutch productized competitors were not found. Adjacent competition exists:
- Review management: Trustpilot/Trusted Shops, Kiyoh, WebwinkelKeur, klant.review, Coosto
- CRO agencies/specialists: expert reviews, UX/CRO audits
- Review mining content: Onder.nl, ShoppingTomorrow, Thuiswinkel.org
- Feedback tools: Mopinion, Haan Digital
- AI agents/customer service: SynAI/Daan, ShopPros, OpenKlauw-like AI for webshops

Differentiation:
- review tools collect/show/reply
- CRO agencies audit broad UX/conversion
- AI agents handle support/conversational flows
- Review to Revenue translates reviews into exact websitecopy, FAQ, trust blocks and conversion fixes within 72h

## Delivery standards

Every recommendation must be:
1. backed by review evidence
2. tied to a specific website page/location
3. written as exact copy or exact page fix
4. prioritized by likely impact and effort

Reject vague advice like:
- add more social proof
- improve product copy
- make the page clearer

Rewrite into:
- exact text
- exact placement
- why this reduces doubt or friction

## Review source strategy

Preferred order:
1. client CSV/export
2. public reviews
3. official API/feed with client-provided access
4. scraping only when permitted and necessary

Platform notes found:
- WebwinkelKeur exposes API endpoints for `/1.0/ratings.json` and product reviews XML when client has `id` and `code`.
- Kiyoh has REST/XML/feed options, likely requiring client access.
- Trustpilot public reviews can be exported with public tools, but prefer client export if available.
- Shopify/Judge.me/Loox exports are easiest through client admin/app.
- Google Business reviews need client access for clean export/API; public reviews can support quick wins.

## Blockers encountered

- Exa search was unavailable because `EXA_API_KEY` was missing. Fallback: `web_search` + `web_extract` with explicit note.
- JavaScript scraping skill failed to load with JSON serialization error. Fallback: do not rely on scraping as the primary plan; prefer export/API/public data.
- Domain/email/public launch require Harry account/payment approval.

## Lesson

This business should be built with service delivery first, not software. Build repeatable templates, reports, and review processing helpers before dashboards or SaaS.
