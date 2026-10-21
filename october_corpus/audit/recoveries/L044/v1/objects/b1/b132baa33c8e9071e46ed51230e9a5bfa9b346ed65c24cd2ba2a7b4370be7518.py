"""Independent corroboration of the written endpoint identities.

Products act from left to right. The uniform proof is the cycle calculation
in the manuscript; these finite checks are not an additional premise.
"""
import json


def case(b, epsilon=0, delta=0, h_kind=None):
    names = ['A0', 'A1', 'A0p', 'A1p']
    names += [f'B{j}{suffix}' for suffix in ['', 'p'] for j in range(b)]

    def perm(pairs):
        p = dict(zip(names, names))
        for a, c in pairs:
            p[a], p[c] = p[c], p[a]
        return p

    def mul(*gs):
        p = dict(zip(names, names))
        for g in gs:
            p = {a: g[p[a]] for a in names}
        return p

    def power(p, n):
        return mul(*([p] * n))

    tau = perm([('A0', 'A0p'), ('A1', 'A1p')]
               + [(f'B{j}', f'B{j}p') for j in range(b)])
    c = perm([('A0', 'A1'), ('A0p', 'A1p')])
    p = perm([('B1', 'B2'), ('B1p', 'B2p')])
    q = perm([(f'B{b-2}', f'B{b-1}'), (f'B{b-2}p', f'B{b-1}p')])
    if b >= 6:
        x = perm([('A0p', 'A1p'), ('B0p', f'B{b-1}p')])
        word = mul(power(mul(tau, power(mul(x, q), 2), x), 2), q)
        expected = c
        label = 'uniform'
    else:
        eta = (1 - epsilon - delta) % 2
        x = perm(([('A0p', 'A1p')] if eta else [])
                 + ([('B1', 'B2')] if epsilon else [])
                 + ([('B1p', 'B2p')] if delta else [])
                 + [('B0p', 'B3p')])
        if epsilon == delta:
            x0 = mul(x, power(p, epsilon))
            word = mul(power(mul(tau, power(mul(x0, q), 2), x0), 2), q)
            expected = c
            label = 'equal'
        else:
            h = [('A1', 'A0p'), ('A1', 'A1p'), ('A0p', 'A1p')][h_kind]
            s = perm([('A0', 'B0'), h])
            w = mul(s, power(mul(tau, s, x), 5), tau, x)
            word = w if h_kind == 1 else power(mul(tau, s, tau, w), 3)
            expected = p
            label = 'unequal'
    if word != expected:
        raise ValueError((b, epsilon, delta, h_kind, label))
    return {'b': b, 'epsilon': epsilon, 'delta': delta, 'h': h_kind, 'word': label}


rows = [case(b) for b in [6, 8, 10]]
rows += [case(4, e, e) for e in [0, 1]]
rows += [case(4, e, 1-e, h) for e in [0, 1] for h in range(3)]
print(json.dumps({'status': 'PASS', 'cases': rows,
                  'role': 'Optional corroboration, not the uniform proof.'}, indent=2))
