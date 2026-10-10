"""Read-only binding check for the integrated three-paper review.

This checks provenance and internal references, not mathematical truth or length.
It imports no author binder and refuses to overwrite its output.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output already exists')
    root = args.root
    contract_path = root / 'phase37_compress_forest_intake.json'
    contract = json.loads(contract_path.read_text())
    manuscript_path = root / 'phase37_compress_forest_manuscript.md'
    manuscript = manuscript_path.read_text()
    bindings = {}

    def bind(record):
        data = (root / record['path']).read_bytes()
        assert sha(data) == record['sha256'], record['path']
        if 'bytes' in record:
            assert len(data) == record['bytes'], record['path']
        bindings[record['path']] = sha(data)

    def span(text, record):
        a, b = record['start_codepoint'], record['end_codepoint_exclusive']
        assert 0 <= a < b <= len(text)
        assert sha(text[a:b].encode()) == record['sha256_utf8']
        return text[a:b]

    for record in contract['source_files'] + contract['artifacts'] + contract['integration']['component_audits']:
        bind(record)
    expected = ([f'A{i}' for i in range(1, 5)] +
                [f'B{i}' for i in range(1, 9)] +
                [f'C{i}' for i in range(1, 12)])
    assert [t['adapter'] for t in contract['targets']] == expected
    assert re.findall(r'\*\*Corollary ([ABC]\d+) —', manuscript) == expected
    for target in contract['targets']:
        span((root / target['source_file']).read_text(), target['source_span'])
        replacement = span(manuscript, target['replacement_span'])
        assert replacement.startswith('**Corollary ' + target['adapter'] + ' —')
    inventory = contract['complete_N008_numbered_inventory']
    assert len(inventory) == 10
    n008 = (root / 'sources/phase16_frattini_geometries.txt').read_text()
    for item in inventory:
        span(n008, item['source_anchor'])
    assert [x['adapter'] for x in inventory] == [f'C{i}' for i in range(1, 10)] + [None]
    assert inventory[-1]['source_result'] == 'Theorem 4.1'
    assert 'retained' in inventory[-1]['scope_status']
    tags = re.findall(r'\\tag\{(\d+\.\d+)\}', manuscript)
    assert len(tags) == len(set(tags))
    for target in contract['targets']:
        for number in re.findall(r'equation\s*(\d+\.\d+)', target['common_result']):
            assert number in tags
    by_id = {t['adapter']: t for t in contract['targets']}
    assert '6.7' in by_id['C10']['common_result']
    assert '6.4' in by_id['C11']['common_result']
    assert manuscript.count('**Theorem R (') == 1
    assert manuscript.count('**Lemma E0 (') == 1
    assert contract['integration']['external_required_proof_appendices'] == []
    assert contract['measurement']['manuscript_ratio'] is None
    author_checks = json.loads((root / 'phase37_compress_forest_checks.json').read_text())
    for name, digest in author_checks['hashes'].items():
        bind({'path': name, 'sha256': digest})
    report = {
        'date': '2026-10-10',
        'status': 'PASS',
        'scope': 'Read-only provenance, exact span, equation-reference and declared-contract checks; not a mathematical proof or length measurement.',
        'script_sha256': sha(Path(__file__).read_bytes()),
        'source_file_bindings': len(contract['source_files']),
        'source_and_replacement_target_pairs': len(expected),
        'N008_numbered_source_anchors': len(inventory),
        'unique_equation_tags': len(tags),
        'component_review_bindings': len(contract['integration']['component_audits']),
        'manuscript_ratio': None,
        'bound_sha256': dict(sorted(bindings.items())),
        'author_binders_executed': False,
        'author_or_source_files_modified': False,
    }
    with args.output.open('x') as out:
        json.dump(report, out, ensure_ascii=False, indent=2)
        out.write('\n')
    print(json.dumps({k: report[k] for k in ['status', 'source_file_bindings', 'source_and_replacement_target_pairs', 'N008_numbered_source_anchors']}))


if __name__ == '__main__':
    main()
