"""Complete finite residue invariants from accepted literal coset models only."""
import sys
if not __debug__: raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,itertools,json
from collections import deque
from pathlib import Path
G=Path(__file__).resolve().parent.parent
D=G/'palette_serialization_v1/derived'
def read(p):return json.loads(p.read_text())
def need(v,s):
    if not v:raise ValueError(s)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def graph_data(vertices,adj,types):
    vs=set(vertices);rows={x:set(adj[x])&vs for x in vs};girth=None;ecc=[set(),set()]
    for start in sorted(vs):
        distance={start:0};parent={start:None};q=deque([start])
        while q:
            x=q.popleft()
            for y in rows[x]:
                if y not in distance:distance[y]=distance[x]+1;parent[y]=x;q.append(y)
                elif parent[x]!=y and parent[y]!=x:
                    length=distance[x]+distance[y]+1
                    girth=length if girth is None else min(girth,length)
        need(set(distance)==vs,'connected rank-two residue')
        ecc[types[start]].add(max(distance.values()))
    sizes=[sum(types[x]==i for x in vs) for i in range(2)]
    degrees=[sorted({len(rows[x]) for x in vs if types[x]==i}) for i in range(2)]
    need(girth is not None and girth%2==0,'finite bipartite girth')
    return dict(type_sizes=sizes,degrees=degrees,girth=girth,gonality=girth//2,
                eccentricities=[sorted(x) for x in ecc],edges=sum(map(len,rows.values()))//2,
                digon=all(len(rows[x])==sizes[1-types[x]] for x in vs))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output');a.out.mkdir()
    group=read(D/'group_elements.json');E=[tuple(p) for p in group['elements']];pos={p:i for i,p in enumerate(E)}
    identity=pos[tuple(range(1,22))];results=[]
    for index in range(1,30):
        m=read(D/f'model{index}.json');r=m['rank'];adj=[{b-1 for b in row} for row in m['adjacency']]
        types=[t-1 for t in m['types']];base=[next(a for a,(u,coset) in enumerate(zip(types,m['coset_positions'])) if u==t and identity+1 in coset) for t in range(r)]
        need(all(base[j] in adj[base[i]] for i,j in itertools.combinations(range(r),2)),'actual identity chamber')
        def residue(ts):
            return {x for x,t in enumerate(types) if t in ts and all(x in adj[base[j]] for j in range(r) if j not in ts)}
        which=[]
        for t in range(r):
            row={k-1:x for x,(u,coset) in enumerate(zip(types,m['coset_positions'])) if u==t for k in coset}
            need(len(row)==len(E),'complete type cosets');which.append(row)
        def act(x,h):
            p=E[m['coset_positions'][x][0]-1];q=E[h]
            return which[types[x]][pos[tuple(q[i-1] for i in p)]]
        H=[{i-1 for i in hs} for hs in m['parabolics']];panels=[];twot=[]
        for t in range(r):
            panel=sorted(residue({t}));panels.append(len(panel)-1)
            stabilizer=set(range(len(E)))
            for j in range(r):
                if j!=t:stabilizer &= H[j]
            need(len(panel)>=2,'panel firmness');u,v=panel[:2]
            image={act(v,h) for h in stabilizer if act(u,h)==u}
            twot.append(image==set(panel)-{u})
        pairs=[]
        for i,j in itertools.combinations(range(r),2):
            vs=residue({i,j});q=graph_data(vs,adj,{v:int(types[v]==j) for v in vs});q['types']=[i+1,j+1];pairs.append(q)
        kernels=[]
        for t in range(r):
            neighbours=adj[base[t]]
            kernel=[h for h in sorted(H[t]) if all(act(x,h)==x for x in neighbours)]
            kernels.append(dict(type=t+1,order=len(kernel),element_positions=[h+1 for h in kernel]))
        q=dict(index=index,source=m['source'],type_sizes=m['type_sizes'],base_chamber=[x+1 for x in base],panel_orders=panels,
               panel_two_transitive=twot,pairs=pairs,local_action_kernels=kernels,input=pin(D/f'model{index}.json'))
        results.append(q);print(index,panels,twot,flush=True)
    out=dict(status='COMPLETE_LITERAL_BASE_RESIDUE_INVARIANTS',records=results,group_input=pin(D/'group_elements.json'),
             target_censuses=0,graph_isomorphism_calls=0,source_credit=0,
             scope='All base residues and local kernels; transfer uses acquired actual flag transitivity. No abstract group-name identification.')
    (a.out/'diagrams.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
