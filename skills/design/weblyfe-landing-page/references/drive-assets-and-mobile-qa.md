# Drive assets and mobile QA for Weblyfe client sites

Use this when improving an existing Weblyfe landing page with client-provided Google Drive assets and responsive polish.

## Google Drive asset extraction pattern

Public Google Drive folder pages often expose useful file/folder metadata in the HTML even when there is no clean API listing.

1. Fetch the folder HTML with `curl -L 'https://drive.google.com/drive/folders/<folder_id>?usp=sharing'`.
2. Extract child folder/file IDs and names from Drive's embedded data. A quick pattern that worked:

```bash
curl -L 'https://drive.google.com/drive/folders/<folder_id>?usp=sharing' \
  | python3 -c 'import sys,re,html; data=sys.stdin.read(); ids=re.findall(r"\\[null,\\\"([A-Za-z0-9_-]{20,})\\\"\\].{0,260}?\\[\\[\\[\\\"([^\\\"]+)", data); print("\\n".join(f"{i} {html.unescape(n)}" for i,n in ids[:120]))'
```

3. Traverse relevant subfolders by ID. Favor folders named like `Website`, `Client Content`, `Pictures Photoshoots`, `Insta Pics`, `Brand Partners`, or client/content labels.
4. Avoid folders whose name or user instruction indicates unrelated branding. Example: if the user says the `Branding` folder is for another golfer project, do not use it even if it contains polished graphics.
5. Download candidate files with:

```bash
curl -L 'https://drive.google.com/uc?export=download&id=<file_id>' -o public/brand/<bucket>/<safe-name>.<ext>
```

6. Immediately validate downloaded files with `file public/brand/<bucket>/*`. Google Drive failures can silently save HTML confirmation/login pages. Only wire files that inspect as real images.
7. Visually inspect selected images before using them. For personal brands, prefer solo, campaign, and proof/context images over random social/couple shots unless the section calls for lifestyle warmth.

## Responsive QA workflow

- Start with code inspection and a real local server, then run Playwright at phone, tablet, and desktop widths.
- At minimum test widths: 375x667, 390x844, 768x1024, 1440x1000.
- Check for horizontal overflow using `document.documentElement.scrollWidth` vs `window.innerWidth` and identify offenders via `getBoundingClientRect()`.
- Capture screenshots for visual review before and after.
- If Playwright launch is blocked by host permissions, be explicit: say physical screenshot verification could not complete, still run `npm run build`, and report the exact blocker. Do not claim Playwright verification if screenshots were not captured.

## Mobile polish checklist

- Reduce `--nav-height` on mobile if the fixed nav consumes too much viewport.
- Tighten `.section` padding and `.container-*` inline padding under 640px.
- Clamp display headings and large stat numbers more aggressively on mobile.
- Make primary CTAs full-width on mobile, with readable tracking and minimum height.
- Check hero image focal point separately for mobile. A desktop-centered portrait often needs `object-[58%_35%]` or similar on small screens.
- Strengthen light hero overlays for mobile if the image fights copy contrast.
- Avoid using dark-section ghost buttons on light hero backgrounds. Use glass/ink variants for readable secondary CTAs.
- Use real partner logos sparingly as proof cards when available, but keep them grayscale/quiet by default so the page does not become a logo wall.
