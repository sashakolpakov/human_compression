import sys
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
from pathlib import Path
import json,math
P=Path(__file__).resolve().parent
def need(b,s):
 if not b:raise ValueError(s)
def compose(a,b):return tuple(b[x]for x in a)
def inverse(a):
 b=[0]*len(a)
 for i,j in enumerate(a):b[j]=i
 return tuple(b)
def product(gs,n):
 a=tuple(range(n))
 for g in gs:a=compose(a,g)
 return a
def order(a):
 seen=set();ans=1
 for x in range(len(a)):
  if x in seen:continue
  k=0;y=x
  while y not in seen:seen.add(y);k+=1;y=a[y]
  need(y==x,'permutation cycles');ans=math.lcm(ans,k)
 return ans
results=[]
for line in (P/'literals.jsonl').read_text().splitlines():
 if not line.strip():continue
 r=json.loads(line);gs=[tuple(x-1 for x in g)for g in r['generators']];n=len(gs[0]);need(all(sorted(g)==list(range(n))for g in gs),'literal bijections')
 if r['word']:
  x=product([gs[i-1]for i in r['word']],n);t=gs[0]
 elif r['name']in['M23','M24']:x,y=gs;t=compose(x,y)
 else:x,t=gs
 xi=inverse(x);y=compose(xi,t)
 a=product([x,t,x,x,t,x,x,x,t],n);b=product([xi,t,xi,xi,t,xi,xi,xi,t],n)
 got=[order(x),order(y),order(a),order(b)];want=r['orders']or({'M23':[11,15,14,6],'M24':[23,15,15,12]}[r['name']])
 need(order(t)==2 and got==want and got[2]!=got[3],'word and involution orders')
 results.append({'name':r['name'],'degree':n,'orders':got})
need(len(results)==12 and len({r['name']for r in results})==12,'all twelve exactly')
out={'status':'PASS_INDEPENDENT_LITERAL_PERMUTATIONS','cases':results,'uses_GAP_for':'Extraction of saved literal permutation arrays only; all word products, inverses and cycle orders recomputed in plain Python.','generation':'Not re-enumerated by this supplementary check; exact finite subgroup generation covered by fresh full checker.'}
(P/'independent_words.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
