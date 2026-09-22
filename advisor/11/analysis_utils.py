"""Read-only numerical helpers for the GUIDE10 evidence audit.
No device, network, or repository mutation is performed.
"""
from pathlib import Path
import json
import numpy as np
from scipy.spatial import cKDTree
from scipy.interpolate import CubicSpline

def load(path):
    text=Path(path).read_text(encoding='utf-8-sig')
    try: return json.loads(text)
    except json.JSONDecodeError:
        obj,end=json.JSONDecoder().raw_decode(text)
        if text[end:] not in ('\\n','\n',''): raise
        return obj

def jlines(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8-sig').splitlines() if line.strip()]

def summary(a):
    a=np.asarray(a,float)
    return dict(n=len(a),mean=float(a.mean()),sd=float(a.std(ddof=1)) if len(a)>1 else None,
                minimum=float(a.min()),q025=float(np.quantile(a,.025)),q25=float(np.quantile(a,.25)),
                median=float(np.median(a)),q75=float(np.quantile(a,.75)),q95=float(np.quantile(a,.95)),
                q975=float(np.quantile(a,.975)),maximum=float(a.max()),
                mae=float(np.abs(a).mean()),abs_median=float(np.median(np.abs(a))),
                abs_p90=float(np.quantile(np.abs(a),.9)),abs_p95=float(np.quantile(np.abs(a),.95)),
                rmse=float(np.sqrt(np.mean(a*a))))

def patch_features(report,statistic='normalized_per_second',accepted_only=True):
    out={}
    for p in report['patches']:
        if not p.get('optimization_eligible',False):continue
        for plane,v in p['planes'].items():
            if plane not in ('R','G1','G2','B'):continue
            if accepted_only and v['quality'].get('accepted') is not True:continue
            out[p['name']+'::'+plane]=float(v['statistics'][statistic]['trimmed_mean'])
    return out

class WhiteProxy:
    """Accelerated numerical replay of the retained approximate CMFs/Planck locus.
    Uses the EXACT retained matrix and approximate CMF formulas, not a new calibration.
    Validate against the submitted replay numbers before using derived intervals.
    """
    def __init__(self,matrix):
        self.inverse=np.linalg.inv(np.asarray(matrix,float))
        w=np.arange(380.,781.,5.)
        def g(mu,l,r):
            t=(w-mu)*np.where(w<mu,l,r)
            return np.exp(-.5*t*t)
        cmf=np.stack([.362*g(442.,.0624,.0374)+1.056*g(599.8,.0264,.0323)-.065*g(501.1,.0490,.0382),
                      .821*g(568.8,.0213,.0247)+.286*g(530.9,.0613,.0322),
                      1.217*g(437.,.0845,.0278)+.681*g(459.,.0385,.0725)],axis=1)
        weights=np.full(len(w),5.);weights[[0,-1]]=2.5
        self.mired=np.linspace(40.,1000.,48001)
        w=w*1e-9
        xyz=[]
        for m in np.array_split(self.mired,20):
            spec=1./(w[None,:]**5*np.expm1(.01438776877*m[:,None]/(1e6*w[None,:])))
            xyz.append(spec@(cmf*weights[:,None]))
        xyz=np.concatenate(xyz);xy=xyz[:,:2]/xyz.sum(axis=1)[:,None]
        self.locus=self.xy_uv(xy)
        self.tree=cKDTree(self.locus)
        self.spline=CubicSpline(self.mired,self.locus)
    @staticmethod
    def xy_uv(xy):
        x,y=xy[...,0],xy[...,1];den=-2*x+12*y+3
        return np.stack([4*x/den,6*y/den],axis=-1)
    def evaluate(self,rgba,initial_mired=None):
        a=np.asarray(rgba,float) # R,G1,G2,B; global scale cancels exactly
        green=(a[...,1]+a[...,2])/2
        neutral=np.stack([a[...,0]/green,np.ones_like(green),a[...,3]/green],axis=-1)
        xyz=neutral@self.inverse.T;xy=xyz[...,:2]/xyz.sum(axis=-1)[...,None]
        uv=self.xy_uv(xy)
        if initial_mired is None:
            _,i=self.tree.query(uv);m=self.mired[i]
        else:
            m=np.broadcast_to(np.asarray(initial_mired,float),uv.shape[:-1]).copy()
        for _ in range(3):
            p=self.spline(m);d=self.spline(m,1);dd=self.spline(m,2);e=p-uv
            step=np.sum(e*d,axis=-1)/(np.sum(d*d,axis=-1)+np.sum(e*dd,axis=-1))
            m=np.clip(m-step,40.,1000.)
        p=self.spline(m);d=-self.spline(m,1);e=uv-p
        sign=np.where(d[...,0]*e[...,1]-d[...,1]*e[...,0]>=0,1.,-1.)
        return np.stack([1e6/m,m,sign*np.linalg.norm(e,axis=-1)],axis=-1)
