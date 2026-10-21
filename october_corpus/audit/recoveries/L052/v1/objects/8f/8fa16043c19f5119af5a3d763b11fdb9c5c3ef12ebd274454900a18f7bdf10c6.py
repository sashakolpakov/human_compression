"""Literal checks of the new A6 deduction and the left/right coset join."""
import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from pathlib import Path
import itertools,json
def compose(a,b):return tuple(a[b[i]]for i in range(len(a)))
def inv(a):return tuple(a.index(i)for i in range(len(a)))
def perm(n,pairs):
 a=list(range(n))
 for i,j in pairs:a[i-1],a[j-1]=a[j-1],a[i-1]
 return tuple(a)
def closure(gens,n):
 e=tuple(range(n));seen={e};todo=[e]
 while todo:
  a=todo.pop()
  for b in gens:
   c=compose(a,b)
   if c not in seen:seen.add(c);todo.append(c)
 return seen
r=[perm(6,x)for x in [[(1,2),(3,4)],[(2,6),(3,5)],[(1,4),(2,3)],[(1,4),(3,5)]]]
assert all(compose(x,x)==tuple(range(6))for x in r)
assert len(closure(r,6))==360
def group(s):return closure([r[i]for i in s],6)
def even(s):return closure([compose(r[i],r[j])for i in s for j in s],6)
I=(0,2,3);J=(0,1,3);K=(0,3)
gi,gj,gk=map(group,[I,J,K]);hi,hj,hk=map(even,[I,J,K])
assert hi==gi and hj==gj
assert len(gi)==len(gj)==60 and gi&gj==gk and len(gk)==10
assert hi&hj==gk and len(hk)==5 and r[0]in hi&hj and r[0]not in hk
alpha=[tuple(range(6))]+[compose(r[0],x)for x in r[1:]]
def difference(s):return closure([compose(inv(alpha[i]),alpha[j])for i in s for j in s],6)
assert all(even(s)==difference(s)for s in[I,J,K])
# Check the convention change literally for all subgroup cosets in S3.
G=set(itertools.permutations(range(3)));e=tuple(range(3));subgroups={frozenset([e]),frozenset(G)}
for a in G:
 for b in G:subgroups.add(frozenset(closure([a,b],3)))
objects=[]
for P in subgroups:
 cosets={frozenset(compose(p,g)for p in P)for g in G}
 for c in cosets:
  inversion=frozenset(inv(x)for x in c);g=next(iter(c))
  assert inversion==frozenset(compose(inv(g),p)for p in P)
  objects.append((c,inversion))
pairs=0
for a,b in itertools.product(objects,repeat=2):assert bool(a[0]&b[0])==bool(a[1]&b[1]);pairs+=1
report=dict(status='PASS_INDEPENDENT_A6_CORRECTION_AND_COSET_INVERSION',A6_order=360,parabolic_orders=[60,60],intersection_order=10,required_rotation_order=5,literal_witness=list(r[0]),pair_difference_equalities=3,S3_subgroups=len(subgroups),typed_cosets=len(objects),incidence_pairs=pairs,author_code_imported=False,classification_census_repeated=False)
Path(__file__).with_name('independent_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
