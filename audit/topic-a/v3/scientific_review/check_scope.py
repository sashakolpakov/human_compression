#!/usr/bin/env python3
"""Independent preservation checks for the proposed A/affine consolidation.

This checks the review boundary, not mathematical truth. No author checker is
imported, no old scientific program is rerun, and no length factor is computed.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def need(condition, message):
    if not condition:
        raise ValueError(message)


def bound(root, row):
    path = Path(row['path'])
    need(not path.is_absolute() and '..' not in path.parts, 'relative path')
    data = (root / path).read_bytes()
    need(len(data) == row['bytes'] and digest(data) == row['sha256'], str(path))
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--public', type=Path, required=True)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists(), 'fresh output required')
    root = args.candidate
    manifest = read(root / 'manifest.json')
    need(digest((root / 'manifest.json').read_bytes()) ==
         '3a51b6f9ddd668f710bc8e91806eb3e896f9e382ccd8c5b2043434cb9c5c4e4d',
         'reviewed candidate edition')
    paths = [row['path'] for row in manifest['exports']]
    need(len(set(paths)) == len(paths) == 119, 'complete export roster')
    for row in manifest['exports']:
        bound(root, row)
    need(sum(row['bytes'] for row in manifest['exports']) == 1987950,
         'whole export bytes')

    inherited = sum((read(root / name)['files'] for name in
                     ['inherited_files.json', 'additional_inherited_files.json']), [])
    need(len(inherited) == 87, 'all admitted predecessor inputs')
    changed = []
    for row in inherited:
        old = (args.public / row['source']).read_bytes()
        need(len(old) == row['bytes'] and digest(old) == row['sha256'],
             'bound public predecessor ' + row['source'])
        current = (root / row['target']).read_bytes()
        if current != old:
            changed.append(row['target'])
    migration = read(root / 'migration.json')
    need(set(changed) == {row['current']['path'] for row in
                         migration['changed_inherited_files']}, 'complete change roster')

    contracts = read(root / 'source_contract_map.json')
    originals = []
    for filename, key in [
        ('prior/audit/topic-a/v2/stage_U_A1_A4_map.json', 'rows'),
        ('prior/audit/topic-a/v2/A5_A6_coverage.json', 'coverage_rows'),
        ('prior/papers/topic-a/extensions/diagram-symmetries/v1/source_clause_map.json', 'rows'),
        ('prior/papers/topic-affine/v2/scope.json', 'source_rows'),
    ]:
        originals.extend(read(root / filename)[key])
    need(len(originals) == 102 and originals ==
         [row['inherited_record'] for row in contracts['rows']],
         'literal source dispositions and qualifications')
    for row in contracts['rows']:
        need(row['contract_changed'] is False and row['current_span_ids'],
             'unchanged routed contract ' + row['id'])
        need(all(sid in contracts['proof_spans'] for sid in row['current_span_ids']),
             'defined proof contexts')
    need(len(contracts['proof_spans']) == 60, 'all inclusive contexts')
    for row in contracts['proof_spans'].values():
        data = (root / row['path']).read_bytes()
        left, right = row['start_byte'], row['end_byte_exclusive']
        need(0 <= left < right <= len(data) and
             digest(data[left:right]) == row['span_sha256'], 'actual context bytes')
    source_ids = ['L032', 'L034', 'F016', 'F013', 'L035', 'N009', 'L128', 'L012']
    need(contracts['source_ids'] == source_ids, 'all eight source identities')
    for row in contracts['source_bindings'].values():
        bound(args.study, row if 'path' in row else row['pdf'])

    programs = read(root / 'program_inventory.json')
    need(len(programs['required_complete_files']) == 11, 'whole required software')
    need(len(programs['auxiliary_files']) == 3, 'whole auxiliary roster')
    for row in programs['required_complete_files'] + programs['auxiliary_files']:
        bound(root, row)
        need(row['path'] not in changed, 'scientific code unchanged')
    formal = read(root / 'formal_scope.json')
    need(len(formal['modules']) == 14, 'whole inherited formal roster')
    for row in formal['modules']:
        bound(root, row['current'])
        need(row['current']['path'] not in changed and row['unchanged'] is True,
             'unchanged formal bytes')
    need(formal['new_declarations'] == 0 and not formal['whole_volume_formalized']
         and not formal['arbitrary_parabolic_theorem_formalized'], 'formal limits')

    # The paper assembly must not import a previous common paper for free.
    scope = read(root / 'scope.json')
    closure = set()
    def include(path):
        need(path.is_file(), 'included TeX exists ' + str(path))
        relative = path.relative_to(root).as_posix()
        if relative in closure:
            return
        closure.add(relative)
        for target in re.findall(r'\\input\{([^}]+)\}', path.read_text()):
            need(not target.startswith('/') and '..' not in Path(target).parts,
                 'internal TeX dependency')
            include(root / (target if target.endswith('.tex') else target + '.tex'))
    pages = 0
    for row in scope['science_documents']:
        include(root / row['tex']['path'])
        pdf = PdfReader(root / row['pdf']['path'])
        need(len(pdf.pages) == row['pages'], 'whole rendered document page count')
        pages += len(pdf.pages)
    need(pages == 98, 'complete document boundary')
    for row in contracts['whole_common'].values():
        bound(root, row)
        need(row['path'] in closure, 'common proof included in assembly')

    # Reuse old appendix layout evidence only after checking actual page streams.
    visual = read(root / 'author_visual_review.json')
    appendix_pages = 0
    for row in visual['reused_complete_appendix_visual_reviews']:
        current = PdfReader(root / row['current']['path'])
        previous = PdfReader(args.public / row['public_predecessor']['path'])
        need(len(current.pages) == len(previous.pages) == row['pages'], 'appendix pages')
        for a, b in zip(current.pages, previous.pages):
            need(a.get_contents().get_data() == b.get_contents().get_data(),
                 'unchanged decoded appendix page')
            need(a.extract_text() == b.extract_text(), 'unchanged appendix text')
        appendix_pages += row['pages']
    need(appendix_pages == 29, 'complete unchanged appendix layout boundary')

    viewed = []
    for index in [1, 2, 3, 4, 5, 6, 15, 16, 17, 18]:
        row = visual['contact_sheets'][index - 1]
        need(digest(Path(row['path']).read_bytes()) == row['sha256'],
             'actual directly viewed sheet')
        viewed.extend(row['pages'])
    need(len(set(viewed)) == 37, 'actual root visual scope')

    report = {
        'status': 'PASS_INDEPENDENT_SCOPE_AND_PRESERVATION',
        'candidate_manifest_sha256': digest((root / 'manifest.json').read_bytes()),
        'candidate_exports': 119, 'candidate_export_bytes': 1987950,
        'public_predecessor_bindings': 87, 'unchanged_inherited_files': 87 - len(changed),
        'changed_inherited_files': changed, 'primary_source_bindings': 8,
        'literal_source_dispositions': 102, 'inclusive_proof_contexts': 60,
        'contexts_are_disjoint_cost_partition': False,
        'required_complete_program_data_files': 11, 'auxiliary_files': 3,
        'unchanged_formal_modules': 14, 'complete_pdf_pages': pages,
        'tex_input_closure': sorted(closure),
        'root_direct_visual_pages': sorted(viewed),
        'unchanged_appendix_layout_pages': appendix_pages,
        'new_source_credit': 0, 'new_question_credit': 0, 'new_formal_credit': 0,
        'ratio': None, 'author_code_imported': False,
        'scientific_programs_or_Lean_reexecuted': False,
        'mathematical_acceptance': 'Separate human-readable reasoning in review.json',
    }
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(report['status'])


if __name__ == '__main__':
    main()
