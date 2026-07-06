# Conversion page live verification

Use this reference for paid product pages, PDF sales pages, Stripe checkout funnels, and other conversion-critical Weblyfe pages.

## Durable pattern

1. Verify the live deployment, not just the local repo.
   - Open the production URL in a browser with a harmless cache-busting query, for example `?live_verify=1`.
   - Confirm the page title, hero headline, key offer details, and visible CTA copy match the intended shipped version.
2. Verify the Git and deployment source.
   - Check the commit SHA and branch status for the deployment working copy.
   - If a separate live clone exists, check both the live clone and the main project repo so uncommitted or unpushed changes are not mistaken for production.
3. Verify conversion plumbing.
   - Primary CTA is visible above the fold.
   - Stripe or checkout link still points to the intended live payment link.
   - UTM or tracking params survive the final URL path where relevant.
   - Thank-you or post-purchase route exists if the funnel depends on it.
4. Verify assets that affect trust.
   - Hero/offer image loads on production.
   - PDF or download asset exists in `public/` or the intended delivery path.
   - No broken image placeholders or stale version labels.
5. Final reply should report the production URL, commit SHA if relevant, and a short verified checklist. Keep it clean and outcome-first.

## Pitfalls

- Do not declare a Vercel or production change live based only on a successful push or local build.
- Do not rely on a browser snapshot alone for conversion pages. Pair it with repo/deploy source status so the verified page can be tied back to a commit.
- For paid pages, treat payment-link and tracking verification as part of QA, not as optional polish.
