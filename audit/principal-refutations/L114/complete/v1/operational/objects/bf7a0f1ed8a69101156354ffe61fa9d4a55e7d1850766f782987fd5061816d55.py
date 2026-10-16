"""Independent panel reader for eight returned recipes; no acquisition or search."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,copy
PRIOR=Path('/Users/sasha/medusa/research/leemans/geometry/suzuki_incidence/prime_patterns/panel_check.py')
spec=importlib.util.spec_from_file_location('accepted_f8_reader',PRIOR)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
need=v.need;mm=v.mm
RECIPES=[(2,5,1,None),(2,7,4,None),(2,13,3,None),(5,7,1,2),(5,13,1,3),(7,7,4,None),(7,13,2,3),(13,13,3,None)]
def power(a,n):
    if n<0:n%=7
    r=1
    for _ in range(n):r=v.mul(r,a)
    return r

def diagonal(t):
    return tuple(power(t,k) if i==j else 0 for i,k in enumerate([5,1,-1,-5]) for j in range(4))

def verify(d):
    need(d['status']=='RETURNED_EIGHT_RETAINED_SZ8_MARKING_PANELS','Actual eight-marking scope')
    need(d['field']=={'degree':3,'modulus':11},'Exact field')
    need(d['excluded_already_checked_marking']==[5,5],'Previously accepted marking excluded')
    need(d['ambient_group_enumerated'] is False and d['complete_group_classification_claim'] is False,'No ambient census claim')
    need(len(d['results'])==8,'Exactly eight returned recipes')
    reports=[]
    for row,(p,p2,x,y) in zip(d['results'],RECIPES):
        need(row['recipe']==dict(p=p,p_prime=p2,t=2,x=x,y=y),'Exact retained recipe')
        if p==2:a,b,c=v.W,v.z(2),v.z(x)
        elif p==p2:a,b,c=v.W,mm(mm(v.z(2),v.W),v.z(2)),v.z(x)
        else:
            ratio=v.mul(power(y,4),power(x,-4));lam=power(ratio,3)
            need(power(lam,5)==ratio and lam!=1,'Retained scalar recipe')
            a,b,c=v.W,mm(diagonal(lam),v.W),v.z(x)
        need([v.matrix(r) for r in row['involutions']]==[a,b,c],'Exact three matrices')
        need(all(t!=v.ID and mm(t,t)==v.ID for t in [a,b,c]),'Three involutions')
        gens=[[a,b],[b,c],[a,c]] if p==2 else [[a,b],[a,c],[b,c]]
        need([[v.matrix(t) for t in r] for r in row['generators']]==gens,'Exact generators')
        need(len(row['groups'])==3,'Three parabolics')
        G=[v.group(r,g,n) for r,g,n in zip(row['groups'],gens,[14,2*p,2*p2])]
        need([len(G[i]&G[j]) for i,j in [(0,1),(0,2),(1,2)]]==[2,2,2] and G[0]&G[1]&G[2]=={v.ID},'Exact intersections')
        panels=[]
        for i in range(3):
            j,k=[t for t in range(3) if t!=i]
            candidates={frozenset(mm(t,h) for h in G[i]) for t in G[j]}
            need(len(candidates)==len(G[j])//len(G[i]&G[j]),'Complete candidate partition')
            records=[]
            for C in sorted(candidates,key=lambda z:sorted(z)):
                if not C&G[k]:continue
                records.append(dict(elements=[list(t) for t in sorted(C)],intersection_with_first=[list(t) for t in sorted(C&G[j])],intersection_with_second=[list(t) for t in sorted(C&G[k])],common_representatives=[list(t) for t in sorted(C&G[j]&G[k])]))
            panels.append(dict(missing_type=i,base_types=[j,k],candidate_cosets=len(candidates),actual_panel_size=len(records),standard_chambers=sum(bool(r['common_representatives']) for r in records),cosets=records))
        need(row['panels']==panels,'Exact actual coset sets and intersections')
        reports.append(dict(parameters=[p,p2],orders=[len(g) for g in G],actual_panel_sizes=[r['actual_panel_size'] for r in panels],standard_chambers=[r['standard_chambers'] for r in panels],nonstandard_cosets=[sum(not c['common_representatives'] for c in r['cosets']) for r in panels]))
    return dict(status='PASS_EIGHT_RETURNED_RETAINED_MARKINGS',markings=reports,ambient_group_enumerated=False,general_thinness_proved=False,source_application='A distinct mathematical source application is required; this reader checks exact subgroup and panel data only')

def controls(d):
    tests=[]
    for i in range(8):
        x=copy.deepcopy(d);x['results'][i]['panels'][0]['actual_panel_size']+=1;tests.append(('panel_count_'+str(i),x))
    x=copy.deepcopy(d);x['results'][0]['groups'][0][0][0]^=1;tests.append(('group_matrix',x))
    x=copy.deepcopy(d);x['results'][3]['recipe']['y']=4;tests.append(('recipe',x))
    x=copy.deepcopy(d);x['results'][7]['panels'][2]['cosets'][0]['common_representatives']=[];tests.append(('common_representative',x))
    rejected=[]
    for name,x in tests:
        try:verify(x)
        except ValueError:rejected.append(name)
        else:raise ValueError('Damage survived: '+name)
    return rejected
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('input',type=Path);p.add_argument('--controls',action='store_true');a=p.parse_args()
    d=json.loads(a.input.read_text());r=verify(d)
    if a.controls:r['rejected_damages']=controls(d)
    print(json.dumps(r,sort_keys=True))
