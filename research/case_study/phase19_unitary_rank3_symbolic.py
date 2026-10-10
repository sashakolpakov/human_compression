#!/usr/bin/env python3
"""Exact identities for the exploratory Pauli/reflection generation proof."""
from pathlib import Path
import hashlib,json,datetime
import sympy as S
z,X=S.symbols('z X');s=-z*z
I=S.eye(4);H=S.diag(1,-1,1,-1);A=S.diag(1,1,-1,-1)
C=S.Matrix([[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]])
v=S.Matrix([z,-1,s-z,s+1]);bar=lambda M:M.subs(z,-z)
B=I+v*bar(v).T*H;n=v+C*v;m=A*n;U=S.expand((B*C)**2);N=U-I;t=2*s*(z-1)
checks=[]
def check(label,lhs,rhs):
 d=lhs-rhs
 if isinstance(d,S.MatrixBase):assert all(S.expand(x)==0 for x in d),label
 else:assert S.expand(d)==0,label
 checks.append(label)
check('v norm',(bar(v).T*H*v)[0],-2)
for label,g in [('A',A),('B',B),('C',C)]:
 check(label+' square',g*g,I);check(label+' unitary',bar(g).T*H*g,H)
check('A determinant',A.det(),1);check('B determinant',B.det(),-1);check('C determinant',C.det(),1)
check('outer anticommute',A*C,-C*A)
check('n coordinates',n,s*S.Matrix([1,1,1,1]));check('m coordinates',m,s*S.Matrix([1,1,-1,-1]))
W=S.Matrix.hstack(n,m)
check('W isotropic',bar(W).T*H*W,S.zeros(2))
check('A projection',A*W,W*S.Matrix([[0,1],[1,0]]));check('C projection',C*W,W*S.diag(1,-1));check('U projection',U*W,W*S.Matrix([[1,t],[0,1]]))
check('N square',N*N,2*n*bar(n).T*H);check('N cube',N*N*N,S.zeros(4))
check('BC characteristic', (B*C).charpoly(X).as_expr(),(X-1)**3*(X+1))
check('AB characteristic', (A*B).charpoly(X).as_expr(),(X-1)*(X+1)*(X*X-2*s*X+1))
check('B fixes n',B*n,n)
check('adjacent planes pairing',(bar(m).T*H*B*m)[0],4*s*s*(1+s))
check('t trace',t+t.subs(z,-z),-4*s);check('t tracezero part',t-t.subs(z,-z),4*s*z);check('t square difference',t*t-t.subs(z,-z)**2,-16*s*s*z)
u,w,uq,wq=S.symbols('u w uq wq');ds=S.symbols('a b c d');es=S.symbols('e f g h');D=S.Matrix(2,2,ds);E=S.Matrix(2,2,es)
P=S.Matrix([[1,u],[0,1]]);Q=S.Matrix([[1,0],[-wq,1]])
check('root-entry cocycle',P*E+D*Q,S.Matrix([[ds[0]+es[0]+u*es[2]-wq*ds[1],ds[1]+es[1]+u*es[3]],[ds[2]+es[2]-wq*ds[3],ds[3]+es[3]]]))
a,alpha=S.symbols('a alpha',nonzero=True)
check('torus weights',S.diag(a,a**-1)*D*S.diag(alpha,alpha**-1),S.Matrix([[a*alpha*ds[0],a/alpha*ds[1]],[alpha/a*ds[2],ds[3]/(a*alpha)]]))
u,ub,a,b,bb,d=S.symbols('u ub a b bb d');M=S.Matrix([[a,b],[bb,d]])
R=lambda x:S.Matrix([[1,x],[0,1]])
check('Hermitian module norm extraction',R(u)*M*R(ub).T+R(-u)*M*R(-ub).T-2*M,S.diag(2*u*ub*d,0))
report={'status':'PASS','executed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'exact_identities':len(checks),'checks':checks,'scope':'Parameter identities only. The subgroup classification, kernel argument and all-field generation remain written proof obligations.'}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
