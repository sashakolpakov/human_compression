"""One fixed Sz32 pair and 248 prescribed third involutions; no ambient census."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,hashlib
SOURCE=Path('/Users/sasha/medusa/research/leemans/phase5_suzuki_check.py')
spec=importlib.util.spec_from_file_location('retained_small_matrices',SOURCE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def need(ok,message):
    if not ok:raise ValueError(message)
F=m.Field(5,37)
def mm(a,b):return F.mm(a,b)
def pair_group(a,b):
    r=mm(a,b);powers=[m.ID];v=r
    while v!=m.ID and len(powers)<=41:
        powers.append(v);v=mm(v,r)
    if v!=m.ID or len(powers) not in [2,5,31,41]:return None
    group=set(powers)|{mm(v,a) for v in powers}
    need(len(group)==2*len(powers),'Exact dihedral pair size')
    return group
def panel(groups,i):
    j,k=[t for t in range(3) if t!=i]
    candidates=set();covered=set()
    for g in sorted(groups[j]):
        if g in covered:continue
        coset=frozenset(mm(g,h) for h in groups[i])
        candidates.add(coset);covered.update(coset&groups[j])
    need(covered==groups[j] and len(candidates)==len(groups[j])//len(groups[i]&groups[j]),'Complete coset partition')
    rows=[]
    for coset in sorted(candidates,key=lambda C:sorted(C)):
        if not coset&groups[k]:continue
        rows.append(dict(elements=sorted(coset),intersection_with_first=sorted(coset&groups[j]),intersection_with_second=sorted(coset&groups[k]),common_representatives=sorted(coset&groups[j]&groups[k])))
    return dict(missing_type=i,base_types=[j,k],candidate_cosets=len(candidates),actual_panel_size=len(rows),standard_chambers=sum(bool(r['common_representatives']) for r in rows),cosets=rows)
def involutions():
    records=[]
    x=1
    for y in range(8):
        u=F.U(x,y);ui=F.mpow(u,3)
        need(mm(u,ui)==mm(ui,u)==m.ID,'Exact root-group inverse')
        for t in range(1,32):
            c=mm(mm(mm(mm(u,m.W),F.U(0,t)),m.W),ui)
            records.append((c,dict(kind='conjugate',x=x,y=y,t=t)))
    need(len(records)==248 and len({c for c,_ in records})==248,'Exactly 248 distinct prescribed matrices')
    need(all(c!=m.ID and mm(c,c)==m.ID for c,_ in records),'Every prescribed matrix an involution')
    return records
def controls():
    need(F.q==32 and F.theta==8 and F.modulus==37,'Exact retained Sz32 field')
    need(all(F.power(t,31)==1 for t in range(1,32)),'Nonzero field elements')
    need(mm(m.W,m.W)==m.ID and F.mpow(F.U(1,1),4)==m.ID,'Elementary retained matrix identities')
    need(pair_group(m.W,m.W) is None,'Degenerate pair excluded')
    return dict(status='PASS_SMALL_SZ32_ARITHMETIC_CONTROL',candidate_family_not_constructed=True,scan_not_run=True)
def main():
    need(len(sys.argv)==1,'Exact fixed-pair target has no target parameters')
    a=m.W;z=F.U(0,3);b=mm(mm(z,m.W),z)
    G0=pair_group(a,b);need(G0 is not None and len(G0)==62,'Fixed retained D62 pair')
    candidates=involutions();log=[];witness=None
    for index,(c,recipe) in enumerate(candidates):
        row=dict(index=index,recipe=recipe)
        G1=pair_group(a,c);G2=pair_group(b,c)
        if G1 is None or G2 is None:
            row['outcome']='nonprime_or_degenerate_pair';log.append(row);continue
        groups=[G0,G1,G2]
        row['orders']=[len(g) for g in groups]
        meets=[len(groups[i]&groups[j]) for i,j in [(0,1),(0,2),(1,2)]]
        if meets!=[2,2,2] or G0&G1&G2!={m.ID}:
            row['outcome']='intersection_filter';row['pair_intersections']=meets;log.append(row);continue
        p=panel(groups,0);row['actual_panel_size']=p['actual_panel_size'];row['standard_chambers']=p['standard_chambers']
        row['outcome']='panel_returned';log.append(row)
        if p['actual_panel_size']!=2:
            witness=dict(index=index,recipe=recipe,involutions=[a,b,c],generators=[[a,b],[a,c],[b,c]],groups=[sorted(g) for g in groups],panels=[p,panel(groups,1),panel(groups,2)])
            break
    matrix_bytes=json.dumps(sorted(c for c,_ in candidates),separators=(',',':')).encode()
    print(json.dumps(dict(status='RETURNED_SZ32_PRESCRIBED_FAMILY_PANEL_SCAN',field=dict(degree=5,modulus=37),fixed_pair=[a,b],candidate_count=248,candidate_matrices_sha256=hashlib.sha256(matrix_bytes).hexdigest(),candidates_considered=len(log),complete_candidate_family=len(log)==248,complete_fixed_pair_scan=False,log=log,witness=witness,ambient_group_enumerated=False,complete_group_classification_claim=False),sort_keys=True))
if __name__=='__main__':
    if sys.argv[1:]==['--controls']:print(json.dumps(controls(),sort_keys=True))
    else:main()
