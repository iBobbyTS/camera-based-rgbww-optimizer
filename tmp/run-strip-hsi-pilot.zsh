#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="${0:A:h:h}"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
RUN_DIR="${1:?run directory required}"
shift
RUN_PARENT="${RUN_DIR:h}"
RUN_NAME="${RUN_DIR:t}"
RUN_LOG="$RUN_PARENT/${RUN_NAME}.runner.log"

cd "$PROJECT_ROOT"
mkdir -p "$RUN_DIR"

child_pid=""
cleaned=0

cleanup() {
  if (( cleaned )); then
    return
  fi
  cleaned=1
  "$PYTHON" -m camera_based_rgbww_optimizer.control.all_off --json \
    >"$RUN_DIR/all-off-shell.json" 2>&1 || true
}

on_signal() {
  local signal="$1"
  trap - "$signal"
  if [[ -n "$child_pid" ]]; then
    kill -"$signal" "$child_pid" 2>/dev/null || true
    wait "$child_pid" 2>/dev/null || true
  fi
  cleanup
  exit 128
}

trap cleanup EXIT
trap 'on_signal INT' INT
trap 'on_signal TERM' TERM
trap 'on_signal HUP' HUP

"$PYTHON" -m camera_based_rgbww_optimizer.optimization.measure_strip_hsi_pilot \
  --execute \
  --allow-high-output \
  --camera-backend remote \
  --location-config "$PROJECT_ROOT/config/location/locations-20260714-211759.json" \
  --output-dir "$RUN_PARENT" \
  --run-name "$RUN_NAME" \
  "$@" \
  >"$RUN_LOG" 2>&1 &
child_pid="$!"
wait "$child_pid"
