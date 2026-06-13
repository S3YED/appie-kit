# Weblyfe blog publish and cover checklist

Use this checklist when moving a drafted article into the live Weblyfe CMS.

## Publish standard
- Publish the post to the live CMS collection, not only as a local markdown draft.
- Confirm the final slug and test the public URL on `https://weblyfe.nl/post/<slug>`.
- Verify the page returns HTTP 200 after redirects.

## Cover image standard (mandatory)
- Every published blog must have a branded cover image.
- Default style: branded abstract AI, dark base with Weblyfe accent colors.
- Set the image on both CMS fields:
  - `main-image`
  - `thumbnail-image`
- Re-check rendered page metadata and header visual after publish.

## Quality checks before handoff
- Title and summary are visible in page metadata.
- Category is set correctly.
- Reading time is set.
- Post body is rendered as valid rich text.
- Cover image URL resolves on CDN and appears in-page.

## Handoff format
When confirming completion to Seyed, always provide:
- live URL
- confirmation that cover image is applied
- one-line verification note (for example: URL loads and returns 200)
