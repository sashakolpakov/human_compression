"""Independent explicit normal-form verification of the small central lift.

No symbolic group package or unproved presentation-consistency assumptions.
The ambient group is an elementary abelian module extended by beta and sigma,
times C_(p^2), with multiplication encoded by its two matrix actions.
"""

from collections import deque
import argparse
import json


def verify(p=5, r=4):
    assert p >= 5 and r % 2 == 0 and 4 <= r <= p - 1
    assert all(p % d for d in range(2, int(p**0.5) + 1)), "p must be prime"
    # Vectors use the cyclic module basis e_i = (T-I)^i e_0.
    # T^n=(I+N)^n, with integer generalized binomial coefficients.
    def binomial(n, k):
        z = 1
        for j in range(k):
            z = z * (n - j) // (j + 1)
        return z

    def T(v, n):
        return tuple(sum(binomial(n, j - i) * v[i]
                         for i in range(j + 1)) % p for j in range(r))

    zero = (0,) * r
    e0 = (1,) + (0,) * (r - 1)
    er = (0,) * (r - 1) + (1,)
    # S(e_i)=(T^-1-I)^i(e_0); this satisfies STS=T^-1.
    cols = [e0]
    for i in range(1, r):
        previous = cols[-1]
        transformed = T(previous, -1)
        cols.append(tuple((transformed[j] - previous[j]) % p
                          for j in range(r)))

    def S(v):
        return tuple(sum(v[i] * cols[i][j] for i in range(r)) % p
                     for j in range(r))

    for i in range(r):
        ei = tuple(int(j == i) for j in range(r))
        assert S(S(ei)) == ei
        assert S(T(S(ei), 1)) == T(ei, -1)
        assert T(ei, p) == ei
    assert S(er) == tuple((-z) % p for z in er)
    assert T(er, 1) == er

    # Elements are (v,k,epsilon,j) = v beta^k sigma^epsilon x^j,
    # 0<=k<p, epsilon in {0,1}, 0<=j<p^2, beta^p=e_(r-1).
    identity = (zero, 0, 0, 0)

    def mul(g, h):
        v, k, epsilon, j = g
        w, l, delta, q = h
        action = T(S(w) if epsilon else w, -k)
        combined = k + (-l if epsilon else l)
        carry, exponent = divmod(combined, p)
        vector = tuple((v[i] + action[i] + (carry if i == r-1 else 0)) % p
                       for i in range(r))
        return (vector, exponent, (epsilon + delta) % 2, (j + q) % (p*p))

    def power(g, n):
        ans = identity
        while n:
            if n & 1:
                ans = mul(ans, g)
            g = mul(g, g)
            n //= 2
        return ans

    def cyclic(g):
        ans = {identity}
        x = g
        while x != identity:
            assert x not in ans, "Multiplication did not define a finite cyclic group"
            ans.add(x)
            x = mul(x, g)
        return ans

    beta = (zero, 1, 0, 0)
    sigma = (zero, 0, 1, 0)
    s1 = (e0, 0, 0, 0)
    assert power(beta, p) == (er, 0, 0, 0)
    assert mul(mul(sigma, beta), sigma) == power(beta, p*p-1)
    assert mul(mul(sigma, s1), sigma) == s1
    a = (T(e0, -1), 1, 0, 1)
    b = (tuple((-z) % p for z in e0), 0, 1, p*p-1)
    aa, bb = cyclic(a), cyclic(b)
    assert len(aa) == p*p
    assert len(bb) == 2*p*p
    assert aa.intersection(bb) == {identity}
    assert power(mul(a, b), 2) == identity
    seen = {identity}
    queue = deque([identity])
    while queue:
        g = queue.popleft()
        for h in (a, b):
            nxt = mul(g, h)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    expected = 2*p**(r+2)
    assert len(seen) == expected
    projected = {(v, k, epsilon) for v, k, epsilon, j in seen}
    kernel = {(v, k, epsilon, j) for v, k, epsilon, j in seen
              if v == zero and k == 0 and epsilon == 0}
    assert len(projected) == 2*p**(r+1)
    assert len(kernel) == p
    assert kernel == cyclic(power(b, 2*p))
    # The fiber equation is exact, not just a subgroup order coincidence.
    assert all(j % p == v[0] for v, k, epsilon, j in seen)
    return {"p": p, "r": r, "m": r+2, "group_order": len(seen),
            "base_order": len(projected), "generator_orders": [len(aa), len(bb)],
            "product_order": len(cyclic(mul(a, b))),
            "cyclic_intersection_order": len(aa & bb), "kernel_order": len(kernel),
            "note": "Chirality follows from the proved invariant-kernel argument; no automorphism enumeration used."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, default=5)
    parser.add_argument("--r", type=int, default=4)
    args = parser.parse_args()
    print(json.dumps(verify(args.p, args.r), indent=2))
