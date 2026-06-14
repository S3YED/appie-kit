# Secret ingestion and local scrub pattern

Use when the user pastes a credential in chat and asks you to save it, then scrub traces.

## Goals

- Save the secret to the correct local secret store.
- Verify only by metadata, never by printing the value.
- Remove the raw value from accessible local logs, session dumps, SQLite state, shell history, and temp files.
- Tell the user when it is safe to delete the original chat message.

## Procedure

1. Save to the appropriate env/auth file with restrictive permissions.
   - Hermes default env path: `$HERMES_HOME/.env`
   - Ensure parent dir is `700` and env file is `600`.
   - If multiple scripts may expect different names, save under the canonical name plus stable aliases, but only when they clearly refer to the same credential class.

2. Verify without disclosure.
   - Report keys present, value length, and optionally a short non-reversible digest prefix such as first 8 chars of SHA-256.
   - Never echo the full value or include it in final messages.

3. Scrub accessible local traces.
   - Search text files under:
     - `$HERMES_HOME/logs`
     - `$HERMES_HOME/sessions`
     - `$HERMES_HOME/cron/output`
     - `/tmp`
     - shell history files where present
   - Replace exact raw secret bytes with a neutral marker such as `[REDACTED_TOKEN]`.
   - For `$HERMES_HOME/state.db`, update text-like columns containing the raw value, then `VACUUM` if possible.
   - Avoid keeping secret-bearing backups. If a backup of SQLite or env contains the raw token, delete it or scrub it too.

4. Verify no remaining matches outside the intended env/auth store.
   - Do not print matching lines.
   - Report only counts and paths if any remain.

5. Operational note.
   - The external messaging platform still contains the original user message until the user deletes it there.
   - After env changes, restart relevant gateways/services only if the token must be picked up by a running process.

## Pitfalls

- Do not use `grep` output containing the secret in the final response.
- Do not create a backup of `.env` and forget to scrub/delete it if it contains the new secret.
- Do not claim platform-side deletion. You can scrub local Hermes-accessible storage, not Telegram's message history.
- Current tool output may already be in the conversation transcript. Minimize repetition and redact in all summaries.
