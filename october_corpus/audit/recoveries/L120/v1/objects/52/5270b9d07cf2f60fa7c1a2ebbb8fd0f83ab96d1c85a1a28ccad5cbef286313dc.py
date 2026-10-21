"""Check all class identifications by solving intertwining constraints.

No author canonicalization or GAP conjugacy routine is imported. For each
possible image of point zero, the marked actions force the entire map.
"""
import ast
import json
from pathlib import Path

P = Path(__file__).resolve().parent
lines = (P / 'fresh01/validation.stdout').read_text().splitlines()
tuples = [tuple(tuple(x-1 for x in g) for g in ast.literal_eval(s.split('|', 1)[1]))
          for s in lines if s.startswith('SOLUTION|')]


def equivalent(a, b):
    if len(a) != len(b):
        return False
    for image0 in range(8):
        mapping = {0: image0}
        pending = [0]
        valid = True
        while pending and valid:
            v = pending.pop()
            for g, h in zip(a, b):
                u, target = g[v], h[mapping[v]]
                if u in mapping:
                    if mapping[u] != target:
                        valid = False
                        break
                else:
                    if target in mapping.values():
                        valid = False
                        break
                    mapping[u] = target
                    pending.append(u)
        if valid:
            if len(mapping) != 8 or len(set(mapping.values())) != 8:
                raise ValueError('Incomplete point bijection')
            if not all(mapping[g[v]] == h[mapping[v]] for g, h in zip(a, b) for v in range(8)):
                raise ValueError('False intertwiner')
            return True
    return False


rows = []
comparisons = 0
for rank in range(3, 8):
    ts = [t for t in tuples if len(t) == rank]
    for i, t in enumerate(ts):
        for j, u in enumerate(ts):
            same = equivalent(t, u)
            comparisons += 1
            if same != (i == j):
                raise ValueError('Repeated or failed class')
    reverse = []
    for t in ts:
        matches = [j for j, u in enumerate(ts) if equivalent(tuple(reversed(t)), u)]
        comparisons += len(ts)
        if len(matches) != 1:
            raise ValueError('Reversal missing or repeated')
        reverse.append(matches[0])
    if not all(reverse[reverse[i]] == i for i in range(len(ts))):
        raise ValueError('Not an involution')
    fixed = sum(i == j for i, j in enumerate(reverse))
    rows.append(dict(rank=rank, ordered=len(ts), fixed=fixed,
                     with_duality=(len(ts)+fixed)//2, reverse=reverse))

expected = json.loads((P / 'fresh01/canonical_report.json').read_text())
for row, answer, maps in zip(rows, expected['rows'], expected['reversal_maps']):
    if row['reverse'] != maps['reversal'] or row['with_duality'] != answer['with_duality']:
        raise ValueError('Independent disagreement')
report = dict(status='PASS_ALL_PAIRWISE_INTERTWINERS', tuples=len(tuples),
              comparisons=comparisons, rows=rows)
(P / 'independent.json').write_text(json.dumps(report, indent=2)+'\n')
print('PASS', comparisons, 'pairwise conjugacy and reversal decisions')
