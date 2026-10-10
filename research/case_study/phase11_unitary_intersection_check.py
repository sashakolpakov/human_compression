"""Exact identities for the conditional IP proof, not a group-proof kernel."""
from pathlib import Path
import datetime,hashlib,json
import sympy as s
k,t,x=s.symbols('k t x');i=s.I;I2=s.eye(2);I4=s.eye(4)
H=s.diag(1,-1,1,-1)
R=s.Matrix([[0,i],[i,0]]);S=s.Matrix([[k,i-k],[i+k,-k]])
r0=s.diag(1,1,-1,-1);r1=s.Matrix([[1,0,0,0],[0,0,0,1],[0,0,-1,0],[0,1,0,0]])
r2=s.diag(R,S);r3=s.zeros(2).row_join(I2).col_join((-I2).row_join(s.zeros(2)))
A=s.Matrix([[0,-k,k-2*i,k],[k,0,k,k+2*i],[-k+2*i,-k,0,-k],[-k,-k-2*i,k,0]])
B=s.diag(i+k,i+k,i-k,i+k)
checks=[]
def check(label,items):
 assert all(s.cancel(s.expand(z))==0 for z in items),label
 checks.append(label)
T=r1*r2;P=x**4+k*x**3-k*x+1
check('A_compatibility',A*H*A.subs(k,-k)*H-(4-k*k)*I4)
check('B_compatibility',B*H*B.subs(k,-k)*H-(-1-k*k)*I4)
v=s.eye(4)[:,0]
check('middle_cyclic',[s.Matrix.hstack(v,T*v,T*T*v,T*T*T*v).det()-i*(k-i)])
check('middle_discriminant',[s.discriminant(P,x)-4*(k*k-8)**2*(k*k+1)])
check('opposite_root_difference',[P-P.subs(x,-x)-2*k*x*(x*x-1)])
W=A*B.inv()
check('middle_commutes_ratio',T*W-W*T)
F=A.inv()*B
factor=-256*k**8*(k-i)*(k+i)**7*(k*k-8)**2/(k*k-4)**10
check('ratio_discriminant',[s.discriminant(F.charpoly(x).as_expr(),x)-factor])
check('inverse_ratio_similarity',B*F.inv()*B.inv()-W)
U1=I2+t*s.Matrix([[-i*k,i*k],[-i*k,i*k]])
U2=I2-t*s.Matrix([[-i*k,i*k],[-i*k,i*k]])
even=U1*((i+k)*I2)*U1.T
check('even_power_off_diagonal',[even[0,1]+2*(i+k)*k*k*t*t])
odd=R*U2*s.diag(i-k,i+k)*U2.T*R.T
check('odd_power_off_diagonal',[odd[0,1]-2*i*k*k*t*(t+1)])
check('odd_power_diagonal_difference',[odd[0,0]-odd[1,1]+2*k*(2*t+1)])
d=s.diag(1,-1,1,-1)
for label,D in [('r0',r0),('d',d),('r0d',r0*d)]:
 # Complete coefficient-free sign pattern: neither scalar sign fixes A.
 assert D*A*D.T!=A and D*A*D.T!=-A,label
 checks.append('diagonal_Klein_'+label)
report={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_check_count':len(checks),'checks':checks,'coefficient_ring':'Z[i,k,t]/(i^2+1), localized at displayed nonzero denominators','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'proof_sha256':hashlib.sha256(Path(__file__).with_name('phase11_unitary_intersection.md').read_bytes()).hexdigest(),'sympy_version':s.__version__,'scope':'Matrix identities and discriminants only. Descent, regular-torus classification, group intersections and parameter existence retain their written-proof scope.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(checks),'exact checks')
