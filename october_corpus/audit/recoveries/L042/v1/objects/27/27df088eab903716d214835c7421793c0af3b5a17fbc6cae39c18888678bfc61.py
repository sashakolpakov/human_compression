"""Exact source-to-wing maps and finite controls for the uniform proof."""
import json,sys
from diagrams import FAMILIES, need, graph, validate, isomorphism, subdivide
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')

def conjugacy(source,target,record):
    n=validate(source);need(validate(target)==n,'degree')
    phi=record['point_map'];need(sorted(phi)==list(range(n)),'point map')
    target=tuple(reversed(target)) if record['reverse_target'] else target
    need(len(source)==len(target),'rank')
    need(all(phi[g[x]]==h[phi[x]] for g,h in zip(source,target) for x in range(n)), 'point conjugacy')

def verify(bases,source_records):
    need(source_records['status']=='PASS_ALL_18_SOURCE_MATRICES','source status')
    rows=source_records['records'];need(len(rows)==len(FAMILIES),'source count')
    results=[];indices={k:set() for k in range(1,5)}
    for (k,name,j),src in zip(FAMILIES,rows):
        need((src['k'],src['family'],src['n'])==(k,name,31),'source row order')
        model,_=graph(k,name,31)
        literal=tuple(tuple(g) for g in src['marks'])
        conjugacy(literal,model,src['to_model'])
        n=2*k+3;t,e=graph(k,name,n);hits=[]
        for i,b in enumerate(bases[str(k)]):
            marks=tuple(tuple(g) for g in b['marks'])
            iso=isomorphism(t,marks)
            if iso is not None:
                conjugacy(t,marks,iso)
                hits.append({'index':i,'left':b['left'],'right':b['right'],**iso})
        need(len(hits)==1,'base uniqueness')
        need(hits[0]['index'] not in indices[k],'duplicate source family')
        indices[k].add(hits[0]['index'])
        controls=[]
        for nn in list(range(n,n+5))+[31]:
            tt,_=graph(k,name,nn);ss=subdivide(tt,j);nt,_=graph(k,name,nn+1)
            iso=isomorphism(ss,nt);need(iso is not None and not iso['reverse_target'],'growth orientation')
            conjugacy(ss,nt,iso);controls.append({'n':nn,**iso})
        results.append({'k':k,'family':name,'base_n':n,'cut':j,'marks':t,'edges':e,
                        'base_match':hits[0],'subdivision_controls':controls})
    for k,covered in indices.items():
        need(covered==set(range(len(bases[str(k)]))),'incomplete base coverage')
    return {'status':'PASS','families':results}
