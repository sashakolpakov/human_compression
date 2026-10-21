"""Prepare a small literal counterexample in the natural projective model."""
import sys
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
from collections import deque
from itertools import product
import json
P=11;points=list(range(P))+[None];idx={x:i for i,x in enumerate(points)};ident=tuple(range(12))
def action(m):
 a,b,c,d=m;out=[]
 for z in points:
  u,v=(a,c)if z is None else((a*z+b)%P,(c*z+d)%P)
  out.append(idx[None if v==0 else u*pow(v,-1,P)%P])
 return tuple(out)
def mul(p,q):return tuple(p[q[i]]for i in range(12))
def closure(gs):
 words={ident:''};queue=deque([ident])
 while queue:
  h=queue.popleft()
  for j,g in enumerate(gs):
   k=mul(h,g)
   if k not in words:words[k]=words[h]+chr(97+j);queue.append(k)
 return words
models={}
for m in product(range(P),repeat=4):
 a,b,c,d=m
 if(a*d-b*c)%P==1:models.setdefault(action(m),m)
invs=sorted(g for g in models if g!=ident and mul(g,g)==ident)
b=action((0,10,1,0));done=False
for a in invs:
 A=closure([a,b])
 if len(A)!=12:continue
 for c in invs:
  B=closure([b,c]);H=set(A)&set(B)
  if len(B)!=12 or len(H)!=4:continue
  G=closure([a,b,c])
  if set(G)!=set(models):continue
  U=action((1,1,0,1));W=action((0,10,1,0))
  out={'field':11,'point_order':points,'matrices':[models[g]for g in(a,b,c)],'permutations':[list(g)for g in(a,b,c)],'standard_U_word':G[U],'standard_W_word':G[W],'group_order':len(G),'pair_orders':[len(A),len(B)],'intersection':[list(h)for h in sorted(H)],'extra_words':[{'permutation':list(h),'in_ab':A[h],'in_bc':B[h]}for h in sorted(H)if h not in(ident,b)]}
  print(json.dumps(out,indent=2));done=True;break
 if done:break
if not done:raise RuntimeError('no example')
