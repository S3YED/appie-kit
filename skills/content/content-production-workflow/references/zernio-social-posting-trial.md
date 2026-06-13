# Zernio social posting trial workflow

Use this reference when Seyed asks Appie to post for him for a short trial period and report back daily.

## Trial shape
- Default trial: 1 post per day for 7 days.
- Primary destination: LinkedIn personal profile when connected in Zernio.
- Secondary destinations are optional and should not block the main LinkedIn post.
- For text-only daily posts, do not force Instagram or YouTube unless a suitable media asset exists.

## Account discovery
Before scheduling or publishing, verify connected accounts with:

```bash
zernio auth:check --pretty
zernio accounts:list --pretty
zernio accounts:health --pretty
```

Use account IDs from `accounts:list`, not platform guesses.

## Publishing pattern
For immediate LinkedIn publication:

```bash
zernio posts:create \
  --text "$POST_TEXT" \
  --accounts "$LINKEDIN_ACCOUNT_ID" \
  --pretty
```

For scheduled publication, add:

```bash
--scheduledAt "YYYY-MM-DDTHH:MM:SSZ" --timezone Europe/Amsterdam
```

## Verification pattern
Do not claim a post is live until a public platform URL exists.

```bash
zernio posts:get "$POST_ID" --pretty
```

Poll until the platform entry has:
- `status: published`
- `platformPostUrl` present

If the top-level status is `partial`, inspect each platform. Report successes with links and failures separately.

## Notification format
Daily notification to Seyed should include:
- Posted today / posting failed.
- Platform and account.
- Public link for every verified post.
- Exact text posted, or concise preview if long.
- Any platform failures or next action needed.

## Failure handling
- If X/Twitter fails but LinkedIn succeeds, report X as a secondary failure and keep the day successful.
- If Zernio account health shows token warnings but `canPost` and `tokenValid` are true, proceed cautiously and verify output.
- Never expose raw config, credentials, refresh tokens, API keys, or OAuth details from CLI output.
