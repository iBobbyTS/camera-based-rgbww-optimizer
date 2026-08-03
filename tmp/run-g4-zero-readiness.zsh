#!/bin/zsh
set -euo pipefail
umask 077

PROJECT_ROOT="${0:A:h:h}"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
OUTPUT_ROOT_INPUT="${1:?exact output root required}"
OUTPUT_ROOT="${OUTPUT_ROOT_INPUT:A}"
OUTPUT_PARENT="${OUTPUT_ROOT:h}"
OUTPUT_NAME="${OUTPUT_ROOT:t}"
SCRATCH_PREFIX="$OUTPUT_PARENT/.${OUTPUT_NAME}"
RUNNER_SCRATCH="$SCRATCH_PREFIX.runner-log.$$.scratch"
WRAPPER_SCRATCH="$SCRATCH_PREFIX.wrapper-log.$$.scratch"
SHELL_JSON_SCRATCH="$SCRATCH_PREFIX.all-off-json.$$.scratch"
SHELL_STDERR_SCRATCH="$SCRATCH_PREFIX.all-off-stderr.$$.scratch"

cd "$PROJECT_ROOT"
: >"$RUNNER_SCRATCH"
: >"$WRAPPER_SCRATCH"
: >"$SHELL_JSON_SCRATCH"
: >"$SHELL_STDERR_SCRATCH"

child_exit=""
received_signal=""
signal_number=0
finalized=0

note() {
  print -r -- "$1" >>"$WRAPPER_SCRATCH"
}

on_signal() {
  received_signal="$1"
  signal_number="$2"
  trap - INT TERM HUP
  exit $((128 + signal_number))
}

on_exit() {
  local incoming=$?
  if (( finalized )); then
    exit "$incoming"
  fi
  finalized=1
  trap - EXIT INT TERM HUP
  set +e
  if [[ -z "$child_exit" ]]; then
    child_exit="$incoming"
  fi

  note "child_exit=$child_exit"
  local shell_exit
  if "$PYTHON" -m camera_based_rgbww_optimizer.control.all_off \
    --json --ray-cct 5600 --ray-gm 100 --ray-timeout 3.0 \
    >"$SHELL_JSON_SCRATCH" 2>"$SHELL_STDERR_SCRATCH"; then
    shell_exit=0
  else
    shell_exit=$?
  fi
  note "shell_cleanup_exit=$shell_exit"

  local wrapper_status wrapper_exit
  if [[ -n "$received_signal" ]]; then
    wrapper_status="signaled"
    wrapper_exit=$((128 + signal_number))
  elif [[ "$child_exit" -ne 0 ]]; then
    wrapper_status="child_failed"
    wrapper_exit="$child_exit"
  elif [[ "$shell_exit" -ne 0 ]]; then
    wrapper_status="shell_cleanup_failed"
    wrapper_exit=70
  else
    wrapper_status="complete"
    wrapper_exit=0
  fi

  "$PYTHON" -m camera_based_rgbww_optimizer.optimization.p7_successor_zero_readiness \
    --finalize-only --allow-device-control --output-root "$OUTPUT_ROOT" \
    --runner-log-source "$RUNNER_SCRATCH" \
    --wrapper-log-source "$WRAPPER_SCRATCH" \
    --shell-json-source "$SHELL_JSON_SCRATCH" \
    --shell-stderr-source "$SHELL_STDERR_SCRATCH" \
    --child-exit-status "$child_exit" \
    --shell-exit-status "$shell_exit" \
    --wrapper-status "$wrapper_status" \
    --wrapper-exit-status "$wrapper_exit" \
    ${received_signal:+--signal-name "$received_signal"} \
    >>"$WRAPPER_SCRATCH" 2>&1
  local finalize_exit=$?

  rm -f -- "$RUNNER_SCRATCH" "$WRAPPER_SCRATCH" "$SHELL_JSON_SCRATCH" "$SHELL_STDERR_SCRATCH"
  exit "$finalize_exit"
}

trap on_exit EXIT
trap 'on_signal INT 2' INT
trap 'on_signal TERM 15' TERM
trap 'on_signal HUP 1' HUP

note "owner_start"
if "$PYTHON" -m camera_based_rgbww_optimizer.optimization.p7_successor_zero_readiness \
  --execute --allow-device-control --output-root "$OUTPUT_ROOT" \
  >"$RUNNER_SCRATCH" 2>&1; then
  child_exit=0
else
  child_exit=$?
fi
note "owner_complete"
exit "$child_exit"
