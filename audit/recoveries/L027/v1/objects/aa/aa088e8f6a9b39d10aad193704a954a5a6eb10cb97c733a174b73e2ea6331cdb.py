"""Exact rational identities in the all-field rank-four proof."""
import sys
if sys.flags.optimize:
    raise SystemExit('normal Python required')
from pathlib import Path
import argparse, json
import sympy as S

def need(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    arg=ap.parse_args()
    need(not arg.out.exists(),'fresh output')
    x,r,s,u,v=S.symbols('x r s u v',nonzero=True)
    I=S.eye(3)
    a=S.Matrix([[x,1,0],[0,1+1/x,-1/x],[0,1,0]])
    b=S.Matrix([[-1/x,0,0],[0,0,1],[0,x,0]])
    c=S.Matrix([[x,0,0],[x-1/x,1,0],[x-1/x,0,1/x]])
    D=S.Matrix([[(x-1/x)**-1,0,0],[0,1,1],[0,1,x]])
    h=lambda t:S.diag(t**-2,t,t)
    K=lambda u,v:S.Matrix([[1,0,0],[u,1,0],[v,0,1]])
    checked=[]
    def eq(name,L,R):
        need(all(S.cancel(t)==0 for t in L-R),name)
        checked.append(name)
    for name,g in [('a',a),('b',b),('c',c)]:
        need(S.cancel(g.det()-1)==0,'determinant '+name)
        checked.append('determinant '+name)
    eq('middle square',b*b,h(x))
    eq('unipotent addition',K(u,v)*K(r,s),K(u+r,v+s))
    C=(r**3-s**3)*(1-x*x)
    word=h(r)*c.inv()*h(s/r)*c*h(1/s)
    eq('corrected source word',word,K(C/x,C))
    eq('unipotent conjugation',c.inv()*K(u,v)*c,K(x*u,x*x*v))
    need(S.cancel(word[1,0]-C)!=0,'the printed uncorrected word must differ')
    # One literal field specialization is sufficient to witness the printed error.
    printed=int(C.subs({x:2,r:1,s:2}))%5
    # The specialization can be fractional before reduction: use modular division.
    fraction=S.cancel(word[1,0]).subs({x:2,r:1,s:2})
    actual=(int(S.numer(fraction))*pow(int(S.denom(fraction)),-1,5))%5
    need(actual!=printed,'field-five source correction witness')
    for name,g,target in [('a',a,c.inv()),('b',b,b.inv()),('c',c,a.inv())]:
        eq('duality '+name,D*g.inv().T*D.inv(),target)
    eq('symmetric duality',D,D.T)
    for name,g in [('ab',a*b),('bc',b*c),('abc',a*b*c)]:
        eq('involution '+name,g*g,I)
    # The matrix of each involution plus I has the displayed axis as kernel.
    axis1=S.Matrix([[0,0,1]])
    axis2=S.Matrix([[1-x,0,-1]])
    eq('axis ab',a*b+I,S.Matrix([1,(x+1)/x,2])*axis1)
    eq('axis abc',a*b*c+I,S.Matrix([-1/x,-(x+1)/x**2,-(x+1)/x])*axis2)
    for name,g,values,points in [
        ('a',a,[x,1,1/x],[[1,0,0],[1,1-x,1-x],[1,1/x-x,1-x*x]]),
        ('c',c,[x,1,1/x],[[x,1+x,x],[0,1,0],[0,0,1]])]:
        for i,(value,point) in enumerate(zip(values,points)):
            vec=S.Matrix(point)
            eq('eigenpoint '+name+str(i),g*vec,value*vec)
    def E(i,j,t):
        M=I.copy();M[i,j]=t;return M
    for i,j,k in [(1,0,2),(2,0,1)]:
        L=E(i,j,u);R=E(j,k,v)
        eq('root commutator '+str((i,j,k)),L*R*L.inv()*R.inv(),E(i,k,u*v))
    eq('dual radical',D*K(u,v).inv().T*D.inv(),
       I-S.Matrix([1/(x-1/x),0,0])*S.Matrix([[0,u,v]])*D.inv())
    report=dict(status='PASS_EXACT_RATIONAL_IDENTITIES',identities=checked,
                hypotheses='Characteristic arbitrary, x nonzero and x^2!=1; rational identities are read after denominators are inverted.',
                source_word_correction_mod5=dict(x=2,r=1,s=2,actual_first_coordinate=actual,printed_first_coordinate=printed),
                whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
    arg.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':
    main()
