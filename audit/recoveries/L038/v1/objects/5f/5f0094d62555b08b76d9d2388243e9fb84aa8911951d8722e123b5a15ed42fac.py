#!/usr/bin/env python3
"""Separate exact matrix enumeration and literal graph checks for L037.

No GAP or author module is imported. All matrix parabolics are explicit sets.
The finite checks validate examples, not the written infinite-family induction.
"""
from pathlib import Path
from itertools import product,permutations
import argparse,hashlib,json,math
PIN='79d9cdf2723db2ba8e7729f1333fa918f241265db95e98d5e681b632fe01f489'
def need(b,s):
 if not b:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
I=tuple(int(i==j) for i in range(4) for j in range(4))
def mul(a,b):return tuple(sum(a[4*i+k]*b[4*k+j] for k in range(4))%3 for i in range(4) for j in range(4))
def trans(a):return tuple(a[4*j+i] for i in range(4) for j in range(4))
def closure(xs):
 found={I};todo=[I]
 while todo:
  a=todo.pop()
  for g in xs:
   b=mul(a,g)
   if b not in found:found.add(b);todo.append(b)
 return frozenset(found)
def order(g):
 h=I
 for k in range(1,1441):
  h=mul(h,g)
  if h==I:return k
 raise ValueError('matrix order not reached')
def ip(xs):
 n=len(xs);sub={i:closure([x for j,x in enumerate(xs) if i>>j&1]) for i in range(1<<n)};tests=0
 for i in sub:
  for j in sub:
   if j<i:continue
   need(sub[i]&sub[j]==sub[i&j],'explicit-set intersection');tests+=1
 return sub,tests
F=(1,1,0,0,1,2,1,0,0,1,1,2,0,0,2,1)
X=[(2,0,0,0,1,1,0,0,0,0,1,0,0,0,0,1),(2,1,0,0,0,1,0,0,0,1,2,0,0,0,0,2),(1,0,0,0,0,1,1,0,0,0,2,0,0,0,2,1),(2,0,0,0,0,2,0,0,0,0,2,1,0,0,0,1)]
def compose(a,b):return tuple(b[a[i]] for i in range(len(a)))
def perm_order(a):
 value=1;seen=set()
 for i in range(len(a)):
  if i in seen:continue
  j=i;k=0
  while j not in seen:seen.add(j);k+=1;j=a[j]
  value=math.lcm(value,k)
 return value

def orbits(gens):
 remaining=set(range(11));out=[]
 while remaining:
  x=min(remaining);seen={x};todo=[x]
  while todo:
   y=todo.pop()
   for g in gens:
    z=g[y]
    if z not in seen:seen.add(z);todo.append(z)
  remaining-=seen;out.append(sorted(seen))
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 need(sha(a.packet/'manifest.json')==PIN,'author pin')
 for r in json.loads((a.packet/'manifest.json').read_text())['exports']:
  p=Path(r['path']);need(not p.is_absolute() and '..' not in p.parts,'safe path');need(sha(a.packet/p)==r['sha256'] and (a.packet/p).stat().st_size==r['bytes'],'export bytes')
 need(all(mul(x,x)==I and x!=I and mul(mul(x,F),trans(x))==F for x in X),'involutory isometries')
 det=sum((-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))*math.prod(F[4*i+p[i]] for i in range(4)) for p in permutations(range(4)))%3
 singular=[v for v in product(range(3),repeat=4) if sum(v[i]*F[4*i+j]*v[j] for i in range(4) for j in range(4))%3==0]
 need(det!=0 and len(singular)==21,'nonsingular minus form')
 Y=[X[1],mul(X[0],X[2]),X[3]];old,n1=ip(X);new,n2=ip(Y)
 need(old[15]==new[7] and len(old[15])==1440,'same full matrix group')
 need([order(mul(X[i],X[i+1])) for i in range(3)]==[4,4,6] and [order(mul(Y[i],Y[i+1])) for i in range(2)]==[6,6],'both exact types')
 need(X[0] not in new[6],'recovery fails')
 rows=[[(0,2),(1,),(0,),(1,),(2,),(3,),(4,),(5,),(4,),(3,5)],[(0,),(1,),(0,2),(1,),(2,),(3,),(4,),(5,),(4,),(3,5)],[(0,),(1,),(0,2),(1,),(2,),(3,),(4,),(3,5),(4,),(5,)]]
 diag=[]
 for row in rows:
  marks=[]
  for lab in range(6):
   perm=list(range(11));edges=[e for e,labels in enumerate(row) if lab in labels]
   need(all(abs(e-f)>1 for i,e in enumerate(edges) for f in edges[i+1:]),'one-label edges disjoint')
   for e in edges:perm[e],perm[e+1]=perm[e+1],perm[e]
   need(len(edges)%2==0,'even involutions');marks.append(tuple(perm))
  for i in range(6):
   for j in range(i+2,6):need(compose(marks[i],marks[j])==compose(marks[j],marks[i]),'string graph')
  left=[marks[1],compose(marks[0],marks[2])]+marks[3:];rev=marks[::-1];right=[rev[1],compose(rev[0],rev[2])]+rev[3:]
  lo,ro=orbits(left),orbits(right);need(len(lo)>1 and len(ro)>1,'both intransitive')
  diag.append(dict(type=[perm_order(compose(marks[i],marks[i+1])) for i in range(5)],left_orbits=lo,right_orbits=ro))
 need([x['type'] for x in diag]==[[5,3,6,3,5],[5,5,6,3,5],[5,5,6,5,5]],'literal three source types')
 need([list(map(len,x['left_orbits'])) for x in diag]==[[1,10],[3,8],[3,8]],'left cancellations')
 need([list(map(len,x['right_orbits'])) for x in diag]==[[10,1],[10,1],[8,3]],'right cancellations')
 # Symbolic determinant recurrence is written. This finite diagnostic checks its base and several periods only.
 determinants=[1,2,3]
 for d in range(3,19):determinants.append(2*determinants[-1]-4*determinants[-2])
 need(all(determinants[j+3]==-8*determinants[j] for j in range(2,16)),'Gram recurrence diagnostic')
 r=dict(status='PASS_DISTINCT_PYTHON',author_imports=False,GAP_imports=False,matrix_order=1440,form_determinant_mod3=det,singular_vectors_including_zero=21,explicit_matrix_IP_pairs=n1+n2,old_parabolic_orders=[len(old[k]) for k in range(16)],new_parabolic_orders=[len(new[k]) for k in range(8)],recovery=False,three_literal_graphs=diag,all_A11_IP_rechecked_here=False,A11_generation_retained_from_fresh_GAP_replay=True,gram_recurrence_diagnostic=determinants,uniform_proof_from_samples=False,formal_credit=0,new_source_credit=0)
 (a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','matrix_order','explicit_matrix_IP_pairs','recovery']}))
if __name__=='__main__':main()
