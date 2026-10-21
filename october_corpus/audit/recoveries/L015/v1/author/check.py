#!/usr/bin/env python3
"""Portable binding/scope/native replay; not a check of the written proof."""
import argparse
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def bound(path, binding):
    data = path.read_bytes()
    require(len(data) == binding['bytes'] and digest(data) == binding['sha256'],
            'binding: ' + str(path))


def semantics(scope, contract, docs, inventory, dependencies):
    require(scope['source_id'] == 'L015' and scope['fixed_source_pages'] == 14,
            'fixed source')
    require(scope['source_rows'] == 45 == len(contract['rows']), 'source routes')
    rows = {r['id']: r for r in contract['rows']}
    require(len(rows) == 45, 'unique route IDs')
    wanted = {
        'T3.2.Generation': 'REFUTED_EXACT_WRITTEN_COUNTEREXAMPLE',
        'C3.5': 'REFUTED_EXACT_WRITTEN_COUNTEREXAMPLE',
        'C3.7.Universal': 'REFUTED_AMBIENT_GENERATION_PART',
        'T3.14.RC': 'REFUTED_AS_PRINTED_AND_REPAIRED',
        'T3.16': 'RECOVERED_CORRECTED_PRINCIPAL_THEOREM',
        'C3.7.Existential': 'RECOVERED_CORRECTED_UNIFORM_PROOF',
        'T2.5': 'RETAINED_WITH_CONVENTION_REPAIR',
        'Introduction.Sz8Counts': 'RETAINED_HISTORICAL_NOT_PREMISE',
    }
    require(all(rows[k]['disposition'] == v for k, v in wanted.items()),
            'corrected and retained scope')
    for name in ['required_mathematical_programs', 'required_stored_mathematical_data',
                 'formal_files', 'new_lean_declarations', 'new_conjecture_credit',
                 'new_original_credit']:
        require(scope[name] == 0, 'unsupported credit/premise: ' + name)
    require(scope['optional_validation_programs'] == scope['operational_drivers'] == 1,
            'whole code roles')
    require(not scope['literal_theorem_set_equivalence'] and
            not contract['literal_theorem_set_equivalence'] and
            not scope['general_m_coset_flag_transitivity'], 'overstated theorem scope')
    require(all(scope[k] is None for k in ['measurement_factors',
                'retained_external_proof_cost', 'source_software_cost']), 'unknown cost')
    require([x['pages'] for x in docs['documents']] == [4, 6, 4] and
            docs['total_pages'] == 14 and docs['all_whole_documents_charged'],
            'complete document closure')
    require([x['tex'] for x in docs['documents']] ==
            ['uniform_generation.tex', 'suzuki_triality_application.tex',
             'dependencies/triality_coordinates.tex'], 'native routes')
    require({x['path']: x['role'] for x in inventory['files']} ==
            {'optional_checks.py': 'OPTIONAL_BOUNDED_VALIDATION',
             'check.py': 'OPERATIONAL_BINDING_SCOPE_RENDER'}, 'program roles')
    require(all(x['whole_file'] for x in inventory['files']) and
            inventory['required_program_count'] == inventory['required_math_data_count'] == 0,
            'required software boundary')
    require(inventory['source_software_cost'] is None and
            inventory['software_inclusive_factor'] is None, 'software symmetry')
    require(len(dependencies['whole_written_premises']) == 1 and
            dependencies['whole_written_premises'][0]['pages'] == 4 and
            dependencies['source']['sha256'] ==
            '627439f5c866001bcaa12add9599f3b60c2a18d53677b5585703111c055df3cc',
            'exact source/common dependency')


def controls(args):
    cases = []
    def reject(name, which, action):
        altered = copy.deepcopy(args)
        action(altered[which])
        try:
            semantics(*altered)
        except (ValueError, KeyError):
            cases.append(name)
        else:
            raise ValueError('control accepted: ' + name)
    reject('drop source row', 1, lambda x: x['rows'].pop())
    reject('restore false universal generation', 1,
           lambda x: next(r for r in x['rows'] if r['id'] == 'T3.2.Generation')
           .update(disposition='RECOVERED_UNQUALIFIED'))
    reject('restore false ambient connectivity', 1,
           lambda x: next(r for r in x['rows'] if r['id'] == 'T3.14.RC')
           .update(disposition='RECOVERED_UNQUALIFIED'))
    reject('invent finite premise', 0, lambda x: x.update(required_mathematical_programs=1))
    reject('free inherited common', 2, lambda x: x['documents'][2].update(pages=0))
    reject('universal theorem equivalence', 0, lambda x: x.update(literal_theorem_set_equivalence=True))
    reject('general m flag-transitivity', 0, lambda x: x.update(general_m_coset_flag_transitivity=True))
    reject('unknown software made zero', 0, lambda x: x.update(source_software_cost=0))
    reject('asymmetric software factor', 3, lambda x: x.update(software_inclusive_factor=1.0))
    reject('optional code made premise', 3,
           lambda x: x['files'][0].update(role='REQUIRED_PROOF'))
    reject('invent original credit', 0, lambda x: x.update(new_original_credit=1))
    reject('wrong primary edition', 4, lambda x: x['source'].update(sha256='0' * 64))
    return cases


def run(args):
    started = time.monotonic()
    out = args.out.resolve()
    require(not out.exists(), 'output must be fresh')
    out.mkdir(parents=True)
    manifest = read('manifest.json')
    for item in manifest['exports']:
        bound(ROOT / item['path'], item)
    scope, contract, docs, inventory, dependencies = [read(x) for x in
        ['scope.json', 'source_contract.json', 'native_documents.json',
         'program_inventory.json', 'dependencies.json']]
    semantic_args = [scope, contract, docs, inventory, dependencies]
    semantics(*semantic_args)
    negative = controls(semantic_args)
    for item in inventory['files']:
        bound(ROOT / item['path'], item)
    whole = dependencies['whole_written_premises'][0]
    for local, kind in zip(whole['copies'], ('tex', 'pdf')):
        bound(ROOT / local, whole[kind])
    external = 0
    if args.study_root:
        bindings = [dependencies['source'], dependencies['source_text_private']]
        bindings += dependencies['prior_bindings'] + dependencies['coordinate_primary']
        bindings += [whole['tex'], whole['pdf']]
        for item in bindings:
            bound(args.study_root / item['path'], item)
        external = len(bindings)
    for item in read('proof_contexts.json')['contexts']:
        tex = (ROOT / item['file']).read_text()
        start = tex.index('\\section{' + item['section'] + '}')
        match = re.search(r'\\section\{', tex[start + 1:])
        end = start + 1 + match.start() if match else tex.index('\\end{document}')
        require(digest(tex[start:end].encode()) == item['sha256'], 'proof context')
    native = []
    if args.render:
        for doc in docs['documents']:
            target = out / Path(doc['tex']).stem
            target.mkdir()
            tex = target / Path(doc['tex']).name
            shutil.copyfile(ROOT / doc['tex'], tex)
            for passno in range(2):
                command = [args.pdflatex, '-interaction=nonstopmode', '-halt-on-error', tex.name]
                result = subprocess.run(command, cwd=target, capture_output=True, text=True,
                                        timeout=90, check=False)
                (target / ('render%d.stdout' % passno)).write_text(result.stdout)
                require(result.returncode == 0, 'native compiler ' + doc['id'])
            log = (target / (tex.stem + '.log')).read_text(errors='replace')
            require(not re.search(r'Overfull|Underfull|LaTeX Warning|Package .* Warning', log),
                    'native diagnostics ' + doc['id'])
            pdf = target / (tex.stem + '.pdf')
            texts = [(p.extract_text() or '') for p in PdfReader(pdf).pages]
            require(len(texts) == doc['pages'] and
                    [digest(t.encode()) for t in texts] == doc['page_text_sha256'],
                    'exact native page text ' + doc['id'])
            native.append({'id': doc['id'], 'pages': len(texts), 'exact_text': True})
    optional = None
    if args.optional:
        dest = out / 'optional.json'
        result = subprocess.run([sys.executable, '-B', '-O', str(ROOT / 'optional_checks.py'),
                                 '--out', str(dest)], capture_output=True, text=True,
                                timeout=60, check=False)
        (out / 'optional.stdout').write_text(result.stdout)
        require(result.returncode == 0, 'optional diagnostic')
        optional = json.loads(dest.read_text())
        require(optional == read('optional_report.json'), 'exact optional report')
    report = {'status': 'PASS_BINDINGS_SCOPE_NATIVE_OPTIONAL_AS_REQUESTED',
              'manifest_sha256': digest((ROOT / 'manifest.json').read_bytes()),
              'exports': len(manifest['exports']), 'source_rows': len(contract['rows']),
              'whole_common_copies': 2, 'external_bindings': external,
              'semantic_negative_controls': negative, 'native_documents': native,
              'optional': optional, 'written_proof_checked_by_this_program': False,
              'elapsed_seconds': round(time.monotonic() - started, 3)}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--study-root', type=Path)
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--optional', action='store_true')
    parser.add_argument('--pdflatex', default='/opt/homebrew/bin/pdflatex')
    run(parser.parse_args())
