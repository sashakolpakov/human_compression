#!/usr/bin/env python3
"""Independent finite regression for the corrected N009 diagonal factors.

Use u=x+y, v=x-y modulo 2s, retaining the exact integral linear part.
These finite cases check, but do not prove, the all-s written correction.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check(s):
    modulus = 2*s
    identity = ((0, 0), (1, 0, 0, 1))

    def multiply(g, h):
        (u, v), (a, b, c, d) = g
        (w, z), (e, f, k, l) = h
        return ((u+a*w+b*z) % modulus, (v+c*w+d*z) % modulus), (
            a*e+b*k, a*f+b*l, c*e+d*k, c*f+d*l)

    def word(*factors):
        value = identity
        for g in factors:
            value = multiply(value, g)
        return value

    def subgroup(generators):
        seen, queue = {identity}, [identity]
        for g in queue:
            for h in generators:
                value = multiply(g, h)
                if value not in seen:
                    seen.add(value)
                    queue.append(value)
        return seen

    def order(g):
        x = identity
        for n in range(1, 16*s*s+1):
            x = multiply(x, g)
            if x == identity:
                return n
        raise ValueError("Order exceeded group bound")

    a = ((1 % modulus, 1 % modulus), (0, -1, -1, 0))
    b = ((0, 0), (1, 0, 0, -1))
    c = ((0, 0), (0, 1, 1, 0))
    require(all(order(g) == 2 for g in (a,b,c)), "Marker orders")
    require(order(word(a,b)) == order(word(b,c)) == 4, "Smooth adjacent pairs")
    require(word(a,c) == word(c,a), "Distant commutation")
    ba, bc, bac = word(a,b,a), word(c,b,c), word(a,c,b,a,c)
    full = subgroup([a,b,c])
    require(len(full) == 16*s*s, "Full diagonal quotient order")
    require(all((u-v) % 2 == 0 for (u,v), _ in full), "Translation lattice")
    first = subgroup([b,bac])
    second = subgroup([ba,bc])
    complement = subgroup([a,c])
    require(len(first) == len(second) == 2*s, "Corrected dihedral orders")
    require(order(word(b,bac)) == order(word(ba,bc)) == s, "Rotation orders")
    require(first & second == {identity}, "Factor intersection")
    require(all(multiply(x,y) == multiply(y,x) for x in first for y in second),
            "Factor commutation")
    product = {multiply(x,y) for x in first for y in second}
    require(len(complement) == 4 and product & complement == {identity},
            "Complement intersection")
    require({multiply(x,y) for x in product for y in complement} == full,
            "Complete semidirect product")
    require(all({word(g,x,g) for x in first} == second for g in (a,c)),
            "Complement action")
    wrong_first, wrong_second = subgroup([b,ba]), subgroup([bc,bac])
    require(len(wrong_first) == len(wrong_second) == 4, "Printed V4 factors")
    center = None
    if s in (1,2,4):
        actual = {g for g in full if all(multiply(g,h) == multiply(h,g) for h in (a,b,c))}
        if s == 1:
            claimed = subgroup([word(a,c), word(a,b,a,b), word(b,c,b,c)])
        else:
            translation = word(a,b,c,b)
            claimed = subgroup([word(*([translation]*s))])
        require(actual == claimed, "Unchanged N5 center formula")
        center = len(actual)
    return {"s":s, "group_order":len(full), "correct_factor_orders":[len(first),len(second)],
            "printed_factor_orders":[len(wrong_first),len(wrong_second)],
            "complement_order":len(complement), "source_factor_order_false":s!=2,
            "center_order_checked":center}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists() and not args.output.is_symlink(), "Fresh output required")
    rows = [check(s) for s in range(1,8)]
    result = {"status":"PASS", "scope":"Seven finite diagonal quotients; all-parameter proof is separate",
              "rows":rows, "script_sha256":sha256(Path(__file__).read_bytes()).hexdigest()}
    with args.output.open("x") as f:
        json.dump(result,f,indent=2); f.write("\n")
    print(json.dumps({"status":"PASS","cases":len(rows),"boundary_s1_included":True}))


if __name__ == "__main__":
    main()
