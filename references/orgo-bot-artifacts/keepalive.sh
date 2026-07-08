#!/usr/bin/env bash
# Persistent supervisor. Respawns the gateway, runs the auto-pair claim as a
# one-shot each tick (no long-lived watcher for Orgo to reap), and clock-syncs.
while true; do
  D=$(curl -sI --max-time 8 https://www.google.com 2>/dev/null | awk -F': ' 'BEGIN{IGNORECASE=1} $1=="date"{print $2}' | tr -d '\r')
  [ -n "$D" ] && date -s "$D" >/dev/null 2>&1
  pgrep -f 'gateway run' >/dev/null 2>&1 || tmux new-session -d -s gw 'hermes gateway run >/root/gw.log 2>&1'
  python3 /root/pair-claim.py --once >>/root/pair.log 2>&1
  pgrep -f disk-guard-loop >/dev/null 2>&1 || nohup ~/disk-guard-loop.sh >/dev/null 2>&1 &
  sleep 15
done
