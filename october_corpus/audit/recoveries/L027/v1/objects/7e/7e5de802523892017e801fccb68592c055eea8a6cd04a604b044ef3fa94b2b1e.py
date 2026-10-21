import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
import argparse,json
from pathlib import Path
import sympy as s
def need(ok,msg):
 if not ok:raise ValueError(msg)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);arg=ap.parse_args()
 a,b,x,y,z,u,v=s.symbols('a b x y z u v');variables=(a,b,x,y,z,u,v);I=s.eye(3);done=[]
 def E(i,j):
  X=s.zeros(3);X[i-1,j-1]=1;return X
 def eq(name,A,B,mod=None):
  D=A-B
  good=all((s.Poly(s.expand(t),*variables,modulus=mod).is_zero if mod else s.expand(t)==0) for t in D)
  need(good,name);done.append(name)
 R=[I+E(2,3),I+a*E(3,1),I+b*E(1,3),I+E(2,1)]
 U=s.Matrix([0,1,a]);f=s.Matrix([[x,y,z]]);S0=I+U*s.Matrix([[1,0,0]]);S1=I+s.Matrix([0,1,0])*s.Matrix([[1,0,1]])
 eq('even-other-first',R[1]*R[3],S0,2);eq('even-other-second',R[0]*R[3],S1,2)
 S2=I+U*f;A=R[3]*S2;B=R[2]*R[3]
 eq('even-first-rotation',A,I+E(2,1)+U*f,2);eq('even-last-rotation',B,I+b*E(1,3)+E(2,1),2)
 eq('even-first-row-obstruction',(B*A-A*B)[:1,:],a*b*f,2)
 eq('even-last-unipotent',(B-I)**3,s.zeros(3),2)
 eq('even-involution-condition',S2*S2-I,U*(y+a*z)*f,2)
 r0=s.diag(1,-1,-1);r1=s.Matrix([[1,0,0],[1,-1,0],[0,0,-1]])
 r2=s.Matrix([[-1,0,0],[0,-1,0],[0,1,1]]);r3=s.diag(-1,-1,1)
 t0=s.Matrix([[-1,0,0],[-1,1,0],[0,0,-1]]);t1=s.diag(-1,1,-1);t2=s.Matrix([[-1,0,u],[0,-1,v],[0,0,1]])
 eq('odd-other-first',r1*r3,t0);eq('odd-other-second',r0*r3,t1)
 eq('odd-involution',t2*t2,I);eq('odd-outer-commutation',t0*t2-t2*t0,(2*v-u)*E(2,3))
 A=r3*t2;B=r2*r3
 eq('odd-first-rotation',A,I-u*E(1,3)-v*E(2,3));eq('odd-last-rotation',B,I-E(3,2))
 eq('odd-last-unipotent',(B-I)**2,s.zeros(3))
 eq('odd-commutator-obstruction',A*B-B*A,u*E(1,2)+v*E(2,2)-v*E(3,3))
 result=dict(status='PASS_EXACT_RANK_OBSTRUCTIONS',identities=done,count=len(done))
 arg.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
