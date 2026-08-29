#!/bin/zsh
set -euo pipefail
PROJECT_ROOT="${0:A:h:h}"
OUTPUT_DIR="${1:?output directory required}"
RUN_NAME="${2:?run name required}"
TARGET_KEYS="${3:?comma-separated target keys required}"
cleanup() { cd "$PROJECT_ROOT"; .venv/bin/python -m camera_based_rgbww_optimizer.control.all_off > "$OUTPUT_DIR/$RUN_NAME/all-off-shell.json" 2>&1 || true; }
trap cleanup EXIT INT TERM
cd "$PROJECT_ROOT"
.venv/bin/python - "$OUTPUT_DIR" "$RUN_NAME" "$TARGET_KEYS" <<'PY'
import json, sys
from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
out_dir, run_name, keys_value = sys.argv[1:]
keys={tuple(map(int,k.split(':'))) for k in keys_value.split(',')}
plan=thermal.build_direct_plan(thermal.TD_C,variant=thermal.GUIDE9_WHITE_LOCAL_PROBES_VARIANT)
plan['captures']=[s for s in plan['captures'] if (int(s['target_cct']),int(s['target_gm'])) in keys]
plan['capture_ids']=[s['capture_id'] for s in plan['captures']]
plan['analysis_contract']['target_contracts']=[r for r in plan['analysis_contract']['target_contracts'] if (int(r['cct']),int(r['gm'])) in keys]
plan['budgets']={'ray_cap':len(keys),'strip_cap':len(keys)*5,'formal_cap':len(plan['captures']),'physical_cr3_cap':len(plan['captures']),'ambient_cap':0,'retry':0}
required={str(s['exposure_cache_key']) for s in plan['captures']}
plan['frozen_shutters']={k:v for k,v in plan['frozen_shutters'].items() if k in required}
plan['shutter_ledger_provenance']={'owner':'experiment_capture_steps','required_cache_keys':sorted(required),'frozen_shutters_sha256':thermal.canonical_sha256(plan['frozen_shutters'])}
plan['recovery_contract']={'schema':'guide9_white70_no_jacobian_probe_batch_v1','targets':sorted([list(k) for k in keys]),'candidate_capture_count':0,'global_model_refit':False}
print(measure.run_authorized_plan(plan,output_dir=out_dir,run_name=run_name,camera_backend=camera_remote.create_camera_backend('remote')))
PY
