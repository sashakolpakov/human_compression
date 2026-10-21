#!/usr/bin/env python3
"""Independent bounded diagnostics for expanded E; imports no author implementation.
These checks support, and do not replace, the quantified written proofs.
"""
import argparse, hashlib, itertools, json
from pathlib import Path
from collections import Counter

def need(v,m):
 if not v: raise ValueError(m)
def mm(x,y,p):
 a,b,c,d=x;e,f,g,h=y
 return ((a*e+b*g)%p,(a*f+b*h)%p,(c*e+d*g)%p,(c*f+d*h)%p)
def tr(x,p):return (x[0]+x[3])%p
def det(x,p):return (x[0]*x[3]-x[1]*x[2])%p
def inv(x,p):
 a,b,c,d=x;u=pow(det(x,p),-1,p)
 return (d*u%p,-b*u%p,-c*u%p,a*u%p)
def norm(x,p):
 u=pow(next(a for a in x if a),-1,p)
 return tuple(a*u%p for a in x)
def pp(x,y,p):return norm(mm(x,y,p),p)
def sub(x,y,p):return tuple((a-b)%p for a,b in zip(x,y))
def scale(x,c,p):return tuple(a*c%p for a in x)
def group(gs,mul,one):
 seen={one};stack=[one]
 while stack:
  x=stack.pop()
  for g in gs:
   y=mul(x,g)
   if y not in seen:seen.add(y);stack.append(y)
 return seen

def trace_checks():
 rows=[];zero_reverse=0;nonzero_no_reverse=0
 for p in (3,5,7):
  one=(1,0,0,1);J=(0,1,p-1,0);half=pow(2,-1,p)
  sl=[x for x in itertools.product(range(p),repeat=4) if det(x,p)==1]
  pgl=list({norm(x,p) for x in itertools.product(range(p),repeat=4) if det(x,p)})
  count=extensions=revchecks=0
  for a,b in itertools.product(range(1,p),repeat=2):
   d=(a*a+b*b-4)%p
   if not d:continue
   U,V=next((u,v) for u,v in itertools.product(range(p),repeat=2) if (u*u+v*v)%p==d)
   u=(U+a)*half%p;w=(V-b)*half%p
   A=(u,(w+b)%p,w,(a-u)%p);B=mm(inv(A,p),J,p)
   need(det(A,p)==det(B,p)==1 and tr(A,p)==a and tr(B,p)==b,'seed')
   comm=sub(mm(A,B,p),mm(B,A,p),p)
   need(det(comm,p)==-d%p,'irreducibility determinant')
   for c in range(p):
    D=(a*a*c*c-4*(a*a+b*b+c*c-4))%p
    actual={C for C in sl if tr(C,p)==c and tr(mm(B,C,p),p)==tr(mm(J,C,p),p)==0}
    roots=[z for z in range(p) if z*z%p==D];pred={}
    for z in roots:
     R=(-b*c*V+z*U)*pow(d,-1,p)%p;S=(b*c*U+z*V)*pow(d,-1,p)%p
     C=((R+c)*half%p,S*half%p,S*half%p,(c-R)*half%p)
     pred[C]=z
     need((2*tr(mm(A,C,p),p)-a*c)%p==z,'actual trace invariant')
    need(actual==set(pred),'all determinant-one extensions')
    count+=1;extensions+=len(actual)
    if c and c*c%p!=4%p:
     reversers=[X for X in pgl if pp(pp(X,A,p),inv(X,p),p)==norm(inv(A,p),p)]
     for C in actual:
      exists=any(pp(pp(X,C,p),inv(X,p),p)==norm(C,p) and pp(pp(X,B,p),inv(X,p),p)==norm(mm(mm(A,A,p),B,p),p) for X in reversers)
      need(exists==(D==0),'projective full reversal iff zero discriminant')
      revchecks+=1
      if exists:zero_reverse+=1
      else:nonzero_no_reverse+=1
  rows.append(dict(p=p,trace_triples=count,extensions=extensions,reversal_checks=revchecks))
 return dict(rows=rows,zero_reversals=zero_reverse,nonzero_nonreversals=nonzero_no_reverse)

def compose(x,y):return tuple(y[x[i]] for i in range(len(x)))
def order(x):
 a=tuple(range(len(x)));n=0
 while True:
  a=compose(a,x);n+=1
  if a==tuple(range(len(x))):return n

def parity(x):return sum(x[i]>x[j] for i in range(len(x)) for j in range(i+1,len(x)))%2

def local_checks():
 out=[]
 for n,even in ((4,True),(4,False),(5,True)):
  els=[p for p in itertools.permutations(range(n)) if not even or not parity(p)];one=tuple(range(n));o={x:order(x) for x in els};cy={x:group([x],compose,one) for x in els};pairs=[]
  for a in els:
   if o[a]<=2:continue
   for b in els:
    if o[b]<=2 or o[compose(a,b)]!=2 or len(cy[a]&cy[b])!=1:continue
    if len(group([a,b],compose,one))==len(els):pairs.append((a,b))
  need(len(pairs)=={12:24,24:48,60:360}[len(els)],'independent complete pair census')
  types=Counter((o[a],o[b]) for a,b in pairs)
  out.append(dict(order=len(els),pairs=len(pairs),types={str(k):v for k,v in types.items()}))
 return out

def exceptional_checks():
 out=[]
 for p,types in ((11,((3,5,3),(5,3,5))),(19,((3,5,3),(5,3,5))),(31,((5,3,4),))):
  one=(1,0,0,1);J=(0,1,p-1,0);half=pow(2,-1,p)
  traces=[(-1+r)*half%p for r in range(p) if r*r%p==5]
  for typ in types:
   rows=[]
   for h in traces:
    a,b,c=(h,1,h) if typ==(5,3,5) else ((1,h,1) if typ==(3,5,3) else (h,1,next(x for x in range(p) if x*x%p==2)))
    d=(a*a+b*b-4)%p;U,V=next((u,v) for u,v in itertools.product(range(p),repeat=2) if (u*u+v*v)%p==d)
    u=(U+a)*half%p;w=(V-b)*half%p;A=(u,(w+b)%p,w,(a-u)%p);B=mm(inv(A,p),J,p)
    D=(a*a*c*c-4*(a*a+b*b+c*c-4))%p
    for z in range(p):
     if z*z%p!=D:continue
     R=(-b*c*V+z*U)*pow(d,-1,p)%p;S=(b*c*U+z*V)*pow(d,-1,p)%p;C=((R+c)*half%p,S*half%p,S*half%p,(c-R)*half%p)
     mul=lambda x,y:pp(x,y,p)
     a0,b0,c0=map(lambda x:norm(x,p),(A,B,C));H=group([a0,b0],mul,one);K=group([b0,c0],mul,one);G=group([a0,b0,c0],mul,one)
     need(len(G)==p*(p*p-1)//2,'independent full projective group')
     need(len(H)==60 and len(K)==(24 if typ[-1]==4 else 60),'independent local group')
     need(z==0 or len(H&K)==typ[1],'nonzero-root full IP')
     rows.append(dict(trace=h,parameter=z,group=len(G),ends=[len(H),len(K)],intersection=len(H&K)))
   out.append(dict(p=p,type=typ,rows=rows))
 return out

def controls():
 # Genuine algebraic weakened variants fail on these literal matrices.
 p=5;A=(1,1,0,1);B=(1,2,0,1)
 need(det(sub(mm(A,B,p),mm(B,A,p),p),p)==0,'drop irreducibility control')
 # d=0 destroys the parameter bijection: choose U=V=b=c=0, any R,S on R²+S²=-4.
 solutions=[(R,S) for R,S in itertools.product(range(p),repeat=2) if (R*R+S*S)%p==1]
 need(len(solutions)>1 and all((0*R+0*S)%p==0 for R,S in solutions),'zero denominator noninjectivity')
 # t odd order violates the middle cyclic intersection despite both full affine ends.
 p=7;t=2;A=(-pow(t,-1,p)%p,1,0,1);B=(t,0,0,1);C=(1,0,1+t,-t%p);mul=lambda x,y:pp(x,y,p);one=(1,0,0,1)
 H=group(list(map(lambda x:norm(x,p),(A,B))),mul,one);K=group(list(map(lambda x:norm(x,p),(B,C))),mul,one);cy=group([norm(B,p)],mul,one)
 need(len(H&K)==6 and len(cy)==3,'drop minus-one condition')
 return ['absolute_irreducibility_needed','nonzero_denominator_needed','pointed_minus_one_needed']

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists(),'fresh output')
 r=dict(status='PASS',trace=trace_checks(),local_pairs=local_checks(),exceptional=exceptional_checks(),weakenings=controls(),scope='finite diagnostics only; no quantified conclusion inferred',author_imports=False)
 r['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
