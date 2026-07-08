#!/usr/bin/env bash
USE=$(df / | awk 'NR==2{gsub("%","",$5); print $5}')
if [ "${USE:-0}" -ge 80 ]; then
  rm -rf ~/.cache/pip ~/.cache/uv ~/.cache/huggingface/hub/tmp* /tmp/* 2>/dev/null
  find ~ -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null
  find ~/.hermes/logs -name "*.log" -size +5M -exec truncate -s 1M {} \; 2>/dev/null
  find ~ -maxdepth 4 -type f \( -name "*.mp4" -o -name "*.mov" -o -name "*.webm" -o -name "*.zip" -o -name "*.tar*" \) -mmin +120 -delete 2>/dev/null
  echo "$(date -u) disk-guard purge -> $(df / | awk 'NR==2{print $5}')" >> ~/disk-guard.log
fi
