import itertools,json,time
from pathlib import Path
s=Path(__file__).resolve().parents[2];p=s/'topic_B_L019_small_symmetric_v2'
def mul(a,b):return tuple(b[x] for x in a)
def group(gs,n):
 e=tuple(range(n));out={e};todo=[e]
 for a in todo:
  for b in gs:
   c=mul(a,b)
   if c not in out:out.add(c);todo.append(c)
 return out
def subs(t,n):return [group([g for i,g in enumerate(t) if k>>i&1],n) for k in range(1<<len(t))]
def orbit(H,a):return {g[a] for g in H}
checks=0
rows=json.loads((p/'eight_tuples.json').read_text())
for idx,row in enumerate(rows):
 t=[tuple(x-1 for x in g) for g in row];H=subs(t,8)
 for i in range(32):
  for j in range(32):
   if H[i]&H[j]!=H[i&j]:raise ValueError(('IP',idx,i,j))
   checks+=1
 if idx<6:
  if len(orbit(H[30],1))!=7 or orbit(H[30],0)!={0}:raise ValueError('pure tail')
e=tuple(range(4));inv=[a for a in itertools.permutations(range(4)) if a!=e and mul(a,a)==e];tails=[a for a in inv if a[0]==0];natural=fractured=0
for a in inv:
 if a[0]==0:continue
 for b,c in itertools.product(tails,repeat=2):
  if mul(a,c)!=mul(c,a) or mul(a,b)==mul(b,a) or mul(b,c)==mul(c,b):continue
  t=[a,b,c];H=subs(t,4)
  if len(H[7])!=24 or any(H[i]&H[j]!=H[i&j] for i in range(8) for j in range(8)):continue
  natural+=1
  if any(len(orbit(H[7^(1<<j)],0))==4 for j in range(3)):continue
  fractured+=1
  if any(sum(g[x]!=x for x in range(4))!=2 for g in t):raise ValueError('not simplex')
if not fractured:raise ValueError('empty m4 control')
r={'status':'PASS','S8_all_subset_intersections':checks,'S8_pure_tail_transitivity':6,'S4_anchored_natural_markings':natural,'S4_fractured_simplex_markings':fractured}
Path(__file__).with_name('extra_report.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
