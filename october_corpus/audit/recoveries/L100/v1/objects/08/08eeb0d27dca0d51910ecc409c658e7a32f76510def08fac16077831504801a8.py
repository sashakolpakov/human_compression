"""Independent integer/set verification of all retained literal palette objects."""
import sys
if not __debug__: raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
from collections import deque
from decode import need

def perm(p,n):
    need(isinstance(p,list) and len(p)==n and all(type(i)is int for i in p) and sorted(p)==list(range(1,n+1)),'literal permutation')
    return tuple(p)
def product(p,q):return tuple(q[i-1] for i in p)
def closure(gs,n):
    one=tuple(range(1,n+1));seen={one};todo=deque([one])
    while todo:
        p=todo.popleft()
        for q in gs:
            z=product(p,q)
            if z not in seen:seen.add(z);todo.append(z)
    return seen
def palette_map(source,target,p):
    n=len(source['types']);r=source['rank'];need(n==target['n'] and r==target['rank'],'palette map equal domains')
    perm(p,n+r);need(set(p[:n])==set(range(1,n+1)) and set(p[n:])==set(range(n+1,n+r+1)),'object/marker cells')
    for a in range(n):
        need(p[n+source['types'][a]-1]==n+target['types'][p[a]-1],'marker type transport')
        need({p[b-1] for b in source['adjacency'][a]}==set(target['adjacency'][p[a]-1]),'complete incidence row transport')

def validate(data,projection):
    group=data['group_elements.json'];gs=[tuple(x)for x in group['generators']];E=[tuple(x)for x in group['elements']];degree=len(gs[0])
    for p in gs+E:perm(list(p),degree)
    need(len(E)==len(set(E))==20160 and closure(gs,degree)==set(E),'actual complete fixed permutation group closure')
    need(group['generators']==projection['group_generators'],'exact input generator correspondence')
    pos={p:i+1 for i,p in enumerate(E)};mul=[[pos[product(p,g)]for p in E]for g in gs]
    result=data['result.json'];checkpoint=data['checkpoint.json'];records=result['records'];sources=projection['representatives'];models={}
    need(result['status']=='COMPLETE_LITERAL_INCIDENCE_AND_PALETTE_CATALOGUE' and result['completed']==list(range(1,30)),'all29 literal outputs')
    need(checkpoint['status']=='COMPLETE_LEADING_REPRESENTATIVES_ONLY' and all(checkpoint[k]==result[k]for k in ['completed','classes','members','records']),'final checkpoint exact result')
    need(len(records)==len(sources)==29 and result['members']==[[q['bare_representative'],q['index']]for q in records],'complete classification records')
    tested_coset_members=tested_rows=0
    for i,(q,s)in enumerate(zip(records,sources),1):
        d=data[f'model{i}.json'];g=data[f'groups{i}.json'];models[i]=d;n=d['n'];r=d['rank']
        need(g==q and q['index']==i and d['source']==q['source']==s['source'],'exact source/record links')
        need(r==q['rank']==len(s['parabolic_generators']) and len(d['types'])==len(d['coset_positions'])==len(d['adjacency'])==n,'literal geometry shape')
        need(set(d['types'])==set(range(1,r+1)) and d['type_sizes']==q['type_sizes']==[d['types'].count(t)for t in range(1,r+1)],'exact types/sizes')
        need(len(d['parabolics'])==r,'one parabolic per type');which=[[0]*len(E)for _ in range(r)]
        for t,sg in enumerate(s['parabolic_generators']):
            H=closure([tuple(x)for x in sg],degree)
            need(set(d['parabolics'][t])=={pos[x]for x in H} and len(d['parabolics'][t])==len(H),'saved subgroup equals exact fusion input')
        for a,(t,c)in enumerate(zip(d['types'],d['coset_positions']),1):
            need(c==sorted(set(c)) and c and all(type(k)is int and 1<=k<=len(E)for k in c),'literal coset domain')
            H=[E[k-1]for k in d['parabolics'][t-1]];x=E[c[0]-1]
            need({pos[product(h,x)]for h in H}==set(c),'actual right coset')
            for k in c:
                need(which[t-1][k-1]==0,'disjoint cosets');which[t-1][k-1]=a
            tested_coset_members+=len(c)
        need(all(all(row)for row in which),'complete coset partition')
        adj=[set()for _ in range(n)]
        for k in range(len(E)):
            cells=[row[k]for row in which]
            for a in cells:adj[a-1].update(b for b in cells if a!=b)
        need(d['adjacency']==[sorted(row)for row in adj],'complete intersection incidence including nonedges')
        need(len(d['group_action'])==len(gs),'actual specified generator action')
        for p,mg in zip(d['group_action'],mul):
            perm(p,n)
            for a,(t,c)in enumerate(zip(d['types'],d['coset_positions']),1):
                need(all(which[t-1][mg[k-1]-1]==p[a-1]for k in c),'every right-action coset member')
            palette_map(d,d,p+list(range(n+1,n+r+1)))
        need(type(q['typed_order'])is int and type(q['correlations_order'])is int and q['typed_order']>=20160 and q['correlations_order']==q['typed_order']*q['type_action_order'],'exact order quotient shape')
        for p in q['correlations_generators']:palette_map(d,d,p);tested_rows+=n
        for p in q['typed_generators']:
            palette_map(d,d,p);need(p[n:]==list(range(n+1,n+r+1)),'typed marker kernel');tested_rows+=n
        hit=q['bare_representative'];need(type(hit)is int and 1<=hit<=i,'sequential class representative');palette_map(models[hit],d,q['bare_map'])
    classes=[q['index']for q in records if q['bare_representative']==q['index']]
    need(result['classes']==classes and all(q['bare_representative']in classes for q in records),'exact bare partition')
    counts=[[r,sum(q['rank']==r for q in records),sum(records[i-1]['rank']==r for i in classes)]for r in sorted({q['rank']for q in records})]
    need(result['counts']==counts,'literal rank totals')
    return dict(models=29,group_elements=len(E),coset_members=tested_coset_members,generator_incidence_rows=tested_rows,counts=counts,full_group_orders='acquired native GRAPE/nauty result; positive checks alone are not completeness')
