# n8n-pro Skill

## Purpose

Operate, harden, monitor, and back up the Weblyfe n8n fleet at `app.n8n.weblyfe.nl`. Codifies the patterns and tools built 2026-05-02 so future sessions don't have to re-derive them.

## Quick reference

| Task | Tool / Command |
|------|----------------|
| Daily JSON backup of every workflow to git | `tools/n8n-backup.py` (launchd `com.weblyfe.appie-1-cron.n8n-backup` at 02:15) |
| Hourly health monitor + Telegram alerts | `tools/n8n-health.py` (launchd `com.weblyfe.appie-1-cron.n8n-health` every 3600s) |
| Apply retry defaults to every active workflow | `tools/n8n-harden.py [--dry-run] [--workflow ID]` |
| Inspect workflow JSON via API | `curl -H "X-N8N-API-KEY: $KEY" https://app.n8n.weblyfe.nl/api/v1/workflows/<id>` |
| List + count active workflows | `curl ...?active=true&limit=100` |
| Activate / deactivate a workflow | `POST /api/v1/workflows/<id>/activate` (or `/deactivate`) |
| Update a workflow | `PUT /api/v1/workflows/<id>` with body `{name, nodes, connections, settings}` only — anything else triggers `request/body must NOT have additional properties` |

## Configuration

API base + key live in `~/.openclaw/openclaw.json` under `env.vars`:

```python
N8N_BASE_URL  # "app.n8n.weblyfe.nl"
N8N_API_KEY   # Bearer-style token, sent as X-N8N-API-KEY header
```

DigitalOcean droplet: `n8n-<your-project>` (region ams3, size s-1vcpu-1gb). DO API token in `~/.openclaw/openclaw.json` as `DIGITALOCEAN_ACCESS_TOKEN`. **No SSH key registered on DO account, so direct SSH from Appie-1 to the droplet is blocked** — add your SSH key via the DO dashboard before attempting direct SSH.

## Production-ready workflow checklist

Before declaring a workflow "foolproof," verify all of the following:

1. **Error handler is wired.** `settings.errorWorkflow` points to the GLOBAL ERROR HANDLER `54kH3T3oXWELrCDuFKMN5`. The handler auto-attaches itself to any active workflow without one (Schedule Trigger at 1am daily), so this is mostly automatic — but verify on PR.
2. **Retries on every API node.** `retryOnFail: true`, `maxTries: 3`, `waitBetweenTries: 2000` minimum. Use `tools/n8n-harden.py --workflow <id>` to apply.
3. **Graceful degradation on non-critical leaf nodes.** Sheet appends and label-adds get `onError: continueRegularOutput` or `continueErrorOutput` so a downstream service hiccup doesn't block the upstream archive.
4. **Idempotent file naming.** Drive uploads use `{sender_domain}_{email_date}_{thread_id_short}.pdf` style — *not* `{$now}` — so retries don't create duplicates.
5. **Subject filter is specific.** A trigger with only `has:attachment` will hit every random PDF (contracts, screenshots, your own outbound mail). Add explicit subject patterns.
6. **Skip rules for known false positives.** Add rules for your known income sources (e.g. Stripe transactions) and your own outbound mail. Embed in a Code node early in the flow.
7. **Multi-attachment handling.** If a single email might carry multiple PDFs (Tally, Midjourney), the Code node must emit one item per PDF — n8n's `Object.keys(...).find(...)` only takes the first.
8. **Folder mapping covers backfill + future.** The Drive folder map should include 2024-2026 and a fallback that auto-discovers via Drive search.
9. **Single-account vs multi-account.** Each Gmail Trigger is bound to one credential. Multi-account coverage requires either multiple Trigger nodes or a parallel pipeline (Python `tools/invoice-pipeline.py` covers all 3 accounts as backup).

## Common API gotchas

- **PUT body schema is strict.** Send `{name, nodes, connections, settings}` only. Any of `id, active, createdAt, updatedAt, versionId, tags, triggerCount, meta, staticData, isArchived, shared, homeProject, scopes, sharedWithProjects, pinData, usedCredentials` causes 400 `request/body must NOT have additional properties`.
- **PUT validates credentials.** If a node references `googleContactsOAuth2Api` (or any other credential type) and that credential no longer exists in the workspace, PUT returns 400 `Cannot publish workflow: N nodes have configuration issues`. Fix in the n8n UI before harden can succeed.
- **Pagination.** List endpoints page via `nextCursor` — always loop until cursor is empty.
- **Activate vs PUT-with-active.** Use the dedicated `POST /workflows/<id>/activate` endpoint; setting `active: true` in PUT body is rejected (it's a read-only field on PUT).

## Workflow node-type cheatsheet

API-touching (always retry):
```
n8n-nodes-base.gmail / .gmailTrigger
n8n-nodes-base.googleDrive / .googleSheets / .googleCalendar / .googleContacts
n8n-nodes-base.airtable / .notion / .slack / .telegram
n8n-nodes-base.httpRequest / .webhook
n8n-nodes-base.stripe / .mailerLite / .brevo / .openAi
n8n-nodes-base.tally / .tidyCal / .calendly / .intercom
@n8n/n8n-nodes-langchain.*  (LLM nodes)
n8n-nodes-base.extractFromFile  (PDF parsing — IO-bound)
```

Local logic (skip retry):
```
n8n-nodes-base.set / .code / .function
n8n-nodes-base.if / .switch / .merge
n8n-nodes-base.splitInBatches / .wait / .noOp
n8n-nodes-base.scheduleTrigger / .cron
n8n-nodes-base.manualTrigger / .errorTrigger
```

`tools/n8n-harden.py` enforces this split via regex patterns.

## Backup + rollback procedure

Backups live at `~/appie-brain/n8n-backups/<workflow_id>__<slug>.json`. Daily commit by `tools/n8n-backup.py`.

To roll back a single workflow to its prior state:

```bash
# Find the previous version
git -C ~/clawd log -p -- n8n-backups/<id>__*.json | less

# Restore from a specific commit
git -C ~/clawd show <commit>:n8n-backups/<id>__<slug>.json > /tmp/restore.json

# PUT the trimmed body back via API
python3 -c "
import json
wf = json.load(open('/tmp/restore.json'))
keep = {k: wf[k] for k in ('name','nodes','connections','settings') if k in wf}
json.dump(keep, open('/tmp/put.json','w'))
"
curl -X PUT -H 'X-N8N-API-KEY: $N8N_API_KEY' -H 'Content-Type: application/json' \
  --data-binary @/tmp/put.json \
  https://app.n8n.weblyfe.nl/api/v1/workflows/<id>
```

## Health monitoring

`tools/n8n-health.py` (hourly):
- **Failure check:** queries `/executions?status=error&limit=50`, filters to last 1h window, aggregates by workflow, alerts via Telegram MarkdownV2.
- **Silent-death check:** queries last 200 executions, finds workflows with `scheduleTrigger`/`cron` that have NO successful run in 24h, alerts.
- **Cooldown:** 30 min per alert key (state in `~/appie-brain/.cache/n8n-health-state.json`) so flapping doesn't spam.

State of failing/silent workflows visible in `~/appie-brain/logs/n8n-health.jsonl`. Common patterns:
- *Whatsapp Agent | DRP failures* — likely external Whatsapp API issues; check execution detail.
- *GLOBAL ERROR HANDLER errors* — usually a downstream issue that the handler couldn't auto-fix.

## When to add a new workflow vs modify an existing one

- **Add new** when the trigger source is genuinely different (a new form, a new webhook URL, a new schedule). Naming convention: `{Domain} | {What it does}` (e.g., `PeakSpring | Contact Form`).
- **Modify existing** when the upstream/downstream stays the same and only the body logic changes.
- **Clone-then-modify** when a major refactor is needed (the Gmail Invoicing v2 example): keep the original active until v2 is verified, then deactivate the original. Old workflows are kept around as inactive (don't delete) so we have history.

## Authoritative refs

- Doctrine: `~/appie-brain/knowledge/token-reduction-system/95-token-reduction.md` (output discipline + tier routing — applies to LLM nodes inside n8n flows).
- This skill: `~/appie-brain/skills/n8n-pro/SKILL.md` (you are here).
- Memory pointer: auto-memory `reference_invoice_pipeline.md` carries the fleet-wide ops summary.
- Backup history: `~/appie-brain/n8n-backups/` (47+ workflow JSONs, daily commits on master).
- Tools: `tools/n8n-backup.py`, `tools/n8n-health.py`, `tools/n8n-harden.py`, `tools/invoice-pipeline.py`.

## Recent landmark events

- **2026-05-02 morning.** Gmail Invoicing v1 (`caS-m8n9KKb4tHBobvSgS`) had a Q2 2026 folder ID typo (`Uvxq` vs real `Uvx`) plus 1x/day polling plus no archive-after-process. Patched in-place, then cloned to v2 (`pgKuiPoPpmv9QKgl`, "no AI"), then hardened with multi-PDF support + Stripe TECHWIZ skip + idempotent filename + tightened subject filter. v1 deactivated. Backup at commit `aea94cc`, post-state at `353d084` and `8b43952`.
- **2026-05-02 same morning.** GLOBAL ERROR HANDLER alert recipient updated to include both the primary admin and a secondary address. Retry added to its `Send a message` node.
- **2026-05-02 same morning.** First fleet-wide harden: 28 active workflows scanned, 20 patched (118 nodes received retry+wait defaults). 8 failed PUT validation due to missing credentials in pre-existing nodes — flagged for manual cleanup in n8n UI.
