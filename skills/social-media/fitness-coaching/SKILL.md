---
name: fitness-coaching
description: "Content, funnel, and communication workflows for personal trainers and fitness influencers."
version: 1.5.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [fitness, coaching, content, funnel, influencer, social-media, giveaway, low-ticket]
    related_skills: [humanizer, youtube-content, notion, typingmind-api]
---

# Fitness Coaching & Influencer Operations

For personal trainers, fitness coaches, and influencers who treat their digital presence as a business pipeline. Covers content creation, funnel optimisation, community management, giveaway campaigns, and recurring operational workflows.

## Communication Style

- **English ONLY.** Do not switch languages. If the client communicates in one language, stay there — do not mirror, do not offer alternatives.
- **No em dashes.** Use commas, colons, or regular hyphens instead. User will flag em dashes.
- **Concise and action-oriented.** Fitness audiences skim. Lead with the hook, deliver value fast, close with a CTA.
- **Motivational but sharp.** Direct feedback. No corporate filler. No AI framing ("as an AI", "I don't have access to...").
- **Short paragraphs.** One idea per paragraph. Let white space do the work.
- **No AI disclaimers or meta-commentary.** Never say "as an AI" or "I can't do X". If something isn't possible, say why plainly in one sentence and offer the next best step.
- **Hero headings max 2 lines.** On landing pages, keep the main headline short enough to fit 2 lines on mobile.

## Content & Landing Page Rules

### Landing Page Structure (High-Ticket Coaching)
- VSL with autoplay muted → 90-second timer gate (sessionStorage persisted) → content unlocks
- Sections: Hero → VSL → Timer Gate → Transformations (8 before/after cards) → Testimonials (8 video cards) → FAQ → Typeform → Footer
- Hero padding: `100px 20px 60px` (sits high on the page)
- Flood social proof: 8 transformation cards + 8 testimonial videos minimum
- Typeform embedded at the bottom with `data-tf-widget`

### Low-Ticket Funnel (e.g. $99/mo group coaching)
- Same layout as high-ticket BUT:
  - No timer gate needed (lower commitment offer)
  - Simplified Typeform: no budget/investment question, no Calendly booking
  - "Does this look like what you're looking for?" Yes/No gate in Typeform
  - Yes → "Why now?" → contact info → payment redirect
  - No → "What's missing?" → contact info → redirect to high-ticket page
- FAQ copy changes: emphasise "cancel anytime", "no contracts", "try for a month"
- Add pricing card section with monthly price

### Giveaway Funnel (Lead Gen via Contest)
- Prize structure: 1st = free coaching (e.g. 12 weeks, valued $5K), 2nd/3rd = discount, everyone = exclusive offer

**Typeform structure — two variants:**

**Full version (high-intent traffic, ads/email):**
- Welcome screen with prize value + deadline (14 days)
- "What made you join? Current situation?" (long text)
- "How would your life change if you won?" (long text — vision)
- "Why now? Cost of staying the same?" (long text — urgency)
- Commitment score (1-10 opinion scale) — winner ranked on seriousness
- Contact info (name, email, phone)
- Instagram handle
- WhatsApp opt-in (yes/no)
- Profession (for profiling)
- Country (with DQ gate for Asia/Africa/South America — but still capture contact info)
- "If you don't win, still interested at a discount?" (pre-qualifies buyable leads)

**Lightweight variant (Instagram stories, short attention span) — PROVEN HIGHER CONVERSION:**
- 4 fields, 90 seconds max. No country gate, no Instagram, no profession, no welcome statement, no opinion scale.
- Q1 (MC — hook/identity): "What's the real reason you're here?"
  - "I'm disciplined everywhere else. This is the last piece."
  - "I know the blueprint. I just need someone to hold me to it."
  - "I want to look in the mirror and see the version I know I am."
  - "I'm tired of being my own biggest obstacle."
  - "I've built everything else. Now I'm building the body that carries it."
- Q2 (long text — pain/deep dive): "What's the main struggle holding you back in your health? Why?"
- Q3 (short text — vision): "In one line, what would transforming in 12 weeks do for you?"
- Q4 (contact_info): Name, Email, Phone only
- **Psychology:** Face truth (EMC hook) → Admit struggle (pain) → Paint vision (future pull) → Give contact info (highest commitment, lowest perceived risk after investment)
- **CRITICAL — 64% drop-off fix: First question MUST be ASPIRATIONAL, not shame-based.** This is a PROVEN improvement from a live giveaway form. The original Q1 asked "What's really made you want to enter?" with options like "I keep starting over," "I've let myself go," "I'm sick of failing." It caused 64% drop-off on the very first screen. Switching to aspirational copy that speaks to the ICP's identity (successful person with untapped potential) fixed it. Rules:
  - Never frame the first question around failure, shame, or "starting over"
  - High-performer ICP sees themselves as UNLOCKED POTENTIAL, not broken
  - Target the tension: "I do hard things all day. Why can't I do this one for myself?"
  - Options should let the user SELECT an identity, not ADMIT a flaw
  - Proven options (from live form, 64% drop-off fixed): "I'm disciplined everywhere else. This is the last piece" / "I know the blueprint. I just need someone to hold me to it" / "I want to look in the mirror and see the version I know I am" / "I'm tired of being my own biggest obstacle" / "I've built everything else. Now I'm building the body that carries it"
- **No country gate** — country disqualification for giveaway leads was explicitly removed. All entries captured regardless of location.
- **Use when:** promoted from Instagram, goal is lead volume, follow-up process (WhatsApp) handles deeper qualification
- **Use full version when:** promoted via ads/email (higher intent), country restrictions critical, need Instagram handle for repurposing

**Landing page structure (giveaway):**
- Hero (badge + prize value) → VSL → How to Win (3 steps) → Prizes → Transformations → Testimonials → What's Included (3 pillars) → Features → Typeform
- VSL placed BETWEEN hero and How to Win (proven layout)
- Button text: "Enter the Giveaway" (not generic "Enter Now" or "Enter the Challenge")
- Subtitle messaging: "Your entry gets you access to a once in a lifetime offer. So there's nothing to lose."

**Giveaway lead management (post-entry):**\n- Commitment score determines priority tier and sequence speed\n- Tier 1 (10/10): Fast track — call invite Day 3-4, 2 value drops, final check Day 12-13\n- Tier 2 (8-9/10): Value first — check-in Day 3-4, call invite Day 5-6\n- Tier 3 (7 and below): No calls — nurture only with value, pivot to low-ticket after giveaway\n- VA handles WhatsApp messaging using scripts in Ibrahim's voice ("I" not "Ibrahim will")\n- Create a clean PDF process doc for VA handoff with tiers, scripts by day, daily checklist, quick reference table\n- Ibrahim handles all calls and closings — VA flags booked calls and strong answers\n- See `references/giveaway-lead-management.md` for the full process template\n- **CRITICAL BOUNDARY:** VA sends WhatsApp messages ONLY. Do NOT write call scripts or sales pitches in the VA docs. Ibrahim explicitly rejected the phrase "I can hold a spot for you after the giveaway" as a first-call tactic. The VA doc must be purely operational: what message to send, when, and who to escalate. See `references/giveaway-lead-management.md` for the full process template.
- **WhatsApp from server (post-entry follow-up):** The `wacli` CLI tool can send follow-up messages to leads automatically from the server. Requires phone-linked auth via QR or pairing code. See `communication/wacli` skill for headless auth setup. **Proven headless auth method (July 2026):** Use `tmux new-session -d -s wacli-pair -x 500` then `tmux send-keys -t wacli-pair "wacli auth --phone '+44...'" Enter`. Wait 8s, capture code with `tmux capture-pane`. This avoids all background-terminal output-buffering issues. QR method (`--qr-format text`) also works but requires generating a PNG and sending via MEDIA: image — phone pairing is simpler for the user. If rate-limited (429), wipe session.db, wait 30-60 min, and retry. See `references/whatsapp-wacli-setup.md` for the full rate-limit troubleshooting table.

## Triage Call Qualification (Giveaway Leads)

Used for 15-min triage calls where the coach qualifies leads for a second sales call. Not a pitch — the coach is selecting who deserves to win.

**Core frame:** *"This is 15 minutes for me to hear your real story. Why you entered, what's going on, and why you think you should win. I'll shortlist the best fit."*

**4 questions to qualify every lead:**
1. **The Trigger** — "What happened recently that made you realise you have to sort your health out now?" (Specific event vs vague feeling)
2. **The Life Audit** — "What do you do for work? What does a normal day look like?" (Income stability + schedule reality)
3. **The Commitment Check** — "Have you signed up for programs before and not followed through? What happened? What's different this time?" (Self-awareness vs excuses)
4. **The Belief** — "Deep down, what's the one thing actually holding you back?" (Internal vs external attribution)

**Scoring:** 3 buckets — HOT (real trigger + stable life + takes responsibility), WARM (2 of 4), COLD (vague + no stability + blames everything). After each call: Name / Score / 1-line gut feel.

**Triage call frame update (from live calls, July 2026):**
- The coach opens with the giveaway frame: "15 minutes to hear your real story and why you think you should win. I'll shortlist the best fit."
- The close teases the three-tier prize structure: "I've never done this before — even if you're not first, there's something special for second and third."
- This framing makes it a **selection call**, not a sales call. Power dynamic is inverted — the coach is choosing who deserves it.
- **Key insight:** Don't pitch. Don't sell. Just qualify. The second call is where the offer happens.
**Recording workflow:** Ibrahim records all triage calls → sends recording or notes → agent transcribes → builds a lead profile → uses profile to prep the second call briefing.
**Post-call reporting:** Ibrahim sends "Name / Score (H/W/C) / 1-line gut feel" for each call. Agent logs it.

**Lead profiling notes (from live session, July 2026):** Ibrahim sends raw stream-of-consciousness notes. The agent structures them using this template:
- Demographics (age, location, occupation, family) → current health state → medical context → why now trigger → past attempts → blockers (internal + external) → what they need from coaching → commitment level → financial reality → gut feel verdict with emoji tag
- Style: short staccato sentences and fragments. Not full prose. Bullet-pointed insights.
- See `references/lead-profiling-notes.md` for templates and live examples.

**Post-call workflow:** Record call → transcribe → build lead profile → tag by status → log to CRM → use profile to draft second-call follow-up.

**7 common objections**

**Post-call workflow:** Record call → transcribe → build lead profile → use profile to prep second/sales call.

See `references/triage-call-qualification.md` for the full framework including exact question wording, objection scripts, and scoring rules.

### WhatsApp Contact Management (via wacli)

When managing giveaway leads through WhatsApp from the server:

**Contact sync (name changes from phone):**
- When Ibrahim renames contacts on his phone (e.g. adding "Giveaway" suffix), names sync to the wacli database but may lag
- `wacli contacts refresh --account=creed` pulls latest names immediately (faster than a full message sync)
- `wacli contacts search <keyword>` — search contacts by name or phone (e.g. `wacli contacts search giveaway --account=creed`)
- Account name is typically `creed`, NOT `default` — check with `wacli accounts list` first

**Sending messages:**
- `wacli send text --to "<name-or-jid>" --message "..." --account=creed` — send a WhatsApp message
- `--to` accepts the contact name as shown in wacli (e.g. "Abdullah Jordan Giveaway") or JID
- Can also send files (`send file`), voice notes (`send voice`), react (`send react`)

**CRITICAL: Approval protocol — Do NOT fire messages without Ibrahim approving the exact wording first.**
- Draft one message at a time
- Present it for review with context (who it's going to, why this message)
- Only send after he confirms
- Do not batch-send multiple messages without per-message approval unless he explicitly says "send them all"

**Lead status tags (for local roster tracking):**
Use these emoji prefixes in the lead roster for quick scan:
- 🔥 **VERY HOT** — ready to buy, follow up aggressively
- 🔥 **HOT** — strong fit, needs one more touch
- 💎 **WARM** — good potential, needs nurturing
- 🟢 **New** — not contacted yet
- ❌ **Cold** — not ICP or can't afford

### Call Funnel Tracking (No CRM API Available)

GHL V1 API deprecated 31 Dec 2025. V2 requires OAuth/JWT (pit- tokens from Company Settings don't work). The reliable lead-tracking approach is a **local JSON CRM** maintained by the agent.

**Workflow:**
1. Agent imports new leads from the lead database into `/root/creed-crm.json`
2. Agent sends Ibrahim morning status (who needs calls, who ghosted, new entries)
3. Ibrahim reports back after calls: "Called Ahmed, good fit. Called Sarah, not ready."
4. Agent updates CRM and sends next-day priorities

**Commands (run via `scripts/creed-crm.py`):**
- `python3 /root/creed-crm.py import` — import new leads
- `python3 /root/creed-crm.py status` — full status + next actions
- `python3 /root/creed-crm.py update "email" "triage_done" "Notes"` — update a lead

See `references/lead-crm-tracking.md` for full details and the daily summary format.

### Landing Page Copy Preferences
- Hero heading: 2 lines max. Keep tight: "Win 12 Weeks 1:1 Coaching". Do NOT include "With Ibrahim Ramzy" in the hero headline - it reads cleaner without it in bio context. Keep his name in body copy and testimonials.
- No em dashes anywhere. Use regular hyphens instead.
- CTA buttons: specific to action ("Enter the Giveaway", "Join Health in Motion", "Reserve My Spot")
- All testimonials from the high-ticket page should be carried over (8 transformation cards + 8 video testimonial cards)

## Technical Workflows

### Typeform Creation (Two-Step Pattern)
Many Typeform features (thankyou screens, logic with yes_no fields) can't be created in a single POST. Use the two-step pattern:
1. POST to create the form with fields and settings only (no logic, no thankyou_screens)
2. GET to retrieve the form (captures auto-generated IDs and thankyou screen refs)
3. PUT to add logic and thankyou screens using the correct refs from step 2

Key Typeform details:
- Default thankyou screen ref is usually `default_tys`
- yes_no field choice refs are NOT "Yes"/"No" — use `multiple_choice` type with explicit refs instead
- Country DQ: use `op: "is"` with `{type: "field", value: "ref"}`, `{type: "choice", value: "ref"}`
- Profession DQ: use `op: "equal"` with `{type: "constant", value: "Student, unemployed, inbetween jobs"}`
- Contact_info field uses nested `fields[]` array, not flat properties
- Statement fields don't need `validations` block
- Top-level `language` field not allowed (goes inside settings)
- `thankyou_screens` go at top level, not inside settings

### Vercel Video Hosting (Avoid 100MB File Limit)
Vercel's free plan has a **100MB per-file upload limit**. The CLI combines all files in the directory, so total deployment size can exceed 100MB. Strategy:
- Deploy videos to ONE Vercel project (e.g. `thecreed-one.vercel.app` or `ibrahim-static.vercel.app`)
- Reference them from other projects using the full URL: `src="https://<existing-project>.vercel.app/videos/video.mp4"`
- Only deploy poster images locally (small files, ~100KB total)
- **If a video is over 100MB raw:** compress first with ffmpeg before deploying. Use `-crf 28` to balance quality/size.
  ```bash
  ffmpeg -i input.mp4 -c:v libx264 -crf 28 -c:a aac -b:a 128k -movflags +faststart output.mp4
  ```

**VSL audio quality pitfall:** Aggressive compression (`-b:a 64k`) destroys voice clarity. Always use at least `-b:a 128k` for VSLs where the user is speaking directly to camera. 128kbps AAC is the floor for spoken-word quality.

- **If you can't access the main project's source** (no cloned repo, no local copy): create a fresh minimal Vercel static project with just the video files, then reference from that new URL:
  1. Create directory with `videos/vercel.json` + `videos/` + `posters/`
  2. Run `vercel deploy --yes --token=$TOKEN --scope=creed-ramzy`
  3. Run `vercel --prod --yes --token=$TOKEN --scope=creed-ramzy` to promote
  4. Reference as `https://<new-project>.vercel.app/videos/steven.mp4`

### Vercel API + Static Site (Pitfall)
If a Vercel project uses `@vercel/static` as its build config (e.g. `{"builds": [{"src": "/*", "use": "@vercel/static"}]}`), **API routes (`api/*.js`) will not work** — Vercel treats everything as static files. Solutions:
1. **No vercel.json at all** — Vercel auto-detects both static files and serverless functions. This is the simplest option.
2. **Explicit build config** — List both static and node builds:
   ```json
   {
     "builds": [
       { "src": "api/*.js", "use": "@vercel/node" },
       { "src": "*.html", "use": "@vercel/static" },
       { "src": "*.{mp4,png,jpg,webp}", "use": "@vercel/static" }
     ],
     "routes": [
       { "src": "/api/(.*)", "dest": "/api/$1" },
       { "src": "/(.*)", "dest": "/$1" }
     ]
   }
   ```
3. **Auto-detect routes only:**
   ```json
   { "version": 2, "routes": [
     { "src": "/api/(.*)", "dest": "/api/$1" },
     { "handle": "filesystem" }
   ]}
   ```
**Key rule:** If you add `builds` to vercel.json, you must include ALL file types. The `@vercel/static` build config overrides default auto-detection.

### Media Embed Pattern: Match Existing First
**CRITICAL RULE:** When adding media (video, image, embed) to an existing page, ALWAYS check what pattern the page already uses and match it exactly. Do not introduce a new embed method.
- If all testimonials use native `<video controls>` tags → new testimonials get `<video>` tags, not iframes
- If they use `<img>` tags → new images get `<img>` tags
- Source the URL scheme the page already uses (relative paths or full URLs)
- **Common Ibrahim page patterns:**
  - Testimonials: inline `<video controls playsinline preload="metadata" poster="..." style="width:100%;border-radius:12px;margin-bottom:12px">`
  - Transformations: `<img src="https://thecreed-one.vercel.app/transformations/name.jpg">`
  - Typeforms: `data-tf-live` attribute embed (not iframe)
- If you're unsure, inspect the page source first. Never guess.
- **Consequence of getting this wrong:** The embed looks different from everything else on the page, breaks the visual consistency, and frustrates the client who has to tell you to fix it.

### OCR Fallback (When vision_analyze Unavailable)
When the active model has no vision capability, use tesseract as fallback:
```bash
tesseract /path/to/image.jpg stdout 2>/dev/null
```
Check availability: `which tesseract`

## Funnel Optimisation Principles

- **ICP: Muslim high-performers (men AND women) 25-45 globally** — already fit but hitting plateaus, not beginners
- **Ad copy: Number + Pain + Dream outcome** in one line. Test multiple hooks with same body copy
- **Lead rescue over cold acquisition** — re-engage existing pipeline contacts before spending on new traffic
- **Low-ticket as front-end** to high-ticket upsell. Not a standalone business line
- **Giveaway leads: everyone gets contacted** — winner gets coaching, disqualified (wrong country) still get contacted for digital offers
- **Qualification logic:** country + profession/student status both gate the high-ticket funnel; low-ticket needs only country gate
