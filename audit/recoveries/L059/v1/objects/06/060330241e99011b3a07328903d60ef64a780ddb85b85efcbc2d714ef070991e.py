from pathlib import Path
import json,sys
if sys.flags.optimize:raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent;S=W.parent.parent
out=W/'current_c4_census';out.mkdir(exist_ok=True)
graphs={(g['n'],g['i']):g for g in json.loads((W/'current_c4_150_bipartite.json').read_text())}
meta=json.loads((W/'c4_table.html.json').read_text())
selected=[r for r in meta if r['n']<=150 and r['bipartite'] and r['tr']!='HT' and (r['vertex_stabilizer']<100 or r['n']==8)]
if len(selected)!=389:raise ValueError('scope changed')
base=(S/'phase177_rank_two_graphs.g').read_text().split('P177Inputs :=')[0].replace('Assert(1,','Need(')
body=['Need:=function(ok) if not ok then Error("L059 current census check failed"); fi; end;;',base]
body.append('Print("CURRENT_C4_CENSUS_START\\n");')
for r in selected:
    n,i=r['n'],r['i'];g=graphs[(n,i)];name=f'{n:03d}_{i:03d}'
    if (out/(name+'.done')).exists():continue
    body.extend([
      'Print("BEGIN '+name+'\\n"); t:=Runtime();;',
      'D:=P177Graph("'+name+'",'+str(n)+','+str(g['black'])+','+str(g['edges'])+');;',
      'R:=P177Census(D);;',
      'Need(Size(R.F)='+str(r['aut_order'])+');;',
      'PrintTo("current_c4_census/'+name+'.g","L059Result := ",R,";\\n");',
      'PrintTo("current_c4_census/'+name+'.done","COMPLETE '+name+' ",Length(R.witnesses)," ",Runtime()-t,"\\n");',
      'Print("END '+name+' TIME_MS ",Runtime()-t,"\\n");'
    ])
body.extend(['Print("CURRENT_C4_CENSUS_COMPLETE\\n");','QUIT;'])
(W/'current_c4_census.g').write_text('\n'.join(body)+'\n')
(W/'current_c4_census_scope.json').write_text(json.dumps({'status':'diagnostic_current_scope; historical_identification_pending','selected':selected,'count':len(selected),'source_inputs':'current_c4_150_bipartite.json','exception':'K4,4 included because L059 prints it despite literal vertex-stabilizer cutoff'},indent=2)+'\n')
print('prepared',len(selected),'graphs; completed result files preserved')
