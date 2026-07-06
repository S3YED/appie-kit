# Competitor Landing Page Deconstruction

## Overview
Methodology for deconstructing competitor landing pages element by element. Translate → Analyse → Recreate for the client's ICP and offer.

## Step 1: Extract Page Content

**Static pages** — Use `web_extract(url)` — works for most landing pages (even heavy ones). Returns markdown of visible text including headlines, body copy, FAQ, CTA.

**Heavy JS pages** (timeout) — Try `curl -sL URL` in terminal to get raw HTML, then `grep` for specific elements. May not capture dynamically loaded content.

**VSL video** — CANNOT extract spoken script from embedded videos. Be transparent about this. Focus on the visible page copy.

## Step 2: Structure The Analysis

For each section of the page, provide:

| Element | Original | Translation | Why It Works | Your Version |
|---------|----------|-------------|--------------|--------------|

### Sections To Analyse
1. **Hero** — Headline + Subheadline (the pain + solution framing)
2. **Social Proof** — Reviews, ratings, count placement
3. **VSL/Timer Gate** — Structure, duration, gate copy
4. **Transformation Gallery** — Number of results, timeframes, format
5. **FAQ** — Each question + answer translated and analysed for technique
6. **CTA** — Wording, positioning, scarcity language
7. **Coach/About Section** — Personal story, credibility stacking

## Step 3: Identify Copy Techniques

Common techniques used by high-converting fitness landing pages:

| # | Technique | Example |
|---|-----------|---------|
| 1 | Pain in headline | "For men tired of a body they're not proud of" |
| 2 | Kill objections in subheadline | "Without extreme diet, hours in gym, turning life upside down" |
| 3 | No pricing shown | Force to the call |
| 4 | "Claim/Apply" not "Buy" | Lower resistance language |
| 5 | "Investment" not "Cost" | Reframes price |
| 6 | Specific timeframes | "70 days, 45 days, 16 weeks" |
| 7 | "They started where you are" | Identification |
| 8 | Aspirational locations | "London, Dubai, Bali" |
| 9 | Authority stacking | Doctor + psychologist + X years + Y clients |
| 10 | "Personal team" positioning | Not a program — a team around you |

## Step 4: Compare With Client

| Element | Competitor | Client | Gap/Opportunity |
|---------|------------|--------|-----------------|
| Target | Men only | Both genders | Bigger market |
| Mechanism | Unnamed | REP Method | Ownable, teachable |
| Faith | Not mentioned | Core angle | Differentiation |
| Transformation | Physical only | Physical + mental + spiritual | Deeper value |

## Step 5: Write File

Save full analysis as a structured markdown file. Every section should answer:
- What did they say? (translation)
- Why does it work? (psychology)
- What should the client do instead? (adaptation)

## Example: Peak Physique V5 Analysis

Full analysis saved at `/root/ibrahim/peak-physique-analysis.md`. Key findings:
- Headline names shame immediately: "For men tired of a body they're not proud of"
- Subheadline kills 3 objections before they form
- 90-second timer gate forces VSL consumption
- FAQ handles 5 objections (investment, time, online, differentiation, deliverables)
- "Claim my spot" language not "buy now"
- Absence of faith angle, gender inclusion, and named mechanism = opportunities

## Example: Ihsan Blueprint Analysis

Full analysis from web_extract. Key findings:
- Headline promises specific weight loss (50-100lbs) + muscle + discipline
- "ONE DAY? or DAY ONE?" tagline is effective
- Coach story section with faith integration ("trust in my Lord")
- "Muslim Grindset" ownable phrase
- No timer gate, no FAQ, no named mechanism = gaps