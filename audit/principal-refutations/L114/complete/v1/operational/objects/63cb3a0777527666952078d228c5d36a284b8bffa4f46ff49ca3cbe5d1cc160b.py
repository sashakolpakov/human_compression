"""Polynomial-arithmetic reader of one returned nonthin Sz8 marking, not a scan."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,copy
PRIOR=Path('/Users/sasha/medusa/research/leemans/geometry/suzuki_incidence/prime_patterns/panel_check.py')
spec=importlib.util.spec_from_file_location('accepted_polynomial_reader',PRIOR)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
need=v.need;mm=v.mm
def power(a,n):
    r=1
    for _ in range(n):r=v.mul(r,a)
    return r
def u(a,b):
    at=power(a,4)
    return (1,0,0,0,a,1,0,0,v.mul(at,a)^b,at,1,0,v.mul(at,v.mul(a,a))^v.mul(a,b)^power(b,4),b,a,1)
def word_table(gens,names):
    words={v.ID:'1'};todo=[v.ID]
    for a in todo:
        for b,name in zip(gens,names):
            c=mm(a,b)
            if c not in words:
                words[c]=('' if words[a]=='1' else words[a])+name;todo.append(c)
    return words
def verify(d):
    need(d['status']=='RETURNED_FIXED_PAIR_PANEL_SCAN','Returned fixed-pair scope')
    need(d['field']=={'degree':3,'modulus':11},'Exact polynomial field')
    need(d['ambient_group_enumerated'] is False and d['complete_group_classification_claim'] is False,'No ambient census claim')
    w=d['witness'];need(isinstance(w,dict),'A returned witness is required')
    need(w['recipe']==dict(kind='conjugate',x=1,y=1,t=1),'Exact returned recipe')
    a=v.W;b=mm(mm(v.z(2),v.W),v.z(2));h=u(1,1);hi=mm(mm(h,h),h)
    need(mm(h,hi)==mm(hi,h)==v.ID,'Root-group inverse checked literally')
    c=mm(mm(mm(mm(h,v.W),v.z(1)),v.W),hi)
    need([v.matrix(t) for t in w['involutions']]==[a,b,c],'Three exact returned matrices')
    need([v.matrix(t) for t in d['fixed_pair']]==[a,b],'Exact fixed pair')
    need(all(t!=v.ID and mm(t,t)==v.ID for t in [a,b,c]),'Three involutions')
    def mpow(t,n):
        z=v.ID
        for _ in range(n):z=mm(z,t)
        return z
    ab,ac,bc=mm(a,b),mm(a,c),mm(b,c)
    need(all(t!=v.ID and mpow(t,p)==v.ID for t,p in [(ab,7),(ac,5),(bc,13)]),'Exact three prime product orders')
    need(mm(mpow(ac,2),mm(mpow(ab,3),a))==mpow(bc,6),'Short nonstandard coset identity')
    gens=[[a,b],[a,c],[b,c]]
    need([[v.matrix(t) for t in g] for g in w['generators']]==gens,'Exact parabolic generators')
    need(len(w['groups'])==3,'Three listed groups')
    G=[v.group(row,g,n) for row,g,n in zip(w['groups'],gens,[14,10,26])]
    need([G[0]&G[1],G[0]&G[2],G[1]&G[2]]==[{v.ID,a},{v.ID,b},{v.ID,c}],'Literal pair intersections')
    need(G[0]&G[1]&G[2]=={v.ID},'Literal triple intersection')
    panels=[];short=[]
    tables=[word_table(g,names) for g,names in zip(gens,[['a','b'],['a','c'],['b','c']])]
    for i in range(3):
        j,k=[t for t in range(3) if t!=i]
        candidates={frozenset(mm(t,h) for h in G[i]) for t in G[j]}
        need(len(candidates)==len(G[j])//len(G[i]&G[j]),'Complete actual candidate partition')
        records=[]
        for C in sorted(candidates,key=lambda z:sorted(z)):
            if not C&G[k]:continue
            records.append(dict(elements=[list(t) for t in sorted(C)],intersection_with_first=[list(t) for t in sorted(C&G[j])],intersection_with_second=[list(t) for t in sorted(C&G[k])],common_representatives=[list(t) for t in sorted(C&G[j]&G[k])]))
            x=min(C&G[j],key=lambda t:(len(tables[j][t]),tables[j][t]))
            y=min(C&G[k],key=lambda t:(len(tables[k][t]),tables[k][t]))
            xi=next(t for t in G[j] if mm(t,x)==v.ID)
            z=mm(xi,y);need(z in G[i],'A literal coset intersection witness')
            short.append(dict(missing_type=i,first_word=tables[j][x],second_word=tables[k][y],connecting_word=tables[i][z],standard=bool(C&G[j]&G[k])))
        panels.append(dict(missing_type=i,base_types=[j,k],candidate_cosets=len(candidates),actual_panel_size=len(records),standard_chambers=sum(bool(r['common_representatives']) for r in records),cosets=records))
    need(w['panels']==panels,'Exact returned full panels and all intersection sets')
    return dict(status='PASS_ONE_NONTHIN_SZ8_WITNESS',orders=[len(g) for g in G],prime_product_orders=[7,5,13],short_identity='(ac)^2 (ab)^3 a = (bc)^6',pair_intersection_orders=[2,2,2],triple_intersection_order=1,actual_panel_sizes=[r['actual_panel_size'] for r in panels],standard_chambers=[r['standard_chambers'] for r in panels],short_coset_witnesses=short,discovery_prefix_replayed=False,ambient_group_enumerated=False,source_application='Separate source-hypothesis proof and distinct review required')
def controls(d):
    tests=[]
    x=copy.deepcopy(d);x['field']['modulus']=13;tests.append(('field',x))
    x=copy.deepcopy(d);x['witness']['recipe']['x']=2;tests.append(('recipe',x))
    x=copy.deepcopy(d);x['witness']['involutions'][2][0]^=1;tests.append(('third_involution',x))
    for i in range(3):
        x=copy.deepcopy(d);x['witness']['groups'][i][0][0]^=1;tests.append(('group_'+str(i),x))
        x=copy.deepcopy(d);x['witness']['panels'][i]['cosets'].pop();tests.append(('panel_'+str(i),x))
    x=copy.deepcopy(d);x['witness']['panels'][0]['actual_panel_size']=2;tests.append(('thinness_count',x))
    x=copy.deepcopy(d);x['witness']['panels'][1]['cosets'][0]['intersection_with_second']=[];tests.append(('intersection',x))
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
