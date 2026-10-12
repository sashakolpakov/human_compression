#!/usr/bin/env python3
"""Complete arithmetic roster under the proved r>=7 condition.

Every r divides WH. A piece is represented by its unordered pair a<=b;
assuming W>=H it fits iff a<=H and b<=W. No orientation-list halving.
"""
import argparse,json,time,math
from functools import lru_cache
from pathlib import Path
@lru_cache(None)
def divisors(n):
 low=[];high=[]
 for d in range(1,math.isqrt(n)+1):
  if n%d==0:
   low.append(d)
   if d*d!=n:high.append(n//d)
 return tuple(low+high[::-1])
def candidates(w,h):
 out=[]
 for r in divisors(w*h):
  if r<7:continue
  a=w*h//r;ds=divisors(a)
  if (len(ds)+1)//2<r:continue
  shapes=[[d,a//d]for d in ds if d*d<=a and d<=h and a//d<=w]
  if len(shapes)>=r:out.append({'width':w,'height':h,'pieces':r,'area':a,'shapes':shapes})
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();start=time.monotonic()
 d={'square_candidates':[x for n in range(1,1001)for x in candidates(n,n)],'rectangle_candidates':[x for w in range(1,401)for h in range(1,w+1)for x in candidates(w,h)]}
 a.out.write_text(json.dumps(d,indent=2)+'\n');print({k:len(v)for k,v in d.items()},'seconds',time.monotonic()-start)
 if Path('arithmetic_candidates.json').exists():print('exact prior roster equality',json.loads(Path('arithmetic_candidates.json').read_text())==d)
