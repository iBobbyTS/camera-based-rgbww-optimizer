# Location Picker dcraw Preview And Bounds Debug

## Symptom

- User saw the Location Picker Web UI at `127.0.0.1:8767` display automatic 4x6 labels/quads outside the image bounds.
- User also expected the Web UI preview to be decoded through `dcraw_emu`, matching the location checker behavior.

## Confirmed Cause

- `location_checker` had a `dcraw_emu` visual preview path.
- `location_picker_ui` still used `camera_gphoto2.auto_expose_capture(... decode_formats=("npy",))` and `load_preview_from_npy(...)` for the visible preview and automatic detection.
- The automatic detector accepted returned quads without validating every point against the decoded preview bounds.
- The currently running UI process was `PID 72858` listening on `127.0.0.1:8767`; it must be restarted to load changed code.

## Fix

- Added shared `interaction.raw_visual_preview` for `dcraw_emu` TIFF visual preview decoding.
- Updated `location_picker_ui` to keep linear NPY decode for auto-exposure metering, then decode the accepted final RAW through `dcraw_emu` for the Web UI preview and automatic detection.
- Follow-up evidence showed `dcraw_emu` full RAW reconstruction for Canon R6 Mark III CR3 was visibly magenta on the picker image, while the CR3 `JpgFromRaw` embedded preview matched Finder/camera rendering.
- Picker/checker now default to the camera-rendered `JpgFromRaw` preview extracted by `exiftool`; `dcraw_emu` remains available through `--preview-source dcraw`.
- Validated automatic detector results from MCC, OpenCV, and projection paths; out-of-bounds results are rejected instead of displayed.
- Updated checker to reuse the shared visual preview decoder.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer/interaction tests/test_location_picker_ui.py tests/test_location_checker.py`
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.test_location_picker_ui.LocationArgsTests tests.test_location_picker_ui.LocationPreviewTests tests.test_location_picker_ui.LocationWebApiTests tests.test_location_checker -v`
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`
