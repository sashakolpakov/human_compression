#!/usr/bin/env python3
"""Four exact common-fixed-point checks for the compact affine splitting."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from phase35_L003_affine_check import MATRICES, OFFSETS, mv


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite saved evidence')
    origin = (1,0,1,1,0,0)
    expected = [(-1,0,0,0,0,0), (0,0,0,0,0,0),
                (0,0,-1,0,0,0), (0,0,-1,-1,0,0)]
    offsets = []
    for M,b,c in zip(MATRICES,OFFSETS,expected):
        A = tuple(x for row in M for x in row)
        v = tuple(x+y-z for x,y,z in zip(b,mv(A,origin),origin))
        assert v == tuple(2*x for x in c)
        offsets.append(v)
    root = Path(__file__).parent
    report = {
        'status':'PASS',
        'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'matrix_source_sha256':sha256((root/'phase35_L003_affine_check.py').read_bytes()).hexdigest(),
        'retained_compact_report_sha256':sha256((root/'phase35_L003_affine_check.json').read_bytes()).hexdigest(),
        'origin':origin,
        'old_offsets_after_origin_change':offsets,
        'integral_offsets_after_scale2':expected,
        'coordinate_equalities':24,
        'scope':'Literal change-of-origin/scale identities only. The written argument retains the full translation kernel and proves Gamma=Z6 semidirect Q and H_m=C_m6 semidirect Q.'
    }
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PHASE35_AFFINE_SPLIT_PASS')


if __name__ == '__main__':
    main()
