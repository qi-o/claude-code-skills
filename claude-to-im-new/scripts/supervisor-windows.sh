#!/usr/bin/env bash
# Windows (Git Bash) supervisor — nohup process management.
# Sourced by daemon.sh; expects CTI_HOME, SKILL_DIR, PID_FILE, STATUS_FILE, LOG_FILE.
#
# On Windows, Node.js process.pid returns the WINDOWS native PID,
# while Git Bash $! and kill use MSYS2 PIDs — they are incompatible.
# daemon.mjs writes its Windows PID to status.json reliably.
# We use tasklist/taskkill for process lifecycle management.

# ── Internal helpers ──

# Read PID from status.json (daemon.mjs writes its Windows PID here reliably).
_pid_from_status() {
  if [ -f "$STATUS_FILE" ]; then
    grep -o '"pid"[[:space:]]*:[[:space:]]*[0-9]*' "$STATUS_FILE" 2>/dev/null | head -1 | grep -o '[0-9]*'
  fi
}

# Check if a PID is alive on Windows.
# Tries Git Bash kill first (MSYS2 PID), then tasklist (Windows native PID).
_pid_alive_win() {
  local pid="$1"
  [ -n "$pid" ] || return 1
  kill -0 "$pid" 2>/dev/null && return 0
  tasklist //FI "PID eq $pid" //NH 2>/dev/null | grep -q "$pid"
}

# ── Public interface (called by daemon.sh) ──

supervisor_start() {
  nohup node "$SKILL_DIR/dist/daemon.mjs" >> "$LOG_FILE" 2>&1 < /dev/null &
  # Write bash $! as fallback PID; daemon.mjs will overwrite with Windows PID
  echo $! > "$PID_FILE"
}

supervisor_stop() {
  local pid
  pid=$(_pid_from_status)
  if [ -z "$pid" ]; then
    pid=$(read_pid)
  fi
  if [ -z "$pid" ]; then echo "No bridge running"; return 0; fi
  if _pid_alive_win "$pid"; then
    # Try MSYS2 kill first, then Windows taskkill
    kill "$pid" 2>/dev/null || taskkill //PID "$pid" //F 2>/dev/null
    for _ in $(seq 1 10); do
      _pid_alive_win "$pid" || break
      sleep 1
    done
    if _pid_alive_win "$pid"; then
      taskkill //PID "$pid" //F 2>/dev/null
    fi
    echo "Bridge stopped"
  else
    echo "Bridge was not running (stale PID file)"
  fi
  rm -f "$PID_FILE"
}

supervisor_is_managed() {
  # Windows supervisor handles start/stop/status lifecycle itself
  # so that daemon.sh delegates to supervisor_stop/supervisor_is_running
  # instead of using the generic read_pid/pid_alive path (which breaks
  # with Windows native PIDs).
  return 0
}

supervisor_status_extra() {
  # No extra status for Git Bash fallback
  :
}

supervisor_is_running() {
  local pid
  pid=$(_pid_from_status)
  if [ -n "$pid" ]; then
    _pid_alive_win "$pid"
  else
    pid=$(read_pid)
    _pid_alive_win "$pid"
  fi
}
