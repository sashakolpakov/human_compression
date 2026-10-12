"""Exact independent integer-permutation check of the literal modified relators."""
from collections import deque
from math import lcm
I=tuple(range(11))
G=[tuple(v-1 for v in row) for row in [[3,4,1,2,6,5,9,8,7,10,11],[2,1,5,6,3,4,8,7,9,10,11],[1,2,6,5,4,3,7,8,10,9,11],[4,3,2,1,5,6,7,8,9,11,10]]]
def mul(a,b):return tuple(a[i] for i in b)
def word(w):
 a=I
 for i in w:a=mul(a,G[i])
 return a
def order(g):
 seen=set();lens=[]
 for x in range(11):
  if x in seen:continue
  y=x;n=0
  while y not in seen:seen.add(y);n+=1;y=g[y]
  lens.append(n)
 return lcm(*lens)
def closure(gs):
 out={I};todo=deque([I])
 while todo:
  a=todo.popleft()
  for b in gs:
   c=mul(a,b)
   if c not in out:out.add(c);todo.append(c)
 return out
BASE=[[i,i] for i in range(4)]+[[0,1]*3,[0,2]*6,[0,3]*2,[1,2]*2,[1,3]*6,[2,3]*3,[3,2,0,2,0,2]*2,[0,1,3,1,3]*2,[1,0,2,0,2,0]*2]
MOD=[2,3,1,3,1]
ORIG=MOD+[3]
def ensure(x,msg):
 if not x:raise ValueError(msg)
def audit():
 ensure(all(sorted(g)==list(range(11)) for g in G),'bijections')
 ensure(all(word(w)==I for w in BASE),'shared relators')
 ensure(word(MOD*2)==I and word(MOD*4)==I,'literal modified words')
 ensure(order(word([1,3]))==6 and word([1,3]*2)!=I,'bd order/nonconsequence')
 H=closure(G);ensure(len(H)==720,'generated order720')
 return {'status':'PASS','points':11,'generated_order':len(H),'literal_base_relators':len(BASE),'modified_relator_orders':[order(word(MOD)),order(word(MOD*2))],'bd_order':6,'bd_square_images_one_based':[x+1 for x in word([1,3]*2)],'original_period_word_order':order(word(ORIG))}
if __name__=='__main__':
 import json;print(json.dumps(audit(),indent=2))
