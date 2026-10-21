"""Exact identities over Q[w]/(w^2+w+1) for the rank-five proof."""
import sys
if sys.flags.optimize:
    raise SystemExit('normal Python required')
import argparse
import json
from pathlib import Path
import sympy as S

def need(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--damage',choices=['unipotent','conic','duality'])
    args=ap.parse_args();need(not args.out.exists(),'fresh output')
    w=S.symbols('w');relation=w*w+w+1;I=S.eye(3);checked=[]
    def red(t):
        nu,de=S.fraction(S.cancel(t))
        return S.rem(nu*S.invert(de,relation,w),relation,w)
    def mat(M):return M.applyfunc(red)
    def eq(name,L,R):
        need(mat(L-R)==S.zeros(*L.shape),name);checked.append(name)
    def sc(name,x,y):eq(name,S.Matrix([[x]]),S.Matrix([[y]]))
    def marking(k):
        return [S.diag(1,w,w*w),S.Matrix([[-1,0,-k],[0,-w*w,-k*w*w],[0,0,w]]),
                S.Matrix([[1,k,0],[0,k,1],[0,-1,0]]),S.Matrix([[0,1,0],[0,0,1],[1,0,0]])]
    P12=S.Matrix([[0,1,0],[1,0,0],[0,0,1]])
    P23=S.Matrix([[1,0,0],[0,0,1],[0,1,0]])
    for k in [1,-1]:
        a,b,c,d=marking(k);tag=str(k)+':'
        for i,g in enumerate([a,b,c,d]):sc(tag+'det'+str(i),g.det(),1)
        target=I.copy();target[0,2]=k*(2*w+1);target[1,2]=-k*(2*w+1)
        if args.damage=='unipotent':target[0,2]*=-1
        eq(tag+'unipotent',b*b*a.inv(),target)
        eq(tag+'ab',a*b,S.Matrix([[-1,0,-k],[0,-1,-k],[0,0,1]]))
        eq(tag+'abc',a*b*c,-P23);eq(tag+'abcd',a*b*c*d,-P12)
        for nm,g,scalar in [('ab',a*b,1),('bc',b*c,1),('cd',c*d,1),('abc',a*b*c,1),('bcd',b*c*d,w*w),('abcd',a*b*c*d,1)]:
            eq(tag+nm+'square',g*g,scalar*I)
        for nm,g,order in [('a',a,3),('b',b,6),('c',c,6 if k==1 else 3),('d',d,3)]:
            eq(tag+nm+'power',g**order,I)
        aa,bb,cc,dd=[mat(g.subs(w,w*w)) for g in marking(k)]
        eq(tag+'mirror a',aa,a.inv());eq(tag+'mirror b',bb,a*a*b)
        eq(tag+'mirror c',cc,c);eq(tag+'mirror d',dd,d)
        Jall=S.ones(3);sc(tag+'centralizer coefficient',(Jall*a*b-a*b*Jall)[2,0],-2)
    a,b,c,d=marking(1)
    J=S.Matrix([[w,w*w,1],[w*w,w,1],[1,1,1]])
    sc('duality determinant',J.det(),-3*(2*w+1))
    for i,(g,h,scalar) in enumerate(zip([a,b,c,d],[mat(h.inv().subs(w,w*w)) for h in [d,c,b,a]],[w*w,w,w*w,w])):
        if args.damage=='duality' and i==0:scalar=1
        eq('duality'+str(i),J.inv()*g*J,scalar*h)
    P=S.Matrix([[1,1,0],[0,w,1],[0,w*w,0]])
    bp=S.diag(-1,w,-w*w);cp=S.Matrix([[1,0,-w*w],[0,-w*w,-w],[0,0,-w]])
    eq('point b',P.inv()*b*P,bp);eq('point c',P.inv()*c*P,cp)
    comm=I.copy();comm[0,2]=-(2*w+1);comm[1,2]=w
    eq('point commutator',bp*cp*bp.inv()*cp.inv(),comm)
    r=S.Matrix([1,w,w*w]);eq('point b eigen',b*r,w*r);eq('point c eigen',c*r,-w*w*r)
    a,b,c,d=marking(-1)
    T=S.Matrix([[1,0,w],[0,0,1],[0,1,w*w]])
    def iota(g):
        aa,bb,cc,dd=list(g)
        return S.Matrix([[aa*aa,2*aa*bb,bb*bb],[aa*cc,aa*dd+bb*cc,bb*dd],[cc*cc,2*cc*dd,dd*dd]])/g.det()
    bg=S.diag(-w*w,1);cg=S.Matrix([[w,-w*w],[0,1]]);dg=S.Matrix([[-w*w,1],[-w,0]])
    if args.damage=='conic':cg[0,1]=w*w
    for nm,g,gg,scalar in [('b',b,bg,w*w),('c',c,cg,w),('d',d,dg,w*w)]:
        eq('conic '+nm,scalar*T*g*T.inv(),iota(gg))
        sc('conic det '+nm,iota(gg).det(),1)
    eq('opposite root transport',S.Matrix([[1,-w],[0,1]])*dg,S.Matrix([[0,1],[-w,0]]))
    ccom=mat(bg*cg*bg.inv()*cg.inv())
    sc('affine commutator first diagonal',ccom[0,0],1)
    sc('affine commutator second diagonal',ccom[1,1],1)
    sc('affine commutator lower',ccom[1,0],0)
    need(red(ccom[0,1])!=0,'nonzero affine commutator')
    checked.append('nonzero affine commutator')
    report=dict(status='PASS_L027_RANK_FIVE_LITERAL_IDENTITIES',identities=checked,
                count=len(checked),coefficient_domain='Q[w]/(w^2+w+1), with characteristic restrictions p>=5 stated in the proof',
                affine_commutator_parameter=str(red(ccom[0,1])),whole_original_credit=0,new_question_credit=0)
    args.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
