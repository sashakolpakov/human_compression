#!/usr/bin/env python3
"""Independent finite checks of the two affine markings and lattice decompositions.
Standard library only; imports no author helper or saved mathematical output.
This is a bounded check, not a substitute for the uniform written proof.
"""
import argparse, hashlib, itertools, json
from pathlib import Path

ID=(1,0,0,1)
A=(-1,0,0,1)
B=(0,1,1,0)
C=(1,0,0,-1)

def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def mm(a,b): return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
def mv(a,v): return (a[0]*v[0]+a[1]*v[1],a[2]*v[0]+a[3]*v[1])

class Affine:
    def __init__(self,q,diagonal):
        self.q=q; self.diagonal=diagonal; self.one=(ID,(0,0))
    def red(self,v):
        x,y=v; q=self.q
        return (x%q,(y-(x//q)*q)%(2*q)) if self.diagonal else (x%q,y%q)
    def elt(self,m,v): return (m,self.red(v))
    def mul(self,x,y):
        w=mv(x[0],y[1]); return (mm(x[0],y[0]),self.red((x[1][0]+w[0],x[1][1]+w[1])))
    def inv(self,x):
        m=x[0]; t=(m[0],m[2],m[1],m[3]);v=mv(t,x[1]);return self.elt(t,(-v[0],-v[1]))
    def conj(self,x,y):return self.mul(self.mul(self.inv(y),x),y)
    def pow(self,x,n):
        z=self.one
        for _ in range(n): z=self.mul(z,x)
        return z
    def word(self,*xs):
        z=self.one
        for x in xs:z=self.mul(z,x)
        return z
    def comm(self,x,y):return self.word(self.inv(x),self.inv(y),x,y)
    def order(self,x):
        z=self.one
        for n in range(1,16*self.q*self.q+1):
            z=self.mul(z,x)
            if z==self.one:return n
        raise RuntimeError('order did not terminate')
    def subgroup(self,gs):
        gs=list(gs); found={self.one};todo=[self.one]
        for x in todo:
            for g in gs:
                y=self.mul(x,g)
                if y not in found:found.add(y);todo.append(y)
        return found

def run(q,diagonal,marking):
    f=Affine(q,diagonal)
    a=f.elt(A,(0,0) if marking=='A3' else (1,0))
    b=f.elt(B,(0,0));c=f.elt(C,(0,1) if marking=='A3' else (0,0))
    gs=(a,b,c);g=f.subgroup(gs); expected=(16 if diagonal else 8)*q*q
    require(len(g)==expected,'full affine group order')
    require(all(f.order(x)==2 for x in gs),'involutions')
    require([f.order(f.mul(a,b)),f.order(f.mul(b,c)),f.order(f.mul(a,c))]==[4,4,2],'pair orders')
    if diagonal:
        xgs=(f.conj(b,a),f.conj(b,c));ygs=(b,f.conj(b,f.mul(a,c)));jgs=(a,c)
    else:
        xgs=(a,f.conj(c,b));ygs=(f.conj(a,b),c);jgs=(b,)
    x=f.subgroup(xgs);y=f.subgroup(ygs);j=f.subgroup(jgs)
    require(len(x)==len(y)==2*q,'two exact factor orders')
    require(f.order(f.mul(*xgs))==f.order(f.mul(*ygs))==q,'rotation orders')
    require(all(f.comm(u,v)==f.one for u in xgs for v in ygs),'cross commutation')
    require(x&y=={f.one},'factor intersection')
    xy={f.mul(u,v) for u in x for v in y}
    require(xy&j=={f.one},'complement intersection')
    require(all(f.conj(u,v) in xy for u in xgs+ygs for v in jgs),'complement normalization')
    require({f.mul(u,v) for u in xy for v in j}==g,'full internal semidirect product')
    require(all({f.conj(u,v) for u in x}==y for v in jgs),'complement exchanges factors')
    old=f.subgroup((b,f.conj(b,a)))
    if diagonal:require(len(old)==4,'printed wrong pair has constant order four')
    # Exact marked change between A3 and N009: reverse endpoints then conjugate by b.
    aa=f.elt(A,(0,0));bb=f.elt(B,(0,0));cc=f.elt(C,(0,1))
    require((f.conj(cc,bb),bb,f.conj(aa,bb))==(f.elt(A,(1,0)),b,f.elt(C,(0,0))),'N009 marking bridge')
    if marking=='A3':
        h=f.comm(f.pow(f.mul(a,b),2),c)
        k=f.comm(f.pow(f.mul(a,b),2),f.pow(f.mul(b,c),2))
        require(h==f.elt(ID,(0,-2)) and k==f.elt(ID,(-2,-2)),'source parity words')
    else:
        require(f.word(a,b,c,b)==f.elt(ID,(1,0)),'N009 first translation')
        require(f.pow(f.word(a,b,c),2)==f.elt(ID,(1,1)),'N009 diagonal translation')
    # Inspect all 64 intersections whenever this is a valid square-map C-group.
    checks=0
    if q>=2:
        pars=[f.subgroup(gs[i] for i in range(3) if mask>>i&1) for mask in range(8)]
        for u,v in itertools.product(range(8),repeat=2):
            require(pars[u]&pars[v]==pars[u&v],'affine full IP');checks+=1
    center={u for u in g if all(f.comm(u,v)==f.one for v in gs)}
    if marking=='N009' and q&(q-1)==0:
        ab2=f.pow(f.mul(a,b),2);bc2=f.pow(f.mul(b,c),2)
        if diagonal:
            expected_center=f.subgroup((f.mul(a,c),ab2,bc2)) if q==1 else f.subgroup((f.pow(f.word(a,b,c,b),q),))
        elif q>=2:
            expected_center=f.subgroup((ab2,bc2)) if q==2 else f.subgroup((f.pow(f.word(a,b,c),q),))
        else:expected_center=None
        if expected_center is not None:require(center==expected_center,'complete source center formula')
    return dict(q=q,lattice='diagonal' if diagonal else 'square',marking=marking,order=len(g),factor_orders=[len(x),len(y)],complement_order=len(j),center_order=len(center),actual_IP_pairs=checks,printed_pair_order=len(old) if diagonal else None)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists() or a.output.is_symlink():raise SystemExit('Refusing existing output')
    rows=[run(q,d,m) for q in range(1,9) for d in (False,True) for m in ('A3','N009')]
    report=dict(status='PASS_bounded_independent_arithmetic',script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=rows,total_cases=len(rows),all_actual_IP_pairs=sum(r['actual_IP_pairs'] for r in rows),range='q=1..8, both lattices and both marked affine conventions',uniform_proof=False,author_imports=False,source_PDF_required=False)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps({k:report[k] for k in ('status','total_cases','all_actual_IP_pairs')}))
if __name__=='__main__':main()
