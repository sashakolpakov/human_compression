from pathlib import Path
import json,re,collections,sys
if sys.flags.optimize:raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent;S=W.parent.parent
workers=W/'cubic_workers';workers.mkdir(exist_ok=True)
out=W/'cubic_markings';out.mkdir(exist_ok=True)
graphs=json.loads((W/'cubic_filter/symmetric_inputs.json').read_text())
for g in graphs:g['family']='symmetric'
ss=[]
for line in (W/'CSS_lcf.txt').read_text().splitlines():
    m=re.fullmatch(r'! (\d+) (\d+): (\[[\d,\s-]+\])\^(\d+)',line.strip())
    if m is None:raise ValueError('LCF syntax')
    n,i=int(m[1]),int(m[2]);code=json.loads(m[3]);power=int(m[4])
    if len(code)*power!=n:raise ValueError('LCF length')
    if n>768:continue
    E={tuple(sorted((v,(v+1)%n))) for v in range(n)}
    for v in range(n):E.add(tuple(sorted((v,(v+code[v%len(code)])%n))))
    if len(E)!=3*n//2 or any(a==b for a,b in E):raise ValueError('LCF graph')
    g={'id':f'CSS_{n}_{i}','n':n,'edges':[list(e) for e in sorted(E)],'lcf':code,'power':power,'family':'semisymmetric'}
    graphs.append(g);ss.append(g)
if len(ss)!=43 or len(graphs)!=304:raise ValueError('cubic scope')
base=(S/'phase177_rank_two_graphs.g').read_text().split('P177Inputs :=')[0].replace('Assert(1,','Need(')
base=base.replace('ConjugacyClassesSubgroups(A)','L059Descent(A,data.edges)')
base=base.replace('subgroup_classes:=Length(classes)','retained_edge_transitive_classes:=Length(classes),search:=L059Search')
header='Need:=function(ok) if not ok then Error("L059 cubic census invalid"); fi; end;;\nRead("maximal_descent.g");;\n'
for g in graphs:
    n=g['n'];adj=[[] for _ in range(n)]
    for a,b in g['edges']:adj[a].append(b);adj[b].append(a)
    if any(len(x)!=3 for x in adj):raise ValueError('degree')
    colors={0:0};q=collections.deque([0])
    while q:
        a=q.popleft()
        for b in adj[a]:
            if b not in colors:colors[b]=1-colors[a];q.append(b)
            elif colors[b]==colors[a]:raise ValueError('not bipartite')
    if len(colors)!=n:raise ValueError('disconnected')
    black=[i+1 for i in range(n) if colors[i]==0];edges=[[a+1,b+1] for a,b in g['edges']];name=g['id']
    body=[header,base,'t:=Runtime();;',
      'D:=P177Graph("'+name+'",'+str(n)+','+str(black)+','+str(edges)+');;',
      'R:=P177Census(D);;']
    if g['family']=='symmetric':body.append('Need(Size(R.F)=2*Size(R.A));;')
    else:body.append('Need(Size(R.F)=Size(R.A));;')
    body.extend(['PrintTo("cubic_markings/'+name+'.g","L059Result := ",R,";\\n");',
      'Print("L059_CUBIC_COMPLETE '+name+' ",Length(R.witnesses)," ",Runtime()-t,"\\n");','QUIT;'])
    (workers/(name+'.g')).write_text('\n'.join(body)+'\n')
(out/'queue.json').write_text(json.dumps([g['id'] for g in graphs],indent=2)+'\n')
(out/'inputs.json').write_text(json.dumps(graphs,separators=(',',':'))+'\n')
print('prepared261symmetric+43semisymmetric complete marking workers')
