#!/bin/zsh
# MIGRATION FREEZE (2026-09-01): retained for macOS provenance and replay only.
# Do not update this launcher while Windows/pwsh owns the active recovery route.
set -euo pipefail
cd "${0:A:h:h}"
exec ./tmp/run-guide9-white70-no-jac-probes.zsh \
  /Volumes/4T/temp/rgbww-optimizer/guide9-white70-no-jac-probes-20260829 \
  "${GUIDE9_PROBE_RUN_NAME:-20260829-19-node-probes-rerun4}" \
  2000:0,2000:70,2000:130,2000:200,2300:0,2700:200,3800:0,3800:70,3800:130,4500:100,4500:130,5000:70,5000:100,6500:130,6500:200,8000:0,8000:70,10000:70,20000:130
