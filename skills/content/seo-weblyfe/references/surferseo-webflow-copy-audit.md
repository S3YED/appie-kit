# SurferSEO + Webflow copy audit workflow

Use this when auditing a Webflow landing page against SurferSEO Content Editor drafts, especially when the Surfer share URL only shows `Loading...` via normal extraction.

## What worked

Surfer public draft URLs like:

```text
https://app.surferseo.com/drafts/s/<permalinkHash>
```

can expose the Content Editor data through Surfer's GraphQL endpoint without a browser session:

```http
POST https://app.surferseo.com/graphql
Content-Type: application/json
Origin: https://app.surferseo.com
Referer: https://app.surferseo.com/drafts/s/<permalinkHash>
```

Minimal query shape:

```graphql
query ContentEditorByPermalinkHash($input: ContentEditorByPermalinkHashInput!) {
  contentEditors {
    id
    byPermalinkHash(input: $input) {
      id
      title
      permalinkHash
      targetDomain
      meta { status importContentUrl }
      progressSnapshots
      notes
      outlines { id content status }
      llmGuidelines {
        status
        facts { id fact sources { id url modelFamilies } }
      }
      seoGuidelines {
        id
        wordCount
        location
        contentScoreGuidelines
        mainKeyword { item included heading ratio { min avg max } count { min avg max } }
        keywords { item }
        customTerms { id item included heading count { min avg max } ratio { min avg max } isNlpEntity }
        prominentTerms { id item included heading count { min avg max } ratio { min avg max } isNlpEntity position }
        questions { id item included count { min avg max } ratio { min avg max } isNlpEntity }
        structuralGuidelines { id factor target { min avg max valueOverride } }
        competitors {
          id url title position displayedLink
          textContent { headings { tag text } alts { tag text } }
          score { value }
          factors { body { wordCount { all outsideLinks } } }
        }
        topics { id item included type metadata { tag pageId } }
      }
    }
  }
}
```

Variables:

```json
{"input":{"permalinkHash":"<permalinkHash>"}}
```

## Interpretation rules

- Surfer drafts may not contain rewritten copy. They often contain guidance only: score, target terms, facts, topics, questions, competitors, structure.
- Translate guidance into human copy recommendations. Do not blindly paste term lists.
- Treat term counts as directional. Some Surfer regexes count subterms and can look like overuse. Verify exact phrases manually before recommending reductions.
- If `meta.importContentUrl` is present, use it to map the Surfer draft to the live page.
- Pull current live page title, meta description, H1/H2 structure, CTA labels, and word count before making recommendations.
- For Webflow Dutch sites, verify the rendered `<html lang>` value. If Dutch content renders as `lang="en"`, flag it as an SEO/accessibility/AEO issue.

## Report shape preferred for Weblyfe client work

For each page include:

1. URL and Surfer draft URL.
2. Primary keyword, Surfer score, live word count, Surfer target.
3. Search intent and implementation priority.
4. Current title, meta description, and H1.
5. Suggested sections to add or strengthen.
6. Copy notes in plain Dutch/business language, not raw Surfer jargon.
7. Useful entities/topics to weave in naturally.
8. AEO facts and FAQ candidates.
9. Global implementation notes: FAQ schema, internal anchors, language tag, CTA/render checks.

## Pitfalls

- Do not call the Surfer term list "suggested copywriting changes" unless actual edited copy/outline exists in `notes` or `outlines`.
- Do not add words just because Surfer says so. If a homepage is already long, restructure and clarify instead.
- Avoid keyword stuffing. Surfer score is a diagnostic, not the client-facing objective.
- Keep Webflow edits read-only until the user explicitly approves implementation.
