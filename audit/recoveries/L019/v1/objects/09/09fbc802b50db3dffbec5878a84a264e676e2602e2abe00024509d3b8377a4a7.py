from pathlib import Path
import itertools,json

def matchings(points,p):
 if not points:yield tuple(p);return
 a=points[0];yield from matchings(points[1:],p)
 for j in range(1,len(points)):
  b=points[j];p[a]=b;p[b]=a
  yield from matchings(points[1:j]+points[j+1:],p)
  p[a]=a;p[b]=b

invs=list(matchings(list(range(10)),list(range(10))))
assert len(invs)==len(set(invs))==9496
nontrivial=[p for p in invs if p!=tuple(range(10))]
assert len(nontrivial)==9495 and sum(p[0]==0 for p in nontrivial)==2619
I=tuple(range(4));small=[p for p in itertools.permutations(range(4))if p!=I and all(p[p[i]]==i for i in range(4))]
def orbit(gs):
 parent=list(range(4))
 def find(a):
  while parent[a]!=a:a=parent[a]
  return a
 for p in gs:
  for a in range(4):parent[find(a)]=find(p[a])
 return frozenset(frozenset(a for a in range(4)if find(a)==find(b))for b in range(4))
cases=redundant=transitive_obstructions=0
for r in range(1,5):
 for gs in itertools.permutations(small,r):
  for j in range(r):
   tail=gs[:j]+gs[j+1:]
   if orbit(gs)!=orbit(tail):continue
   redundant+=1
   for x in small:
    assert orbit(gs+(x,))==orbit(tail+(x,));cases+=1
    if len(orbit(gs+(x,)))==1:transitive_obstructions+=1
out={'status':'PASS_DISTINCT_TEN_POINT_CONTROLS','independent_matchings':9496,'nonidentity_involutions':9495,'anchor_fixing':2619,'redundant_prefixes':redundant,'one_step_orbit_persistence':cases,'transitive_omission_obstructions':transitive_obstructions}
Path(__file__).with_name('independent_controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
