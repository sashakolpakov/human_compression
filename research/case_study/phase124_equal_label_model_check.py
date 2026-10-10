#!/usr/bin/env python3
"""Exact small models; checks stay active under python -O. No universal-presentation claim."""
import json, time, hashlib, argparse, math
from pathlib import Path

def subgroup(gens, one, mul):
    seen = {one}
    todo = [one]
    for a in todo:
        for g in gens:
            v = mul(a, g)
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return seen

def test(d, n):
    if n == 4:
        pairs = [(i, j) for i in range(d + 1) for j in range(i + 1, d + 1)]
        pos = {v: k for k, v in enumerate(pairs)}
        one = 0

        def mul(a, b):
            c = a ^ b
            for i, j in pairs:
                v = sum(((a >> pos[i, k] & 1) * (b >> pos[k, j] & 1) for k in range(i + 1, j))) & 1
                c ^= v << pos[i, j]
            return c
        marks = [1 << pos[i, i + 1] for i in range(d)]
        order = 2 ** len(pairs)

        def allowed(x, J):
            return all((not x >> k & 1 or all((j in J for j in range(a, b))) for k, (a, b) in enumerate(pairs)))
    else:
        one = tuple(range(d + 1))

        def mul(a, b):
            return tuple((a[b[i]] for i in range(d + 1)))
        marks = []
        for i in range(d):
            a = list(one)
            a[i], a[i + 1] = (a[i + 1], a[i])
            marks.append(tuple(a))
        order = math.factorial(d + 1)

        def allowed(x, J):
            blocks = [0]
            for i in range(d):
                blocks.append(blocks[-1] + (i not in J))
            return all((blocks[i] == blocks[x[i]] for i in range(d + 1)))

    def powr(x, k):
        out = one
        for _ in range(k):
            out = mul(out, x)
        return out
    subs = []
    subsets = []
    for m in range(1 << d):
        J = {i for i in range(d) if m >> i & 1}
        subsets.append(J)
        subs.append(subgroup([marks[i] for i in J], one, mul))
    full = subs[-1]
    if not len(full) == order:
        raise AssertionError('Exact model check failed')
    for J, H in zip(subsets, subs):
        if not H == {g for g in full if allowed(g, J)}:
            raise AssertionError('Exact model check failed')
    for i in range(1 << d):
        for j in range(i, 1 << d):
            if not subs[i] & subs[j] == subs[i & j]:
                raise AssertionError('Exact model check failed')
    for r in marks:
        if not (r != one and mul(r, r) == one):
            raise AssertionError('Exact model check failed')
    for i in range(d):
        for j in range(i + 1, d):
            v = mul(marks[i], marks[j])
            expected = n if j == i + 1 else 2
            if not (powr(v, expected) == one and all((powr(v, k) != one for k in range(1, expected)))):
                raise AssertionError('Exact model check failed')
    for i in range(d - 2):
        A = mul(marks[i], marks[i + 1])
        B = mul(marks[i + 1], marks[i + 2])
        for k in range(1, n):
            if not powr(mul(powr(B, k), powr(A, k)), 2) == one:
                raise AssertionError('Exact model check failed')
    return {'d': d, 'n': n, 'order': order, 'parabolics': 1 << d, 'unordered_subset_pairs': (1 << d) * ((1 << d) + 1) // 2, 'parabolic_membership_profiles_exact': True, 'all_extra_relators_pass': True}

def main():
    a = argparse.ArgumentParser()
    a.add_argument('--report', type=Path, required=True)
    args = a.parse_args()
    if args.report.exists():
        raise SystemExit('Refusing to overwrite report')
    t = time.monotonic()
    rows = [test(d, n) for n in [3, 4] for d in [3, 4, 5]]
    out = {'status': 'PASS', 'scope': 'six finite explicit models; uniform proofs are separate; no universal-group-order inference', 'results': rows, 'seconds': time.monotonic() - t, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with args.report.open('x') as f:
        json.dump(out, f, indent=2)
        f.write('\n')
    print(json.dumps(out, indent=2))
if __name__ == '__main__':
    main()
