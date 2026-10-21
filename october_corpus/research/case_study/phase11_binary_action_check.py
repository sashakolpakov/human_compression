#!/usr/bin/env python3
"""Complete finite enumeration of the binary square-action lemma.

Vectors are three-bit integers; matrix tuples list the images of x=1,
y=2,z=4. Uses only Python's standard library.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def apply(matrix, vector):
    answer = 0
    for i in range(3):
        if vector >> i & 1:
            answer ^= matrix[i]
    return answer


def run():
    identity = (1,2,4)
    matrices = [m for m in itertools.product(range(8), repeat=3)
                if len({apply(m,v) for v in range(8)}) == 8]
    assert len(matrices) == 168
    solutions = []
    for s in matrices:
        if s[0] != 1 or any(apply(s,apply(s,v)) != v for v in range(8)):
            continue
        for t in matrices:
            if t[1] != 2 or any(apply(t,apply(t,v)) != v for v in range(8)):
                continue
            if any(apply(s,apply(t,v)) != apply(t,apply(s,v)) for v in range(8)):
                continue
            for d in range(8):
                if t[0] != (1 ^ d ^ apply(s,d)):
                    continue
                if s[1] != (2 ^ d ^ apply(t,d)):
                    continue
                for f in range(8):
                    if 4 != (1 ^ 2 ^ apply(t,d) ^ f ^ apply(s,apply(t,f))):
                        continue
                    image_s = {apply(s,v) ^ v for v in range(8)}
                    image_t = {apply(t,v) ^ v for v in range(8)}
                    if s == t == identity:
                        coordinate = None
                    else:
                        assert image_s == image_t
                        assert len(image_s) == 2
                        coordinate = next(v for v in image_s if v)
                        assert coordinate in (1,2,4)
                        assert apply(s,coordinate) == coordinate == apply(t,coordinate)
                    solutions.append(dict(S=s,T=t,d=d,f=f,common_image_coordinate=coordinate))
    pairs = sorted({(tuple(q['S']),tuple(q['T'])) for q in solutions})
    assert len(solutions) == 32 and len(pairs) == 4
    return dict(status='PASS',invertible_matrices=168,
                hypothesis_solutions=len(solutions),action_pairs=pairs,
                solutions=solutions,
                scope='Exhaustive finite check of the F2^3 linear lemma only; not the full group-theoretic theorem.')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    result=run()
    root=Path(__file__).resolve().parent
    names=['phase11_abelian_frattini.md',Path(__file__).name]
    result['input_sha256']={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text,end='')


if __name__=='__main__':
    main()
