# P7-D0 generation-bearing device-state preflight

## Frozen scope

- Authorization consumed: exact `p7_strip_state_readback_preflight` only.
- Frozen raw PWM `(cw, ww, r, g, b) = (8, 16, 24, 32, 48)` with `curve_path=None`.
- No firmware compile/upload, camera, CR3, `.env`, P7-R1, sentinel-v2, or high output.
- Run: `/Volumes/4T/temp/rgbww-optimizer/strip-state-readback-preflight/p7-strip-state-readback-preflight-20260718-223408`.

## Offline implementation evidence

- `eb226bd` adds the thin `control.strip_state_readback_preflight` orchestrator while `control.esphome.verified_light` remains the only device-state parser and `control.all_off` remains the cleanup owner.
- Focused D0/ESPHome/all-off tests pass `17/17`; final full suite passes `432/432` in `143.567s`. Compileall, wrapper syntax, diff-check, and CodeGraph pass.
- Dry-run audit confirms five frozen steps, repeated low payload, raw PWM maximum 48, `curve_path=null`, and zero device/camera calls.
- Early test-only failures were an invalid multi-context `with` syntax and a fake background zsh child that inherited ignored SIGINT. The final signal test uses a Python fake with the production handlers and covers normal, exception, INT, TERM, and HUP cleanup exactly once.

## Real result

- `startup_zero` failed with `RGBWW device-state entity is missing or duplicated`; `primary_failure.branch=D0-FIRMWARE-MISSING`.
- Python all-off succeeded, but `final_zero` failed for the same missing entity, so the run correctly finished `cleanup_state_unknown` with `failure_branch=D0-CLEANUP-UNKNOWN`.
- No verified transition passed and the low-output command was never attempted. There are no CR3 or NPY files.
- Preflight, Python, shell, and independent recovery all-off evidence each report ESPHome zero acknowledgement and Ray intensity 0. Because acknowledgement is not independent readback, safety remains unknown.
- The outer launch command printed a literal `WRAPPER_EXIT=0` instead of preserving `$?`; runner log, run.json, and failure.json prove the child failure, but wrapper exit is unknown and must remain an explicit evidence gap.

## Blocker and recovery

The required firmware source is already frozen in commit `a380dfe` and current hash `deaf0a0717130b60805e3beddb9fa3b59e0f8695d8a22d4f2997859235082ab0`. It adds `rgbww_state_generation`, `rgbww_commanded_state`, and shared `apply_rgbww_12bit` publication. The installed target `bedroom-rgbww-strip` does not expose exactly one usable frozen entity; the retained error cannot distinguish zero from duplicate entities. Planner must decide whether to request separate compile/upload authorization and an OTA recovery plan; only after an authorized upload may D0 be rerun in a new directory. P7-R1 remains locked.
