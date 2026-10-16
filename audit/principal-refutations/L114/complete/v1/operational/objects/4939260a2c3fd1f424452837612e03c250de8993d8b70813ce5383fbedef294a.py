"""One fixed involution pair and 455 explicit third involutions; no ambient census."""
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
F=m.Field(3,11)
def mm(a,b):return F.mm(a,b)
def pair_group(a,b):
    r=mm(a,b);powers=[m.ID];v=r
    while v!=m.ID and len(powers)<=13:
        powers.append(v);v=mm(v,r)
    if v!=m.ID or len(powers) not in [2,5,7,13]:return None
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
    for t in range(1,8):records.append((F.U(0,t),dict(kind='center',t=t)))
    for x in range(8):
        for y in range(8):
            u=F.U(x,y);ui=F.mpow(u,3)
            need(mm(u,ui)==mm(ui,u)==m.ID,'Exact root-group inverse')
            for t in range(1,8):
                c=mm(mm(mm(mm(u,m.W),F.U(0,t)),m.W),ui)
                records.append((c,dict(kind='conjugate',x=x,y=y,t=t)))
    need(len(records)==455 and len({c for c,_ in records})==455,'Exactly 455 distinct prescribed matrices')
    need(all(c!=m.ID and mm(c,c)==m.ID for c,_ in records),'Every prescribed matrix an involution')
    return records
def controls():
    # This only reads the already accepted (5,5) marking, never calls involutions().
    d=json.loads(Path('/Users/sasha/medusa/research/leemans/geometry/suzuki_incidence/panel_actual01/stdout').read_text())
    a,b,c=[tuple(x) for x in d['involutions']]
    groups=[pair_group(a,b),pair_group(a,c),pair_group(b,c)]
    need([sorted(g) for g in groups]==[[tuple(x) for x in g] for g in d['groups']],'Accepted fixture groups')
    p=panel(groups,0)
    need(json.loads(json.dumps(p))==d['panels'][0],'Accepted fixture panel')
    need(pair_group(a,a) is None,'Degenerate pair excluded')
    return dict(status='PASS_SMALL_ACCEPTED_FIXTURE_CONTROL',involution_set_not_constructed=True,scan_not_run=True)
def main():
    need(len(sys.argv)==1,'Exact fixed-pair target has no target parameters')
    a=m.W;z=F.U(0,2);b=mm(mm(z,m.W),z)
    G0=pair_group(a,b);need(G0 is not None and len(G0)==14,'Fixed accepted D14 pair')
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
    print(json.dumps(dict(status='RETURNED_FIXED_PAIR_PANEL_SCAN',field=dict(degree=3,modulus=11),fixed_pair=[a,b],candidate_count=455,candidate_matrices_sha256=hashlib.sha256(matrix_bytes).hexdigest(),candidates_considered=len(log),complete_fixed_pair_scan=len(log)==455,log=log,witness=witness,ambient_group_enumerated=False,complete_group_classification_claim=False),sort_keys=True))
if __name__=='__main__':
    if sys.argv[1:]==['--controls']:print(json.dumps(controls(),sort_keys=True))
    else:main()
