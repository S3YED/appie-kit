#!/bin/bash
# Security Scan — Daily audit for your OpenClaw workspace
# Usage: ./security-scan.sh [workspace-path]
# Checks: exposed secrets, file permissions, open ports, gateway binding

set -e

WORKSPACE="${1:-$(pwd)}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ISSUES=0

echo "🔒 Security Scan Started - $(hostname) - $TIMESTAMP"

# 1. Check for exposed secrets in recent git commits
echo "  [1/5] Scanning for exposed secrets in git..."
if [ -d "$WORKSPACE/.git" ]; then
    EXPOSED=$(git -C "$WORKSPACE" log --all --pretty=format: -p --since="7 days ago" 2>/dev/null | \
        grep -iE "(sk-[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36}|xox[baprs]-[a-zA-Z0-9-]{10,})" | \
        head -5)
    if [ -n "$EXPOSED" ]; then
        echo "  ⚠️  POTENTIAL SECRETS IN GIT HISTORY"
        ISSUES=$((ISSUES + 1))
    else
        echo "  ✅ No secrets found in recent commits"
    fi
else
    echo "  ⏭️  Not a git repo, skipping"
fi

# 2. Check file permissions on sensitive files
echo "  [2/5] Checking file permissions..."
for SENSITIVE in ".env" ".env.secrets" ".env.local"; do
    if [ -f "$WORKSPACE/$SENSITIVE" ]; then
        PERMS=$(stat -f "%Lp" "$WORKSPACE/$SENSITIVE" 2>/dev/null || stat -c "%a" "$WORKSPACE/$SENSITIVE" 2>/dev/null)
        if [ "$PERMS" != "600" ]; then
            echo "  ⚠️  $SENSITIVE has permissions $PERMS (should be 600)"
            ISSUES=$((ISSUES + 1))
        else
            echo "  ✅ $SENSITIVE permissions OK (600)"
        fi
    fi
done

# 3. Check SSH key permissions
echo "  [3/5] Checking SSH key permissions..."
for KEY in ~/.ssh/id_*; do
    if [ -f "$KEY" ] && [[ "$KEY" != *.pub ]]; then
        PERMS=$(stat -f "%Lp" "$KEY" 2>/dev/null || stat -c "%a" "$KEY" 2>/dev/null)
        if [ "$PERMS" != "600" ]; then
            echo "  ⚠️  $KEY has permissions $PERMS (should be 600)"
            ISSUES=$((ISSUES + 1))
        fi
    fi
done
echo "  ✅ SSH keys checked"

# 4. Check gateway binding (should be localhost only)
echo "  [4/5] Checking gateway binding..."
GATEWAY_PID=$(pgrep -f "openclaw-gateway" 2>/dev/null || pgrep -f "openclaw gateway" 2>/dev/null || true)
if [ -n "$GATEWAY_PID" ]; then
    # Check if gateway is bound to 0.0.0.0 (dangerous!)
    PUBLIC_BIND=$(lsof -i -P -n 2>/dev/null | grep "$GATEWAY_PID" | grep "0.0.0.0" || true)
    if [ -n "$PUBLIC_BIND" ]; then
        echo "  🚨 CRITICAL: Gateway bound to 0.0.0.0 (publicly accessible!)"
        ISSUES=$((ISSUES + 1))
    else
        echo "  ✅ Gateway bound to localhost only"
    fi
else
    echo "  ⏭️  Gateway not running"
fi

# 5. Check for hardcoded secrets in workspace files
echo "  [5/5] Scanning workspace for hardcoded secrets..."
HARDCODED=$(grep -rl --include="*.md" --include="*.yaml" --include="*.yml" --include="*.json" --include="*.js" --include="*.ts" \
    -E "(sk-[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36})" \
    "$WORKSPACE" 2>/dev/null | grep -v node_modules | grep -v .git | head -5)
if [ -n "$HARDCODED" ]; then
    echo "  ⚠️  Possible secrets found in:"
    echo "$HARDCODED" | sed 's/^/    /'
    ISSUES=$((ISSUES + 1))
else
    echo "  ✅ No hardcoded secrets found"
fi

# Summary
echo ""
if [ $ISSUES -eq 0 ]; then
    echo "✅ Security scan complete — no issues found"
else
    echo "⚠️  Security scan complete — $ISSUES issue(s) found"
fi

exit $ISSUES
