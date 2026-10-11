#!/usr/bin/env python3
"""Independent exact checks of the literal affine words, not a uniform theorem test."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ONE = ((1, 0, 0, 1), (0, 0))

def mul(g, h):
    a, b, c, d = g[0]
    e, f, j, k = h[0]
    x, y = h[1]
    return ((a*e+b*j, a*f+b*k, c*e+d*j, c*f+d*k),
            (a*x+b*y+g[1][0], c*x+d*y+g[1][1]))

def inv(g):
    a, b, c, d = g[0]
    det = a*d-b*c
    if det not in (-1, 1):
        raise ValueError("not an integral affine automorphism")
    m = (d//det, -b//det, -c//det, a//det)
    x, y = g[1]
    return (m, (-m[0]*x-m[1]*y, -m[2]*x-m[3]*y))

def power(g, n):
    r = ONE
    for _ in range(n):
        r = mul(r, g)
    return r

def word(*letters):
    r = ONE
    for g in letters:
        r = mul(r, g)
    return r

def comm(g, h):
    return word(inv(g), inv(h), g, h)

def require(condition, message):
    if not condition:
        raise ValueError(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    a = ((-1, 0, 0, 1), (0, 0))
    b = ((0, 1, 1, 0), (0, 0))
    c = ((1, 0, 0, -1), (0, 1))
    for s in (a, b, c):
        require(power(s, 2) == ONE, "marker is not an involution")
        require(mul(s, inv(s)) == ONE, "inverse convention")
    for g, n in ((word(a,b),4), (word(b,c),4), (word(a,c),2)):
        require(power(g, n) == ONE, "Coxeter relation")
        require(all(power(g, m) != ONE for m in range(1,n)), "exact pair order")
    even = comm(power(word(a,b),2), c)
    odd = comm(power(word(a,b),2), power(word(b,c),2))
    require(even == (ONE[0], (0,-2)), "even parity word")
    require(odd == (ONE[0], (-2,-2)), "odd parity word")
    T, U = word(a,b,c,b), word(c,b,a,b)
    require(T == (ONE[0],(-1,0)) and U == (ONE[0],(0,1)), "translation generators")
    orbit = lambda v: sorted(set((eps*v[i],eta*v[1-i])
        for i in (0,1) for eps,eta in itertools.product((-1,1), repeat=2)))
    require(len(orbit(even[1])) == len(orbit(odd[1])) == 4, "orbit size")
    # H6 has lattice 2<(1,1),(1,-1)>: both coordinates are even,
    # and after division by two they have equal parity.
    in_h6_lattice = lambda v: v[0]%2 == v[1]%2 == 0 and (v[0]//2-v[1]//2)%2 == 0
    require(not in_h6_lattice((2,0)), "first doubled translation nontrivial")
    require(not in_h6_lattice((0,2)), "second doubled translation nontrivial")
    require(in_h6_lattice((2,-2)), "their classes coincide")
    require(in_h6_lattice((4,0)) and in_h6_lattice((0,4)), "both have order two")
    # A changed parity translation is a meaningful negative control.
    rejected = False
    try:
        require(even == (ONE[0],(0,-1)), "altered parity translation")
    except ValueError:
        rejected = True
    require(rejected, "negative control was accepted")
    out = {"status":"PASS", "convention":"rightmost affine transformation acts first; [g,h]=g^-1 h^-1 g h",
        "even_commutator":even, "odd_commutator":odd,
        "even_signed_orbit":orbit(even[1]), "odd_signed_orbit":orbit(odd[1]),
        "translation_words":{"abcb":T,"cbab":U},
        "H6_doubled_translations":"equal nonidentity elements of order two",
        "altered_word_rejected":rejected,
        "scope":"Exact literal word arithmetic and H6 check. The all-parameter lattice and presentation conclusions are independently reviewed written proofs, not extrapolations from this computation.",
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.out.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({"status":"PASS","report":str(args.out)}))

if __name__ == "__main__":
    main()
