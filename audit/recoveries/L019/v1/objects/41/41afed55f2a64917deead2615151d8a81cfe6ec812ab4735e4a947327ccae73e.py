import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
import itertools,json,time
from pathlib import Path
N=7;V=tuple(range(N));start=time.monotonic()
def compose(p,q):return tuple(q[p[x]]for x in V)
def parts(marks):
 parent=list(V)
 def root(x):
  while parent[x]!=x:x=parent[x]
  return x
 for p in marks:
  for x in V:
   a,b=root(x),root(p[x]);parent[a]=b
 return tuple(root(x)for x in V)
def eligible(t,i):
 labels=parts([p for j,p in enumerate(t)if j!=i]);return [(x,t[i][x])for x in V if x<t[i][x]and labels[x]!=labels[t[i][x]]]
inv=[p for p in itertools.permutations(V)if p!=V and all(p[p[x]]==x for x in V)]
left=[p for p in inv if p[0]!=0 and p[6]==6];middle=[p for p in inv if p[0]==0 and p[6]==6];right=[p for p in inv if p[0]==0 and p[6]!=6]
counts={'involutions':len(inv),'left':len(left),'middle':len(middle),'right':len(right),'commuting_end_pairs':0,'distinct_triples':0,'transitive_triples':0,'paired_transitive_triples':0};survivors=[];distribution={}
for a in left:
 for c in right:
  if compose(a,c)!=compose(c,a):continue
  counts['commuting_end_pairs']+=1
  for b in middle:
   t=(a,b,c)
   if len(set(t))!=3:continue
   counts['distinct_triples']+=1
   if len(set(parts(t)))!=1:continue
   counts['transitive_triples']+=1;e=[eligible(t,i)for i in range(3)];k=','.join(map(str,map(len,e)));distribution[k]=distribution.get(k,0)+1
   if min(map(len,e))>=2:counts['paired_transitive_triples']+=1;survivors.append({'marks':t,'eligible':e})
report={'status':'COMPLETE_LABELLED_ANCHORED_TRANSITIVE_TRIPLES','counts':counts,'eligible_distribution':distribution,'survivors':survivors,'seconds':time.monotonic()-start,'claim':'Only combinatorial normalized-anchor, commutation, transitivity and eligibility conditions; full Sym7 and IP not presumed.'}
p=Path(__file__).with_name('enumeration01.json');assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='survivors'}))
