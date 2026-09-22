from analysis_utils import *
from collections import Counter
B=Path('/mnt/data/audit_work');OUT=Path(__file__).parent
pol=load(B/'src/config/hsi/strip-hsi-policy-v2-waiting.json');ids=pol['feature_set']['ids']
ix=[ids.index('block_06::'+c) for c in ('R','G1','G2','B')]
vR=np.array(pol['reference_policy']['ray_within_state_diagonal_variance']);vS=np.array(pol['repeatability_policy']['classes']['sat100_fullscale']['p1_floor_diagonal_variance'])
obs=jlines(B/'supp/OBSERVATIONS.jsonl');omap={o['observation_id']:o for o in obs}
rp=load(B/'supp/replay/w6_w7_long_white_pair_replay.json')['pairs']
cp=load(B/'supp/source-data/guide10-white70-w6/formal-20260920-1230/experiment-spec.json')['analysis_contract']['target_contracts'];contracts={(x['cct'],x['gm']):x for x in cp}
hc={(r['target']['cct'],r['target']['gm']):{'resolved_cct_tolerance_K':25.,'cct_tolerance_mired':1.,'duv_tolerance':.0005} for r in rp['w7']}
mat=[[.9538999795913696,-.27950000762939453,-.12240000069141388],[-.41749998927116394,1.1998000144958496,.24580000340938568],[-.04650000110268593,.17550000548362732,.6047999858856201]]
proxy=WhiteProxy(mat);rng=np.random.default_rng(20260922);N=12000;results=[];center_checks=[]
for group in ('w6','w7','long'):
 for row in rp[group]:
  target=row['target'];key=(target['cct'],target['gm']);c=hc[key] if group=='w7' else contracts[key]
  lim=np.array([c['resolved_cct_tolerance_K'],c['cct_tolerance_mired'],c['duv_tolerance']]);views=[];draws=[];centers=[]
  for label,variance in [('ray',vR),('strip',vS)]:
   o=omap[row[label+'_observation_id']];fv=o['feature_vector']['values'];f=np.array([fv[k] for k in ids]);f/=np.linalg.norm(f);views.append(f)
   center=proxy.evaluate(f[ix],1e6/row[label+'_white_point']['cct_K']);centers.append(center)
   sim=f[ix]+rng.standard_normal((N,4))*np.sqrt(variance[ix]);draws.append(proxy.evaluate(sim,center[1]))
  d=draws[1]-draws[0];central=centers[1]-centers[0];ret=np.array([row['errors'][k] for k in ('cct_K','mired','duv')]);center_checks.append(np.abs(central-ret))
  # Center propagated conditional errors on the original submitted point estimate.
  dc=d-central+ret
  ci=np.quantile(dc,[.025,.975],axis=0);m=views[1]-views[0];cos=float(views[1]@views[0])
  out=dict(group='additional_FAST_mislabeled_LONG' if group=='long' else group,target=target,command=row['diagnostic']['strip_command'],ray_id=row['ray_observation_id'],strip_id=row['strip_observation_id'],errors=row['errors'],limits=dict(zip(('cct_K','mired','duv'),lim.tolist())),legacy_point_pass=bool(np.all(abs(ret)<=lim)),conditional_frozen_model_95_intervals={k:[float(ci[0,i]),float(ci[1,i])] for i,k in enumerate(('cct_K','mired','duv'))},conditional_standard_uncertainties=dict(zip(('cct_K','mired','duv'),np.std(dc,axis=0,ddof=1).tolist())),full_predictive_uncertainty_identified=False,unit58_l2=float(np.linalg.norm(m)),unit58_cosine=cos,optimal_scale_relative_rmse=float(np.sqrt(max(0,1-cos*cos))),whitened58_diagnostic_score=float(np.linalg.norm(m/np.sqrt(vR+vS))))
  # Simultaneous Bonferroni 95% box, conditional on the frozen model, not a new acceptance gate.
  box=np.quantile(dc,[.05/6,1-.05/6],axis=0)
  out['conditional_simultaneous_box_within_legacy_limits']=bool(np.all(box[0]>=-lim)&np.all(box[1]<=lim))
  out['conditional_marginal_95_box_within_legacy_limits']=bool(np.all(ci[0]>=-lim)&np.all(ci[1]<=lim))
  results.append(out)
 summ={}
 for g in sorted(set(x['group'] for x in results)):
  rr=[x for x in results if x['group']==g]
  summ[g]={'count':len(rr),'point_pass_count':sum(x['legacy_point_pass'] for x in rr),'conditional_simultaneous_pass_count':sum(x['conditional_simultaneous_box_within_legacy_limits'] for x in rr),'error_distribution':{k:summary([x['errors'][k] for x in rr]) for k in ('cct_K','mired','duv')},'multipatch_unit58_relative_rmse':summary([x['optimal_scale_relative_rmse'] for x in rr]),'conditional_u_distribution':{k:summary([x['conditional_standard_uncertainties'][k] for x in rr]) for k in ('cct_K','mired','duv')}}
print('center replay max absolute differences',np.max(center_checks,axis=0))
data={'method':{'seed':20260922,'draws_per_source_per_pair':N,'confidence_scope':'conditional propagation of frozen source-specific diagonal 58-feature variance, not total CI or prediction interval','camera_already_in_source_variance':True,'absolute_CIE_validity_claim':False,'marginal_vs_simultaneous':'95% marginal and Bonferroni simultaneous box (95% lower bound); historical 99.73% gates not modified','long_label_correction':'all six legacy long pairs executed FAST 600/120, not LONG 1800/600','covariance_limitation':'frozen diagonal approximation; historical state transfer, source temperature, between-session, common-reference and interpolation effects not included','max_replay_center_difference_K_mired_duv':np.max(center_checks,axis=0).tolist()},'summary':summ,'points':results}
(OUT/'white_per_point_results.json').write_text(json.dumps(data,indent=2,ensure_ascii=False));print(json.dumps(summ,indent=2))
