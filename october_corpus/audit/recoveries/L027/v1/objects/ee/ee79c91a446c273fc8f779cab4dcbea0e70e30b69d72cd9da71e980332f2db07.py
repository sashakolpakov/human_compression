import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
import argparse,json,itertools
from pathlib import Path
P=17
Z=(0,0);O=(1,0);B=(0,1)
def add(x,y):return ((x[0]+y[0])%P,(x[1]+y[1])%P)
def neg(x):return ((-x[0])%P,(-x[1])%P)
def mul(x,y):return ((x[0]*y[0]+3*x[1]*y[1])%P,(x[0]*y[1]+x[1]*y[0])%P)
def bar(x):return (x[0],(-x[1])%P)
def norm(x):return mul(x,bar(x))
def scale(n,x):return mul((n%P,0),x)
def inv(x):
 n=norm(x);need(n[1]==0 and n[0]!=0,'invert nonzero field element');return scale(pow(n[0],-1,P),bar(x))
def total(xs):
 a=Z
 for x in xs:a=add(a,x)
 return a
def need(ok,msg):
 if not ok:raise ValueError(msg)
I=tuple(tuple(O if i==j else Z for j in range(3))for i in range(3))
def mm(A,C):return tuple(tuple(total(mul(A[i][k],C[k][j])for k in range(3))for j in range(3))for i in range(3))
def mp(A,k):
 ans=I
 for _ in range(k):ans=mm(ans,A)
 return ans
def star(A):return tuple(tuple(bar(A[j][i])for j in range(3))for i in range(3))
def scalar(A):return all(A[i][j]==Z for i in range(3)for j in range(3)if i!=j)and A[0][0]==A[1][1]==A[2][2]
def det(A):
 ans=Z
 for p in itertools.permutations(range(3)):
  n=sum(p[i]>p[j]for i in range(3)for j in range(i+1,3));v=mul(mul(A[0][p[0]],A[1][p[1]]),A[2][p[2]])
  ans=add(ans,neg(v)if n%2 else v)
 return ans
def hom(v):
 n=total(norm(x)for x in v);need(n!=Z,'nonisotropic');f=scale(2,inv(n))
 return tuple(tuple(add(neg(I[i][j]),mul(f,mul(v[i],bar(v[j]))))for j in range(3))for i in range(3))
def diag(v):return tuple(tuple(v[i]if i==j else Z for j in range(3))for i in range(3))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);arg=ap.parse_args()
 alpha=(0,4);u=hom([alpha,Z,O]);w=hom([Z,Z,O]);centres=[[(3,4),(1,3),O],[(7,1),(1,3),O],[(8,6),(4,1),O]]
 ns=[(a,b)for a in range(P)for b in range(P)if norm((a,b))==O];need(len(ns)==18,'norm-one group')
 maps=[]
 for e in range(2):
  for r in ns:
   D=diag([O if not e else mul(alpha,inv(bar(alpha))),r,O]);maps.append((e,D))
   for A in [u,w]:
    C=A if not e else tuple(tuple(bar(x)for x in row)for row in A)
    need(mm(mm(D,C),star(D))==A,'centralizer map fixes involutions')
 rows=[]
 for k,vv in zip([7,8,9],centres):
  need(total(norm(x)for x in vv)==(4,0),'centre norm');v=hom(vv);a=mm(w,v);b=mm(mm(v,w),u);c=mm(u,w)
  for A in [u,v,w,a,b,c]:need(mm(A,star(A))==I and det(A)==O,'unitary determinant')
  need(mm(a,b)==u and mm(b,c)==v and mm(mm(a,b),c)==w,'interval identities')
  orders=[]
  for A,expected in zip([a,b,c],[3,k,3]):
   order=next(j for j in range(1,expected+1)if scalar(mp(A,j)));need(order==expected,'exact projective order');orders.append(order)
  trace=add(mul(vv[0],inv(alpha)),bar(mul(vv[0],inv(alpha))));need(trace!=Z,'nonzero trace')
  target=mm(mm(w,v),w);reversers=0
  for e,D in maps:
   C=v if not e else tuple(tuple(bar(x)for x in row)for row in v)
   reversers+=mm(mm(D,C),star(D))==target
  need(reversers==0,'no reversing centralizer map');rows.append(dict(type=orders,centre=vv,trace=trace,matrices=[a,b,c],reversers=reversers))
 vv=[O,(6,0),O];v=hom(vv);target=mm(mm(w,v),w);count=0
 for e,D in maps:
  C=v if not e else tuple(tuple(bar(x)for x in row)for row in v)
  count+=mm(mm(D,C),star(D))==target
 need(count>0,'negative reflection control')
 result=dict(status='PASS_LITERAL_PSU17',field='F17[beta]/(beta^2-3)',rows=rows,centralizer_maps=36,negative_reversers=count)
 arg.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status=result['status'],rows=3,centralizer_maps=36,negative_reversers=count)))
if __name__=='__main__':main()
