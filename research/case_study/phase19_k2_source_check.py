"""Compare factual census counts with the excess-two formulas.

Obtain Conder's primary source independently; it is not distributed here.
This parses record headers only and does not execute source presentations.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

URL = ('https://www.math.auckland.ac.nz/~conder/'
       'RegularPolytopesWithFewFlags-ByOrder.txt')
HEADER = re.compile(r'Regular (\d+)-polytope with group of order (\d+)'
                    r'\s+(NSD|SD)\s+Type \[ (.*?) \]')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = args.source.read_bytes()
    records = []
    for lineno, line in enumerate(raw.decode().splitlines(), 1):
        match = HEADER.fullmatch(line.strip())
        if match:
            rank, order = int(match[1]), int(match[2])
            if (rank, order) in {(3, 128), (4, 512)}:
                records.append((lineno, rank, order, match[3],
                                tuple(map(int, match[4].split(',')))))
    cases = []
    for d in (3, 4):
        selected = [r for r in records if r[1] == d]
        assert selected
        counts = Counter()
        for _, _, _, duality, typ in selected:
            counts[typ] += 1
            if duality == 'NSD':
                counts[typ[::-1]] += 1
        categories = Counter()
        for typ, count in counts.items():
            if all(x == 4 for x in typ):
                category = 'all_four'
            elif sorted(typ) == sorted([8] + [4]*(d-2)):
                category = 'one_eight'
            elif sorted(typ) == sorted([8, 8] + [4]*(d-3)):
                category = 'two_eights'
            elif sorted(typ) == sorted([16] + [4]*(d-2)):
                category = 'one_sixteen'
            else:
                raise AssertionError(('Unexpected type', typ))
            categories[category] += count
        expected = {'all_four': (d-1)*(d-2)//2,
                    'one_eight': 4*(d-2)**2,
                    'two_eights': 8*d*d-40*d+52,
                    'one_sixteen': 4*d-8}
        assert categories == expected
        assert sum(counts.values()) == (25*d*d-107*d+122)//2
        cases.append({
            'rank': d, 'order': 2**(2*d+1),
            'source_records_up_to_duality': len(selected),
            'self_dual_records': sum(r[3] == 'SD' for r in selected),
            'ordered_marked_count': sum(counts.values()),
            'type_counts': [{'type': typ, 'count': count}
                           for typ, count in sorted(counts.items())],
            'aggregated_counts': dict(categories),
            'local_source_line_range': [selected[0][0], selected[-1][0]],
            'status': 'PASS',
        })
    report = {
        'status': 'PASS', 'source_url': URL,
        'source_attribution': 'Marston Conder, author census, June 2012',
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_scope': 'Nondegenerate regular polytopes with at most 2000 flags, up to isomorphism and duality; SD/NSD flags expand to ordered markings.',
        'comparison_scope': 'Counts and type multiplicities only; no row-level presentation identification, classification proof or publication-priority claim.',
        'rank_five_boundary': 'Excess-two rank-five order2048 exceeds this source limit and is not compared.',
        'cases': cases,
    }
    text = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
