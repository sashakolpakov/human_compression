#!/usr/bin/env python3
"""Exact bounded diagnostics for phase11's unique large Frattini class.

Reuses the frozen phase10 coordinate multiplication, without modifying it.
The all-parameter classification and theorem remain mathematical inputs.
"""
import argparse
import hashlib
import json
from pathlib import Path
from phase10_cyclic_tpp_check import metacyclic, nonmetacyclic, semidirect


def inspect(n, mul, swap, maximum):
    ext = semidirect(mul, swap)
    one = (0, 0, 0)
    gens = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    count, corefree, largest = 0, 0, 0
    for i in range(n):
        for j in range(n):
            x = (i, j, 1)
            invol, order = x, 2
            while ext(invol, invol) != one:
                invol = ext(invol, invol)
                order *= 2
                assert order <= 2*n
            central = all(ext(invol, g) == ext(g, invol) for g in gens)
            if not central:
                corefree += 1
                largest = max(largest, order)
                assert order <= maximum
            count += 1
    assert largest <= maximum
    a_invol = (n//2, 0, 0)
    assert any(ext(a_invol, g) != ext(g, a_invol) for g in gens)
    return dict(outside_elements=count, center_free_outside_elements=corefree,
                maximum_center_free_outside_order=largest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-e', type=int, default=6)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if not 3 <= args.max_e <= 9:
        ap.error('--max-e must be between 3 and 9')
    models = []
    for e in range(3, args.max_e+1):
        n = 2**e
        for k in range(2):
            for ell in range(2):
                mul, swap = nonmetacyclic(n,k,ell)
                models.append(dict(branch='nonmetacyclic',e=e,k=k,ell=ell,
                                   **inspect(n,mul,swap,4)))
        for ratio in range(1,n,4):
            mul, swap, _ = metacyclic(n,ratio)
            models.append(dict(branch='metacyclic',e=e,ratio=ratio,
                               **inspect(n,mul,swap,2)))
    root = Path(__file__).resolve().parent
    names = ['phase11_cyclic_tpp.md',Path(__file__).name,
             'phase10_cyclic_tpp_check.py','phase10_cyclic_tpp.md']
    report = dict(status='PASS',models=models,
                  model_count=len(models),
                  outside_elements=sum(x['outside_elements'] for x in models),
                  center_free_outside_elements=sum(x['center_free_outside_elements'] for x in models),
                  input_sha256={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names},
                  scope='Bounded normal-form checks only; no order-1024 catalogue and no complete gamma-eight exclusion.')
    text=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text,end='')


if __name__=='__main__':
    main()
