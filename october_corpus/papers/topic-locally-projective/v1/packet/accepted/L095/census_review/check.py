#!/usr/bin/env python3
"""Distinct review replay; shared exact GAP algorithms remain explicit premises."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parent


def need(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def binding(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def bound(base, row):
    rel = Path(row['path'])
    need(not rel.is_absolute() and '..' not in rel.parts, 'relative path')
    path = base / rel
    need(binding(path) == {k: row[k] for k in ['bytes', 'sha256']}, 'changed ' + str(path))
    return path


def documentary(packet, study):
    from pypdf import PdfReader
    spec = read(packet / 'source_bindings.json')
    for row in spec.values():
        bound(study, row)
    pdf = PdfReader(study / spec['L095']['path'])
    compact = lambda text: ''.join(unicodedata.normalize('NFKC', text).split())
    pages = [page.extract_text() or '' for page in pdf.pages]
    rows = read(packet / 'source_tables.json')
    for row in rows:
        fields = [str(row['label']), row['group_literal_extracted'],
                  ', '.join(map(str, row['subgroups'])) if row['subgroups'] else '–',
                  row['facets_literal_extracted'], row['automorphism_literal_extracted']]
        need(compact(' '.join(fields)) in compact(pages[row['physical_page'] - 1]),
             'literal primary row ' + str(row['label']))
    need(len(rows) == 145, 'all source rows')
    return {'source_bindings': len(spec), 'complete_rows': len(rows),
            'page_text_sha256': [hashlib.sha256(x.encode()).hexdigest() for x in pages]}


def graph_check(packet, result):
    census = read(packet / 'evidence/census.json')
    mapping = {int(k): v for k, v in read(packet / 'reconciliation.json')['historical_to_computed'].items()}
    source = {r['label']: r for r in read(packet / 'source_tables.json')}
    groups = {r[0]: r for r in census['survivors']}
    need(set(mapping) == set(range(1, 146)) - {13, 70, 78, 90, 91, 95, 111, 127}, 'exact retained labels')
    need(len(set(mapping.values())) == 137 and set(mapping.values()) == set(groups), 'bijection')
    edges = {(mapping[a], mapping[b]) for a in mapping for b in source[a]['subgroups']}
    need(edges == set(map(tuple, census['maximal_edges'])) and len(edges) == 349, 'all source links')
    reached = set(edges)
    while True:
        enlarged = reached | {(a, d) for a, b in reached for c, d in reached if b == c}
        if enlarged == reached:
            break
        reached = enlarged
    need(len(reached) == 961 and all(a != b for a, b in reached), 'full strict relation')
    need(result['strict_containment_pairs'] == len(reached), 'fresh containment count')
    need(result['cover_edges'] == 349 and result['maxima'] == 26, 'fresh extrema')
    need(len(result['facet_rows']) == len(result['normalizer_orders']) == 137, 'every output row')
    for lab, order, d, h, m in result['facet_rows']:
        need([mapping[lab], order, d, h] == groups[mapping[lab]], 'fresh facet row')
        need(order * (120 * d + 60 * h) == 600415200 and m >= 0, 'facet partition')
    return {'all_source_links': 349, 'strict_pairs': 961, 'complete_facet_rows': 137}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--study-root', type=Path)
    parser.add_argument('--gap', default=shutil.which('gap'))
    args = parser.parse_args()
    need(args.gap is not None and not args.out.exists(), 'GAP and fresh output required')
    args.out.mkdir(parents=True)
    if (ROOT / 'manifest.json').exists():
        for row in read(ROOT / 'manifest.json')['exports']:
            bound(ROOT, row)
    author = read(ROOT / 'review.json')['author_manifest']
    need(binding(args.packet / 'manifest.json') == {k: author[k] for k in ['bytes', 'sha256']}, 'author edition')
    mf = read(args.packet / 'manifest.json')
    for row in mf['exports']:
        bound(args.packet, row)
    doc = documentary(args.packet, args.study_root) if args.study_root else None
    shutil.copytree(args.packet / 'programs', args.out / 'programs')
    shutil.copy2(args.packet / 'evidence/computed_subgroups.g', args.out / 'computed_subgroups.g')
    shutil.copy2(ROOT / 'distinct.g', args.out / 'distinct.g')
    c = read(args.packet / 'evidence/census.json')
    m = read(args.packet / 'reconciliation.json')['historical_to_computed']
    groups = {row[0]: row for row in c['survivors']}
    rows = [[int(k)] + groups[i] for k, i in sorted(m.items(), key=lambda x: int(x[0]))]
    (args.out / 'root_input.g').write_text('rootRows:=' + json.dumps(rows) + ';;\nrootExpectedEdges:=' +
                                         json.dumps(sorted(c['maximal_edges'])) + ';;\n')
    proc = subprocess.run([args.gap, '-q', '-b', '-A', '-r', 'distinct.g'], cwd=args.out,
                          capture_output=True, text=True, timeout=600)
    (args.out / 'gap.stdout').write_text(proc.stdout)
    (args.out / 'gap.stderr').write_text(proc.stderr)
    need(proc.returncode == 0 and 'ROOT_L084_DISTINCT_PASS' in proc.stdout and
         not any(x in proc.stdout + proc.stderr for x in ['Error,', 'Syntax error', 'Syntax warning']), 'GAP replay')
    result = read(args.out / 'root_distinct_result.json')
    need(result == read(ROOT / 'distinct_result.json'), 'exact independent result')
    graph = graph_check(args.packet, result)
    report = {'status': 'PASS', 'author_exports': len(mf['exports']), 'documentary': doc,
              'distinct_graph_and_facets': graph, 'normalizer_orders': 137,
              'formal_declarations': 0, 'shared_computational_premise': 'GAP and the named TomLib model'}
    (args.out / 'report.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'PASS', 'author_exports': len(mf['exports']), **graph}))


if __name__ == '__main__':
    main()
