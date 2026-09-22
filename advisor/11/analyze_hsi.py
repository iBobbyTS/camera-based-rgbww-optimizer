from analysis_utils import *
import sys
from collections import defaultdict
from scipy.optimize import least_squares
sys.path.insert(0,'/mnt/data/audit_work/src/src')
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold,_accepted_features,_feature_center,_pooled_zero_direction
B=Path('/mnt/data/audit_work');OUT=Path(__file__).parent
pol=load(B/'src/config/hsi/strip-hsi-policy-v2-waiting.json');ids=pol['feature_set']['ids']
vR=np.array(pol['reference_policy']['ray_within_state_diagonal_variance']);vS=np.array(pol['repeatability_policy']['classes']['sat100_fullscale']['p1_floor_diagonal_variance']);den=np.sqrt(vR+vS)
p6=B/'supp/source-data/ray-hsi-manifold-p6';cap=jlines(p6/'captures.jsonl');groups=defaultdict(list)
for c in cap:
 if c.get('source')=='ray' and c.get('ray_mode')=='hsi':
  st=c['ray_state'];f=p6/'measurements'/Path(c['capture']['patch_statistics']).name
  groups[(int(st['hue']),int(st['sat']))].append(_accepted_features(load(f)))
centers={k:_feature_center(v) for k,v in groups.items()};z,zsc=_pooled_zero_direction({h:centers[h,0] for h in range(0,360,60)})
model=RayHsiManifold(config={},nodes={k:v for k,v in centers.items() if k[1]!=0},zero_direction=z,zero_scales=zsc,repeatability_three_sigma=load(p6/'ray-hsi-analysis.json')['repeatability']['three_sigma_proxy'])
S=np.array([0,5,20,50,80,95,100.]);grid=np.array([[[model._node(h,int(s))[i] for i in ids] for s in S] for h in range(0,360,30)])

def unit_jac(t,dt):
 n=np.linalg.norm(t);u=t/n
 return u,(dt-u[:,None]*(u@dt)[None,:])/n

def cell_fun(x,i,j):
 a,b=x;g00=grid[i,j];g10=grid[(i+1)%12,j];g01=grid[i,j+1];g11=grid[(i+1)%12,j+1]
 t=(1-a)*(1-b)*g00+a*(1-b)*g10+(1-a)*b*g01+a*b*g11
 dt=np.stack([(1-b)*(g10-g00)+b*(g11-g01),(1-a)*(g01-g00)+a*(g11-g10)],axis=1)
 return unit_jac(t,dt)

def project(cand,var,nrepeat=1):
 sol=[]
 for i in range(12):
  for j in range(6):
   def fun(x):return (cell_fun(x,i,j)[0]-cand)/den
   def jac(x):return cell_fun(x,i,j)[1]/den[:,None]
   rr=least_squares(fun,[.5,.5],jac=jac,bounds=([0.,0.],[1.,1.]),gtol=1e-9,xtol=1e-10,ftol=1e-10,max_nfev=120)
   sol.append((float(np.linalg.norm(rr.fun)),i,j,rr.x,rr))
 sol.sort(key=lambda z:z[0]);score,i,j,x,res=sol[0];h=(30*i+30*x[0])%360;s=S[j]+(S[j+1]-S[j])*x[1]
 pred,dt=cell_fun(x,i,j);J=dt/np.array([30.,S[j+1]-S[j]])[None,:];Jw=J/den[:,None]
 # Finite-difference full objective Hessian handles curvature under misspecification.
 # Conditional delta-method intervals are descriptive only, never usable as equivalence.
 eps=1e-4;H=np.empty((2,2))
 def grad(hs):
  xx=x+hs/np.array([30.,S[j+1]-S[j]]);t,d=cell_fun(xx,i,j);jj=d/np.array([30.,S[j+1]-S[j]])[None,:]
  return jj.T@((t-cand)/(den*den))
 for q in range(2):
  delta=np.zeros(2);delta[q]=eps;H[:,q]=(grad(delta)-grad(-delta))/(2*eps)
 H=(H+H.T)/2
 A=np.linalg.pinv(H)@(J.T/(den*den));cov=A@np.diag(var/nrepeat)@A.T;sd=np.sqrt(np.maximum(0,np.diag(cov)))
 ci=[[float(h-1.96*sd[0]),float(h+1.96*sd[0])],[max(0.,float(s-1.96*sd[1])),min(100.,float(s+1.96*sd[1]))]]
 alternatives=[]
 for sc,ii,jj,xx,_ in sol:
  hh=(ii*30+xx[0]*30)%360;ss=S[jj]+xx[1]*(S[jj+1]-S[jj])
  if abs((hh-h+180)%360-180)>2 or abs(ss-s)>2:
   alternatives.append({'hue':float(hh),'sat':float(ss),'score':sc});break
 return dict(nearest_hue=float(h),nearest_sat=float(s),whitened_distance_to_historical_manifold=score,unit58_distance=float(np.linalg.norm(cand-pred)),conditional_fixed_manifold_projection_sd=sd.tolist(),conditional_fixed_manifold_projection_95_intervals=ci,interval_scope='delta-method local projection of source measurement noise only; NOT valid Ray-equivalent coverage interval',alternative_separated_solution=alternatives,cell=[i,j],on_cell_boundary=bool(np.any((x<1e-5)|(x>1-1e-5))),hessian_eigenvalues=np.linalg.eigvalsh(H).tolist())
obs=jlines(B/'supp/OBSERVATIONS.jsonl');labels=['guide9-h120-s50-best','guide9-h120-s25-best','guide9-h0-s0-best','guide9-h300-s50-best'];results=[]
for lab in labels:
 oo=[o for o in obs if o['source_label']==lab]
 roots=sorted(set(o['root'] for o in oo));print(lab,roots,flush=True)
 # H120/S50 folder includes two roots; choose latest successful retry2 only.
 if lab=='guide9-h120-s50-best':oo=[o for o in oo if '193335' in o['root']]
 record={'label':lab,'root':list(sorted(set(o['root'] for o in oo))),'sources':{}}
 for source,var in [('ray',vR),('strip',vS)]:
  subset=[o for o in oo if o['source_id']==source and o['feature_vector'].get('values')]
  aa=np.array([[o['feature_vector']['values'][i] for i in ids] for o in subset]);aa=aa/np.linalg.norm(aa,axis=1)[:,None];mean=aa.mean(axis=0);mean/=np.linalg.norm(mean)
  result=project(mean,var,len(subset));result.update(observation_ids=[o['observation_id'] for o in subset],n=len(subset),requested_target=subset[0]['target'],command=subset[0]['command']);record['sources'][source]=result
 record['valid_Ray_equivalent_or_gamut_claim']=False;record['reason']='no demonstrated current-to-P6 transfer and large orthogonal multi-material residual; nearest projection is not a valid saturation ceiling'
 results.append(record);print(record,flush=True)
(OUT/'hsi_projection_diagnostics.json').write_text(json.dumps({'method':{'P6_center':'per-feature median; SAT0 pooled median unit direction on original common feature space; bilinear raw-feature interpolation then unit-normalize ordered58','global_search':'bounded solve of all 72 piecewise cells, analytic residual Jacobian','weight':'frozen Sigma_R+Sigma_S diagonal; no covariance inflation','intervals':'conditional fixed-manifold projection only, exclude manifold/session/model uncertainty','current_best_repeat_count_in_each_confirmation_root':2,'strict_equivalence_claim':False},'results':results},indent=2,ensure_ascii=False))
