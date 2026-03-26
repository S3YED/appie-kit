# TOOLS.md — Tool Reference

# This file documents what tools your AI has access to.
# Add API endpoints, CLI commands, and service references here.
# NEVER put actual API keys here — use .env.secrets for that.

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
