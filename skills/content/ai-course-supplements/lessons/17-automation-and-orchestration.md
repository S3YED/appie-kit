---
name: 17-automation-and-orchestration
title: n8n + Hermes for 5-creator agency operation
fills_gap: Course assumes a single operator clicking buttons in ComfyUI, posting to IG by hand, replying to Fanvue DMs in person. That maxes out at 1 creator / 12 hour day. Real agencies in 2026 run 5-10 creators on a webhook-driven orchestration layer. This lesson is the n8n + Hermes blueprint for that layer.
course_module: AIIC V2 Phase 4 (Boosting), Vault (general operational), nothing on automation
date_researched: 2026-05-07
---

# n8n + Hermes for 5-creator agency operation

## Why this lesson exists

Lesson 10 (multi-creator scale) gives you the ComfyUI side: subgraph blueprints, per-creator JSON config, master workflow. That handles generation. It does not handle the rest of the loop: where the rendered file goes, who posts it, when ManyChat fires, when a Fanvue subscription event triggers a custom-content offer, how Notion gets updated, how Telegram alerts the operator, how 5 creators run in parallel without colliding.

By 2026, two open-source orchestration layers solve this without writing custom infra:
- **n8n** for the workflow graph (HTTP triggers, retries, branch logic, OpenAI/Claude calls).
- **Hermes** (Seyed's MiniMax-2.7 fleet runtime, sibling to OpenClaw) for autonomous agent dispatch on top of n8n's mechanical workflow.

This lesson is the n8n template + Hermes integration blueprint. It assumes the n8n-pro skill is already deployed (Seyed has this; n8n.weblyfe.nl). It builds on top.

## What's the 2026 state of the art

Five integration primitives compose the agency stack:

1. **n8n-nodes-comfyui** (npm package, MIT). Drops a ComfyUI node into n8n. Workflow JSON in, generated images/videos out (JPEG/PNG/WebP/Raw), API-key auth, configurable timeout (up to 20 min), per-item execution. Default endpoint http://127.0.0.1:8188. https://registry.npmjs.org/n8n-nodes-comfyui · https://ncnodes.com/package/n8n-nodes-comfyui
2. **n8n-nodes-cloudflare-r2-storage v0.3.0** (jezweb, Aug 2025). Native R2 PUT/GET, batch ops, much cleaner than n8n's S3 node which has known compatibility issues with R2 (community Issue Feb 2025). https://registry.npmjs.org/n8n-nodes-cloudflare-r2-storage · https://github.com/jezweb/n8n-nodes-cloudflare-r2 · https://community.n8n.io/t/s3-node-with-cloudflare-r2-issue/76824
3. **ComfyDeploy webhook API**. `runUpdateWebhook` fires on every status transition (queued / running / success / error). Use when you split rendering across local Spark + cloud burst capacity. https://docs.comfydeploy.com/docs/api/runUpdateWebhook · https://docs.comfydeploy.com/docs/api · https://github.com/comfy-deploy/comfy-deploy-ts
4. **Fanvue Webhooks API** (live 2026, `api.fanvue.com`). Five event types: Message Received, Message Read, New Follower, New Subscriber, Purchase Received, Tip Received. POST to your endpoint, 2xx required, retries on non-2xx. Configured per-app in Fanvue Developer Area. https://api.fanvue.com/docs/webhooks/webhooks/webhooks-overview · https://api.fanvue.com/docs/webhooks/webhooks/new-subscriber · https://api.fanvue.com/docs · https://api.fanvue.com/docs/integrations/conversion-tracking
5. **ManyChat triggers + webhooks**. Comments-trigger and Auto-DM-from-comments natively; outbound webhook to n8n on link-click for Notion logging. Known instability after 2-3 messages with sync webhooks; use async pattern. https://help.manychat.com/hc/en-us/articles/14281316989724-Instagram-Post-and-Reel-Comments-trigger · https://help.manychat.com/hc/en-us/articles/16654065283100-Quick-Automation-Auto-DM-links-from-comments · https://community.manychat.com/general-q-a-43/instagram-dm-automation-unstable-after-2-3-messages-manychat-make-webhook-synchronous-issue-9521

Plus three Notion building blocks:
- **Notion API** for per-creator databases. Asset library, posting calendar, revenue tracker, custom-commission queue. https://developers.notion.com/docs/creating-pages-from-templates · https://developers.notion.com/reference/post-page · https://www.notion.com/templates/creator-calendar
- **n8n Telegram multi-bot node** (G0ld9n/n8n-nodes-telegram-multi). Solves the standard n8n Telegram-bot single-bot limitation; enables one bot per creator without spinning up multiple n8n instances. https://github.com/G0ld9n/n8n-nodes-telegram-multi · https://github.com/n8n-io/n8n/issues/13826
- **Multi-user Telegram routing** workflow template (n8n.io); per-user state via Redis or n8n's static data. https://n8n.io/workflows/7664-telegram-bot-inline-keyboard-with-dynamic-menus-and-rating-system

## How to set it up on Spark (orchestration blueprint)

**Architecture (5-creator agency):**

```
ComfyUI on Spark  ─────────►  n8n (n8n.weblyfe.nl)  ◄─── Fanvue webhooks
        ▲                        │  ▲       │         ◄─── ManyChat webhooks
        │                        │  │       │         ◄─── ComfyDeploy bursts
        │                        ▼  │       ▼
        │                    R2 store    Notion (per-creator DB)
        │                                Telegram (per-creator bot)
        │                                Hermes (Appie-3) agent dispatch
        └────── Hermes triggers next render via ComfyUI API ─────┘
```

### 1. Install community nodes

```bash
# In n8n container or self-host
npm install n8n-nodes-comfyui n8n-nodes-cloudflare-r2-storage @G0ld9n/n8n-nodes-telegram-multi
n8n start --tunnel  # restart to load community nodes
```

### 2. Per-creator config layer

```json
{
  "creator_id": "eva",
  "comfyui_workflow": "creators/eva/master.json",
  "lora_path": "creators/eva/lora-v3.safetensors",
  "fanvue_webhook_secret": "...",
  "manychat_page_token": "...",
  "telegram_bot_token": "...",
  "notion_db_id": "...",
  "r2_bucket": "creators-eva",
  "ig_handle": "eva_lifestyle",
  "default_sub_price_cents": 999
}
```

Store in Notion or a private GitHub repo, not in n8n credentials (keep n8n stateless).

### 3. Workflow A — daily render → R2 → Notion log → Telegram alert

```
Schedule Trigger (06:00 CET, per creator stagger)
  ↓
Get Creator Config (HTTP from config repo)
  ↓
ComfyUI Node (workflow JSON from config)
  ↓
Cloudflare R2 PUT (object key: creators/{id}/{date}-{seq}.jpg)
  ↓
Notion Append (creator_db, status=ready, asset_url, timestamp)
  ↓
Telegram Multi (creator's bot, "✓ 6 new assets ready")
```

### 4. Workflow B — Fanvue New Subscriber → ManyChat welcome → Notion → Telegram

```
Webhook (POST /fanvue/{creator_id}/new-subscriber)
  ↓
Verify HMAC signature
  ↓
Notion Append (subscribers_db, sender_uuid, price_minor, ts)
  ↓
ManyChat API (Send welcome flow to sender_handle)
  ↓
HTTP to Hermes (queue: prepare welcome PPV pack for {creator}/{sender})
  ↓
Telegram Multi (operator's bot, "💸 New sub for {creator}: ${price}")
```

### 5. Workflow C — ComfyUI rendered → multi-channel publish

```
Webhook from ComfyUI (or n8n schedule)
  ↓
Branch:
  ├─ R2 upload (storage of record)
  ├─ HTTP to Buffer/Later/Metricool (IG schedule)
  ├─ HTTP to Fanvue API (PPV draft)
  └─ HTTP to ManyChat (broadcast trigger if new-subs flow)
  ↓
Notion calendar entry (status=scheduled, channel mix)
```

### 6. Workflow D — Bouncy AI link rotation on threshold

```
Cron (every 6h)
  ↓
HTTP get IG follower count (Graph API)
  ↓
If delta > threshold (warmup phase complete):
   Bouncy AI API (rotate to Fanvue link)
   Notion Append (event=link_rotated)
   Telegram Multi (operator alert)
```

### 7. Hermes agent layer (Appie-3, MiniMax 2.7)

Where n8n is mechanical (if-this-then-that), Hermes handles fuzzy decisions:

- "Three subs in last hour from one IP cluster — fraud or organic?"
- "PPV pack performing 3 SD below mean — re-render with different style?"
- "Fanvue chat backlog at 47 unread — generate first-pass replies for operator review?"

Hermes integrates via:
```bash
# n8n HTTP node calls Hermes Atlas
POST https://hermes.weblyfe.internal/dispatch
{
  "agent": "appie-3",
  "task": "review fanvue chat backlog for {creator_id}",
  "context_url": "notion://chat-export/{creator_id}/today",
  "callback": "https://n8n.weblyfe.nl/webhook/hermes-callback/{run_id}"
}
```

Hermes Atlas + skills/openclaw-imports/n8n integration patterns are documented in the Hermes runtime (`~/.hermes/skills/`).

## Quality benchmarks

- n8n single-instance throughput: 1000+ executions/hour on Hetzner CX22 (€4/month). 5-creator agency at 100 events/creator/day = 500 events/day, ~5% of capacity.
- ComfyUI node timeout default 60s, raise to 600-1200s for video generation. Past 1200s, switch to async ComfyDeploy webhook pattern.
- Fanvue webhook delivery: at-least-once with retries. Idempotency by ts+sender_uuid.
- ManyChat webhook: known instability past 2-3 sync calls. Always answer 2xx within 1.5s, then process async via internal queue.
- R2 vs S3: R2 is ~30% cheaper at AI-creator volumes (no egress fees) but n8n's S3 node has compatibility quirks; use the dedicated R2 node.
- Notion API: 3 requests/sec/integration. Batch with `database.query` not per-page reads.

## Common failure modes + fixes

- **n8n executes ComfyUI node twice on retry** → ComfyUI happily renders twice, R2 has duplicates, Notion logs both. Fix: idempotency key in workflow JSON (seed = hash of trigger ts + creator_id + asset_id), drop duplicates downstream.
- **R2 with n8n's S3 node** → silent auth failures. Use `n8n-nodes-cloudflare-r2-storage` directly.
- **ManyChat sync webhook stalls** → pattern: ManyChat → cheap n8n endpoint that 200s immediately → internal queue (Redis BLPOP or n8n trigger) → real workflow. Don't do real work on the ManyChat webhook itself.
- **Single Telegram bot for 5 creators** → message routing collisions. Use n8n-nodes-telegram-multi with one bot per creator. Issue #13826 documents the limitation; multi-node solves it.
- **Notion rate limit** (429) → exponential backoff. Or upgrade to a Notion enterprise plan; agency-scale usage usually fits Pro.
- **Fanvue webhook secret rotation** without n8n update → events drop silently. Schedule a quarterly rotation reminder (n8n cron + Telegram alert).
- **Hermes agent loop** → if Hermes call has no callback timeout, n8n hangs. Always set HTTP node timeout 60s with retry; Hermes async work returns via callback webhook.

## When to choose this over the course's recipe

- **Always**, when running ≥2 creators. The marginal cost of n8n is hours, not days; the savings on operator time at 2 creators already pay it off.
- **Always**, when responsiveness matters: Fanvue subscriber gets a ManyChat welcome within 30 seconds vs hours-later if operator is asleep.
- **Always**, for 24/7 ops where the operator is in BKK and Fanvue traffic spikes US-evening: workflow A schedule fires while you sleep.
- **Always**, when planning to delegate (VAs, chatters, managers): n8n + Notion is the source of truth they read; no mystery operator knowledge.
- **Skip the Hermes layer** for the first 30 days; just run n8n. Add Hermes when fuzzy decisions repeat enough to be worth automating (~3 occurrences).
- **Stick with manual operation** only at single-creator pre-revenue. Once Tier 2 is in sight (lesson 14 thresholds), automate or get out-scaled.

## Sources

- https://registry.npmjs.org/n8n-nodes-comfyui
- https://ncnodes.com/package/n8n-nodes-comfyui
- https://sebsvisual.com/2024/07/21/automating-ai-image-generation-with-n8n-and-comfyui/
- https://www.alexanderharte.com/comfyui-api-integration-guide/
- https://registry.npmjs.org/n8n-nodes-cloudflare-r2-storage
- https://github.com/jezweb/n8n-nodes-cloudflare-r2
- https://community.n8n.io/t/s3-node-with-cloudflare-r2-issue/76824
- https://ncnodes.com/node/@jezweb-n8n-nodes-cloudflare-r2@0.1.0-cloudflarer2/Batch%20Operations:Delete%20Multiple
- https://docs.comfydeploy.com/docs/api/runUpdateWebhook
- https://docs.comfydeploy.com/docs/api
- https://github.com/comfy-deploy/comfy-deploy-ts
- https://www.comfydeploy.com/blog/create-your-comfyui-based-app-and-served-with-comfy-deploy/
- https://api.fanvue.com/docs
- https://api.fanvue.com/docs/webhooks/webhooks/webhooks-overview
- https://api.fanvue.com/docs/webhooks/webhooks/new-subscriber
- https://api.fanvue.com/docs/integrations/conversion-tracking
- https://help.manychat.com/hc/en-us/articles/14281316989724-Instagram-Post-and-Reel-Comments-trigger
- https://help.manychat.com/hc/en-us/articles/16654065283100-Quick-Automation-Auto-DM-links-from-comments
- https://community.manychat.com/general-q-a-43/instagram-dm-automation-unstable-after-2-3-messages-manychat-make-webhook-synchronous-issue-9521
- https://developers.notion.com/docs/creating-pages-from-templates
- https://developers.notion.com/reference/post-page
- https://developers.notion.com/guides/data-apis/workspace-setup-for-public-integrations
- https://www.notion.com/templates/creator-calendar
- https://github.com/G0ld9n/n8n-nodes-telegram-multi
- https://github.com/n8n-io/n8n/issues/13826
- https://n8n.io/workflows/7664-telegram-bot-inline-keyboard-with-dynamic-menus-and-rating-system
- https://www-staging.n8n.io/workflows/5468-multi-user-telegram-bot-to-summarize-and-repurpose-youtube-videos-with-gpt-4o/
