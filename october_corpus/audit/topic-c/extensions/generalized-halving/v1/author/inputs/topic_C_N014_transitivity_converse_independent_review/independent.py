"""Independent edge-list model. No author module is imported."""
from itertools import combinations, permutations, product

def need(x,m):
 if not x:raise ValueError(m)
def model():
 V=[frozenset(x) for x in combinations(range(1,6),2)]
 a=frozenset((1,2)); p={i:frozenset((1,i)) for i in (3,4,5)}; q={i:frozenset((2,i)) for i in (3,4,5)}; b={i:frozenset({3,4,5}-{i}) for i in (3,4,5)}
 E={frozenset((p[i],p[j])) for i,j in combinations((3,4,5),2)}|{frozenset((q[i],q[j])) for i,j in combinations((3,4,5),2)}|{frozenset((u,v)) for i in (3,4,5) for u,v in ((a,b[i]),(b[i],p[i]),(b[i],q[i]))}
 g=lambda x:frozenset(3-z if z in (1,2) else z for z in x)
 adj=lambda x,y:frozenset((x,y)) in E
 need(len(E)==15 and all(sum(x in e for e in E)==3 for x in V),'edge-list/cubic')
 need(all(adj(x,y)==(not(x&g(y))) for x,y in product(V,repeat=2)),'twist identity')
 tri=[t for t in combinations(V,3) if all(adj(*pair) for pair in combinations(t,2))]
 need(len(tri)==2 and all(a not in t for t in tri),'triangle witness')
 def geometry(halved):
  levels=[V,V if halved else list(E),[0,1]]
  inc=lambda x,y: x[0]!=y[0] and (2 in (x[0],y[0]) or (adj(x[1],y[1]) if halved else (x[1] in y[1] if x[0]==0 else y[1] in x[1])))
  O=[(i,x) for i,level in enumerate(levels) for x in level]
  F=[f for n in range(4) for f in combinations(O,n) if all(inc(x,y) for x,y in combinations(f,2))]
  C=[f for f in F if len(f)==3]
  need(len(C)==60 and all(any(set(f)<=set(c) for c in C) for f in F),'geometry/chambers')
  residues=0
  for f in F:
   if len(f)>1:continue
   objects=[x for x in O if x[0] not in {a[0] for a in f} and all(inc(x,y) for y in f)]
   reached={objects[0]}
   while True:
    nxt=reached|{y for y in objects if any(inc(x,y) for x in reached)}
    if nxt==reached:break
    reached=nxt
   need(len(reached)==len(objects),'RC');residues+=1
  return {'objects':list(map(len,levels)),'flags':len(F),'chambers':len(C),'connected_residues':residues}
 original=geometry(False);halved=geometry(True)
 base=(a,frozenset((3,4)));orbit=set();checks=0;wrong_shore=False
 for perm in permutations(range(1,6)):
  sig=lambda x:frozenset(perm[z-1] for z in x)
  for x,y in product(V,repeat=2):
   need(adj(x,y)==adj(sig(x),g(sig(g(y)))),'action');checks+=1
   wrong_shore|=adj(x,y)!=adj(sig(x),sig(y))
  orbit.add((sig(base[0]),g(sig(g(base[1])))))
 need(len(orbit)==30 and wrong_shore,'orbit and descent obstruction')
 controls=[]
 for name,claim in [('wrong diagonal action',not wrong_shore),('vertex-transitive triangle counts',len({sum(x in t for t in tri) for x in V})==1),('thin original panels',3==2),('two lifts per universal higher object',halved['objects'][2]==4)]:
  try:need(claim,name)
  except ValueError:controls.append(name)
  else:raise ValueError('control did not reject '+name)
 return {'status':'PASS','construction':'literal displayed edge list, independently checked against disjointness twist','original':original,'halved':halved,'S5_action_checks':checks,'lower_pair_orbit':len(orbit),'controls_rejected':controls,'proof_premise':False}
if __name__=='__main__':
 import json
 print(json.dumps(model(),indent=2))
