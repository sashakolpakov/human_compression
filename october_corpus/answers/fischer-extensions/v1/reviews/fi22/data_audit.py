#!/usr/bin/env python3
"""Parse the literal witness without executing it; inspect the actual catalogue route."""
from pathlib import Path
import gzip, hashlib, json, re

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def binding(path):
    b = path.read_bytes()
    return {'path': str(path), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def audit(witness, package=None):
    s = witness.read_text()
    pattern = (r'\s*Fi22r\s*:=\s*\[(.*?)\]\s*;\s*'
               r'Fi22Prime11\s*:=\s*\[\s*\[([\d,\s]+)\],\s*(\d+)\s*\]\s*;\s*'
               r'Fi22Prime13\s*:=\s*\[\s*\[([\d,\s]+)\],\s*(\d+)\s*\]\s*;\s*'
               r'Fi22Type\s*:=\s*\[([\d,\s]+)\]\s*;\s*')
    m = re.fullmatch(pattern, s, re.S)
    need(m is not None, 'witness is not the four declared literal assignments')
    perms = re.split(r'(?<=\))\s*,\s*(?=\()', m[1])
    need(len(perms) == 3, 'not three literal permutations')
    rows = []
    for p in perms:
        p = re.sub(r'\s+', '', p)
        pairs = re.findall(r'\((\d+),(\d+)\)', p)
        need(re.sub(r'\(\d+,\d+\)', '', p).strip() == '', 'nonliteral permutation syntax')
        values = [int(x) for pair in pairs for x in pair]
        need(len(set(values)) == len(values) and min(values) >= 1 and max(values) <= 3510,
             'not disjoint transpositions in the declared degree')
        rows.append({'transpositions': len(pairs), 'moved_points': len(values), 'maximum_point': max(values)})
    need([x['transpositions'] for x in rows] == [1723, 1728, 1728], 'literal counts changed')
    words = [[int(x) for x in m[i].split(',')] for i in (2, 4)]
    need(all(x in [1, 2, 3] for w in words for x in w), 'word index outside marking')
    need([int(x) for x in m[6].split(',')] == [6, 13], 'saved type')
    result = {'status': 'PASS', 'literal_three_involutions': rows, 'no_executable_witness_code': True,
              'word11': words[0], 'word13': words[1]}
    if package is not None:
        raw = gzip.decompress((package/'data/gps34.g.gz').read_bytes())
        need(b'PRIMGRP[3510]' in raw, 'correct data file lacks degree3510')
        result.update({
            'current_route': 'PRIMINDX[3510]=34; loader PRIMGRP[3510][2]; exact group record socle type Spor/Fi(22)/1',
            'additional_loader_index_binding': binding(package/'lib/primitiv.grp'),
            'decompressed_gps34_bytes': len(raw), 'decompressed_gps34_sha256': hashlib.sha256(raw).hexdigest(),
            'scope': 'Named catalogue identity remains retained; this independently confirms the actual corrected record route.'})
    return result

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('--witness', type=Path, required=True)
    p.add_argument('--package', type=Path); p.add_argument('--out', type=Path, required=True)
    a = p.parse_args(); need(not a.out.exists() and not a.out.is_symlink(), 'output exists')
    a.out.write_text(json.dumps(audit(a.witness, a.package), indent=2)+'\n')
