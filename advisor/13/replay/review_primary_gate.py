"""Supplemental primary-vs-secondary review, no devices / network.
Usage: python review_primary_gate.py BASE COMPLETION OUTPUT
Requires numpy, scipy. Run review_guide12.py first.
"""
import json,sys,math,collections
from pathlib import Path
import numpy as np
from scipy.stats import t,chi2
from scipy.optimize import linprog
B,C,O=map(Path,sys.argv[1:4]); O.mkdir(parents=True,exist_ok=True)
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def jl(p):return [json.loads(s)for s in p.read_text(encoding='utf-8').splitlines()if s.strip()]
def clean(a):
 if isinstance(a,np.ndarray):return clean(a.tolist())
 if isinstance(a,np.generic):return a.item()
 if isinstance(a,dict):return {k:clean(v)for k,v in a.items()}
 if isinstance(a,(tuple,list)):return [clean(v)for v in a]
 return a
def save(name,a):(O/name).write_text(json.dumps(clean(a),ensure_ascii=False,indent=2),encoding='utf-8')
obs=jl(C/'OBSERVATIONS_COMPLETE.jsonl'); rows=[];n2=[];iso=collections.Counter();ap=collections.Counter()
for o in obs:
 step=o.get('plan_step')or{};cap=o.get('capture')or{};inner=cap.get('capture')or{}
 iso[str(inner.get('iso'))]+=1;ap[str(inner.get('aperture'))]+=1
 if not (step.get('n2_state_key','').startswith('color')or('guide12-c122/'in o['run_alias']and o.get('source_id')=='strip')):continue
 p=B/'measurements'/o['run_alias']/(o['capture_id']+'.patch-statistics.json')
 if not p.exists():p=C/'measurements'/o['run_alias']/(o['capture_id']+'.patch-statistics.json')
 st=load(p);q=next(x for x in st['patches']if x['index']==6)['planes'];pl=('R','G1','G2','B')
 qs={k:q[k]['quality']['status']for k in pl};v={k:q[k]['statistics']['normalized_per_second']['trimmed_mean']for k in pl};g=(v['G1']+v['G2'])/2
 z=[math.log(v['R']/g),math.log(v['B']/g)]if min(v.values())>0 else None
 r={'run':o['run_alias'],'capture_id':o['capture_id'],'source':o.get('source_id'),'target':step.get('c122_request',step.get('n2_state_key')),'tag':step.get('c122_tag'), 'primary_quality':qs,'primary_valid':all(x=='accepted'for x in qs.values()),'global_quality':(cap.get('direct_quality')or{}).get('status'),'source_stats':str(p.relative_to(B)if p.is_relative_to(B)else p.relative_to(C)),'command':step.get('command'),'z':z,'cycle':step.get('n2_cycle_index'),'burst_role':step.get('n2_burst_role')}
 (n2 if step.get('n2_state_key','').startswith('color')else rows).append(r)
excluded=[r for r in rows if r['global_quality']!='pass'and r['primary_valid']]
search=load(O/'color_search_and_quality.json');hulls={}
for lab in ('0/100','120/100','180/100','240/100','300/100'):
 valid=[r for r in search[lab]['rows']if r['primary_valid']and max(r['command'].values())==4095 and r['dz']is not None]
 Z=np.array([r['dz']for r in valid]);lp=linprog(np.zeros(len(Z)),A_eq=np.vstack((Z.T,np.ones(len(Z)))),b_eq=[0,0,1],bounds=(0,None),method='highs')
 hulls[lab]={'target_inside_convex_hull_of_observed_z_residuals':bool(lp.success),'weights_if_feasible':[{'run':valid[i]['run'],'capture_id':valid[i]['capture_id'],'tag':valid[i]['tag'],'weight':float(w)}for i,w in enumerate(lp.x)if w>1e-6]if lp.success else [],'not_a_physical_gamut_result':'Convex combinations in log-ratio space are only candidate-design hints; strip command response is nonlinear and bracket centers differ. No averaged PWM is validated by this computation.'}
# Recover only the preselected N2 sessions and the primary-valid BLUE state.
roots=['formal-n2-session1-r5','formal-n2-session2-r2','formal-n2-session3']; pairs=[]
for si,run in enumerate(roots,1):
 for cyc in (1,2):
  r=[x for x in n2 if x['run'].endswith('/'+run)and x['target']=='color_blue'and x['cycle']==cyc]
  rr=[x for x in r if x['source']=='ray'];ss=[x for x in r if x['source']=='strip']
  if len(rr)!=1 or len(ss)!=1:raise ValueError((run,cyc,len(rr),len(ss)))
  if not rr[0]['primary_valid']or not ss[0]['primary_valid']:raise ValueError('primary invalid')
  pairs.append({'session':si,'cycle':cyc,'Ray':rr[0],'strip':ss[0],'dz':np.array(ss[0]['z'])-np.array(rr[0]['z'])})
a=np.array([p['dz']for p in pairs]).reshape(3,2,2);means=a.mean(axis=1);mu=means.mean(axis=0);sd=means.std(axis=0,ddof=1);within=((a-means[:,None,:])**2).sum(axis=(0,1))/3;tau=np.maximum(0,sd**2-within/2);q=t.ppf(.975,2)
blue={'pairs':pairs,'session_means':means,'mean_dz':mu,'session_mean_ci95':np.stack([mu-q*sd/np.sqrt(3),mu+q*sd/np.sqrt(3)],-1),'next_session_mean_pi95':np.stack([mu-q*sd*np.sqrt(1+1/3),mu+q*sd*np.sqrt(1+1/3)],-1),'within_cycle_sd':np.sqrt(within),'within_cycle_sd_ci95':np.stack([np.sqrt(3*within/chi2.ppf(.975,3)),np.sqrt(3*within/chi2.ppf(.025,3))],-1),'between_session_sd_moment':np.sqrt(tau),'assumptions':'Conditional Gaussian/exchangeable session means, 3 sessions only. Not a Hue/SAT or spectral-gamut claim. Reclassification pertains ONLY to primary block_06; original 58-feature near-noise failure remains.'}
save('primary_secondary_gate_audit.json',{'rows_checked':len(rows),'original_global_pass':sum(r['global_quality']=='pass'for r in rows),'primary_valid_global_rejected_count':len(excluded),'primary_valid_global_rejected':excluded,'C122_rows':rows,'N2_color_rows':n2,'N2_blue_recovered_primary_analysis':blue,'observed_z_convex_hull_diagnostic_only':hulls,'metadata_recovery':{'nested_capture_iso_counts':dict(iso),'nested_capture_aperture_counts':dict(ap),'note':'These are acquisition metadata; implicit auto is not a measured aperture. They do not prove fixed physical aperture or RAW EXIF ISO independently.'},'scientific_disposition':'Use existing primary-valid frames in a NEW derived primary analysis. Do not alter historic all-feature verdicts. Do not claim entire sensor exposure linearity from accepted block statistics alone.'})
print('Excluded-but-primary-valid',len(excluded),'blue',clean(blue['mean_dz']),clean(blue['session_mean_ci95']))
