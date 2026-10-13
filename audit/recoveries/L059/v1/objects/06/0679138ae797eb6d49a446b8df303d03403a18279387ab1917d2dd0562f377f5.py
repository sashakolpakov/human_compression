from pathlib import Path
import json, collections, pynauty, sys, hashlib
if sys.flags.optimize:raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent
workers=W/'cubic_2048_fast_workers';workers.mkdir(exist_ok=True)
data=W/'cubic_2048_nauty';data.mkdir(exist_ok=True)
base=(W.parent.parent/'phase177_rank_two_graphs.g').read_text().split('P177Inputs :=')[0]
base=base.replace('Assert(1,','Need(').replace('ConjugacyClassesSubgroups(A)','L059Descent(A,data.edges)')
base=base.replace('subgroup_classes:=Length(classes)','retained_edge_transitive_classes:=Length(classes),search:=L059Search')
base=base.replace('A := AutGroupGraph(data.graph,[data.black,data.white]);','A := data.A;')
base=base.replace('F := AutGroupGraph(data.graph);','F := data.F;')
graphs=[g for g in json.loads((W/'cubic_2048_bipartite.json').read_text()) if 'retained_id' not in g]
for i,g in enumerate(graphs):
    name=g['id'];n=g['n'];adj={j:[] for j in range(n)};E={tuple(e) for e in g['edges']}
    for a,b in E:adj[a].append(b);adj[b].append(a)
    gens,man,exp,_,_=pynauty.autgrp(pynauty.Graph(n,adjacency_dict=adj))
    if exp!=0 or man!=int(man) or man>=2**53:raise ValueError('inexact automorphism order')
    for perm in gens:
        if sorted(perm)!=list(range(n)):raise ValueError('not a permutation')
        if {tuple(sorted((perm[a],perm[b]))) for a,b in E}!=E:raise ValueError('not an automorphism')
    col={0:0};q=collections.deque([0])
    while q:
        a=q.popleft()
        for b in adj[a]:
            if b not in col:col[b]=1-col[a];q.append(b)
            elif col[a]==col[b]:raise ValueError('not bipartite')
    if len(col)!=n:raise ValueError('disconnected')
    black=[j+1 for j in range(n) if col[j]==0];white=[j+1 for j in range(n) if col[j]==1]
    pin={'name':name,'n':n,'edges':g['edges'],'full_automorphism_generators':gens,
         'full_automorphism_order':int(man),'oracle':'pynauty.autgrp','pynauty_version':pynauty.__version__}
    f=data/(name+'.json');f.write_text(json.dumps(pin,separators=(',',':'))+'\n')
    ps=','.join('PermList('+str([j+1 for j in p])+')' for p in gens)
    s='Need:=function(ok) if not ok then Error("L059 cubic fast worker invalid"); fi; end;;\nRead("maximal_descent.g");;\n'+base
    s+='\nF:=Group(['+ps+']);;\nNeed(Size(F)='+str(int(man))+');;\n'
    s+='A:=Stabilizer(F,'+str(black)+',OnSets);;\nNeed(Index(F,A)=2);;\n'
    s+='D:=rec(label:="'+name+'",n:='+str(n)+',black:='+str(black)+',white:='+str(white)+',edges:='+str([[a+1,b+1] for a,b in sorted(E)])+',F:=F,A:=A);;\n'
    s+='R:=P177Census(D);;\nPrintTo("cubic_2048_markings/'+name+'.g","L059Result := ",R,";\\n");\n'
    s+='Print("L059_CUBIC2048_COMPLETE '+name+' ",Length(R.witnesses),"\\n");\nQUIT;\n'
    (workers/(name+'.g')).write_text(s)
    if (i+1)%50==0:print('prepared',i+1,flush=True)
print('FAST_WORKERS_PREPARED',len(graphs),flush=True)
