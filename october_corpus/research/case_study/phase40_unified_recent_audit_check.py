#!/usr/bin/env python3
"""Independent, read-only integration accounting/binding replay; not a proof checker."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--study', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        ap.error('output already exists; use a fresh output path')
    p = args.study.resolve()
    digest = lambda b: hashlib.sha256(b).hexdigest()
    readj = lambda n: json.loads((p / n).read_text())
    bind = lambda n: {'path': n, 'sha256': digest((p / n).read_bytes()),
                      'bytes': len((p / n).read_bytes())}
    frozen = readj('phase39_compress_unified_freeze.json')
    for n, meta in frozen['files'].items():
        assert bind(n)['sha256'] == meta['sha256'], n
        assert bind(n)['bytes'] == meta['bytes'], n
    contract = readj('phase39_compress_unified_intake.json')
    old_a = readj('phase37_compress_forest_intake.json')
    old_b = readj('phase37_compress_twogroups_manifest.json')
    assert contract['intake_ids'] == ['N001', 'N003', 'N008', 'L032', 'L035', 'F013', 'F016']
    assert contract['source_versions'] == {**old_a['source_versions'], **old_b['source_versions']}
    stable_fields = ['adapter', 'paper', 'source_reference', 'full_source_formulation_normalized',
                     'literal_or_scoped', 'source_statement_reproduced_verbatim',
                     'source_file', 'source_span']
    for former, current in zip(old_a['targets'], contract['targets'][:23]):
        for field in stable_fields:
            assert former[field] == current[field], (current['adapter'], field)
        assert set(former['imported_background_transitive_closure']) <= set(
            current['imported_background_transitive_closure']), current['adapter']
    assert len(old_a['targets']) == 23
    assert contract['complete_N008_numbered_inventory'] == old_a['complete_N008_numbered_inventory']
    ledger_rows = []
    for line in (p / 'phase37_compress_twogroups_ledger.md').read_text().splitlines():
        if re.match(r'^\| (L032 1\.2|L035 1\.[23]|F013 1\.|F016 [567]\.)', line):
            cells = [s.strip() for s in line.strip('|').split('|')]
            ledger_rows.append({'target': cells[0], 'full_normalized_clause': cells[1],
                                'source_specific_proof_cost': cells[3]})
    assert len(ledger_rows) == 17
    assert ledger_rows == contract['B_clause_rows']
    texts = {n: (p / n).read_text() for n in [
        'phase37_compress_forest_manuscript.md',
        'phase37_compress_twogroups_manuscript.md',
        'phase39_compress_unified_manuscript.md']}
    a, b, u = texts.values()
    bodies = {
        'before_A': a[a.index('## Abstract and scope'):a.index('## References and source versions')],
        'before_B': b[b.index('This is a new'):],
        'after_unified': u[u.index('A subgroup kernel'):u.index('## References and exact source versions')],
    }
    accounting = readj('phase39_compress_unified_accounting.json')
    measured = {}
    for key, body in bodies.items():
        measured[key] = {
            'raw_NFC_whitespace_tokens': len(unicodedata.normalize('NFC', body).split()),
            'raw_codepoints': len(body), 'utf8_bytes': len(body.encode()),
            'sha256_utf8': digest(body.encode()),
        }
        assert measured[key] == accounting[key], key
    delta = measured['after_unified']['raw_NFC_whitespace_tokens'] - sum(
        measured[key]['raw_NFC_whitespace_tokens'] for key in ['before_A', 'before_B'])
    assert delta == 706 == accounting['raw_token_delta']
    assert frozen['raw_A_plus_B_tokens'] == 14813
    assert frozen['raw_unified_tokens'] == 15519
    old_app = b[b.index('## Appendix A.'):]
    new_app = u[u.index('## Appendix A.'):u.index('## References and exact source versions')]
    old_code = re.findall(r'```gap\n(.*?)\n```', old_app, re.S)
    new_code = re.findall(r'```gap\n(.*?)\n```', new_app, re.S)
    assert len(old_code) == 1 and new_code == old_code
    assert len(new_code[0].splitlines()) == 41
    assert new_app.index('```gap') < new_app.index('```', new_app.index('```gap') + 3)
    assert u.index('## Appendix A.') < u.index('## References and exact source versions')
    for binding in contract['source_files'] + contract['component_provenance'] + contract['proof_census_costs']:
        assert bind(binding['path'])['sha256'] == binding['sha256'], binding['path']
    assert len(contract['source_files']) == 16
    expected_adapters = ([f'A{i}' for i in range(1, 5)] + [f'B{i}' for i in range(1, 9)]
                         + [f'C{i}' for i in range(1, 12)] + [f'D{i}' for i in range(1, 12)])
    assert [row['adapter'] for row in contract['targets']] == expected_adapters
    for row in contract['targets']:
        for text, span in [((p / row['source_file']).read_text(), row['source_span']),
                           (u, row['replacement_span'])]:
            start, end = span['start_codepoint'], span['end_codepoint_exclusive']
            assert 0 <= start < end <= len(text)
            assert digest(text[start:end].encode()) == span['sha256_utf8'], row['adapter']
    # Replay the author entry point without importing its mutating assembly tools.
    author_run = subprocess.run([sys.executable, str(p / 'phase39_compress_unified_check.py')],
                                capture_output=True, text=True, check=True)
    author_output = json.loads(author_run.stdout)
    assert author_output['status'] == 'PASS_read_only_integrity_not_mathematical_review'
    assert not author_run.stderr
    for n, meta in frozen['files'].items():
        assert bind(n)['sha256'] == meta['sha256'], n
    report = {
        'status': 'PASS_independent_integrity_contract_and_raw_accounting_replay',
        'mathematical_review_is_separate': True,
        'manuscript': bind('phase39_compress_unified_manuscript.md'),
        'intake': bind('phase39_compress_unified_intake.json'),
        'freeze': bind('phase39_compress_unified_freeze.json'),
        'checker': bind(Path(__file__).name),
        'frozen_files_checked_before_and_after': len(frozen['files']),
        'primary_and_support_source_bindings': len(contract['source_files']),
        'source_and_replacement_span_pairs': len(contract['targets']),
        'inherited_A_targets_exact_stable_contract_fields': 23,
        'source_versions_exact': True,
        'inherited_B_clause_rows_exact': 17,
        'N008_numbered_inventory_exact': 10,
        'full_census_code_unchanged_lines': len(new_code[0].splitlines()),
        'census_freshly_rerun': False,
        'fresh_author_readonly_checker': author_output,
        'independent_raw_body_measurements': measured,
        'raw_token_growth': delta,
        'seven_source_factor': None,
        'published': False,
    }
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'output': str(args.output),
                      'sha256': digest(args.output.read_bytes()), 'raw_token_growth': delta}, indent=2))


if __name__ == '__main__':
    main()
