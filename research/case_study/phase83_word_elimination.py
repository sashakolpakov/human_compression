#!/usr/bin/env python3
"""Generate the exact elementary elimination trace for the complement group."""
import argparse
from pathlib import Path
from collections import Counter
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def reduce(w):
    out = []
    for x in w:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def inverse(w):
    return tuple(-x for x in reversed(w))


def subst(w, v, replacement):
    return reduce(y for x in w for y in
                  (replacement if x == v else inverse(replacement) if x == -v else (x,)))


def cyclic(w):
    w = reduce(w)
    prefix = []
    while len(w) > 1 and w[0] == -w[-1]:
        prefix.append(w[0]); w = w[1:-1]
    return tuple(prefix), w


def build(path):
    model = json.loads((ROOT / 'phase66_coprime_cover_permutation_model.json').read_text())
    gens = [tuple(g) for g in model['generators']]
    one = tuple(range(1, 129))
    group, seen = [one], {one}
    for g in group:
        for s in gens:
            gs = tuple(s[i-1] for i in g)
            if gs not in seen:
                seen.add(gs); group.append(gs)
    base = [1, gens[3][0], gens[0][0], gens[0][gens[3][0]-1]]
    quads = sorted({tuple(g[i-1] for i in base) for g in group})
    originals = [(-d, c, -a, b) for a, b, c, d in quads]
    rows = {i: w for i, w in enumerate(originals)}
    delta = (-1, 40)
    steps = []
    while True:
        candidates = []
        for i, w in rows.items():
            counts = Counter(map(abs, w))
            single = [v for v, count in counts.items() if count == 1]
            if single:
                v = max(single)
                candidates.append((len(w), -v, i))
        if not candidates:
            break
        _, negv, i = min(candidates)
        v, w = -negv, rows[i]
        pos = next(j for j, x in enumerate(w) if abs(x) == v)
        a, b, sign = w[:pos], w[pos+1:], 1 if w[pos] > 0 else -1
        replacement = reduce(inverse(a) + inverse(b) if sign == 1 else b + a)
        steps.append(dict(variable=v, relation=i, before=w, replacement=replacement,
                          left=a, right=b, sign=sign))
        del rows[i]
        rows = {j: new for j, row in rows.items() if (new := subst(row, v, replacement))}
        delta = subst(delta, v, replacement)
    unique = {}
    for i, w in rows.items():
        pre, cyc = cyclic(w)
        rotations = [cyc[j:] + cyc[:j] for j in range(len(cyc))]
        ic = inverse(cyc)
        rotations += [ic[j:] + ic[:j] for j in range(len(ic))]
        key = min(rotations)
        unique.setdefault(key, []).append(i)
    data = dict(model_sha256=hashlib.sha256((ROOT / 'phase66_coprime_cover_permutation_model.json').read_bytes()).hexdigest(),
                group_order=len(group), quads=quads, originals=originals, steps=steps,
                remaining=rows, cyclic_classes=[dict(word=k, original_indices=v) for k, v in unique.items()],
                delta=delta, delta_squared_cyclic=cyclic(delta + delta))
    with path.open('x') as output:
        output.write(json.dumps(data, indent=2) + '\n')
    print(json.dumps(dict(steps=len(steps), remaining=len(rows),
                         cyclic_classes=len(data['cyclic_classes']), delta=delta,
                         output=str(path)), indent=2))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    build(ap.parse_args().output)
