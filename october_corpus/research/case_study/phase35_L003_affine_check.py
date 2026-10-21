#!/usr/bin/env python3
"""Standalone six-dimensional integral affine certificate; no input tables."""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path

MATRICES = [
    [[-1,-1,0,0,0,1],[0,1,0,0,0,0],[0,0,0,1,1,1],
     [0,0,0,1,0,0],[0,0,1,-1,0,-1],[0,0,0,0,0,1]],
    [[0,0,0,1,0,0],[0,-1,0,0,0,0],[0,-1,1,0,0,0],
     [1,0,0,0,0,0],[0,0,0,0,0,-1],[0,0,0,0,-1,0]],
    [[1,0,0,0,0,0],[-1,-1,0,1,0,0],[0,0,-1,1,-1,1],
     [0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]],
    [[1,1,0,0,0,-1],[0,-1,0,0,0,0],[0,0,0,-1,-1,-1],
     [0,0,-1,0,-1,0],[0,0,0,0,1,1],[0,0,0,0,0,-1]],
]
OFFSETS = [(0,0,0,0,0,0), (0,0,0,0,0,0),
           (0,0,-1,0,0,0), (0,0,0,0,0,0)]
BASIS_EDGES = [(143,0),(152,3),(162,2),(172,1),(223,2),(244,0)]
IDENTITY_MATRIX = tuple(int(i == j) for i in range(6) for j in range(6))
IDENTITY = (IDENTITY_MATRIX, (0,)*6)


def mm(A, B):
    return tuple(sum(A[6*i+k]*B[6*k+j] for k in range(6))
                 for i in range(6) for j in range(6))


def mv(A, v):
    return tuple(sum(A[6*i+j]*v[j] for j in range(6)) for i in range(6))


def mul(a, b):
    A, u = a
    B, v = b
    return mm(A, B), tuple(x+y for x, y in zip(u, mv(A, v)))


def prod(*args):
    out = IDENTITY
    for a in args:
        out = mul(out, a)
    return out


def power(a, n):
    assert n >= 0
    out = IDENTITY
    while n:
        if n & 1:
            out = mul(out, a)
        a = mul(a, a)
        n //= 2
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite saved evidence')
    marks = [(tuple(a for row in A for a in row), b)
             for A, b in zip(MATRICES, OFFSETS)]
    assert all(mul(a, a) == IDENTITY for a in marks)
    x, y, z = [mul(marks[0], a) for a in marks[1:]]
    xi, yi = mul(marks[1], marks[0]), mul(marks[2], marks[0])
    relators = [
        power(x,6), power(y,3), power(z,2), power(prod(z,x),3),
        power(prod(z,y),6), power(prod(xi,y),2),
        power(prod(yi,power(xi,2)),3), power(prod(z,power(x,3)),2),
        prod(xi,z,power(prod(yi,z),2),z,x,power(prod(z,y),2)),
    ]
    assert all(a == IDENTITY for a in relators)

    # Linear quotient plus actual affine word representatives.
    reps = [IDENTITY]
    words = [()]
    index = {IDENTITY_MATRIX: 0}
    todo = deque([0])
    right = []
    while todo:
        a = todo.popleft()
        assert a == len(right)
        row = []
        for j, mark in enumerate(marks):
            b = mul(reps[a], mark)
            if b[0] not in index:
                index[b[0]] = len(reps)
                reps.append(b)
                words.append(words[a]+(j,))
                todo.append(index[b[0]])
            row.append(index[b[0]])
        right.append(row)
        assert len(reps) <= 1296
    assert len(reps) == 1296
    assert len({tuple(a % 2 for a in A) for A, u in reps}) == 1296
    translations = {}
    for a in range(1296):
        for j, mark in enumerate(marks):
            b = mul(reps[a], mark)
            target = reps[right[a][j]]
            assert b[0] == target[0]
            v = tuple(x-y for x, y in zip(b[1], target[1]))
            assert all(t % 2 == 0 for t in v)
            translations[a,j] = v
    for i, edge in enumerate(BASIS_EDGES):
        assert translations[edge] == tuple(2*int(i == j) for j in range(6))
    literal_basis_words = []
    for i, (a,j) in enumerate(BASIS_EDGES):
        word = words[a]+(j,)+words[right[a][j]][::-1]
        value = prod(*(marks[k] for k in word))
        assert value == (IDENTITY_MATRIX, tuple(2*int(i == j) for j in range(6)))
        literal_basis_words.append(list(word))

    # Local infinite lattice and three exact finite parabolics.
    T = prod(y,power(prod(z,y),2))
    A = power(T,2)
    u, ui = prod(yi,z), prod(z,y)
    B = prod(ui,A,u)
    assert A[0] == B[0] == IDENTITY_MATRIX
    assert T[0] != IDENTITY_MATRIX and mm(T[0],T[0]) == IDENTITY_MATRIX
    assert all(a % 2 == 0 for a in A[1]+B[1])
    a, b = tuple(t//2 for t in A[1]), tuple(t//2 for t in B[1])
    ij = next((i,j) for i in range(6) for j in range(i+1,6)
              if abs(a[i]*b[j]-a[j]*b[i]) == 1)
    assert any(abs(t) == 1 for t in a)
    local_minor = [[a[i],b[i]] for i in ij]
    fixed = {}
    for mask, expected in [(14,36),(11,48),(7,108)]:
        seen = {IDENTITY_MATRIX: IDENTITY}
        todo = deque([IDENTITY])
        while todo:
            v = todo.popleft()
            for j in range(4):
                if not mask & (1 << j):
                    continue
                w = mul(v, marks[j])
                if w[0] in seen:
                    assert w == seen[w[0]]
                else:
                    seen[w[0]] = w
                    todo.append(w)
            assert len(seen) <= expected
        assert len(seen) == expected
        fixed[str(mask)] = len(seen)

    # The base modulo 2 has exactly this linear quotient's Cayley graph:
    # every Schreier translation is even and the linear quotient is faithful.
    left = [[index[mm(mark[0], A)] for mark in marks] for A, u in reps]
    assert all(left[right[a][j]][i] == right[left[a][i]][j]
               for a in range(1296) for i in range(4) for j in range(4))
    def cosets(mask):
        unseen = set(range(1296))
        rows = []
        while unseen:
            a = min(unseen)
            todo = [a]
            unseen.remove(a)
            bits = 0
            while todo:
                b = todo.pop()
                bits |= 1 << b
                for j in range(4):
                    if mask & (1 << j):
                        c = left[b][j]
                        if c in unseen:
                            unseen.remove(c)
                            todo.append(c)
            rows.append(bits)
        return rows
    all_cosets = [cosets(mask) for mask in range(16)]
    subgroups = [row[0] for row in all_cosets]
    assert all(subgroups[a]&subgroups[b] == subgroups[a&b]
               for a in range(16) for b in range(16))
    pars = [all_cosets[15^(1<<i)] for i in range(4)]
    assert [len(row) for row in pars] == [36,27,27,12]
    flags = Counter()
    chambers = []
    def visit(next_type, selected, common, mask):
        assert common
        flags[mask] += 1
        if mask == 15:
            assert common.bit_count() == 1
            chambers.append(common)
        for i in range(next_type,4):
            for coset in pars[i]:
                if all(coset&old for old in selected):
                    visit(i+1,selected+[coset],common&coset,mask|(1<<i))
    visit(0,[],(1<<1296)-1,0)
    assert len(chambers) == len(set(chambers)) == 1296

    report = {
        'status':'PASS',
        'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'external_mathematical_data_files':[],
        'linear_matrices':MATRICES,
        'affine_offsets':OFFSETS,
        'integer_source_relators':9,
        'linear_group_order':1296,
        'distinct_linear_images_mod2':1296,
        'schreier_vectors_all_even':5184,
        'schreier_coordinate_parity_checks':5184*6,
        'basis_edges_zero_based':BASIS_EDGES,
        'literal_words_for_translations_2e_i':literal_basis_words,
        'kernel_lattice':'2Z^6',
        'parameter_word':'T=y(zy)^2',
        'local_translation_vectors_divided_by2':[a,b],
        'local_minor_coordinates_zero_based':ij,
        'local_minor':local_minor,
        'fixed_integer_parabolic_orders':fixed,
        'base_subgroup_orders':[v.bit_count() for v in subgroups],
        'base_marked_meets':256,
        'base_pairwise_incident_flags':sum(flags.values()),
        'base_flags_by_type_mask':dict(sorted(flags.items())),
        'base_singleton_common_point_chambers':1296,
        'finite_modulus':'2m',
        'full_group_order':'1296*m^6',
        'scope':'Standalone exact integral affine marking. Written lattice/reduction and local toroidal-order/quotient arguments establish the all-even family. No universal-group order or split-extension claim.'
    }
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PHASE35_L003_AFFINE_PASS',sum(flags.values()),
          'base flags; 5184 Schreier vectors; kernel2Z6')


if __name__ == '__main__':
    main()
