# Development & Operations Prompts

## Deploy Check
```
Before deploying {{PROJECT}}:
1. Run git status — any uncommitted changes?
2. Check for console.log/debug statements
3. Verify environment variables are set on Vercel
4. Run build locally to catch errors
5. If all clear, push to main and monitor deployment
6. Verify the live URL works after deploy
```

## Security Audit
```
Run a security audit:
1. Check file permissions on all .env files (should be 600)
2. Scan recent git commits for exposed secrets
3. Verify gateway is bound to localhost only
4. Check SSH key permissions
5. Review open ports
6. Check SSL certificate expiry dates
Report findings and fix anything safe to fix automatically.
```

## Server Health
```
Check all servers:
1. Gateway status (running? uptime?)
2. Disk space (alert if >80%)
3. Memory usage
4. Recent error logs
5. Session count (clean stale ones if >100)
6. SSL cert expiry
Report status for each server.
```

## Database Cleanup
```
Clean up the Airtable base:
1. Find duplicate records (same email)
2. Find records with missing required fields
3. Archive leads older than 90 days with no activity
4. Report what you'd clean (don't delete without approval)
```

## Incident Response
```
{{SERVICE}} is down/broken.
1. Diagnose: What's the error? When did it start?
2. Impact: Who's affected? What's broken?
3. Fix: What's the quickest safe fix?
4. Root cause: Why did it happen?
5. Prevention: How do we stop it happening again?
6. Update HEARTBEAT.md with incident details
```

## Dependency Update
```
Check for outdated dependencies in {{PROJECT}}:
1. npm outdated (or equivalent)
2. Any security vulnerabilities? (npm audit)
3. Which updates are safe (patch/minor)?
4. Which need careful testing (major)?
5. Create a plan to update safely
Don't auto-update major versions without approval.
```

## Backup Verification
```
Verify backups are current:
1. GitHub repos — last push date for each
2. Airtable — can we access via API?
3. Memory files — synced to GitHub?
4. .env.secrets — backed up securely?
5. DNS records — documented?
Report anything that needs attention.
```
