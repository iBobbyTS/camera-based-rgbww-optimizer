#!/bin/zsh
set -euo pipefail
PROJECT_ROOT="${0:A:h:h}"
OUTPUT_DIR="${1:?output directory required}"
RUN_NAME="${2:?run name required}"
cleanup() {
  [[ "${GUIDE9_VALIDATE_ONLY:-0}" == "1" ]] && return 0
  cd "$PROJECT_ROOT"
  .venv/bin/python -m camera_based_rgbww_optimizer.control.all_off > "$OUTPUT_DIR/$RUN_NAME/all-off-shell.json" 2>&1 || true
}
trap cleanup EXIT INT TERM
cd "$PROJECT_ROOT"
.venv/bin/python - "$OUTPUT_DIR" "$RUN_NAME" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

output_dir, run_name = sys.argv[1:]
resume_from = int(os.environ.get("GUIDE9_RESUME_FROM_CAPTURE", "0"))
payload=json.loads(thermal.GUIDE9_WHITE_70_CANDIDATE_PATH.read_text())
corrections={
 (1800,0):{"cw":105,"ww":4090,"r":4095,"g":12,"b":82},
 (1800,100):{"cw":0,"ww":0,"r":4095,"g":1196,"b":0},
 (1800,200):{"cw":1,"ww":788,"r":4095,"g":900,"b":1},
 (3200,0):{"cw":24,"ww":4095,"r":157,"g":10,"b":836},
 (3200,100):{"cw":2271,"ww":506,"r":4095,"g":1939,"b":56},
 (3200,200):{"cw":756,"ww":440,"r":4095,"g":2431,"b":32},
 (5600,0):{"cw":2892,"ww":4095,"r":14,"g":91,"b":1671},
 (5600,100):{"cw":4095,"ww":428,"r":142,"g":17,"b":116},
 (20000,0):{"cw":4095,"ww":1078,"r":5,"g":59,"b":1957},
 (20000,100):{"cw":0,"ww":196,"r":3201,"g":4095,"b":3529},
 (20000,200):{"cw":4095,"ww":114,"r":400,"g":3792,"b":3067},
}
captures=[]; contracts=[]; shutters={}
for index,row in enumerate(payload['targets']):
 cct,gm=int(row['cct']),int(row['gm']); key=(cct,gm)
 command=corrections.get(key,{ch:int(row['selected_command'][ch]) for ch in thermal.CHANNELS})
 ray_shutter=str(row['ray']['auto_exposure']['final']['shutter_speed'])
 strip_shutter=str(row['feedback_optimizer']['best']['capture']['shutter_speed'])
 cache=f'white-{cct}-gm{gm}'; shutters[f'ray-{cache}']=ray_shutter; shutters[f'strip-{cache}']=strip_shutter
 order=('ray','strip') if index%2==0 else ('strip','ray')
 contracts.append({'target_index':index,'cct':cct,'gm':gm,'source_order':list(order),'strip_command':command,'resolved_cct_tolerance_K':float(row['feedback_goal']['resolved_cct_tolerance_K']),'cct_tolerance_mired':float(row['feedback_goal']['cct_tolerance_mired']),'duv_tolerance':float(row['feedback_goal']['duv_tolerance']),'command_owner':'accepted_local_correction' if key in corrections else 'retained_70_node_candidate'})
 for source_order,source in enumerate(order,1):
  cmd={'mode':'cct','cct':cct,'gm':gm,'intensity_percent':100.0} if source=='ray' else dict(command)
  capture_index=len(captures)
  captures.append({'capture_id':f'{capture_index:03d}-{source}-guide9-white70-cct{cct}-gm{gm}','source_id':source,'state_id':f'CCT{cct}_GM{gm}','role':f'{source}_cct{cct}_gm{gm}','capture_role':'formal','formal_measurement':True,'command':cmd,'exact_command_hash':thermal.canonical_sha256(cmd),'requested_elapsed_s':120,'nominal_shutter':ray_shutter if source=='ray' else strip_shutter,'exposure_cache_key':f'{source}-{cache}','timing_acceptance':'observed_elapsed_record_only','strip_zero_required':source=='ray','ray_zero_required':source=='strip','session_index':index+1,'source_order':source_order,'target_cct':cct,'target_gm':gm,'steady_claim':False})
camera=thermal.build_direct_plan(thermal.TD_C,variant=thermal.GUIDE9_WHITE12_VARIANT)['camera']
plan={'schema':thermal.PLAN_SCHEMA_V2,'status':'execute_authorized','experiment_id':thermal.TD_C,'guide_experiment_id':'GUIDE9_WHITE_FAST_DIRECT_FULL_70_V1','variant':thermal.GUIDE9_WHITE12_VARIANT,'stage':'GUIDE9-WHITE-FAST-DIRECT-70','phase':'formal','source':'white_full70_validation','created_at':datetime.now(timezone.utc).isoformat(),'inputs':{'location':thermal.file_reference(thermal.LOCATION_PATH),'policy':thermal.file_reference(thermal.POLICY_PATH),'uncertainty':thermal.file_reference(thermal.UNCERTAINTY_PATH),'code_duty_curve':thermal.file_reference(thermal.CURVE_PATH),'white_70_candidate':thermal.file_reference(thermal.GUIDE9_WHITE_70_CANDIDATE_PATH)},'camera':camera,'captures':captures,'capture_ids':[x['capture_id'] for x in captures],'timing_contract':thermal.timing_contract(2),'cold_proxy':600,'cold_proxy_wait_s':600,'native_raw_ambient_policy':thermal.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,'frozen_shutters':shutters,'exposure_setup_required':[],'shutter_ledger_provenance':{'owner':'experiment_capture_steps','required_cache_keys':sorted(shutters),'frozen_shutters_sha256':thermal.canonical_sha256(shutters)},'budgets':{'ray_cap':70,'strip_cap':70,'formal_cap':140,'physical_cr3_cap':140,'ambient_cap':0,'retry':0},'execution_authorization':{'schema':'direct_guide9_white12_v1','human_authorization_required':False,'human_authorization_verified':True,'human_authorization_experiment_id':'GUIDE9_WHITE_FAST_DIRECT_FULL_70_V1','bounded_device_scope':True,'experiment_id':'GUIDE9_WHITE_FAST_DIRECT_FULL_70_V1','remote_v2_capability':True},'analysis_contract':{'method':'white_fast_direct_full_70','target_contracts':contracts,'independent_reset_s':600,'dwell_s':120,'source_order_balanced':True,'local_correction_only_for_failed_nodes':True,'global_model_refit':False,'default_lut_installation':False,'steady_claim':False,'pass_next':'GUIDE9_WHITE_INTERPOLATION_HOLDOUT_20','failure_next':'GUIDE9_WHITE70_LOCAL_NODE_CORRECTION'}}
if resume_from:
    plan["captures"] = [step for step in plan["captures"] if int(step["capture_id"].split("-", 1)[0]) >= resume_from]
    plan["capture_ids"] = [step["capture_id"] for step in plan["captures"]]
    plan["budgets"] = {
        "ray_cap": sum(step["source_id"] == "ray" for step in plan["captures"]),
        "strip_cap": sum(step["source_id"] == "strip" for step in plan["captures"]),
        "formal_cap": len(plan["captures"]), "physical_cr3_cap": len(plan["captures"]),
        "ambient_cap": 0, "retry": 0,
    }
    plan["analysis_contract"]["resume_from_capture"] = resume_from
if os.environ.get('GUIDE9_VALIDATE_ONLY') == '1':
    measure.validate_authorized_execution_plan(plan)
    print(json.dumps({'captures':len(captures),'targets':len(contracts),'corrected_nodes':len(corrections)}))
    raise SystemExit(0)
print(measure.run_authorized_plan(plan,output_dir=output_dir,run_name=run_name,camera_backend=camera_remote.create_camera_backend('remote')))
PY
