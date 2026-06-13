# Weblyfe publishing notes

This file captures the verified publishing quirks that are easy to forget.

## Core rules
- Write in English unless the user asks otherwise.
- Avoid em dashes.
- Keep tone human, specific, and useful.
- Favor concrete market signals and internal learnings over generic filler.

## Notion publishing
- Prefer the Weblyfe blog database or accessible parent page workflow.
- Notion API version used in this environment is 2025-09-03.
- Databases behave as data sources when querying.
- If a direct data source ID is not usable, create the article page under the accessible parent page and append content blocks there.
- Sanitize markdown links before converting them to rich text blocks.

## Post-publish verification
- Confirm the page title is correct.
- Confirm the page exists via API.
- Confirm child blocks were appended successfully.
- If a social derivative is created, verify the returned URL and published status.

## LinkedIn derivative pattern
- Hook
- A few concrete takeaways
- Direct link
- Simple CTA
- 3 to 5 hashtags