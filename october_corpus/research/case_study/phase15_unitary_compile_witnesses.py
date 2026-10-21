#!/usr/bin/env python3
"""Compile existing exact parameter outputs into portable tower coordinates."""
import json
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
base=Path(__file__).resolve().parent
pr=json.loads((base/'phase15_unitary_prime_witnesses.json').read_text())
assert pr['missing']==[19,43]
rows={}
for r in pr['witnesses']:
 q=r['q'];rows[q]={'q':q,'p':q,'exponent':1,'kind':'primitive_norm',
 'base_polynomial':[0,1],'quadratic_relation':'i^2=-1',
 'lambda_real':[r['lambda'][0]],'lambda_imaginary':[r['lambda'][1]],
 'norm_lambda':[r['norm_lambda']],'parameter_t':[r['tracezero_parameter_t']],
 'primitive_order':q*q-1,'prime_divisors':r['prime_divisors']}
comp=[]
for line in (base/'phase15_unitary_composite_witnesses.log').read_text().splitlines():
 if line.startswith('WITNESS '):
  q,p,e,poly,A,B,ss,t,ps=json.loads(line[len('WITNESS '):]);comp.append(q)
  assert q not in rows
  rows[q]={'q':q,'p':p,'exponent':e,'kind':'primitive_norm','base_polynomial':poly,
  'quadratic_relation':'i^2=-1','lambda_real':A,'lambda_imaginary':B,
  'norm_lambda':ss,'parameter_t':t,'primitive_order':q*q-1,'prime_divisors':ps}
special=[]
for line in (base/'phase15_unitary_special_parameters.log').read_text().splitlines():
 if line.startswith('PARAMETER '):
  q,t,x,y,m,orders,aa,bb=json.loads(line[len('PARAMETER '):])
  r={'q':q,'p':q,'exponent':1,'kind':'direct_parameter','base_polynomial':[0,1],
  'quadratic_relation':'i^2=-1','parameter_t':[t],'parameter_x':[x],'parameter_y':[y],
  'projective_middle_order':m,'rank_one_projective_orders':orders}
  special.append(r)
  if q in [19,43]:assert q not in rows;rows[q]=r
sieve=json.loads((base/'phase15_unitary_sieve_check.json').read_text())
assert sorted(rows)==sieve['exceptions'] and len(rows)==1699 and len(comp)==6 and len(special)==3
files=['phase15_unitary_compile_witnesses.py','phase15_unitary_prime_witnesses.py','phase15_unitary_prime_witnesses.json',
 'phase15_unitary_composite_witnesses.g','phase15_unitary_composite_witnesses.log',
 'phase15_unitary_special_parameters.g','phase15_unitary_special_parameters.log','phase15_unitary_sieve_check.json']
report={'status':'PASS','compiled_at_utc':datetime.now(timezone.utc).isoformat(),
 'scope':'Compilation and exact field-list coverage of prior successful outputs, not an independent arithmetic verification.',
 'field_count':1699,'primitive_norm_count':1697,'direct_parameter_count':2,
 'coordinate_convention':'F_p[z]/base_polynomial, low-to-high coefficients; extend by i^2=-1; lambda=lambda_real+i*lambda_imaginary.',
 'application_exceptions':{'7':'Use frozen phase14 full matrix/permutation certificate.',
 '11':'Use phase15 full matrix/permutation certificate; no claim that the sufficient order>5 generation clause applies.',
 '23':'Use the separate direct parameter record below because the generic b-count requires q>=27.'},
 'witnesses':[rows[q] for q in sorted(rows)],'special_parameters':special,
 'input_sha256':{f:sha256((base/f).read_bytes()).hexdigest() for f in files}}
(base/'phase15_unitary_witnesses.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS:1699fields=1697primitive norm witnesses+2direct parameters;3small/special parameter records.')
