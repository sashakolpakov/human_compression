"""Exact polynomial checks for the unitary template; no generation/IP proof."""
from pathlib import Path
import hashlib,json,datetime
import sympy as s
k=s.symbols('k');i=s.I
I=s.eye(4);I2=s.eye(2);H=s.diag(1,-1,1,-1)
r0=s.diag(1,1,-1,-1)
r1=s.Matrix([[1,0,0,0],[0,0,0,1],[0,0,-1,0],[0,1,0,0]])
r3=s.zeros(2).row_join(I2).col_join((-I2).row_join(s.zeros(2)))
R=s.Matrix([[0,i],[i,0]]);S=s.Matrix([[k,i-k],[i+k,-k]])
r2=s.diag(R,S);rr=[r0,r1,r2,r3];checks=[]
def check(label,mat):
 assert all(s.expand(x)==0 for x in mat),label
 checks.append(label)
for j,r in enumerate(rr):
 check(f'determinant_{j}',[r.det()-1])
 check(f'unitary_{j}',r*H*r.subs(k,-k).T-H)
 check(f'square_{j}',r*r-(I if j<2 else -I))
check('commute_02',r0*r2-r2*r0)
check('anticommute_03',r0*r3+r3*r0)
check('anticommute_13',r1*r3+r3*r1)
check('d',(r0*r1)**2-s.diag(1,-1,1,-1))
U=s.diag(s.Matrix([[1-i*k,i*k],[-i*k,1+i*k]]),s.Matrix([[1+i*k,-i*k],[i*k,1-i*k]]))
check('u',(r2*r3)**2-U)
check('u_square_zero',(U-I)**2)
x=s.symbols('x')
check('middle_characteristic',[(r1*r2).charpoly(x).as_expr()-(x**4+k*x**3-k*x+1)])
check('last_characteristic',[(r2*r3).charpoly(x).as_expr()-(x-1)**2*(x+1)**2])
Z=s.diag(1,-1)
check('first_kernel_word',(Z*R)**2-I2)
check('second_kernel_trace',[s.trace(Z*S)-2*k])
check('second_kernel_determinant',[(Z*S).det()+1])
B=s.diag(i+k,i+k,i-k,i+k)
A=s.Matrix([[0,-k,k-2*i,k],[k,0,k,k+2*i],[-k+2*i,-k,0,-k],[-k,-k-2*i,k,0]])
check('symmetric_B',B-B.T)
check('alternating_A',A+A.T)
check('determinant_A',[A.det()-(k*k-4)**2])
for j,eps in [(0,1),(1,1),(2,-1)]:check(f'B_multiplier_{j}',rr[j]*B*rr[j].T-eps*B)
for j,eps in [(1,-1),(2,1),(3,1)]:check(f'A_multiplier_{j}',rr[j]*A*rr[j].T-eps*A)
check('A_real_structure',A*H*A.subs(k,-k)*H-(4-k*k)*I)
report={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_identity_count':len(checks),'checks':checks,'coefficient_ring':'Z[i,k]/(i^2+1); bar fixes i and sends k to -k','scope':'Polynomial identities only; group generation, Dickson inputs, parameter existence, and intersection property are not certified by this script.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'proof_sha256':hashlib.sha256(Path(__file__).with_suffix('.md').read_bytes()).hexdigest() if Path(__file__).with_suffix('.md').exists() else hashlib.sha256(Path(__file__).with_name('phase11_unitary_template.md').read_bytes()).hexdigest(),'sympy_version':s.__version__}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(checks),'exact polynomial identities')
