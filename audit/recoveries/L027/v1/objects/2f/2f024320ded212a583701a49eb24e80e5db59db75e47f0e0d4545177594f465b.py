import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
from pathlib import Path
import json,argparse
import sympy as s
t=s.Symbol('t')
def red(x):return s.rem(s.Poly(s.expand(x),t),s.Poly(t*t-5,t)).as_expr()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def primitive(x):
 den=s.ilcm(1,*[s.denom(c) for c in s.Poly(x,t).all_coeffs()]);return s.Poly(s.expand(den*x),t).as_expr(),int(den)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);arg=ap.parse_args()
 a,b,X=s.symbols('a b X');r1=s.diag(1,-1,-1);r4=s.diag(-1,-1,1)
 r2=s.Matrix([[a,-a-1,0],[a-1,-a,0],[0,0,-1]]);r3=s.Matrix([[-1,0,0],[0,-b,b-1],[0,-b-1,b]])
 polys=[(X-1)*(X*X-2*a*X+1),(X-1)*(X*X+(-a*b+a+b+1)*X+1),(X-1)*(X*X-2*b*X+1)]
 for i,M in enumerate([r1*r2,r2*r3,r3*r4]):need(s.expand(M.charpoly(X).as_expr()-polys[i])==0,'literal characteristic polynomial')
 aa=[('3',-s.Rational(1,2)),('5+',(-1+t)/4),('5-',(-1-t)/4)];rows=[]
 expected={(0,0,3):[5],(0,0,4):[],(0,0,5):[11],(0,1,3):[],(0,1,5):[59],(0,2,3):[],(0,2,5):[59],(1,0,3):[],(1,0,5):[59],(1,1,3):[19],(1,1,5):[3,11],(1,2,3):[],(1,2,5):[19],(2,0,3):[],(2,0,5):[59],(2,1,3):[],(2,1,5):[19],(2,2,3):[19],(2,2,5):[3,11]}
 for i,(an,a) in enumerate(aa):
  for j,(bn,b) in enumerate(aa):
   c=red(-a*b+a+b+1);row=dict(left=an,right=bn,a=str(a),aprime=str(b),C=str(c),cells=[])
   for m in [3,4,5]:
    if m==4 and (i or j):row['cells'].append(dict(order=m,status='excluded_by_end_type',reason='S4/A5 rank3 cannot have adjacent orders5 and4'));continue
    e=red(c-1 if m==3 else c if m==4 else c*c-c-1);num,den=primitive(e)
    res=s.resultant(t*t-5,num,t);primes=sorted(p for p in s.factorint(abs(int(res))) if p!=2)
    # Table's No entries have no odd prime, or the candidate forces an excluded a=0,+/-1.
    valid=[];filters=[]
    for p in primes:
     rt=s.polys.domains.GF(p);rr=s.Poly(t*t-5,t,modulus=p);ee=s.Poly(num,t,modulus=p)
     roots=s.gcd(rr,ee)
     invalid=s.Poly(1,t,modulus=p)
     for value in [a,b]:
      for bad in [0,1,-1]:
       n,d=primitive(value-bad);invalid*=s.Poly(n,t,modulus=p)
     permitted=s.quo(roots,s.gcd(roots,invalid))
     # In characteristic5 t²-5 has multiplicity; permitted roots are tested squarefree.
     permitted=permitted.sqf_part()
     if permitted.degree()>0:valid.append(p)
     else:filters.append(p)
    need(valid==expected[(i,j,m)],'source exact permitted prime cell '+str((i,j,m,valid,primes,filters)))
    row['cells'].append(dict(order=m,equation=str(e),integer_numerator=str(num),denominator=den,resultant=int(res),candidate_primes=primes,excluded_degenerate_primes=filters,possible_characteristics=valid))
   rows.append(row)
 result=dict(status='PASS_TABLE_ONE_ARITHMETIC',characteristic_polynomials=[str(s.expand(x)) for x in polys],rows=rows,scope='Necessary parameter cells only; exact displayed equation and field/root choice remain required, no IP from arithmetic')
 arg.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
