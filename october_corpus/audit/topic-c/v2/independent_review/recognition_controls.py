#!/usr/bin/env python3
"""Independent finite checks of the exact generic recognition interface.

These are hypothesis controls, not proofs of the arbitrary-group theorem.
The complete written argument and actual Lean file are reviewed separately.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def perm_mul(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def closure(generators, multiply, identity):
    found = {identity}
    pending = [identity]
    for x in pending:
        for g in generators:
            y = multiply(x, g)
            if y not in found:
                found.add(y)
                pending.append(y)
    return found


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    require(not a.out.exists() and not a.out.is_symlink(), 'fresh output')
    a.out.mkdir(parents=True)
    I = (0, 1, 2)
    c = (1, 2, 0)
    s = (0, 2, 1)
    powers = [I, c, perm_mul(c, c)]
    pairs = list(itertools.product(range(3), range(2)))
    mul = lambda u, v: ((u[0] + (-1 if u[1] else 1) * v[0]) % 3, u[1] ^ v[1])
    inverse = lambda u: perm_mul(powers[u[0]], s if u[1] else I)
    permutations = set(itertools.permutations(range(3)))
    q = {inverse(u): u for u in pairs}
    require(set(q) == permutations, 'S3 normal forms')
    require(all(inverse(mul(u,v)) == perm_mul(inverse(u),inverse(v))
                for u,v in itertools.product(pairs,repeat=2)), 'actual noncommutative semidirect lift')
    require(all(q[inverse(u)] == u for u in pairs), 'right inverse')
    require(all(inverse(q[g]) == g for g in permutations), 'left inverse')
    require(closure([c,s],perm_mul,I)==permutations, 'generation')

    # Missing generation: P=C2^3, N=H=C2, q forgets the third coordinate.
    xor = lambda x,y: x ^ y
    P = set(range(8))
    f = lambda n:n
    j = lambda h:2*h
    q2 = lambda x:x&3
    covariance = all(xor(xor(j(h),f(n)),j(h))==f(n) for n,h in itertools.product(range(2),repeat=2))
    require(covariance and all(q2(f(n))==n for n in range(2)) and
            all(q2(j(h))==2*h for h in range(2)), 'other hypotheses with no generation')
    require(closure([1,2],xor,0)==set(range(4)) and q2(0)==q2(4), 'extra invisible factor')

    # Missing covariance: C3 x C2 cannot map to S3 by these component maps.
    direct = lambda u,v:((u[0]+v[0])%3,u[1]^v[1])
    witness = next((u,v) for u,v in itertools.product(pairs,repeat=2)
                   if inverse(direct(u,v))!=perm_mul(inverse(u),inverse(v)))

    # Each inverse-value condition is separately needed, even with generation.
    drop_f = lambda x:x&2
    drop_j = lambda x:x&1
    require(all(drop_f(2*h)==2*h for h in range(2)) and drop_f(1)==drop_f(0), 'missing q-f condition')
    require(all(drop_j(n)==n for n in range(2)) and drop_j(2)==drop_j(0), 'missing q-j condition')
    output = dict(status='PASS_INDEPENDENT_FINITE_INTERFACE_CONTROLS',
        positive_model='S3 = C3 semidirect C2, inversion action',
        positive_multiplication_pairs_checked=36,
        controls=[dict(dropped='generation',model='C2^3 projects onto C2^2',kernel_order=2),
                  dict(dropped='covariance',model='C3 x C2 component formula into S3',witness=witness),
                  dict(dropped='q on N',model='C2^2',kernel_order=2),
                  dict(dropped='q on H',model='C2^2',kernel_order=2)],
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        arbitrary_group_theorem_proved_by_this_program=False)
    (a.out/'report.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(status=output['status'],controls=4,positive_pairs=36)))


if __name__=='__main__':main()
