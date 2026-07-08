#!/usr/bin/env bash
exec >>/root/provision2.log 2>&1
echo "=== fix start $(date -u) ==="
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y xz-utils ca-certificates curl git
echo "xz: $(which xz) $(xz --version 2>/dev/null | head -1)"
echo "=== re-run provision ==="
bash /root/run-prov.sh
echo "=== fix done $(date -u) ==="
