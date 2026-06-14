# Vercel API function triage

Use this when a deployed app shows a frontend JSON parse error or a generic Vercel 500 on an API route.

## Symptom pattern
- UI shows an invite/error page that says `Unexpected token 'A', "A server e"... is not valid JSON`.
- `curl` to the API route returns HTTP 500 with `A server error has occurred`.
- `vercel logs` shows `FUNCTION_INVOCATION_FAILED` or `ERR_MODULE_NOT_FOUND`.

## Fast checks
1. Confirm the route itself fails, not just the UI:
   ```bash
   curl -i https://<project>.vercel.app/api/<route>
   ```
2. Pull recent runtime logs:
   ```bash
   vercel logs --project <project> --token "$VERCEL_TOKEN" --since 24h --expand --level error
   ```
3. Inspect the project and env linkage:
   ```bash
   vercel project inspect <project> --token "$VERCEL_TOKEN"
   vercel env list --token "$VERCEL_TOKEN" --cwd <repo>
   ```

## Common root causes
- The function throws before `res.json()` is reached, so the frontend tries to parse plain text as JSON.
- A shared helper imported by a serverless function is missing from the deployed bundle or resolves to the wrong path at runtime.
- Project env vars exist locally but are not present in the Vercel project or the project is linked to the wrong team/scope.

## What to verify before redeploying
- Build succeeds locally.
- The API route returns JSON on both success and error paths.
- Any shared helper modules used by `/api/*` routes are included in the deployment bundle.
- The Vercel project name, scope, and env vars match the repo you actually deployed.

## Session note
In one triage session, `/api/redeem-invite` and sibling routes on `<team>/<project>` returned `FUNCTION_INVOCATION_FAILED`; logs showed `ERR_MODULE_NOT_FOUND` for `/var/task/api/_audit`, while the frontend surfaced `Unexpected token 'A'... is not valid JSON`.