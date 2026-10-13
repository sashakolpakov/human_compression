from pathlib import Path
import argparse, collections, hashlib, json, sys
if sys.flags.optimize:
    raise RuntimeError('optimized Python unsupported')
import pynauty
p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('folder');a=p.parse_args()
W=Path(__file__).resolve().parent
if not a.folder.startswith('nonbipartite_retry') or '/' in a.folder:
    raise ValueError('retry folder')
old=W/'nonbipartite_subdivisions'/(a.name+'.receipt.json')
if json.loads(old.read_text())['status']!='TIME_LIMIT_NO_CONCLUSION':
    raise ValueError('only a capped incomplete case may be retried')
out=W/a.folder;out.mkdir(exist_ok=False)
source=W/'cubic_2048_nonbipartite.json'
g=next(x for x in json.loads(source.read_text()) if x['id']==a.name)
n=g['n'];edges={tuple(e) for e in g['edges']};adj={j:[] for j in range(n)}
for u,v in edges:
    if not 0<=u<v<n:raise ValueError('edge endpoints')
    adj[u].append(v);adj[v].append(u)
if len(edges)*2!=3*n or any(len(v)!=3 for v in adj.values()):raise ValueError('cubic')
seen={0};q=collections.deque([0])
while q:
    for v in adj[q.popleft()]:
        if v not in seen:seen.add(v);q.append(v)
if len(seen)!=n:raise ValueError('connected')
gens,man,exp,_,_=pynauty.autgrp(pynauty.Graph(n,adjacency_dict=adj))
if exp!=0 or man!=int(man) or man>=2**53:raise ValueError('inexact order')
for perm in gens:
    if sorted(perm)!=list(range(n)):raise ValueError('permutation')
    if {tuple(sorted((perm[u],perm[v]))) for u,v in edges}!=edges:raise ValueError('automorphism')
record=dict(name=a.name,n=n,edges=sorted(edges),generators=gens,order=int(man),
            oracle='pynauty.autgrp',version=pynauty.__version__,
            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
(out/'oracle.json').write_text(json.dumps(record,separators=(',',':'))+'\n')
perms=','.join('PermList('+str([v+1 for v in perm])+')' for perm in gens)
lines=['Read("subdivision_actual_actions.g");;', 'Read("maximal_descent_arcs.g");;',
       'F:=Group(['+perms+']);;', 'Need(Size(F)='+str(int(man))+');;',
       'L059Edges:=Set('+str([[u+1,v+1] for u,v in sorted(edges)])+');;',
       'arcs:=Concatenation(List(L059Edges,e->[e,Reversed(e)]));;',
       'reps:=List(L059DescentArcs(F,arcs),Representative);;',
       'S:=rec(label:="'+a.name+'",n_original:='+str(n)+',edges_original:=L059Edges,A_subdivision:=F,witnesses:=L059SubdivisionRows(F,L059Edges,reps),search:=L059Search);;',
       'PrintTo("'+a.folder+'/'+a.name+'.g","L059Subdivision := ",S,";\\n");',
       'Print("L059_NONBIPARTITE_RETRY_COMPLETE '+a.name+' ",Length(S.witnesses),"\\n");',
       'QUIT_GAP(0);']
(out/'worker.g').write_text('\n'.join(lines)+'\n')
print(a.name,'fullAut',int(man),'worker ready')
