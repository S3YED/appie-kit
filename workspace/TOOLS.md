# TOOLS.md — Tool Reference

# This file documents what tools your AI has access to.
# Add API endpoints, CLI commands, and service references here.
# NEVER put actual API keys here — use .env.secrets for that.


## AI Models (via OpenRouter)

### MiniMax M2.7 (Recommended)
- Provider: OpenRouter
- Cost: ~$0.01/1M tokens (input), ~$0.03/1M tokens (output)
- Quality: GPT-4 class, excellent reasoning
- Setup: Set OPENROUTER_API_KEY in .env.secrets
- Model ID: minimax/minimax-m2.7

### Claude (fallback)
- Provider: Anthropic via OpenRouter
- Cost: ~$3/1M tokens (opus)
- Best for: complex reasoning, coding, safety-critical tasks
- Setup: Set ANTHROPIC_API_KEY in .env.secrets
- Model ID: anthropic/claude-3.5-sonnet

### Recommended Fallback Chain
1. MiniMax M2.7 (primary)
2. MiniMax M2.7-highspeed (faster)
3. GPT-4o-mini (OpenAI via OpenRouter)
4. Claude-3-haiku (Anthropic fallback)

See full pricing: https://openrouter.ai/models

## Platform Access

### Email (Brevo / SendGrid / etc.)
- Service: {{EMAIL_SERVICE}}
- API docs: {{API_DOCS_URL}}
- Capabilities: Send transactional, manage lists, templates

### CRM (Airtable / HubSpot / etc.)
- Service: {{CRM_SERVICE}}
- Base ID: {{BASE_ID}}
- Tables: {{LIST_YOUR_TABLES}}

### Website (Vercel / Netlify / etc.)
- Service: {{HOSTING_SERVICE}}
- Project: {{PROJECT_NAME}}
- Deploy: `git push` triggers auto-deploy

### DNS (Namecheap / Cloudflare / etc.)
- Service: {{DNS_SERVICE}}
- Domains: {{YOUR_DOMAINS}}

## Custom Scripts

### Security Scan
```bash
./tools/security-scan.sh
# Checks: exposed keys, file permissions, open ports, gateway binding
```

### Health Check
```bash
./tools/health-check.sh
# Checks: gateway status, session count, disk usage, memory
```

### Session Manager
```bash
./tools/session-manager.sh
# Cleans stale sessions, reports active count
```

## API Keys Location

All secrets stored in `.env.secrets` (chmod 600).
Reference them in scripts via:
```bash
source .env.secrets
echo $BREVO_API_KEY  # Available in shell
```

## MCP Servers
# List any MCP servers your AI connects to:
# - Notion: Search, query databases, create/update pages
# - Offorte: Create proposals, track views, manage templates
# - n8n: Trigger workflows, manage automations

## Notes
# Add tool-specific notes here as you discover them:
# - "Vercel encrypted env vars corrupt JWT tokens — always use plain type"
# - "Airtable rate limit: 5 requests/sec"
# - "Brevo: 300 emails/day on free plan"
