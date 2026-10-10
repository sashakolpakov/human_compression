#!/usr/bin/env python3
"""Deterministic primitive norm-curve witnesses over prime fields, no group enumeration."""
from pathlib import Path
from math import gcd
from hashlib import sha256
from datetime import datetime,timezone
import json
b=Path(__file__).resolve().parent
sieve=json.loads((b/'phase15_unitary_sieve_check.json').read_text())
rows=[r for r in sieve['field_records'] if r['sieve_certificate'] is None and r['exponent']==1]
witnesses=[];missing=[]
for row in rows:
 q=row['q'];N=q*q-1;ps=sorted(set(map(int,row['minus_factors']))|set(map(int,row['plus_factors'])))
 fm=list(map(int,row['minus_factors']))
 g=next(g for g in range(2,q) if all(pow(g,(q-1)//r,q)!=1 for r in fm))
 def mul(x,y):return ((x[0]*y[0]-x[1]*y[1])%q,(x[0]*y[1]+x[1]*y[0])%q)
 def power(x,n):
  a=(1,0)
  while n:
   if n&1:a=mul(a,x)
   x=mul(x,x);n//=2
  return a
 inv4=pow(4,-1,q);found=None;trials=0;s=1
 for k in range(1,q):
  s=s*g%q
  if gcd(k,q-1)>1:continue
  trials+=1
  aa=(s*s+4*s+1)*inv4%q;bb=-(s*s+1)*inv4%q
  A=pow(aa,(q+1)//4,q);B=pow(bb,(q+1)//4,q)
  if A*A%q!=aa or B*B%q!=bb:continue
  lam=(A,B)
  if any(power(lam,N//r)==(1,0) for r in ps):continue
  assert power(lam,N)==(1,0) and (A*A+B*B)%q==s
  si=pow(s,-1,q);u=(A*(1-si)%q,B*(1+si)%q)
  assert (u[0]*u[0]+u[1]*u[1])%q==q-2
  t=-2*u[1]%q
  assert t and (t*t-1)%q and (t*t+8)%q
  found={'q':q,'p':q,'exponent':1,'quadratic_polynomial':[1,0,1],
    'lambda':[A,B],'norm_lambda':s,'tracezero_parameter_t':t,
    'cyclic_order':N,'prime_divisors':ps,'trials':trials}
  break
 if found is None:missing.append(q)
 else:witnesses.append(found)
 if len(witnesses)%100==0:print('progress',q,len(witnesses),'missing',missing,flush=True)
assert missing==[19,43]
report={'status':'PASS_WITH_LISTED_EXCEPTIONS','executed_at_utc':datetime.now(timezone.utc).isoformat(),
 'scope':'Exact primitive elements of F_p[i], i²=−1, and norm equation for prime exceptional fields; no matrix groups are enumerated.',
 'field_count':len(rows),'witness_count':len(witnesses),'missing':missing,'witnesses':witnesses,
 'input_sha256':{Path(__file__).name:sha256(Path(__file__).read_bytes()).hexdigest(),
 'phase15_unitary_sieve_check.json':sha256((b/'phase15_unitary_sieve_check.json').read_bytes()).hexdigest()}}
(b/'phase15_unitary_prime_witnesses.json').write_text(json.dumps(report,indent=2)+'\n')
print('FINAL',len(rows),len(witnesses),'missing',missing)
