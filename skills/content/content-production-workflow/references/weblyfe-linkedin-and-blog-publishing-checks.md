# Weblyfe LinkedIn publishing and blog-publication checks

Use this when Seyed asks whether a Notion content item is live on Weblyfe, or asks to turn a draft into a LinkedIn post and publish it.

## Check if a Weblyfe blog draft is published

1. Read the Notion page metadata and markdown first.
   - Extract title, status, note, upload date, and candidate slug words.
   - If Notion status is `Not started`, treat that as a strong draft signal, but still verify the public site.
2. Check the live Weblyfe blog index:
   - `https://weblyfe.nl/blog-weblyfe`
   - Search for the exact title and distinctive phrases.
3. Probe likely post slugs directly, for example:
   - `/post/<notion-title-slug>`
   - `/post/<short-title-slug>`
   - any slug mentioned in Notion fields.
4. Check `https://weblyfe.nl/sitemap.xml` for the exact title slug or distinctive title words.
5. Optionally use web search with exact phrases:
   - `site:weblyfe.nl "Exact Title"`
   - `site:weblyfe.nl/post "Distinctive phrase"`
6. Report clearly:
   - `published` only when a live URL returns 200 and contains matching content.
   - `not published yet` when blog index, likely slugs, sitemap, and search do not show it.
   - include the Notion status as supporting evidence, not the only proof.

## Turn a Notion draft into a LinkedIn post

1. Read the full Notion markdown, not only the first chunk.
2. Rewrite for LinkedIn as a native post, not as an article dump:
   - strong first line
   - short paragraphs
   - concrete founder/operator details
   - no em dashes
   - no corporate filler
   - no "AI assistant" vagueness without examples
   - keep one clear thesis
3. Run an anti-AI pass:
   - remove "pivotal", "landscape", "unlock", "leverage" when they sound generic
   - remove formulaic rules of three
   - remove robotic summary endings
   - keep slight human mess where it helps voice
4. Keep LinkedIn personal posts around 2,800 to 3,000 characters when possible. Zernio may accept longer text, but shorter is safer and more readable.
5. Use 3 to 5 hashtags max.

## Nice image for LinkedIn posts

1. Generate a premium landscape visual, preferably 1200x627 final crop.
2. For Weblyfe/Appie AI posts, a good default is:
   - dark cinematic workspace
   - subtle teal and warm gold accents
   - abstract automation nodes
   - small wizard-like AI assistant silhouette
   - no text, no logos, no watermark
3. Verify the image visually before posting:
   - no readable text
   - no fake logos
   - no distorted UI artifacts that distract
   - professional enough for LinkedIn
4. Center-crop or resize to `1200x627` before uploading when needed.

## Publish with Zernio to LinkedIn

1. Verify the LinkedIn account ID from `zernio accounts:list --pretty`; do not assume from profile name alone.
2. Upload media first:
   - `zernio media:upload /path/to/image.png --pretty`
3. Publish immediately only when the user explicitly asked to post now:
   - `zernio posts:create --text "$POST_TEXT" --accounts "$LINKEDIN_ACCOUNT_ID" --media "$MEDIA_URL" --pretty`
4. Save the post result JSON if useful.
5. Verify success from the returned platform status and URL:
   - `platforms[].status == published`
   - `platforms[].platformPostUrl` exists
6. Final response should include the live URL and mention whether media was attached.

### Zernio scheduled-to-now pitfall

When Seyed asks to post a carousel that is already scheduled:
1. Fetch the scheduled post first with `zernio posts:get <post_id> --pretty` and extract `content`, `mediaItems[].url`, and `platforms[].accountId._id`.
2. Try creating the immediate post only if it will not duplicate an existing scheduled item.
3. If Zernio returns `409 This exact content is already scheduled, publishing, or was posted to this account within the last 24 hours`, delete the scheduled post only after the content, account IDs, and media URLs have been saved locally/in variables.
4. Recreate the post immediately with `zernio posts:create --text ... --accounts ... --media ... --pretty`.
5. Verify via `zernio posts:list --pretty --limit 20` or `zernio posts:get <new_id>` because create output can be sparse even when the post publishes successfully.
6. Confirm the old scheduled item is gone so it does not double-post.

### LinkedIn growth intelligence loop

For Seyed's LinkedIn growth, treat analytics plus research as a recurring production input, not a one-off tip list:
- Pull `zernio analytics:posts --pretty --platform linkedin --limit 25` and `zernio analytics:best-time --pretty --platform linkedin`.
- Compare winning posts by topic, hook, format, media type, time slot, comments/reactions, and profile-click intent where available.
- Current working hypothesis to test: concrete Appie/Weblyfe founder-operator stories with real client/workflow details, practical before/after, strong photos of Seyed when relevant, and no corporate framing.
- Recommend one next publish action with format, topic, time in Dutch time, and CTA.
- Keep the research output concise and decision-oriented; do not publish from a research job.
