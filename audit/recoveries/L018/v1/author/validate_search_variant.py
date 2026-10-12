#!/usr/bin/env python3
"""Independent cell-cover oracle and positive congruence-relaxed controls.

No complete large census claim. The literal target forbids repeated shapes;
positive controls deliberately relax that rule and their witnesses must fail
only the original noncongruence requirement.
"""
import argparse, json, math, subprocess, tempfile, time, hashlib
from pathlib import Path

def grid_oracle(w, h, r, seconds=2):
    if w * h % r:
        return {'status': 'INFEASIBLE', 'nodes': 0}
    a = w * h // r
    shapes = [(d, a // d) for d in range(1, math.isqrt(a) + 1) if a % d == 0 and (d <= w and a // d <= h or (d <= h and a // d <= w))]
    full = (1 << w * h) - 1
    nodes = 0
    start = time.monotonic()

    def rec(occ, used, depth):
        nonlocal nodes
        nodes += 1
        if nodes % 1024 == 0 and time.monotonic() - start > seconds:
            raise TimeoutError
        if depth == r:
            return occ == full
        free = full ^ occ
        first = (free & -free).bit_length() - 1
        y, x = divmod(first, w)
        for si, (a, b) in enumerate(shapes):
            if used >> si & 1:
                continue
            for wi, hi in set(((a, b), (b, a))):
                if x + wi > w or y + hi > h:
                    continue
                mask = sum(((1 << wi) - 1 << xx * w + x for xx in range(y, y + hi)))
                if mask & occ:
                    continue
                if rec(occ | mask, used | 1 << si, depth + 1):
                    return True
        return False
    try:
        s = 'FEASIBLE' if rec(0, 0, 0) else 'INFEASIBLE'
    except TimeoutError:
        s = 'UNKNOWN'
    return {'status': s, 'nodes': nodes, 'seconds': time.monotonic() - start}

def check_placement(d, distinct):
    w, h, r = (d['width'], d['height'], d['pieces'])
    p = d['placement']
    if not len(p) == r:
        raise AssertionError('validation condition failed')
    area = w * h // r
    for _, x, y, wi, hi in p:
        if not (min(wi, hi) > 0 and min(x, y) >= 0 and (x + wi <= w) and (y + hi <= h) and (wi * hi == area)):
            raise AssertionError('validation condition failed')
    for i, (_, x, y, wi, hi) in enumerate(p):
        for _, xx, yy, ww, hh in p[:i]:
            if not (x + wi <= xx or xx + ww <= x or y + hi <= yy or (yy + hh <= y)):
                raise AssertionError('validation condition failed')
    if distinct:
        if not len({tuple(sorted(z[3:])) for z in p}) == r:
            raise AssertionError('validation condition failed')
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--cpp', type=Path, required=True)
    p.add_argument('--binary', required=True)
    a = p.parse_args()
    a.out.mkdir()
    rows = json.loads(Path('arithmetic_candidates.json').read_text())['rectangle_candidates']
    cases = [(z['width'], z['height'], z['pieces']) for z in rows if z['width'] <= 120][::max(1, len([z for z in rows if z['width'] <= 120]) // 25)]
    exact = []
    for w, h, r in cases:
        q = grid_oracle(w, h, r)
        d = json.loads(subprocess.check_output([a.binary, str(w), str(h), str(r), '2'], text=True))
        if not (q['status'] == 'UNKNOWN' or d['status'] == 'UNKNOWN' or q['status'] == d['status']):
            raise AssertionError('validation condition failed')
        exact.append({'width': w, 'height': h, 'pieces': r, 'cell_oracle': q, 'skyline': d})
    s = a.cpp.read_text()
    needle = 'if(S.size()>63)return 4;'
    if not needle in s:
        raise AssertionError('validation condition failed')
    s = s.replace(needle, '{auto original=S;S.clear();for(int i=0;i<R;++i)S.insert(S.end(),original.begin(),original.end());}' + needle)
    src = a.out / 'allow_repetitions.cpp'
    src.write_text(s)
    exe = a.out / 'allow_repetitions'
    subprocess.run(['clang++', '-O3', '-std=c++17', '-include', 'array', str(src), '-o', str(exe)], check=True)
    positive = []
    for w, h, r in [(4, 4, 4), (6, 4, 6), (8, 6, 12), (10, 6, 10), (6, 6, 9)]:
        d = json.loads(subprocess.check_output([str(exe), str(w), str(h), str(r), '5'], text=True))
        if not d['status'] == 'FEASIBLE':
            raise AssertionError('validation condition failed')
        check_placement(d, False)
        try:
            check_placement(d, True)
        except AssertionError:
            pass
        else:
            raise AssertionError('Repeated shapes should violate target')
        positive.append(d)
    report = {'status': 'PASS_BOUNDED_METHOD_CHECKS', 'grid_comparisons': exact, 'congruence_relaxed_positive_controls': positive, 'source_sha256': hashlib.sha256(a.cpp.read_bytes()).hexdigest(), 'scope': 'Small independent cell-cover comparisons and five deliberately relaxed positive tilings; no independent human review or large-census claim.'}
    (a.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(len(exact), len(positive))
