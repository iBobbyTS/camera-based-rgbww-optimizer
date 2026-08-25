#!/bin/zsh
set -euo pipefail
PROJECT_ROOT="${0:A:h:h}"
OUTPUT_DIR="${1:?output directory required}"
RUN_NAME="${2:?run name required}"
cleanup() { cd "$PROJECT_ROOT"; .venv/bin/python -m camera_based_rgbww_optimizer.control.all_off > "$OUTPUT_DIR/$RUN_NAME/all-off-shell.json" 2>&1 || true; }
trap cleanup EXIT INT TERM
cd "$PROJECT_ROOT"
.venv/bin/python - "$OUTPUT_DIR" "$RUN_NAME" <<'PY'
import sys
from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
output_dir, run_name = sys.argv[1:]
plan=thermal.build_direct_plan(thermal.TD_C,variant=thermal.GUIDE9_WHITE_LOCAL_PROBES_VARIANT)
key=(1800,100); command={"cw":0,"ww":0,"r":4095,"g":1196,"b":0}
steps=[s for s in plan['captures'] if (int(s['target_cct']),int(s['target_gm']))==key]
ray=dict(next(s for s in steps if s['source_id']=='ray')); strip=dict(next(s for s in steps if s['role']=='strip_base'))
captures=[]
for i,(source,step) in enumerate((('ray',ray),('strip',strip))):
 step['capture_id']=f'{i:03d}-{source}-guide9-white-1800-gm100-final'; step['role']='ray_reference' if source=='ray' else 'strip_candidate'
 if source=='strip': step['command']=command; step['exact_command_hash']=thermal.canonical_sha256(command)
 captures.append(step)
contract=dict(next(x for x in plan['analysis_contract']['target_contracts'] if (x['cct'],x['gm'])==key)); contract['strip_command']=command
keys={s['exposure_cache_key'] for s in captures}
plan.update({'guide_experiment_id':thermal.GUIDE9_WHITE_LOCAL_CONFIRM2_EXPERIMENT_ID,'variant':thermal.GUIDE9_WHITE_LOCAL_CONFIRM2_VARIANT,'stage':'GUIDE9-WHITE12-1800-GM100-FINAL','captures':captures,'capture_ids':[s['capture_id'] for s in captures],'frozen_shutters':{k:v for k,v in plan['frozen_shutters'].items() if k in keys},'budgets':{'ray_cap':1,'strip_cap':1,'formal_cap':2,'physical_cr3_cap':2,'ambient_cap':0,'retry':0},'execution_authorization':{**plan['execution_authorization'],'schema':'direct_guide9_white_local_confirm2_v1','experiment_id':thermal.GUIDE9_WHITE_LOCAL_CONFIRM2_EXPERIMENT_ID,'human_authorization_experiment_id':None},'analysis_contract':{**plan['analysis_contract'],'method':'white12_1800_gm100_scaled_face_final','target_contracts':[contract],'global_model_refit':False,'pass_next':'GUIDE9_WHITE_FAST_DIRECT_FULL_70','failure_next':'GUIDE9_WHITE12_LOCAL_PROBE_REASSESSMENT'}})
plan['shutter_ledger_provenance']={'owner':'experiment_capture_steps','required_cache_keys':sorted(keys),'frozen_shutters_sha256':thermal.canonical_sha256(plan['frozen_shutters'])}
print(measure.run_authorized_plan(plan,output_dir=output_dir,run_name=run_name,camera_backend=camera_remote.create_camera_backend('remote')))
PY
