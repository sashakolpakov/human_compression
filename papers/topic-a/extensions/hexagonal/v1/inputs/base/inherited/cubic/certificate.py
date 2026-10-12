"""Complete bounded affine certificate; no parameter-dependent group census."""
from collections import deque
from itertools import combinations
import json
I=((1,0,0),(0,1,0),(0,0,1)); Z=(0,0,0); ONE=(I,Z)
W=((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1))
def mv(a,v):return tuple(sum(x*y for x,y in zip(row,v)) for row in a)
def mm(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def mul(x,y):
 a,u=x;b,v=y;return mm(a,b),tuple(i+j for i,j in zip(u,mv(a,v)))
def inv(x):
 a,u=x;b=tuple(zip(*a));return b,tuple(-v for v in mv(b,u))
def power(x,n):
 y=ONE
 for _ in range(n):y=mul(y,x)
 return y
def word(w,r):
 x=ONE
 for i in w:x=mul(x,r[i-1] if i>0 else inv(r[-i-1]))
 return x
def close(gs,limit=100):
 seen={ONE};todo=deque([ONE])
 while todo:
  x=todo.popleft()
  for y in gs:
   z=mul(x,y)
   if z not in seen:
    seen.add(z);todo.append(z)
    if len(seen)>limit:raise ValueError('unexpected subgroup bound')
 return seen
R=[(((0,1,0),(1,0,0),(0,0,1)),Z),(((1,0,0),(0,0,1),(0,1,0)),Z),(((0,-1,0),(-1,0,0),(0,0,-1)),(0,0,1)),(((0,-1,0),(-1,0,0),(0,0,1)),Z)]
def ensure(t,msg):
 if not t:raise ValueError(msg)
def determinant(a):return sum(a[0][i]*(a[1][(i+1)%3]*a[2][(i+2)%3]-a[1][(i+2)%3]*a[2][(i+1)%3]) for i in range(3))
def kernel_check(k):
 ensure(k['linear_order']==48 and k['kernel_generators']==3,'kernel dimensions')
 rr=k['kernel_relators'];pairs=[]
 for r in rr:
  ensure(len(r)==4 and r[0]==-r[2] and r[1]==-r[3] and abs(r[0])!=abs(r[1]),'literal commutator presentation')
  pairs.append(tuple(sorted((abs(r[0]),abs(r[1])))))
 ensure(sorted(pairs)==[(1,2),(1,3),(2,3)],'all and only three commutators')
 vals=[word(w,R) for w in k['basis_words']]
 ensure(len(vals)==3 and all(a==I for a,u in vals),'kernel word images')
 basis=[u for a,u in vals];ensure(abs(determinant(basis))==2,'whole D3 basis')
 return basis

def plane(g,i,k,s):
 a,v=g;y=mv(a,W[i]);epsilon=1 if y in W else -1
 j=W.index(tuple(epsilon*t for t in y));num=epsilon-1+2*sum(x*y for x,y in zip(W[j],v))
 ensure(num%4==0,'plane level integrality')
 return j,(epsilon*k+num//4)%s

def cpr_edges(s):
 e=[[] for _ in range(4)];e[3].append((0,1));prev=1
 for b in range(s-1):
  l=2+4*b;u=l+1;d=l+2;r=l+3;e[1].append((prev,l))
  if b%2==0:e[0]+=[(l,u),(d,r)];e[2]+=[(l,d),(u,r)]
  else:e[3]+=[(l,u),(d,r)];e[2]+=[(l,r),(u,d)]
  prev=r
 e[1].append((prev,4*s-2));e[3 if s%2==0 else 0].append((4*s-2,4*s-1))
 if s%2:e[2].append((4*s-2,4*s-1))
 return e

def cpr_labels(s):
 v=[(0,0),(3,0)]
 for b in range(s-1):
  h=b//2
  if b%2==0:v += [(2,h),(1,h),(1,-h-1),(2,-h-1)]
  else:v += [(3,-h-1),(0,-h-1),(0,h+1),(3,h+1)]
 v += [(3,s//2),(0,s//2)] if s%2==0 else [(2,s//2),(1,s//2)]
 return [(i,k%s) for i,k in v]

def audit(k):
 basis=kernel_check(k)
 for r in R:ensure(power(r,2)==ONE,'involution')
 orders={}
 for i,j in combinations(range(4),2):
  n=next(n for n in range(1,13) if power(mul(R[i],R[j]),n)==ONE);orders[f'{i}{j}']=n
 ensure(list(orders.values())==[3,2,2,6,3,2],'pair orders')
 u=word([1,2,3,2,3,2],R);v=word([4,2,3,2,3,2],R)
 ensure(u==(I,(1,-1,0)) and power(v,2)==ONE,'literal source period words')
 q=close([(a,Z) for a,v in R]);ensure(len(q)==48,'whole signed permutation group')
 roots={mv(a,u[1]) for a,v in q}
 ensure(len(roots)==12 and all(sum(x)%2==0 for x in roots),'D3 root orbit')
 ensure(all(x in roots for x in [(1,-1,0),(0,1,-1),(0,1,1)]),'D3 root basis')
 H={m:close([R[i] for i in range(4) if m>>i&1]) for m in range(15) if m!=7}
 Q={m:{a for a,v in h} for m,h in H.items()};Q7={a for a,v in close([(R[i][0],Z) for i in [0,1,2]])}
 ensure(len(Q7)==12,'infinite parabolic linear image')
 diffbound=0
 for m,h in H.items():
  ensure(len(h)==len(Q[m]),'faithful finite linear image')
  for n,t in H.items():
   ensure(h&t==H[m&n],'all finite support intersections')
   for a,u in h:
    for b,v in t:
     if a==b:diffbound=max(diffbound,*(abs(x-y) for x,y in zip(u,v)))
  ensure(Q[m]&Q7==Q[m&7],'all infinite/finite linear intersections')
  for a,v in h:
   if a in Q7:ensure(sum(v)==(0 if sum(a[0])==1 else 1),'actual infinite fiber sum')
 ensure(diffbound==1,'uniform quotient exclusion bound')
 locals=[]
 for m in [7,11,13,14]:
  x,y,z=[H[m^(1<<i)] for i in range(4) if m>>i&1]
  yz={mul(a,b) for a in y for b in z};lhs={mul(a,b) for a in x&y for b in x&z}
  ensure(x&yz==lhs,'rank-three coset Helly')
  bound=max(abs(i-j) for a,u in x for b,v in yz if a==b for i,j in zip(u,v))
  ensure(bound<=1,'rank-three Helly survives every s>=3')
  locals.append({'support':m,'rhs_product_size':len(yz),'intersection_size':len(lhs),'difference_bound':bound})
 reps=[ONE,R[3],word([2,4],R),word([1,2,4],R)]
 ensure(set().union(*[{mul(t,h) for h in H[3]} for t in reps])==H[11],'complete S4 four-coset decomposition')
 examples=[]
 for s in range(3,13):
  labels=cpr_labels(s);ensure(len(set(labels))==4*s,'complete CPR labeling')
  edges=cpr_edges(s)
  for t in range(4):
   want={tuple(sorted((labels.index(plane(R[t],i,k,s)),j))) for j,(i,k) in enumerate(labels) if plane(R[t],i,k,s)!=(i,k)}
   ensure(want=={tuple(sorted(x)) for x in edges[t]},'literal CPR comparison')
  orb={plane(g,0,0,s) for g in H[14]}
  ensure(orb=={(0,0),(3,0),(2,0),(1,s-1)},'four-element forbidden-coset orbit')
  ensure(plane(reps[3],0,0,s)==(1,0) and (1,0) not in orb,'bad coset empty')
  examples.append(s)
 # Necessary range control: the same 4s action is not faithful at s=2.
 bad=(tuple(tuple(-a for a in row) for row in I),(1,1,-1))
 ensure(all(plane(bad,i,k,2)==(i,k) for i in range(4) for k in range(2)) and bad[0]!=I,'s2 nonfaithfulness control')
 return {'status':'PASS','kernel_translation_basis':basis,'linear_order':48,'pair_orders':orders,'finite_support_orders':{str(m):len(h) for m,h in H.items()},'finite_pair_intersections':196,'uniform_difference_bound':diffbound,'local_Helly':locals,'CPR_diagnostic_periods':examples,'CPR_diagnostics_are_uniform_proof':False,'uniform_proof':'cubic_family.tex','s2_action_nonfaithful_control':True}
