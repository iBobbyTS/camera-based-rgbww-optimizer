#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="${0:A:h:h}"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
WRAPPER="$PROJECT_ROOT/tmp/run-hsi-reference-repeatability.zsh"
RUN_DIR_INPUT="${1:?fresh R1 run directory required}"
RUN_DIR="${RUN_DIR_INPUT:A}"
PREFLIGHT_DIR="${RUN_DIR}-preflight"

if [[ -e "$RUN_DIR" || -e "$PREFLIGHT_DIR" ]]; then
  print -u2 -- "run and preflight directories must both be fresh"
  exit 64
fi

mkdir -p "$PREFLIGHT_DIR"
cd "$PROJECT_ROOT"

started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
print -r -- "$$" >"$PREFLIGHT_DIR/launcher.pid"
print -r -- "$PPID" >"$PREFLIGHT_DIR/terminal-shell.pid"
print -r -- "$started_at" >"$PREFLIGHT_DIR/started-at.txt"
ps -o pid=,ppid=,pgid=,tty=,stat=,etime=,command= -p "$$" "$PPID" \
  >"$PREFLIGHT_DIR/process-ownership.txt"
git rev-parse HEAD >"$PREFLIGHT_DIR/git-head.txt"
git status --porcelain=v1 >"$PREFLIGHT_DIR/git-status.txt"
git diff --name-only e8c6af203c0292cebe8d6a9d004824cba7d7f0b7..HEAD -- \
  src tests config tmp/run-hsi-reference-repeatability.zsh \
  >"$PREFLIGHT_DIR/execution-tree-drift.txt"
df -h "$RUN_DIR:h" >"$PREFLIGHT_DIR/disk.txt"

preflight_complete=0
cleanup_preflight_failure() {
  local incoming_exit=$?
  if (( preflight_complete )); then
    return "$incoming_exit"
  fi
  set +e
  "$PYTHON" -m camera_based_rgbww_optimizer.control.all_off --json \
    >"$PREFLIGHT_DIR/all-off-preflight-failure.json" \
    2>"$PREFLIGHT_DIR/all-off-preflight-failure.stderr.log"
  print -r -- "$?" >"$PREFLIGHT_DIR/all-off-preflight-failure.exit-status.txt"
  print -r -- "$incoming_exit" >"$PREFLIGHT_DIR/preflight.exit-status.txt"
  return "$incoming_exit"
}

trap cleanup_preflight_failure EXIT INT TERM HUP

"$PYTHON" -m camera_based_rgbww_optimizer.control.all_off --json \
  >"$PREFLIGHT_DIR/all-off-before.json" 2>"$PREFLIGHT_DIR/all-off-before.stderr.log"
"$PYTHON" -m camera_based_rgbww_optimizer.control.camera_remote health --json \
  >"$PREFLIGHT_DIR/camera-health.json" 2>"$PREFLIGHT_DIR/camera-health.stderr.log"
"$PYTHON" -m camera_based_rgbww_optimizer.control.camera_remote config --json \
  >"$PREFLIGHT_DIR/camera-config.json" 2>"$PREFLIGHT_DIR/camera-config.stderr.log"
"$PYTHON" -m camera_based_rgbww_optimizer.control.ray120c node-config \
  >"$PREFLIGHT_DIR/ray-node-config.json" 2>"$PREFLIGHT_DIR/ray-node-config.stderr.log"
"$PYTHON" -m camera_based_rgbww_optimizer.control.ray120c get-hsi \
  >"$PREFLIGHT_DIR/ray-get-hsi.json" 2>"$PREFLIGHT_DIR/ray-get-hsi.stderr.log"
"$PYTHON" -m camera_based_rgbww_optimizer.control.ray120c get-cct \
  >"$PREFLIGHT_DIR/ray-off-readback.json" 2>"$PREFLIGHT_DIR/ray-off-readback.stderr.log"
"$PYTHON" -m camera_based_rgbww_optimizer.control.all_off --json \
  >"$PREFLIGHT_DIR/all-off-after.json" 2>"$PREFLIGHT_DIR/all-off-after.stderr.log"

preflight_complete=1
trap - EXIT INT TERM HUP
print -r -- "0" >"$PREFLIGHT_DIR/preflight.exit-status.txt"
print -r -- "pass" >"$PREFLIGHT_DIR/preflight.status"
exec /bin/zsh "$WRAPPER" "$RUN_DIR"
