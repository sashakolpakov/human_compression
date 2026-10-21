"""Literal rooted canonicalization and exact small closure controls.
No full-census completeness follows from these positive checks alone.
"""
import ast,hashlib,json,sys
from pathlib import Path
if sys.flags.optimize: raise RuntimeError('unoptimized execution required')
def need(x,msg):
 if not x:raise ValueError(msg)
def validate(t):
 n=len(t[0]);need(all(len(g)==n and sorted(g)==list(range(n)) and all(g[g[x]]==x for x in range(n)) and any(g[x]!=x for x in range(n)) for g in t),'invalid involutions')
 need(all(all(g[h[x]]==h[g[x]] for x in range(n)) for i,g in enumerate(t) for j,h in enumerate(t) if abs(i-j)>1),'string')
 return n
def canon(t,root):
 n=validate(t);queue=[root];indices={root:0}
 for v in queue:
  for g in t:
   if g[v] not in indices:indices[g[v]]=len(queue);queue.append(g[v])
 need(len(queue)==n,'not transitive')
 return tuple(tuple(indices[g[v]] for v in queue) for g in t)
def closure(gs,n):
 identity=tuple(range(n));s={identity};q=[identity]
 for x in q:
  for g in gs:
   y=tuple(g[x[i]] for i in range(n))
   if y not in s:s.add(y);q.append(y)
 return s
def parts(gs,n):
 remain=set(range(n));answer=[]
 while remain:
  root=min(remain);q=[root];o={root}
  for x in q:
   for g in gs:
    if g[x] not in o:o.add(g[x]);q.append(g[x])
  remain-=o;answer.append(tuple(sorted(o)))
 return sorted(answer)
def small_checks(t):
 n=validate(t);r=len(t);subs=[closure([g for j,g in enumerate(t) if m>>j&1],n) for m in range(1<<r)]
 for a in range(1<<r):
  for b in range(1<<r):need(subs[a]&subs[b]==subs[a&b],'actual subset intersection')
 need(t[0][0]!=0 and all(g[0]==0 for g in t[1:]),'anchor')
 need(all(len(parts(t[:j]+t[j+1:],n))>1 for j in range(r)),'fracture')
 for j in range(1,r+1):
  old=subs[(1<<(j-1))-1];new=subs[(1<<j)-1];X={g[0] for g in old};outside=set(range(n))-X
  kernel={g for g in new if all(g[x]==x for x in outside)}
  need(kernel<=old,'full leaf kernel')
 return {'group_order':len(subs[-1]),'subset_pairs':(1<<r)**2,'kernels':r}
def glue(left,right):
 a=len(left[0]);b=len(right[0]);n=a+b+1
 def extend(g,offset):
  h=list(range(n))
  for x,y in enumerate(g):h[x+offset]=y+offset
  return tuple(h)
 u=list(range(n));u[0],u[a]=a,0
 v=list(range(n));v[a],v[a+1]=a+1,a
 return tuple(extend(g,0) for g in reversed(left))+(tuple(u),tuple(v))+tuple(extend(g,a+1) for g in right)
def load_run(w,n):
 d=w/f'n{n}_run03' if n==12 else w/f'n{n}_run01';receipt=json.loads((d/'receipt.json').read_text());need(receipt['status']=='COMPLETE_DIAGNOSTIC','incomplete census')
 raw=(d/'stdout.log').read_bytes();need(hashlib.sha256(raw).hexdigest()==receipt['stdout_sha256'],'receipt mismatch');need(not (d/'stderr.log').read_bytes(),'stderr')
 tuples=[tuple(tuple(x-1 for x in g) for g in ast.literal_eval(line.split('|',1)[1])) for line in raw.decode().splitlines() if line.startswith('SOLUTION|')]
 keys=[canon(t,0) for t in tuples];need(len(keys)==len(set(keys)),'duplicate rooted marking')
 return tuples
if __name__=='__main__':
 w=Path(__file__).resolve().parent;all_wings={p:load_run(w,2*p) for p in range(1,7)}
 controls={str(p):[small_checks(t) for t in ts] for p,ts in all_wings.items() if p<=3}
 derived={};classdata={}
 for k in range(1,7):
  candidates=[];keys=[]
  for p in range(1,k+1):
   q=k+1-p
   if p>q:continue
   for i,left in enumerate(all_wings[p]):
    for j,right in enumerate(all_wings[q]):
     if p==q and i>j:continue
     t=glue(left,right);n=validate(t);key=min(canon(orient,v) for orient in [t,tuple(reversed(t))] for v in range(n));keys.append(key)
     candidates.append({'left':[p,i],'right':[q,j],'marks':[list(g) for g in t]})
  need(len(keys)==len(set(keys)),'two balanced pairs yielded equivalent full markings')
  derived[str(k)]=len(candidates);classdata[str(k)]=candidates
 out={'status':'PASS','wing_counts':{str(p):len(t) for p,t in all_wings.items()},'small_literal_controls':controls,'boundary_counts':derived,'boundary_literal_classes':classdata}
 (w/'arrays_report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='boundary_literal_classes'}))
