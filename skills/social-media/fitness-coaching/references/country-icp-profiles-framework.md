# Country ICP Profile Framework — Ad Scripting

When a client wants geographically-targeted ads, build **country-specific ICP profiles** first — before writing a single line of ad copy. This framework was developed for Ibrahim Ramzy / The Creed (fitness coaching, Muslim high-performers 25-45, both genders).

---

## Why Profiles First

The user's exact words: *"I want to build out the profiles of my ideal client and then I can create the copywriting that goes within them."*

Do NOT jump to writing the ad. Start with:
1. Country
2. Gender (men, women, or both)
3. Local pain specific to that country
4. Testimonial templates that feel local
5. CTA that fits the culture
6. Verbatim pain language (the exact words they use)
7. Headline angles using Sabri's formulas

---

## Profile Structure Template

Each country profile should contain:

| Section | Content |
|---------|---------|
| **Country flag + name** | 🇦🇪 UAE — Dubai / Abu Dhabi |
| **Target** | Gender, age range, occupations, lifestyle |
| **The Person** | 2-3 sentence description of who they are |
| **Primary Pain (Named)** | Bold one-liner + paragraph expanding |
| **Sub-Pains** | Bullet list of secondary pains |
| **Verbatim Pain Language** | Their exact words from research |
| **Testimonial Template** | Fill-in-the-blank format + named example |
| **CTA Formulas** | 2-3 CTA options that fit the culture |
| **Headline Angles** | 3-4 headline ideas using Sabri's formulas |

---

## Example: UAE Profile

```
🇦🇪 UAE — Dubai / Abu Dhabi

TARGET: Both men and women. 28-45. Finance, tech, real estate, consultancy, entrepreneurship.
LIFESTYLE: High income, long hours, app-dependent, car-dependent, AC-dependent.

THE PERSON: On paper, you've made it. Good salary. Nice apartment in Marina or Downtown.
But your body doesn't reflect your success.

PRIMARY PAIN (The Golden Cage): "I earn well but my body is paying the price."
Every meal ordered from an app. AC and traffic all day. Tried every PT in the building gym,
every wellness clinic, every biohacking gadget — all surface. Botox before bloodwork.
Aesthetics before health.

SUB-PAINS:
• No real community — transient city, hard to build accountability
• Heat kills outdoor exercise 6 months a year
• Work never stops — WhatsApp 24/7
• Brunch culture + Deliveroo at 11pm = metabolic disaster

VERBATIM PAIN LANGUAGE:
• "I've tried every PT in my building"
• "I work 12 hour days — when am I supposed to train?"
• "Ramadan kills my progress every year"

TESTIMONIAL TEMPLATE:
"[Name], [job] in [city]. [Start] → [Result] in [timeframe]. Trained from [location]."
Example: "Omar, strategy consultant in Dubai. Stuck at same weight 2 years.
Down 8kg in 12 weeks. Training at 6am before the market opens."

CTA FORMULAS:
• "Book your deep dive call. 15 minutes. I'll show you where your body is leaking progress."
• "Apply below. If [Name] can do it with their schedule, so can you."

HEADLINE ANGLES (Sabri's formulas applied):
• "6 ways to get your body back without quitting your Dubai job" (Formula 1)
• "How to eliminate belly fat without giving up brunch — in 90 days" (Formula 4)
• "The dirty truth about 'wellness' in Dubai revealed" (Formula 9)
```

---

## Delivery: Google Doc in Client's Drive

Use the Google Docs API to create a structured doc the client can open, edit, and reference:

1. Generate auth URL via `gws-wrapper auth login --full`
2. User approves with their work email
3. Exchange auth code for tokens
4. Create doc via `POST https://docs.googleapis.com/v1/documents`
5. Populate with batchInsert requests
6. Share the URL

Reference script: `scripts/create-icp-profile-doc.py`

---

## Known Country Profiles (Ibrahim Ramzy)

See the Google Doc at:
https://docs.google.com/document/d/1dH-uxNsSDMje6Yla3fAt2XroXc0avtaMpp3PgrZp89M/edit

Profiles created:
- 🇦🇪 UAE — The Golden Cage
- 🇬🇧 UK — The Grey Ceiling
- 🇺🇸 USA — Death by Information
- 🇦🇺 AUS — The Comparison Trap
- 🌍 Europe — The Efficient Decline