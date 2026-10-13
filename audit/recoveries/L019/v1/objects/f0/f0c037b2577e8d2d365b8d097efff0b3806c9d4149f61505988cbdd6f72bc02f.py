"""Independent small literal control of the universal one-bridge identity.
No author modules, canonicalizer, finite classification or source-count premise.
"""
import itertools,json,time
from pathlib import Path
if __import__('sys').flags.optimize:raise RuntimeError('normal Python required')
def mul(a,b):return tuple(b[x]for x in a)
def closure(gens,n):
    ident=tuple(range(n));got={ident};todo=[ident]
    while todo:
        a=todo.pop()
        for b in gens:
            c=mul(a,b)
            if c not in got:got.add(c);todo.append(c)
    return frozenset(got)
def allsub(n):
    elems=list(itertools.permutations(range(n)));ident=tuple(range(n));groups={frozenset([ident]):()};todo=[frozenset([ident])]
    while todo:
        H=todo.pop()
        for g in elems:
            if g in H:continue
            G=closure(groups[H]+(g,),n)
            if G not in groups:groups[G]=groups[H]+(g,);todo.append(G)
    return groups
def lift(p,off,n):
    a=list(range(n))
    for i,v in enumerate(p):a[i+off]=v+off
    return tuple(a)
def need(x,s):
    if not x:raise RuntimeError(s)
start=time.monotonic();P=allsub(4);Q=allsub(2);need(len(P)==30 and len(Q)==2,'literal subgroup inventories')
PL=list(P);QL=list(Q);Hs={};bridge=(4,1,2,3,0,5)
for i,p in enumerate(PL):
    for j,q in enumerate(QL):Hs[i,j]=closure(tuple(lift(x,0,6)for x in P[p])+tuple(lift(x,4,6)for x in Q[q])+(bridge,),6)
checks=0
for i0,p0 in enumerate(PL):
 for i1,p1 in enumerate(PL):
  if not p0<=p1:continue
  for j0,q0 in enumerate(QL):
   for j1,q1 in enumerate(QL):
    if not q0<=q1:continue
    need(Hs[i0,j1]&Hs[i1,j0]==Hs[i0,j0],'bridge rectangle');checks+=1
# The diagonal pair couples the anchor orbit and its complement before the bridge.
diag=closure(((1,0,3,2),),4);idx=PL.index(diag);triv=next(j for j,q in enumerate(QL)if len(q)==1)
pure_comp=(0,1,3,2,4,5)
need(pure_comp in Hs[idx,triv],'complementary correlation cancelled by actual bridge')
r={'status':'PASS_INDEPENDENT_LITERAL_BRIDGE_CONTROL','s4_subgroups':len(P),'s2_subgroups':len(Q),'bridge_groups':len(Hs),'nested_rectangle_cases':checks,'diagonal_complement_control':True,'seconds':time.monotonic()-start,'scope':'supplementary control only; universal proof is handwritten'}
Path(__file__).with_name('bridge_report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
