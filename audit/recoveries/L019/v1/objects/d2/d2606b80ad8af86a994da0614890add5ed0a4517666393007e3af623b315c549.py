import hashlib
import json
from pathlib import Path
import sys
if sys.flags.optimize:
    raise SystemExit('optimized Python is unsupported')
w=Path(__file__).resolve().parent
s=w.parents[2]
def pin(p):
    return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
pa=s/'topic_B_L019_actual_wings_v1/wing_inputs.json'
ps=s/'topic_B_L044_symmetric_faithful_pairs_v1/finite/author_certificate01/records.json'
pe=s/'topic_B_L047_candidate_v2/finite_results.json'
data={'a11_rank_six':json.loads(pa.read_text())['a11_rank_six'],
      's8_rank_six':[{'source_index':i,'permutations':p} for i,p in enumerate(json.loads(ps.read_text()))],
      'small_extremal':json.loads(pe.read_text())['small_extremal']['extremal_markings']}
(w/'inputs.json').write_text(json.dumps(data,indent=2)+'\n')
(w/'extraction.json').write_text(json.dumps({'inputs':[pin(pa),pin(ps),pin(pe)],'method':'Complete retained literal arrays, without filtering or alteration.'},indent=2)+'\n')
g=['SizeScreen([100000,100000]);;']
for i,row in enumerate(data['a11_rank_six']):
    g.append('tt:=List('+json.dumps(row['permutations'])+',PermList);;')
    g.append('for rev in [false,true] do if rev then t:=Reversed(tt);else t:=tt;fi; c:=Centralizer(SymmetricGroup(11),Group(t{[2..6]})); if Size(c)<>1 then Error("nontrivial A11 tail centralizer");fi; Print("A11|'+str(i)+'|",rev,"|",Size(c),"\\n");od;')
for i,row in enumerate(data['s8_rank_six']):
    g.append('t:=List('+json.dumps(row['permutations'])+',PermList);;')
    g.append('for j in [1..6] do o:=Orbits(Group(t{Difference([1..6],[j])}),[1..8]); if Length(o)<2 then Error("transitive S8 omission");fi; Print("S8|'+str(i)+'|",j-1,"|",SortedList(List(o,Length)),"\\n");od;')
for i,row in enumerate(data['small_extremal']):
    n=row['n'];g.append('t:=List('+json.dumps(row['permutations'])+',PermList);;')
    g.append('if not ForAll([1..Length(t)-1],j->Order(t[j]*t[j+1])=3) then Error("not simplex");fi;')
    g.append('Print("SMALL|'+str(i)+'|",List([1..Length(t)],j->SortedList(List(Orbits(Group(t{Difference([1..Length(t)],[j])}),[1..'+str(n)+']),Length))),"\\n");')
g+=['Print("PASS_INITIAL_FRACTURE_BOUNDARIES\\n");QUIT;']
(w/'gap_boundaries.g').write_text('\n'.join(g)+'\n')
print('Extracted all four A11 tuples and both S8 tuples.')
