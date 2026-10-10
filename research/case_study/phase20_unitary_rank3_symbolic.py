#!/usr/bin/env python3
"""Exact identities for the anti-isometric-endpoint unitary rank-three template."""
from pathlib import Path
import hashlib,json,datetime
import sympy as S
t,tb,eta=S.symbols('t tb eta',nonzero=True)
X=S.symbols('X')
I=S.eye(4);J=S.Matrix([[0,1],[1,0]]);H=S.diag(J,-J)
A=S.Matrix([[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]])
C=S.diag(1,1,-1,-1);v=S.Matrix([1,0,2/t,tb/2])
bar=lambda M:M.subs({t:tb,tb:t,eta:-1/eta},simultaneous=True)
B=I+v*bar(v).T*H;n=v+C*v;m=A*n;U=(B*C)**2;N=U-I
checks=[]
def check(label,lhs,rhs):
 d=lhs-rhs
 if isinstance(d,S.MatrixBase):assert all(S.cancel(x)==0 for x in d),label
 else:assert S.cancel(d)==0,label
 checks.append(label)
check('H involution',H*H,I)
check('v norm',(bar(v).T*H*v)[0],-2)
check('v C pairing',(bar(v).T*H*C*v)[0],2)
for label,g,mult in [('normalized A',A,-1),('B',B,1),('C',C,1)]:
 check(label+' square',g*g,I);check(label+' multiplier',bar(g).T*H*g,mult*H)
check('eta A unitary',bar(eta*A).T*H*(eta*A),H)
check('eta A square',(eta*A)**2,eta**2*I)
check('eta A determinant',(eta*A).det(),eta**4)
check('B determinant',B.det(),-1);check('C determinant',C.det(),1)
check('outer anticommute',A*C,-C*A)
check('n coordinates',n,S.Matrix([2,0,0,0]));check('m coordinates',m,S.Matrix([0,0,2,0]))
W=S.Matrix.hstack(n,m)
check('W isotropic',bar(W).T*H*W,S.zeros(2))
check('A projection',A*W,W*S.Matrix([[0,1],[1,0]]));check('C projection',C*W,W*S.diag(1,-1));check('U projection',U*W,W*S.Matrix([[1,t],[0,1]]))
check('N square',N*N,2*n*bar(n).T*H);check('N cube',N*N*N,S.zeros(4))
check('BC characteristic', (B*C).charpoly(X).as_expr(),(X-1)**3*(X+1))
check('B fixes n',B*n,n)
check('adjacent planes pairing',(bar(m).T*H*B*m)[0],t*tb)
u,w,uq,wq=S.symbols('u w uq wq');ds=S.symbols('d11 d12 d21 d22');es=S.symbols('e11 e12 e21 e22');D=S.Matrix(2,2,ds);E=S.Matrix(2,2,es)
P=S.Matrix([[1,u],[0,1]]);Q=S.Matrix([[1,0],[-wq,1]])
check('root-entry cocycle',P*E+D*Q,S.Matrix([[ds[0]+es[0]+u*es[2]-wq*ds[1],ds[1]+es[1]+u*es[3]],[ds[2]+es[2]-wq*ds[3],ds[3]+es[3]]]))
a,alpha=S.symbols('a alpha',nonzero=True)
check('torus weights',S.diag(a,a**-1)*D*S.diag(alpha,alpha**-1),S.Matrix([[a*alpha*ds[0],a/alpha*ds[1]],[alpha/a*ds[2],ds[3]/(a*alpha)]]))
u,ub,a,b,bb,d=S.symbols('u ub a b bb d');MM=S.Matrix([[a,b],[bb,d]]);RR=lambda x:S.Matrix([[1,x],[0,1]])
check('Hermitian module norm extraction',RR(u)*MM*RR(ub).T+RR(-u)*MM*RR(-ub).T-2*MM,S.diag(2*u*ub*d,0))
# q=3 coordinates are reduced exactly in F3[T]/(T^2-T-1).
T=S.symbols('T');poly=S.Poly(T*T-T-1,T,modulus=3)
def red(x):
 num,den=S.fraction(S.together(x));return (S.Poly(num,T,modulus=3)*S.invert(S.Poly(den,T,modulus=3),poly)).rem(poly)
B3=S.Matrix([[1,1,T,-T],[0,1,0,0],[0,1-T,0,1],[0,T-1,1,0]])
assert all(red(x).is_zero for x in B.subs({t:T,tb:1-T})-B3);checks.append('q3 explicit B coordinates')
assert red(T**4+1).is_zero and not red(T**2-1).is_zero;checks.append('q3 parameter order eight')
report={'status':'PASS','executed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'exact_identities':len(checks),'checks':checks,'scope':'Rational matrix identities and exact q3 polynomial reduction. The uniform subgroup/weight/module arguments remain written proof obligations; q3 group order and IP are checked by the separate GAP certificate.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
