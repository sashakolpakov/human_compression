"""Independent finite regular-action checks; these are not proof premises."""
from pathlib import Path
from math import gcd
import json,time
P=Path(__file__).resolve().parent;start=time.monotonic();rows=[]
for m in range(1,31):
 elements=[(k,e)for e in range(2)for k in range(m)];pos={x:i for i,x in enumerate(elements)}
 def mul(a,b):return ((a[0]+(-1 if a[1]else 1)*b[0])%m,a[1]^b[1])
 translations=[[pos[mul(g,x)]for x in elements]for g in [(1%m,0),(0,1)]]
 theta=[pos[((-k)%m,0)if e==0 else((1-k)%m,1)]for k,e in elements]
 def orbits(generators):
  unseen={(a,b)for a in range(2*m)for b in range(a+1,2*m)};count=0
  while unseen:
   seed=min(unseen);todo=[seed];unseen.remove(seed);count+=1
   while todo:
    a,b=todo.pop()
    for g in generators:
     image=tuple(sorted((g[a],g[b])))
     if image in unseen:unseen.remove(image);todo.append(image)
  return count
 inner=orbits(translations);outer=orbits(translations+[theta]);assert(inner,outer)==(m+m//2,m)
 reflections={pos[(k,1)]for k in range(m)};seen=set();reflection_orbits=0
 for r in reflections:
  if r not in seen:seen.update([r,theta[r]]);reflection_orbits+=1
 assert reflection_orbits==(m+1)//2
 rows.append(dict(m=m,unordered_inner_orbits=inner,unordered_outer_orbits=outer,reflection_outer_orbits=reflection_orbits))
residues=[]
for p in range(1,120):
 if gcd(p,120)!=1 or p%40 not in [3,13,27,37]:continue
 epsilon=1 if p%3==1 else -1
 if ((p-epsilon)//6)%2==0:residues.append(p)
assert residues==[13,37,83,107]
report=dict(status='PASS_INDEPENDENT_REGULAR_ACTION_ORBITS',seconds=time.monotonic()-start,m_values=30,rows=rows,cyclic_six_residues_mod120=residues,group_searches=0,scope='Tiny abstract dihedral actions, including m1/2; no PSL/PGL enumeration and no source credit.')
(P/'orbits01.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],report['seconds'])
