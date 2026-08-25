#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="${0:A:h:h}"
OUTPUT_DIR="${1:?output directory required}"
RUN_NAME="${2:?run name required}"
ANALYSIS="${3:?recovered local-probe analysis required}"

cleanup() {
  cd "$PROJECT_ROOT"
  .venv/bin/python -m camera_based_rgbww_optimizer.control.all_off \
    > "$OUTPUT_DIR/$RUN_NAME/all-off-shell.json" 2>&1 || true
}
trap cleanup EXIT INT TERM

cd "$PROJECT_ROOT"
.venv/bin/python - "$OUTPUT_DIR" "$RUN_NAME" "$ANALYSIS" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

output_dir, run_name, analysis_value = sys.argv[1:]
analysis_path = Path(analysis_value).resolve()
analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
if analysis.get("status") != "candidates_preregistered" or int(analysis.get("node_count", -1)) != 6:
    raise ValueError("local-probe candidate execution requires the accepted six-node analysis")
recovery = analysis.get("recovery_evidence") or {}
if recovery.get("rejected_dark_capture_included") is not False or recovery.get("diagnostic_captures_included") is not False:
    raise ValueError("local-probe analysis includes prohibited recovery observations")

candidates = {
    (int(node["cct"]), int(node["gm"])): {
        channel: int(node["candidate"]["command"][channel])
        for channel in thermal.CHANNELS
    }
    for node in analysis["nodes"]
}
plan = thermal.build_direct_plan(
    thermal.TD_C,
    variant=thermal.GUIDE9_WHITE_LOCAL_PROBES_VARIANT,
)
contracts = []
for row in plan["analysis_contract"]["target_contracts"]:
    item = dict(row)
    key = (int(item["cct"]), int(item["gm"]))
    item["strip_command"] = candidates[key]
    item["candidate_owner"] = "recovered_current_session_local_probe_jacobian"
    contracts.append(item)

captures = []
for contract in contracts:
    key = (int(contract["cct"]), int(contract["gm"]))
    source_steps = [
        step for step in plan["captures"]
        if (int(step["target_cct"]), int(step["target_gm"])) == key
    ]
    ray = dict(next(step for step in source_steps if step["source_id"] == "ray"))
    strip = dict(next(step for step in source_steps if step["role"] == "strip_base"))
    for source, step in (("ray", ray), ("strip", strip)):
        index = len(captures)
        step["capture_id"] = (
            f"{index:03d}-{source}-guide9-white-local-probe-candidate-"
            f"cct{key[0]}-gm{key[1]}"
        )
        step["role"] = "ray_reference" if source == "ray" else "strip_candidate"
        if source == "strip":
            step["command"] = dict(candidates[key])
            step["exact_command_hash"] = thermal.canonical_sha256(step["command"])
        captures.append(step)

plan.update({
    "guide_experiment_id": thermal.GUIDE9_WHITE_LOCAL_JAC_EXPERIMENT_ID,
    "variant": thermal.GUIDE9_WHITE_LOCAL_JAC_VARIANT,
    "stage": "GUIDE9-WHITE12-LOCAL-PROBE-CANDIDATES",
    "captures": captures,
    "capture_ids": [step["capture_id"] for step in captures],
    "budgets": {
        "ray_cap": 6, "strip_cap": 6, "formal_cap": 12,
        "physical_cr3_cap": 12, "ambient_cap": 0, "retry": 0,
    },
    "execution_authorization": {
        **plan["execution_authorization"],
        "schema": "direct_guide9_white_local_jacobian_v1",
        "experiment_id": thermal.GUIDE9_WHITE_LOCAL_JAC_EXPERIMENT_ID,
        "human_authorization_experiment_id": None,
    },
    "analysis_contract": {
        **plan["analysis_contract"],
        "method": "white12_recovered_local_probe_candidates",
        "target_contracts": contracts,
        "parent_analysis": {
            "path": str(analysis_path),
            "sha256": hashlib.sha256(analysis_path.read_bytes()).hexdigest(),
        },
        "pass_next": "GUIDE9_WHITE_FAST_DIRECT_FULL_70",
        "failure_next": "GUIDE9_WHITE12_LOCAL_PROBE_REASSESSMENT",
        "global_model_refit": False,
    },
})

backend = camera_remote.create_camera_backend("remote")
root = measure.run_authorized_plan(
    plan,
    output_dir=output_dir,
    run_name=run_name,
    camera_backend=backend,
)
print(root)
PY
