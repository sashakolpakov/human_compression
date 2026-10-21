#!/usr/bin/env python3
"""Exact finite diagnostics for the central-join theorem, using only Python.

The seed is an explicitly enumerated affine torus group, not a group catalogue.
The proof remains the uniform evidence; these finite checks do not replace it.
Run: python3 phase16_central_join_check.py --output REPORT.json
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def closure(generators, mul):
    seen = {0}
    queue = [0]
    for x in queue:
        for g in generators:
            y = mul(x, g)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return seen


def marked_characters(size, generators, mul):
    chars = {0: 0}
    queue = [0]
    for x in queue:
        for i, g in enumerate(generators):
            y = mul(x, g)
            value = chars[x] ^ (1 << i)
            if y in chars:
                assert chars[y] == value
            else:
                chars[y] = value
                queue.append(y)
    assert len(chars) == size
    return [chars[i] for i in range(size)]


def torus_seed():
    # Z^2/<(2,2),(-2,2)> is (Z/4)^2/<(2,2)>, of order eight.
    def red(v):
        x, y = v[0] % 4, v[1] % 4
        return min((x, y), ((x + 2) % 4, (y + 2) % 4))

    points = sorted({red(v) for v in itertools.product(range(4), repeat=2)})
    identity = (1, 0, 0, 1)
    matrices = []
    for s, t in itertools.product((-1, 1), repeat=2):
        matrices.extend(((s, 0, 0, t), (0, s, t, 0)))
    matrices = [identity] + sorted(set(matrices) - {identity})

    def act(m, v):
        a, b, c, d = m
        return (a * v[0] + b * v[1], c * v[0] + d * v[1])

    def mm(m, n):
        a, b, c, d = m
        e, f, g, h = n
        return (a * e + b * g, a * f + b * h,
                c * e + d * g, c * f + d * h)

    elements = [((0, 0), identity)]
    elements += [x for x in itertools.product(points, matrices) if x != elements[0]]
    index = {x: i for i, x in enumerate(elements)}
    table = []
    for v, m in elements:
        row = []
        for w, n in elements:
            mw = act(m, w)
            row.append(index[(red((v[0] + mw[0], v[1] + mw[1])), mm(m, n))])
        table.append(row)
    a = index[((1, 0), (-1, 0, 0, 1))]
    b = index[((0, 0), (0, 1, 1, 0))]
    c = index[((0, 0), (1, 0, 0, -1))]
    mul = lambda x, y: table[x][y]
    assert len(elements) == 64
    for x, y, z in itertools.product(range(64), repeat=3):
        assert mul(mul(x, y), z) == mul(x, mul(y, z))
    inv = [next(y for y in range(64) if mul(x, y) == 0 and mul(y, x) == 0)
           for x in range(64)]
    generators = (a, b, c)
    for g in generators:
        assert mul(g, g) == 0
    chars = marked_characters(64, generators, mul)
    for x, y in itertools.product(range(64), repeat=2):
        assert chars[mul(x, y)] == chars[x] ^ chars[y]
    return table, inv, generators, chars


class Join:
    def __init__(self, d, blocks, seed):
        self.d = d
        self.blocks = blocks
        self.table, self.seed_inverse, self.seed_generators, self.seed_chars = seed
        self.inside = {v for block in blocks for v in block}
        self.outside = [v for v in range(d) if v not in self.inside]
        self.edges = [(v, v + 1) for v in range(d - 1)
                      if not {v, v + 1} <= self.inside]
        self.hbits = 6 * len(blocks)
        self.bbits = self.hbits + len(self.outside)
        self.hmask = (1 << self.hbits) - 1
        self.bmask = (1 << self.bbits) - 1
        self.size = 1 << (self.bbits + len(self.edges))
        self.chars = []
        for base in range(1 << self.bbits):
            chars = 0
            for i, block in enumerate(blocks):
                local = self.seed_chars[(base >> (6 * i)) & 63]
                for j, v in enumerate(block):
                    if (local >> j) & 1:
                        chars |= 1 << v
            for i, v in enumerate(self.outside):
                if (base >> (self.hbits + i)) & 1:
                    chars |= 1 << v
            self.chars.append(chars)
        self.beta = [[sum((((a >> v) & 1) * ((b >> u) & 1)) << j
                          for j, (u, v) in enumerate(self.edges))
                      for b in range(1 << d)] for a in range(1 << d)]
        self.generators = [0] * d
        for i, block in enumerate(blocks):
            for j, v in enumerate(block):
                self.generators[v] = self.seed_generators[j] << (6 * i)
        for i, v in enumerate(self.outside):
            self.generators[v] = 1 << (self.hbits + i)

    def mul(self, x, y):
        base_x, base_y = x & self.bmask, y & self.bmask
        h = 0
        for i in range(len(self.blocks)):
            h |= self.table[(x >> (6 * i)) & 63][(y >> (6 * i)) & 63] << (6 * i)
        outside = (base_x ^ base_y) & (self.bmask ^ self.hmask)
        central = ((x >> self.bbits) ^ (y >> self.bbits)
                   ^ self.beta[self.chars[base_x]][self.chars[base_y]])
        return h | outside | (central << self.bbits)

    def inv(self, x):
        base = x & self.bmask
        h = 0
        for i in range(len(self.blocks)):
            h |= self.seed_inverse[(x >> (6 * i)) & 63] << (6 * i)
        outside = base & (self.bmask ^ self.hmask)
        central = (x >> self.bbits) ^ self.beta[self.chars[base]][self.chars[base]]
        return h | outside | (central << self.bbits)

    def comm(self, x, y):
        return self.mul(self.mul(self.inv(x), self.inv(y)), self.mul(x, y))

    def normal_closure(self, seeds):
        generators = list(set(seeds) - {0})
        subgroup = closure(generators, self.mul)
        changed = True
        while changed:
            changed = False
            for x in list(generators):
                for r in self.generators:
                    y = self.mul(self.mul(r, x), r)
                    if y not in subgroup:
                        generators.append(y)
                        subgroup = closure(generators, self.mul)
                        changed = True
        return subgroup, generators

    def check(self):
        d = self.d
        for x in range(self.size):
            assert self.mul(x, self.inv(x)) == self.mul(self.inv(x), x) == 0
        # Exhaust every vertex-character cocycle identity, including characters
        # of the nonabelian H base. This implies associativity via its group law.
        for a, b, c in itertools.product(range(1 << d), repeat=3):
            assert (self.beta[a][b] ^ self.beta[a ^ b][c]
                    == self.beta[b][c] ^ self.beta[a][b ^ c])
        local_subgroups = [closure([self.seed_generators[j] for j in range(3)
                                    if (mask >> j) & 1],
                                   lambda x, y: self.table[x][y])
                           for mask in range(8)]
        parabolics, encoded = [], []
        for mask in range(1 << d):
            got = closure([g for v, g in enumerate(self.generators) if (mask >> v) & 1], self.mul)
            allowed_h = []
            for block in self.blocks:
                local_mask = sum(((mask >> v) & 1) << j for j, v in enumerate(block))
                allowed_h.append(local_subgroups[local_mask])
            allowed_o = [i for i, v in enumerate(self.outside) if (mask >> v) & 1]
            allowed_z = [i for i, (u, v) in enumerate(self.edges)
                         if (mask >> u) & 1 and (mask >> v) & 1]
            expected = set()
            for hs in itertools.product(*allowed_h):
                h = sum(x << (6 * i) for i, x in enumerate(hs))
                for omask in range(1 << len(allowed_o)):
                    o = sum(((omask >> j) & 1) << (self.hbits + i)
                            for j, i in enumerate(allowed_o))
                    for zmask in range(1 << len(allowed_z)):
                        z = sum(((zmask >> j) & 1) << (self.bbits + i)
                                for j, i in enumerate(allowed_z))
                        expected.add(h | o | z)
            assert got == expected
            parabolics.append(got)
            encoded.append(sum(1 << x for x in got))
        assert len(parabolics[-1]) == self.size
        for a, b in itertools.product(range(1 << d), repeat=2):
            assert encoded[a] & encoded[b] == encoded[a & b]
        derived, derived_generators = self.normal_closure(
            [self.comm(a, b) for a in self.generators for b in self.generators])
        gamma3, gamma3_generators = self.normal_closure(
            [self.comm(a, b) for a in derived_generators for b in self.generators])
        gamma4, _ = self.normal_closure(
            [self.comm(a, b) for a in gamma3_generators for b in self.generators])
        assert len(gamma3) == 1 << len(self.blocks)
        assert gamma4 == {0}
        support_mask = (1 << d) - 1
        for mask, subgroup in enumerate(parabolics):
            if gamma3 <= subgroup:
                support_mask &= mask
        assert {v for v in range(d) if (support_mask >> v) & 1} == self.inside
        assert all((x >> self.hbits) == 0 for x in gamma3)
        core_mask = support_mask | ((support_mask << 1) & ((1 << d) - 1)) | (support_mask >> 1)
        core_size = len(parabolics[core_mask])
        triple_orders = [len(parabolics[7 << i]) for i in range(d - 2)]
        assert triple_orders == [64 if tuple(range(i, i + 3)) in self.blocks else 32
                                 for i in range(d - 2)]
        edge_orders = []
        for i in range(d - 1):
            x = self.mul(self.generators[i], self.generators[i + 1])
            cur, order = 0, 0
            while True:
                cur, order = self.mul(cur, x), order + 1
                if cur == 0:
                    break
            assert order == 4
            edge_orders.append(order)
        return {
            "rank": d, "seed_blocks_one_based": [[v + 1 for v in block] for block in self.blocks],
            "order": self.size, "excess": len(self.blocks),
            "derived_order": len(derived), "gamma3_order": len(gamma3),
            "gamma4_order": len(gamma4), "edge_orders": edge_orders,
            "kernel_support_one_based": [v + 1 for v in range(d) if (support_mask >> v) & 1],
            "canonical_core_vertices_one_based": [v + 1 for v in range(d) if (core_mask >> v) & 1],
            "canonical_core_order": core_size, "triple_orders": triple_orders,
            "parabolic_closures": len(parabolics), "exact_ip_meets": 1 << (2 * d),
            "vertex_cocycle_triples": 1 << (3 * d), "inverse_checks": self.size,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    seed = torus_seed()
    cases = [(4, []), (4, [(0, 1, 2)]), (6, [(1, 2, 3)]),
             (7, [(0, 1, 2), (4, 5, 6)])]
    results = [Join(d, blocks, seed).check() for d, blocks in cases]
    report = {
        "status": "PASS", "scope": "Finite diagnostics, not a uniform proof or a group census",
        "implementation": "Python standard library; exact affine seed and character cocycle",
        "script_sha256": digest(__file__),
        "proof_sha256": digest(Path(__file__).with_name("phase16_central_join.md")),
        "seed_order": 64, "seed_associativity_triples": 64 ** 3,
        "seed_character_products": 64 ** 2, "cases": results,
        "total_exact_ip_meets": sum(x["exact_ip_meets"] for x in results),
        "total_parabolic_closures": sum(x["parabolic_closures"] for x in results),
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
