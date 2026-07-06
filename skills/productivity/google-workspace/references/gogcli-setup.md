# gogcli Setup Guide

[gogcli](https://github.com/openclaw/gogcli) (by openclaw) is a single Go binary for Google Workspace APIs — Gmail, Drive, Docs, Sheets, Slides, Calendar, Contacts, Tasks, and more. It handles PKCE OAuth natively and is suited for headless agents, CI, and terminals.

## Installation

### Linux (amd64) — from GitHub Releases

```bash
# Find latest version from https://github.com/openclaw/gogcli/releases
VERSION="v0.28.0"  # replace with latest
curl -sL "https://github.com/openclaw/gogcli/releases/download/${VERSION}/gogcli_${VERSION#v}_linux_amd64.tar.gz" \
  -o /tmp/gogcli.tar.gz
cd /tmp && tar -xzf gogcli.tar.gz
sudo mv gog /usr/local/bin/gog
gog --version
```

### macOS — via Homebrew

```bash
brew install openclaw/tap/gogcli
gog --version
```

## OAuth Setup

### Step 1: Get your client_secret.json

From Google Cloud Console:
1. Create a project (or select existing)
2. Enable the APIs you need (Gmail API, Drive API, **Docs API**, **Sheets API**, **Slides API**, etc.)
3. Credentials → Create Credentials → OAuth 2.0 Client ID → Desktop app
4. If in Testing mode, add your email as a test user under OAuth consent screen
5. Download the JSON file

**Important:** The Docs API, Sheets API, and Slides API must be **separately enabled** in the API Library for `gog docs read`, `gog sheets`, and `gog slides` to work. Enabling only Gmail + Drive is not enough for Docs/Sheets/Slides access.

### Step 2: Store credentials in gogcli

**On headless systems (no TTY):** use `--insecure` (stores client_secret in a file instead of keyring):

```bash
gog auth credentials set /path/to/client_secret.json --client my-client --insecure
```

**On systems with a TTY:** omit `--insecure` to store in the system keyring.

### Step 3: Set keyring password (headless only)

On headless systems, token storage also needs a keyring password. Set it as an env var:

```bash
export GOG_KEYRING_PASSWORD="your-secure-password"
```

This env var must be present ***every*** time `gog` runs and needs to read/write tokens — including `--remote --step=2` when the code is exchanged. Set it in `~/.hermes/.env`, `~/.bashrc`, `~/.profile`, or service environment.

### Step 4: OAuth authorization

**Always use `--remote` when the user is on a different machine (Telegram, Discord, CI).** The `--manual` flow blocks waiting for TTY input which cannot be provided over messaging platforms.

**Always include `--force-consent`.** Without it, Google may skip the consent screen for returning users and not issue a fresh refresh token, which is required for headless/long-running setups.

**Step 4a — Generate the auth URL:**

```bash
gog auth add "user@example.com" \
  --client my-client \
  --services "gmail,drive" \
  --remote --step=1 \
  --force-consent
```

This prints an `auth_url`. Send it to the user so they can open it in a browser and grant access.

**Step 4b — Exchange the authorization code:**

After the user authorizes, they are redirected to `http://127.0.0.1:<port>/oauth2/callback?code=...&state=...`. Ask them to copy the **entire URL** from the address bar and paste it back.

```bash
gog auth add "user@example.com" \
  --client my-client \
  --services "gmail,drive" \
  --remote --step=2 \
  --auth-url "http://127.0.0.1:34207/oauth2/callback?code=4/0A...&state=..." \
  --force-consent
```

### Step 5: Verify

```bash
gog auth doctor --check
```

or do a quick smoke test:

```bash
export GOG_KEYRING_PASSWORD="..."
gog gmail search "newer_than:1d" --max 2 --client my-client --account user@example.com
gog drive ls --max 3 --client my-client --account user@example.com
```

## Reading Google Docs (when Docs API is disabled)

If the **Docs API is not enabled** in the Google Cloud Console, `gog docs read` fails with:

```
Docs API is not enabled for this OAuth project.
Enable it at: https://console.developers.google.com/apis/api/docs.googleapis.com/overview?project=XXXXXX
Then retry the command. If you enabled it on a different OAuth client, re-authenticate with: gog auth add <account> --services docs
```

**Two workarounds:**

### A) Enable the Docs API (recommended)
1. User visits the link from the error message
2. Click "Enable"
3. Re-authenticate with `gog auth add` including `--services docs`

### B) Export as plain text via Drive API (no Docs API needed)
Google Docs can be exported as plain text through the **Drive API** without the Docs API:

```bash
# Using curl directly with an access token
ACCESS_TOKEN=$(gog ...)  # obtain from gog's keyring
curl -s "https://www.googleapis.com/drive/v3/files/FILE_ID/export?mimeType=text/plain" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

Or, if re-authenticating with docs scope, include it during auth:

```bash
gog auth add "user@example.com" \
  --client my-client \
  --services "gmail,drive,docs" \
  --remote --step=1 \
  --force-consent
```

Note: Adding `docs` after initial auth requires re-authorization. The consent screen will show new scopes.

## State-Resume Pitfall (common failure)

If a previous OAuth flow failed partway through (e.g. keyring not set, manual flow cancelled), the state file persists and `--remote --step=1` returns `state_reused: true` with the **same** auth URL. The user visiting that URL again produces a code for a state that was already consumed, and step 2 fails with `auth state missing`.

**Fix:** Delete the stale state files before generating a new URL.

```bash
rm -rf /root/.config/gogcli
```

Or specifically:

```bash
rm -f /root/.config/gogcli/oauth-manual-state-*.json
```

Then re-add credentials and regenerate the auth URL. The output should show `state_reused: false`.

**Full reset script (when things are really stuck):**

```bash
rm -rf /root/.local/share/gogcli /root/.config/gogcli
export GOG_KEYRING_PASSWORD="..."
gog auth credentials set /path/to/client_secret.json --client my-client --insecure
gog auth add "user@example.com" --client my-client --services "gmail,drive" --remote --step=1 --force-consent
```

## Cross-Machine Flow (Telegram / Discord / etc.)

When the user is talking to you on a messaging platform (not local CLI):

1. **Ask for their email first** — you'll need it for `gog auth add`
2. **Store credentials** with `--insecure` (no TTY available for keyring prompts)
3. **Set GOG_KEYRING_PASSWORD** in the session's shell or `~/.hermes/.env`
4. **Generate URL** with `--remote --step=1` + `--force-consent`
5. **Send the URL** as a clickable link. Explain:
   - Open the link → log in with Google → grant access → browser goes to `http://127.0.0.1:...` (won't load, that's expected)
   - Copy the **entire URL** from the address bar and paste it back
6. **Exchange** with `--remote --step=2 --auth-url "<pasted-url>"`
7. **Test** with a quick `gog gmail search` or `gog drive ls`

## Useful Commands

```bash
# List stored credentials
gog auth credentials list

# List stored accounts
gog auth list

# Search Gmail
gog gmail search "is:unread newer_than:1d" --max 5 --client my-client

# Search Drive
gog drive ls --max 10 --client my-client

# Tree view (with folder ID filter)
gog drive tree --parent FOLDER_ID --client my-client

# Run with a specific client profile
gog --client my-client gmail search "is:unread"
```

## Pitfalls

| Problem | Fix |
|---------|------|
| `no TTY available for keyring` | Set `GOG_KEYRING_PASSWORD` env var, or use `--insecure` on credentials set |
| `manual auth state missing` | The OAuth state was consumed. Rerun the full flow (step 1 → user authorizes → step 2) |
| `state_reused: true` | Stale state file exists. `rm -rf /root/.config/gogcli` then restart from credentials set |
| `OAuth completed but saving token failed` | Same keyring issue. Ensure `GOG_KEYRING_PASSWORD` is set before running step 2 |
| Token expired / 401 errors | gogcli auto-refreshes, but if refresh token is revoked, re-run the full OAuth flow |
| `unexpected argument list` on drive | Use `gog drive ls` not `gog drive list` |
| `Docs API is not enabled` | Enable the API in Google Cloud Console and re-auth with `--services docs` |
| `unknown flag --path` on drive tree | Use `--parent FOLDER_ID` instead of `--path` for folder filtering |