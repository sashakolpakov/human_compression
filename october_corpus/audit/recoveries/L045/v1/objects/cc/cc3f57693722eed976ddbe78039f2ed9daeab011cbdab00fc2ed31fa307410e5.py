"""Exact root-lattice checks for the two small exceptional tori.

This verifies the finite lattice and Weyl-group calculations only. The
algebraic-group interpretation of a rational torus is a separate premise.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
from pathlib import Path
import argparse, json, subprocess
from collections import deque
import sympy as sp


def need(b, text):
    if not b:
        raise ValueError(text)


def roots(A):
    n = len(A)
    basis = [tuple(int(i == j) for i in range(n)) for j in range(n)]
    seen = set(basis)
    todo = deque(basis)
    def reflect(v, i):
        u = list(v)
        u[i] -= sum(a*b for a, b in zip(A[i], v))
        return tuple(u)
    while todo:
        v = todo.popleft()
        for i in range(n):
            u = reflect(v, i)
            if u not in seen:
                seen.add(u)
                todo.append(u)
    R = sorted(seen)
    loc = {r:i+1 for i, r in enumerate(R)}
    generators = [[loc[reflect(r, i)] for r in R] for i in range(n)]
    return R, generators, basis


def check(A, name, desired_order, expected_size, expected_roots, O):
    R, generators, basis = roots(A)
    need(len(R) == expected_roots, 'entire root system')
    script = 'SizeScreen([1000000,1000000]);;\n'
    script += 'W:=Group(List('+json.dumps(generators)+',PermList));;\n'
    script += 'Print("SIZE|",Size(W),"\\n");\n'
    script += 'w:=();;\nfor cl in ConjugacyClasses(W) do\n w:=Representative(cl);;\n'
    script += 'if Order(w)='+str(desired_order)+' then\n'
    script += 'Print("ELEMENT|",List([1..'+str(len(R))+'],x->x^w),"|",Size(Centralizer(W,w)),"\\n");\n'
    script += 'fi;od;\nPrint("COMPLETE\\n");QUIT;\n'
    (O/(name+'.g')).write_text(script)
    cp = subprocess.run(['/opt/homebrew/bin/gap','-q','-T',str(O/(name+'.g'))],capture_output=True,timeout=60)
    (O/(name+'.stdout')).write_bytes(cp.stdout)
    (O/(name+'.stderr')).write_bytes(cp.stderr)
    need(cp.returncode == 0 and not cp.stderr, 'clean Weyl enumeration')
    text = cp.stdout.decode()
    need(text.rstrip().endswith('COMPLETE'), 'terminal Weyl enumeration')
    need('SIZE|'+str(expected_size)+'\n' in text, 'Weyl order')
    candidates = []
    X = sp.Symbol('X')
    for line in text.splitlines():
        if not line.startswith('ELEMENT|'):
            continue
        _, raw, centralizer = line.split('|')
        p = json.loads(raw)
        need(sorted(p) == list(range(1,len(R)+1)), 'literal permutation')
        columns = [R[p[R.index(b)]-1] for b in basis]
        M = sp.Matrix.hstack(*map(sp.Matrix,columns))
        need(all(tuple(M*sp.Matrix(r)) == R[p[i]-1] for i,r in enumerate(R)), 'linear action on every root')
        target = sp.cyclotomic_poly(desired_order,X)
        if name.startswith('E7'):
            target = sp.expand(target*(X+1))
        if M.charpoly(X).as_expr() == target:
            candidates.append((M, int(centralizer), p))
    need(len(candidates) == 1, 'unique required Weyl class')
    M, centralizer, p = candidates[0]
    # Frobenius is -2w in twisted E6, and 2w in untwisted F4.
    sign, d = (-1,3) if name == 'E6' else (1,1)
    q = 3 if name == 'E7order18' else 2
    if name == 'E7order18':
        d = 2
    Fminus = sign*q*M-sp.eye(len(A))
    determinant = abs(int(Fminus.det()))
    need(determinant == {'E6':57,'F4':17,'E7order14':129,'E7order18':2812}[name], 'small torus order')
    inverse = Fminus.inv()
    values = [inverse*(d*sp.Matrix(r)) for r in R]
    need(all(any(x.q != 1 for x in v) for v in values), 'no root vanishes on the simple-group torus')
    if name == 'E6':
        need(centralizer == 9, 'odd E6 torus normalizer quotient')
    if name.startswith('E7'):
        need(centralizer == desired_order, 'cyclic E7 Weyl centralizer')
        m = determinant//d
        need(next(i for i in range(1,desired_order+1) if pow(q,i,m)==1)==desired_order,
             'faithful finite torus normalizer action')
    return dict(name=name, cartan=A, roots=R, simple_reflections=generators,
                weyl_order=expected_size, element_permutation=p,
                matrix=[[int(x) for x in row] for row in M.tolist()],
                characteristic_polynomial=str(M.charpoly(X).as_expr()),
                weyl_centralizer_order=centralizer, frobenius_sign=sign,
                q=q, simple_group_index=d, adjoint_torus_order=determinant,
                root_lattice_coordinates=[[[int(x.p),int(x.q)] for x in v] for v in values])


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists(), 'fresh output required');a.out.mkdir(parents=True)
    E6 = [[2*int(i==j) for j in range(6)] for i in range(6)]
    for i,j in [(0,1),(1,2),(2,3),(3,4),(2,5)]:
        E6[i][j]=E6[j][i]=-1
    F4=[[2,-1,0,0],[-1,2,-2,0],[0,-1,2,-1],[0,0,-1,2]]
    E7 = [[2*int(i==j) for j in range(7)] for i in range(7)]
    for i,j in [(0,1),(1,2),(2,3),(3,4),(4,5),(2,6)]:
        E7[i][j]=E7[j][i]=-1
    result = [check(E6,'E6',9,51840,72,a.out),check(F4,'F4',8,1152,48,a.out),
              check(E7,'E7order14',14,2903040,126,a.out),
              check(E7,'E7order18',18,2903040,126,a.out)]
    (a.out/'report.json').write_text(json.dumps(dict(status='PASS_FINITE_ROOT_LATTICES',cases=result,whole_original_credit=0),indent=2)+'\n')
    print('PASS: E6, F4 and both E7 root equations and Weyl centralizers')


if __name__ == '__main__':
    main()
