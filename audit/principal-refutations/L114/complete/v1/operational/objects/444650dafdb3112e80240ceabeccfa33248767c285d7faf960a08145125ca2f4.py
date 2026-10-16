"""The other eight already retained Sz8 shapes: actual panels, no ambient census."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json
SOURCE=Path('/Users/sasha/medusa/research/leemans/phase5_suzuki_check.py')
spec=importlib.util.spec_from_file_location('retained_small_matrices',SOURCE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    need(len(sys.argv)==1,'Eight fixed previously retained markings only')
    F=m.Field(3,11)
    recipes=[(2,5,1,None),(2,7,4,None),(2,13,3,None),(5,7,1,2),(5,13,1,3),(7,7,4,None),(7,13,2,3),(13,13,3,None)]
    results=[]
    for p,p2,x,y in recipes:
        if p==2:a,b,c=m.W,F.U(0,2),F.U(0,x)
        elif p==p2:
            z=F.U(0,2);a,b,c=m.W,F.mm(F.mm(z,m.W),z),F.U(0,x)
        else:
            ratio=F.mul(F.power(y,F.theta),F.power(x,-F.theta))
            lam=F.power(ratio,3)
            need(F.power(lam,F.theta+1)==ratio and lam!=1,'Exact retained diagonal recipe')
            a,b,c=m.W,F.mm(F.h(lam),m.W),F.U(0,x)
        need(all(F.mm(t,t)==m.ID and t!=m.ID for t in [a,b,c]),'Three involutions')
        generators=[[a,b],[b,c],[a,c]] if p==2 else [[a,b],[a,c],[b,c]]
        bounds=[14,2*p,2*p2]
        groups=[F.generated(g,n) for g,n in zip(generators,bounds)]
        need([len(g) for g in groups]==bounds,'Exact retained parabolic orders')
        need([len(groups[i]&groups[j]) for i,j in [(0,1),(0,2),(1,2)]]==[2,2,2],'Exact retained pair intersections')
        need(groups[0]&groups[1]&groups[2]=={m.ID},'Exact retained triple intersection')
        panels=[]
        for i in range(3):
            j,k=[t for t in range(3) if t!=i]
            candidates={frozenset(F.mm(g,h) for h in groups[i]) for g in groups[j]}
            need(len(candidates)==len(groups[j])//len(groups[i]&groups[j]),'All incident cosets enumerated once')
            rows=[]
            for coset in sorted(candidates,key=lambda C:sorted(C)):
                if not coset&groups[k]:continue
                rows.append(dict(elements=sorted(coset),intersection_with_first=sorted(coset&groups[j]),intersection_with_second=sorted(coset&groups[k]),common_representatives=sorted(coset&groups[j]&groups[k])))
            panels.append(dict(missing_type=i,base_types=[j,k],candidate_cosets=len(candidates),actual_panel_size=len(rows),standard_chambers=sum(bool(r['common_representatives']) for r in rows),cosets=rows))
        results.append(dict(recipe=dict(p=p,p_prime=p2,t=2,x=x,y=y),involutions=[a,b,c],generators=generators,groups=[sorted(g) for g in groups],panels=panels))
    print(json.dumps(dict(status='RETURNED_EIGHT_RETAINED_SZ8_MARKING_PANELS',field=dict(degree=3,modulus=11),results=results,excluded_already_checked_marking=[5,5],ambient_group_enumerated=False,complete_group_classification_claim=False),sort_keys=True))
if __name__=='__main__':main()
