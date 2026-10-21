#!/usr/bin/env python3
"""Independent read-only continuity/binding check; never executes an author assembler.

This is not a mathematical proof checker. The accompanying independent review
records the proof assessment. No GAP or Lean execution is performed here.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

P = Path(__file__).resolve().parent
SHA = lambda data: hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--report', type=Path, required=True)
    args = ap.parse_args()
    if args.report.exists():
        ap.error('report exists; refusing to overwrite')
    read = lambda n: (P/n).read_text()
    obj = lambda n: json.loads(read(n))
    verified = {}

    def bind(row):
        name = row['path']
        data = (P/name).read_bytes()
        assert SHA(data) == row['sha256'], name
        if 'bytes' in row:
            assert len(data) == row['bytes'], name
        verified[name] = {'path': name, 'sha256': SHA(data), 'bytes': len(data)}

    for name, sha in {
        'phase45_ten_source_manifest.json': '83fd6dcd563f5cbbd76f431215b3d78ba792db47975796982d03a71a822fb908',
        'phase45_ten_source_errata.json': 'b5aecfb1fbda630fa4d3c8d9cd91258c3f6c98a5f7039efe6daa5beee3d02f6a',
        'phase45_ten_source_errata.md': 'bad11f9a405d30cbdefdb0a04eb7750e650e6f1016cf70b805db2a96fcee05aa',
    }.items():
        bind({'path': name, 'sha256': sha})
    freeze = obj('phase45_ten_source_manifest.json')
    for row in freeze['files']:
        bind(row)
    contract = obj('phase45_ten_source_adapter_map.json')
    for row in contract['component_bindings']:
        bind(row)
    unified = obj('phase39_compress_unified_intake.json')
    operations = obj('phase40_compress_operations_intake.json')
    cover = obj('phase41_chiral_cover_intake.json')
    for row in unified['source_files'] + operations['source_bindings']:
        bind(row)
    for name in ['phase41_chiral_cover_source_web.txt', 'phase41_chiral_cover_tight_excerpts_web.txt']:
        row = obj('phase41_chiral_cover_manifest.json')['files'][name]
        bind(dict(path=name, **row))
    assert contract['source_versions']['Unified'] == unified['source_versions']
    assert contract['source_versions']['Operations'] == operations['sources']
    assert contract['source_versions']['N016'] == cover['target']
    assert contract['detailed_two_group_clause_rows'] == unified['B_clause_rows']
    assert contract['complete_N008_numbered_inventory'] == unified['complete_N008_numbered_inventory']
    assert contract['retained_background']['Unified'] == unified['retained_background']
    assert contract['retained_background']['Operations'] == operations['sources']
    ledger = read('phase41_chiral_cover_ledger.md')
    inventory = ledger.split('## Dependency inventory', 1)[1].split('## Source acquisition and reading limits', 1)[0]
    assert contract['retained_background']['N016_verbatim_inventory'] == inventory
    assert len(contract['contracts']) == 79
    rows = contract['contracts']
    permitted_changes = {'imported_background_transitive_closure', 'mathematical_status', 'replacement_span', 'replacement_file'}
    for old, new in zip(unified['targets'], rows[:34]):
        assert new['integration_id'] == 'U.' + old['adapter']
        assert {k for k in old if old[k] != new.get(k)} == permitted_changes
        assert new['full_dependency_closure_certified'] is False
        source = read(new['source_file'])
        span = new['source_span']
        assert SHA(source[span['start_codepoint']:span['end_codepoint_exclusive']].encode()) == span['sha256_utf8']
    old_operations = obj('phase40_compress_operations_ledger.json')['rows']
    assert len(old_operations) == 27
    for old, new in zip(old_operations, rows[34:61]):
        assert new['integration_id'] == 'O.' + old['id']
        assert all(new.get(k) == v for k, v in old.items())
    cover_table = ledger.split('## Exact target contract', 1)[1].split('The claim is coverage', 1)[0]
    cover_rows = [[c.strip() for c in line.strip().strip('|').split('|')]
                  for line in cover_table.splitlines() if line.startswith('|')][2:]
    assert len(cover_rows) == 18
    for i, (old, new) in enumerate(zip(cover_rows, rows[61:]), 1):
        assert new['integration_id'] == f'COV.{i}'
        assert [new[k] for k in ['source_reference', 'full_source_formulation_normalized',
                                'component_proof_location_and_cost', 'component_status']] == old
    manuscript = read('phase45_ten_source_manuscript.md')
    proof_spans = 0
    for row in rows:
        for key in ['integrated_proof_span', 'additional_full_proof_span']:
            if key in row:
                span = row[key]
                fragment = manuscript[span['start_codepoint']:span['end_codepoint_exclusive']]
                assert SHA(fragment.encode()) == span['sha256_utf8'], (row['integration_id'], key)
                proof_spans += 1
    for adapter in ['O.N8', 'O.N12']:
        row = next(r for r in rows if r['integration_id'] == adapter)
        assert row['proposed_dependency_delta']['retained_background_removal_now_proved'] is True
    assert all('Unproved; not counted' == row['component_status'] for row in rows[-2:])

    def sections(text):
        matches = list(re.finditer(r'^## (\d+)\.', text, re.M))
        return {int(m[1]): text[m.start():matches[i+1].start() if i+1 < len(matches) else len(text)]
                for i, m in enumerate(matches)}

    old_sections = sections(read('phase39_compress_unified_manuscript.md'))
    new_sections = sections(manuscript)
    unchanged = list(range(3, 9)) + list(range(10, 16))
    assert all(old_sections[i] == new_sections[i] for i in unchanged)
    assert new_sections[9].startswith(old_sections[9])
    assert list(new_sections) == list(range(1, 25))
    erratum = obj('phase45_ten_source_errata.json')
    assert erratum['manuscript_sha256'] == SHA(manuscript.encode())
    for change in erratum['changes']:
        assert manuscript.count(change['old']) == 1
        assert change['new'] in read('phase45_ten_source_errata.md')
    programs = [
        'phase37_compress_twogroups_census.g',
        'phase40_compress_operations_check.g',
        'phase40_compress_operations_exhaustive.g',
        'phase41_chiral_cover_check.g',
    ]
    expected = [
        '0a1e993362b263c9ef23e8fca5103c3a2b766a937a2f9af7608fbca8252d2752',
        'f1d49b61e210e0026468a2bcb2621399e5fda10778893fd1c20d364019f54810',
        'bfe4190665e751a3c65d00fd692ae0a6059d25f6345fd11f0efdc5a5a938c952',
        '59bf1cd96626df42e1e1baed82b88538416f336443c1a4076dfbb5f09bdcc69e',
    ]
    blocks = re.findall(r'```gap\n(.*?)\n```', manuscript, re.S)
    assert len(blocks) == 4
    code_rows = []
    for name, sha, block in zip(programs, expected, blocks):
        data = (block.rstrip() + '\n').encode()
        assert SHA(data) == sha
        assert (P/name).read_bytes() == data
        bind({'path': name, 'sha256': sha})
        code_rows.append({'path': name, 'sha256': sha, 'bytes': len(data), 'fresh_execution_here': False})
    report = {
        'status': 'PASS',
        'mathematical_proof_checker': False,
        'source_versions_equal_to_component_contracts': True,
        'source_contract_rows_preserved': {'Unified': 34, 'Operations': 27, 'N016': 18},
        'qualification_rows_are_not_all_proved_theorems': True,
        'additional_two_group_clause_rows': 17,
        'N008_complete_numbered_inventory': 10,
        'integrated_proof_spans_checked': proof_spans,
        'byte_identical_unified_sections': unchanged,
        'original_square_section_is_exact_prefix': True,
        'required_additive_namespace_erratum_occurrences': 1,
        'complete_programs': code_rows,
        'embedded_program_bytes_charged_once': sum(r['bytes'] for r in code_rows),
        'whole_markdown_bytes_including_all_frontmatter_references_and_code': len(manuscript.encode()),
        'whole_markdown_raw_whitespace_units_not_common_PDF_tokens': len(manuscript.split()),
        'quantitative_ten_source_factor': None,
        'GAP_or_Lean_executed': False,
        'bindings': [verified[k] for k in sorted(verified)],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open('x') as stream:
        stream.write(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'bindings'}, indent=2))


if __name__ == '__main__':
    main()
