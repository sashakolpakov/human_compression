import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
import argparse,json
from pathlib import Path
import sympy as s
def need(ok,msg):
 if not ok:raise ValueError(msg)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);arg=ap.parse_args();done=[]
 a,x,y,z,X,Y,Z,k=s.symbols('a x y z X Y Z k');I=s.eye(3)
 def eq(name,A,B):need(all(s.cancel(t)==0 for t in A-B),name);done.append(name)
 M=lambda x,y:s.Matrix([[1,0,0],[0,1,0],[x,y,1]])
 U=lambda x,y,z:s.Matrix([[1,x,0],[0,1,0],[y,z,1]])
 d1=s.diag(1,-1,-1);d2=s.diag(-1,1,-1);d3=s.diag(-1,-1,1)
 A=s.Matrix([[a,-a-1,0],[a-1,-a,0],[0,0,-1]]);t=M(1,-1)*A
 eq('generic-square',t*t,I);eq('actual-kernel',(t*d3)**2,M(2,-2))
 c1=M(0,1/(1-a));c2=M(-1/(a+1),0)
 for i,(d,c) in enumerate([(d1,c1),(d2,c2)]):
  eq('complement-t'+str(i),c.inv()*A*c,t);eq('complement-fixed-end'+str(i),c.inv()*d*c,d)
  eq('central-lift'+str(i),c.inv()*d3*c,M(-2*c[2,0],-2*c[2,1])*d3)
 eq('translation-action',A.inv()*M(x,y)*A,M(-a*x-(a-1)*y,(a+1)*x+a*y))
 eq('heisenberg-law',U(x,y,z)*U(X,Y,Z),U(x+X,y+Y,z+Z+y*X))
 h=U(2,1,1);hh=d2*h*d2
 eq('heisenberg-conjugate',hh,U(-2,1,-1));eq('heisenberg-commutator',h.inv()*hh.inv()*h*hh,U(0,0,-4))
 T=h*d1;eq('heisenberg-middle',T,s.Matrix([[1,-2,0],[0,-1,0],[1,-1,-1]]))
 eq('second-end-kernel',(d2*T)**2,U(-4,0,-2));eq('third-end-kernel',(d3*T)**2,U(0,-2,2))
 eq('second-end-third-coset',U(x,0,x/2)*(d2*T),U(x-2,1,x/2-1)*d3)
 eq('third-end-second-coset',U(0,y,-y)*(d3*T),U(2,y-1,y-1)*d2)
 u1,u2,u3,f1,f2=s.symbols('u1 u2 u3 f1 f2',nonzero=True);f3=(1-u1*f1-u2*f2)/u3
 u=s.Matrix([u1,u2,u3]);f=s.Matrix([[f1,f2,f3]]);H=-I+2*u*f;Q=s.diag(f1/u1,f2/u2,f3/u3)
 eq('conic-homology-square',H*H,I);eq('conic-form',H.T*Q*H,Q)
 result=dict(status='PASS_EXACT_ODD_THREE_IDENTITIES',count=len(done),identities=done);arg.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
