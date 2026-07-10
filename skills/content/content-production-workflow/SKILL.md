---
name: content-production-workflow
description: End-to-end workflow for creative review gates, content drafting, and publishing to blogs, Notion, and social channels with explicit approval checkpoints.
---

# Content Production Workflow

Use this skill for content work that needs both a clear approval gate and a reliable publishing path. It covers short-form creative review packs, blog/article drafting, and platform-specific publishing checks.

## When to use
- The user wants a review pack before final production or publication.
- You are drafting, refining, or publishing content for a brand or publication.
- The work needs a pause point for human curation before expensive downstream steps.
- You need to keep approved anchors stable while iterating on nearby details.

## Core workflow
1. **Clarify the content target.**
   - Identify the format, audience, channel, and success criterion.
   - Separate locked canon from flexible draft material.

2. **Build a reviewable draft first.**
   - For creative assets: script, beat list, keyframes, CTA notes.
   - For articles: outline, thesis, draft body, sources, and distribution variants.

2.5 **Analyze the actual media before writing any copy (mandatory for video).**
   - Download the media file. Run ffprobe for duration/codec/specs.
   - Transcribe audio with Whisper: `whisper audio.wav --model base --language nl --output_dir /tmp/analysis`
   - Extract key frames every 5 seconds: `ffmpeg -i video.mp4 -vf "fps=1/5,scale=480:-1" -q:v 2 /tmp/frames/frame_%03d.jpg`
   - Read the full transcript. The transcript is the single source of truth.
   - Write caption based ONLY on what the video actually shows and says.
   - Do not invent angles, themes, or hooks that are not in the video.

3. **Make the approval boundary explicit.**
   - Say what is locked.
   - Say what the user can change.
   - Say what will not proceed until approval arrives.

4. **Pause at the gate.**
   - Do not continue into animation, bulk generation, final packaging, or publishing until the approved state is clear.

5. **Resume from the approved state only.**
   - If the user changes one part, adjust the smallest adjacent pieces and re-present the updated pack or draft.

6. **Publish with verification.**
   - Sanity-check links, titles, formatting, and destination state.
   - After publishing, verify the page or post actually exists and matches the intended content.

## Review-gate subsection
Use this when producing reels, ads, storyboards, or other assets that need user curation before final production.

### Review pack contents
- Clear title and goal
- Short script or narration draft
- Frame list with IDs and one-line purpose
- Aspect-ratio callout when relevant
- Canonical design constraints
- CTA or end-card direction
- Direct question to the user about what to change, keep, or approve

### Review-gate pitfalls
- Do not silently continue after the user asked for curation.
- Do not bury the approval request in a long explanation.
- Do not regenerate everything when only one frame or line needs review.
- Do not mix draft, approved, and pending assets without labels.

## Publishing subsection
Use this when creating blog posts, updating editorial content, or publishing into a CMS or knowledge base.

### Publishing workflow
- **Analyze the actual video before writing any copy.** For video posts: download the media, run Whisper transcription, extract key frames. The transcript is the single source of truth. Never write a caption based on assumptions about what the video must be about. Using the Zernio REST API? See `references/zernio-rest-api.md` for full endpoint reference.
- Prefer concrete market signals, internal learnings, and practical value over filler.
- Draft in the brand voice requested by the user.
- Add sources, backlinks, or citations when they strengthen trust.
- Verify title, formatting, and destination content after publishing.
- **Zernio media upload:** Use `zernio media:upload <file> --pretty` first. It can upload large H.264/AAC MP4s and returns a temp URL that Zernio promotes to `https://media.zernio.com/media/...` when the post is created. Verify the created post shows permanent `/media/` URLs.
- **Duplicate check:** Before creating a post, fetch recent posts via `GET /v1/analytics` and compute token‑overlap similarity with the new transcript; if similarity > 30 %, consider not posting to avoid redundancy.
- **Cross‑platform validation:** Before scheduling any multi‑platform post, run the checklist in `references/zernio-cross-platform-validation-checklist.md`. It prevents the three most common Zernio failures: Instagram aspect‑ratio violation, LinkedIn mixed‑media rejection, and Twitter/X caption overflow.
- **Optimal:** Schedule for Friday 17:00 Amsterdam time (UTC+2) – this slot yields the highest engagement (≈92).
- **Caption lock:** Published posts cannot have their captions edited; only the recycling configuration can be changed. To modify the caption, delete and repost (you will lose existing engagement).

### Weblyfe-specific notes
- Write in English unless the user explicitly asks for another language.
- Avoid em dashes.
- Keep tone human, specific, and useful.
- For LinkedIn derivatives, keep the structure compact: hook, concrete founder/operator details, one clear thesis, simple CTA if needed, and 3-5 hashtags.
- **Language-based Instagram routing (hard rule):**
- **English content** → Instagram account `@seyed.jpg` (accountId: `69c7c4e96cb7b8cf4ca8ad9e`)
- **Dutch content** → Instagram account `@techwizseyed` (accountId: `6a3ac4c09d9472faaec70ae9`)
- These are hard boundaries for Instagram. Never post English on `techwizseyed` or Dutch on `seyed.jpg`.
- Other platforms (LinkedIn, X/Twitter, YouTube) do not have the same language separation. Crosspost English and Dutch there only when suitable or requested.
- If Seyed says “just post this on TechWiz/TechWiz Seyed”, schedule only the `@techwizseyed` Instagram account, not LinkedIn/X/YouTube.
- When scheduling via Zernio CLI: `--accounts 69c7c4e96cb7b8cf4ca8ad9e` for seyed.jpg, `--accounts 6a3ac4c09d9472faaec70ae9` for techwizseyed.

**Zernio CLI video posting pattern (works):**
1. Upload video: `zernio media:upload /path/to/video.MOV --pretty` → returns `url`
2. Create post: `zernio posts:create --text "caption" --accounts <ACCOUNT_ID> --media <MEDIA_URL> --scheduledAt <ISO_TIME> --timezone Europe/Amsterdam --pretty`
3. The temp URL gets automatically promoted to a `/media/` URL by Zernio
4. Instagram API does NOT support custom thumbnails — user must set via Instagram app after posting
5. If you scheduled on the wrong account: `zernio posts:delete <POST_ID>` then recreate with correct `--accounts`

For Seyed/Appie/Instant Appie social posts, avoid generic AI-workflow commentary when there is fresh founder proof available. Lead with what was actually built, shipped, debugged, or learned from real Weblyfe/Appie work. Strong recurring angle: "we built so many Instant Appies that the pattern became impossible to ignore" and "the problem is not lack of tools, it is that nobody holds the loose ends."
- When Seyed says to prevent AI speech, run an explicit anti-AI pass: remove common AI words and structures such as "delve into", "at its core", "pivotal", "underscore", "harness", "realm", "that being said", "to put it simply", generic significance language, corporate filler, over-tidy transitions, rule-of-three padding, and robotic upbeat endings. Prefer direct wording, lived details, varied rhythm, and Seyed's natural founder/operator voice.
- For Weblyfe blog publication checks and LinkedIn publishing with generated images, use `references/weblyfe-linkedin-and-blog-publishing-checks.md`.
- For premium launch films or carousel-to-video work, use `references/premium-launch-film-styleframes.md`: styleframe gate first, one metaphor, readable proof modules, mascot integrated not pasted.
- Sanitize markdown links before sending rich-text blocks to Notion.
- After publishing, verify the page title, the page existence, and that child blocks were appended successfully.
- If a social post is created, verify the returned URL and published status.
- For status checks and asset handoffs, use `references/status-and-asset-handoff.md`: verify state before answering, separate script-ready / asset-ready / scheduled / published, and include preview/zip paths without implying publication.
- For short-term autonomous posting trials through Zernio, use `references/zernio-social-posting-trial.md`: verify connected accounts, publish primarily to LinkedIn, poll for `platformPostUrl`, and notify Seyed daily with the exact public link and text posted.
- For Zernio performance analysis and Instagram Trial Reels, use `references/zernio-analytics-and-trial-reels.md`: pull analytics through `zernio analytics:posts`, normalize metrics by platform/theme, avoid overvaluing tiny-sample engagement rates, and use direct Zernio API `platformSpecificData.trialParams` for Trial Reels when the CLI lacks flags.
- For Seyed's weekly/monthly social analytics reports and evolving content doctrine, use `references/social-analytics-reporting-and-doctrine.md`: pull Zernio data with date-only filters if needed, format Telegram reports as codeblock tables, write Notion reports, and update doctrine only from stable patterns.
- For Seyed/Weblyfe social analytics reports in Telegram, use `references/social-analytics-reporting-for-telegram.md`: pull longer windows in chunks, deduplicate analytics, translate metrics into content rules, and present review tables in fenced `text` codeblocks rather than normal Markdown tables when legibility matters.
- For checking whether social analytics are up to date in Mission Control, use `references/social-analytics-mission-control-sync.md`: pull Zernio analytics for the requested window, push the same window with `SOCIAL_DAYS` explicitly set, verify MC via `/api/social?days=N`, and run Content Factory sync when needed. Do not shell-source `/root/clawd/.env.secrets`; let the Python sync script parse it.
- For Drive/shared-folder video analysis and Zernio scheduling, use `references/drive-video-zernio-social-publishing.md`: download the actual video, analyse frames/audio/transcript, convert MOV/HEVC to social-safe MP4 if needed, create/upload clean first-frame assets, use Zernio REST when the CLI lacks thumbnail/Reel-cover/Trial-Reel fields, choose channels by content fit, and verify scheduled/public status correctly.
- For ongoing autonomous content work, create or maintain a daily “posted & done” digest: report what was actually published only when verified by public URL/platform/CMS status, then separate drafted/prepared work, operational work, blockers, and links/files. If no public post is verified, say so explicitly rather than implying publication. See `references/daily-posted-done-digest.md`.
- For nightly Content Factory maintenance, use `references/content-factory-nightly-sync.md`: correlate Notion Content Factory rows with Google Drive assets and Zernio posts/analytics, update Drive links/live links/status/one-week views only on confident matches, and report blockers such as invalid Notion auth without implying updates happened.
- For adding/backfilling the dedicated Content Factory live URL field, use `references/content-factory-live-link-sync.md`: add/verify the `Live Reel Link` URL property, backfill only verified public Zernio URLs, and keep the nightly sync cron enabled.
- For scheduled nightly CMO carousel drafts for @seyed.jpg/Clark, write exactly the requested slide count, include Dutch + English on every slide, save to `/root/clawd/cache/content-drafts/`, send only the 3-line preview through the configured Telegram bot or final cron response when the delivery wrapper forbids manual sending, and verify file shape plus delivery state before finalizing. See `references/nightly-cmo-carousel-workflow.md` and use `scripts/verify-nightly-carousel.py` for deterministic draft checks.

For dubbing video content between languages via ElevenLabs (e.g. English → Dutch), use `references/elevenlabs-dubbing-workflow.md`. Handles API upload, status polling, and download of the dubbed file.

For LinkedIn growth strategy research and 2026 algorithm best practices for Seyed/Weblyfe, use `references/linkedin-growth-strategy-2026.md`. Covers Interest Graph model, Depth Score, content pillars, format mix, and profile optimization.

For gog OAuth re-authentication when the keyring is corrupt (aes.KeyUnwrap failure), use `references/gog-oauth-reauth-flow.md`. Covers the remote OAuth flow (step 1 + step 2) for seyed@weblyfe.nl Drive/Docs/Sheets access.

For Drive video download and Zernio social publishing with the full pipeline (download → transcode → transcribe → caption → Zernio draft → schedule), use `references/drive-video-zernio-social-publishing.md`.
- For product launch/content strategy derived from app repos, scan marketing docs, live pages, dashboard code, and internal case notes; separate shipped reality from roadmap claims before writing public copy. See `references/product-launch-content-from-codebase.md`.

### Pitfalls
- When Seyed sends a voice note for content or production direction, do **not** echo the transcription back to him. Briefly confirm receipt and continue using the transcript internally.
- Zernio failure prevention is mandatory before scheduling: Twitter/X captions must be ≤280 chars, LinkedIn video posts must not include separate image media in the same post, Instagram feed/Reel cover images must be within 0.75-1.91 aspect ratio, and Google Business must never receive video. If thumbnails/covers are risky, schedule the video-only Instagram post and let Seyed adjust the cover manually.
- Every scheduled Zernio post needs a one-shot post-publish verification cron 15-30 minutes after scheduled time. Report the actual `platformPostUrl` when published, exact errors when failed, and never imply scheduled means live.
- After a verification cron confirms the post is live and reachable, remove the completed one-shot verification cron or ensure `appie2-cron-completed-job-cleanup` will remove it. Do not leave successful one-shot verification jobs hanging around in the cron list.
- When another agent may have handled the same posting request, run `references/zernio-scheduled-duplicate-audit.md` before publish time: audit all scheduled posts, detect same-account/similar-content duplicates, delete unsafe duplicates, then verify deleted IDs return 404 and verification crons target the surviving post IDs.
- **Do NOT write captions or copy for any video content without first analyzing the actual media.** Download the video, transcribe the audio with Whisper, extract key frames, and confirm the content before writing a single word. Seyed will call you out when captions don't match the reel because the video is about something completely different than what you assumed. The transcript is the single source of truth — never invent or guess what a video is about. Seyed gave sharp, frustrated feedback on exactly this: captions that don't match the reel are worse than no caption at all.
- When downloading from Google Drive: the link Seyed shares may be a FOLDER, not a file. Check the `application/vnd.google-apps.folder` MIME type. If it's a folder, inside it is the actual video file. Drive download may return 500 errors for large files — ask Seyed for the direct file link or the exact filename inside the folder.
- Do not force a pre-made content calendar if the user wants reactive, evidence-based ideas.
- Do not write generic filler that is disconnected from actual work.
- Do not leave the final asset in a local draft state if the task includes publishing.
- Do not assume markdown links survive rich-text conversion unchanged.
- For reels-only opportunity scans, do not collapse the output into a strategy recap. Preserve ranking and convert each item into a shot-ready brief.
- If a scan is being turned into briefs, keep the source ranking stable and only reorder when a later item is clearly stronger on watch-time, shareability, proof density, or why-now freshness.

## Support-file guidance
- Put reusable review-pack examples, checklists, or brand-specific publishing notes in `references/`.
- Put copyable starter drafts in `templates/`.
- Put repeatable validation or publishing probes in `scripts/`.
- For live reels scans, keep a dated seed snapshot in `references/` so future scans can reuse the live angle without rereading the full source material.
