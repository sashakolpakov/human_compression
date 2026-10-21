#!/usr/bin/env python3
"""Distinct bounded permutation/vector checks; no author module or GAP imports.
These checks are diagnostics, not a repeated completeness search.
"""
import argparse,hashlib,itertools,json,math,re
from pathlib import Path

def require(x,s):
 if not x: raise ValueError(s)
def mul(a,b): return tuple(a[b[i]] for i in range(len(a)))
def inverse(a): return tuple(a.index(i) for i in range(len(a)))
def group(gs,n):
 e=tuple(range(n));d={e};q=[e]
 for x in q:
  for y in gs:
   z=mul(x,y)
   if z not in d:d.add(z);q.append(z)
 return d
def order(g):
 r=tuple(range(len(g)));t=r
 for n in range(1,10000):
  t=mul(t,g)
  if t==r:return n
 raise ValueError('order')
def ip(gs,n):
 S=[group([g for i,g in enumerate(gs) if a>>i&1],n) for a in range(1<<len(gs))]
 for a in range(len(S)):
  for b in range(len(S)):
   require(S[a]&S[b]==S[a&b],'IP')
 return S
def literal(n,gs,types,expected=None):
 require(all(sorted(g)==list(range(n)) and order(g)==2 for g in gs),'involutions')
 require([order(mul(a,b)) for a,b in zip(gs,gs[1:])]==types,'ordered types')
 require(all(mul(gs[i],gs[j])==mul(gs[j],gs[i]) for i in range(len(gs)) for j in range(i+2,len(gs))),'string')
 S=ip(gs,n)
 if expected is not None:require(len(S[-1])==expected,'order')
 return S
def sign(g): return sum(g[i]>g[j] for i in range(len(g)) for j in range(i+1,len(g)))%2
def span(vs):
 out={0}
 for v in vs:out |= {x^v for x in out}
 return out
def even_modules(m):
 lam=(1<<m)-1
 W=[span([lam^(1<<i) for i in range(a)]) for a in range(1,m+1)]
 for a in range(m):
  for b in range(m):require(W[a]&W[b]==W[min(a,b)],'nested initial support')
 if m%2:
  require(len(W[-1])==2**(m-1) and lam not in W[-1],'odd central independence')
 else:
  require(len(W[-1])==2**m and lam in W[-1],'even parity obstruction')
 return {'m':m,'full_span_dimension':int(math.log2(len(W[-1]))),'central_independent':lam not in W[-1]}
def wreath_marking(m):
 def flip(mask):return tuple(2*i+(b^((mask>>i)&1)) for i in range(m) for b in range(2))
 def swap(i):return tuple(2*(i+1 if j==i else i if j==i+1 else j)+b for j in range(m) for b in range(2))
 lam=(1<<m)-1
 return [flip(lam),flip(lam^1)]+[swap(i) for i in range(m-1)]
def audit(packet):
 receipt=[];totalpairs=0;outer=[]
 for name in ['small_transitive','primitive_markings']:
  txt=(packet/'author_programs'/f'{name}.stdout.log').read_text()
  expected_orders={(6,9):36,(6,11):48,(8,45):576} if name=='small_transitive' else {(6,1):60,(6,2):120,(10,5):720}
  for line in txt.splitlines():
   if not line.startswith('SOLUTION|'):continue
   _,n,i,types,perms=line.split('|');n=int(n);i=int(i);types=json.loads(types);gs=[tuple(x-1 for x in p) for p in json.loads(perms)]
   S=literal(n,gs,types,expected_orders[n,i]);require(len({g[0] for g in S[-1]})==n,'transitive')
   if n==6 and i==9 and name=='small_transitive':require(types==[3,2,3] and 48%36!=0,'source order36 correction')
   if (name=='small_transitive' and n==6) or (name=='primitive_markings' and i in [2,5]):require(any(sign(g) for g in gs),'alternating exclusion')
   totalpairs+=len(S)**2;receipt.append({'kind':name,'n':n,'id':i,'rank':len(gs),'order':len(S[-1]),'types':types})
 txt=(packet/'author_programs/small_extremal.stdout.log').read_text()
 for line in txt.splitlines():
  if not line.startswith('EXTREMAL|'):continue
  _,n,perms=line.split('|');n=int(n);gs=[tuple(x-1 for x in p) for p in json.loads(perms)]
  S=literal(n,gs,[3]*(n-2),math.factorial(n));tail=group(gs[1:],n)
  # Compute the actual derived tail from conjugates of all pair commutators.
  comm=[mul(mul(mul(inverse(a),inverse(b)),a),b) for a in gs[1:] for b in gs[1:]]
  comm=[mul(mul(inverse(h),c),h) for h in tail for c in comm]
  der=group(comm,n)
  centralizer=[p for p in itertools.permutations(range(n)) if all(mul(p,g)==mul(g,p) for g in der)]
  require(len(centralizer)==1,'actual derived-tail centralizer')
  require(all(sign(g) for g in gs),'odd extremal generators')
  outer.append({'degree':n,'derived_tail_order':len(der),'derived_tail_orbit0':len({g[0] for g in der}),'centralizer':len(centralizer)})
 require(len(receipt)==26 and len(outer)==3,'literal receipt counts')
 examples=[]
 for m in [3,5]:
  gs=wreath_marking(m);S=literal(2*m,gs,[2,4]+[3]*(m-2),2**m*math.factorial(m));
  typ=[order(mul(a,b)) for a,b in zip([gs[0]]+list(reversed(gs[1:])),([gs[0]]+list(reversed(gs[1:])))[1:])]
  require(typ==[2]+[3]*(m-2)+[4],'component reversal')
  require(typ!=list(reversed([2,4]+[3]*(m-2))),'not global dual')
  examples.append({'m':m,'group_order':len(S[-1]),'subset_pairs':len(S)**2,'second_type':typ})
 module=[even_modules(m) for m in range(3,16)]
 require(all(n*math.prod(n-2**i for i in range(n.bit_length()-1))<2**(n-1) for n in range(26,64)),'Maroti interval')
 for q in range(6,100):require((q+1)**2<=2**q-1,'dyadic induction threshold')
 controls=[]
 for label,fn in [('even_m_does_not_have_extra_central_rank',lambda:literal(8,wreath_marking(4),[2,4,3,3])),('incorrect_source_order36_type',lambda:literal(6,[tuple(x-1 for x in p) for p in json.loads(next(x for x in (packet/'author_programs/small_transitive.stdout.log').read_text().splitlines() if x.startswith('SOLUTION|')).split('|')[4])],[2,3,3]))]:
  try:fn()
  except ValueError:controls.append(label)
  else:raise ValueError('failed negative '+label)
 return {'status':'PASS_DISTINCT_BOUNDED_DIAGNOSTICS','positive_tuples':receipt,'literal_positive_count':len(receipt),'positive_IP_pairs':totalpairs,'actual_extremal_tails':outer,'wreath_models':examples,'module_cases':module,'integer_interval_checks':38,'negative_controls':controls,'complete_new_GAP_census_repeated':False,'author_modules_imported':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=audit(a.packet);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['positive_tuples','module_cases']}))
