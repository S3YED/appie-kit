# Service-first marketplace ideas — NL research notes

Use when Harry asks for Airbnb/Uber-like ideas: simple services that connect people, assets, labor, locations, or capacity. This is a different class from AI workflow/compliance/document automation.

## Core lesson

Do **not** recommend broad marketplaces like “Werkspot but with AI” or “Temper but better.” General marketplaces need liquidity and are usually already crowded. The attackable wedge is a **managed niche marketplace**: start concierge/manual with WhatsApp/Tally/Sheets/Mollie, validate paid transactions, then automate intake, matching, trust, scheduling, payment, evidence, and follow-up.

## Research finding

Exa may be blocked in Hermes profiles by missing `EXA_API_KEY`; if blocked, continue with web_search/web_extract and label the fallback. Do not stall.

## NL crowded categories to avoid unless very narrow

- General klus/home services: Werkspot, Zoofy, Trustoo, Homedeal.
- General horeca/flex shifts: Temper, YoungOnes, Staffyou.
- General babysitting: Charly Cares, Sitly, Oppasland.
- General pet sitting: Pawshake, Petbnb.
- General car sharing: SnappCar.
- Restaurant booking: TheFork, Google, TripAdvisor.
- Beauty booking: Treatwell, Salonized.

## Stronger Dutch gaps

Prioritize vertical/managed wedges with recurring use:

1. **Short-stay host operations club** — Airbnb/Booking hosts ↔ cleaners, linen, handymen, keyholders. Recurring every turnover. Start with €99-€299/month host management fee + margin per clean/repair.
2. **Move-out / borg-terug cleaning + small repairs** — expats/students/tenants ↔ cleaners, painters, handymen, waste pickup. Deposit-focused bundle, €249-€899/job.
3. **VvE kluspool / building maintenance desk** — VvE/building managers ↔ vetted handymen/trades. €99-€499/month per VvE + job margin.
4. **Landlord handyman subscription** — private landlords ↔ repair vendors. €49-€199/month + repair margin.
5. **Marktplaats bulky delivery** — secondhand buyers/sellers ↔ vans/student movers. Take-rate per delivery.
6. **Estate cleanout / senior move concierge** — families/seniors ↔ movers, cleaners, kringloop, appraisers, waste pickup.
7. **Senioren practical help / mantelzorg relief** — non-medical only unless compliance is handled.
8. **Special-needs pet care** — medical/anxious pets ↔ vet assistants/trainers/experienced sitters.
9. **Shared commercial kitchen hours** — foodtrucks/caterers/startup bakers ↔ certified kitchens off-hours.
10. **Bouwmateriaal runner service** — contractors/installers ↔ runners/van owners for urgent missing parts/materials.

## Concierge MVP stack

- Landing page: Carrd/static HTML.
- Intake: Tally or Typeform.
- Matching/CRM: Google Sheets or Airtable.
- Communication: WhatsApp Business + labels/templates.
- Payment: Mollie/Stripe Payment Links/Tikkie.
- Planning: Google Calendar/Calendly.
- Ops: Notion/Google Docs SOP + checklists.
- Automation later: Make/Zapier/n8n, WhatsApp API, provider dashboard, Stripe/Mollie Connect.

## Validation rules

14-day go criteria:
- 5+ paid transactions or 2+ monthly memberships.
- 30%+ gross margin possible.
- Customers ask for repeat service.
- Supply accepts platform rules and responds quickly.

Kill criteria:
- Demand wants only information, not payment/deposit.
- Supply is unreliable or too expensive to keep margin.
- Matching is generic enough that customers can easily do it themselves.

## Best current first bet

Short-stay host operations club.

Positioning: “Wij regelen je turnover-operatie: schoonmaak, linnen, kleine fixes en bewijsfoto’s. Geen losse app. Elke check-out strak geregeld.”

First paid offer: €149/month management fee per host + cost-plus cleaning/repair with ~20% margin.

First actions:
1. Build host + cleaner Tally intake.
2. Build list of 50 short-stay hosts/property managers in Amsterdam/Rotterdam/Den Haag.
3. Recruit 10 cleaners/handymen and close 5 paid turnovers manually.
