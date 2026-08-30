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
import json, re, sys
from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
out_dir, run_name, keys_value = sys.argv[1:]
keys={tuple(map(int,m)) for m in re.findall(r'(\d+):(\d+)', keys_value)}
if len(keys) != 19:
    raise ValueError(f"expected 19 target keys, got {sorted(keys)}")
plan=thermal.build_direct_plan(thermal.TD_C,variant=thermal.GUIDE9_WHITE12_VARIANT)
baseline=json.loads(thermal.GUIDE9_WHITE_70_CANDIDATE_PATH.read_text())
baseline_by_key={(int(r['cct']),int(r['gm'])):r for r in baseline['targets']}
source_captures=[]
for key in sorted(keys):
    row=baseline_by_key[key]; base={ch:int(row['selected_command'][ch]) for ch in thermal.CHANNELS}
    active=str(row['feedback_optimizer']['active_channel']); probes=[]
    for ch in thermal.CHANNELS:
        if ch==active: continue
        delta=256 if base[ch] <= 4095-256 else -256
        cmd=dict(base); cmd[ch]+=delta; probes.append((ch,cmd))
    cct,gm=key; ray_source={'mode':'cct','cct':cct,'gm':gm,'intensity_percent':100.0}
    for role,source,cmd in [('ray_reference','ray',ray_source),('strip_base','strip',base),*[(f'strip_probe_{ch}','strip',cmd) for ch,cmd in probes]]:
        source_captures.append({'capture_id':f'{len(source_captures):03d}-{source}-guide9-white70-probe-cct{cct}-gm{gm}-{role}','source_id':source,'state_id':f'CCT{cct}_GM{gm}','role':role,'capture_role':'formal','formal_measurement':True,'command':cmd,'exact_command_hash':thermal.canonical_sha256(cmd),'requested_elapsed_s':120,'nominal_shutter':str(row['ray']['auto_exposure']['final']['shutter_speed'] if source=='ray' else row['feedback_optimizer']['best']['capture']['shutter_speed']),'exposure_cache_key':f'{source}-white-{cct}-gm{gm}','timing_acceptance':'observed_elapsed_record_only','strip_zero_required':source=='ray','ray_zero_required':source=='strip','session_index':len(source_captures)+1,'source_order':1 if source=='ray' else 2,'target_cct':cct,'target_gm':gm,'steady_claim':False})
plan['captures']=source_captures
plan['capture_ids']=[s['capture_id'] for s in source_captures]
plan['analysis_contract']['target_contracts']=[{'target_index':i,'cct':cct,'gm':gm,'active_channel':str(baseline_by_key[(cct,gm)]['feedback_optimizer']['active_channel']),'base_command':{ch:int(baseline_by_key[(cct,gm)]['selected_command'][ch]) for ch in thermal.CHANNELS},'probes':[],'resolved_cct_tolerance_K':float(baseline_by_key[(cct,gm)]['feedback_goal']['resolved_cct_tolerance_K']),'duv_tolerance':float(baseline_by_key[(cct,gm)]['feedback_goal']['duv_tolerance']),'channel_penalties':dict(baseline_by_key[(cct,gm)]['feedback_optimizer']['channel_penalties']),'damping':float(baseline_by_key[(cct,gm)]['feedback_optimizer']['damping']),'maximum_step_code':int(baseline_by_key[(cct,gm)]['feedback_optimizer']['final_max_step_code'])} for i,(cct,gm) in enumerate(sorted(keys))]
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
