# P7-D0 generation-bearing device-state preflight

## Frozen scope

- Authorization: exact `p7_strip_state_readback_preflight` only.
- Output: raw PWM `(cw, ww, r, g, b) = (8, 16, 24, 32, 48)` with `curve_path=None`.
- No firmware upload, camera, CR3, `.env`, P7-R1, sentinel-v2, or high output.
- Every real path requires Python cleanup, final verified zero, and an independent shell-trap cleanup.

## Confirmed baseline

- `control.esphome.verified_light()` owns the generation-bearing snapshot protocol and disconnects on every exit.
- `control.all_off.turn_everything_off()` attempts ESPHome and Ray shutdown independently; Ray is commanded with intensity `0`.
- Planner accepted P7-R0K and split the active plan; the only current action is D0 implementation, offline validation, one bounded device run, and stop for Planner.

## Current hypothesis and next diagnostic

The device can pass D0 only if its installed firmware already exposes the frozen `rgbww_commanded_state` entity and increments generation for repeated identical commands. Implement a thin orchestration module without duplicating ESPHome parsing, prove all fail-closed and signal-cleanup paths offline, audit a dry-run plan, then execute the wrapper once. Any firmware/readback/cleanup mismatch is retained as the corresponding D0 stop branch.

## Offline implementation evidence

- The first focused run stopped before imports at an invalid multi-context `with` syntax in the new test; the syntax was corrected without touching product behavior.
- The next signal test exposed that a background fake zsh child inherits ignored `SIGINT`. Replacing it with a fake Python child that explicitly installs the same INT/TERM/HUP handlers as the production module made the test model the formal process correctly; no product cleanup contract was weakened.
- Focused D0/ESPHome/all-off tests now pass `17/17`, including exact raw payload, global generation, identity drift, missing/duplicate entity, stale/mismatched/timeout evidence, cleanup unknown, and normal/exception/INT/TERM/HUP shell cleanup.
- No device, Ray, camera, network, `.env`, or real all-off call has occurred during these checks.
