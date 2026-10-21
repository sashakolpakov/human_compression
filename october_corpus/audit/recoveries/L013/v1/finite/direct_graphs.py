"""Literal adjacency verification and exact paired-partition automorphism search."""
from collections import Counter,deque
from itertools import combinations

def need(v,m):
 if not v:raise ValueError(m)
def check_simple(A):
 n=len(A);A=[set(x) for x in A]
 need(all(all(0<=v<n and v!=u and u in A[v] for v in A[u]) for u in range(n)),'simple symmetric graph')
 return A

def distances(A,start):
 d={start:0};q=deque([start])
 while q:
  u=q.popleft()
  for v in A[u]:
   if v not in d:d[v]=d[u]+1;q.append(v)
 return d

def profile(A):
 A=check_simple(A);n=len(A);girth=None;diam=0;connected=True
 for root in range(n):
  d={root:0};parent={root:-1};q=deque([root])
  while q:
   u=q.popleft()
   for v in A[u]:
    if v not in d:d[v]=d[u]+1;parent[v]=u;q.append(v)
    elif parent[u]!=v and parent[v]!=u:
     length=d[u]+d[v]+1
     if girth is None or length<girth:girth=length
  connected &= len(d)==n;diam=max(diam,max(d.values()))
 return dict(order=n,degrees=sorted(set(map(len,A))),girth=girth,diameter=diam if connected else None,connected=connected)

def valid_map(A,B,p):return sorted(p)==list(range(len(A))) and all({p[v] for v in A[u]}==B[p[u]] for u in range(len(A)))

def isomorphisms(A,B,first=False):
 A=check_simple(A);B=check_simple(B)
 if len(A)!=len(B):return dict(count=0,nodes=0,witness=None)
 count=0;nodes=0;witness=None
 def refine(P,Q):
  while True:
   posP={v:i for i,c in enumerate(P) for v in c};posQ={v:i for i,c in enumerate(Q) for v in c};R=[];S=[]
   for pc,qc in zip(P,Q):
    def buckets(cell,G,pos):
     out={}
     for v in cell:
      counts=Counter(pos[u] for u in G[v]);sig=tuple(counts.get(i,0) for i in range(len(P)));out.setdefault(sig,[]).append(v)
     return out
    bp=buckets(pc,A,posP);bq=buckets(qc,B,posQ)
    if set(bp)!=set(bq) or any(len(bp[k])!=len(bq[k]) for k in bp):return None
    for k in sorted(bp):R.append(bp[k]);S.append(bq[k])
   if len(R)==len(P):return R,S
   P,Q=R,S
 def walk(P,Q):
  nonlocal count,nodes,witness
  nodes+=1;rs=refine(P,Q)
  if rs is None:return False
  P,Q=rs
  if len(P)==len(A):
   p=[None]*len(A)
   for pc,qc in zip(P,Q):p[pc[0]]=qc[0]
   need(valid_map(A,B,p),'literal final permutation');count+=1
   if witness is None:witness=p
   return first
  i=min((i for i,c in enumerate(P) if len(c)>1),key=lambda i:(len(P[i]),i));a=P[i][0]
  PP=P[:i]+[[a],[v for v in P[i] if v!=a]]+P[i+1:]
  for b in Q[i]:
   QQ=Q[:i]+[[b],[v for v in Q[i] if v!=b]]+Q[i+1:]
   if walk(PP,QQ):return True
  return False
 walk([list(range(len(A)))],[list(range(len(A)))])
 return dict(count=count,nodes=nodes,witness=witness)

def generated_order(A,generators):
 A=check_simple(A);n=len(A)
 for g in generators:need(valid_map(A,A,g),'automorphism generator')
 identity=tuple(range(n));seen={identity};q=deque([identity])
 while q:
  g=q.popleft()
  for h in generators:
   x=tuple(h[g[v]] for v in range(n))
   if x not in seen:seen.add(x);q.append(x)
 return len(seen)

def middle_profiles(A):
 A=check_simple(A);out=[]
 for r in range(len(A)):
  d=distances(A,r)
  for c in range(r+1,len(A)):
   if d[c]!=4:continue
   vertices=sorted(set(range(len(A)))-{r,c}-A[r]-A[c]);index={v:i for i,v in enumerate(vertices)}
   H=[{index[w] for w in A[v] if w in index} for v in vertices]
   out.append(dict(pair=[r,c],middle_vertices=vertices,profile=profile(H)))
 return out
