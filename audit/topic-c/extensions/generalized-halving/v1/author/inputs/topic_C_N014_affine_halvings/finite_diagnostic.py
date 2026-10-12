"""Private exact diagnostic; no claim of whole-source recovery."""
from collections import deque
import json
from pathlib import Path


def compose(g, h, modulus):
    t, p = g
    u, q = h
    v = tuple((t[i] + (1 if p[i] > 0 else -1) * u[abs(p[i])-1]) % modulus
              for i in range(len(p)))
    r = tuple((1 if p[i] > 0 else -1) * q[abs(p[i])-1]
              for i in range(len(p)))
    return v, r


def identity(n):
    return (0,) * n, tuple(range(1, n+1))


def product(gens, word, modulus):
    result = identity(len(gens[0][0]))
    for i in word:
        result = compose(result, gens[i], modulus)
    return result


def order(g, modulus):
    e = identity(len(g[0]))
    h, n = e, 0
    while True:
        h = compose(h, g, modulus)
        n += 1
        if h == e:
            return n
        assert n < 10000


def closure(gens, modulus):
    e = identity(len(gens[0][0]))
    seen, todo = {e}, deque([e])
    while todo:
        g = todo.popleft()
        for h in gens:
            x = compose(g, h, modulus)
            if x not in seen:
                seen.add(x)
                todo.append(x)
    return seen


def run():
    old = [((1, 0, 0), (-1, 2, 3)),
           ((0, 0, 0), (2, 1, 3)),
           ((0, 0, 0), (1, 3, 2)),
           ((0, 0, 0), (1, 2, -3))]
    expected = [[1, 2, 3, 2], [2, 1, 3, 2],
                [3, 3, 1, 4], [2, 2, 4, 1]]
    rows = []
    for modulus in [3, 6]:
        gens = [product(old, [0, 1, 0], modulus)] + old[1:]
        pair_orders = [[order(compose(a, b, modulus), modulus)
                        for b in gens] for a in gens]
        assert pair_orders == expected
        w = product(gens, [0, 2, 3, 2, 1], modulus)
        assert compose(w, w, modulus) == ((2 % modulus, 0, 0), (1, 2, 3))
        assert order(w, modulus) == 6
        group = closure(gens, modulus)
        translations = [g for g in group if g[1] == (1, 2, 3)]
        linear_parts = {g[1] for g in group}
        assert len(linear_parts) == 48
        assert len(group) == (1296 if modulus == 3 else 5184)
        if modulus == 6:
            assert all(sum(g[0]) % 2 == 0 for g in group)
            assert len(translations) == 108
        else:
            assert group == closure(old, modulus)
            assert len(translations) == 27
        rows.append({'modulus': modulus, 'generators': gens,
                     'pair_orders': pair_orders, 'extra_word': w,
                     'extra_word_order': 6, 'translation_count': len(translations),
                     'linear_count': len(linear_parts), 'group_order': len(group)})
    return {'status': 'PASS_DIAGNOSTIC', 'parameters': {'n': 3, 'k': 1, 's': 3},
            'cases': rows,
            'conclusion': 'The displayed Coxeter relations and extra word to power six admit a group of order5184; the actual halving group has order1296. Thus they cannot be an exact presentation of that group.',
            'source_boundary': 'N014 arXiv2405.19050v1 Proposition5.8 and its proof; not a journal-version or priority claim.'}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'parameters', 'conclusion']}))
