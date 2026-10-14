import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
import argparse,json
from pathlib import Path
import sympy as s
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);arg=ap.parse_args()
    a,b,d,e,c,f=s.symbols('a b d e c f',nonzero=True);I=s.eye(3);done=[]
    def eq(name,A,B):
        need(all(s.cancel(x)==0 for x in A-B),name);done.append(name)
    r0=s.diag(1,-1,-1);r3=s.diag(-1,-1,1)
    r1=s.Matrix([[a,b,0],[(1-a*a)/b,-a,0],[0,0,-1]])
    r2=s.Matrix([[-1,0,0],[0,-d,(1-d*d)/e],[0,e,d]])
    Q=s.diag((1-a*a)/b**2,1,(1-d*d)/e**2)
    for k,r in enumerate([r0,r1,r2,r3]):eq('square'+str(k),r*r,I);eq('quadratic'+str(k),r.T*Q*r,Q)
    eq('zero-a-forces-last',(r0*r1.subs(a,0))**2,r3)
    t1=s.Matrix([[1,0,0],[c,-1,0],[0,0,-1]])
    t2=s.Matrix([[-1,0,0],[0,-d,f],[0,e,d]])
    result=s.Matrix([[1,0,0],[(1-d)*c,1,0],[e*c,0,1]])
    eq('one-zero-defect',((t1*t2)**2).subs(f,(1-d*d)/e),result)
    h=lambda x,y,z:s.Matrix([[1,0,0],[x,1,0],[z,y,1]])
    u=h(1,0,0)*r0;v=h(0,-1,0)*r3
    eq('Heisenberg-middle',(u*v)**2,h(0,0,1))
    eq('Heisenberg-first-end',r0*v,v*r0);eq('Heisenberg-second-end',u*r3,r3*u)
    x,y,z,X,Y,Z=s.symbols('x y z X Y Z')
    eq('Heisenberg-law',h(x,y,z)*h(X,Y,Z),h(x+X,y+Y,z+Z+y*X))
    obj={'status':'PASS_EXACT_ODD_IDENTITIES','count':len(done),'identities':done}
    arg.out.write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps(obj))
if __name__=='__main__':main()
