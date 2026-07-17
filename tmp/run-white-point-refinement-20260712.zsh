#!/bin/zsh

set -eu

cd /Users/ibobby/Projects/WLED-RGBWW

: "${CCT:?CCT is required}"
: "${GM:?GM is required}"
: "${RUN_NAME:?RUN_NAME is required}"
: "${INITIAL_LUT:?INITIAL_LUT is required}"

OUTPUT_ROOT="${OUTPUT_ROOT:-/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration}"

cleanup() {
  .venv/bin/python -m camera_based_rgbww_optimizer.control.all_off \
    --ray-cct "${CCT}" --ray-gm "${GM}" --json || true
}

trap cleanup EXIT HUP INT TERM

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  -m camera_based_rgbww_optimizer.optimization.measure_white_lut \
  --output-dir "${OUTPUT_ROOT}" \
  --run-name "${RUN_NAME}" \
  --target-ccts "${CCT}" \
  --target-gm-values "${GM}" \
  --initial-lut "${INITIAL_LUT}" \
  --feedback-cct-tolerance-k 12.5 \
  --feedback-cct-tolerance-mired 0.5 \
  --feedback-duv-tolerance 0.00025 \
  --feedback-rounds 16 \
  --settle-seconds 2 \
  --allow-high-output

RESULT="${OUTPUT_ROOT}/${RUN_NAME}/white-lut-calibration.json"
jq -e '.status == "complete" and (.targets | length) == 1 and .targets[0].status == "complete"' \
  "${RESULT}" >/dev/null
