#!/bin/zsh

set -eu

cd /Users/ibobby/Projects/WLED-RGBWW

cleanup() {
  .venv/bin/python -m camera_based_rgbww_optimizer.control.all_off \
    --ray-cct 20000 --ray-gm 200 --json || true
}

trap cleanup EXIT HUP INT TERM

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  tmp/recheck-white-top10-20260712.py "$@"
