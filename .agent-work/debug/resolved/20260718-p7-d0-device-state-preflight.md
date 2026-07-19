# P7-D0 generation-bearing device-state preflight

## Frozen scope

- The initial authorization covered exact `p7_strip_state_readback_preflight` only.
- Frozen raw PWM `(cw, ww, r, g, b) = (8, 16, 24, 32, 48)` with `curve_path=None`.
- No camera, CR3, `.env`, P7-R1, sentinel-v2, or high output.
- Initial run: `/Volumes/4T/temp/rgbww-optimizer/strip-state-readback-preflight/p7-strip-state-readback-preflight-20260718-223408`.

## Initial real result

- `startup_zero` failed with `RGBWW device-state entity is missing or duplicated`; primary branch was `D0-FIRMWARE-MISSING`.
- Python all-off succeeded, but `final_zero` failed for the same missing entity, so safety remained `D0-CLEANUP-UNKNOWN`.
- No verified transition passed and the low-output command was never attempted. No CR3 or NPY was created.
- Preflight, Python, shell, and independent recovery all-off evidence each reported ESPHome zero acknowledgement and Ray intensity 0; acknowledgement was correctly not promoted to independent readback.
- The outer launch printed a literal `WRAPPER_EXIT=0` instead of preserving `$?`; the failed run remains valid evidence, but this wrapper evidence gap was frozen for repair.

## Resolution

- The generation-bearing WebUI firmware was compiled, uploaded by authorized OTA, and accepted by Planner at checkpoint `ac36e77eff13c09da88ff54fd8b34cbb9673120a`.
- Post-upload independent zero readback found exact device identity, unique `rgbww_commanded_state`, generation `2 -> 3`, and five zero channels; the firmware prerequisite is resolved.
- The separate wrapper-exit investigation closes the evidence gap before any new five-step D0 run. The historical failed run is not rewritten as pass.
- P7-R1 remains locked until a fresh complete D0 passes and Planner accepts it.
