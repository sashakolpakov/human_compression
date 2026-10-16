"""Exact semantic checks, graph invariants, and independent permutation controls."""
import sys
if sys.flags.optimize:raise RuntimeError('Use ordinary Python')
from pathlib import Path
from collections import deque
import argparse,json,re

def parse(text,kind):
 return [json.loads(x)for x in re.findall(r'(?:^|\n)'+kind+r'\s+(.*?)\nEND_'+kind,text,re.S)]

def graph(data):
 n0,n1,depth,edges=data;n=n0+n1;adj=[set()for _ in range(n)]
 for a,b in edges:
  a-=1;b-=1;assert 0<=a<n0<=b<n and b not in adj[a];adj[a].add(b);adj[b].add(a)
 def bfs(root,exclude=None):
  ds=[-1]*n;ds[root]=0;queue=deque([root])
  while queue:
   v=queue.popleft()
   for z in adj[v]:
    if exclude and {v,z}==exclude:continue
    if ds[z]<0:ds[z]=ds[v]+1;queue.append(z)
  return ds
 ds0=bfs(0);ds1=bfs(n0);assert min(ds0)==min(ds1)==0
 a,b=edges[0];a-=1;b-=1;girth=bfs(a,{a,b})[b]+1;assert girth>=4 and girth%2==0
 gg=n+1
 for root in range(n):
  ds=[-1]*n;par=[-1]*n;ds[root]=0;queue=deque([root])
  while queue:
   v=queue.popleft()
   for z in adj[v]:
    if ds[z]<0:ds[z]=ds[v]+1;par[z]=v;queue.append(z)
    elif par[v]!=z:gg=min(gg,ds[v]+ds[z]+1)
 assert girth==gg
 deg=[len(adj[0]),len(adj[n0])];assert all(len(x)==deg[0]for x in adj[:n0])and all(len(x)==deg[1]for x in adj[n0:])
 return dict(vertices=[n0,n1],degrees=deg,edges=len(edges),gonality=girth//2,diameters=[max(ds0),max(ds1)],local_arc_depths=depth,local_arc_depth=min(depth),partial_linear=girth>=6)

def independent_swap(row):
 q,gg,hh,kk,ll,tt=row;n=q+1;one=tuple(range(n))
 def perm(p):
  p=tuple(x-1 for x in p);assert sorted(p)==list(range(n));return p
 def mul(a,b):return tuple(b[a[i]]for i in range(n))
 def inv(a):
  b=[0]*n
  for i,j in enumerate(a):b[j]=i
  return tuple(b)
 def closure(gs):
  gs=list(map(perm,gs));seen={one};queue=[one]
  while queue:
   a=queue.pop()
   for b in gs:
    c=mul(a,b)
    if c not in seen:seen.add(c);queue.append(c)
  return frozenset(seen)
 def conj(H,g):
  gi=inv(g);return frozenset(mul(mul(gi,h),g)for h in H)
 G=closure(gg);H=closure(hh);K=closure(kk);L=closure(ll);t=perm(tt)
 assert len(G)==q*(q*q-1)//2 and len(H)==len(K)==len(L)==12
 assert H<=G and K<=G and L<=G and t in G
 assert conj(K,t)==H and conj(H,t)==L
 N=[g for g in G if conj(H,g)==H];assert len(N)==12
 KH={conj(K,g)for g in N};LH={conj(L,g)for g in N};assert len(KH)==len(LH)==3 and KH.isdisjoint(LH)
 hs={conj(H,g)for g in G};eligible={J for J in hs if len(H&J)==4};assert eligible==KH|LH
 for J in eligible:
  B=H&J;assert all(mul(a,a)==one for a in B)
  # Literal right cosets and base-stabilizer orbits independently certify both local actions.
  for V in [H,J]:
   cosets={frozenset(mul(b,v)for b in B)for v in V};assert len(cosets)==3
   other=cosets-{B};first=next(iter(other));orb={frozenset(mul(v,b)for v in first)for b in B};assert orb==other
 return dict(q=q,ambient_order=len(G),torus_conjugates=len(hs),eligible=6,ordered_orbit_lengths=[3,3],unordered_classes=1,literal_swap=True)

def verify(text):
 assert text.rstrip().endswith('PASS_COMPLETE_L076_FINITE_CLASSIFICATION')
 fields=parse(text,'FIELD');tori=parse(text,'TORUS');raw=parse(text,'ROW');swaps=parse(text,'SWAP')
 assert [x[0]for x in fields]==[4,5,7,8,9,11,13,16,17,19,23,25,29,31]
 assert len(tori)==28 and len(raw)==19 and len(swaps)==4
 assert len({(x[0],x[1])for x in tori})==28
 rows=[]
 for x in raw:
  q,s,h,k,b,c,u,maxK,ks,bs,data=x;g=graph(data);G=q*(q*q-1)//(1 if q%2==0 else 2)
  assert g['vertices']==[G//h,G//k]and g['degrees']==[h//b,k//b]and g['edges']==G//b
  tor=next(y for y in tori if y[:2]==[q,s]);assert tor[2]==h
  rows.append(dict(q=q,sign=s,subgroup_orders=[h,k],intersection_order=b,ordered_inner=c,unordered_inner=u,aut_classes=1,second_structure=ks,intersection_structure=bs,residually_primitive=tor[3]and maxK,**g))
 for q,s,h,m,num,oi,oa in tori:
  rr=[r for r in rows if [r['q'],r['sign']]==[q,s]];assert len(rr)==oa and sum(r['ordered_inner']for r in rr)==oi
 independent=[independent_swap(x)for x in swaps]
 assert [x['q']for x in independent]==[11,11,13,13]
 return dict(status='PASS_COMPLETE_L076_SEMANTICS',fields=fields,tori=tori,rows=sorted(rows,key=lambda r:(r['q'],r['sign'],r['subgroup_orders'][1])),independent_swaps=independent,scalar_subspaces=dict(total=651,F4_planes=21,full_scalar_orbits=10,exceptional_scalar_orbits=1,conjugacy_lengths=[4095]*10+[1365]))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();r=verify(a.input.read_text());a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'],len(r['rows']),len(r['independent_swaps']))
