#!/bin/bash
# Session Manager — Clean stale sessions and manage memory
# Usage: ./session-manager.sh [clean|status]

ACTION="${1:-status}"
SESSION_DIR="${HOME}/.openclaw/sessions"
MAX_AGE_HOURS=24

case "$ACTION" in
    status)
        echo "📊 Session Status — $(date -u +"%Y-%m-%d %H:%M UTC")"
        if [ -d "$SESSION_DIR" ]; then
            TOTAL=$(ls "$SESSION_DIR" 2>/dev/null | wc -l | xargs)
            echo "  Total sessions: $TOTAL"
            
            # Count by age
            RECENT=$(find "$SESSION_DIR" -maxdepth 1 -mmin -60 2>/dev/null | wc -l | xargs)
            OLD=$(find "$SESSION_DIR" -maxdepth 1 -mmin +1440 2>/dev/null | wc -l | xargs)
            echo "  Active (last hour): $RECENT"
            echo "  Stale (>24h): $OLD"
        else
            echo "  No session directory found"
        fi
        ;;
    
    clean)
        echo "🧹 Cleaning stale sessions (>${MAX_AGE_HOURS}h old)..."
        if [ -d "$SESSION_DIR" ]; then
            COUNT=0
            for SESSION in $(find "$SESSION_DIR" -maxdepth 1 -mmin +$((MAX_AGE_HOURS * 60)) -type d 2>/dev/null); do
                echo "  Removing: $(basename $SESSION)"
                rm -rf "$SESSION"
                COUNT=$((COUNT + 1))
            done
            echo "  ✅ Cleaned $COUNT stale sessions"
        else
            echo "  No session directory found"
        fi
        ;;
    
    *)
        echo "Usage: $0 [status|clean]"
        exit 1
        ;;
esac
