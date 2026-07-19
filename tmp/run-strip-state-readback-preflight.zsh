#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="${0:A:h:h}"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
RUN_DIR_INPUT="${1:?run directory required}"
RUN_DIR="${RUN_DIR_INPUT:A}"
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
child_exit_code=""
shell_cleanup_exit_code=""
received_signal=""
signal_number=0
cleaned=0
finalized=0
started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

atomic_text() {
  local target_path="$1"
  local value="$2"
  local tmp="${target_path:h}/.${target_path:t}.tmp.$$"
  print -r -- "$value" >"$tmp"
  mv -f "$tmp" "$target_path"
}

record_child_exit() {
  if [[ -z "$child_pid" ]]; then
    atomic_text "$RUN_DIR/child-exit-status.txt" "not_started"
  else
    atomic_text "$RUN_DIR/child-exit-status.txt" "$child_exit_code"
  fi
}

wait_for_child() {
  if [[ -z "$child_pid" || -n "$child_exit_code" ]]; then
    return
  fi
  if wait "$child_pid"; then
    child_exit_code=0
  else
    child_exit_code=$?
  fi
  record_child_exit
}

cleanup_once() {
  if (( cleaned )); then
    return
  fi
  cleaned=1

  local stdout_path="$RUN_DIR/all-off-shell.json"
  local stderr_path="$RUN_DIR/all-off-shell.stderr.log"
  local stdout_tmp="$RUN_DIR/.all-off-shell.json.tmp.$$"
  local stderr_tmp="$RUN_DIR/.all-off-shell.stderr.log.tmp.$$"

  if "$PYTHON" -m camera_based_rgbww_optimizer.control.all_off --json \
    >"$stdout_tmp" 2>"$stderr_tmp"; then
    shell_cleanup_exit_code=0
  else
    shell_cleanup_exit_code=$?
  fi
  mv -f "$stdout_tmp" "$stdout_path"
  mv -f "$stderr_tmp" "$stderr_path"
  atomic_text "$RUN_DIR/all-off-shell.exit-status.txt" "$shell_cleanup_exit_code"
}

write_wrapper_result() {
  local wrapper_exit_code="$1"
  local result_status="$2"
  local finished_at="$3"
  local result_path="$RUN_DIR/wrapper-result.json"
  local result_tmp="$RUN_DIR/.wrapper-result.json.tmp.$$"

  "$PYTHON" -c '
import json
import sys
from pathlib import Path

(
    output,
    status,
    child_pid,
    child_exit,
    cleanup_exit,
    wrapper_exit,
    signal_name,
    started_at,
    finished_at,
    run_dir,
    runner_log,
    wrapper_log,
    shell_cleanup,
) = sys.argv[1:]
payload = {
    "schema_version": 1,
    "experiment": "p7_strip_state_readback_preflight",
    "status": status,
    "child_pid": None if child_pid == "" else int(child_pid),
    "child_exit_code": None if child_exit == "" else int(child_exit),
    "shell_cleanup_exit_code": int(cleanup_exit),
    "wrapper_exit_code": int(wrapper_exit),
    "signal": None if signal_name == "" else signal_name,
    "started_at": started_at,
    "finished_at": finished_at,
    "artifacts": {
        "run_dir": run_dir,
        "runner_log": runner_log,
        "wrapper_log": wrapper_log,
        "shell_cleanup": shell_cleanup,
    },
}
Path(output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
' "$result_tmp" "$result_status" "$child_pid" "$child_exit_code" \
    "$shell_cleanup_exit_code" "$wrapper_exit_code" "$received_signal" \
    "$started_at" "$finished_at" "$RUN_DIR" "$RUNNER_LOG" "$WRAPPER_LOG" \
    "$RUN_DIR/all-off-shell.json"
  mv -f "$result_tmp" "$result_path"
}

finalize() {
  local incoming_exit_code="$1"
  if (( finalized )); then
    return
  fi
  finalized=1
  set +e

  wait_for_child
  record_child_exit
  cleanup_once

  local wrapper_exit_code
  local result_status
  if [[ -n "$received_signal" ]]; then
    wrapper_exit_code=$((128 + signal_number))
    result_status="signaled"
  elif [[ -n "$child_exit_code" && "$child_exit_code" -ne 0 ]]; then
    wrapper_exit_code="$child_exit_code"
    result_status="child_failed"
  elif [[ "$shell_cleanup_exit_code" -ne 0 ]]; then
    wrapper_exit_code=70
    result_status="cleanup_failed"
  else
    wrapper_exit_code="$incoming_exit_code"
    result_status="complete"
  fi

  local finished_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  write_wrapper_result "$wrapper_exit_code" "$result_status" "$finished_at"
  return "$wrapper_exit_code"
}

on_exit() {
  local incoming_exit_code=$?
  trap - EXIT INT TERM HUP
  finalize "$incoming_exit_code"
  local wrapper_exit_code=$?
  exit "$wrapper_exit_code"
}

on_signal() {
  received_signal="$1"
  signal_number="$2"
  trap - INT TERM HUP
  if [[ -n "$child_pid" ]]; then
    kill -"$received_signal" "$child_pid" 2>/dev/null || true
  fi
  wait_for_child
  exit $((128 + signal_number))
}

trap on_exit EXIT
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

wait_for_child
exit "${child_exit_code:-1}"
