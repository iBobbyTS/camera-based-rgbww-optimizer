#!/bin/zsh
set -euo pipefail

RUN_DIR="${1:?run directory required}"
CONFIG="firmware/esphome/bedroom-rgbww-strip-webui.yaml"
DEVICE="bedroom-rgbww-strip.local"

mkdir -p "$RUN_DIR"

cleanup() {
  set +e
  .venv/bin/python -m camera_based_rgbww_optimizer.control.all_off --json \
    >"$RUN_DIR/all-off-shell.json" 2>"$RUN_DIR/all-off-shell.stderr.log"
  print -r -- "$?" >"$RUN_DIR/all-off-shell.exit-status.txt"
}

trap cleanup EXIT
trap 'exit 130' INT TERM HUP

date -u +%Y-%m-%dT%H:%M:%SZ >"$RUN_DIR/started_at_utc.txt"
print -r -- "$$" >"$RUN_DIR/wrapper.pid"
print -r -- ".venv/bin/python -m esphome upload $CONFIG --device $DEVICE" \
  >"$RUN_DIR/command.txt"

.venv/bin/python -m camera_based_rgbww_optimizer.control.all_off --json \
  >"$RUN_DIR/all-off-before.json" 2>"$RUN_DIR/all-off-before.stderr.log"

.venv/bin/python -m esphome upload "$CONFIG" --device "$DEVICE" \
  2>&1 | tee "$RUN_DIR/upload.log"
upload_rc=${pipestatus[1]}
print -r -- "$upload_rc" >"$RUN_DIR/upload.exit-status.txt"
if (( upload_rc != 0 )); then
  exit "$upload_rc"
fi

sleep 10
.venv/bin/python -m camera_based_rgbww_optimizer.control.all_off --json \
  >"$RUN_DIR/all-off-after.json" 2>"$RUN_DIR/all-off-after.stderr.log"

.venv/bin/python -c \
  'import json; from camera_based_rgbww_optimizer.control.esphome import verified_light; print(json.dumps(verified_light(0, 0, 0, 0, 0, curve_path=None, state_timeout=10.0), sort_keys=True))' \
  >"$RUN_DIR/verified-zero.json" 2>"$RUN_DIR/verified-zero.stderr.log"

date -u +%Y-%m-%dT%H:%M:%SZ >"$RUN_DIR/finished_at_utc.txt"
