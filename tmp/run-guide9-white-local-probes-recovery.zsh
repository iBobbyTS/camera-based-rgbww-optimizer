#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="${0:A:h:h}"
OUTPUT_DIR="${1:?output directory required}"
RUN_NAME="${2:?run name required}"

cleanup() {
  cd "$PROJECT_ROOT"
  .venv/bin/python -m camera_based_rgbww_optimizer.control.all_off \
    > "$OUTPUT_DIR/$RUN_NAME/all-off-shell.json" 2>&1 || true
}
trap cleanup EXIT INT TERM

cd "$PROJECT_ROOT"
.venv/bin/python - "$OUTPUT_DIR" "$RUN_NAME" <<'PY'
import sys

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

output_dir, run_name = sys.argv[1:]
remaining = {(5600, 0), (20000, 0)}
plan = thermal.build_direct_plan(
    thermal.TD_C,
    variant=thermal.GUIDE9_WHITE_LOCAL_PROBES_VARIANT,
)
plan["captures"] = [
    step for step in plan["captures"]
    if (int(step["target_cct"]), int(step["target_gm"])) in remaining
]
plan["capture_ids"] = [step["capture_id"] for step in plan["captures"]]
plan["analysis_contract"]["target_contracts"] = [
    row for row in plan["analysis_contract"]["target_contracts"]
    if (int(row["cct"]), int(row["gm"])) in remaining
]
plan["budgets"] = {
    "ray_cap": 2,
    "strip_cap": 10,
    "formal_cap": 12,
    "physical_cr3_cap": 12,
    "ambient_cap": 0,
    "retry": 0,
}
required_cache_keys = {
    str(step["exposure_cache_key"]) for step in plan["captures"]
}
plan["frozen_shutters"] = {
    key: value for key, value in plan["frozen_shutters"].items()
    if key in required_cache_keys
}
plan["shutter_ledger_provenance"] = {
    "owner": "experiment_capture_steps",
    "required_cache_keys": sorted(required_cache_keys),
    "frozen_shutters_sha256": thermal.canonical_sha256(plan["frozen_shutters"]),
}
plan["recovery_contract"] = {
    "schema": "guide9_white_local_probes_remaining_suffix_v1",
    "immutable_prefix_root": (
        "/Volumes/4T/temp/rgbww-optimizer/guide9-white-local-probes-20260824/"
        "20260824-092424-no-model6"
    ),
    "immutable_prefix_accepted_count": 24,
    "remaining_targets": [[5600, 0], [20000, 0]],
    "rejected_dark_capture_allowed": False,
}

backend = camera_remote.create_camera_backend("remote")
root = measure.run_authorized_plan(
    plan,
    output_dir=output_dir,
    run_name=run_name,
    camera_backend=backend,
)
print(root)
PY
