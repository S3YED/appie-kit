---
name: seo-checklist
description: "Run the Weblyfe pre-publish on-page SEO checklist for pages, blog posts, and landing pages before publication."
version: 1.0.0
category: content
---

# SEO Checklist Skill

## Purpose
Pre-publish on-page SEO checklist for every page or article on a Weblyfe site. Run this before hitting publish on any new page, blog post, or landing page. Based on the Tornado Masterclass "Zoekwoorden-checklist" visual from Seyed's course. Each item is a concrete, verifiable action.

## Source
"SEO Checklist - On page optimalisatie" PDF from Seyed's Weblyfe University Tornado Masterclass (downloaded from Drive 2026-05-03).

## Quick reference
| Element | Requirement |
|---------|-------------|
| Title tag | Contains primary keyword |
| Meta description | Contains primary keyword |
| URL | SEO-friendly slug containing keyword |
| H1 | One H1, contains keyword |
| First paragraph | Keyword used at least once |
| Body text | Keyword appears multiple times naturally |
| Bold in first paragraph | Keyword printed bold at least once |
| H2/H3 subheadings | At least one subheading contains keyword |
| Featured image | Filename and alt-tag contain keyword |
| Content images | Filename and alt-tag contain keyword |
| Breadcrumb | Visible on page, keyword in trail |
| Media | At least one relevant image or video |

## Core principles
1. Title tag first. It is the highest-weight on-page signal. Keyword must appear in the title.
2. "Hoe verder naar voren een woord staat, hoe meer waarde het van Google krijgt." - place keyword early in the title, not at the end.
3. Meta description does not directly affect ranking but affects CTR. Write it to compel the click, with keyword included.
4. One H1 per page. It should mirror or closely match the title tag with the keyword.
5. Keyword in the first 100 words. Google weights early content more than later content.
6. Keyword appears multiple times in body (laat je zoekwoord op meerdere plekken terugkomen) - naturally, not stuffed.
7. Bold the keyword once in the first paragraph. This signals emphasis to both users and crawlers.
8. Images carry SEO weight via filename and alt-tag. Both the featured image and in-content images should include the keyword.
9. Breadcrumbs help Google understand site hierarchy and put the keyword in the navigation trail.
10. Rich media (video, infographic) increases time-on-page and engagement - both indirect ranking signals.

## How to apply (for any new Weblyfe site)
- Create a checklist copy of the table above for each page/post before publishing.
- Write the title tag first. Include keyword, keep under 60 characters, keyword near the front.
- Write meta description with keyword, 140-155 characters, include a call to action.
- Set the URL slug: lowercase, hyphens between words, keyword included, no stop words (de/het/een).
- Open the editor, type H1 containing the keyword.
- Write first paragraph: use keyword in the first sentence or two, bold it once.
- Write subheadings (H2, H3): at least one must include the keyword or a close variant.
- Before uploading the featured image: rename the file to include the keyword (e.g., `seo-tips-voor-mkb.jpg`). Set alt text to keyword phrase.
- Do the same for any in-content images.
- Enable breadcrumbs in WordPress/Webflow/CMS (Yoast SEO, Rank Math, or CMS breadcrumb component).
- Embed or link at least one relevant video or add a relevant image beyond the featured image.
- Run a final read-through: does the keyword appear naturally in the first alinea, in at least one H2/H3, and multiple times in the body?

## Anti-patterns (what the PDF says NOT to do)
- Publishing with a generic title that omits the keyword ("Welkom op onze blog"). No keyword = no signal.
- Using the same keyword-stuffed pattern for every page. Each page should have its own primary keyword.
- Uploading images with default camera filenames (IMG_4521.jpg). Always rename before upload.
- Empty alt text on images. Screen readers and crawlers both need it.
- Skipping the meta description. Google may auto-generate one that does not compel the click.
- URLs with special characters, capitals, or Dutch stop words (/de-beste-seo-tips/ is fine; /De-Beste-SEO-Tips/ is not).

## Examples and templates
Checklist from the Tornado Masterclass visual (verbatim items):
- "Geef een relevante title tag op met daarin het zoekwoord."
- "Geef een relevante meta description op met daarin het zoekwoord."
- "Werk met een zoekmachine vriendelijke URL met daarin het zoekwoord."
- "Verwerk je zoekwoord in de bestandsnaam en alt-tag van je uitgelichte afbeelding."
- "Toon een broodkruimelspoor op je pagina met daarin het zoekwoord."
- "Begin je artikel met een kop 1 (H1) met daarin het zoekwoord."
- "Gebruik je zoekwoord minstens eenmaal in je eerste alinea."
- "Laat je zoekwoord op meerdere plekken in je content terugkomen."
- "Druk je zoekwoord 1x dik in je eerste alinea."
- "Verwerk je zoekwoord in de bestandsnaam en alt-tag van afbeeldingen in de content."
- "Maak gebruik van tussenkoppen (H2, H3) met daarin het zoekwoord."
- "Verrijk je content met relevante media."

## Cross-skill references
- `seo-keyword-strategie`: determines which keyword to use before running this checklist
- `seo-technische-seo`: covers site-level technical requirements; this checklist covers page-level
- `seo-smart-content`: each article in a content cluster must pass this checklist
- `seo-bezoekersmagneet`: the 6 Google signals (Relevantie, Kwaliteit, Leesbaarheid etc.) are all addressed by items in this checklist
