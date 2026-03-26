# HEARTBEAT.md — Proactive Check-In Config

# Your AI reads this file on every heartbeat (configurable interval).
# Use it as a lightweight task list for periodic checks.
# Keep it small to minimize token usage.

## Periodic Checks

### Email (check every 4-6 hours)
- [ ] Check inbox for urgent/unread messages
- [ ] Flag anything from VIP contacts

### Calendar (check every 2-4 hours)
- [ ] Upcoming events in next 24h
- [ ] Prep materials for meetings

### Health (check every heartbeat)
- [ ] Gateway running?
- [ ] Disk space OK?
- [ ] Any error logs?

## Current Tasks
# Add short-term reminders here:
# - [ ] Follow up with {{CLIENT}} about proposal
# - [ ] Check deployment status of {{PROJECT}}
# - [ ] Review analytics for this week

## Notes
# - Heartbeat interval is configured in gateway.yaml (default: 30min)
# - Use cron for exact-time tasks instead of heartbeats
# - Batch similar checks together to save API calls
# - Late night (23:00-08:00): skip non-urgent checks
