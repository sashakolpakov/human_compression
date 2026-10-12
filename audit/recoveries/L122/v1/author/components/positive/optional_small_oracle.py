#!/usr/bin/env python3
"""Optional independent-coordinate checks of the written small examples."""
import itertools,json

def need(x,m):
 if not x:raise ValueError(m)
def adjacency(n,steps):
 return {(x,y) for x in range(n) for y in range(n) if (y-x)%n in steps}
def connected(vertices,edges):
 v=set(vertices)
 if not v:return True
 seen={next(iter(v))}
 while True:
  nxt=seen|{y for x,y in edges if x in seen and y in v}
  if nxt==seen:return seen==v
  seen=nxt

def run():
 c6=adjacency(6,{1,5});reset=lambda x:(x+(1 if x%2==0 else -1))%6
 need((1,2) in c6 and (reset(1),reset(2)) not in c6,'literal dual reset obstruction')
 v=[0,2,4];rot={(x,y) for x in v for y in v if (x,(y+1)%6) in c6};pol={(x,y) for x in v for y in v if (x,(1-y)%6) in c6}
 need(sum(x==y for x,y in rot)==3 and sum(x==y for x,y in pol)==2,'distinct reductions')
 need(rot != {(y,x) for x,y in rot},'orientation essential')
 c9=adjacency(9,{1,2,7,8});tri=[t for t in itertools.combinations(range(9),3) if all((x,y) in c9 for x,y in itertools.combinations(t,2))]
 need(len(tri)==9 and all(any(x in t and y in t for t in tri) for x,y in c9),'all flags extend')
 need(connected(range(9),c9),'connected empty residue')
 for x in range(9):need(connected([y for y in range(9) if (x,y) in c9],c9),'all vertex residues connected')
 reset=lambda x:(x+(-2 if x%3==2 else 1))%9
 need((2,3) in c9 and (reset(2),reset(3)) not in c9,'literal triality reset obstruction')
 need((3,2) in c9 and (4,0) not in c9,'natural voltage lift obstruction')
 auto=[]
 for p in itertools.permutations(range(9)):
  if all((p[x],p[y]) in c9 for x,y in c9):auto.append(p)
 need(len(auto)==18,'full graph automorphism group')
 thirds=[p for p in auto if p!=tuple(range(9)) and all(p[p[p[x]]]==x for x in range(9))]
 need(len(thirds)==2 and all(all(p[x]%3==x%3 for x in range(9)) for p in thirds),'no order-three type cycle')
 typed=[p for p in auto if all(p[x]%3==x%3 for x in range(9))]
 need(len(typed)==3,'full typed group')
 pair={(x,y) for x,y in c9 if x%3==0 and y%3==1};orbits=[]
 while pair:
  x,y=next(iter(pair));orb={(p[x],p[y]) for p in typed};orbits.append(orb);pair-=orb
 need(len(orbits)==2,'not a coset geometry counterexample')
 # The Mathieu incidence model needs only the retained 3-transitive group input.
 labels=range(12);chambers=list(itertools.permutations(labels,3))
 need(len(chambers)==1320,'all distinct-label chambers')
 for a,b in itertools.permutations(labels,2):need(sum(c[0]==a and c[1]==b for c in chambers)==10,'firm ten-completion panels')
 for x in labels:
  vertices={(i,y) for i in [1,2] for y in labels if y!=x}
  edges={((1,a),(2,b)) for a in labels for b in labels if a!=x and b!=x and a!=b}
  edges|={(b,a) for a,b in list(edges)};need(connected(vertices,edges),'Mathieu model rank-two residue')
 return {'status':'PASS','role':'OPTIONAL_VALIDATION_NOT_PROOF_PREMISE','cycle6_loops':[3,2],'cycle9_chambers':9,'cycle9_full_graph_automorphisms':18,'cycle9_order_three_automorphisms':2,'cycle9_typed_incident_pair_orbits':2,'mathieu_model_chambers':1320,'mathieu_panel_completions':10}
if __name__=='__main__':print(json.dumps(run(),indent=2))
