"""Exact binary-coordinate verification of the eight L035 extension models.

This verifies constructions, not completeness of a classification. All arithmetic
is integer/xor arithmetic; GAP's separate census supplies the finite base audit.
"""
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def model(s, m, beta=0, nu=0):
    dim = s - 2
    half = m // 2
    bit = 1 << dim
    ds = list(range(2 * bit))

    def dm(x, y):
        extra = 0
        if dim == 3:
            extra = beta * (((x >> 1) & 1) * (y & 1)
                            + ((x >> 2) & 1) * ((y >> 1) & 1)) % 2
        return x ^ y ^ (extra * bit)

    assert all(dm(dm(x, y), z) == dm(x, dm(y, z))
               for x, y, z in product(ds, repeat=3))

    if dim == 1:
        tgens = [1 ^ (nu * bit)]
    elif dim == 2:
        tgens = [2, 1 ^ (nu * bit)]
    else:
        tgens = [2, 4, 7 ^ (nu * bit)]

    def extend(images, x):
        y = x & bit
        for i in range(dim):
            if x & (1 << i):
                y = dm(y, images[i])
        return y

    tp = [list(ds)]
    for _ in range(4):
        tp.append([extend(tgens, x) for x in tp[-1]])
    assert tp[4] == ds
    assert len(set(tp[1])) == len(ds)
    assert all(tp[1][dm(x, y)] == dm(tp[1][x], tp[1][y])
               for x, y in product(ds, repeat=2))

    # Normal form D(v) r^k with the z bit absorbed into r^(m/2).
    ns = list(product(range(bit), range(m)))
    one = (0, 0)
    rot = (0, 1)
    lamp = (1, 0)

    def nm(x, y):
        v, k = x
        w, l = y
        d = dm(v, tp[(-k) % 4][w])
        return d % bit, (k + l + (d // bit) * half) % m

    def npow(x, k):
        out = one
        while k:
            if k & 1:
                out = nm(out, x)
            x = nm(x, x)
            k //= 2
        return out

    # Build A and C from their specified images on D and r.
    agens = [1 << i for i in range(dim)]
    if dim == 3:
        agens[2] ^= beta * bit
    cgens = [tp[(1 - i) % 4][1] for i in range(dim)]

    def action(images, rimage):
        powers = [one]
        for _ in range(m):
            powers.append(nm(powers[-1], rimage))
        assert powers[-1] == one
        out = {}
        for v, k in ns:
            d = extend(images, v)
            image = (d % bit, (d // bit) * half)
            out[v, k] = nm(image, powers[k])
        return out

    aa = action(agens, nm(lamp, rot))
    cc = action(cgens, (0, m - 1))
    ident = {x: x for x in ns}
    ac = {x: aa[cc[x]] for x in ns}
    assert all(aa[aa[x]] == cc[cc[x]] == x and aa[cc[x]] == cc[aa[x]] for x in ns)
    # Full pair checks, not random sampling, for both automorphisms.
    for f in (aa, cc):
        assert len(set(f.values())) == len(ns)
        assert all(f[nm(x, y)] == nm(f[x], f[y]) for x, y in product(ns, repeat=2))
    acts = [ident, aa, cc, ac]

    def gm(x, y):
        n, h = x
        q, j = y
        return nm(n, acts[h][q]), h ^ j

    unit = (one, 0)
    a, c, r = (one, 1), (one, 2), (rot, 0)
    b = gm(r, c)

    def power(x, k):
        out = unit
        while k:
            if k & 1:
                out = gm(out, x)
            x = gm(x, x)
            k //= 2
        return out

    def inv(x):
        return power(x, 4 * len(ns) - 1)

    def comm(x, y):
        return gm(gm(gm(inv(x), inv(y)), x), y)

    def closure(gens):
        seen = {unit}
        queue = [unit]
        for x in queue:
            for y in gens:
                xy = gm(x, y)
                if xy not in seen:
                    seen.add(xy)
                    queue.append(xy)
        return seen

    full = closure([a, b, c])
    left, right = closure([a, b]), closure([b, c])
    assert len(full) == 4 * len(ns) == (2 ** s) * m
    assert len(left) == 8 and len(right) == 2 * m
    assert left & right == {unit, b}
    assert all(gm(x, x) == unit for x in (a, b, c))
    assert gm(a, c) == gm(c, a)
    assert power(r, m) == unit and power(r, half) != unit
    d = power(gm(a, b), 2)
    z = power(r, half)
    assert d != unit and gm(d, d) == unit
    if s == 3:
        assert comm(d, c) == power(z, nu)
    elif s == 4:
        assert comm(d, power(r, 2)) == power(z, nu)
    else:
        assert power(comm(a, power(r, 2)), 2) == power(z, beta)
        assert comm(a, power(r, 4)) == power(z, nu)
    return dict(s=s, m=m, beta=beta, nu=nu, order=len(full),
                small_D_order=len(ds), automorphism_pairs_checked=2 * len(ns)**2,
                pair_orders=[4, m, 2], parabolic_intersection=2, status="PASS")


if __name__ == "__main__":
    rows = [model(3, 128, nu=e) for e in (0, 1)]
    rows += [model(4, 64, nu=e) for e in (0, 1)]
    rows += [model(5, 32, beta=b, nu=v) for b, v in product((0, 1), repeat=2)]
    record = dict(check="eight binary extension models at n=10", arithmetic="exact",
                  scope="Construction verification; classification completeness is separate",
                  results=rows, status="PASS")
    (ROOT / "phase3_extension_check.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))
