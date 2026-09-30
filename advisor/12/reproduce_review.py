#!/usr/bin/env python3
"""Reproduce the GUIDE11 review from processed evidence only.

Usage:
  python reproduce_review.py --evidence /path/to/extracted/evidence --out ./review.json
  python reproduce_review.py --evidence GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929.zip --out ./review.json

Requires numpy and scipy, and the source snapshot included in the evidence.
No RAW decoding, network requests, equipment access, or modification of evidence.
The historical source helper is used only for the frozen white-point arithmetic.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import tempfile
import zipfile
from collections import Counter
import numpy as np
from scipy.stats import t, chi2
from scipy.spatial import cKDTree

AXES = ('cct_K', 'mired', 'duv')
CHANNELS = ('cw', 'ww', 'r', 'g', 'b')

def read_json(p: Path):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def jsonl(p: Path):
    return [json.loads(s) for s in p.read_text(encoding='utf-8-sig').splitlines() if s.strip()]

def zvec(z):
    return np.array([z['log_R_over_G'], z['log_B_over_G']], dtype=float)

def exportable(x):
    if isinstance(x, np.ndarray): return exportable(x.tolist())
    if isinstance(x, np.generic): return exportable(x.item())
    if isinstance(x, dict): return {str(k): exportable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [exportable(v) for v in x]
    if isinstance(x, float) and not math.isfinite(x): return None
    return x

def error(a, b):
    return {x: float(a[x]-b[x]) for x in AXES}

def objective(e, tol):
    return float(max(abs(e[x])/tol[x] for x in AXES))

def distribution(rows):
    x = np.asarray([[r[k] for k in AXES] for r in rows])
    return {'n':len(rows), 'interpretation':'empirical distribution over this designed grid, NOT a noise or population distribution',
            'absolute_error_quantiles':{k:dict(zip(('median','p95','maximum'),np.quantile(abs(x[:,i]),[.5,.95,1]).tolist())) for i,k in enumerate(AXES)}}

def normal_t_intervals(values):
    a=np.asarray(values,float); n=len(a); sd=a.std(ddof=1); mu=a.mean(); q=t.ppf(.975,n-1)
    return {'n_independent_cycles':n,'mean':mu,'sample_sd':sd,
            'CI95_mean_conditional':[mu-q*sd/np.sqrt(n),mu+q*sd/np.sqrt(n)],
            'PI95_one_new_cycle_conditional':[mu-q*sd*np.sqrt(1+1/n),mu+q*sd*np.sqrt(1+1/n)],
            'assumptions':'iid approximately normal cycle differences; small n; no established transfer to different sessions/environment/commands',
            'unconditional_operational_coverage_established':False}

def map_points(grid):
    """Exact legacy forward map and original 0.1 degree / 1 pp inverse lattice."""
    white=zvec(next(x for x in grid if x['sat']==0)['z_mean'])
    h=np.arange(3600)/10; s=np.arange(101)
    def level(sat):
        a=sorted((x['hue'],zvec(x['z_mean'])) for x in grid if x['sat']==sat)
        hs=np.array([x[0] for x in a]); zs=np.array([x[1] for x in a])
        return np.array([np.interp(h,hs,zs[:,i],period=360) for i in range(2)]).T
    z50,z100=level(50),level(100); out=np.empty((3600,101,2))
    out[:,:51]=white+(s[:51]/50)[None,:,None]*(z50[:,None]-white)
    out[:,51:]=z50[:,None]+((s[51:]-50)/50)[None,:,None]*(z100[:,None]-z50[:,None])
    return out.reshape(-1,2)

def analyze(root: Path):
    root=root.resolve()
    j=lambda p:read_json(root/p)
    manifest=j('MANIFEST.json')
    entries=manifest.get('files',manifest.get('members',[]))
    # Export uses a list of path/bytes/sha256 records.
    if isinstance(entries,dict): entries=[dict(path=k,**v) for k,v in entries.items()]
    if not entries: raise ValueError('Manifest has no supported file entries')
    failed=[]
    for rec in entries:
        rel=rec.get('path',rec.get('relative_path',rec.get('archive_path')))
        p=root/rel
        size=rec.get('byte_count',rec.get('bytes',rec.get('size')))
        ok=p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256']
        if size is not None: ok=ok and p.stat().st_size==size
        if not ok: failed.append(rel)
    if failed: raise ValueError(f'Manifest verification failed: {failed[:10]}')
    sys.path.insert(0,str(root/'source/src'))
    from camera_based_rgbww_optimizer.optimization.white_calibration_common import estimate_white_point_from_camera_neutral
    observations=jsonl(root/'OBSERVATIONS.jsonl')
    pwm=j('replay/fullscale-pwm-ledger.json')['rows']
    full={(p['run_alias'],cid):p['fullscale_4095_actual'] for p in pwm for cid in p['group_capture_ids']}
    channel_keys={'cw':'cold_white','ww':'warm_white','r':'red','g':'green','b':'blue'}
    actual={(p['run_alias'],cid):{k:p['readback_device_snapshot'][v] for k,v in channel_keys.items()}
            for p in pwm for cid in p['group_capture_ids'] if p.get('readback_device_snapshot')}
    flat=[]; rail=[]; matrices={}
    for o in observations:
        key=o['logical_key']; path=o.get('measurement_file')
        a={'alias':key['run_alias'],'capture_id':key['capture_id'],'source':o['source_id'],
           'raw_sha256':o['raw_identity']['sha256'],'target':o.get('target'),
           'command':o.get('requested_command'),'timing':o.get('timing'),
           'fullscale_actual':full.get((key['run_alias'],key['capture_id'])),
           'command_coordinate':'plan_command_before_control_mapping',
           'actual_pwm':actual.get((key['run_alias'],key['capture_id'])),
           'measured':bool(path and (root/path).is_file())}
        if a['measured']:
            st=j(path); block=next(b for b in st['patches'] if b['index']==6)
            p={k:block['planes'][k]['statistics']['normalized_per_second']['trimmed_mean'] for k in ('R','G1','G2','B')}
            g=(p['G1']+p['G2'])/2
            a['planes']=p; a['z']=[math.log(p['R']/g),math.log(p['B']/g)] if min(p.values())>0 else None
            a['exposure_seconds']=st.get('exposure_seconds')
            for k,plane in block['planes'].items():
                raw=plane['statistics']['raw_code']
                if raw.get('variance')==0 and raw.get('maximum',0)>=16000:
                    rail.append({'alias':a['alias'],'capture_id':a['capture_id'],'plane':k,
                                 'raw_code_statistics':raw,'metrics':plane['metrics'],
                                 'legacy_quality':plane['quality'],'cfa':plane.get('cfa'),
                                 'status':'near_white_zero_variance_rail_diagnostic_not_valid_for_color_fit'})
            if a['target'] and a['target'].get('target_cct') is not None and a['z']:
                mid=o['raw_identity']['matrix_id']
                if mid not in matrices: matrices[mid]=np.array(j(f'matrices/{mid}.json')['rgb_xyz_matrix_first3'])
                est=estimate_white_point_from_camera_neutral([p['R']/g,1,p['B']/g],matrices[mid])
                a['wp']={'cct_K':float(est['cct_K']),'mired':1e6/float(est['cct_K']),'duv':float(est['duv'])}
        flat.append(a)
    lookup={(a['alias'],a['capture_id']):a for a in flat}
    targets=j('derived/guide11-n1/w1-frozen-targets-20260922.json')['nodes']
    tby={(a['cct'],a['gm']):a for a in targets}
    wf=j('frozen-inputs/guide11-white-final-report-20260928.json')
    pairs=[]
    for a in flat:
        if not a['alias'].startswith('guide11-w2/') or a['source']!='strip' or 'wp' not in a: continue
        k=(a['target']['target_cct'],a['target']['target_gm']); cid=a['capture_id'].rsplit('candidate',1)[-1]
        rr=[b for b in flat if b['alias'].startswith('guide11-w2/') and b['source']=='ray' and
            (b['target']['target_cct'],b['target']['target_gm'])==k and b['capture_id'].endswith('candidate'+cid)]
        if len(rr)!=1: raise ValueError(f'Ambiguous W2 pair: {k} {cid}')
        b=rr[0]; tol=tby[k]['tolerances']; e=error(a['wp'],b['wp']); eh=error(a['wp'],tby[k]['ray_target'])
        pairs.append({'cct':k[0],'gm':k[1],'candidate':cid,'command':a['command'],'command_coordinate':a['command_coordinate'],'actual_pwm':a['actual_pwm'],'fullscale':a['fullscale_actual'],
                      'strip_key':[a['alias'],a['capture_id']],'ray_key':[b['alias'],b['capture_id']],
                      'e_paired':e,'E_paired':objective(e,tol),'e_historical':eh,'E_historical':objective(eh,tol),
                      'CI95':None,'PI95':None,'interval_status':'single selection observation, no independent confirmation'})
    selected=[]; clean70=[]
    for r in wf['nodes']:
        if r['command_source']!='w8_fallback':
            cc=next(a for a in pairs if (a['cct'],a['gm'])==(r['cct'],r['gm']) and a['command']==r['command'])
            selected.append(cc); e=cc['e_paired']; scope='W2_selection_frame_vs_same_candidate_fresh_Ray'
        else:
            e={x:r['error_evidence']['e_'+x] for x in AXES}; scope='W6_single_historical_pair'
        clean70.append({'cct':r['cct'],'gm':r['gm'],'command':r['command'],'actual_pwm':cc['actual_pwm'] if scope.startswith('W2') else None,
                        'command_coordinate':'plan_command_before_control_mapping','historical_readback_note':'W6 rows retain historical evidence without a new readback claim in this replay',
                        'errors':e,'scope':scope,
                        'tolerances':r['tolerances'],'E':objective(e,r['tolerances']),
                        'CI95':None,'PI95':None,'interval_status':'no validated current-epoch node-level prediction model; N1 anchors reported separately'})
    secants=[]
    for node in targets:
        dd=node.get('measured_secant_evidence',{}).get('observations',[]);k=(node['cct'],node['gm'])
        if k not in {(a['cct'],a['gm']) for a in pairs} or len(dd)<2:continue
        tol=np.array([node['tolerances'][x] for x in AXES]); tv=np.array([node['ray_target'][x] for x in AXES])/tol
        rr=np.array([[a['strip_white_point'][x] for x in AXES] for a in dd])/tol-tv
        cs=np.array([[a['command'][x] for x in CHANNELS] for a in dd],float)
        bidx=np.argmin(np.max(abs(rr),axis=1)); mask=np.any(cs!=cs[bidx],axis=1); A=cs[mask]-cs[bidx]
        wrong=np.linalg.lstsq(A,rr[mask],rcond=None)[0]; correct=np.linalg.lstsq(A,rr[mask]-rr[bidx],rcond=None)[0]
        secants.append({'cct':k[0],'gm':k[1],'rank_command_deltas':int(np.linalg.matrix_rank(A)),
                        'wrong_sensitivity_norm':float(np.linalg.norm(wrong)),
                        'corrected_sensitivity_norm':float(np.linalg.norm(correct)),
                        'relative_difference':float(np.linalg.norm(wrong-correct)/max(np.linalg.norm(correct),1e-20))})
    w3=j('derived/guide11-w3/w3-holdout-analysis-20260924.json'); w3rows=[]
    for r in w3['points']:
        a=next(a for a in flat if a['alias'].startswith('guide11-w3/') and a['source']=='strip' and
               (a['target']['target_cct'],a['target']['target_gm'])==(r['cct'],r['gm']))
        e=error(r['strip_white_point'],r['ray_white_point'])
        w3rows.append({'cct':r['cct'],'gm':r['gm'],'command':r['command'],'E':r['holdout_E'],
                       'errors':e,'actual_pwm':a['actual_pwm'],'command_coordinate':a['command_coordinate'],
                       'fullscale_actual':a['fullscale_actual'],'CI95':None,'PI95':None,
                       'interval_status':'one pair, no validated transfer model; two isolated passing samples do not establish an interval'})
    n1=j('derived/guide11-n1/n1-combined-analysis-20260922.json'); noise=[]; bursts=[]; n1_replay=[]
    for p in n1['points']:
        for cycle_id, cy in p['cycles'].items():
            rr=next(a for a in flat if a['alias'].startswith('guide11-n1/') and a['capture_id']==cy['ray_capture'])
            ss=next(a for a in flat if a['alias'].startswith('guide11-n1/') and a['capture_id']==cy['strip_capture'])
            n1_replay.append({'cct':p['cct'],'gm':p['gm'],'cycle_id':cycle_id,
                'recomputed_minus_frozen':{x:(ss['wp'][x]-rr['wp'][x])-cy['diff'][x] for x in AXES}})
        noise.append({'cct':p['cct'],'gm':p['gm'],
                      'axes':{x:normal_t_intervals([c['diff'][x] for c in p['cycles'].values()]) for x in AXES}})
        if not p.get('is_burst_point'):continue
        for source in ('ray','strip'):
            ids=set(p['burst_layer'][source]['capture_ids'])
            aa=[a for a in flat if a['alias'].startswith('guide11-n1/') and a['capture_id'] in ids]
            stat={}
            for x in AXES:
                v=np.array([a['wp'][x] for a in aa]); n=len(v); sd=v.std(ddof=1)
                stat[x]={'mean':v.mean(),'sd':sd,'sd_CI95_normal':[sd*np.sqrt((n-1)/chi2.ppf(.975,n-1)),sd*np.sqrt((n-1)/chi2.ppf(.025,n-1))]}
            bursts.append({'cct':p['cct'],'gm':p['gm'],'source':source,'n':len(aa),'statistics':stat})
    w4=j('derived/guide11-w4/w4-protocol-analysis-20260924.json'); long=[]
    for p in w4['points']:
        tol=tby[p['cct'],p['gm']]['tolerances']
        e=error(p['long_strip_minus_ray'],p['fast_strip_minus_ray'])
        long.append({'cct':p['cct'],'gm':p['gm'],'delta_LONG_minus_FAST_error':e,
                     'FAST_error':p['fast_strip_minus_ray'],'LONG_error':p['long_strip_minus_ray'],
                     'FAST_E':objective(p['fast_strip_minus_ray'],tol),'LONG_E':objective(p['long_strip_minus_ray'],tol),
                     'CI95':None,'PI95':None,'interpretation':'one pair per point; all FAST before all LONG; protocol confounded with period/session'})
    c1=j('derived/guide11-c1/c1-confirm-analysis-20260928.json'); colors=[]
    for r in c1['targets']:
        alias='guide11-c1/'+r['bracket_root'].replace('\\','/').split('/')[-1]
        rr=[a for a in flat if a['alias']==alias and a['source']=='ray' and a['target']['c1_hue']==r['hue'] and a['target']['c1_sat']==r['sat'] and a['measured']]
        ss=[lookup[alias,c['capture_id']] for c in r['confirms']]
        rz=np.array([a['z'] for a in rr]); sz=np.array([a['z'] for a in ss]); e=sz.mean(0)-rz.mean(0)
        se=np.sqrt(sz.var(0,ddof=1)/len(sz)+rz.var(0,ddof=1)/len(rz)); q=t.ppf(.975,1)
        ci=np.stack([e-q*se,e+q*se])
        colors.append({'hue':r['hue'],'sat':r['sat'],'command':r['selected_command'],
                       'fullscale_actual':all(a['fullscale_actual'] for a in ss),
                       'actual_pwm':ss[0]['actual_pwm'],'command_coordinate':'plan_command_before_control_mapping','n_ray':len(rr),'n_strip':len(ss),
                       'delta_z':e,'z_distance':np.linalg.norm(e),'ratio_percent':100*np.expm1(e),
                       'CI95_delta_z_conditional_t_df1':ci,'CI95_ratio_percent_conditional':100*np.expm1(ci),
                       'CI_axis_order':['R/G','B/G'],'CI_array_order':['lower','upper'],
                       'strip_repeat_distance_z':np.linalg.norm(sz[0]-sz[1]),
                       'PI95':None,'interval_status':'source-independent normal repeat errors, conservative df1 marginal intervals; selection excluded; not simultaneous and not an across-session guarantee',
                       'coverage_Ray_sat':None,'coverage_status':'map_unqualified; not 0 percent'})
    c2=j('derived/guide11-c2/c2-s25-analysis-20260928.json');c4=j('derived/guide11-c4/c4-holdout-analysis-20260928.json')
    grid=j('derived/guide11-c1/c3-anchor-self-check-20260925.json')['grid'];tree=cKDTree(map_points(grid));selfcheck=[]
    for cohort,ts in [('C2S25',c2['targets']),('C4',c4['targets']),('C1confirm_calibration_not_holdout',c1['targets'])]:
        for r in ts:
            distance,idx=tree.query(zvec(r['ray_z_mean'])); h=(int(idx)//101)/10;s=int(idx)%101
            selfcheck.append({'cohort':cohort,'hue':r['hue'],'sat':r['sat'],'Ray_self_hue':h,'Ray_self_sat':s,
                              'hue_error':(h-r['hue']+180)%360-180,'sat_error_pp':s-r['sat'],'residual_z':distance})
    zero=[a for a in flat if a['alias'].startswith('guide9/guide9-h0-s0-best') and a.get('z')]
    rz=np.array([a['z'] for a in zero if a['source']=='ray']);sz=np.array([a['z'] for a in zero if a['source']=='strip'])
    e=sz.mean(0)-rz.mean(0); se=np.sqrt(sz.var(0,ddof=1)/len(sz)+rz.var(0,ddof=1)/len(rz))
    fake=zvec(next(a for a in grid if a['sat']==0)['z_mean']); actual=rz.mean(0)
    zero_result={'legacy_C3_zero':fake,'true_historical_HSI_zero':actual,'distance':np.linalg.norm(fake-actual),
                 'ratio_difference_percent':100*np.expm1(fake-actual),'historical_strip_minus_true_HSI_Ray_z':e,
                 'CI95_marginal_conditional':np.stack([e-t.ppf(.975,1)*se,e+t.ppf(.975,1)*se]),
                 'strip_ratio_error_percent':100*np.expm1(e),'SAT0_point_pass':bool(np.all(abs(e)<=.01)),
                 'current_epoch_validation':False}
    eligible=[a for a in w3rows if a['fullscale_actual']]
    return exportable({'schema':'guide12_advisor_recomputed_v1','evidence_manifest_members_verified':len(entries),
        'physical_rows':len(flat),'unique_RAW_hashes':len({a['raw_sha256'] for a in flat}),
        'RAW_hash_recalculation':'not performed here; original RAW not in ZIP; ledger/exporter hashes retained',
        'measured_rows':sum(a['measured'] for a in flat),'source_counts':dict(Counter(a['source'] for a in flat)),
        'strip_command_rows':len(pwm),'actual_fullscale_command_rows':sum(a['fullscale_4095_actual'] for a in pwm),
        'white70_mixed_epoch_count_only':sum(a['E']<=1 for a in clean70),
        'white70':clean70,'white70_empirical_distribution':distribution([a['errors'] for a in clean70]),
        'W2_all_paired':pairs,'W2_adopted':selected,'W2_adopted_same_pair_point_pass':sum(a['E_paired']<=1 for a in selected),
        'W2_independent_confirmations':0,'W2_secant_diagnostics':secants,
        'W3':w3rows,'W3_point_pass':sum(a['E']<=1 for a in w3rows),
        'W3_fullscale_count':len(eligible),'W3_fullscale_point_pass':sum(a['E']<=1 for a in eligible),
        'W3_empirical_distribution':distribution([a['errors'] for a in w3rows]),
        'N1':noise,'N1_bursts':bursts,'N1_primitive_replay':n1_replay,'W4':long,'C1_two_independent_confirmations':colors,
        'Ray_self_inverse_diagnostic':selfcheck,'SAT0':zero_result,'near_white_rail_planes':rail,
        'C1_B1_rail_frame_count':len({(a['alias'],a['capture_id']) for a in rail if a['alias']=='guide11-c1/formal-c1-20260924-r8'}),
        'C1_B1_strip_frame_count':sum(a['alias']=='guide11-c1/formal-c1-20260924-r8' and a['source']=='strip' for a in flat),
        'physical_observation_index':[{k:a[k] for k in ('alias','capture_id','source','raw_sha256','target','command','command_coordinate','actual_pwm','fullscale_actual','measured')} for a in flat]})

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--out',type=Path,required=True); args=ap.parse_args()
    if args.evidence.is_file():
        with tempfile.TemporaryDirectory(prefix='guide11-readonly-') as td:
            base=Path(td)
            with zipfile.ZipFile(args.evidence) as z:
                if z.testzip() is not None: raise ValueError('ZIP CRC failure')
                for name in z.namelist():
                    if not (base/name).resolve().is_relative_to(base.resolve()):raise ValueError('Unsafe ZIP path')
                z.extractall(base)
            roots=list(base.rglob('OBSERVATIONS.jsonl'))
            root=next(p.parent for p in roots if (p.parent/'MANIFEST.json').is_file())
            result=analyze(root)
    else: result=analyze(args.evidence)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('evidence_manifest_members_verified','physical_rows','unique_RAW_hashes','white70_mixed_epoch_count_only','W3_fullscale_point_pass')},ensure_ascii=False))

if __name__=='__main__':main()
