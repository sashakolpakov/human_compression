#!/usr/bin/env python3
"""Literal source construction on the point-doubled affine plane of order three."""
import argparse,itertools,json,pathlib

def need(ok,s):
 if not ok:raise RuntimeError('PHASE265_REJECT '+s)
def component(adj,start):
 seen={start};todo=[start]
 for x in todo:
  for y in adj[x]:
   if y not in seen:seen.add(y);todo.append(y)
 return seen

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=pathlib.Path,required=True);args=ap.parse_args()
 need(not args.out.exists() and not args.out.is_symlink(),'fresh output')
 base=list(itertools.product(range(3),repeat=2))
 lines=[frozenset(i for i,(x,y) in enumerate(base) if x==b) for b in range(3)]
 lines += [frozenset(i for i,(x,y) in enumerate(base) if (y-a*x-b)%3==0) for a,b in itertools.product(range(3),repeat=2)]
 pts=list(itertools.product(range(9),range(2)))
 inc=lambda p,L:pts[p][0] in lines[L]
 flags=[(p,L) for p in range(18) for L in range(12) if inc(p,L)]
 need(len(flags)==72,'input flags')
 input_adj=[set() for _ in range(30)]
 for p,L in flags:input_adj[p].add(18+L);input_adj[18+L].add(p)
 need(len(component(input_adj,0))==30,'input connected')
 p0,p1=0,1;two=sorted(input_adj[p0])[:2]
 need(len(two)==2 and all(L in input_adj[p1] for L in two),'literal input four-cycle')
 vertices=[(p,L,i) for i in range(3) for p,L in flags];index={v:i for i,v in enumerate(vertices)}
 adj=[set() for _ in vertices]
 for x,(p,L,i) in enumerate(vertices):
  for q,M in flags:
   if inc(p,M) and not inc(q,L):
    y=index[q,M,(i+1)%3];adj[x].add(y);adj[y].add(x)
 need(len(component(adj,0))==216,'whole triangle geometry connected')
 parts=[set(range(i*72,(i+1)*72)) for i in range(3)]
 chambers=set();panels=set()
 for x in parts[0]:
  for y in adj[x]&parts[1]:
   last=adj[x]&adj[y]&parts[2];need(len(last)==4,'panel size four')
   for z in last:chambers.add((x,y,z))
 for i,j in [(0,1),(0,2),(1,2)]:
  for x in parts[i]:
   for y in adj[x]&parts[j]:panels.add(len(adj[x]&adj[y]&parts[3-i-j]))
 need(len(chambers)==3456 and panels=={4},'all chambers and panels')
 for x in range(216):
  residue=adj[x];local={y:adj[y]&residue for y in residue}
  need(len(residue)==24 and {len(v) for v in local.values()}=={4},'literal residue parameters')
  need(component(local,next(iter(local)))==residue,'every rank-two residue connected')
 # Coordinate affine generators plus independent original-point clone swaps.
 basegens=[]
 maps=[lambda x,y:((x+1)%3,y),lambda x,y:(x,(y+1)%3),
       lambda x,y:((x+y)%3,y),lambda x,y:(y,x),lambda x,y:((-x)%3,y)]
 for f in maps:basegens.append([base.index(f(*v)) for v in base])
 gens=[]
 for g in basegens:
  lg=[lines.index(frozenset(g[x] for x in L)) for L in lines]
  gens.append([index[pts.index((g[pts[p][0]],pts[p][1])),lg[L],i] for p,L,i in vertices])
 for a in range(9):
  gens.append([index[pts.index((pts[p][0],1-pts[p][1] if pts[p][0]==a else pts[p][1])),L,i] for p,L,i in vertices])
 for g in gens:
  need(sorted(g)==list(range(216)),'actual permutations')
  need(all({g[y] for y in adj[x]}==adj[g[x]] for x in range(216)),'literal incidence automorphisms')
 orbit={next(iter(chambers))};todo=list(orbit)
 for C in todo:
  for g in gens:
   D=tuple(g[x] for x in C)
   need(D in chambers,'chamber preservation')
   if D not in orbit:orbit.add(D);todo.append(D)
 need(orbit==chambers,'full chamber transitivity')
 report=dict(status='PASS',input=dict(points=18,lines=12,incidences=72,girth=4,four_cycle=[p0,two[0],p1,two[1]],has_repeated_neighborhoods=True),
  triangle=dict(vertices=216,vertices_per_type=72,edges=sum(map(len,adj))//2,chambers=len(chambers),panel_sizes=sorted(panels),rank_two_residues_checked=216,residue_vertices=24,residue_degrees=4,whole_graph_connected=True,chamber_orbit=len(orbit)),
  scope='Literal finite counterexample to the unrestricted gonality-two speculation; twin-free and gonality-three questions are untouched.')
 args.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
