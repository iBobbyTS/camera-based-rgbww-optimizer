#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="${0:A:h:h}"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
SESSION_WRAPPER="$PROJECT_ROOT/tmp/run-p7-thermal-diagnostics.zsh"
ROOT_INPUT="${1:?bridge root required}"
PREREQUISITE_INPUT="${2:?accepted strip analyzer-v3 required}"
ROOT="${ROOT_INPUT:A}"
PREREQUISITE="${PREREQUISITE_INPUT:A}"
EXPERIMENT_ID="GUIDE5-RAY-FAST-LONG-BRIDGE-OP120-OP600-RESET600-RESET1800-V1"

if [[ -e "$ROOT" ]]; then
  print -u2 -- "bridge root already exists: $ROOT"
  exit 64
fi
if [[ ! -f "$PREREQUISITE" || -L "$PREREQUISITE" ]]; then
  print -u2 -- "strip analyzer-v3 is not a regular file: $PREREQUISITE"
  exit 64
fi
if [[ -n "$(git -C "$PROJECT_ROOT" status --porcelain)" ]]; then
  print -u2 -- "bridge execution requires a clean Git checkpoint"
  exit 65
fi

mkdir -p "$ROOT"
chmod 0700 "$ROOT"
child_pid=""

atomic_text() {
  local target="$1"
  local value="$2"
  local temporary="${target:h}/.${target:t}.tmp.$$"
  print -r -- "$value" >"$temporary"
  mv -f "$temporary" "$target"
}

all_off() {
  "$PYTHON" -m camera_based_rgbww_optimizer.control.all_off --json \
    >"$ROOT/all-off-latest.json" 2>"$ROOT/all-off-latest.stderr.log" || true
}

cleanup_exit() {
  local incoming=$?
  trap - EXIT INT TERM HUP
  if [[ -n "$child_pid" ]]; then
    kill -TERM "$child_pid" 2>/dev/null || true
    wait "$child_pid" 2>/dev/null || true
  fi
  all_off
  atomic_text "$ROOT/bridge-exit.txt" "$incoming"
  exit "$incoming"
}

on_signal() {
  local name="$1"
  local code="$2"
  trap - EXIT INT TERM HUP
  if [[ -n "$child_pid" ]]; then
    kill -"$name" "$child_pid" 2>/dev/null || true
    wait "$child_pid" 2>/dev/null || true
  fi
  all_off
  atomic_text "$ROOT/bridge-exit.txt" "$code"
  exit "$code"
}

trap cleanup_exit EXIT
trap 'on_signal INT 130' INT
trap 'on_signal TERM 143' TERM
trap 'on_signal HUP 129' HUP

states=(C C B B)
protocols=(FAST LONG LONG FAST)
resets=(600 1800 1800 600)

for mini_session_index in 1 2 3 4; do
  state="${states[$mini_session_index]}"
  protocol="${protocols[$mini_session_index]}"
  reset_s="${resets[$mini_session_index]}"
  run_dir="$ROOT/mini-session-$mini_session_index"
  condition="Ray and strip continuously off for at least $reset_s s before the GUIDE5 $state $protocol mini-session; both-source zero readback passes at run start"

  atomic_text "$ROOT/bridge-current.txt" "reset:$mini_session_index:$state:$protocol:$reset_s"
  all_off
  date -u +%Y-%m-%dT%H:%M:%SZ >"$ROOT/mini-session-$mini_session_index-reset-started.txt"
  sleep "$reset_s"
  date -u +%Y-%m-%dT%H:%M:%SZ >"$ROOT/mini-session-$mini_session_index-reset-ended.txt"
  atomic_text "$ROOT/bridge-current.txt" "running:$mini_session_index:$state:$protocol"

  "$SESSION_WRAPPER" "$run_dir" \
    --experiment-id "$EXPERIMENT_ID" \
    --source ray --variant core --phase formal \
    --direct-ray-fast-long-bridge \
    --bridge-mini-session "$mini_session_index" \
    --session-start-condition "$condition" \
    --prerequisite-analysis "$PREREQUISITE" &
  child_pid="$!"
  wait "$child_pid"
  child_pid=""
done

atomic_text "$ROOT/bridge-current.txt" "complete:4:B:FAST"
trap - EXIT INT TERM HUP
all_off
atomic_text "$ROOT/bridge-exit.txt" "0"
