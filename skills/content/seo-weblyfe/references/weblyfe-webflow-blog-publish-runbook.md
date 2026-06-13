# Weblyfe blog publish runbook (Webflow CMS)

Use when the user asks to "push it live" for a Weblyfe blog draft.

## Preconditions
- Draft content is final and source-backed.
- You have valid Webflow API token and site access.
- Never expose tokens in chat or code.

## Minimal publish sequence
1. Confirm target site/domain first.
2. Resolve the Blog Posts collection and required fields.
3. Create the CMS item as live (`/items/live`) with:
   - `name`
   - `slug`
   - `category` (valid option id)
   - `post-summary`
   - `post-body` (valid rich text HTML)
4. Verify the live URL with `curl -L` and confirm HTTP 200.
5. Verify title/snippet match expected content before reporting success.

## Weblyfe-specific notes from this session
- Site: `weblyfe.nl` (Webflow site id observed: `615bd59fd9d3edeb08fd3ea9`)
- Blog collection observed: `Blog Posts` (`65bf2899afe1cc2af3665110`)
- CMS path pattern verified: `/post/<slug>`

## Pitfalls
- Do not claim "live" from API response alone. Always validate the public URL and content.
- If skill names are ambiguous, use fully-qualified skill paths before proceeding.
- Keep publishing operational, concise, and action-first when user asks for immediate go-live.
