#!/usr/bin/env python3
"""Independent finite hypothesis checks; not a proof of infinite classification."""
import itertools,json,argparse
from collections import deque,Counter
from pathlib import Path

def need(x,s):
 if not x:raise ValueError(s)
def mul(x,y):return tuple(y[i]for i in x)
def group(gens):
 one=tuple(range(len(gens[0])));G={one};q=[one]
 for g in q:
  for s in gens:
   h=mul(g,s)
   if h not in G:G.add(h);q.append(h)
 return G

def auto(r):
 n=len(r[0]);out=[]
 for z in range(n):
  f={0:z};q=[0];good=True
  for x in q:
   for s in r:
    if s[x]in f:
     if f[s[x]]!=s[f[x]]:good=False;break
    else:f[s[x]]=s[f[x]];q.append(s[x])
   if not good:break
  if good and len(f)==n and len(set(f.values()))==n:out.append(tuple(f[i]for i in range(n)))
 return out

def commuting_matchings(p):
 def rec(left,match):
  if not left:yield tuple(match);return
  i=min(left)
  # A self orbit would repeat color0 or be fixed, so is correctly absent.
  for j in sorted(left-{i}):
   for b in [0,1]:
    v=match[:]
    for e in [0,1]:v[2*i+e]=2*j+(e^b);v[2*j+(e^b)]=2*i+e
    yield from rec(left-{i,j},v)
 yield from rec(set(range(p)),[-1]*(2*p))

def one_face():
 rows=[]
 for p in range(2,9):
  n=2*p;a=tuple(x^1 for x in range(n));b=tuple((x+1)%n if x%2 else(x-1)%n for x in range(n));D=group([a,b]);need(len(D)==n,'polygon group');counts=Counter();valid=0;tested12=0
  for c in commuting_matchings(p):
   if any(c[x]==b[x]for x in range(n)):continue
   valid+=1;aut=auto([a,b,c]);orbits=n//len(aut)
   if orbits>2:continue
   images={g[0]for g in aut};kind=tuple(i for i,s in enumerate([a,b,c])if s[0]in images);counts[str(kind)]+=1
   if orbits==2:
    need(kind in [(1,),(1,2),(0,2)],'excluded two-orbit type occurred')
    if kind==(1,2):
     w=next(g for g in D if g[0]==c[0]);awa=mul(mul(a,w),a)
     need(all(c[x]==(w[x]if x in images else awa[x])for x in range(n)),'exact polygon formula');need(mul(w,w)==tuple(range(n))and w[0]in images,'color-preserving involution');tested12+=1
  rows.append(dict(p=p,all_simple_commuting_matchings=valid,at_most_two_orbit_types=dict(counts),literal_12_formula_checks=tested12))
 return rows

def nonorientable():
 def perm(*cycles):
  a=list(range(4))
  for cyc in cycles:
   for i,j in zip(cyc,cyc[1:]+cyc[:1]):a[i]=j
  return tuple(a)
 a=perm((0,1));b=perm((1,2));c=perm((0,1),(2,3));one=tuple(range(4));G=group([a,b,c]);rot=group([mul(a,b),mul(b,c)]);H=[group([b,c]),group([a,c]),group([a,b])];intersection=set.intersection(*H);S={mul(mul(a,b),g)for g in H[0]}&H[1]&H[2]
 need(len(G)==24 and rot==G and intersection=={one}and a in S,'faithful nonorientable control')
 return dict(group='S4',marks=['(12)','(23)','(12)(34)'],order=len(G),rotation_group_order=len(rot),chain_stabilizer_order=len(intersection),S_size=len(S),rho0_in_S=True,meaning='Disproves extending the orientable H=1 and S=empty criterion to nonorientable regular maniplexes; does not contradict Proposition4.14.')

def cube():
 vertices=list(itertools.product([-1,1],repeat=3));faces={i:[t for t in itertools.product([-1,0,1],repeat=3)if t.count(0)==i]for i in [0,1,2]}
 def le(a,b):return all(y==0 or x==y for x,y in zip(a,b))
 def merged(v):return ('identified',)if v in [(-1,-1,-1),(1,1,1)]else v
 flags=[(merged(v),e,f)for v in vertices for e in faces[1]if le(v,e)for f in faces[2]if le(e,f)];need(len(flags)==len(set(flags))==48,'no identified flags');ix={x:i for i,x in enumerate(flags)};r=[]
 for rank in range(3):
  rr=[]
  for x in flags:
   ys=[y for y in flags if y!=x and all(y[j]==x[j]for j in range(3)if j!=rank)];need(len(ys)==1,'thin merged cube');rr.append(ix[ys[0]])
  r.append(tuple(rr))
 def comps(colors,subset):
  left=set(subset);out=[]
  while left:
   seen={next(iter(left))};q=list(seen)
   for x in q:
    for i in colors:
     y=r[i][x]
     if y in left and y not in seen:seen.add(y);q.append(y)
   out.append(seen);left-=seen
  return out
 need(len(comps(range(3),range(48)))==1,'connected flag graph')
 rank_counts=[];stars={}
 for i in range(3):
  cc=comps([j for j in range(3)if j!=i],range(48));rank_counts.append(len(cc))
  for label in set(x[i]for x in flags):stars[str((i,label))]=len(comps([j for j in range(3)if j!=i],[k for k,x in enumerate(flags)if x[i]==label]))
 need(rank_counts==[8,12,6]and sorted(stars.values()).count(2)==1 and max(stars.values())==2,'exact split face and no other defect')
 return dict(original_rank_counts=[7,12,6],reconstructed_rank_counts=rank_counts,flags=48,disconnected_stars=1,merged_star_components=2,meaning='Thin and globally flag-connected is insufficient: the natural reconstruction splits the identified vertex exactly as the face-star theorem predicts.')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');d=dict(status='PASS_INDEPENDENT_FINITE_HYPOTHESIS_CHECKS',polygon=one_face(),nonorientable=nonorientable(),reconstruction=cube(),scope='Finite controls support the distinct complete written proof review; no finite sample is used to prove a uniform or infinite theorem. No author model module imported.');a.out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
if __name__=='__main__':main()
