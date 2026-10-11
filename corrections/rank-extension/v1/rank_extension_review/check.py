from itertools import combinations
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--packet",type=Path,required=True);p.add_argument("--out",type=Path,required=True);args=p.parse_args()
if args.out.exists():raise ValueError("fresh output")
pin="2e182cee7ea5e9148694c8a43244caeebfa1f4bca6993c4dde5cee19bf83ff70"
if hashlib.sha256((args.packet/"manifest.json").read_bytes()).hexdigest()!=pin:raise ValueError("author freeze")
for row in json.loads((args.packet/"manifest.json").read_text())["exports"]:
 blob=(args.packet/row["path"]).read_bytes()
 if len(blob)!=row["bytes"] or hashlib.sha256(blob).hexdigest()!=row["sha256"]:raise ValueError("exact export")
N=10;ONE=tuple(range(1,N+1))
def perm(*cycles):
 p=list(ONE)
 for c in cycles:
  for a,b in zip(c,c[1:]+c[:1]):p[a-1]=b
 return tuple(p)
def mul(p,q):return tuple(q[x-1]for x in p)
def generated(gs):
 seen={ONE:()};todo=[ONE]
 for a in todo:
  for label,g in gs:
   b=mul(a,g)
   if b not in seen:seen[b]=seen[a]+(label,);todo.append(b)
 return seen
def allsub(gs):return [generated([(i,g)for i,g in enumerate(gs)if (mask>>i)&1])for mask in range(1<<len(gs))]
def orbitparts(gs,points):
 remaining=set(points);parts=[]
 while remaining:
  orbit={min(remaining)};todo=list(orbit)
  for a in todo:
   for g in gs:
    b=g[a-1]
    if b not in orbit:orbit.add(b);todo.append(b)
  parts.append(sorted(orbit));remaining-=orbit
 return parts
def require(x,msg):
 if not x:raise ValueError(msg)
old=[perm((1,2),(8,9)),perm((2,3),(6,7)),perm((3,4),(6,7)),perm((4,5))]
new=[old[0],perm((2,10)),perm((3,10),(6,7)),old[2],old[3]]
a=allsub(old);b=allsub(new)
require(len(a[-1])==480 and len(b[-1])==2880,'full group orders')
for gs in [old,new]:
 require(len(set(gs))==len(gs) and all(x!=ONE and mul(x,x)==ONE for x in gs),'distinct nonidentity involutions')
 require(all(mul(gs[i],gs[j])==mul(gs[j],gs[i])for i in range(len(gs))for j in range(len(gs))if abs(i-j)>1),'string commutations')
failed=[]
for par in [a,b]:failed.append([(i,j)for i in range(len(par))for j in range(len(par))if set(par[i])&set(par[j])!=set(par[i&j])])
require(len(failed[0])==0 and len(failed[1])==72,'every subset intersection')
orbits=orbitparts(old,range(1,10));fracture=[]
for i,edge in enumerate([(1,2),(2,3),(3,4),(4,5)]):
 parts=orbitparts([g for j,g in enumerate(old)if j!=i],range(1,10))
 require(len(parts)>len(orbits) and old[i][edge[0]-1]==edge[1] and not any(set(edge)<=set(p)for p in parts),'exact fracture edge')
 fracture.append(dict(label=i,edge=edge,parabolic_orbits=parts))
require(len(fracture[1]['parabolic_orbits'])==len(orbits)+1,'exact split orbit count')
left={1,2,8,9};right={3,4,5,6,7}
require(left|right==set(range(1,10))and not left&right,'whole partition')
require(all(old[0][x-1]==x for x in right)and all(old[j][x-1]==x for j in [2,3]for x in left),'perfect split sides')
require([(x,old[1][x-1])for x in sorted(left)if old[1][x-1]in right]==[(2,3)],'unique cross edge')
require(all(old[1][x-1]==x for x in left-{2}),'alpha trivial')
require(any(g[1]!=2 for j,g in enumerate(old)if j!=1)and any(g[2]!=3 for j,g in enumerate(old)if j!=1),'both endpoints moved')
beta=perm((6,7));I=6;J=24;K=I&J
require(beta in b[I]and beta in b[J]and beta not in b[K],'explicit defect element')
# Independently identify every displayed subgroup as a set of actual permutations.
def parity(g):return sum(g[i]>g[j]for i in range(5)for j in range(i+1,5))%2
def supported(g,points):return all(g[i-1]==i for i in range(1,6)if i not in points)
full=set(a[-1]);formulas={
 'P':(7,{g for g in full if supported(g,{1,2,3,4})and parity(g)==int(g[5]!=6)^int(g[7]!=8)}),
 'Q':(14,{g for g in full if supported(g,{2,3,4,5})and g[7]==8}),
 'M':(6,{g for g in full if supported(g,{2,3,4})and g[7]==8 and parity(g)==int(g[5]!=6)}),
 'left_pair':(3,{g for g in full if supported(g,{1,2,3})and parity(g)==int(g[5]!=6)^int(g[7]!=8)}),
 'right_pair':(12,{g for g in full if supported(g,{3,4,5})and g[7]==8})}
for name,(mask,want)in formulas.items():require(set(a[mask])==want,'actual subgroup formula '+name)
require(set(a[3])&set(a[6])==set(a[2])and set(a[6])&set(a[12])==set(a[4])and set(a[7])&set(a[14])==set(a[6]),'all three end intersections')
result=dict(status='PASS_DISTINCT_LITERAL_T64_COUNTEREXAMPLE',implementation='Pure Python permutation tuples and breadth-first generated subgroups; no author or GAP imports.',old_order=len(a[-1]),new_order=len(b[-1]),old_intersections=256,new_intersections=1024,old_failures=len(failed[0]),new_failures=len(failed[1]),old_orbits=orbits,fracture=fracture,perfect_partition=[sorted(left),sorted(right)],split_label=1,split_edge=[2,3],alpha_identity=True,both_endpoints_moved=True,witness=dict(element='(6 7)',left_labels=[1,2],right_labels=[3,4],left_word=b[I][beta],right_word=b[J][beta],intersection_order=len(set(b[I])&set(b[J])),common_order=len(b[K])),source_credit=0,question_credit=0,interpretation='Literal intransitive Theorem 6.4 only; complete written proof and source review are separate. No main stability theorem disproof.')
result.update(author_manifest_sha256=pin,actual_subgroup_formulas=5,end_intersections=3)
args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
