#!/usr/bin/env python3
"""Exact bounded parity-fiber checks; independent of other local files, no universal claim."""
import argparse
import hashlib
import json
import time
from pathlib import Path


def require(test, label):
    if not test:
        raise ValueError(label)


def components(mask, d):
    out = []
    for i in range(d):
        if mask >> i & 1:
            if i == 0 or not (mask >> (i - 1) & 1):
                out.append([])
            out[-1].append(i)
    return out


def two_factor(d, exponent):
    if exponent == 2:
        return 0, lambda a, b: a ^ b, [1 << i for i in range(d)]
    pairs = [(i, j) for i in range(d + 1) for j in range(i + 1, d + 1)]
    pos = {p: k for k, p in enumerate(pairs)}

    def mul(a, b):
        c = a ^ b
        for i, j in pairs:
            cross = sum((a >> pos[i, k] & 1) * (b >> pos[k, j] & 1)
                        for k in range(i + 1, j)) & 1
            c ^= cross << pos[i, j]
        return c
    return 0, mul, [1 << pos[i, i + 1] for i in range(d)]


def symmetric(d):
    one = tuple(range(d + 1))
    marks = []
    for i in range(d):
        a = list(one)
        a[i], a[i + 1] = a[i + 1], a[i]
        marks.append(tuple(a))
    return one, lambda a, b: tuple(a[b[i]] for i in range(d + 1)), marks


def orthogonal_four():
    # F4=F2[t]/(t^2+t+1), four-dimensional full ambient quadratic space.
    d = 4

    def product(a, b):
        c = 0
        while b:
            if b & 1:
                c ^= a
            a <<= 1
            if a & 4:
                a ^= 7
            b >>= 1
        return c
    tab = [[product(a, b) for b in range(4)] for a in range(4)]

    def mul(a, b):
        c = [0] * 16
        for i in range(d):
            for k in range(d):
                for j in range(d):
                    c[i*d+j] ^= tab[a[i*d+k]][b[k*d+j]]
        return tuple(c)
    one = tuple(int(i == j) for i in range(d) for j in range(d))
    marks = []
    for i in range(3):
        r = list(one)
        for j in [i - 1, i + 1]:
            if 0 <= j < d:
                r[i*d+j] ^= 2
        marks.append(tuple(r))

    def dickson(a):
        rows = [[a[i*d+j] ^ int(i == j) for j in range(d)] for i in range(d)]
        rank = 0
        for col in range(d):
            piv = next((i for i in range(rank, d) if rows[i][col]), None)
            if piv is None:
                continue
            rows[rank], rows[piv] = rows[piv], rows[rank]
            inv = next(x for x in range(1, 4) if tab[x][rows[rank][col]] == 1)
            rows[rank] = [tab[inv][x] for x in rows[rank]]
            for i in range(d):
                if i != rank:
                    c = rows[i][col]
                    rows[i] = [x ^ tab[c][y] for x, y in zip(rows[i], rows[rank])]
            rank += 1
        return rank & 1
    return one, mul, marks, dickson


class Factor:
    def __init__(self, one, mul, marks, dickson=None):
        self.one, self.mul, self.marks = one, mul, marks
        self.elements = [one]
        self.index = {one: 0}
        self.parity = [0]
        self.edges = []
        for x in self.elements:
            row = []
            ix = self.index[x]
            for r in marks:
                y = mul(x, r)
                if y not in self.index:
                    self.index[y] = len(self.elements)
                    self.elements.append(y)
                    self.parity.append(self.parity[ix] ^ 1)
                iy = self.index[y]
                require(self.parity[iy] == self.parity[ix] ^ 1, 'factor parity consistency')
                row.append(iy)
            self.edges.append(row)
        if dickson:
            require(all(dickson(x) == self.parity[i] for i, x in enumerate(self.elements)),
                    'whole ambient Dickson parity')

    def support(self, mask):
        cs = components(mask, len(self.marks))
        bits = {i: 1 << j for j, c in enumerate(cs) for i in c}
        tags, queue = {0: 0}, [0]
        for x in queue:
            for i, bit in bits.items():
                y, tag = self.edges[x][i], tags[x] ^ bit
                if y not in tags:
                    tags[y] = tag
                    queue.append(y)
                require(tags[y] == tag, 'component parity consistency')
        return tags


def model(d, n, e):
    E = Factor(*two_factor(d, e))
    G = Factor(*symmetric(d)) if n == 3 else Factor(*orthogonal_four())
    ES, GS, HS = [], [], []
    for mask in range(1 << d):
        et, gt = E.support(mask), G.support(mask)
        seen, todo = {(0, 0)}, [(0, 0)]
        for x, y in todo:
            for i in range(d):
                if mask >> i & 1:
                    v = (E.edges[x][i], G.edges[y][i])
                    if v not in seen:
                        seen.add(v)
                        todo.append(v)
        fiber = {(x, y) for x in et for y in gt if et[x] == gt[y]}
        require(seen == fiber, 'exact all-parabolic parity fiber')
        require(len(seen) * 2 ** len(components(mask, d)) == len(et) * len(gt),
                'parabolic order formula')
        ES.append(set(et)); GS.append(set(gt)); HS.append(seen)
    pairs = 0
    for j in range(1 << d):
        for k in range(j, 1 << d):
            require(ES[j] & ES[k] == ES[j & k], 'E IP')
            require(GS[j] & GS[k] == GS[j & k], 'G IP')
            require(HS[j] & HS[k] == HS[j & k], 'mix full IP')
            pairs += 1
    def word(w):
        x, y = 0, 0
        for i in w:
            x, y = E.edges[x][i], G.edges[y][i]
        return x, y
    label = e * n
    for i in range(d):
        require(word([i]) != (0, 0) and word([i, i]) == (0, 0), 'involution')
        for j in range(i + 1, d):
            order = label if j == i + 1 else 2
            require(word([i, j] * order) == (0, 0), 'pair power')
            require(all(word([i, j] * k) != (0, 0) for k in range(1, order)), 'exact pair order')
    count = 0
    for i in range(d - 2):
        for k in range(1, label):
            w = [i + 1, i + 2] * k + [i, i + 1] * k
            require(word(w + w) == (0, 0), 'Li-Zhang power relation')
            count += 1
    return dict(rank=d, odd_label=n, two_label=e, resulting_label=label,
                E_order=len(E.elements), G_order=len(G.elements), H_order=len(HS[-1]),
                parabolics=1 << d, unordered_subset_pairs=pairs,
                exact_component_fibers=True, all_three_IP_checks=True,
                power_relators=count, dickson_all_G_elements=(n == 5))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    require(not a.report.exists(), 'Refusing to overwrite report')
    t = time.monotonic()
    rows = [model(d, n, e) for d, n in [(3, 3), (4, 3), (3, 5)] for e in [2, 4]]
    out = dict(status='PASS', scope='six exact finite examples; no substitute for the written all-rank theorem',
               results=rows, total_subset_pairs=sum(r['unordered_subset_pairs'] for r in rows),
               total_power_relators=sum(r['power_relators'] for r in rows),
               script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               seconds=time.monotonic()-t)
    with a.report.open('x') as f:
        json.dump(out, f, indent=2); f.write('\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
