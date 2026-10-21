"""Finite checks of the displayed permutations, not a substitute for the proof."""
import json
import sys

if not __debug__:
    raise SystemExit("Run without Python optimization; the checks must remain enabled.")


def cycle(n, labels):
    p = list(range(n))
    for a, b in zip(labels, labels[1:] + labels[:1]):
        p[a] = b
    return tuple(p)


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    ans = [0] * len(p)
    for i, v in enumerate(p):
        ans[v] = i
    return tuple(ans)


def power(p, k):
    ans = tuple(range(len(p)))
    for _ in range(k):
        ans = compose(ans, p)
    return ans


def conjugate(p, h):
    return compose(h, compose(p, inverse(h)))


def pairs(n, edges):
    p = list(range(n))
    for a, b in edges:
        p[a], p[b] = b, a
    return tuple(p)


def check():
    rows = []
    for n in range(8, 102):
        odd = n % 2
        labels = list(range(n)) if odd else list(range(1, n))
        x = cycle(n, labels)
        t = pairs(n, [(0, 1), (2, 5) if odd else (2, 3)])
        tx = conjugate(t, power(x, 2 if odd else 3))
        expected = pairs(n, [(2, 3), (4, 7)] if odd else [(0, 4), (5, 6)])
        assert tx == expected
        product = compose(t, tx)
        square = power(product, 2)
        support = [i for i in range(n) if square[i] != i]
        assert len(support) == 3 and power(square, 3) == tuple(range(n))
        assert set(support) == ({2, 3, 5} if odd else {0, 1, 4})
        inverters = []
        for c in range(len(labels)):
            h = list(range(n))
            for k, a in enumerate(labels):
                h[a] = labels[(c - k) % len(labels)]
            h = tuple(h)
            assert conjugate(x, h) == inverse(x)
            assert conjugate(t, h) != t
            inverters.append(h)
        assert len(set(inverters)) == len(labels)
        rows.append({"n": n, "three_cycle_support": support,
                     "inverting_permutations_checked": len(inverters)})
    # Check the disjoint-transposition identity used by the merge lemma.
    assert pairs(4, [(0, 1), (2, 3)]) == compose(
        cycle(4, [0, 2, 1]), cycle(4, [0, 2, 3]))
    return {"status": "PASS", "range": [8, 101], "cases": len(rows),
            "rows": rows, "role": "Finite algebra checks only; the TeX proof covers all n."}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
