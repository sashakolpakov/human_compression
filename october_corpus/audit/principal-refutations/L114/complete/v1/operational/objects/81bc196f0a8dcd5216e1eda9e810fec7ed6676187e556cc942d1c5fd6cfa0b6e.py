"""One retained Sz8 marking; literal panels, with no ambient group enumeration."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json
SOURCE=Path('/Users/sasha/medusa/research/leemans/phase5_suzuki_check.py')
spec=importlib.util.spec_from_file_location('retained_small_matrices',SOURCE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def need(ok,message):
    if not ok:raise ValueError(message)
def main():
    need(len(sys.argv)==1,'One fixed saved marking')
    F=m.Field(3,11)
    z=F.U(0,2)
    a,b,c=m.W,F.mm(F.mm(z,m.W),z),F.U(0,1)
    need(all(F.mm(x,x)==m.ID and x!=m.ID for x in [a,b,c]),'Three involutions')
    generators=[[a,b],[a,c],[b,c]]
    bounds=[14,10,10]
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
        panels.append(dict(missing_type=i,base_types=[j,k],candidate_cosets=len(candidates),actual_panel_size=len(rows),standard_chambers=sum(bool(x['common_representatives']) for x in rows),cosets=rows))
    print(json.dumps(dict(status='RETURNED_ONE_SAVED_SZ8_MARKING_PANELS',field=dict(degree=3,modulus=11),involutions=[a,b,c],generators=generators,groups=[sorted(g) for g in groups],panels=panels,ambient_group_enumerated=False,complete_group_classification_claim=False),sort_keys=True))
if __name__=='__main__':main()
