#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="${0:A:h:h}"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
RUN_DIR_INPUT="${1:?run directory required}"
RUN_DIR="${RUN_DIR_INPUT:A}"
shift
RUNNER_ARGS=("$@")
RUN_PARENT="${RUN_DIR:h}"
RUN_NAME="${RUN_DIR:t}"
RUNNER_LOG="$RUN_PARENT/${RUN_NAME}.runner.log"
WRAPPER_LOG="$RUN_PARENT/${RUN_NAME}.wrapper.log"
WRAPPER_STATE="$RUN_PARENT/${RUN_NAME}.wrapper-state.json"

cd "$PROJECT_ROOT"
mkdir -p "$RUN_DIR" "$RUN_PARENT"
exec > >(tee -a "$WRAPPER_LOG") 2>&1

child_pid=""
child_exit=""
cleanup_exit=""
independent_zero_exit=""
terminal_finalize_exit=""
received_signal=""
signal_number=0
cleaned=0
finalized=0
started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if ! terminal_mode="$("$PYTHON" -m camera_based_rgbww_optimizer.optimization.p7_td_b_r6_terminal classify-wrapper -- "${RUNNER_ARGS[@]}")"; then
  print -u2 -- "Ray R6 wrapper argument classification failed"
  exit 64
fi
if [[ "$terminal_mode" != "r6" && "$terminal_mode" != "legacy" ]]; then
  print -u2 -- "Ray R6 wrapper argument classification returned an invalid mode"
  exit 64
fi
if [[ "$terminal_mode" == "r6" ]]; then
  chmod 0700 "$RUN_DIR"
  umask 077
fi

atomic_text() {
  local target="$1"
  local value="$2"
  local temporary="${target:h}/.${target:t}.tmp.$$"
  print -r -- "$value" >"$temporary"
  mv -f "$temporary" "$target"
}

write_json() {
  local target="$1"
  local result_status="$2"
  local wrapper_exit="${3:-}"
  local temporary="${target:h}/.${target:t}.tmp.$$"
  "$PYTHON" -c '
import json, sys
from pathlib import Path
target,status,run_dir,wrapper_pid,child_pid,child_exit,cleanup_exit,wrapper_exit,signal_name,started=sys.argv[1:]
value={"schema_version":1,"experiment":"p7_thermal_diagnostics_v1","status":status,
"run_dir":run_dir,"wrapper_pid":int(wrapper_pid),"child_pid":None if not child_pid else int(child_pid),
"child_exit_code":None if not child_exit else int(child_exit),"shell_cleanup_exit_code":None if not cleanup_exit else int(cleanup_exit),
"wrapper_exit_code":None if not wrapper_exit else int(wrapper_exit),"signal":signal_name or None,"started_at":started}
Path(target).write_text(json.dumps(value,indent=2,sort_keys=True)+"\n")
' "$temporary" "$result_status" "$RUN_DIR" "$$" "$child_pid" "$child_exit" "$cleanup_exit" "$wrapper_exit" "$received_signal" "$started_at"
  mv -f "$temporary" "$target"
}

wait_child() {
  if [[ -z "$child_pid" || -n "$child_exit" ]]; then return; fi
  if wait "$child_pid"; then child_exit=0; else child_exit=$?; fi
  atomic_text "$RUN_DIR/child-exit-status.txt" "$child_exit"
}

cleanup_once() {
  if (( cleaned )); then return; fi
  cleaned=1
  local stdout_tmp="$RUN_DIR/.all-off-shell.json.tmp.$$"
  local stderr_tmp="$RUN_DIR/.all-off-shell.stderr.log.tmp.$$"
  if "$PYTHON" -m camera_based_rgbww_optimizer.control.all_off --json >"$stdout_tmp" 2>"$stderr_tmp"; then
    cleanup_exit=0
  else
    cleanup_exit=$?
  fi
  mv -f "$stdout_tmp" "$RUN_DIR/all-off-shell.json"
  mv -f "$stderr_tmp" "$RUN_DIR/all-off-shell.stderr.log"
  atomic_text "$RUN_DIR/all-off-shell.exit-status.txt" "$cleanup_exit"
}

finalize() {
  local incoming="$1"
  if (( finalized )); then return; fi
  finalized=1
  set +e
  wait_child
  if [[ -z "$child_exit" ]]; then atomic_text "$RUN_DIR/child-exit-status.txt" "not_started"; fi
  cleanup_once
  local final_exit final_status result_write_exit state_write_exit
  if [[ "$terminal_mode" == "r6" ]]; then
    if "$PYTHON" -m camera_based_rgbww_optimizer.optimization.p7_td_b_r6_terminal \
      independent-final-zero --run-dir "$RUN_DIR"; then
      independent_zero_exit=0
    else
      independent_zero_exit=$?
    fi
    if "$PYTHON" -m camera_based_rgbww_optimizer.optimization.p7_td_b_r6_terminal \
      finalize --run-dir "$RUN_DIR" --child-exit "${child_exit:-125}" \
      --shell-cleanup-exit "${cleanup_exit:-125}" \
      --independent-zero-exit "${independent_zero_exit:-125}" \
      --signal "$received_signal"; then
      terminal_finalize_exit=0
    else
      terminal_finalize_exit=$?
    fi
  fi
  if [[ -n "$received_signal" ]]; then
    final_exit=$((128 + signal_number)); final_status="signaled"
  elif [[ -n "$child_exit" && "$child_exit" -ne 0 ]]; then
    final_exit="$child_exit"; final_status="child_failed"
  elif [[ "$cleanup_exit" -ne 0 ]]; then
    final_exit=70; final_status="cleanup_failed"
  elif [[ "$terminal_mode" == "r6" && "$independent_zero_exit" -ne 0 ]]; then
    final_exit=71; final_status="independent_zero_failed"
  elif [[ "$terminal_mode" == "r6" && "$terminal_finalize_exit" -ne 0 ]]; then
    final_exit=72; final_status="terminal_finalize_failed"
  else
    final_exit="$incoming"; final_status="complete"
  fi
  write_json "$RUN_DIR/wrapper-result.json" "$final_status" "$final_exit"
  result_write_exit=$?
  write_json "$WRAPPER_STATE" "finished" "$final_exit"
  state_write_exit=$?
  if [[ "$terminal_mode" == "r6" && ( "$result_write_exit" -ne 0 || "$state_write_exit" -ne 0 ) ]]; then
    final_exit=73
    if [[ "$result_write_exit" -eq 0 ]]; then
      write_json "$RUN_DIR/wrapper-result.json" "terminal_write_failed" "$final_exit" || true
    fi
    if [[ "$state_write_exit" -eq 0 ]]; then
      write_json "$WRAPPER_STATE" "terminal_write_failed" "$final_exit" || true
    fi
  fi
  return "$final_exit"
}

on_exit() {
  local incoming=$?
  trap - EXIT INT TERM HUP
  finalize "$incoming"
  exit $?
}

on_signal() {
  received_signal="$1"; signal_number="$2"
  trap - INT TERM HUP
  if [[ -n "$child_pid" ]]; then kill -"$received_signal" "$child_pid" 2>/dev/null || true; fi
  wait_child
  exit $((128 + signal_number))
}

trap on_exit EXIT
trap 'on_signal INT 2' INT
trap 'on_signal TERM 15' TERM
trap 'on_signal HUP 1' HUP

"$PYTHON" -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  --execute --allow-device-control --output-dir "$RUN_PARENT" --run-name "$RUN_NAME" "${RUNNER_ARGS[@]}" \
  >"$RUNNER_LOG" 2>&1 &
child_pid="$!"
write_json "$WRAPPER_STATE" "running"
wait_child
exit "${child_exit:-1}"
