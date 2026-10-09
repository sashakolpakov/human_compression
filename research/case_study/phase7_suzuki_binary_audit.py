"""Independent exhaustive binary matrix check of the Suzuki torus sign input.

Enumerates all 2^16 binary matrices directly. No group library or Suzuki
arithmetic module is imported. This checks a finite seed, not the universal
Lang descent, character-lattice calculation, or all-rank geometry theorem.
"""
from itertools import product
from pathlib import Path
from hashlib import sha256
import json


def reverse4(x):
    return sum(((x >> i) & 1) << (3-i) for i in range(4))


def form(x, y):
    return (x & reverse4(y)).bit_count() % 2


def mm(g, h):
    rows = []
    for row in g:
        out = 0
        for j in range(4):
            if (row >> j) & 1:
                out ^= h[j]
        rows.append(out)
    return tuple(rows)


def rho(g):
    pairs = [(0, 1), (0, 2), (1, 3), (2, 3)]
    rows = []
    for i, j in pairs:
        row = 0
        for c, (k, l) in enumerate(pairs):
            value = (((g[i] >> k) & 1) & ((g[j] >> l) & 1)) ^ \
                    (((g[i] >> l) & 1) & ((g[j] >> k) & 1))
            row |= value << c
        rows.append(row)
    return tuple(rows)


def encode(rows):
    return tuple(sum(x << j for j, x in enumerate(row)) for row in rows)


def main():
    I = (1, 2, 4, 8)
    M = encode([[1,1,1,0], [0,0,1,1], [0,1,1,1], [1,0,0,0]])
    r = encode([[1,0,0,0], [1,1,0,0], [1,1,1,0], [1,0,1,1]])
    w = (8, 4, 2, 1)
    # Alternating diagonal entries vanish automatically in characteristic two.
    H = {g for g in product(range(16), repeat=4)
         if all(form(g[i], g[j]) == int(i+j == 3)
                for i in range(4) for j in range(i+1, 4))}
    assert len(H) == 720
    assert all(rho(g) in H and rho(rho(g)) == g for g in H)
    fixed = {g for g in H if rho(g) == g}
    assert len(fixed) == 20
    generated = {I}
    queue = [I]
    while queue:
        g = queue.pop()
        for s in [r, w]:
            h = mm(g, s)
            if h not in generated:
                generated.add(h)
                queue.append(h)
    assert generated == fixed
    centralizer = {g for g in H if mm(g, M) == mm(M, g)}
    fixed_centralizer = fixed & centralizer
    assert len(centralizer) == 5 and fixed_centralizer == {I}
    # Independently check the given normalizer relation and exact order four.
    r2 = mm(r, r)
    assert r2 != I and mm(r2, r2) == I
    rinv = mm(r2, r)
    assert mm(mm(rinv, M), r) == mm(M, M)
    source = Path(__file__)
    result = {
        'status': 'PASS',
        'scope': 'Exhaustive binary matrix seed only; no universal geometry or Lang theorem inferred.',
        'all_binary_matrices_considered': 65536,
        'symplectic_matrices': len(H),
        'rho_square_checks': len(H),
        'rho_fixed_matrices': len(fixed),
        'rho_fixed_group_generated_by_r_w': True,
        'binary_symplectic_centralizer_of_M': len(centralizer),
        'rho_fixed_centralizer_of_M': len(fixed_centralizer),
        'order_four_normalizer_relation': True,
        'matrix_encoding': 'Four row integers; bit j is column j, zero-based.',
        'M_rows': M, 'r_rows': r, 'w_rows': w,
        'source_sha256': sha256(source.read_bytes()).hexdigest(),
    }
    source.with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print('PASS: 65536 binary matrices; 720 symplectic; 20 rho-fixed; fixed centralizer = 1.')


if __name__ == '__main__':
    main()
