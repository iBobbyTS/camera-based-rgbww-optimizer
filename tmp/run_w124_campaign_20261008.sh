#!/usr/bin/env bash
# GUIDE12 W12-4 campaign: eight point/protocol runs in the frozen execution
# order (LONG precedes FAST for 3200/20000, FAST precedes LONG for
# 1800/5600, points interleaved). Source order per run comes from the
# frozen W124_RAY_FIRST table (CLI default). Aborts on the first failed
# run so no partial campaign continues silently.
set -u
cd C:/Users/iBobb/Projects/WLED-RGBWW
mkdir -p D:/rgbww-optimizer/guide12-w124
seq=(
  "3200/100 long"
  "1800/100 fast"
  "20000/100 long"
  "5600/100 fast"
  "3200/100 fast"
  "1800/100 long"
  "20000/100 fast"
  "5600/100 long"
)
i=1
for spec in "${seq[@]}"; do
  point="${spec% *}"; protocol="${spec#* }"
  name=$(printf "formal-w124-%02d-p%s-%s" "$i" "${point//\//}" "$protocol")
  echo "=== $name start $(date '+%Y-%m-%d %H:%M:%S') ==="
  .venv/Scripts/python.exe -m camera_based_rgbww_optimizer.optimization.measure_guide12_w124 \
    --point "$point" --protocol "$protocol" \
    --output-dir D:/rgbww-optimizer/guide12-w124 --run-name "$name" \
    --execute --allow-device-control \
    > "D:/rgbww-optimizer/guide12-w124/${name}-launch.log" 2>&1
  rc=$?
  echo "=== $name exit=$rc $(date '+%Y-%m-%d %H:%M:%S') ==="
  if [ "$rc" -ne 0 ]; then
    echo "CAMPAIGN_ABORT rc=$rc at $name"
    exit "$rc"
  fi
  i=$((i+1))
done
echo "CAMPAIGN_COMPLETE $(date '+%Y-%m-%d %H:%M:%S')"
