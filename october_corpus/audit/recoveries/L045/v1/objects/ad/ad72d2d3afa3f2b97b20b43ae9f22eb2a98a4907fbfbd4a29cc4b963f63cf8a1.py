#!/usr/bin/env python3
"""Exact controls for the written linear/unitary estimates; not a census."""
import sys
if sys.flags.optimize:
    raise RuntimeError('optimized execution is not accepted')
from fractions import Fraction as F
from lower_bounds import linear_bound
import argparse,json
from pathlib import Path

def need(test,message):
    if not test:raise ValueError(message)

def primes(n):return [p for p in range(2,n+1)if n%p==0 and all(p%d for d in range(2,int(p**.5)+1))]
def central(n,q):
 if n==4:return q**4+q**3+(2*q*q-q if q%2 else -q*q-1)
 if n%2:
  e=(n*n-1)//4;return 2*(q**e+q**(e-1))
 m=n//2
 if q%2:return 2*(q**(m*m)+q**(m*m-1))
 return q**(n-1)-1+2*q**(n-2)*(q**(m*m-m)+q**(m*m-m-1))
def cover(n,q,u):
 if u and n%2==0:
  k=n-1;a=(k*k+k-2)//2;return (1 if q%2==0 else 2)*(2*(q**a+q**(a-1))+1)-1
 total=0
 for r in primes(n):
  k=n//r
  if k==1:continue
  a=(k*k+k-2)//2;upper=2*(q**(r*a)+q**(r*(a-1)))
  total+=((q+1)if r==2 else (1 if q%2==0 else 2))*(upper+1)-1
 return total

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 need(not a.out.exists(),'output exists')
 rows=[];finite=[]
 for q in [2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,31,32,49,64]:
  for n in range(4,61):
   for u in (False,True):
    T=F(q**n+1,q+1)if u and n%2 else (q**(n-1)+1 if u else F(q**n-1,q-1))
    upper=T*central(n,q)+cover(n,q,u);lo=linear_bound(n,q,u)[0]
    route=(n==4 and q in [2,3,4]) or (n in [5,6]and q in [2,3]) or (n==8 and q==2)
    r=dict(n=n,q=q,family='U'if u else 'L',quarter_pass=F(q**(n*n//2),4)>upper,class_pass=lo>upper,upper=str(upper),lower=str(lo))
    if route:finite.append(r);continue
    need(lo>upper,f'class lower comparison {n,q,u}')
    if (n,q)!=(4,5):need(r['quarter_pass'],f'uniform quarter comparison {n,q,u}')
    rows.append(r)
 need(linear_bound(4,5,False)[0]==251875 and linear_bound(4,5,True)[0]==170625,'exact degree-four lower examples')
 need(F(5**4-1,4)*central(4,5)+cover(4,5,False)==131825,'linear degree-four upper example')
 need((5**3+1)*central(4,5)+cover(4,5,True)==115171,'unitary degree-four upper example')
 report={'status':'PASS_EXACT_LINEAR_UNITARY_INEQUALITY_CONTROLS','number_of_rows':len(rows),'rows':rows,'separately_acquired_finite_routes':finite,'scope':'All-rank inequalities are proved in the manuscript; samples are controls only. Source Table4 classification is retained explicitly.'}
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(report['status'],len(rows))
if __name__=='__main__':main()
