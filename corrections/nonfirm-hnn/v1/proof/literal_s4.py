"""Independent literal permutation and coset reconstruction of a proposed example."""
import itertools,json
E=tuple(itertools.permutations(range(4)));one=tuple(range(4))
def mul(x,y):return tuple(y[x[i]] for i in range(4))
def inv(x):return tuple(x.index(i) for i in range(4))
def cycle(*xs):
 a=list(one)
 for x,y in zip(xs,xs[1:]+xs[:1]):a[x-1]=y-1
 return tuple(a)
def subgroup(gs):
 seen={one};todo=[one]
 while todo:
  x=todo.pop()
  for y in gs:
   z=mul(x,y)
   if z not in seen:seen.add(z);todo.append(z)
 return frozenset(seen)
def coset(x,H):return frozenset(mul(x,h) for h in H)
def need(x,s):
 if not x:raise ValueError(s)
a=cycle(3,4);b=cycle(1,2);r=mul(cycle(1,3),cycle(2,4));s=mul(cycle(1,4),cycle(2,3));
P=[subgroup([a]),subgroup([b]),subgroup([cycle(1,3),cycle(2,4)]),subgroup([cycle(1,4),cycle(2,3)]),subgroup([a,b,r]),subgroup([r])]
phi=lambda x:mul(mul(b,x),b)
L={frozenset(E)}
for H in P:L|={Q&H for Q in tuple(L)}
need(len(L)==9,'nine exact unlabelled parabolics')
need({frozenset(map(phi,H)) for H in L}==L,'literal source admissibility')
cosets=[tuple({coset(x,H) for x in E}) for H in P]
counts=[0]*7;chambers=[]
def visit(i,flag):
 if i==len(P):
  counts[len(flag)]+=1
  total=set(E)
  for Q in flag:total.intersection_update(Q)
  need(total,'every literal source flag has common representative')
  if len(flag)==6:chambers.append(flag)
  return
 visit(i+1,flag)
 for Q in cosets[i]:
  if all(Q&R for R in flag):visit(i+1,flag+[Q])
visit(0,[])
need(len(chambers)==24,'24 source chambers')
parent=list(range(6))
def find(i):
 while parent[i]!=i:i=parent[i]
 return i
for i,j in itertools.product(range(6),repeat=2):
 if frozenset(map(phi,P[i]))==P[j]:parent[find(i)]=find(j)
classes=sorted([sorted(i+1 for i in range(6) if find(i)==r0) for r0 in {find(i) for i in range(6)}])
need(classes==[[1],[2],[3,4],[5],[6]],'literal named equivalence classes')
K=subgroup([r,s]);need(len(K)==4 and mul(a,b) in K and a not in K and b not in K,'orbit-closure obstruction')
F=[P[0],P[1],coset(a,K)]
need(all(F[i]&F[j] for i,j in itertools.combinations(range(3),2)) and not set.intersection(*map(set,F)),'three pairwise incident output fibers without a common representative')
print(json.dumps(dict(status='LITERAL_FINITE_BASE_CHECK_PASS',group_order=24,subgroup_orders=list(map(len,P)),unlabelled_parabolics=len(L),flag_counts=counts,source_chambers=len(chambers),literal_classes=classes,orbit_closure_order=len(K),failed_output_fiber_sizes=list(map(len,F)),pair_intersection_sizes=[len(F[i]&F[j]) for i,j in itertools.combinations(range(3),2)],triple_intersection_size=len(set.intersection(*map(set,F))),scope='Finite base and fibers checked independently; the passage to the infinite HNN extension requires the separately written semidirect normal-form proof.'),indent=2))
