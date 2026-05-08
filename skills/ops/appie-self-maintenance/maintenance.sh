#!/bin/bash
# Appie-2 Self-Maintenance Script
# Run by cron or on-demand

WORKSPACE="/root/.openclaw/workspace"
HEARTBEAT="$WORKSPACE/HEARTBEAT.md"
MEMORY="$WORKSPACE/memory"
GIT_DIR="$WORKSPACE/.git"
LOG_FILE="/tmp/appie-maintenance.log"

log() {
    echo "[$(date)] $1" >> $LOG_FILE
}

log "=== Starting self-maintenance ==="

# 1. Gateway health
GW_STATUS=$(curl -s http://127.0.0.1:18789/ 2>/dev/null | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "DOWN")
log "Gateway status: $GW_STATUS"

# 2. Disk space
DISK=$(df -h /root | tail -1 | awk '{print $5}' | sed 's/%//')
log "Disk usage: ${DISK}%"

# 3. Git status
cd $WORKSPACE
HAS_CHANGES=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$HAS_CHANGES" -gt 0 ]; then
    log "Git has $HAS_CHANGES uncommitted changes"
else
    log "Git is clean"
fi

# 4. Memory file freshness
TODAY_MEM="$MEMORY/$(date +%Y-%m-%d).md"
if [ -f "$TODAY_MEM" ]; then
    log "Today's memory exists"
else
    log "WARNING: Today's memory file missing"
fi

# 5. Archive old memory (>7 days)
find $MEMORY -name "2026-*.md" -mtime +7 ! -name "*.dreams*" -exec echo "Old memory: {}" \; >> $LOG_FILE 2>/dev/null

# 6. OpenClaw version
OC_VERSION=$(openclaw --version 2>/dev/null | head -1 || echo "unknown")
log "OpenClaw version: $OC_VERSION"

# 7. Update HEARTBEAT if issues found
if [ "$GW_STATUS" != "ok" ] && [ "$GW_STATUS" != "ready" ]; then
    log "WARNING: Gateway may be unhealthy"
fi

if [ "$DISK" -gt 90 ]; then
    log "WARNING: Disk above 90%"
fi

log "=== Maintenance complete ==="
echo "[$(date)] Maintenance ran - GW:$GW_STATUS DISK:${DISK}% CHANGES:$HAS_CHANGES"
