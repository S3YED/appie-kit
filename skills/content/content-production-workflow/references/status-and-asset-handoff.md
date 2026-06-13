# Status and Asset Handoff for Content Production

Use this when the user asks variants of `How is X going?`, `Did you make Y?`, `Where is the asset?`, or asks for a current production-state recap.

## Workflow
1. Verify the work state before answering.
   - Check completion reports, local asset folders, Content Factory/Notion state when relevant, and generated media files.
   - Do not rely only on memory or prior conversational claims.
2. Separate production states clearly:
   - **Script/content ready**: copy, scripts, shot lists, captions exist.
   - **Asset ready**: images/video/zip/caption files exist locally.
   - **Queued/scheduled**: publishing tool has a scheduled item.
   - **Published**: live URL verified.
3. If a publish/schedule state has not been verified, say that explicitly.
   - Good: `Asset-wise it is ready. I have not verified whether it is posted or scheduled yet.`
   - Avoid implying publication from local file existence.
4. Deliver usable handoff paths.
   - Include preview media via `MEDIA:/absolute/path` when helpful.
   - Include source/zip/caption paths if the user needs to hand off to a designer/editor.
5. Keep the recap short and decision-oriented.
   - What is done.
   - What is not verified or pending.
   - The next concrete production step.

## Weblyfe/Appie examples
- For the Instant Appie 9-reel launch sequence, confirm whether the Content Factory pages are `Ready to Record` and whether old versions were archived before reporting completion.
- For an Appie carousel, distinguish `10-slide carousel files + caption exist` from `posted/scheduled on @appie.ai`.
- For review bundles, provide the preview grid/contact sheet first, then the downloadable zip or source folder.

## Pitfalls
- Do not answer `done` when only drafts exist.
- Do not bury the publish caveat after a long explanation.
- Do not send every individual slide unless the user needs them. Prefer preview grid + zip.
- Do not create new production work during a status check unless the user explicitly asks to continue production.
