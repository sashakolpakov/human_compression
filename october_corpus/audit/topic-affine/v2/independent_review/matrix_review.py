#!/usr/bin/env python3
"""Independent homogeneous-matrix check of the written affine tables and periods."""
from pathlib import Path
from collections import deque
import argparse, hashlib, json
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form

def need(ok, message):
    if not ok: raise ValueError(message)

def affine(linear, translation):
    return sp.ImmutableMatrix(sp.Matrix(linear).row_join(sp.Matrix(translation)).col_join(sp.Matrix([[0,0,0,1]])))

def conjugate(x, y): return y.inv()*x*y
def commutator(x, y): return x.inv()*y.inv()*x*y
def key(x): return tuple(x[:3,:3])
def vector(x):
    need(x[:3,:3]==sp.eye(3),'Expected a pure translation')
    return tuple(map(int,x[:3,3]))

def subgroup(generators):
    seen={sp.ImmutableMatrix(sp.eye(4))};queue=deque(seen)
    while queue:
        x=queue.popleft()
        for g in generators:
            y=g*x
            if y not in seen:
                need(len(seen)<48,'Finite adjacent subgroup bound')
                seen.add(y);queue.append(y)
    return seen

def model(second_label):
    identity=sp.ImmutableMatrix(sp.eye(4))
    a=affine([[0,1,0],[1,0,0],[0,0,1]],[0,0,0])
    b=affine([[-1,0,0],[0,0,1],[0,1,0]],[1,0,0])
    c=affine([[1,0,0],[0,1,0],[0,0,-1]] if second_label==4 else
             [[0,-1,0],[-1,0,0],[0,0,1]],[0,0,0])
    generators=[a,b,c]
    need(all(g*g==identity for g in generators),'All three involutions')
    relations=[(a*b)**6,(b*c)**second_label,(a*c)**2]
    relations.append(commutator(a,(b*c)**2)**2 if second_label==4 else (c*b*a*b)**3)
    need(all(r==identity for r in relations),'Every literal universal relator')
    representatives={key(identity):identity};queue=deque([identity])
    while queue:
        x=queue.popleft()
        for g in generators:
            y=g*x
            if key(y) not in representatives:
                representatives[key(y)]=y;queue.append(y)
    need(len(representatives)==48,'Full signed point group')
    translations=[]
    for x in representatives.values():
        for g in generators:
            y=g*x;translations.append(vector(representatives[key(y)].inv()*y))
    hnf=hermite_normal_form(sp.Matrix.hstack(*(sp.Matrix(v) for v in translations)))
    need(abs(hnf.det())==(4 if second_label==4 else 16),'Independent normalized Schreier lattice determinant')
    if second_label==4:
        expected_kernel=sp.Matrix.hstack(sp.Matrix([2,0,0]),sp.Matrix([0,2,0]),sp.Matrix([1,1,1]))
        words=[[(b*conjugate(c,b*a))**2,(conjugate(c,b)*conjugate(b,a))**2,(c*conjugate(b,a*b))**2],
               [(conjugate(a,b)*conjugate(b,a*c))**2,(conjugate(b,a*c*b)*a)**2,
                (conjugate(a,b*c*b)*conjugate(b,a*b))**2],
               [(b*a*c)**6,(c*b*a)**6,conjugate(c*b*a,b)**6]]
        expected=[[(2,0,0),(0,-2,0),(0,0,-2)],[(2,0,2),(2,-2,0),(-2,-2,0)],
                  [(2,-2,2),(2,-2,-2),(-2,-2,-2)]]
        determinants=[8,16,32]
    else:
        expected_kernel=sp.Matrix.hstack(sp.Matrix([2,2,0]),sp.Matrix([2,0,2]),sp.Matrix([0,2,2]))
        z=((b*c)**3*(a*b)**3)**2
        words=[[conjugate((a*c*b)**4,b),(c*b*a)**4,conjugate((c*b*a)**4,b)],
               [conjugate(z,a*b),conjugate(z,c),conjugate(z,c*b)],
               [conjugate(((a*b)**2*(c*b)**2)**3,a),((b*c)**2*(b*a)**2)**3,
                conjugate(((b*a)**2*(b*c)**2)**3,c)]]
        expected=[[(4,0,0),(0,-4,0),(0,0,-4)],[(4,-4,0),(4,0,-4),(-4,-4,0)],
                  [(4,-4,4),(4,-4,-4),(-4,-4,4)]]
        determinants=[64,128,256]
    need(hnf==hermite_normal_form(expected_kernel),'Exact independently computed kernel lattice')
    vectors=[[vector(w) for w in row] for row in words]
    need(vectors==expected,'All nine literal source-word values')
    lattices=[]
    for row,det in zip(vectors,determinants):
        basis=sp.Matrix.hstack(*(sp.Matrix(v) for v in row))
        need(abs(basis.det())==det,'Exact period index')
        for g in generators:
            coordinate_action=basis.inv()*g[:3,:3]*basis
            need(all(x.is_Integer for x in coordinate_action),'Period lattice invariant under each generator')
        lattices.append(basis)
    left,right=subgroup([a,b]),subgroup([b,c])
    need(len(left)==12 and len(right)==2*second_label,'Actual adjacent group orders')
    need(len({key(x) for x in left})==len(left) and len({key(x) for x in right})==len(right),'Both point maps faithful')
    need(left&right=={identity,b},'Actual adjacent intersection')
    overlaps=[]
    for x in left:
        for y in right:
            if key(x)!=key(y):continue
            diff=vector(x*y.inv());overlaps.append(diff)
            if diff!=(0,0,0):
                for basis in lattices:
                    need(any(not t.is_Integer for t in basis.inv()*sp.Matrix(diff)),'Extra intersection excluded from each period lattice')
    need(sorted(overlaps)==([(0,0,0)]*2 if second_label==4 else [(0,0,0)]*2+[(0,2,2)]*2),'Complete point-overlap table')
    return dict(second_label=second_label,point_order=48,normalized_transitions=len(translations),
        kernel_Hermite_basis=[list(map(int,hnf.row(i))) for i in range(3)],kernel_index=int(abs(hnf.det())),
        source_word_vectors=vectors,period_determinants=determinants,point_overlap_differences=sorted(overlaps),
        adjacent_orders=[len(left),len(right)],integer_invariance_checks=9)

def square():
    a=sp.Matrix([[-1,0,0],[0,1,0],[0,0,1]])
    b=sp.Matrix([[0,1,0],[1,0,0],[0,0,1]])
    c=sp.Matrix([[1,0,0],[0,-1,1],[0,0,1]])
    first=commutator((a*b)**2,c);second=commutator((a*b)**2,(b*c)**2)
    need(first==sp.Matrix([[1,0,0],[0,1,-2],[0,0,1]]) and
         second==sp.Matrix([[1,0,-2],[0,1,-2],[0,0,1]]),'Square source commutator vectors')
    return dict(first_commutator=[0,-2],second_commutator=[-2,-2])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    need(not args.out.exists(),'Fresh output required')
    result=dict(status='PASS_INDEPENDENT_AFFINE_MATRIX_REVIEW',sympy_version=sp.__version__,
        checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        cubic_models=[model(4),model(6)],square_source_vectors=square(),
        author_programs_imported=False,source_word_values_checked=18,
        limits=['Coordinates and lattice identities only; abstract universal-group kernels require the separately reviewed GAP rewriting.',
                'Finite point/parabolic enumeration is an exact uniform proof input, not sampling of arbitrary periods.',
                'Not a separate Lean or polytope-classification proof.'])
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],source_word_values_checked=18)))

if __name__=='__main__':main()
