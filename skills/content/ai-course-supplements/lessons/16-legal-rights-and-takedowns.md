---
name: 16-legal-rights-and-takedowns
title: TOS, DMCA, deepfake laws, jurisdiction
fills_gap: Course says "AI content is allowed on Fanvue, banned on OnlyFans" and stops there. Doesn't cover EU AI Act enforcement (live August 2026), the Tennessee ELVIS Act, DMCA takedown procedure, right-of-publicity exposure when a Flux character resembles a real person, IRS 1099-K thresholds, or EU VAT. Operating without these = bans, lawsuits, or six-figure tax surprises.
course_module: AIIC V2 Vault (Fanvue setup), generally absent from rest of course
date_researched: 2026-05-07
---

# TOS, DMCA, deepfake laws, jurisdiction

## Why this lesson exists

The course's only legal content is "Fanvue allows AI; OnlyFans doesn't." True in 2024. In 2026 the perimeter is larger: EU AI Act Article 50 transparency obligations live **2 August 2026** (deepfake disclosure required); Tennessee ELVIS Act (eff. July 2024) extends right-of-publicity to voice + secondary liability for tool providers; Fanvue allows AI but enforces labeling rules; Meta's NSFW policy is a 4-tier enforcement system; IRS 1099-K threshold reset to $20k + 200 transactions for 2026 (OBBB); Fanvue handles EU VAT but creators owe income tax in their own jurisdiction.

A creator operating without these will hit a wall: account bans, failed DMCA counter-notices because the work was never registered, or a March 2027 tax bill that wipes a year of margin.

## What's the 2026 state of the art

### Fanvue TOS specifics
Fanvue **explicitly permits AI-generated content** with mandatory labeling and creator-account disclosure. Fanvue's Help Center "Is AI content allowed on Fanvue?" article (updated Aug 2025): allowed when (a) content is original to the creator, (b) AI status is disclosed on the profile, (c) no real-person likeness without consent, (d) no minors / no non-consensual content. https://help.fanvue.com/en/articles/9538738-is-ai-content-allowed-on-fanvue · https://legal.fanvue.com/creator-terms · https://legal.fanvue.com/terms-conditions · https://legal.fanvue.com/content-moderation

OnlyFans bans AI-only profiles. Patreon, Reddit r/Fanvue and adjacent platforms are stricter than Fanvue. Treat Fanvue as the default monetization endpoint; do not cross-post to OnlyFans.

### Meta AI-NSFW gray zone
Meta's adult-nudity-and-sexual-activity Community Standards Enforcement Report shows enforcement continues to climb on Instagram (transparency.meta.com data). The Oversight Board's "Reported AI-Generated Sexualized Video" precedent set the standard: AI-generated sexualized content of real persons is removable; suggestive AI-generated content of fictional persons is policed by the standard 4-tier system but not categorically banned. https://transparency.meta.com/oversight/oversight-board-cases/reported-ai-generated-sexualized-video/ · https://b9-agency.com/blog/nsfw-instagram-policy-2025

For AI creators: keep IG content suggestive, not explicit. Keep explicit content on Fanvue. Lesson 9 has shadowban specifics.

### EU AI Act Article 50 — applicable 2 August 2026
Required of providers (you, when you generate the content) and deployers (you, when you publish it):
- Machine-readable label that the content is AI-generated (metadata, watermark).
- Human-visible disclosure for deepfakes "no later than at the time of first interaction or exposure" — distinguishable, regardless of artistic quality, regardless of intent.
- Voluntary EU Code of Practice (final draft expected mid-2026) provides safe harbor; signing is the cheapest compliance path for small creators.

For AI creators: add metadata via C2PA-compliant tags on your renders (ComfyUI has the `c2pa-comfy-node` for this) and add a "AI / digital persona" line to IG bio + Fanvue profile. https://truescreen.io/insights/ai-act-article-50-labelling-synthetic-content-august-2026/ · https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content · https://www.ypog.law/en/insight/ai-labelling-under-the-ai-act-an-operational-guide-for-providers-and-deployers-of-ai-systems

### US deepfake / right-of-publicity law (state patchwork)
- **Tennessee ELVIS Act** (eff. 1 July 2024). Expanded right-of-publicity to voice, including soundalikes and simulations. Adds **secondary liability** for tool providers — anyone distributing software that enables unauthorized voice cloning. Misdemeanor + civil. https://www.lexology.com/library/detail.aspx?g=709f4b97-e043-4152-9b87-aafc9b2489ed · https://www.adamsandreese.com/insights/elvis-act-tennessee-safeguards-against-deepfakes · https://natlawreview.com/article/king-back-digital-era-elvis-act-generative-ai-and-right-publicity
- **NY Civil Rights Law §§50-51 + revenge-porn extensions**: AI-generated sexual content of identifiable individuals is actionable.
- **CA, IL, TX, FL, VA, WA**: each has 2024-2026 deepfake bills passed or pending — generally targeting non-consensual sexual imagery and political deepfakes. The patchwork means national release of any creator content needs to assume the strictest applicable state.

For AI creators: keep your character demonstrably synthetic. If a face accidentally resembles a real celebrity (common with random LoRA training pulls), regenerate. Quinn Emanuel's white paper on right of publicity in the AI age: courts weigh "degree of resemblance × commercial use." https://www.quinnemanuel.com/media/rxcfnm1y/the-right-of-publicity-in-the-ai-age.pdf · https://www.americanbar.org/groups/business_law/resources/business-law-today/2023-august/whats-real-whats-fake-the-right-of-publicity/ · https://www.americanbar.org/groups/intellectual_property_law/resources/landslide/archive/deepfakes-deepfame-complexities-right-publicity-ai-world/

### DMCA takedown procedure (when your content is stolen)
US 17 USC §512: notice-and-takedown for hosted content. Standard creator path:
1. Locate infringing copy. Document URL, screenshot, timestamp.
2. File DMCA takedown notice with the host (most platforms have a form). Include identification of original work, identification of infringing material, sworn good-faith statement, contact info, and electronic signature.
3. Host removes within 24-72 hours typically; counter-notice from infringer is rare for AI content because they'd have to identify themselves under penalty of perjury.
4. Optional: register the work with the US Copyright Office (Form VA for visual, $45-65). Required if you want statutory damages ($750-$30k/work, up to $150k for willful) in litigation.
5. Note: AI-only generated work is **not copyrightable** in the US per the 2023 Copyright Office guidance (Thaler v Perlmutter affirmed). Your registrable claim is in the human-authored compilation, selection, or modification — not the raw AI render. https://www.copyright.gov/dmca/ · https://heimlichlaw.com/blog/dmca-takedown-notices-complete-guide-for-creators/ · https://getaitoolhub.com/articles/dmca-and-ai-content-copyright-2026

### IRS 1099-K threshold (2026)
OBBB reset the threshold back to **$20,000 AND 200 transactions** for third-party settlement organizations. Below that, no Form 1099-K is issued — but you still owe income tax on all earnings.

For Fanvue payouts (US creators): if Fanvue's payment partner (Stripe/etc.) hits $20k + 200 txn through your account in a year, expect a 1099-K. File Schedule C as self-employed creator; deduct Spark amortization, RunPod / SaaS opex, software subscriptions, internet, percentage-of-rent home office. https://www.irs.gov/newsroom/irs-issues-faqs-on-form-1099-k-threshold-under-the-one-big-beautiful-bill-dollar-limit-reverts-to-20000 · https://www.irs.gov/businesses/understanding-your-form-1099-k · https://boomtax.com/1099-forms/form-1099-k-reporting-threshold

### EU VAT (NL ZZP / BV creators specifically, given operator profile)
Fanvue is UK-incorporated. It applies and remits VAT on EU-resident subscriber payments under the UK-EU agreement. Creator receives net of VAT. NL ZZP / BV creator still must:
- Register for VAT (BTW) if NL turnover crosses €20k threshold (2026).
- Apply Dutch BTW on customs invoiced direct to NL customers.
- File quarterly BTW returns.
- Income tax (IB) on net profit applies regardless. NL BV recommended for creators projecting >€60k/year for the 19% corporate rate vs progressive IB. https://help.fanvue.com/en/articles/7860519-how-does-fanvue-handle-vat · https://help.fanvue.com/en/articles/7860767-do-fanvue-creators-pay-tax · http://eurotradeconcept.nl/dutch-bv-for-influencers-and-content-creators-legal-and-tax · https://eubiztools.com/vat-calculator/vat-digital-services-eu/ · https://legal.fanvue.com/creator-earnings-payouts

## How to set it up on Spark (operational checklist)

1. **C2PA metadata** on every export: `pip install c2pa-python` and bake a manifest into ComfyUI saves with creator name + AI-tool fingerprint.
2. **Boilerplate Fanvue / IG bio line**: "Digital creator. Content includes AI-generated material." Satisfies Fanvue creator-disclosure rule + EU AI Act deployer obligation.
3. **Watermark / AI tag** in ComfyUI workflow: `c2pa-comfy-node` after VAE decode.
4. **Content-release form** for any human contributors (voice samples, motion-capture, anyone who lends a body part to a training set). Keep on file. Standard photographer's release form template adapted for AI training.
5. **Copyright registration**: register your top 20 best-selling images / videos as a quarterly batch with the US Copyright Office (Form VA, ~$65 group). Costs <$300/year, unlocks statutory damages.
6. **Tax bookkeeping**: dedicated business account, separate from personal. NL ZZP: use Moneybird or e-Boekhouden. US LLC: Wave or QuickBooks Self-Employed. Reconcile monthly.
7. **DMCA-ready folder**: store original prompt files, ComfyUI workflow JSON, generation timestamp, and final exports. Originality is provable from the workflow + seed + checkpoint hash.
8. **Jurisdiction split**: NL operator with US audience → consider US LLC + NL holding for IP licensing structure once revenue >$10k/month. Talk to a cross-border tax accountant before the structure goes live.

## Quality benchmarks (compliance levers)

- DMCA takedown success rate: >95% for AI-creator content on cooperative hosts (Reddit, Twitter/X, Pinterest, Discord). Slower on shady mirror sites; use the host's upstream provider or registrar instead.
- EU AI Act fines: up to 3% of worldwide turnover or €15M for transparency violations (Article 99). Disclosure costs you literally one bio line.
- Right-of-publicity exposure: Tennessee statutory damages $5k+ per work; California (CA Civ Code §3344) similar. Re-rolling a Flux character that accidentally resembles a celebrity costs pennies; defending the suit costs >$50k.
- 1099-K mismatch: if IRS shows $25k 1099-K and your return shows $15k, automatic AUR (Automated Underreporter) notice. Match exactly.

## Common failure modes + fixes

- **Bio doesn't disclose AI** → Fanvue can suspend; EU AI Act enforcement after 2 Aug 2026 risks fine. Add the line.
- **LoRA trained on celebrity dataset** → right-of-publicity exposure even if you "didn't intend" the resemblance. Re-train or regenerate.
- **AI voice clone of real person** without consent → ELVIS Act applies even if buyer/distributor isn't in TN; venue can be where the harm occurred. Don't.
- **Selling NSFW of real person** → revenge-porn / NCII statutes apply in most US states + UK + EU. Hard ban.
- **Underreporting Fanvue income** → 1099-K trips IRS AUR; penalty + interest + potential fraud assessment.
- **Cross-platform repost OnlyFans → Fanvue** → instant ban under OnlyFans TOS. They monitor.
- **Forgetting NL BTW threshold** → Belastingdienst surcharge + interest.

## When to choose this over the course's recipe

- **Always**, before launching a new creator into a EU/US-facing market.
- **Always**, when scaling past $5k/month — the cost of getting the structure right is dwarfed by the tax efficiency once revenue is real.
- **Always**, when generating any content that depicts a recognizable person (consent + release, or don't ship).
- **Stick with Herman's "AI is allowed on Fanvue"** as the entry premise, but treat this lesson as the perimeter rule set you operate inside.

## Sources

- https://help.fanvue.com/en/articles/9538738-is-ai-content-allowed-on-fanvue
- https://legal.fanvue.com/terms-conditions
- https://legal.fanvue.com/creator-terms
- https://legal.fanvue.com/content-moderation
- https://help.fanvue.com/en/articles/7860519-how-does-fanvue-handle-vat
- https://help.fanvue.com/en/articles/7860767-do-fanvue-creators-pay-tax
- https://legal.fanvue.com/creator-earnings-payouts
- https://transparency.meta.com/oversight/oversight-board-cases/reported-ai-generated-sexualized-video/
- https://transparency.meta.com/data/community-standards-enforcement/adult-nudity-and-sexual-activity/instagram
- https://b9-agency.com/blog/nsfw-instagram-policy-2025
- https://truescreen.io/insights/ai-act-article-50-labelling-synthetic-content-august-2026/
- https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content
- https://www.ypog.law/en/insight/ai-labelling-under-the-ai-act-an-operational-guide-for-providers-and-deployers-of-ai-systems
- https://link.europa.eu/QW4wNh
- https://www.lexology.com/library/detail.aspx?g=709f4b97-e043-4152-9b87-aafc9b2489ed
- https://www.adamsandreese.com/insights/elvis-act-tennessee-safeguards-against-deepfakes
- https://www.lw.com/en/admin/upload/SiteAttachments/The-ELVIS-Act-Tennessee-Shakes-Up-Its-Right-of-Publicity-Law-and-Takes-On-Generative-AI.pdf
- https://natlawreview.com/article/king-back-digital-era-elvis-act-generative-ai-and-right-publicity
- https://www.quinnemanuel.com/media/rxcfnm1y/the-right-of-publicity-in-the-ai-age.pdf
- https://www.americanbar.org/groups/business_law/resources/business-law-today/2023-august/whats-real-whats-fake-the-right-of-publicity/
- https://www.americanbar.org/groups/intellectual_property_law/resources/landslide/archive/deepfakes-deepfame-complexities-right-publicity-ai-world/
- https://www.copyright.gov/dmca/
- https://heimlichlaw.com/blog/dmca-takedown-notices-complete-guide-for-creators/
- https://getaitoolhub.com/articles/dmca-and-ai-content-copyright-2026
- https://www.irs.gov/newsroom/irs-issues-faqs-on-form-1099-k-threshold-under-the-one-big-beautiful-bill-dollar-limit-reverts-to-20000
- https://www.irs.gov/businesses/understanding-your-form-1099-k
- https://www.irs.gov/pub/taxpros/fs-2025-08.pdf
- https://boomtax.com/1099-forms/form-1099-k-reporting-threshold
- http://eurotradeconcept.nl/dutch-bv-for-influencers-and-content-creators-legal-and-tax
- https://eubiztools.com/vat-calculator/vat-digital-services-eu/
