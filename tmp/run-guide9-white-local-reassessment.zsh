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
plan = thermal.build_direct_plan(thermal.TD_C, variant=thermal.GUIDE9_WHITE_LOCAL_PROBES_VARIANT)
base = {"cw": 0, "ww": 0, "r": 3276, "g": 964, "b": 0}
probe_commands = {
    "strip_probe_cw": {**base, "cw": 256},
    "strip_probe_ww": {**base, "ww": 256},
    "strip_probe_g": {**base, "g": 1220},
    "strip_probe_b": {**base, "b": 256},
}
candidate_20000 = {"cw": 4095, "ww": 1078, "r": 5, "g": 59, "b": 1957}
captures = []
for key, roles in (
    ((1800, 100), [("ray_reference", None), ("strip_base", base), *probe_commands.items()]),
    ((20000, 0), [("ray_reference", None), ("strip_candidate", candidate_20000)]),
):
    source_steps = [step for step in plan["captures"] if (int(step["target_cct"]), int(step["target_gm"])) == key]
    ray_template = next(step for step in source_steps if step["source_id"] == "ray")
    strip_template = next(step for step in source_steps if step["role"] == "strip_base")
    for role, command in roles:
        source = "ray" if role == "ray_reference" else "strip"
        step = dict(ray_template if source == "ray" else strip_template)
        index = len(captures)
        step["capture_id"] = f"{index:03d}-{source}-guide9-white-local-reassessment-cct{key[0]}-gm{key[1]}-{role}"
        step["role"] = role
        if command is not None:
            step["command"] = dict(command)
            step["exact_command_hash"] = thermal.canonical_sha256(step["command"])
        captures.append(step)
keys = {str(step["exposure_cache_key"]) for step in captures}
plan.update({
    "guide_experiment_id": thermal.GUIDE9_WHITE_LOCAL_PROBES_EXPERIMENT_ID,
    "stage": "GUIDE9-WHITE12-LOCAL-REASSESSMENT",
    "captures": captures, "capture_ids": [step["capture_id"] for step in captures],
    "frozen_shutters": {key: value for key, value in plan["frozen_shutters"].items() if key in keys},
    "budgets": {"ray_cap": 2, "strip_cap": 6, "formal_cap": 8, "physical_cr3_cap": 8, "ambient_cap": 0, "retry": 0},
    "analysis_contract": {
        **plan["analysis_contract"],
        "method": "white12_local_reassessment",
        "scaled_1800_gm100_base": base,
        "scaled_1800_gm100_scale": 0.8,
        "scaled_1800_gm100_probes": probe_commands,
        "candidate_20000_gm0": candidate_20000,
        "global_model_refit": False,
    },
})
plan["shutter_ledger_provenance"] = {"owner": "experiment_capture_steps", "required_cache_keys": sorted(keys), "frozen_shutters_sha256": thermal.canonical_sha256(plan["frozen_shutters"])}
backend = camera_remote.create_camera_backend("remote")
print(measure.run_authorized_plan(plan, output_dir=output_dir, run_name=run_name, camera_backend=backend))
PY
