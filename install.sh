#!/bin/bash
# Appie Kit Installer - Copy workspace files and skills to your agent workspace
# Usage: ./install.sh [target-directory]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:-}"

echo "🧙🏽‍♂️ Appie Kit Installer"
echo ""

if [ -z "$TARGET" ]; then
    echo "Usage: ./install.sh /path/to/your/agent/workspace"
    echo ""
    echo "Example:"
    echo "  ./install.sh ~/appie"
    echo "  ./install.sh /home/<agent-user>/workspace"
    echo ""
    echo "This will copy:"
    echo "  - Workspace files (SOUL.md, AGENTS.md, USER.md, etc.)"
    echo "  - Skills: all public skills from skills/<category>/<skill>/ into target/skills/<skill>/"
    echo "  - Tools (security-scan.sh, health-check.sh, etc.)"
    echo "  - .env.example"
    echo ""
    echo "It will NOT overwrite existing files."
    exit 1
fi

# Create target directories
mkdir -p "$TARGET/memory"
mkdir -p "$TARGET/tools"
mkdir -p "$TARGET/skills"

# Copy workspace files (don't overwrite)
echo "=== Copying workspace files ==="
for FILE in AGENTS.md SOUL.md USER.md TOOLS.md IDENTITY.md HEARTBEAT.md; do
    if [ -f "$TARGET/$FILE" ]; then
        echo "  ⏭️  $FILE already exists (skipping)"
    else
        cp "$SCRIPT_DIR/workspace/$FILE" "$TARGET/$FILE"
        echo "  ✅ $FILE"
    fi
done

# Copy skills (don't overwrite)
# Skills are organized as skills/<category>/<skill>/
# We flatten them into target/skills/<skill>/ for agent consumption.
# INDEX.md and README.md at the category level are skipped.
echo ""
echo "=== Copying skills ==="
for CATEGORY_DIR in "$SCRIPT_DIR"/skills/*/; do
    CATEGORY=$(basename "$CATEGORY_DIR")
    # Skip non-directory entries and meta-files
    [ -d "$CATEGORY_DIR" ] || continue
    for SKILL_DIR in "$CATEGORY_DIR"*/; do
        [ -d "$SKILL_DIR" ] || continue
        SKILLNAME=$(basename "$SKILL_DIR")
        if [ -d "$TARGET/skills/$SKILLNAME" ]; then
            echo "  ⏭️  skills/$SKILLNAME already exists (skipping)"
        else
            cp -r "$SKILL_DIR" "$TARGET/skills/$SKILLNAME"
            echo "  ✅ skills/$CATEGORY/$SKILLNAME"
        fi
    done
done

# Copy tools
echo ""
echo "=== Copying tools ==="
for TOOL in "$SCRIPT_DIR"/tools/*.sh; do
    BASENAME=$(basename "$TOOL")
    if [ -f "$TARGET/tools/$BASENAME" ]; then
        echo "  ⏭️  tools/$BASENAME already exists (skipping)"
    else
        cp "$TOOL" "$TARGET/tools/$BASENAME"
        chmod +x "$TARGET/tools/$BASENAME"
        echo "  ✅ tools/$BASENAME"
    fi
done

# Copy .env.example
if [ ! -f "$TARGET/.env.secrets" ]; then
    cp "$SCRIPT_DIR/.env.example" "$TARGET/.env.secrets"
    chmod 600 "$TARGET/.env.secrets"
    echo ""
    echo "  ✅ .env.secrets created (fill in your API keys!)"
else
    echo ""
    echo "  ⏭️  .env.secrets already exists"
fi

echo ""
echo "=========================================="
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET"
echo "  2. Edit SOUL.md (replace {{placeholders}} with your info)"
echo "  3. Edit USER.md (your name, timezone, company)"
echo "  4. Edit .env.secrets (add API keys)"
echo "  5. hermes  (or: openclaw gateway start)"
echo ""
echo "Docs: https://weblyfe.ai/pdf"
echo "GitHub: https://github.com/S3YED/appie-kit"
echo "=========================================="
