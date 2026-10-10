#!/usr/bin/env python3
"""Exhaust small vector-space coset systems; no imported proof implementation.

This tests the coordinate conclusion, not the uniform group-theoretic lemma.
Only the Python standard library is used. Output defaults beside the script.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def enumerate_spaces(p, d):
    size = p**d
    digits = [tuple((v // p**i) % p for i in range(d)) for v in range(size)]
    add = [[sum(((x + y) % p) * p**i for i, (x, y) in enumerate(zip(a, b)))
            for b in digits] for a in digits]
    multiples = [[sum(((c * a) % p) * p**i for i, a in enumerate(v))
                  for c in range(p)] for v in digits]
    spaces = {1}
    queue = [1]
    for space in queue:
        members = [v for v in range(size) if (space >> v) & 1]
        for v in range(1, size):
            if (space >> v) & 1:
                continue
            bigger = 0
            for x in members:
                for y in multiples[v]:
                    bigger |= 1 << add[x][y]
            if bigger not in spaces:
                spaces.add(bigger)
                queue.append(bigger)
    return sorted(spaces), add, multiples


def audit(p, d, max_rank):
    spaces, add, multiples = enumerate_spaces(p, d)
    full = (1 << p**d) - 1
    proper = [s for s in spaces if s != full]
    results = []
    for r in range(1, max_rank + 1):
        checked = firm = passed = coordinate_bijections = 0
        for family in itertools.combinations(proper, r):
            checked += 1
            meets = [full] * (1 << r)
            for mask in range(1, 1 << r):
                low = mask & -mask
                meets[mask] = meets[mask ^ low] & family[low.bit_length() - 1]
            if len(set(meets)) != 1 << r:
                continue
            firm += 1
            reachable = {0}
            for mask in range(1 << r):
                if mask not in reachable:
                    continue
                for i in range(r):
                    nxt = mask | (1 << i)
                    if nxt != mask and meets[mask].bit_count() == p * meets[nxt].bit_count():
                        reachable.add(nxt)
            chain = (1 << r) - 1 in reachable
            hyperplanes = all(s.bit_count() == p**(d - 1) for s in family)
            assert chain == hyperplanes, (p, d, r, family)
            if not chain:
                continue
            passed += 1
            for mask, meet in enumerate(meets):
                assert meet.bit_count() == p**(d - mask.bit_count())
            base = meets[-1]
            witnesses = []
            for i, subspace in enumerate(family):
                difference = meets[((1 << r) - 1) ^ (1 << i)] & ~subspace
                assert difference
                witnesses.append((difference & -difference).bit_length() - 1)
            # Enumerate the actual coefficient representatives and check that
            # their cosets of B partition the entire vector space.
            covered = 0
            for coefficients in itertools.product(range(p), repeat=r):
                representative = 0
                for c, v in zip(coefficients, witnesses):
                    representative = add[representative][multiples[v][c]]
                coset = 0
                for b in range(p**d):
                    if (base >> b) & 1:
                        coset |= 1 << add[representative][b]
                assert not (covered & coset)
                covered |= coset
            assert covered == full
            coordinate_bijections += 1
        expected = 0
        if r <= d:
            numerator = math.prod(p**d - p**j for j in range(r))
            denominator = (p - 1)**r * math.factorial(r)
            assert numerator % denominator == 0
            expected = numerator // denominator
        assert passed == expected
        results.append(dict(rank=r, families_examined=checked,
                            firm_families=firm, maximal_chain_families=passed,
                            coordinate_bijections=coordinate_bijections,
                            expected_unordered_count=expected))
    return dict(p=p, dimension=d, subspaces=len(spaces), ranks=results)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--source-pdf', type=Path,
                        help='Optional privately acquired primary PDF, used only for identity verification')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    source_hash = 'cfbd53bc367ecaea644214eb0f64fc5db0c20d63096fdc239cf5d61c3f72c5c9'
    if args.source_pdf:
        assert digest(args.source_pdf) == source_hash, 'Primary PDF identity mismatch'
    cases = [(2, d, d + (d < 4)) for d in range(1, 5)]
    cases += [(3, d, d + (d < 3)) for d in range(1, 4)]
    cases += [(5, d, d + 1) for d in range(1, 3)]
    results = [audit(*case) for case in cases]
    report = dict(status='PASS', scope='Exhaustive finite coordinate diagnostics only',
                  source_pdf_sha256=source_hash,
                  source_pdf_verification='verified' if args.source_pdf else 'not_supplied',
                  script_sha256=digest(Path(__file__)), cases=results,
                  families_examined=sum(r['families_examined'] for c in results for r in c['ranks']),
                  coordinate_bijections=sum(r['coordinate_bijections'] for c in results for r in c['ranks']))
    output = args.output or here / 'phase16_frattini_coordinate_check.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['status', 'families_examined', 'coordinate_bijections']}))


if __name__ == '__main__':
    main()
