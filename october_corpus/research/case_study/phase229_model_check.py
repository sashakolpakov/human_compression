#!/usr/bin/env python3
"""Finite implementation checks for the written all-n polygon construction."""
import json
from itertools import combinations

def require(test, message):
    if not test:
        raise RuntimeError(message)

def model(n):
    one = (0, 0, 0)
    def action(g, mask):
        _, k, e = g
        out = 0
        for i in range(n):
            if (mask >> i) & 1:
                out ^= 1 << ((k + (-1 if e else 1) * i) % n)
        return out
    def mul(g, h):
        v, k, e = g
        w, l, f = h
        return (v ^ action(g, w), (k + (-1 if e else 1) * l) % n, e ^ f)
    def power(g, k):
        out = one
        for _ in range(k):
            out = mul(out, g)
        return out
    def closure(gens):
        reached, queue = {one}, [one]
        for g in queue:
            for h in gens:
                p = mul(g, h)
                if p not in reached:
                    reached.add(p); queue.append(p)
        return reached
    def dual(g):
        return (g[0] ^ 1 ^ action(g, 1), g[1], g[2])
    r = [(0, 1, 1), (0, 0, 1), (3, 1, 1)]
    parabolics = [closure([r[i] for i in range(3) if (I >> i) & 1]) for I in range(8)]
    require(len(parabolics[7]) == n * 2 ** n, 'full generation/order')
    for I in range(8):
        for J in range(8):
            require(parabolics[I] & parabolics[J] == parabolics[I & J], 'IP')
    require(all(power(g, 2) == one and g != one for g in r), 'involutions')
    require(power(mul(r[0], r[2]), 2) == one, 'string')
    x, y = mul(r[0], r[1]), mul(r[1], r[2])
    for g in (x, y):
        require(power(g, n) == one, 'adjacent order upper')
        require(all(power(g, k) != one for k in range(1, n)), 'adjacent order lower')
    for k in range(n):
        require(mul(power(y, k), power(x, k)) == (1 ^ (1 << (-k % n)), 0, 0), 'displacement basis')
    require([dual(g) for g in r] == list(reversed(r)), 'mark reversal')
    for g in parabolics[7]:
        require(dual(dual(g)) == g, 'dual involution')
        for h in r:
            require(dual(mul(g, h)) == mul(dual(g), dual(h)), 'dual right-generator compatibility')
    return {'n': n, 'group_order': len(parabolics[7]), 'parabolic_orders': [len(g) for g in parabolics], 'intersection_pairs_checked': 64, 'model_pass': True}

def inverse_action_counterexample():
    n = 3
    def act(k, e, w):
        return sum(((w >> i) & 1) << ((k + (-1 if e else 1) * i) % n) for i in range(n))
    def wrong(g, h):
        v, k, e = g; w, l, f = h
        inverse_k = (-(-1 if e else 1) * k) % n
        return (v ^ act(inverse_k, e, w), (k + (-1 if e else 1) * l) % n, e ^ f)
    u, v, w = (0, 1, 0), (0, 0, 1), (3, 0, 0)
    left, right = wrong(wrong(u, v), w), wrong(u, wrong(v, w))
    require(left == (3, 1, 1) and right == (6, 1, 1), 'explicit inverse-action nonassociativity')
    return {'n': n, 'inputs': [u, v, w], 'left_bracketing': left, 'right_bracketing': right, 'associative': False}

if __name__ == '__main__':
    print(json.dumps({'status': 'P229_FINITE_MODEL_PASS', 'scope': 'Diagnostics n=3..10; the unbounded proof is written, not inferred from these samples.', 'models': [model(n) for n in range(3, 11)], 'inverse_action_counterexample': inverse_action_counterexample()}, indent=2))
