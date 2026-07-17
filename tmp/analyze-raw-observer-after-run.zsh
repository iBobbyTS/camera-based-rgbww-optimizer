#!/bin/zsh
set -euo pipefail

RUNNER_PID="${1:?runner pid required}"
RUN_DIR="${2:?run directory required}"
PROJECT_ROOT="${0:A:h:h}"
PYTHON="$PROJECT_ROOT/.venv/bin/python"

while kill -0 "$RUNNER_PID" 2>/dev/null; do
  sleep 10
done

"$PYTHON" -m camera_based_rgbww_optimizer.optimization.analyze_raw_observer_validation \
  "$RUN_DIR" \
  >"$RUN_DIR/analysis-runner.log" 2>&1
