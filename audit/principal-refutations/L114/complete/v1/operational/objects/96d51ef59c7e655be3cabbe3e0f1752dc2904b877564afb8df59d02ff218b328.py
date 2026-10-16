"""Literal projective orbits compared with the all-parameter fixed-line formula."""
from pathlib import Path
import argparse, importlib.util, json, math, time
W=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('root_controls',W.parent/'rank_two_families/quotient_controls.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
need=base.need

def fixed_formula(n,d,j):
 r=n//d;h=math.gcd(d,j);g=math.gcd(n,j)
 need(n%d==0 and r>1 and all(r%p for p in range(2,math.isqrt(r)+1)), 'prime relative degree')
 need(g in (h,r*h),'two gcd possibilities, including repeated primes')
 return ((1<<(h*(r-1)))-1)//((1<<h)-1) if g==r*h else math.gcd(r,(1<<h)-1)-1

def count_formula(n,d):
 total=sum(fixed_formula(n,d,j)for j in range(n))
 need(total%n==0,'integral orbit formula')
 return total//n

def check_orbits(n,d,points,step):
 remaining=set(points);hist={};fixed=[0]*n
 while remaining:
  x=min(remaining);o=[];v=x
  while v not in o:
   o.append(v);v=step(v)
  need(v==x and set(o)<=remaining,'actual permutation cycle')
  remaining-=set(o);length=len(o)
  need(n%length==0,'Frobenius cycle divides absolute degree')
  hist[length]=hist.get(length,0)+1
  for j in range(n):
   if j%length==0:fixed[j]+=length
 expected=[fixed_formula(n,d,j)for j in range(n)]
 need(fixed==expected,'every actual fixed-line count agrees')
 need(sum(hist.values())==count_formula(n,d),'actual orbit total agrees')
 return dict(n=n,d=d,r=n//d,projective_points=len(points),cycle_counts=hist,
             fixed_counts=fixed,orbits=sum(hist.values()))

def binary_field_case(n,d,polynomial):
 f=base.Field(n,polynomial);q=1<<n;s=1<<d
 # Rabin's irreducibility criterion, checked with literal polynomial division.
 def remainder(a,b):
  while a and a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
  return a
 def gcd(a,b):
  while b:a,b=b,remainder(a,b)
  return a
 need(f.power(2,1<<n)==2,'polynomial divides X^(2^n)-X')
 primes=[p for p in range(2,n+1)if n%p==0 and all(p%t for t in range(2,math.isqrt(p)+1))]
 need(all(gcd(polynomial,f.power(2,1<<(n//p))^2)==1 for p in primes),'irreducible binary polynomial')
 K=[a for a in range(q)if f.power(a,s)==a]
 need(len(K)==s,'actual embedded subfield')
 pivots={}
 for a in K:
  v=a
  while v:
   p=v.bit_length()-1
   if p in pivots:v^=pivots[p]
   else:pivots[p]=v;break
 need(len(pivots)==d,'subfield binary rank')
 def reduce(v):
  for p in sorted(pivots,reverse=True):
   if(v>>p)&1:v^=pivots[p]
  return v
 quotient={reduce(v)for v in range(q)}
 need(len(quotient)==q//s,'literal additive quotient')
 canon={0:0};points=[]
 for v in sorted(quotient-{0}):
  if v in canon:continue
  line={reduce(f.mul(k,v))for k in K if k}
  need(len(line)==s-1 and 0 not in line,'projective line has s-1 nonzero vectors')
  c=min(line);points.append(c)
  for x in line:need(x not in canon,'projective lines disjoint');canon[x]=c
 need(len(canon)==len(quotient),'projective partition complete')
 row=check_orbits(n,d,points,lambda v:canon[reduce(f.mul(v,v))])
 row.update(model='binary polynomial field',polynomial=polynomial)
 return row

def kummer_case():
 # K=F8 with a primitive element a=2.  X^7-a is irreducible: a root
 # has order49, and ord_49(8)=7.  This supplies F_(8^7) without enumerating it.
 f=base.Field(3,0xb);a=2
 need(f.power(a,7)==1 and a!=1,'primitive order-seven scalar')
 need(pow(8,7,49)==1 and all(pow(8,k,49)!=1 for k in range(1,7)), 'Kummer extension degree seven')
 inverses={x:f.power(x,6)for x in range(1,8)}
 points=[]
 for first in range(6):
  for tail in range(8**(5-first)):
   v=[0]*first+[1];z=tail
   for k in range(5-first):v.append(z%8);z//=8
   points.append(tuple(v))
 need(len(set(points))==(8**6-1)//7,'complete normalized six-coordinate projective space')
 def step(v):
  out=[0]*6
  for i,c in enumerate(v,1):
   degree=2*i;factor=a if degree>=7 else 1
   out[(degree%7)-1]=f.mul(f.mul(c,c),factor)
  lead=next(x for x in out if x)
  return tuple(f.mul(x,inverses[lead])for x in out)
 row=check_orbits(21,3,points,step)
 row.update(model='Kummer X^7-a over F8; quotient constant coordinate removed')
 return row

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);out=p.parse_args().out
 need(not out.exists(),'fresh output');start=time.monotonic()
 rows=[binary_field_case(9,3,0x211),binary_field_case(15,3,0x8003),binary_field_case(15,5,0x8003),kummer_case()]
 need([r['orbits']for r in rows]==[1,41,3,1791],'actual requested totals')
 n27=count_formula(27,9);need(n27==19,'second repeated-prime-index arithmetic case')
 result=dict(status='PASS_LITERAL_PROJECTIVE_FROBENIUS_CONTROLS',rows=rows,arithmetic_only_n27_d9=n27,
             seconds=time.monotonic()-start,ambient_group_censuses=0,source_credit=0,whole_original_credit=0,
             qualification='Full finite projective actions in four models; general theorem remains the written proof.')
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
