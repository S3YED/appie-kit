#!/bin/bash
# Setup OpenClaw on macOS — One-command install
# Usage: ./setup-openclaw-mac.sh

set -e

echo "🧙🏽‍♂️ Setting up OpenClaw on macOS..."
echo ""

# 1. Check prerequisites
echo "=== Checking prerequisites ==="

# Homebrew
if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
echo "  ✅ Homebrew"

# Node.js
if ! command -v node &>/dev/null; then
    echo "Installing Node.js..."
    brew install node
fi
NODE_VERSION=$(node --version)
echo "  ✅ Node.js $NODE_VERSION"

# Git
if ! command -v git &>/dev/null; then
    echo "Installing Git..."
    brew install git
fi
echo "  ✅ Git"

# 2. Install OpenClaw
echo ""
echo "=== Installing OpenClaw ==="
if command -v openclaw &>/dev/null; then
    CURRENT=$(openclaw --version 2>/dev/null || echo "unknown")
    echo "  OpenClaw already installed: $CURRENT"
    echo "  Updating to latest..."
    npm update -g openclaw
else
    echo "  Installing OpenClaw globally..."
    npm install -g openclaw
fi
echo "  ✅ OpenClaw $(openclaw --version 2>/dev/null)"

# 3. Create workspace
echo ""
echo "=== Setting up workspace ==="
WORKSPACE="${HOME}/appie"
if [ -d "$WORKSPACE" ]; then
    echo "  Workspace already exists at $WORKSPACE"
else
    mkdir -p "$WORKSPACE/memory"
    echo "  Created workspace at $WORKSPACE"
fi

# 4. Environment file
if [ ! -f "$WORKSPACE/.env.secrets" ]; then
    cat > "$WORKSPACE/.env.secrets" << 'ENVEOF'
# OpenClaw Environment — Add your API keys here
# NEVER commit this file to git!

# Required: Anthropic API key for Claude
ANTHROPIC_API_KEY=

# Optional: Telegram bot token (from @BotFather)
TELEGRAM_BOT_TOKEN=

# Optional: Other services
# BREVO_API_KEY=
# AIRTABLE_API_KEY=
# OPENAI_API_KEY=
# EXA_API_KEY=
# BRAVE_API_KEY=
ENVEOF
    chmod 600 "$WORKSPACE/.env.secrets"
    echo "  ✅ Created .env.secrets (edit this with your API keys)"
else
    echo "  .env.secrets already exists"
fi

# 5. Tailscale (recommended for security)
echo ""
echo "=== Optional: Tailscale (secure remote access) ==="
if command -v tailscale &>/dev/null; then
    echo "  ✅ Tailscale already installed"
else
    echo "  Recommended: brew install tailscale"
    echo "  This enables secure access to your Appie from anywhere"
fi

# 6. Summary
echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. cd $WORKSPACE"
echo "  2. Edit .env.secrets (add your Anthropic API key)"
echo "  3. Copy workspace files from appie-kit:"
echo "     cp -r /path/to/appie-kit/workspace/* $WORKSPACE/"
echo "  4. Customize SOUL.md, USER.md, TOOLS.md"
echo "  5. Start: openclaw gateway start"
echo ""
echo "Need help? https://weblyfe.ai/openclaw"
echo "=========================================="
