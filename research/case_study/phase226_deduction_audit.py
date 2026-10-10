#!/usr/bin/env python3
"""Independent structural replay of phase219's rank-three deduction records.
This Python check is supplementary; Lean certifies the actual coset semantics.
It imports no author generator or checker and never uses a proposed action
as a premise for an installed edge.
"""
import argparse
import ast
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
AUTHOR_SHA = '0e97c6931e3c0ae67ef9a33c429d1d017a43cc193f10e65101e39b05dd6d8469'


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def expected_relators():
    return [[0, 1] * 11, [0, 2] * 2, [1, 2] * 11] + [
        ([1, 2] * k + [0, 1] * k) * 2 for k in range(1, 11)]


def verify(trace, require_literal=True):
    n, d = trace['nodes'], trace['generators']
    require((n, d) == (1024, 3), 'wrong rank-three dimensions')
    relations, reps = trace['relators'], trace['representatives']
    if require_literal:
        require(relations == expected_relators(), 'source relators differ')
    require(len(reps) == n and reps[0] == [], 'incorrect root or representative count')
    require(all(all(type(s) is int and 0 <= s < d for s in w) for w in reps), 'invalid word')
    proved, transitions = [], {}
    counts = Counter()
    for j, step in enumerate(trace['steps']):
        edge = tuple(step['edge'])
        require(len(edge) == 3 and all(type(x) is int for x in edge), 'invalid edge')
        u, s, v = edge
        require(0 <= u < n and 0 <= v < n and 0 <= s < d, 'out-of-range edge')
        require((u, s) not in transitions, 'duplicate transition')
        kind = step['kind']
        if kind == 'rootLoop':
            require(u == v == 0 and s in (0, 1), 'unjustified subgroup loop')
        elif kind == 'tree':
            require(reps[v] == reps[u] + [s], 'false tree definition')
        elif kind == 'reverse':
            k = step['previous']
            require(type(k) is int and 0 <= k < j, 'forward dependency')
            require(proved[k] == (v, s, u), 'false reverse edge')
        elif kind == 'gap':
            start = step['start']
            require(type(start) is int and 0 <= start < n, 'invalid scan origin')
            def walk(indices):
                at, letters = start, []
                for k in indices:
                    require(type(k) is int and 0 <= k < j, 'unproved scan dependency')
                    a, label, b = proved[k]
                    require(a == at, 'discontinuous scan')
                    at = b
                    letters.append(label)
                return at, letters
            a, prefix = walk(step['forward'])
            b, reversed_suffix = walk(step['backward'])
            require(a == u and b == v, 'wrong gap endpoints')
            suffix = list(reversed(reversed_suffix))
            require(prefix == step['left'] and suffix == step['right'], 'wrong scan words')
            relation = step['relation']
            require(type(relation) is int and 0 <= relation < len(relations), 'unlisted relation')
            require(prefix + [s] + suffix == relations[relation], 'missing relator justification')
        else:
            raise RuntimeError('unknown inference')
        proved.append(edge)
        transitions[u, s] = v
        counts[kind] += 1
    require(set(transitions) == {(u, s) for u in range(n) for s in range(d)}, 'incomplete deductions')
    return dict(nodes=n, transitions=len(proved), inference_counts=dict(counts))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    require(not args.out.exists() and not args.out.is_symlink(), 'fresh output file required')
    require(digest(ROOT / 'phase219_manifest.json') == AUTHOR_SHA, 'changed author freeze')
    manifest = json.loads((ROOT / 'phase219_manifest.json').read_text())
    for row in manifest['exports']:
        p = ROOT / row['path']
        require(p.stat().st_size == row['bytes'] and digest(p) == row['sha256'], 'changed author export')
    trace = json.loads((ROOT / 'phase219_rank3_trace.json').read_text())
    result = verify(trace)
    source = (ROOT / 'phase219_formal/LabelElevenRankThree.lean').read_text()
    actual = next(line.split(':=', 1)[1].strip() for line in source.splitlines()
                  if line.startswith('def relators :'))
    require(ast.literal_eval(actual) == expected_relators(), 'Lean relators differ')
    theorem_rows = re.findall(r'^private theorem edge(\d+) : D (\d+) \[(\d+)\] (\d+) :=', source, re.M)
    require(len(theorem_rows) == len(trace['steps']), 'wrong proof declaration count')
    for j, (index, u, s, v) in enumerate(theorem_rows):
        require(int(index) == j and [int(u), int(s), int(v)] == trace['steps'][j]['edge'],
                'Lean edge declarations differ')
    controls = {}
    for name in ['false_tree', 'unchecked_relator', 'root_loops_only']:
        bad = deepcopy(trace)
        if name == 'false_tree':
            first = next(x for x in bad['steps'] if x['kind'] == 'tree')
            bad['representatives'][first['edge'][2]] = []
        elif name == 'unchecked_relator':
            first = next(x for x in bad['steps'] if x['kind'] == 'gap')
            bad['relators'][first['relation']] = []
        else:
            bad['steps'] = [x for x in bad['steps'] if x['kind'] == 'rootLoop']
        try:
            verify(bad, require_literal=False)
        except RuntimeError as error:
            controls[name] = {'status': 'REJECTED', 'reason': str(error)}
        else:
            raise RuntimeError('negative control was accepted: ' + name)
    result.update(status='PASS', author_manifest_sha256=AUTHOR_SHA,
                  bound_author_exports=len(manifest['exports']), negative_controls=controls,
                  scope='Independent finite syntactic replay only; actual-group semantics are established by the reviewed Lean proofs.')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'transitions': result['transitions'], 'negative_controls': len(controls)}))


if __name__ == '__main__':
    main()
