"""Independent checks of saved positive maps and bounded distance/name controls."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,itertools,json
from pathlib import Path
from construction_join import c,D,C,read,need,pin
from literal_diagrams import graph_data
from named_residues import identify
W=Path(__file__).resolve().parent

def verify_saved(q,metadata,duality):
    m=read(D/f'model{q["catalogue_index"]}.json');geo=c.Geometry(metadata,q['model'],q['choice'])
    need(m['source']==q['source'],'literal source link')
    ts=[i-1 for i in q['catalogue_to_construction_types']];images=q['object_images']
    need(sorted(ts)==sorted(i-1 for i in q['retained_types']),'complete type bijection')
    need(len(images)==m['n'],'object map length')
    for t in range(m['rank']):
        need(sorted(images[i]for i,u in enumerate(m['types'])if u==t+1)==list(range(len(geo.objects[ts[t]]))),'object map bijection')
    for a,(u,x)in enumerate(zip(m['types'],images)):
        expected={b+1 for b,(v,y)in enumerate(zip(m['types'],images))if u!=v and (geo.adj[ts[u-1],ts[v-1]][x]>>y)&1}
        need(expected==set(m['adjacency'][a]),'every incidence/nonincidence row')
    group=read(D/'group_elements.json');gens=[[x-1 for x in p]for p in group['generators']]
    if q['group_automorphism']=='duality':gens=duality['generator_images']
    else:need(q['group_automorphism']=='identity','exact automorphism choice')
    for p,g in zip(m['group_action'],gens):
        for a,(u,x)in enumerate(zip(m['types'],images)):
            need(images[p[a]-1]==geo.object_image(ts[u-1],x,g),'every generator intertwines actual object actions')
    return m['n'],m['n']*len(gens)

def rejects(f):
    try:f()
    except (ValueError,KeyError,IndexError,TypeError):return
    raise ValueError('damaged control accepted')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir()
    joins=read(W/'construction_join03/joins.json');meta=read(C/'expected/model.json');rows=edges=0
    for q in joins['routes']:
        n,e=verify_saved(q,meta,joins['duality']);rows+=n;edges+=e
    damages=[]
    q=joins['routes'][0]
    for kind in ['duplicate-object','swap-object','wrong-source','wrong-type','wrong-automorphism','wrong-hyperoval-choice']:
        d=copy.deepcopy(q)
        if kind=='duplicate-object':d['object_images'][0]=d['object_images'][1]
        elif kind=='swap-object':d['object_images'][0],d['object_images'][1]=d['object_images'][1],d['object_images'][0]
        elif kind=='wrong-source':d['source'][0]+=1
        elif kind=='wrong-type':d['catalogue_to_construction_types'][0]=d['catalogue_to_construction_types'][1]
        elif kind=='wrong-automorphism':d['group_automorphism']='identity'
        else:d['choice']=[0,1]
        rejects(lambda:verify_saved(d,meta,joins['duality']));damages.append(kind)
    graph_controls=0
    for n in range(4,14,2):
        A=[{(i-1)%n,(i+1)%n}for i in range(n)];q=graph_data(range(n),A,{i:i%2 for i in range(n)})
        need(q['girth']==n and q['eccentricities']==[[n//2],[n//2]],'even cycle distance/girth oracle');graph_controls+=1
    for n,m in itertools.product(range(2,6),range(2,7)):
        A=[set(range(n,n+m))for _ in range(n)]+[set(range(n))for _ in range(m)]
        q=graph_data(range(n+m),A,{i:int(i>=n)for i in range(n+m)})
        need(q['girth']==4 and q['digon'] and q['eccentricities']==[[2],[2]],'complete bipartite oracle');graph_controls+=1
    # Independently retained exact six-cycle behind the proposed missing3.5 bond.
    m=read(D/'model14.json');d=read(W/'literal_diagrams01/diagrams.json')['records'][13];base=d['base_chamber'][0]-1
    vertices={x-1 for x in m['adjacency'][base]};A=[{v-1 for v in row}for row in m['adjacency']]
    need(len(vertices)==6 and all(len(A[v]&vertices)==2 for v in vertices),'literal3.5 six-cycle degrees')
    q=graph_data(vertices,A,{v:int(m['types'][v]==3)for v in vertices})
    need(q['girth']==6 and q['type_sizes']==[3,3] and q['edges']==6,'literal3.5 full residue')
    (a.out/'residue_3.5.json').write_text(json.dumps(dict(catalogue_index=14,fixed_vertex=base+1,vertices=[v+1 for v in sorted(vertices)],
        adjacency=[[v+1,sorted(x+1 for x in A[v]&vertices)]for v in sorted(vertices)],data=q,input=pin(D/'model14.json')),indent=2)+'\n')
    named_controls=0
    for n in range(3,9):
        pairs=list(itertools.combinations(range(n),2));N=n+len(pairs);A=[set()for _ in range(N)]
        for i,(u,v)in enumerate(pairs,n):A[i]={u,v};A[u].add(i);A[v].add(i)
        q=identify(set(range(N)),[0]*n+[1]*len(pairs),A,'C-right',1)
        need(q['points']==n,'complete graph exact named incidence');named_controls+=1
        bad=copy.deepcopy(A);bad[n].remove(next(iter(bad[n])))
        rejects(lambda:identify(set(range(N)),[0]*n+[1]*len(pairs),bad,'C-right',1));damages.append(f'missing-K{n}-endpoint')
    report=dict(status='PASS_SOURCE_JOIN_BOUNDED_CONTROLS',saved_maps=len(joins['routes']),incidence_rows=rows,actual_generator_rows=edges,
        graph_controls=graph_controls,named_controls=named_controls,damages=damages,
        target_runs=0,source_credit=0,inputs=[pin(W/'construction_join03/joins.json'),pin(C/'expected/model.json'),pin(W/'literal_diagrams01/diagrams.json')])
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
