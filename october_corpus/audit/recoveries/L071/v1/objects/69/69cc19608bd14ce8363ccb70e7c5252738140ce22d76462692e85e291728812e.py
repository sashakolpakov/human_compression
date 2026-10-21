#!/usr/bin/env python3
"""Exhaustive H3 marking census, root author; no whole F006 credit."""
from itertools import permutations
from functools import lru_cache
from pathlib import Path
import json,hashlib,time,argparse
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=False)
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):return tuple(p.index(i) for i in range(len(p)))
G=sorted(p+z for p in permutations(range(5)) if parity(p)==0 for z in [(5,6),(6,5)])
idx={p:i for i,p in enumerate(G)};identity=idx[tuple(range(7))];
if identity!=0:raise ValueError('identity indexing')
mul=[[idx[compose(p,q)] for q in G] for p in G];size=len(G);full=(1<<size)-1
invols=[i for i in range(1,size) if mul[i][i]==0];
if size!=120 or len(invols)!=31:raise ValueError('group inventory')
@lru_cache(None)
def subgroup(gens):
 seen=1;stack=[0]
 while stack:
  x=stack.pop()
  for y in gens:
   z=mul[x][y]
   if not (seen>>z)&1:seen|=1<<z;stack.append(z)
 return seen

def sub(gens):return subgroup(tuple(sorted(gens)))
def ip(t):
 hs=[sub(tuple(x for j,x in enumerate(t) if m>>j&1)) for m in range(1<<len(t))]
 return all(hs[i]&hs[j]==hs[i&j] for i in range(len(hs)) for j in range(i))
def order(x):
 y=x;n=1
 while y:
  y=mul[y][x];n+=1
 return n
automorphisms=[]
for p0 in permutations(range(5)):
 p=p0+(5,6);q=inv(p);automorphisms.append([idx[compose(p,compose(g,q))] for g in G])
def canonical(t,duality=True):
 choices=[tuple(a[x] for x in t) for a in automorphisms]
 if duality:choices += [tuple(reversed(x)) for x in choices]
 return min(choices)
counts={r:0 for r in range(1,7)};solutions={r:set() for r in range(1,7)};start=time.monotonic()
def walk(t,H):
 counts[len(t)]+=1
 if H==full:
  solutions[len(t)].add(canonical(t));return
 if len(t)==6:return
 for x in invols:
  if H>>x&1:continue
  if any(mul[x][y]!=mul[y][x] for y in t[:-1]):continue
  nt=t+(x,)
  if len(nt)>=3 and not ip(nt):continue
  walk(nt,sub(nt))
for x in invols:walk((x,),sub((x,)))
rows=[]
for r in range(1,7):
 reps=sorted(solutions[r]);entries=[]
 for t in reps:
  sch=[order(mul[t[j]][t[j+1]]) for j in range(r-1)]
  entries.append(dict(marking=[list(G[x]) for x in t],indices=t,schlafli=sch,connected=all(x>2 for x in sch),self_dual=canonical(t,False)==canonical(t[::-1],False)))
 rows.append(dict(rank=r,count=len(reps),self_dual=sum(x['self_dual'] for x in entries),connected=sum(x['connected'] for x in entries),representatives=entries))
report=dict(status='COMPLETE_FINITE_CENSUS_EXECUTION',group='Alt(5) x C2 in degree7',group_order=size,involutions=len(invols),automorphisms_supplied=len(automorphisms),valid_prefixes_by_rank=counts,rows=rows,elapsed_seconds=time.monotonic()-start,complete_rank_bound='Each independent-prefix index is at least 2, giving 2^rank <= 120 and rank <= 6.',whole_original_credit=0,runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','group_order','involutions','valid_prefixes_by_rank','elapsed_seconds']}))
print(json.dumps([{k:x[k] for k in ['rank','count','self_dual','connected']} for x in rows]))
