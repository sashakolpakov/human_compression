"""Independent symbolic and lattice arithmetic controls.

The library expressions below are written directly from the manuscript;
the polynomial list arithmetic of the author programs is not imported.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse, json
from pathlib import Path
import sympy as s


def need(b, reason):
    if not b:
        raise ValueError(reason)


def expression(coefficients, q):
    return sum(s.Rational(*c) * q**i if isinstance(c,list) else c*q**i
               for i,c in enumerate(coefficients))


def main():
    a=argparse.ArgumentParser();a.add_argument('--input',type=Path,required=True);a.add_argument('--out',type=Path,required=True);p=a.parse_args()
    need(not p.out.exists(), 'fresh output required')
    q=s.Symbol('q');z=s.Symbol('z')
    orders={
        'E8':q**120*s.prod(q**i-1 for i in [2,8,12,14,18,20,24,30]),
        'E7':q**63*s.prod(q**i-1 for i in [2,6,8,10,12,14,18]),
        'E6+':q**36*s.prod(q**i-1 for i in [2,5,6,8,9,12]),
        'E6-':q**36*s.prod(q**i-(-1)**i for i in [2,5,6,8,9,12]),
        'F4':q**24*s.prod(q**i-1 for i in [2,6,8,12]),
        'G2':q**6*(q**2-1)*(q**6-1),
        '3D4':q**12*(q**8+q**4+1)*(q**6-1)*(q**2-1),
        '2F4':q**12*(q**6+1)*(q**4-1)*(q**3+1)*(q-1),
        '2G2':q**3*(q**3+1)*(q-1),
        '2B2':q**2*(q**2+1)*(q-1)}
    lower=json.loads((p.input/'exceptional_lower_bounds.json').read_text())
    need(len(lower['rows'])==18,'all parity cases')
    for row in lower['rows']:
        need(s.expand(orders[row['family']]-expression(row['group_order'],q))==0,'independent group order')
        P=row['lower_denominator']*orders[row['family']]-q**row['lower_exponent']*expression(row['centralizer_order'],q)
        need(s.expand(P-expression(row['difference'],q))==0,'actual lower-bound difference')
        shifted=s.Poly(P.subs(q,z+row['minimum']),z)
        need(all(c>=0 for c in shifted.all_coeffs()) and shifted.eval(0)>0,'independent positive translation')
        need(s.expand(shifted.as_expr()-expression(row['shifted_coefficients'],z))==0,'every stored coefficient')
    final=json.loads((p.input/'exceptional_coset_inequalities.json').read_text())
    need(len(final['rows'])==9 and len(final['fixed'])==3,'complete final cases')
    for row in final['rows']:
        L,T,C,B=[expression(row[k],q) for k in ['lower','torus_upper','mu_upper','other_maximals_upper']]
        P=L-row['kappa']*T*C-B-row['weyl_order']*T
        need(s.expand(P-expression(row['difference'],q))==0,'actual final difference')
        shifted=s.Poly(P.subs(q,z+row['minimum']),z)
        need(all(c>=0 for c in shifted.all_coeffs()) and shifted.eval(0)>0,'independent final translation')
        need(s.expand(shifted.as_expr()-expression(row['shifted_coefficients'],z))==0,'every final stored coefficient')
    for row in final['fixed']:
        L=s.Rational(row['lower']);margin=L-row['kappa']*row['torus']*row['mu']-row['other_maximals']-row['normalizer']
        need(margin==s.Rational(row['margin']) and margin>0,'fixed positive margin')
    auxiliary=[
        ('E8 odd',2*q**84*(q**20+q**19)-8*(q**64+q**63),3),
        ('E7 odd',2*q**42*(q**12+q**11)-16*(q**35+q**34),3),
        ('F4 odd',q**22-4*(q**2+1)*(q**12+q**11),3),
        ('G2 odd',q**5-2*(q**2+1)**2,3),
        ('3D4 odd',q**11-2*(q**2+1)*(q**6+1),3),
        ('E8 field',2*q**84*(q**20+q**19)-4*q**64,2),
        ('E7 field',2*q**42*(q**12+q**11)-4*q**35,2),
        ('E6 field',2*(q**28+q**27)-4*q**21,2),
        ('E6 C4',2*(q**28+q**27)-2*(q**20+q**19),2),
        ('F4 field',q**22-4*q**14,2),
        ('G2 field',q**5-4*q**4,5),
        ('3D4 field',q**11-4*q**8,2),
        ('F4 graph field',q**22-2*(q**14+q**13),2),
        ('G2 graph field',q**5-2*(q**4+q**3),5),
        ('small Ree',2*q**2-(q*(q-1)+1),3)]
    for name,P,minimum in auxiliary:
        poly=s.Poly(P.subs(q,z+minimum),z)
        need(all(c>=0 for c in poly.all_coeffs()) and poly.eval(0)>0,'auxiliary '+name)
    # Verify each rational solution by integer equations, independent of inversion.
    lattice=json.loads((p.input/'lattice/report.json').read_text())
    need(len(lattice['cases'])==4,'all four lattice cases')
    need(sorted(r['name'] for r in lattice['cases'])==['E6','E7order14','E7order18','F4'],'actual lattice cases')
    root_equations=0
    for row in lattice['cases']:
        M=row['matrix'];n=len(M);q0=row['q'];sign=row['frobenius_sign'];d=row['simple_group_index']
        roots={tuple(r) for r in row['roots']}
        need(len(roots)==len(row['roots'])=={'E6':72,'F4':48,'E7order14':126,'E7order18':126}[row['name']], 'literal root inventory')
        need(all(tuple(int(i==j) for i in range(n)) in roots for j in range(n)), 'simple roots retained')
        for root in roots:
            for i in range(n):
                v=list(root);v[i]-=sum(row['cartan'][i][j]*root[j] for j in range(n))
                need(tuple(v) in roots,'independent reflection closure')
        for root,coordinates in zip(row['roots'],row['root_lattice_coordinates'],strict=True):
            v=[s.Rational(a,b) for a,b in coordinates]
            need(any(x.q>1 for x in v),'root nonintegrality')
            need(all(sign*q0*sum(M[i][j]*v[j] for j in range(n))-v[i]==d*root[i] for i in range(n)), 'literal root equation')
            root_equations+=1
    report=dict(status='PASS_INDEPENDENT_EXCEPTIONAL_ARITHMETIC',lower_cases=18,final_families=9,fixed_cases=3,auxiliary_inequalities=len(auxiliary),root_equations=root_equations,whole_original_credit=0)
    p.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


if __name__=='__main__':main()
