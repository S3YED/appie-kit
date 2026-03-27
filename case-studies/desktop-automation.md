# Case Study: Desktop Automation with Clawd Cursor

## The Problem

Every SaaS tool your agent needs requires a separate API integration:

| Service | API Key? | OAuth? | Rate Limits? | Maintenance? |
|---------|----------|--------|--------------|--------------|
| Gmail | ✅ | ✅ Complex | ✅ | Breaking changes |
| Slack | ✅ | ✅ | ✅ | Webhook management |
| Jira | ✅ | ✅ | ✅ | Schema changes |
| Figma | ✅ | ✅ | ✅ | Version updates |
| Stripe Dashboard | ✅ | ❌ | ✅ | UI changes |
| Webflow | ✅ | ✅ | ✅ | API deprecations |

That's 6+ API keys, 6+ auth flows, 6+ rate limit handlers, and 6+ integrations that can break when the provider updates their API.

## The Solution

[Clawd Cursor](https://clawdcursor.com) — one OpenClaw skill that gives your agent a screen and a cursor.

```bash
# Install
openclaw skills install clawd-cursor

# Or manual
git clone https://github.com/AmrDab/clawd-cursor.git
cd clawd-cursor && npm install && npm run setup
clawdcursor doctor  # auto-configures providers
clawdcursor start   # starts the agent server
```

Your agent sees the screen and interacts with any app the same way you do. If you're logged in, your agent is too. Zero per-service setup.

## How It Works

Clawd Cursor uses a 3-layer smart pipeline. Each task falls to the cheapest layer that can handle it:

### Layer 1: Action Router ($0, instant)
- Regex + pattern matching
- Queries native accessibility tree
- Finds elements by name, clicks directly
- **Zero LLM calls needed**
- Example: "Open Calculator" → 2 seconds, free

### Layer 2: Accessibility Reasoner ($0 with Ollama)
- Reads the UI Automation tree (text-only, no screenshots)
- Sends to a text LLM for reasoning
- Handles moderate complexity
- Example: "Find the Send button in Gmail" → 1 second

### Layer 3: Screenshot + Vision (cloud pricing)
- Full screenshot sent to vision LLM
- Plans and executes step by step
- Verifies each action before continuing
- Handles multi-app, unfamiliar UIs
- Example: "Copy data from Stripe dashboard to a spreadsheet" → 30-60 seconds

## Real Results

| Task | Time | Cost | Layer |
|------|------|------|-------|
| Open Calculator, type 255*38= | 2.6s | $0 | 1 |
| Chrome → Google Docs → write sentence | 101.7s | ~$0.10 | 3 |
| GitHub → read repos → Notepad → save | 134.1s | ~$0.18 | 3 |
| Open Notepad (Action Router) | ~2s | $0 | 1 |
| Gmail compose email | 21.7s | ~$0.01 | 3 |

## Our Setup (Weblyfe)

We run Clawd Cursor on our Mac Mini (Appie-1) for tasks where we don't have API access:

- **Webflow visual editing** — no API needed for design changes
- **Stripe dashboard checks** — read payment data without API setup
- **Figma exports** — grab assets without Figma API token
- **Browser-based admin panels** — any SaaS tool with a web UI

### Configuration

```json
{
  "provider": "openai",
  "pipeline": {
    "layer2": { "model": "gpt-4o-mini", "provider": "openai" },
    "layer3": { "model": "gpt-4o", "provider": "openai" }
  }
}
```

For cost savings, use Ollama for Layer 2 (free) and cloud only for Layer 3 (vision).

## Safety

Clawd Cursor has built-in safety tiers:

| Tier | Actions | Behavior |
|------|---------|----------|
| **Auto** | Open apps, navigate, read screen | Executes immediately |
| **Preview** | Type text, fill forms | Logged before executing |
| **Confirm** | Send messages, delete files | Waits for human approval |

Sensitive apps (email, banking, messaging) always require confirmation.

## Key Takeaway

> "Stop integrating APIs. Start using the screen."

One skill. Zero API keys per service. Your agent sees what you see and does what you'd do — just faster and 24/7.

**Links:**
- Website: [clawdcursor.com](https://clawdcursor.com)
- GitHub: [github.com/AmrDab/clawd-cursor](https://github.com/AmrDab/clawd-cursor)
- Discord: [discord.gg/UGBWKvmj](https://discord.gg/UGBWKvmj)
