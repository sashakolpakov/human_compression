from pathlib import Path
import json,sys
if sys.flags.optimize:raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent;S=W.parent.parent
workers=W/'descent_workers';workers.mkdir(exist_ok=True)
out=W/'current_c4_descent';out.mkdir(exist_ok=True)
graphs={(g['n'],g['i']):g for g in json.loads((W/'current_c4_150_bipartite.json').read_text())}
scope=json.loads((W/'current_c4_census_scope.json').read_text())
base=(S/'phase177_rank_two_graphs.g').read_text().split('P177Inputs :=')[0].replace('Assert(1,','Need(')
base=base.replace('ConjugacyClassesSubgroups(A)','L059Descent(A,data.edges)')
base=base.replace('subgroup_classes:=Length(classes)','retained_edge_transitive_classes:=Length(classes),search:=L059Search')
header='Need:=function(ok) if not ok then Error("L059 descent invalid"); fi; end;;\nRead("maximal_descent.g");;\n'
crosschecks={(8,1),(10,2),(12,1),(32,5),(64,6)}
queue=[]
for r in scope['selected']:
    n,i=r['n'],r['i'];name=f'{n:03d}_{i:03d}'
    old=W/'current_c4_census'/(name+'.done')
    if old.exists() and (n,i) not in crosschecks:continue
    g=graphs[(n,i)]
    body=[header,base,'t:=Runtime();;',
      'D:=P177Graph("'+name+'",'+str(n)+','+str(g['black'])+','+str(g['edges'])+');;',
      'R:=P177Census(D);;Need(Size(R.F)='+str(r['aut_order'])+');;',
      'PrintTo("current_c4_descent/'+name+'.g","L059Result := ",R,";\\n");']
    if (n,i) in crosschecks:
        body.extend(['Read("current_c4_census/'+name+'.g");;',
          'Need(Length(R.witnesses)=Length(L059Result.witnesses));;',
          'for x in R.witnesses do y:=First(L059Result.witnesses,y->IsConjugate(R.A,x.H,y.H)); Need(y<>fail); Need(x.maxcode=y.maxcode and x.normcode=y.normcode and x.dualorder=y.dualorder and x.maxorder=y.maxorder); od;',
          'Print("OLD_COMPLETE_CENSUS_MATCH\\n");'])
    body.extend(['Print("L059_DESCENT_COMPLETE '+name+' ",Length(R.witnesses)," ",Runtime()-t,"\\n");','QUIT;'])
    (workers/(name+'.g')).write_text('\n'.join(body)+'\n')
    queue.append(name)
(W/'descent_queue.json').write_text(json.dumps(queue,indent=2)+'\n')
print('prepared',len(queue),'workers including',len(crosschecks),'independent complete-census cross-checks')
