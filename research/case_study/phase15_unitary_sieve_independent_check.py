#!/usr/bin/env python3
"""Independent exact prime-power/sieve audit; no author code imported."""
from pathlib import Path
from fractions import Fraction
from math import isqrt, prod
from hashlib import sha256
import argparse
import json


def prime_roster(limit):
    mask = bytearray(b'\x01') * (limit + 1)
    mask[0:2] = b'\x00\x00'
    for p in range(2, isqrt(limit) + 1):
        if mask[p]:
            mask[p*p:limit+1:p] = b'\x00' * ((limit-p*p)//p+1)
    return [n for n, flag in enumerate(mask) if flag]


def trial_factors(n, primes):
    factors = {}
    for p in primes:
        if p*p > n:
            break
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def coefficient(support, core_count, constant=8, genus=1):
    tail = support[core_count:]
    delta = Fraction(1) - sum((Fraction(1, p) for p in tail), Fraction(0))
    if delta <= 0:
        return None
    # Base normalized error plus the sum of normalized mixed differences.
    weight = 2**core_count
    base_error = constant*(weight-1) + 2*genus
    mixed_error = constant*weight*sum((Fraction(p-1, p) for p in tail), Fraction(0))/delta
    return base_error + mixed_error, delta


def ceiling(x):
    return (x.numerator + x.denominator - 1)//x.denominator


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    root = args.directory
    author_path = root/'phase15_unitary_sieve_check.json'
    author_bytes = author_path.read_bytes()
    author = json.loads(author_bytes)
    cutoff = 1029254
    primes = prime_roster(cutoff+1)
    c6 = prod((Fraction(64, p) for p in primes if p < 64), start=Fraction(1))
    qbound = ceiling(8**6*c6)
    assert qbound == 725311328745792 == author['initial_cutoff']
    assert [c6.numerator, c6.denominator] == author['initial_C_sixth_power']
    boot = []
    for max_support, core_count, target in [(21,3,16427566),(12,2,1574926),(11,2,1029254)]:
        primorial = prod(primes[:max_support+1])
        assert primorial >= qbound*qbound
        A, delta = coefficient(primes[:max_support], core_count)
        assert A > 0 and ceiling(A*A) == target
        entry = {'previous_cutoff':qbound, 'omega_max':max_support,
                 'core_prime_count':core_count, 'excluded_primorial':primorial,
                 'delta':[delta.numerator,delta.denominator],
                 'coefficient':[A.numerator,A.denominator], 'new_cutoff':target}
        boot.append(entry)
        qbound = target
    assert boot == author['bootstrap']
    roster = {}
    for p in primes:
        q, exponent = p, 1
        while q < cutoff:
            if q >= 7 and q % 4 == 3:
                assert p % 4 == 3 and exponent % 2 == 1
                assert q not in roster
                roster[q] = (p, exponent)
            q *= p
            exponent += 1
    saved = {r['q']:r for r in author['field_records']}
    assert len(saved) == len(author['field_records']) and saved.keys() == roster.keys()
    exceptional = []
    for q in sorted(roster):
        p, exponent = roster[q]
        row = saved[q]
        assert (row['p'], row['exponent']) == (p, exponent)
        fm, fp = trial_factors(q-1, primes), trial_factors(q+1, primes)
        assert prod(r**e for r,e in fm.items()) == q-1
        assert prod(r**e for r,e in fp.items()) == q+1
        assert fm == {int(r):e for r,e in row['minus_factors'].items()}
        assert fp == {int(r):e for r,e in row['plus_factors'].items()}
        support = sorted(fm.keys() | fp.keys())
        constant, genus = (2,0) if p == 3 else (8,1)
        assert constant == row['character_bound']
        certificate = None
        for core_count in range(len(support)+1):
            result = coefficient(support, core_count, constant, genus)
            if result is None:
                continue
            A, delta = result
            assert A > 0
            # Clear denominators before the strictly positive comparison.
            numerator = (q+1)**2 * A.denominator**2 - q*A.numerator**2
            if numerator > 0:
                margin = Fraction(numerator, A.denominator**2)
                certificate = {'core_prime_count':core_count,
                               'delta':[delta.numerator,delta.denominator],
                               'coefficient':[A.numerator,A.denominator],
                               'squared_margin':[margin.numerator,margin.denominator]}
                break
        assert certificate == row['sieve_certificate'], q
        if certificate is None:
            exceptional.append(q)
    assert exceptional == author['exceptions']
    assert len(roster) == author['field_count'] == 40389
    assert len(exceptional) == author['exception_count'] == 1699
    assert max(exceptional) == 245519
    report = {
        'status':'PASS',
        'author_report_sha256':sha256(author_bytes).hexdigest(),
        'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'prime_backend':'Independent bytearray Eratosthenes sieve; trial division for every q-1 and q+1',
        'bound_backend':'Fractions and integer cleared-denominator comparisons; independently derived base-plus-mixed coefficient',
        'initial_cutoff':725311328745792,
        'bootstrap':boot,
        'field_count':len(roster),
        'factorizations_verified':2*len(roster),
        'every_field_certificate_matches':True,
        'exception_count':len(exceptional),
        'maximum_exception':max(exceptional),
        'exceptions':exceptional,
        'scope':'Exact arithmetic coverage only; no author code imported. Character bounds and the proof that these thresholds cover all larger q are separately reviewed. No finite parameter witnesses checked by this script.'
    }
    out = args.output or root/'phase15_unitary_sieve_independent_check.json'
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','field_count','factorizations_verified','exception_count','maximum_exception']},indent=2))


if __name__ == '__main__':
    main()
