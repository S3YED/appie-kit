#!/bin/bash
# fleet-dream.sh — Cross-fleet nightly memory consolidation
# Runs: 05 3 * * * on Appie-1 (Mac Mini)
set +e

TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -v-1d +%Y-%m-%d)
APPIE1_MEM="$HOME/.openclaw/workspace/memory"
FLEET_DREAM_DIR="$HOME/memory/fleet-dreams"
OUT_FILE="$FLEET_DREAM_DIR/$TODAY.md"
SSH_KEY="$HOME/.ssh/id_ed25519"
SSH_OPTS="-o ConnectTimeout=4 -o StrictHostKeyChecking=no -o BatchMode=yes"

mkdir -p "$FLEET_DREAM_DIR"
mkdir -p "$HOME/.openclaw/logs"

{
echo "=== Fleet Dream: $TODAY ==="
echo "Started: $(date '+%H:%M:%S')"
echo ""

# --- Appie-2 (Hetzner VPS) ---
echo "## Appie-2 (Hetzner VPS)"
ssh -i "$SSH_KEY" $SSH_OPTS root@<appie-2-host> \
  "cat /root/.openclaw/workspace/memory/$TODAY.md 2>/dev/null || cat /root/.openclaw/workspace/memory/$YESTERDAY.md 2>/dev/null || echo 'No memory file found'" >> "$OUT_FILE" 2>/dev/null
echo "[OK] Appie-2 done"

# --- Appie-3 (Hetzner VPS) ---
echo "## Appie-3 (Hetzner VPS)"
ssh -i "$SSH_KEY" $SSH_OPTS root@<appie-3-host> \
  "cat /root/.openclaw/workspace/memory/$TODAY.md 2>/dev/null || cat /root/.openclaw/workspace/memory/$YESTERDAY.md 2>/dev/null || echo 'No memory file found'" >> "$OUT_FILE" 2>/dev/null
echo "[OK] Appie-3 done"

# --- Appie-4 (Hetzner VPS) ---
echo "## Appie-4 (Hetzner VPS)"
ssh -i "$SSH_KEY" $SSH_OPTS root@<appie-4-host> \
  "cat /root/.openclaw/workspace/memory/$TODAY.md 2>/dev/null || cat /root/.openclaw/workspace/memory/$YESTERDAY.md 2>/dev/null || echo 'No memory file found'" >> "$OUT_FILE" 2>/dev/null
echo "[OK] Appie-4 done"

# --- Eugi (Hetzner VPS) ---
echo "## Eugi (Hetzner VPS)"
ssh -i "$SSH_KEY" $SSH_OPTS root@<eugi-host> \
  "cat /root/.openclaw/workspace/memory/$TODAY.md 2>/dev/null || cat /root/.openclaw/workspace/memory/$YESTERDAY.md 2>/dev/null || echo 'No memory file found'" >> "$OUT_FILE" 2>/dev/null
echo "[OK] Eugi done"

# --- Spark Atlas ---
echo "## Spark Atlas"
ssh -i "$SSH_KEY" $SSH_OPTS admin@<spark-atlas-host> \
  "cat ~/.openclaw/workspace/memory/$TODAY.md 2>/dev/null || cat ~/.openclaw/workspace/memory/$YESTERDAY.md 2>/dev/null || echo 'No memory file found'" >> "$OUT_FILE" 2>/dev/null
echo "[OK] Spark Atlas done"

# --- Appie-1 Local (Mac Mini) ---
echo "## Appie-1 Local (Mac Mini)"
if [ -f "$APPIE1_MEM/$TODAY.md" ]; then
  cat "$APPIE1_MEM/$TODAY.md" >> "$OUT_FILE"
elif [ -f "$APPIE1_MEM/$YESTERDAY.md" ]; then
  cat "$APPIE1_MEM/$YESTERDAY.md" >> "$OUT_FILE"
else
  RECENT=$(ls "$APPIE1_MEM"/20*.md 2>/dev/null | sort | tail -1)
  if [ -n "$RECENT" ]; then cat "$RECENT" >> "$OUT_FILE"; fi
fi
echo "[OK] Appie-1 done"

# --- Heartbeat state ---
echo ""
echo "## Heartbeat State"
cat "$APPIE1_MEM/heartbeat-state.json" 2>/dev/null || echo "[none]"

echo ""
echo "---"
echo "Fleet Dream completed: $(date '+%Y-%m-%d %H:%M:%S')"

} > "$OUT_FILE" 2>&1

echo "Fleet Dream complete: $OUT_FILE ($(wc -l < "$OUT_FILE") lines)"
