#!/usr/bin/env python3
"""Independent direct signed-sum/endpoint derivation of both special reductions."""
import argparse,itertools,json
from pathlib import Path

def require(c,m):
 if not c:raise ValueError(m)
def derive():
 weights=[49,3,45,35,5,21,7,9,15]
 result=[]
 # Ternary assignments (-1,0,1) directly enumerate every signed zero subset.
 zero={}
 for signs in itertools.product((-1,0,1),repeat=9):
  if sum(s*w for s,w in zip(signs,weights)):continue
  mask=sum(1<<i for i,s in enumerate(signs)if s)
  neg=sum(1<<i for i,s in enumerate(signs)if s<0)
  zero.setdefault(mask,[]).append(neg)
 for omit in range(9):
  mask=511^(1<<omit)
  for x in zero:
   if x&~mask:continue
   y=mask^x
   for px in zero[x]:
    for py in zero.get(y,[]):result.append((omit,x,px,py))
 require(len(result)==44,'signed list size');reduced=[r for r in result if r[1].bit_count()>=4]
 require(len(reduced)==26,'rotation list size')
 patterns=[]
 for order in itertools.permutations([1,-5,-3]):
  pos=0;starts={7:0};pos=7
  for step in order:starts[abs(step)]=min(pos,pos+step);pos+=step
  require(pos==0,'cycle closure');v=[starts[w]for w in [7,5,3,1]];lo=min(v);patterns.append(tuple(x-lo for x in v))
 expected=[(0,0,4,4),(0,0,5,7),(0,2,0,2),(0,3,0,7),(1,0,5,0),(1,3,0,0)]
 require(sorted(patterns)==expected,'interval patterns')
 for start in patterns:
  events={}
  for y,h in zip(start,[7,5,3,1]):events[y]=events.get(y,0)^1;events[y+h]=events.get(y+h,0)^1
  require(not any(events.values()),'endpoint parity')
 # Midline reflections complement the appropriate signs, and quarter-turn
 # exchanges axes, possibly complementing one sign list. The full list is
 # checked literally, including all labels rather than count equality.
 rs=set(result)
 for o,x,px,py in result:
  y=(511^(1<<o))^x
  require((o,x,x^px,py)in rs and(o,x,px,y^py)in rs,'reflection closure')
  require((o,y,py,x^px)in rs,'quarter-turn closure')
 return {'weights20':weights,'all44':sorted(result),'rotation26':sorted(reduced),'interval_patterns21':expected,'symmetry_closure_verified':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.write_text(json.dumps(derive(),indent=2)+'\n');print('PASS 44/26 color configurations, six interval patterns and exact symmetry closure')
