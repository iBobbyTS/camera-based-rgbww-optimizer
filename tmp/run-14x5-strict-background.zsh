#!/bin/zsh
set -eu

cd /Users/ibobby/Projects/WLED-RGBWW
: "${RUN_NAME:?RUN_NAME is required}"

cleanup() {
  .venv/bin/python -m camera_based_rgbww_optimizer.control.all_off >/dev/null 2>&1 || true
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'exit 129' HUP

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  -m camera_based_rgbww_optimizer.optimization.measure_white_lut \
  --output-dir /Volumes/4T/temp/rgbww-optimizer/white-lut-calibration \
  --run-name "${RUN_NAME}" \
  --target-ccts 1800,2000,2300,2700,3200,3800,4500,5000,5600,6500,8000,10000,14000,20000 \
  --target-gm-values 0,70,100,130,200 \
  --initial-lut /Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-strict-seed-20260712.json \
  --settle-seconds 2 \
  --allow-high-output
