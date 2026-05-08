#!/bin/bash
# install-ssh-keys.sh — Run ONCE on Appie-3 and Appie-4 to enable fleet-dream
# Adds Appie-1's SSH public key to authorized_keys
# Run on each Hermes server via: bash <this script> from your terminal

set -e

# Appie-1's public key (Mac Mini)
APPY1_PUBKEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIF5Qk/HR6Dazsn0ruojjFhrxzy+1S40hoYnt0bJDU1qC appie-1-macmini"

echo "Installing Appie-1 SSH key on $(hostname)..."

# Create .ssh dir
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add key if not already present
if ! grep -q "appie-1-macmini" ~/.ssh/authorized_keys 2>/dev/null; then
  echo "$APPY1_PUBKEY" >> ~/.ssh/authorized_keys
  echo "Key added ✅"
else
  echo "Key already present ✅"
fi

chmod 600 ~/.ssh/authorized_keys
echo "Done. Appie-1 can now SSH to this host."
