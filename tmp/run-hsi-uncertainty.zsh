#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="${0:A:h:h}"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
EVIDENCE_DIR="${1:?evidence directory required}"
shift
RUN_LOG="$EVIDENCE_DIR/runner.log"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

cd "$PROJECT_ROOT"
mkdir -p "$EVIDENCE_DIR"

heartbeat_pid=""
child_pid=""
cleaned=0
cleanup_trigger="EXIT"

cleanup() {
  if (( cleaned )); then
    return
  fi
  cleaned=1
  if [[ -n "$heartbeat_pid" ]]; then
    kill "$heartbeat_pid" 2>/dev/null || true
    wait "$heartbeat_pid" 2>/dev/null || true
  fi
  "$PYTHON" -c 'from datetime import datetime, timezone; import json, pathlib, sys; p=pathlib.Path(sys.argv[1]); p.write_text(json.dumps({"at": datetime.now(timezone.utc).isoformat(), "trigger": sys.argv[2], "offline_only": True, "sources_touched": False, "device_calls_performed": False, "status": "safe_by_device_isolation", "reason": "Phase A prohibits camera, Ray, ESPHome, and real all-off calls"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")' \
    "$EVIDENCE_DIR/all-off-shell.json" "$cleanup_trigger" || true
}

on_signal() {
  local signal="$1"
  trap - "$signal"
  cleanup_trigger="$signal"
  cleanup
  if [[ -n "$child_pid" ]]; then
    kill -"$signal" "$child_pid" 2>/dev/null || true
    wait "$child_pid" 2>/dev/null || true
  fi
  exit 128
}

trap cleanup EXIT
trap 'on_signal INT' INT
trap 'on_signal TERM' TERM
trap 'on_signal HUP' HUP

(
  while true; do
    date -u '+heartbeat %Y-%m-%dT%H:%M:%SZ' >>"$RUN_LOG"
    sleep 60
  done
) &
heartbeat_pid="$!"

"$PYTHON" -m camera_based_rgbww_optimizer.measurement.hsi_uncertainty \
  --output "$PROJECT_ROOT/config/hsi/strip-hsi-uncertainty.json" \
  --evidence-dir "$EVIDENCE_DIR" \
  "$@" \
  >>"$RUN_LOG" 2>&1 &
child_pid="$!"

"$PYTHON" -c 'import json, os, pathlib, sys; p=pathlib.Path(sys.argv[1]); p.write_text(json.dumps({"wrapper_pid": os.getppid(), "child_pid": int(sys.argv[2]), "run_dir": sys.argv[3], "log_path": sys.argv[4], "started_at": sys.argv[5], "offline_only": True}, indent=2, sort_keys=True) + "\n", encoding="utf-8")' \
  "$EVIDENCE_DIR/launch.json" "$child_pid" "$EVIDENCE_DIR" "$RUN_LOG" "$STARTED_AT"

wait "$child_pid"
