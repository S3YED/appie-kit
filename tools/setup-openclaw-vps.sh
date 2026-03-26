#!/bin/bash
# Setup OpenClaw on Ubuntu/Debian VPS — One-command install
# Usage: curl -sSL https://raw.githubusercontent.com/S3YED/appie-kit/main/tools/setup-openclaw-vps.sh | bash
# Or: ./setup-openclaw-vps.sh

set -e

echo "🧙🏽‍♂️ Setting up OpenClaw on VPS..."
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo ./setup-openclaw-vps.sh"
    exit 1
fi

# 1. System updates
echo "=== Updating system ==="
apt-get update -qq
apt-get upgrade -y -qq

# 2. Install Node.js (LTS)
echo ""
echo "=== Installing Node.js ==="
if ! command -v node &>/dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
    apt-get install -y nodejs
fi
echo "  ✅ Node.js $(node --version)"
echo "  ✅ npm $(npm --version)"

# 3. Install essential tools
echo ""
echo "=== Installing tools ==="
apt-get install -y -qq git curl jq ufw

# 4. Install OpenClaw
echo ""
echo "=== Installing OpenClaw ==="
npm install -g openclaw
echo "  ✅ OpenClaw $(openclaw --version 2>/dev/null)"

# 5. Firewall setup
echo ""
echo "=== Configuring firewall ==="
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
echo "  ✅ UFW configured (SSH only)"
echo "  ⚠️  Add Tailscale for secure remote access (recommended over public SSH)"

# 6. Create appie user
echo ""
echo "=== Creating appie user ==="
if id "appie" &>/dev/null; then
    echo "  User 'appie' already exists"
else
    useradd -m -s /bin/bash appie
    echo "  ✅ Created user 'appie'"
fi

# 7. Setup workspace
WORKSPACE="/home/appie/clawd"
mkdir -p "$WORKSPACE/memory"
mkdir -p "$WORKSPACE/tools"

# Create env file
if [ ! -f "$WORKSPACE/.env.secrets" ]; then
    cat > "$WORKSPACE/.env.secrets" << 'ENVEOF'
# OpenClaw Environment — Add your API keys here
ANTHROPIC_API_KEY=
TELEGRAM_BOT_TOKEN=
ENVEOF
    chmod 600 "$WORKSPACE/.env.secrets"
fi

chown -R appie:appie "$WORKSPACE"
echo "  ✅ Workspace at $WORKSPACE"

# 8. Tailscale (optional but recommended)
echo ""
echo "=== Optional: Tailscale ==="
if command -v tailscale &>/dev/null; then
    echo "  ✅ Tailscale already installed"
else
    echo "  Install with: curl -fsSL https://tailscale.com/install.sh | sh"
    echo "  Then: tailscale up"
    echo "  This replaces public SSH with secure private access"
fi

# 9. Systemd service
echo ""
echo "=== Creating systemd service ==="
cat > /etc/systemd/system/openclaw.service << 'SVCEOF'
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=appie
WorkingDirectory=/home/appie/clawd
ExecStart=/usr/bin/openclaw gateway start --foreground
Restart=always
RestartSec=10
Environment=HOME=/home/appie

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
echo "  ✅ Service created (start with: systemctl start openclaw)"

# Summary
echo ""
echo "=========================================="
echo "✅ VPS Setup complete!"
echo ""
echo "Next steps:"
echo "  1. su - appie"
echo "  2. cd ~/clawd"
echo "  3. Edit .env.secrets (add your API keys)"
echo "  4. Copy workspace files from appie-kit"
echo "  5. systemctl start openclaw"
echo "  6. systemctl enable openclaw (auto-start on boot)"
echo ""
echo "Security recommendations:"
echo "  - Install Tailscale and disable public SSH"
echo "  - Set up token-guard.sh as a cron job"
echo "  - Run security-scan.sh daily"
echo "=========================================="
