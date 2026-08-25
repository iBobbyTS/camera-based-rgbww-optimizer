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
import json
import sys
from pathlib import Path

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

output_dir, run_name = sys.argv[1:]
commands = {
    (1800, 0): {"cw": 105, "ww": 4090, "r": 4095, "g": 12, "b": 82},
    (3200, 0): {"cw": 24, "ww": 4095, "r": 157, "g": 10, "b": 836},
    (5600, 0): {"cw": 2892, "ww": 4095, "r": 14, "g": 91, "b": 1671},
    (20000, 0): {"cw": 4095, "ww": 1075, "r": 3, "g": 59, "b": 1963},
}
plan = thermal.build_direct_plan(thermal.TD_C, variant=thermal.GUIDE9_WHITE_LOCAL_PROBES_VARIANT)
contracts = []
for row in plan["analysis_contract"]["target_contracts"]:
    key = (int(row["cct"]), int(row["gm"]))
    if key in commands:
        item = dict(row)
        item["strip_command"] = commands[key]
        item["candidate_owner"] = "same_local_jacobian_plus_first_candidate_paired_residual"
        contracts.append(item)
captures = []
for contract in contracts:
    key = (int(contract["cct"]), int(contract["gm"]))
    source_steps = [step for step in plan["captures"] if (int(step["target_cct"]), int(step["target_gm"])) == key]
    ray = dict(next(step for step in source_steps if step["source_id"] == "ray"))
    strip = dict(next(step for step in source_steps if step["role"] == "strip_base"))
    for source, step in (("ray", ray), ("strip", strip)):
        index = len(captures)
        step["capture_id"] = f"{index:03d}-{source}-guide9-white-local-probe-confirm2-cct{key[0]}-gm{key[1]}"
        step["role"] = "ray_reference" if source == "ray" else "strip_candidate"
        if source == "strip":
            step["command"] = commands[key]
            step["exact_command_hash"] = thermal.canonical_sha256(step["command"])
        captures.append(step)
keys = {str(step["exposure_cache_key"]) for step in captures}
plan.update({
    "guide_experiment_id": thermal.GUIDE9_WHITE_LOCAL_CONFIRM2_EXPERIMENT_ID,
    "variant": thermal.GUIDE9_WHITE_LOCAL_CONFIRM2_VARIANT,
    "stage": "GUIDE9-WHITE12-LOCAL-PROBE-CONFIRM2",
    "captures": captures, "capture_ids": [step["capture_id"] for step in captures],
    "frozen_shutters": {key: value for key, value in plan["frozen_shutters"].items() if key in keys},
    "budgets": {"ray_cap": 4, "strip_cap": 4, "formal_cap": 8, "physical_cr3_cap": 8, "ambient_cap": 0, "retry": 0},
    "execution_authorization": {**plan["execution_authorization"], "schema": "direct_guide9_white_local_confirm2_v1", "experiment_id": thermal.GUIDE9_WHITE_LOCAL_CONFIRM2_EXPERIMENT_ID, "human_authorization_experiment_id": None},
    "analysis_contract": {**plan["analysis_contract"], "method": "white12_local_probe_second_confirmation", "target_contracts": contracts, "global_model_refit": False, "pass_next": "GUIDE9_WHITE_FAST_DIRECT_FULL_70", "failure_next": "GUIDE9_WHITE12_LOCAL_PROBE_REASSESSMENT"},
})
plan["shutter_ledger_provenance"] = {"owner": "experiment_capture_steps", "required_cache_keys": sorted(keys), "frozen_shutters_sha256": thermal.canonical_sha256(plan["frozen_shutters"])}
backend = camera_remote.create_camera_backend("remote")
print(measure.run_authorized_plan(plan, output_dir=output_dir, run_name=run_name, camera_backend=backend))
PY
