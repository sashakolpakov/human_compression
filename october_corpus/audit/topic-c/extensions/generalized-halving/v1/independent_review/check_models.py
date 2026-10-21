"""Independent bounded models for the new residue-transport interface.
No author imports; diagnostics are not uniform proof premises.
"""
from itertools import combinations,product,permutations
import json,argparse

def need(t,m):
 if not t:raise ValueError(m)
def comps(vertices,edges):
 rem=set(vertices); out=[]
 while rem:
  start=min(rem); got={start}; todo=[start];rem.remove(start)
  while todo:
   x=todo.pop()
   for e in edges:
    if x in e:
     for y in e:
      if y in rem:rem.remove(y);got.add(y);todo.append(y)
  out.append(frozenset(got))
 return out
def dc(S,E):
 return comps({2*x+b for x in S for b in (0,1)},[{2*x,2*y+1} for x,y in E if x in S and y in S]+[{2*x+1,2*y} for x,y in E if x in S and y in S])
def subsets(items):
 for r in range(len(items)+1):yield from combinations(items,r)
def intersect_sets(seq,whole):
 out=set(whole)
 for s in seq:out.intersection_update(s)
 return frozenset(out)
def connected_with_edge(S,E):
 return len(S)>=2 and len(comps(S,[{x,y} for x,y in E if x in S and y in S]))==1

def run():
 counts={'families':0,'compatible_lift_flags':0,'pc_families':0,'restriction_bijections':0,'incidence_pairs':0,'pc_failures':0}
 models=[('C4',4,[(i,(i+1)%4) for i in range(4)]),('C5',5,[(i,(i+1)%5) for i in range(5)]),('K4',4,list(combinations(range(4),2))),('diamond',4,[(0,1),(0,2),(1,2),(0,3),(1,3)]),('two_triangles_square',6,[(0,1),(1,2),(2,3),(3,0),(0,4),(1,4),(2,5),(3,5)])]
 bad=False
 for name,n,E in models:
  V=frozenset(range(n)); C=dc(V,E)[0]
  subs=[frozenset(S) for S in subsets(tuple(V)) if connected_with_edge(S,E)]
  parts={S:[c for c in dc(S,E) if c<=C] for S in subs}
  nonbip={S:len(dc(S,E))==1 for S in subs}
  # The three higher types form one base flag; every subflag shadow is connected.
  for fam in combinations(subs,3):
   subkeys=list(subsets((0,1,2)))
   common={F:intersect_sets((fam[i] for i in F),V) for F in subkeys}
   if not all(connected_with_edge(S,E) for S in common.values()):continue
   counts['families']+=1
   pc=all(not all(nonbip[fam[i]] for i in F) or len(dc(common[F],E))==1 for F in subkeys if F)
   counts['pc_families']+=int(pc)
   for F in subkeys:
    for chosen in product(*(parts[fam[i]] for i in F)):
     if not all(x&y for x,y in combinations(chosen,2)):continue
     W=intersect_sets(chosen,C); S=common[F]
     counts['compatible_lift_flags']+=1
     need(bool(W),'flag intersection nonempty')
     Ds=dc(S,E)
     if F and all(nonbip[fam[i]] for i in F):
      need(W==frozenset.union(*Ds),'all nonbipartite constituents keep both sheets')
     else:need(W in Ds,'bipartite constituent selects one component')
     if W not in Ds:bad=True;counts['pc_failures']+=1
     if not pc:continue
     need(W in Ds,'PC produces one local component')
     remaining=[i for i in range(3) if i not in F]
     good={}
     for i in remaining:
      good[i]=[c for c in parts[fam[i]] if all(c&d for d in chosen)]
      local=[d for d in dc(S&fam[i],E) if d<=W]
      restrictions=[c&W for c in good[i]]
      need(len(restrictions)==len(set(restrictions)) and set(restrictions)==set(local),'component restriction bijection')
      counts['restriction_bijections']+=1
     for i,j in combinations(remaining,2):
      for a,b in product(good[i],good[j]):
       need(bool(a&b)==bool(a&b&W),'higher incidence survives restriction')
       counts['incidence_pairs']+=1
 need(bad,'without-PC negative model present')
 # Fresh literal twisted Petersen graph, with the S5 shore action checked directly.
 V=list(combinations(range(5),2)); twist=(1,0,2,3,4)
 act=lambda p,X:tuple(sorted(p[x] for x in X))
 Q={frozenset((X,Y)) for X,Y in combinations(V,2) if not(set(X)&set(act(twist,Y)))}
 adj=lambda X,Y:frozenset((X,Y)) in Q
 need(len(Q)==15 and len(comps(V,Q))==1,'twisted graph connected cubic size')
 tri={X:sum(adj(X,Y) and adj(X,Z) and adj(Y,Z) for Y,Z in combinations([Y for Y in V if Y!=X],2)) for X in V}
 need(set(tri.values())=={0,1},'triangle obstruction to original transitivity')
 lower=[(X,Y) for X in V for Y in V if adj(X,Y)]
 orbit=set(); base=lower[0]
 for p in permutations(range(5)):
  other=lambda Y:act(twist,act(p,act(twist,Y)))
  need(all(adj(act(p,X),other(Y)) for X,Y in lower),'conjugated second-shore action')
  orbit.add((act(p,base[0]),other(base[1])))
 need(orbit==set(lower),'transformed lower-flag transitivity')
 # Wrong shared-shore action fails for some S5 permutation, so descent is not inferred.
 need(any(any(not adj(act(p,X),act(p,Y)) for X,Y in lower) for p in permutations(range(5))),'same-shore-action negative control')
 return {'status':'PASS','residue_models':counts,'twist_vertices':10,'twist_edges':15,'lifted_lower_flags':len(lower),'transformed_chambers':len(lower)*2,'negative_models':['all-nonbipartite shadows can have two-component common cover without PC','common S5 shore action need not descend to the original graph'],'uniform_proof_by_enumeration':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();r=run();open(a.out,'w').write(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
