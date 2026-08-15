# PLAN — HUMAN_GATE_REQUIRED: establish strip emission/path before F1 retry

## Retained attempt

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide7-h120-s100-f1-20260815/20260815-171419-ec-historical-shutter`
- Git checkpoint: `19c766770b5685655b971c9ea3fb52e50c99373b`.
- Result: wrapper child exit 1; Python and shell cleanup pass; Ray/strip zero
  reconfirmed; worktree clean.
- Completed: 1/16 accepted formal observations and 2 physical returns.
- Ray `Q_before` at requalified `1/5000` passed 58/58.
- The first strip base at `1/1600` returned a valid CR3/sidecar but rejected 19/58
  required features; no probe, Jacobian, solver candidate or confirmation ran.

## Gate

`HUMAN_GATE_REQUIRED`: controller command/readback showed the expected physical
payload (`cold_white=481`, `green=4095`, other channels zero), but the camera
response was about an order of magnitude below two previously accepted roots using
the same nominal shutter and exact command. Repository-local evidence cannot prove
whether the strip actually emitted normally or whether its power/optical path was
interrupted.

Human must inspect the local strip power/emission and chart illumination path and
confirm that the fixture is visibly illuminating the chart normally. Keep both
sources off while inspecting. After confirmation, perform a fresh F1 attempt; do
not pool or overwrite this failed root.
