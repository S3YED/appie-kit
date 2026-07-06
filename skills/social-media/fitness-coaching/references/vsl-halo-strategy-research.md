# Sabri Suby Halo Strategy + VSL Framework

## Overview
Full research-to-script pipeline for fitness coaching VSLs. Based on Sabri Suby's $200M+ VSL framework from his YouTube course (Feb 2026). Generated $7.8B across 1,000+ niches.

## Phase 1: Halo Strategy Research (4 Sources)

### Source 1: Reddit
- **Subreddits:** r/fitness, r/xxfitness, r/getdisciplined, r/MuslimLounge, r/loseit, r/workingmoms, r/daddit, r/fitness30plus, r/Hijabis
- **Keywords:** "busy", "dad", "mom", "failed", "consistency", "stuck", "tried everything", "over 30"
- **Tool:** Use `web_search` with site:reddit.com prefix to find relevant threads, then `web_extract` to pull page content

### Source 2: Amazon/Goodreads Reviews
- **Books to mine:** Bigger Leaner Stronger, Thinner Leaner Stronger, Atomic Habits, Discipline Equals Freedom, The Compound Effect, The 4-Hour Body
- **What to extract:**
  - 1-star: complaints, what they hated
  - 3-star: what they wanted but didn't get
  - 5-star: what they loved, what they wish existed
- **Tool:** `web_search` → `web_extract` on the review pages

### Source 3: YouTube Comments
- **Channels to mine:** Athlean X, Jeremy Ethier, Fitness FAQs, Sean Nalewanyj, Kneesovertoesguy, Kinobody, Garage Strength, Ian Barseagle, The Jacked Vegan
- **Also check:** Direct competitors in the client's niche
- **Tool for extracting comments:** Invidious API — `https://inv.zzls.xyz/api/v1/comments/VIDEO_ID` — returns top comments with likes, author, text
- **What to extract:** Pain, desire, objection, identity quotes (verbatim)

### Source 4: Google Forum Foraging
- Use Chrome extension "Discussions" or site: filters
- `site:forum.bodybuilding.com "over 30" "consistency"`
- `site:community.myfitnesspal.com "failed" "motivation"`
- Muslim-specific: `site:reddit.com "Muslim" "fitness" "struggle"`, Muslim Skool communities

## Phase 2: Synthesis

Organise research into:
- **PAIN QUOTES** (verbatim) — top 5 themes ranked by frequency
- **DESIRE QUOTES** (verbatim) — what they actually want
- **OBJECTIONS** — why they won't buy
- **IDENTITY MARKERS** — how they describe themselves (busy dad, tired mum, CEO)

## Phase 3: VSL Script (120 seconds)

### N.U.E.E.P.H. Framework
Every script must hit all 6:
- **N**ew — feels novel, fresh angle
- **U**nique — can't be categorised as "just like X"
- **E**xciting — visceral, heart-pumping transformation vision
- **E**asy — push-button, step-by-step, not complex
- **P**redictable — specific proof, named clients, numbers
- **H**uge — zoom out to bigger stakes (legacy, identity, leadership)

### 8-Step Story Selling Structure

| Time | Element | What To Do |
|------|---------|------------|
| :00-:15 | Attention | Pattern interrupt. Steal verbatim pain from research. No warm up. |
| :15-:35 | Identity (They Are You) | "I was you. Same failures. Same frustration." |
| :35-:55 | Struggle | Agitate their specific pain. Past failed attempts. |
| :55-1:15 | Discovery | How you found the solution. What didn't work. The breakthrough. |
| 1:15-1:30 | Value | Why past solutions failed. How yours works differently. |
| 1:30-1:40 | Hero Mechanism | Named framework (e.g., REP). Branded steps. |
| 1:40-1:50 | Results | Named clients. Specific numbers. Both genders if applicable. |
| 1:50-2:00 | Action | Walk them through the CTA vividly. Why now. |

### REP Method Mechanism (if applicable)
- **R — Replace:** Upgrade behaviours (random → structured, emotional eating → intentional)
- **E — Embody:** Identity shift. "What would ___ do?"
- **P — Pursue:** Compounding progress once identity is aligned

Frame as: "This isn't a workout program. It's an identity upgrade that shows up on your body."

## Phase 4: What To Steal From Competitor Pages

When analysing a competitor landing page:
1. Extract page copy via web_extract
2. Translate if needed
3. For each section: Original → Translation → Why It Works → Your Version
4. Key elements to analyse: hero headline, social proof, VSL/timer gate, transformation gallery, FAQ, CTA

## Key Verbatim Quotes (Universal Pain)
- "I've tried everything. And nothing works."
- "I can't stick to a routine for more than a week."
- "I look in the mirror and feel stuck — ashamed of how I look."
- "Between work, family, and my faith, when am I supposed to find time for me?"
- "I'm tired of being tired."

## Key Verbatim Quotes (Muslim-specific)
- "For the brother who's tired of being tired. For the sister who's sick of fad diets that don't align with our deen."
- "I want to feel strong in my salah, confident in my clothes, and in control of my nafs."
- "Fitness isn't just about looks — it's about fulfilling our amanah, taking care of the body Allah gave us."

## Objections To Handle
| Objection | Response |
|-----------|----------|
| "I've heard this before" | "You've tried programs. You've never tried an identity system." |
| "I don't have time" | "You don't need more time. You need the right 30 minutes." |
| "I'll fail again" | "This isn't built on motivation. It's built on [mechanism]." |
| "Too expensive" | Frame as investment in amanah, not cost |
| "Just another coach" | Unique mechanism + identity framing sets you apart |

## Limitations
- YouTube comments are rate-limited via Invidious API (returns top ~20 comments)
- Some Invidious instances are down/blocked — have alternatives ready
- Facebook Ads Library blocks programmatic access entirely
- VSL spoken script cannot be extracted from embedded videos on landing pages