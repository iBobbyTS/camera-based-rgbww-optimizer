from analysis_utils import *
from scipy.stats import t,chi2
from collections import defaultdict
B=Path('/mnt/data/audit_work');OUT=Path(__file__).parent
mat=[[.9538999795913696,-.27950000762939453,-.12240000069141388],[-.41749998927116394,1.1998000144958496,.24580000340938568],[-.04650000110268593,.17550000548362732,.6047999858856201]];proxy=WhiteProxy(mat);res=[]
for day,folder in [('D1','p1-d1'),('D2','p1-d2-cross-day')]:
 a=load(B/'delta/source-data'/folder/'analysis.json')
 for source in ['ray','strip']:
  rp=a['repeatability'][source];groups=defaultdict(dict)
  for o in rp['collection']['observations']:
   if o['feature_id'].startswith('block_06::'):groups[o['report_id']][o['feature_id'].split('::')[1]]=o['value']
  order=sorted(groups);x=np.array([[groups[g][c] for c in ['R','G1','G2','B']] for g in order]);w=proxy.evaluate(x);green=(x[:,1]+x[:,2])/2;lc=np.stack([np.log(x[:,0]/green),np.log(x[:,3]/green)],axis=1)
  def est(vals):
   mean=float(np.mean(vals));sd=float(np.std(vals,ddof=1));n=len(vals);return dict(n=n,mean=mean,sd=sd,mean95CI=[mean-t.ppf(.975,n-1)*sd/np.sqrt(n),mean+t.ppf(.975,n-1)*sd/np.sqrt(n)],sd95CI=[np.sqrt((n-1)*sd*sd/chi2.ppf(.975,n-1)),np.sqrt((n-1)*sd*sd/chi2.ppf(.025,n-1))],conditional_next_observation95PI=[mean-t.ppf(.975,n-1)*sd*np.sqrt(1+1/n),mean+t.ppf(.975,n-1)*sd*np.sqrt(1+1/n)])
  res.append(dict(day=day,source=source,report_ids=order,raw_feature_CV=rp['summary']['coefficient_of_variation'],metrics={k:est(v) for k,v in zip(['cct_K','mired','duv','log_R_over_G','log_B_over_G'],list(w.T)+list(lc.T))},log_chroma_covariance=np.cov(lc.T).tolist(),white_proxy_values=w.tolist()))
p2=load(B/'delta/source-data/p2-five-channel-basis/basis-analysis.json');p3=load(B/'delta/source-data/p3-additivity/basis-validation.json')
result={'method':{'P1_estimand':'same-source repeated 5600K/GM100 and fixed strip command, 5 independent paired repeats in each historical day; no camera-only attribution','interval_assumption':'iid approximately normal within each five-observation group; Student t mean and predictive interval; chi-square sd interval; n=5 cannot validate normality or long-term stationarity','do_not_pool_days':True,'unknown_total_variance':'observed within-state fluctuations already include camera plus source and protocol; cannot add a separate camera variance again','P3':'model discrepancy distribution across 24 test commands, not stochastic noise or physical gamut'},'p1_groups':res,'p2_summary':{k:v for k,v in p2.items() if k in ['status','identifiability','repeatability_summary','level_shape_comparison','basis_identifiability']},'p3_summary':{k:v for k,v in p3.items() if k in ['status','aggregate','aggregate_summary','summary','correlations']}}
(OUT/'noise_and_model_diagnostics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,indent=2)[:9000]);print(p2.keys());print(p3.keys())
