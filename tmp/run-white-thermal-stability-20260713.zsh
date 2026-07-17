#!/bin/zsh

set -eu

cd /Users/ibobby/Projects/WLED-RGBWW

cleanup() {
  .venv/bin/python -m camera_based_rgbww_optimizer.control.all_off \
    --ray-cct 14000 --ray-gm 130 --json || true
}

trap cleanup EXIT HUP INT TERM

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  tmp/measure-white-thermal-stability-20260713.py
