# Case Study: How Weblyfe Runs 3 AI Employees

## The Setup

[Weblyfe](https://weblyfe.ai) is a web design agency based in Thailand (founder is Dutch) that builds brand identities and websites for businesses worldwide. Instead of hiring a team of 10, the founder runs 3 AI employees — each with distinct roles.

### The Fleet

| Agent | Role | Machine | Monthly Cost |
|-------|------|---------|-------------|
| **Appie-1** | Orchestrator | Mac Mini M2 | ~$20 (electricity + API) |
| **Appie-2** | CMO (Marketing) | DigitalOcean 8GB VPS | ~$48 (VPS) + ~$15 (API) |
| **Appie-3** | CTO (DevOps) | DigitalOcean 8GB VPS | ~$48 (VPS) + ~$15 (API) |

**Total: ~$146/month** for 3 AI employees running 24/7.

Compare: A single human assistant in Thailand costs $800-1,200/month. In the US, $3,000-5,000/month.

### What Each Agent Does

**Appie-1 (Orchestrator):**
- Manages calendar, email triage, and client communication
- Dispatches tasks to Appie-2 and Appie-3
- Maintains the master memory and decision log
- Handles all sensitive operations (billing, contracts)
- Runs on Claude Opus (best reasoning)

**Appie-2 (CMO Herald):**
- Competitor monitoring (weekly reports)
- Content generation (blog drafts, social media)
- Email campaigns (Brevo templates, lead nurturing)
- SEO analysis and recommendations
- Runs on Claude Sonnet (good balance of speed/quality)

**Appie-3 (CTO DevOps):**
- Server monitoring and health checks
- Deployment automation (git push → Vercel)
- Security scanning (daily audits)
- Database maintenance
- Runs on Claude Sonnet (shared bucket with Appie-2)

### Communication

All three agents communicate over **Tailscale** (private VPN):
- Direct SSH for commands
- Message relay for async coordination
- Shared GitHub repo for brain sync
- Each has its own Telegram bot for human interaction

### Key Learnings

1. **Separate rate limit buckets matter.** Appie-1 on Opus, Appie-2/3 on Sonnet = no interference.
2. **Heartbeat frequency matters.** Every 30 minutes is too often for VPS agents. 1 hour with Haiku model for heartbeats saves money.
3. **Context size kills VPS performance.** Trimmed workspace files from 77KB to 13KB for DO agents.
4. **Security is non-negotiable.** SSH restricted to Tailscale only. No public ports. Secrets in `.env.secrets` with 600 permissions.

### Real Numbers

| Metric | Before AI | After AI |
|--------|-----------|----------|
| Email response time | 2-4 hours | < 5 minutes |
| Lead capture | Manual copy-paste | Automatic (< 2 seconds) |
| Security audits | Never | Daily, automated |
| Content drafts | 4+ hours/piece | 15 minutes |
| Server monitoring | "Check when it breaks" | 24/7 proactive |
| Weekly competitor reports | 2 hours manual | Automatic, delivered Monday AM |

### What Would Be Different

If starting over:
- Start with 1 agent, add more only when needed
- Use Haiku for all heartbeats from day 1 (cheaper)
- Set up Tailscale before anything else
- Keep workspace files under 15KB total
- Don't store secrets in git (learned the hard way)
