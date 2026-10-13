"""Offline Advisor review. Usage: python review_guide12.py BASE COMPLETION OUTPUT
No device/network access. Inputs are immutable extracted GUIDE12 packages.
Requires numpy/scipy. Imports only supplied white estimator and pure runtime functions.
"""
from pathlib import Path
import sys,json,hashlib,math,collections,inspect
import numpy as np
from scipy.stats import t,chi2
B,C,O=map(Path,sys.argv[1:4]); O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(C/'source/src'))
from camera_based_rgbww_optimizer.optimization import white_calibration_common as wcc,guide12_w123 as w123,guide12_c124 as c124

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def jl(p):return [json.loads(x) for x in Path(p).read_text(encoding='utf-8').splitlines() if x.strip()]
def clean(x):
 if isinstance(x,np.ndarray):return clean(x.tolist())
 if isinstance(x,np.generic):return clean(x.item())
 if isinstance(x,float) and not math.isfinite(x):return None
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x
def save(name,x):(O/name).write_text(json.dumps(clean(x),ensure_ascii=False,indent=2),encoding='utf-8')
obs=jl(C/'OBSERVATIONS_COMPLETE.jsonl'); ri=jl(C/'RAW_INDEX_COMPLETE.jsonl')
bykey={(x['run_alias'],x['capture_id']):x for x in obs}
MAT=next(iter((C/'matrices').glob('*.json'))); matrix=load(MAT)['matrix_3x3']
feature_ids=load(C/'config/hsi/strip-hsi-policy-v2-waiting.json')['feature_set']['ids']
W=load(B/'results/w12-2-verification-analysis.json'); N=load(B/'results/n2-repeatability-analysis-20261005.json'); L=load(B/'models/white-final-lut.json')
prim={}; allrows=[]
for ob in obs:
 alias,cid=ob['run_alias'],ob['capture_id']; stp=B/'measurements'/alias/(cid+'.patch-statistics.json')
 if not stp.exists():stp=C/'measurements'/alias/(cid+'.patch-statistics.json')
 st=load(stp); blocks={p['index']:p for p in st['patches']}; block=blocks[6]
 planes={pl:block['planes'][pl]['statistics']['normalized_per_second']['trimmed_mean'] for pl in ('R','G1','G2','B')}
 g=(planes['G1']+planes['G2'])/2
 z=[math.log(planes['R']/g),math.log(planes['B']/g)] if min(planes.values())>0 else None
 pqual={pl:block['planes'][pl]['quality']['status'] for pl in planes}
 feat=[]; fqual=[]
 for fid in feature_ids:
  idx,pl=fid.split('::'); p=blocks[int(idx.split('_')[1])]['planes'][pl]
  feat.append(p['statistics']['normalized_per_second']['trimmed_mean']); fqual.append(p['quality']['status']=='accepted')
 p={'run':alias,'capture_id':cid,'source':ob.get('source_id'), 'step':ob.get('plan_step')or{},'z':z,'planes':planes,'primary_quality':pqual,'primary_valid':all(q=='accepted' for q in pqual.values()), 'features58':feat,'valid_features58':sum(fqual),'frame_status':((ob.get('capture')or{}).get('direct_quality')or{}).get('status'), 'exposure_s':st.get('exposure_seconds'),'raw_sha':st['source'].get('sha256'), 'source_stat':str(stp.relative_to(B) if stp.is_relative_to(B) else stp.relative_to(C)),
 'primary_metrics':{pl:{'raw_min':block['planes'][pl]['statistics']['raw_code']['minimum'],'raw_max':block['planes'][pl]['statistics']['raw_code']['maximum'],'raw_mean':block['planes'][pl]['statistics']['raw_code']['mean'],'raw_variance':block['planes'][pl]['statistics']['raw_code']['variance'],'black_level':block['planes'][pl]['cfa']['black_level'],'white_level':block['planes'][pl]['cfa']['effective_white_level'],**block['planes'][pl]['metrics']}for pl in planes}}
 for idx in (5,):
  v={pl:blocks[idx]['planes'][pl]['statistics']['normalized_per_second']['trimmed_mean']for pl in planes};gg=(v['G1']+v['G2'])/2
  p[f'z_block{idx}']=[math.log(v['R']/gg),math.log(v['B']/gg)] if min(v.values())>0 else None
 prim[(alias,cid)]=p;allrows.append(p)
print('primitives',len(prim),flush=True)
wp_cache={}
def wp(alias,cid):
 key=(alias,cid)
 if key not in wp_cache:
  z=prim[key]['z'];d=wcc.estimate_white_point_from_camera_neutral([math.exp(z[0]),1,math.exp(z[1])],matrix)
  wp_cache[key]={'cct_K':d['cct_K'],'mired':1e6/d['cct_K'],'duv':d['duv']}
 return wp_cache[key]
components=['cct_K','mired','duv'];tol=np.array([25.,1.,.0005])
def intervals_iid(arr,alpha=.05):
 a=np.asarray(arr,float);n=len(a);mu=a.mean(axis=0);ret={'n':n,'mean':mu,'min':a.min(axis=0),'max':a.max(axis=0)}
 if n<2:return {**ret,'sd':None,'mean_ci95':None,'next_pi95':None,'reason':'only_one_independent_observation; no_empirical_variance'}
 sd=a.std(axis=0,ddof=1);q=t.ppf(1-alpha/2,n-1);k=a.shape[1]if a.ndim>1 else 1;qj=t.ppf(1-alpha/(2*k),n-1)
 return {**ret,'sd':sd,'sd_ci95':np.stack([sd*np.sqrt((n-1)/chi2.ppf(.975,n-1)),sd*np.sqrt((n-1)/chi2.ppf(.025,n-1))],-1),'mean_ci95':np.stack([mu-q*sd/np.sqrt(n),mu+q*sd/np.sqrt(n)],-1),'next_pi95':np.stack([mu-q*sd*np.sqrt(1+1/n),mu+q*sd*np.sqrt(1+1/n)],-1),'joint_mean_box95':np.stack([mu-qj*sd/np.sqrt(n),mu+qj*sd/np.sqrt(n)],-1),'joint_next_box95':np.stack([mu-qj*sd*np.sqrt(1+1/n),mu+qj*sd*np.sqrt(1+1/n)],-1),'assumption':'conditional iid Gaussian independent cycles at same fixed source/protocol; not established across arbitrary sessions','df':n-1}
# White source replay and per-node reporting
pairs=[];maxdev={k:0. for k in components}
for orig in W['node_pairs']:
 refs=[];ids=[];sq=None
 for role,s in orig['steps'].items():
  alias='guide12-w122/'+s['run'];cid=s['capture_id'];p=prim[(alias,cid)]
  if role=='strip':sq=p
  elif role in ('ray','raybefore','rayafter') and s['quality']=='pass':refs.append(wp(alias,cid));ids.append({'run':alias,'capture_id':cid})
 if sq is not None and refs:
  ww=wp(sq['run'],sq['capture_id']);ref={k:np.mean([r[k] for r in refs])for k in components};err={k:ww[k]-ref[k]for k in components}
  for k in components:maxdev[k]=max(maxdev[k],abs(err[k]-orig['signed_errors'][k]))
  pairs.append({'node':orig['node'],'repeat':orig['repeat'],'signed_errors':err,'E':max(abs(err[k])/v for k,v in zip(components,tol)), 'original_pair_valid':orig.get('pair_valid'), 'primary_valid':sq['primary_valid']and all(prim[(r['run'],r['capture_id'])]['primary_valid']for r in ids), 'source':{'strip':{'run':sq['run'],'capture_id':sq['capture_id']},'ray':ids},'command':sq['step']['command'],'reference':ref,'strip_white_point':ww,'original_reference_drift':orig.get('cold_drift')})
nodes=[]
for n in L['nodes']:
 key=f"{n['cct']}/{n['gm']}";rr=[p for p in pairs if p['node']==key];aa=[p for p in rr if p['original_pair_valid']and p['primary_valid']]
 rawerr=np.array([[p['signed_errors'][c]for c in components]for p in rr]);validerr=np.array([[p['signed_errors'][c]for c in components]for p in aa])
 stats=intervals_iid(validerr)if len(validerr)else {'n':0,'mean_ci95':None,'next_pi95':None,'reason':'reference_bracket_failed'}
 nodes.append({'node':key,'cct':n['cct'],'gm_raw':n['gm'],'command':n['command'],'changed':n['changed_since_w2'],'observed_pairs':len(rr),'valid_pairs':len(aa),'original_verdict':next(x['verdict']for x in W['node_summary']if x['node']==key),'descriptive_mean_error_including_reference_limited':dict(zip(components,rawerr.mean(axis=0))), 'conditional_statistics_valid_pairs':stats,'validation_shortfall':(max(0,3-len(aa))if n['changed_since_w2']else None),'independently_verified_across_sessions':key=='3200/0','CI_PI_note':'n=1 cannot inherit a variance model without demonstrated transfer; n=2 intervals are conditional descriptive, not full GUIDE12 assurance'})
summary={'original_machine_summary':W['summary'],'report_exceeds_typo':{'claimed':19,'machine_and_recomputed':29},'node_count':len(nodes),'point_pass_percent':38/70*100,'actual_new_confirmation_counts':dict(collections.Counter(p['observed_pairs']for p in nodes)), 'corrected_vs_source_max_abs_deviation':maxdev,'changed_nodes':sum(n['changed']for n in nodes),'changed_three_confirmations_short':sum(n['changed']and n['node']!='3200/0'and n['valid_pairs']<3 for n in nodes)}
e=np.array([list(n['descriptive_mean_error_including_reference_limited'].values())for n in nodes]);summary['across_70_design_nodes_error_distribution']={k:{'abs_median':np.median(abs(e[:,i])),'abs_p95':np.percentile(abs(e[:,i]),95),'abs_max':np.max(abs(e[:,i])),'signed_min':np.min(e[:,i]),'signed_max':np.max(e[:,i])}for i,k in enumerate(components)}
save('white_nodes.json',{'summary':summary,'components':components,'nodes':nodes,'pairs':pairs})
print('white done',summary,flush=True)
# Correct interpolation as an OFFLINE mathematical counterfactual, not new photometric validation.
def corrected(cct,gm):
 ccts=sorted({n['cct']for n in L['nodes']});gms=sorted({n['gm']for n in L['nodes']});by={(n['cct'],n['gm']):n for n in L['nodes']}
 if (cct,gm)in by:return dict(by[(cct,gm)]['command'])
 i=next(i for i in range(len(ccts)-1)if ccts[i]<=cct<=ccts[i+1]);j=next(j for j in range(len(gms)-1)if gms[j]<=gm<=gms[j+1]);mlo,mhi=1e6/ccts[i],1e6/ccts[i+1];w=(1e6/cct-mhi)/(mlo-mhi);v=(gm-gms[j])/(gms[j+1]-gms[j]);raw={ch:w*(1-v)*by[ccts[i],gms[j]]['command'][ch]+w*v*by[ccts[i],gms[j+1]]['command'][ch]+(1-w)*(1-v)*by[ccts[i+1],gms[j]]['command'][ch]+(1-w)*v*by[ccts[i+1],gms[j+1]]['command'][ch]for ch in w123.CHANNELS};mx=max(raw.values());return {ch:int(round(x*4095/mx))for ch,x in raw.items()}
bad=[]
for n in L['nodes']:
 old=w123.interpolate_fullscale_command(L['nodes'],n['cct'],n['gm'])['command']
 if old!=n['command']:bad.append({'node':f"{n['cct']}/{n['gm']}",'expected':n['command'],'executed_function_at_node':old})
counter=[]
for cct,gm in w123.W123_REQUESTS:
 old=w123.interpolate_fullscale_command(L['nodes'],cct,gm)['command'];new=corrected(cct,gm);ccts=sorted({n['cct']for n in L['nodes']});i=next(i for i in range(len(ccts)-1)if ccts[i]<=cct<=ccts[i+1]);counter.append({'request':f'{cct}/{gm}','old':old,'corrected_mathematical_candidate':new,'old_weights_correspond_to_mirrored_menu_cct':1e6/(1e6/ccts[i]+1e6/ccts[i+1]-1e6/cct),'max_command_change':max(abs(old[ch]-new[ch])for ch in old),'photometric_validation_of_corrected_command':'not_acquired'})
save('interpolation_audit.json',{'node_identity_failures':len(bad),'total_nodes':70,'failures':bad,'corrected_identity_passes':sum(corrected(n['cct'],n['gm'])==n['command']for n in L['nodes']),'counterfactuals':counter,'original_white_holdout':load(B/'results/w12-3-interpolation-analysis-20261008.json'),'color_endpoint_commands':{f'{h}/{s}':c124.c124_model_command(h,s)['command']for h,s in [(0,0),(0,10),(0,20),(0,25),(60,50),(60,100)]},'note':'corrected output is a proposed command only; old photographs do not validate it'})
# N2 session/cycle statistics, source separated. Exact mean/session-mean prediction
# under iid normal session means, moment-estimator individual-operation PI labeled approximate.
noise=[]
for state in N['white_states']:
 old=N['white_states'][state];d=[];sources={s:[]for s in ['ray','strip']}
 for sess in [1,2,3]:
  ar=[]
  for cyc in [1,2]:
   pp={}
   for s in sources:
    frame=next(f for f in N['frames']if f['session']==sess and f['cycle']==cyc and f['state']==state and f['source']==s and not f['is_burst_extra']);alias='guide12-n2/'+frame['run_root'].replace('\\','/').split('/')[-1];vv=wp(alias,frame['capture_id']);pp[s]=np.array([vv[k]for k in components]);sources[s].append(pp[s])
   ar.append(pp['strip']-pp['ray'])
  d.append(ar)
 a=np.asarray(d);sm=a.mean(axis=1);cw=(a-sm[:,None,:]);vw=np.sum(cw*cw,axis=(0,1))/3;vbar=sm.var(axis=0,ddof=1);vb=np.maximum(0,vbar-vw/2);mu=a.mean(axis=(0,1));marg=intervals_iid(sm);q=t.ppf(.975,2);qj=t.ppf(1-.05/6,2)
 predvar=vb+vw+(vb+vw/2)/3;predhalf=q*np.sqrt(predvar);predj=qj*np.sqrt(predvar)
 stats={'state':state,'paired_values':a,'session_means':sm,'mean':mu,'min':a.min(axis=(0,1)),'max':a.max(axis=(0,1)),'session_mean_statistics':marg,'within_cycle_sd':np.sqrt(vw),'within_cycle_sd_ci95':np.stack([np.sqrt(3*vw/chi2.ppf(.975,3)),np.sqrt(3*vw/chi2.ppf(.025,3))],-1),'between_session_sd_moment':np.sqrt(vb),'approx_next_individual_operation_PI95':np.stack([mu-predhalf,mu+predhalf],-1),'approx_next_individual_operation_joint95':np.stack([mu-predj,mu+predj],-1),'prediction_caveat':'random-intercept Gaussian stationary-session moment model; df=2 working approximation without a guaranteed conservative coverage, not exact calibrated finite-sample prediction; trends and arbitrary ambient changes not covered','independent_sessions':3,'cycles_per_session':2,'sources':{}}
 # conservative Bonferroni variance-component interval; derived from two variance CIs
 lo_mean=2*vbar/chi2.ppf(.9875,2);hi_mean=2*vbar/chi2.ppf(.0125,2);lo_w=3*vw/chi2.ppf(.9875,3);hi_w=3*vw/chi2.ppf(.0125,3)
 stats['between_session_sd_conservative_ci95']=np.sqrt(np.stack([np.maximum(0,lo_mean-hi_w/2),np.maximum(0,hi_mean-lo_w/2)],-1))
 for s,v in sources.items():
  v=np.array(v).reshape(3,2,3);m=v.mean(axis=1);ssw=np.sum((v-m[:,None,:])**2,axis=(0,1))/3;ssb=np.maximum(0,m.var(axis=0,ddof=1)-ssw/2)
  stats['sources'][s]={'values':v,'session_means':m,'cycle_sd':np.sqrt(ssw),'cycle_sd_ci95':np.sqrt(np.stack([3*ssw/chi2.ppf(.975,3),3*ssw/chi2.ppf(.025,3)],-1)),'between_session_sd_moment':np.sqrt(ssb),'session_mean_statistics':intervals_iid(m)}
 stats['old_PI_schema_issue']={k:{'old_low_high_are_mean_CI':[old['component_statistics'][k]['pi_next_fast_operation_marginal95']['low'],old['component_statistics'][k]['pi_next_fast_operation_marginal95']['high']],'old_pi_half_width':old['component_statistics'][k]['pi_next_fast_operation_marginal95']['pi_half_width']}for k in components}
 noise.append(stats)
bursts=[]
for state in N['white_states']:
 for s in ['ray','strip']:
  fs=[f for f in N['frames']if f['state']==state and f['source']==s and f['session']==1 and f['cycle']==1]
  if len(fs)<3:continue
  vals=[];tt=[]
  for f in fs:
   alias='guide12-n2/'+f['run_root'].replace('\\','/').split('/')[-1];ww=wp(alias,f['capture_id']);vals.append([ww[k]for k in components]);o=bykey[alias,f['capture_id']];tt.append(o.get('best_effort_exposure_start_elapsed_s'))
  bursts.append({'state':state,'source':s,'observed_elapsed_s':tt,'values':vals,'last_minus_first':np.array(vals[-1])-vals[0],'descriptive_statistics':intervals_iid(vals),'caveat':'same on-state time sequence; trend, not independent reset sample'})
save('noise_analysis.json',{'components':components,'correct_Bonferroni_t_df2_three_outputs':float(t.ppf(1-.05/6,2)),'old_used_t':9.925,'states':noise,'bursts':bursts,'ordinary_ci_assumptions':'All intervals are conditional normal-model intervals. The experiment cannot identify ambient-temperature fractions or pure-camera versus PWM contributions.'})
print('noise done',flush=True)
# Full adopted color vectors; report conditional strip-repeat CI given observed brackets,
# and separately include shared-Ray covariance rather than pretending each d has a new Ray.
adopt=load(B/'models/strip-hsi-command-model.json')['adopted'];adopt['0/0']={'cw':4095,'ww':2240,'r':658,'g':1681,'b':1425}
colors=[]
for label,cmd in sorted(adopt.items(),key=lambda p:tuple(map(int,p[0].split('/')))):
 matching=[p for p in allrows if p['step'].get('c122_request')==label and p['source']=='strip'and p['step'].get('command')==cmd]
 confirms=[p for p in matching if p['step'].get('candidate_role')=='confirmation']; groups=collections.defaultdict(list)
 for p in confirms:groups[p['run']].append(p)
 d=[];diag58=[];idrows=[];rgroups=[];SSE=np.zeros((2,2));dfS=0
 for run,pp in groups.items():
  rays=[p for p in allrows if p['run']==run and p['source']=='ray'and p['primary_valid']];rarr=np.array([p['z']for p in rays]);ref=rarr.mean(axis=0);sa=np.array([p['z']for p in pp]);SSE+=(sa-sa.mean(axis=0)).T@(sa-sa.mean(axis=0));dfS+=len(sa)-1
  for p in pp:
   dd=np.array(p['z'])-ref;d.append(dd);idrows.append({'run':run,'strip_capture_id':p['capture_id'],'Ray_capture_ids':[r['capture_id']for r in rays],'dz':dd,'primary_valid':p['primary_valid'],'feature58_valid_count':p['valid_features58']})
   fs=np.array(p['features58']);fr=np.mean([r['features58']for r in rays],axis=0);sc=np.dot(fs,fr)/np.dot(fs,fs);diag58.append(np.linalg.norm(sc*fs-fr)/np.linalg.norm(fr))
  rgroups.append({'run':run,'n_strip':len(sa),'n_ray':len(rarr),'ray_drift':rarr[-1]-rarr[0],'ray_cov':np.cov(rarr,rowvar=False,ddof=1)if len(rarr)>1 else None,'ray_z':rarr})
 d=np.array(d);n=len(d);mu=d.mean(axis=0);sd=d.std(axis=0,ddof=1);df=n-1
 cond=intervals_iid(d);covS=SSE/dfS if dfS else np.eye(2)*np.nan; contributions=[np.diag(covS)/n];contrib_df=[dfS]
 covmean=covS/n
 for r in rgroups:
  cv=np.array(r['ray_cov']);weight=(r['n_strip']/n)**2/r['n_ray'];covmean+=weight*cv;contributions.append(weight*np.diag(cv));contrib_df.append(r['n_ray']-1)
 var=np.diag(covmean);den=sum(c*c/f for c,f in zip(contributions,contrib_df)if f>0);dfeff=np.divide(var**2,den,out=np.full(2,np.nan),where=den>0);q=t.ppf(.975,dfeff);qj=t.ppf(.9875,dfeff)
 ci=np.stack([mu-q*np.sqrt(var),mu+q*np.sqrt(var)],-1);ciJ=np.stack([mu-qj*np.sqrt(var),mu+qj*np.sqrt(var)],-1)
 colors.append({'target':label,'actual_command':cmd,'total_observations_including_selection':len(matching),'independent_confirmations':n,'independent_confirmation_blocks':len(groups),'mean_dz_confirm_only':mu,'relative_ratio_error_percent':100*np.expm1(mu),'conditional_fixed_bracket_statistics':cond,'shared_Ray_mean_covariance_working':covmean,'shared_Ray_Welch_df':dfeff,'shared_Ray_mean_ci95_working':ci,'shared_Ray_mean_joint95_working':ciJ,'relative_ratio_ci95_working':100*np.expm1(ci),'confirmation_identities':idrows,'Ray_groups':rgroups,'material58_relative_L2_descriptive':{'values':diag58,'median':np.median(diag58)},'qualifier':'Shared-Ray Welch intervals assume independent Gaussian resets and a stationary bracket within each block; not unconditional future sessions and not H/S mapping uncertainty. Fixed-bracket PI omits future reference/session variability.','H_S_ci':None,'H_S_ci_reason':'global map failed; reported orthogonal tangent and long SAT secants have not been locally validated'})
save('color_confirmations.json',{'components':['log_R_over_G','log_B_over_G'],'adopted_target_count_including_S0':len(colors),'reported_validated_samples':17,'actual_confirmed_discrete_target_count':14,'colors':colors})
# Raw limits and actual command search evidence
search={}
for p in allrows:
 label=p['step'].get('c122_request')
 if not label or p['source']!='strip':continue
 e=search.setdefault(label,{'commands':{},'probed_channels':set(),'rows':[]});key=json.dumps(p['step']['command'],sort_keys=True);e['commands'][key]=p['step']['command'];pc=p['step'].get('candidate_probe_channel')
 if pc:e['probed_channels'].add(pc)
 refs=[r for r in allrows if r['run']==p['run']and r['source']=='ray'and r['z']is not None];ref=np.mean([r['z']for r in refs],axis=0)if refs else None
 e['rows'].append({'run':p['run'],'capture_id':p['capture_id'],'tag':p['step'].get('candidate_tag'),'role':p['step'].get('candidate_role'),'command':p['step']['command'],'primary_valid':p['primary_valid'],'frame_status':p['frame_status'],'dz':np.array(p['z'])-ref if p['z']is not None and ref is not None else None,'primary_metrics':p['primary_metrics']})
for label,e in search.items():
 cmds=list(e.pop('commands').values());e['unique_commands_including_rejected']=len(cmds);e['unique_command_list']=cmds;e['probed_channels']=sorted(e['probed_channels']);a=np.array([[c[ch]for ch in w123.CHANNELS]for c in cmds]);e['measured_command_difference_rank']=int(np.linalg.matrix_rank(a-a[0]));e['unique_true_fullscale_face_sets']=sorted({','.join(ch for ch in w123.CHANNELS if c[ch]==4095)for c in cmds})
save('color_search_and_quality.json',search)
# Explicitly recompute the report's H300/S50 orthogonal decomposition (not certify it).
x=next(c for c in colors if c['target']=='300/50');dz=np.array(x['mean_dz_confirm_only']);ur=np.array([.772,.639]);ur/=np.linalg.norm(ur);ut=np.array([-ur[1],ur[0]])
mapdata=load(B/'results/c12-1-mapping-20261005.json')
# Show that orthogonal surrogate is not a coordinate Jacobian. Counterexample J where dot-product loses cross term.
save('map_and_gate_audit.json',{'H300_S50_report_formula_only':{'mean_dz':dz,'radial_axis':ur,'tangent_axis':ut,'radial_pp':float(dz@ur/.01703),'tangential_z':float(dz@ut),'hue_deg_if_using_report_0p0184':float(dz@ut/.0184),'reported_hue_deg':.38,'reported_tangential_z':.007,'not_a_certified_H_S_estimate':True},'global_mapping_original_summary':mapdata['holdout_summary'],'global_mapping_model':mapdata['model_selection'],'global_mapping_records':mapdata['records'],'global_mapping_original_inversions':mapdata['holdout_inversions'],'C124_original_holdout':load(B/'results/c12-4-holdout-analysis-20261012.json'),'structural_cautions':['orthogonal rotation is not inverse of measured [dz/dH,dz/dS] unless columns orthogonal','IDW kNN switching/duplicates can create flat regions/minima; model singularity is not proof of physical low-SAT unidentifiability','np.percentile(errors,95) is empirical quantile, not a 95% confidence upper bound','Two different-Hue distances from white do not test fixed-Hue SAT monotonicity','C124 clamps S0..S25 to S25 and S50..100 to S50, ignoring S0 and H60/S100 endpoints']})
save('environment_and_protocol.json',{'batch1_original':load(C/'results/original/guide12-batch1-derived/b1-exposure-qualification-20260930.json'),'long_original':load(B/'results/w12-4-order-reverification-analysis-20261009.json'),'limits':'All-off point ratios apply only to sampled exposure/settings/time; no replicated environment CI or global ambient guarantee. One DiD per node cannot separate source order and period from protocol; LONG is not steady truth.'})
save('review_integrity.json',{'source_package_hashes':{'base':'3ed20b169cb2cc60470702a05c0e0bfb96f38aa24010b7948e664d271f53d500','completion':'85a61c4ee3a46c28f5922804dcd3f69590c82069477f1f9ad8924627cb52b4bc'},'source_member_counts':{'base':1115,'completion':4999},'raw_physical_rows':len(obs),'primitive_rows_recomputed':len(prim),'matrix':load(MAT),'white_recompute_max_abs_deviation':maxdev,'original_replay_local':load(C/'replay/validation-report.json')if(C/'replay/validation-report.json').exists()else None,'already_acquired_input_sufficiency':True,'historical_unidentifiables':load(C/'MISSING_OR_UNIDENTIFIABLE.json'),'run_note':'No source acquisition files modified; numerical replay artifacts are separate. Portable nonlinear CCT minimization differs from the frozen evaluation by at most 0.0013 K (paired error), 1e-5 mired; Duv agrees to numerical precision. This is far below physical tolerances, but not bitwise replay.'})
print('DONE',flush=True)
