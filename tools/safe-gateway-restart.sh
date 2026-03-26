#!/bin/bash
# Safe Gateway Restart — Zero-downtime restart
# Usage: ./safe-gateway-restart.sh

echo "🔄 Safe Gateway Restart..."

# Check if gateway is running
GATEWAY_PID=$(pgrep -f "openclaw-gateway" 2>/dev/null || true)

if [ -z "$GATEWAY_PID" ]; then
    echo "  Gateway not running. Starting fresh..."
    openclaw gateway start
    echo "  ✅ Gateway started"
    exit 0
fi

echo "  Current PID: $GATEWAY_PID"

# Restart
openclaw gateway restart 2>/dev/null || {
    echo "  ⚠️  Restart command failed, trying stop + start..."
    openclaw gateway stop 2>/dev/null || true
    sleep 2
    openclaw gateway start
}

# Verify
sleep 3
NEW_PID=$(pgrep -f "openclaw-gateway" 2>/dev/null || true)
if [ -n "$NEW_PID" ]; then
    echo "  ✅ Gateway restarted (new PID: $NEW_PID)"
else
    echo "  ❌ Gateway failed to start! Check logs."
    exit 1
fi
