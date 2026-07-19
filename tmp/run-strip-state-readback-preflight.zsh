#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="${0:A:h:h}"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
RUN_DIR="${1:?run directory required}"
RUN_PARENT="${RUN_DIR:h}"
RUN_NAME="${RUN_DIR:t}"
RUNNER_LOG="$RUN_PARENT/${RUN_NAME}.runner.log"
WRAPPER_LOG="$RUN_PARENT/${RUN_NAME}.wrapper.log"
WRAPPER_STATE="$RUN_PARENT/${RUN_NAME}.wrapper-state"

cd "$PROJECT_ROOT"
mkdir -p "$RUN_DIR"
mkdir -p "$RUN_PARENT"
exec > >(tee -a "$WRAPPER_LOG") 2>&1

child_pid=""
cleaned=0
started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

cleanup() {
  if (( cleaned )); then
    return
  fi
  cleaned=1
  local cleanup_tmp="$RUN_DIR/.all-off-shell.json.tmp.$$"
  "$PYTHON" -m camera_based_rgbww_optimizer.control.all_off --json \
    >"$cleanup_tmp" 2>&1 || true
  mv -f "$cleanup_tmp" "$RUN_DIR/all-off-shell.json"
}

on_signal() {
  local signal_name="$1"
  local signal_number="$2"
  trap - "$signal_name"
  if [[ -n "$child_pid" ]]; then
    kill -"$signal_name" "$child_pid" 2>/dev/null || true
    wait "$child_pid" 2>/dev/null || true
  fi
  cleanup
  exit $((128 + signal_number))
}

trap cleanup EXIT
trap 'on_signal INT 2' INT
trap 'on_signal TERM 15' TERM
trap 'on_signal HUP 1' HUP

"$PYTHON" -m camera_based_rgbww_optimizer.control.strip_state_readback_preflight \
  --execute \
  --allow-device-control \
  --named-experiment p7_strip_state_readback_preflight \
  --output-dir "$RUN_PARENT" \
  --run-name "$RUN_NAME" \
  >"$RUNNER_LOG" 2>&1 &
child_pid="$!"

state_tmp="$WRAPPER_STATE.tmp.$$"
{
  print -r -- "child_pid=$child_pid"
  print -r -- "run_dir=$RUN_DIR"
  print -r -- "runner_log=$RUNNER_LOG"
  print -r -- "wrapper_log=$WRAPPER_LOG"
  print -r -- "started_at=$started_at"
} >"$state_tmp"
mv -f "$state_tmp" "$WRAPPER_STATE"

wait "$child_pid"
