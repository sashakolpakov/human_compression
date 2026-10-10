"""Phase250 {6,4} affine exploration; arithmetic reuses phase2 definitions."""
from collections import deque
from itertools import combinations
from pathlib import Path
import hashlib
import json
import math
import argparse

ROOT = Path(__file__).resolve().parent
I = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ZERO = (0, 0, 0)
ONE = (I, ZERO)


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3))
                       for j in range(3)) for i in range(3))


def mv(a, v):
    return tuple(sum(a[i][j] * v[j] for j in range(3)) for i in range(3))


def mul(x, y):
    return mm(x[0], y[0]), tuple(a + b for a, b in zip(mv(x[0], y[1]), x[1]))


def inverse(x):
    m = tuple(zip(*x[0]))
    return m, tuple(-a for a in mv(m, x[1]))


def power(x, n):
    y = ONE
    for _ in range(n):
        y = mul(y, x)
    return y


def word(*xs):
    y = ONE
    for x in xs:
        y = mul(y, x)
    return y


def conjugate(x, y):
    return word(inverse(y), x, y)


def determinant(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def subgroup(gens):
    result = {ONE}
    queue = deque(result)
    while queue:
        x = queue.popleft()
        for g in gens:
            y = mul(g, x)
            if y not in result:
                if len(result)>96: raise RuntimeError("PHASE250_REJECT finite parabolic bound")
                result.add(y)
                queue.append(y)
    return result


def need(ok, reason):
    if not ok: raise RuntimeError("PHASE250_REJECT "+reason)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--corrupt-translation',action='store_true');args=ap.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'fresh output')
    a=(((0,1,0),(1,0,0),(0,0,1)),ZERO)
    b=(((-1,0,0),(0,0,1),(0,1,0)),ZERO if args.corrupt_translation else (1,0,0))
    c=(((1,0,0),(0,1,0),(0,0,-1)),ZERO);gens=[a,b,c]
    comm=lambda x,y:word(inverse(x),inverse(y),x,y)
    relators=[power(x,2) for x in gens]+[power(word(a,b),6),power(word(b,c),4),power(word(a,c),2),power(comm(a,power(word(b,c),2)),2)]
    need(all(x==ONE for x in relators),'all literal universal relators')
    signed=[(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]
    permutations=[[signed.index(mv(g[0],v))+1 for v in signed] for g in gens]
    need(permutations==[[2,1,3,5,4,6],[4,3,2,1,6,5],[1,2,6,4,5,3]],'literal point quotient')
    lifts={I:ONE};words={I:''};queue=deque([I])
    while queue:
        matrix=queue.popleft()
        for label,gen in zip('abc',gens):
            y=mul(gen,lifts[matrix])
            if y[0] not in lifts:lifts[y[0]]=y;words[y[0]]=label+words[matrix];queue.append(y[0])
    need(len(lifts)==48,'point group48')
    transitions=[]
    for matrix,lift in lifts.items():
        for label,gen in zip('abc',gens):
            y=mul(gen,lift);z=mul(inverse(lifts[y[0]]),y);need(z[0]==I,'transition translation')
            transitions.append(dict(word='('+words[y[0]]+')^-1'+label+words[matrix],vector=z[1]))
    vectors=sorted(set(tuple(x['vector']) for x in transitions));index=0
    for basis in combinations(vectors,3):index=math.gcd(index,abs(determinant(*basis)))
    need(index==4,'translation lattice index4')
    need(all((v[0]-v[1])%2==0 and (v[1]-v[2])%2==0 for v in vectors),'equal parity containment')
    need(all(v in vectors for v in [(-2,0,0),(0,0,2),(-1,-1,-1),(-1,1,-1)]),'explicit full lattice generators')
    source=[
        [power(word(b,conjugate(c,word(b,a))),2),power(word(conjugate(c,b),conjugate(b,a)),2),power(word(c,conjugate(b,word(a,b))),2)],
        [power(word(conjugate(a,b),conjugate(b,word(a,c))),2),power(word(conjugate(b,word(a,c,b)),a),2),power(word(conjugate(a,word(b,c,b)),conjugate(b,word(a,b))),2)],
        [power(word(b,a,c),6),power(word(c,b,a),6),power(conjugate(word(c,b,a),b),6)]]
    need(all(w[0]==I for row in source for w in row),'source words are translations')
    bases=[[w[1] for w in row] for row in source]
    expected=[[(2,0,0),(0,-2,0),(0,0,-2)],[(2,0,2),(2,-2,0),(-2,-2,0)],[(2,-2,2),(2,-2,-2),(-2,-2,-2)]]
    need(bases==expected,'exact source vector triples')
    dets=[abs(determinant(*row)) for row in bases];need(dets==[8,16,32],'source determinants')
    contains=[lambda v:all(x%2==0 for x in v),lambda v:all(x%2==0 for x in v) and sum(v)%4==0,
        lambda v:all(x%2==0 for x in v) and (v[0]-v[1])%4==0 and (v[1]-v[2])%4==0]
    for base,test in zip(bases,contains):
        need(all(test(mv(q,v)) for q in lifts for v in base),'period invariance under every point element')
    left=subgroup([a,b]);right=subgroup([b,c]);need(len(left)==12 and len(right)==8,'adjacent orders')
    need(len({g[0] for g in left})==12 and len({g[0] for g in right})==8,'faithful linear parabolics')
    overlaps=[dict(matrix=x[0],left_translation=x[1],right_translation=y[1],difference=tuple(s-t for s,t in zip(x[1],y[1]))) for x in sorted(left) for y in sorted(right) if x[0]==y[0]]
    need(len(overlaps)==2 and all(row['difference']==ZERO for row in overlaps),'exact two-element overlap')
    need(left&right=={ONE,b},'middle involution intersection')
    # A raw-difference trap: raw transitions span only e1, whereas the
    # correct normalized transitions span e1,e2. This tests the lemma's orientation.
    neg=(((-1,0,0),(0,-1,0),(0,0,1)),ZERO)
    shift=(neg[0],(1,0,0));swap=a
    pure={I:ONE};todo=deque([I])
    while todo:
        matrix=todo.popleft()
        for gen in [neg,swap]:
            y=mul(gen,pure[matrix])
            if y[0] not in pure:pure[y[0]]=y;todo.append(y[0])
    raw=[];normalized=[]
    for lift in pure.values():
        for gen in [shift,neg,swap]:
            y=mul(gen,lift)
            raw.append(mul(y,inverse(pure[y[0]]))[1])
            normalized.append(mul(inverse(pure[y[0]]),y)[1])
    need(set(raw)=={ZERO,(1,0,0)},'raw differences only one coordinate')
    need(all(v[2]==0 for v in normalized) and any(v[1]!=0 for v in normalized),'normalized transitions recover second coordinate')
    minor_gcd=0
    for v,w in combinations(normalized,2):minor_gcd=math.gcd(minor_gcd,abs(v[0]*w[1]-v[1]*w[0]))
    need(minor_gcd==1,'normalized full planar lattice')
    print('SCHREIER_NORMALIZATION_CONTROL_PASS raw_rank1 normalized_rank2')
    out=dict(status='PASS',generators=gens,point_permutations=permutations,point_group_order=48,
        normalization_control=dict(raw_rank=1,normalized_rank=2),translation_lattice='2Z^3+Z(1,1,1)',translation_index=4,schreier_transitions=transitions,
        source_word_vectors=bases,period_determinants=dets,period_indices=[2,4,8],
        finite_order_constants=[96,192,384],adjacent_orders=[12,8],overlaps=overlaps,
        uniform_scope='Every positive m: lattice mLambda, exact order constant*m^3, same type6,4 and IP.',
        retained_step='Exact abstract point-kernel presentation is separately verified in GAP.',
        arithmetic_provenance='Elementary matrix functions reused from phase2_cubic_lattice_check.py; no old top-level code executed.')
    args.out.write_text(json.dumps(out,indent=2)+'\n')
    print('PHASE250_AFFINE_PASS point48 lattice_index4 period_indices2,4,8 overlap2')
if __name__=='__main__':main()
