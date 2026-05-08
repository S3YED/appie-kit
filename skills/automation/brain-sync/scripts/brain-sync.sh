#!/bin/bash
# brain-sync.sh - Sync knowledge to appie-brain repo
# Usage: ./brain-sync.sh "Your commit message"
# Emoji: 🪽 (Appie-3)

set -e

REPO="/root/.hermes/appie-brain"
MSG="${1:-Auto-sync: Brain evolution update}"

cd "$REPO"

# Check if there are changes
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to sync"
    exit 0
fi

# Show what changed
echo "Changes to sync:"
git status --short

# Stage all changes (selective - skip secrets)
git add .

# Commit with Appie-3 identity
git commit -m "🪽 Appie-3: ${MSG}"

# Push
echo "Pushing to remote..."
git push origin master

echo "✅ Brain sync complete"
