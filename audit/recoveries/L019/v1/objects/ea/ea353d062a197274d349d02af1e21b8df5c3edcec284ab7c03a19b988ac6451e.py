import itertools,json,time
from pathlib import Path
start=time.monotonic();N=9;points=tuple(range(N))
def matchings(V):
 if not V:
  yield ();return
 x,*R=V
 for s in matchings(R):yield s
 for j,y in enumerate(R):
  for s in matchings(R[:j]+R[j+1:]):yield ((x,y),)+s

def perm(M):
 q=list(points)
 for x,y in M:q[x]=y;q[y]=x
 return tuple(q)
def commute(a,b):return all(a[b[x]]==b[a[x]] for x in points)
def orbit_labels(T):
 labels=[-1]*N
 for x in points:
  if labels[x]>=0:continue
  labels[x]=x;stack=[x]
  while stack:
   u=stack.pop()
   for p in T:
    v=p[u]
    if labels[v]<0:labels[v]=x;stack.append(v)
 return labels
A=[perm(((0,1),)+M) for M in matchings(list(range(2,8)))];D=[perm(((7,8),)+M) for M in matchings(list(range(1,7)))];middle=[perm(M) for M in matchings(list(range(1,8))) if M]
ends=[(a,d) for a in A for d in D if commute(a,d)]
assert len(ends)==196 and len(middle)==231
seq=[0,1,0,1,2,3,2,3];target=[perm([(j,j+1) for j,c in enumerate(seq) if c==i]) for i in range(4)]
pairs=transitive=survivors=mapchecks=0
for a,d in ends:
 B=[b for b in middle if commute(b,d)];C=[c for c in middle if commute(c,a)]
 for b,c in itertools.product(B,C):
  pairs+=1;T=(a,b,c,d)
  if len(set(T))<4 or len(set(orbit_labels(T)))!=1:continue
  transitive+=1
  for i,p in enumerate(T):
   lab=orbit_labels(T[:i]+T[i+1:]);count=sum(x<p[x] and lab[x]!=lab[p[x]] for x in points)
   if count<2:break
  else:
   survivors+=1;f={0:0};stack=[0]
   while stack:
    x=stack.pop()
    for p,q in zip(T,target):
     y=p[x];v=q[f[x]]
     if y in f:assert f[y]==v
     else:f[y]=v;stack.append(y)
   assert len(f)==len(set(f.values()))==9 and f[8]==8
   for p,q in zip(T,target):
    for x in points:assert f[p[x]]==q[f[x]];mapchecks+=1
report={'status':'PASS_INDEPENDENT_ALL_LITERAL_ENDPOINTS','endpoint_pairs':len(ends),'middle_involutions':len(middle),'middle_pairs':pairs,'transitive':transitive,'survivors':survivors,'literal_conjugacy_entries':mapchecks,'normalization_used':False,'seconds':time.monotonic()-start}
print(json.dumps(report));Path('/Users/sasha/medusa/research/leemans/reboot_20261013/L019_nine_anchors_root_review_work/independent_control.json').write_text(json.dumps(report,indent=2)+'\n')
