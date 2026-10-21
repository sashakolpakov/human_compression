"""Exact parameter identities and the subfield-lattice arithmetic, not a group census."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Use ordinary Python')
from pathlib import Path
import json, math
import sympy as s

def need(ok, message):
    if not ok:
        raise ValueError(message)
def run():
    a,b,A,B,c,f,C,F,T,t = s.symbols('a b A B c f C F T t', nonzero=True)
    def U(x,y,X,Y):
        return s.Matrix([[1,0,0,0],[x,1,0,0],[x*X+y,X,1,0],[x*x*X+x*y+Y,y,x,1]])
    h = s.diag(T,t,1/t,1/T)
    w = s.zeros(4)
    for i in range(4):
        w[i,3-i] = 1
    closed = U(a,b,A,B)*h
    opened = closed*w*U(c,f,C,F)
    # A,B,C,F stand for the respective theta-powers. These particular
    # entries require no additional identity among those powers.
    identities = [closed[1,1]-t, closed[1,0]/closed[0,0]-a,
                  closed[3,1]/t-b, opened[0,3]-T,
                  opened[0,2]/opened[0,3]-c,
                  opened[0,1]/opened[0,3]-f,
                  opened[1,3]/opened[0,3]-a,
                  opened[2,3]/opened[0,3]-a*A-b]
    need(all(s.cancel(x)==0 for x in identities), 'All eight parameter identities')
    primes = [3,5,7,11]
    n = 3*math.prod(primes)
    exponents = {mask:n//math.prod(p for i,p in enumerate(primes) if mask>>i&1) for mask in range(16)}
    need(len(set(exponents.values()))==16 and exponents[15]==3, 'Sixteen distinct exponents and simple bottom')
    edges = []
    for mask,e in exponents.items():
        for i,p in enumerate(primes):
            if not mask>>i&1:
                smaller=exponents[mask|1<<i]
                need(smaller>1 and e==p*smaller, 'Prime-degree simple subfield step')
                edges.append([mask,mask|1<<i,p])
    for j in exponents:
        for k in exponents:
            need(math.gcd(exponents[j],exponents[k])==exponents[j|k], 'All field intersections')
    need(len(edges)==32 and len(primes)-1<4, 'Cube edges and literal source rank bound')
    return dict(status='PASS_L110_SUBFIELD_BOUNDARY_CONTROLS',symbolic_parameter_identities=8,
                field_degree=n,exponents=exponents,maximality_edges=edges,meet_checks=256,
                source_maximum_pure_rank=3,example_rank=4,
                scope='Supplementary identities and arithmetic only; classical Suzuki model and maximality are retained written premises.',
                whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
if __name__ == '__main__':
    report=run()
    Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
