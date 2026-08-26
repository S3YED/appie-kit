#!/usr/bin/env bash
# Daily managed software updater for Clark/Appie fleet nodes.
# Updates installed operating-system packages and managed agent toolchains.
# It never updates project dependencies, reboots, or restarts a serving brain.
set -uo pipefail

MODE="${1:-run}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
STATE_DIR="${MANAGED_UPDATE_STATE_DIR:-$HERMES_HOME/updates}"
LOG="${MANAGED_UPDATE_LOG:-$HERMES_HOME/logs/managed-software-update.log}"
STATUS="$STATE_DIR/managed-software-update.status.json"
LOCK="$STATE_DIR/managed-software-update.lock"
DRY="${MANAGED_UPDATE_DRY_RUN:-0}"
NO_JITTER="${MANAGED_UPDATE_NO_JITTER:-0}"
JITTER_MAX="${MANAGED_UPDATE_JITTER_MAX:-1800}"
FAILED=0
UPDATED=0

mkdir -p "$STATE_DIR" "$(dirname "$LOG")" 2>/dev/null || exit 1
if command -v flock >/dev/null 2>&1; then
  exec 9>"$LOCK"
  flock -n 9 || exit 0
else
  # macOS does not ship flock. mkdir is atomic and gives the same one-run gate.
  LOCKDIR="$LOCK.d"
  mkdir "$LOCKDIR" 2>/dev/null || exit 0
  trap 'rmdir "$LOCKDIR" 2>/dev/null || true' EXIT
fi

ts(){ date -u +%Y-%m-%dT%H:%M:%SZ; }
log(){ printf '%s %s\n' "$(ts)" "$*" | tee -a "$LOG" >&2; }

if [ "$NO_JITTER" != "1" ] && [ "$JITTER_MAX" -gt 0 ] 2>/dev/null; then
  jitter=$(( $(hostname 2>/dev/null | cksum | awk '{print $1}') % JITTER_MAX ))
  log "jitter ${jitter}s"
  sleep "$jitter"
fi

run_lane(){
  local label="$1"; shift
  if [ "$DRY" = "1" ]; then
    printf 'DRY-RUN [%s]' "$label"
    printf ' %q' "$@"
    printf '\n'
    return 0
  fi
  log "START $label"
  if "$@" >>"$LOG" 2>&1; then
    log "OK $label"
    UPDATED=$((UPDATED+1))
    return 0
  fi
  log "UPDATE FAILED $label"
  FAILED=$((FAILED+1))
  return 0
}

with_timeout(){
  local seconds="$1"; shift
  if command -v timeout >/dev/null 2>&1; then timeout "$seconds" "$@"; else "$@"; fi
}

update_apt(){
  with_timeout 3600 bash -c '
    export DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=l
    apt-get -q update &&
    apt-get -y -q -o Dpkg::Options::=--force-confold upgrade &&
    apt-get -y -q autoremove &&
    apt-get clean
  '
}

update_brew(){
  local brew
  brew=$(command -v brew 2>/dev/null || true)
  [ -n "$brew" ] || return 0
  with_timeout 3600 "$brew" update &&
  with_timeout 3600 "$brew" upgrade &&
  "$brew" cleanup
}

update_hermes(){
  with_timeout 600 hermes update --check >>"$LOG" 2>&1 || true
  # Use Hermes' configured/default pre-update snapshot policy. Forcing a full
  # HERMES_HOME zip on every upstream commit fills small customer disks.
  with_timeout 3600 hermes update --yes
}

update_claude(){
  CI=1 with_timeout 1800 claude update
}

update_pipx(){ with_timeout 1800 pipx upgrade-all; }
update_uv(){ with_timeout 1800 uv tool upgrade --all; }
update_npm(){ with_timeout 1800 npm update -g --no-audit --no-fund; }

health_check(){
  local active="hermes"
  [ -r /root/.clark/active-brain ] && active=$(tr -d ' \r\n' </root/.clark/active-brain)
  case "$active" in
    claude)
      pgrep -f 'claude .*--channels' >/dev/null 2>&1 || return 1
      ;;
    hermes)
      pgrep -f '(hermes|hermes_cli).*gateway.*run' >/dev/null 2>&1 || return 1
      ;;
  esac
  if [ -r /root/.clark/poll-health.json ]; then
    python3 - <<'PY'
import datetime,json
p='/root/.clark/poll-health.json'
x=json.load(open(p))
ts=datetime.datetime.fromisoformat(str(x.get('ts','')).replace('Z','+00:00'))
age=(datetime.datetime.now(datetime.timezone.utc)-ts).total_seconds()
assert age < 600 and x.get('telegram_connected') is True
PY
  fi
}

write_status(){
  local result="ok"
  [ "$FAILED" -gt 0 ] && result="failed"
  local tmp="$STATUS.tmp.$$"
  python3 - "$tmp" "$result" "$UPDATED" "$FAILED" <<'PY'
import datetime,json,os,sys
path,result,updated,failed=sys.argv[1:]
with open(path,'w') as f:
 json.dump({'schema_version':'clark.managed-update.v1','ts':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':result,'lanes_completed':int(updated),'lanes_failed':int(failed)},f,separators=(',',':'))
 f.write('\n')
os.chmod(path,0o600)
PY
  mv "$tmp" "$STATUS"
}

case "$MODE" in
  check)
    MANAGED_UPDATE_DRY_RUN=1 MANAGED_UPDATE_NO_JITTER=1 exec "$0" run
    ;;
  run) ;;
  *) echo "usage: $0 run|check" >&2; exit 2 ;;
esac

log "managed update start"
[ "$DRY" = "1" ] && printf 'DRY-RUN discovery\n'
if command -v apt-get >/dev/null 2>&1 && [ "$(id -u)" = "0" ]; then
  run_lane apt update_apt
fi
if command -v brew >/dev/null 2>&1; then run_lane brew update_brew; fi
if command -v hermes >/dev/null 2>&1; then run_lane hermes update_hermes; fi
if command -v claude >/dev/null 2>&1; then run_lane claude update_claude; fi
if command -v pipx >/dev/null 2>&1; then run_lane pipx update_pipx; fi
if command -v uv >/dev/null 2>&1; then run_lane uv-tools update_uv; fi
if command -v npm >/dev/null 2>&1; then run_lane npm-globals update_npm; fi

if [ "$DRY" = "1" ]; then
  log "managed update dry-run complete"
  exit 0
fi

if ! health_check; then
  log "UPDATE DEGRADED post-update serving health failed"
  FAILED=$((FAILED+1))
fi
write_status
if [ "$FAILED" -gt 0 ]; then
  log "UPDATE FAILED lanes=$FAILED completed=$UPDATED"
  exit 1
fi
log "managed update complete lanes=$UPDATED"
exit 0
