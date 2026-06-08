# Token-only direct deploy from constrained sessions

Use this when a user wants the agent to work directly with an existing Vercel token, especially from Telegram or another non-interactive runner.

## Pattern

1. Use the existing environment token without printing it:
   ```bash
   cd /path/to/project
   vercel deploy --prod --token "$VERCEL_TOKEN" --yes --no-color
   ```
2. If local build is blocked by filesystem/sandbox permissions, try remote deploy anyway. Vercel can build remotely from the uploaded project.
3. If the CLI exits cleanly but suppresses the deployment URL, query Vercel instead of guessing:
   ```bash
   python3 - <<'PY'
   import json, os, urllib.request
   from pathlib import Path

   project = json.loads(Path('.vercel/project.json').read_text())
   token = os.environ['VERCEL_TOKEN']
   url = f"https://api.vercel.com/v6/deployments?projectId={project['projectId']}&limit=5"
   if project.get('orgId'):
       url += f"&teamId={project['orgId']}"
   req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
   with urllib.request.urlopen(req, timeout=20) as r:
       data = json.load(r)
   for d in data.get('deployments', [])[:5]:
       print(d.get('state'), d.get('target'), 'https://' + d.get('url', ''))
   PY
   ```
4. Verify the public custom domain independently:
   ```bash
   curl -I https://example.com
   curl -Ls https://example.com | head
   ```
5. Only attach the alias after you have a confirmed deployment URL:
   ```bash
   vercel alias set https://DEPLOYMENT_URL example.com --token "$VERCEL_TOKEN"
   ```

## Pitfalls

- Do not expose the token in chat, logs, or command output.
- A clean CLI exit without a printed URL is not proof the custom domain changed. Verify the domain content.
- Do not claim success when the domain still serves an old platform, e.g. Shopify. Say exactly what was verified and what remains unverified.
- If API/network access is sandbox-blocked, the durable lesson is the fallback sequence above, not that Vercel or the browser is broken.
