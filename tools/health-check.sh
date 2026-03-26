#!/bin/bash
# Health Check — Monitor your OpenClaw instance
# Usage: ./health-check.sh

echo "🏥 Health Check — $(hostname) — $(date -u +"%Y-%m-%d %H:%M UTC")"
echo ""

# 1. Gateway status
echo "=== Gateway ==="
GATEWAY_PID=$(pgrep -f "openclaw-gateway" 2>/dev/null || true)
if [ -n "$GATEWAY_PID" ]; then
    echo "  ✅ Running (PID: $GATEWAY_PID)"
    # Uptime
    if command -v ps &>/dev/null; then
        UPTIME=$(ps -p "$GATEWAY_PID" -o etime= 2>/dev/null | xargs)
        echo "  ⏱️  Uptime: $UPTIME"
    fi
else
    echo "  ❌ NOT RUNNING"
    echo "  Fix: openclaw gateway start"
fi

# 2. OpenClaw version
echo ""
echo "=== Version ==="
if command -v openclaw &>/dev/null; then
    echo "  $(openclaw --version 2>/dev/null || echo 'unknown')"
else
    echo "  ❌ OpenClaw not installed"
fi

# 3. Disk space
echo ""
echo "=== Disk Space ==="
if command -v df &>/dev/null; then
    USAGE=$(df -h / | tail -1 | awk '{print $5}')
    echo "  Root: $USAGE used"
    USAGE_NUM=${USAGE%\%}
    if [ "$USAGE_NUM" -gt 90 ]; then
        echo "  🚨 CRITICAL: Disk almost full!"
    elif [ "$USAGE_NUM" -gt 75 ]; then
        echo "  ⚠️  Warning: Disk getting full"
    fi
fi

# 4. Memory
echo ""
echo "=== Memory ==="
if command -v free &>/dev/null; then
    free -h | head -2
elif command -v vm_stat &>/dev/null; then
    # macOS
    PAGES_FREE=$(vm_stat | grep "Pages free" | awk '{print $3}' | tr -d '.')
    PAGES_ACTIVE=$(vm_stat | grep "Pages active" | awk '{print $3}' | tr -d '.')
    echo "  Free pages: $PAGES_FREE | Active pages: $PAGES_ACTIVE"
fi

# 5. Active sessions
echo ""
echo "=== Sessions ==="
SESSION_DIR="${HOME}/.openclaw/sessions"
if [ -d "$SESSION_DIR" ]; then
    TOTAL=$(ls "$SESSION_DIR" 2>/dev/null | wc -l | xargs)
    echo "  Total sessions: $TOTAL"
else
    echo "  Session directory not found"
fi

# 6. Recent errors
echo ""
echo "=== Recent Errors (last 10 lines) ==="
LOG_FILE="${HOME}/.openclaw/logs/gateway.log"
if [ -f "$LOG_FILE" ]; then
    grep -i "error\|fatal\|panic" "$LOG_FILE" 2>/dev/null | tail -5 || echo "  No recent errors"
else
    echo "  No log file found"
fi

echo ""
echo "✅ Health check complete"
