#!/usr/bin/env python3
"""Independent structural audit of the frozen M22 core and a fresh GAP replay.

This checks bindings, output consistency and a separately computed coarse
matching. It does not replace the mathematical review or the exhaustive GAP
algorithm, and never grants a complete refined source-table contract.
"""
import argparse
import copy
import hashlib
import json
import re
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST_SHA = "4c6b9b3432011119f100694dddc28caf14dbac0afd7e67c02d034ffbb0ada6e1"
BRIDGE_SHA = "2f2463b68ab0951bf3a6eff753629e1e7c9f6ee3d772319701ec6c9a745947ab"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def need(test, message):
    if not test:
        raise ValueError(message)


def binding(root, item):
    path = root / item['path']
    need(path.is_file(), 'missing bound file: ' + item['path'])
    need(path.stat().st_size == item['bytes'], 'size mismatch: ' + item['path'])
    need(digest(path) == item['sha256'], 'hash mismatch: ' + item['path'])


def maximum_matching(edges):
    """Unit-capacity integral max flow; independent of the author's DFS matcher."""
    count = len(edges)
    source, sink = 0, 2 * count + 1
    graph = [set() for _ in range(sink + 1)]
    residual = {}

    def add(a, b):
        graph[a].add(b)
        graph[b].add(a)
        residual[a, b] = 1
        residual[b, a] = 0

    for i, neighbors in enumerate(edges, 1):
        add(source, i)
        for witness in set(neighbors):
            need(1 <= witness <= count, 'out-of-range matching witness')
            add(i, count + witness)
    for witness in range(1, count + 1):
        add(count + witness, sink)
    flow = 0
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            a = queue.popleft()
            for b in sorted(graph[a]):
                if b not in parent and residual[a, b]:
                    parent[b] = a
                    queue.append(b)
        if sink not in parent:
            return flow
        b = sink
        while b != source:
            a = parent[b]
            residual[a, b] -= 1
            residual[b, a] += 1
            b = a
        flow += 1


def check_diagnostic(table, shadow, diagnostic):
    rows, witnesses = table['rows'], shadow['triples']
    need(len(rows) == 431 and len(witnesses) == 431, 'wrong table cardinality')
    need([r['row'] for r in rows] == list(range(1, 432)), 'unstable source row IDs')
    need({w['witness'] for w in witnesses} == set(range(1, 432)), 'bad witness IDs')
    numbers = Counter(r['source_number'] for r in rows)
    need({k: v for k, v in numbers.items() if v != 1} == {61: 2}, 'printed duplicate mismatch')
    need(set(range(1, 432)) - set(numbers) == {62}, 'printed omission mismatch')
    need(len(diagnostic['rows']) == 431, 'truncated comparison')
    edges = []
    for row, compared in zip(rows, diagnostic['rows']):
        need(all(row[k] == compared[k] for k in row), 'changed source row')
        match = re.fullmatch(r'M([1-8]{3})\((.*)\)', row['label_text'])
        need(match is not None, 'unparsed source label')
        # Only the leading ordinary intersection sizes are used. Refined
        # subscripts and colon suffixes remain outside this weaker comparison.
        signature = list(map(int, match[1])) + [int(v.strip()[0]) for v in match[2].split(',')]
        actual = sorted(w['witness'] for w in witnesses if signature in w['signatures'])
        need(sorted(set(compared['coarse_candidates'])) == actual, 'wrong coarse candidates')
        need(compared['coarse_signature'] == signature, 'wrong coarse signature')
        compatible = sorted(w['witness'] for w in witnesses
                            if w['witness'] in actual and w['borel_id'][0] == compared['predicted_borel_order'])
        need(sorted(set(compared['order_compatible_candidates'])) == compatible, 'wrong order candidates')
        edges.append(compatible)
    count = maximum_matching(edges)
    need(count == diagnostic['matched'] == 419, 'wrong maximum coarse matching')
    need(sum(not neighbors for neighbors in edges) == 11, 'wrong empty-row count')
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', type=Path, default=ROOT)
    parser.add_argument('--replay-dir', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--check-private-source', action='store_true')
    args = parser.parse_args()
    need(not args.report.exists() and not args.report.is_symlink(), 'refusing existing report')
    root, replay = args.input_dir, args.replay_dir
    manifest_path = root / 'phase164_m22_core_checkpoint01_manifest.json'
    need(digest(manifest_path) == MANIFEST_SHA, 'wrong author checkpoint')
    manifest = json.loads(manifest_path.read_text())
    need(manifest['source_contract_complete'] is False, 'inflated source scope')
    items = manifest['files'] + [manifest['retained_umbrella']]
    if args.check_private_source:
        items.append(manifest['private_source'])
    for item in items:
        binding(root, item)
    need(digest(root / 'phase164_m22_source_bridge.md') == BRIDGE_SHA, 'wrong additive converse')
    run = json.loads((replay / 'replay.json').read_text())
    need(run['status'] == 'PASS_author_replay_not_independent_review', 'failed author replay')
    need(run['source_geometry_inputs'] is False, 'source geometry input')
    need(run['full_source_table_contract_complete'] is False, 'inflated replay scope')
    need(len(run['records']) == 4, 'incomplete replay stages')
    for record, label in zip(run['records'], ['environment', 'census', 'validate', 'shadows']):
        log = replay / (label + '.log')
        need(record['passed'] and record['exit_code'] == 0, 'failed stage: ' + label)
        need(digest(log) == record['log_sha256'], 'changed replay log')
        content = log.read_text()
        need(record['footer'] in content and 'Error,' not in content, 'incomplete stage log')
    for name, expected in run['inputs'].items():
        need(digest(root / name) == expected == digest(replay / name), 'wrong replay program')
    census = (replay / 'census.log').read_text()
    need('OBJECTS 2300 AUT_ORDER 887040' in census, 'wrong maximal/automorphism action')
    need(re.search(r'PAIR_TOTAL TESTED \d+ CLASSES 81\n', census) is not None, 'wrong pair census')
    need('TRIPLE_TOTAL TESTED 11866 ACCEPTED_BEFORE_FUSION 1193 CLASSES 431' in census, 'wrong triple census')
    validation = (replay / 'validate.log').read_text()
    need('WITNESSES_PAIRS 81 TRIPLES 431 THREE_WAY_HELLY 1293 RESIDUE_GENERATION 1293 FIRM_PANELS 1293' in validation, 'wrong witness checks')
    need('SHADOW_FAMILIES [ 22, 77, 176, 176, 330, 231, 616, 1344 ] STEINER_BLOCKS 759 FIVE_SUBSETS 42504 DODECADS 2576' in (replay / 'shadows.log').read_text(), 'wrong Steiner/shadow checks')
    for name, key in [('phase164_m22_witnesses.g', 'witnesses_sha256'), ('phase164_m22_shadow_data.json', 'shadow_data_sha256')]:
        need(digest(replay / name) == run[key] == digest(root / 'phase164_m22_author' / name), 'changed output: ' + name)
    table = json.loads((root / 'phase164_L073_table_contract.json').read_text())
    shadow = json.loads((replay / 'phase164_m22_shadow_data.json').read_text())
    comparison = json.loads((root / 'phase164_m22_coarse_comparison.json').read_text())
    matched = check_diagnostic(table, shadow, comparison)
    controls = []
    mutations = [
        ('deleted_source_row', lambda t, s, c: t['rows'].pop()),
        ('duplicate_witness_ID', lambda t, s, c: s['triples'][0].update(witness=2)),
        ('altered_source_number', lambda t, s, c: t['rows'][0].update(source_number=62)),
        ('inflated_matching', lambda t, s, c: c.update(matched=431)),
        ('invented_matching_edge', lambda t, s, c: c['rows'][53]['order_compatible_candidates'].append(1)),
        ('truncated_comparison', lambda t, s, c: c['rows'].pop()),
    ]
    for name, mutate in mutations:
        t, s, c = copy.deepcopy((table, shadow, comparison))
        mutate(t, s, c)
        try:
            check_diagnostic(t, s, c)
        except ValueError as exc:
            controls.append(dict(name=name, rejected=True, reason=str(exc)))
        else:
            raise ValueError('accepted negative control: ' + name)
    report = dict(status='PASS_independent_structural_review_not_full_source_admission',
                  checkpoint_sha256=MANIFEST_SHA, additive_bridge_sha256=BRIDGE_SHA,
                  bound_files_checked=len(items), private_source_checked=args.check_private_source,
                  replay_report_sha256=digest(replay / 'replay.json'),
                  exact_reproduction_of_frozen_witness_and_shadow_bytes=True,
                  independent_unit_capacity_flow=matched, source_rows=431,
                  controls=controls, refined_source_table_complete=False,
                  lean_verified=False, replacement_ratio=None)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: frozen bindings, fresh replay, independent coarse matching, six negative controls; full table remains unresolved.')


if __name__ == '__main__':
    main()
