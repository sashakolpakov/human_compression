"""Check the O'Nan source completion and preserve the published predecessor.

This checks publication integrity and a previously acquired portable replay.
Run check.py separately for a new mathematical composition/arithmetic replay.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
import ast
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

BASELINE = 'b0f975b4e8e5c4ab1562cc68bcb6356ac2efa175'
DATA = 'data/onan_regular_maps/'
ADMISSION = DATA + 'admission.json'
REGISTRATION = DATA + 'registration.json'
PUBLICATION = 'provenance/publication_manifest.json'
SYNTHESIS = '27238130dda9fb1d8a0343e1602dc7ecbe7eb1ee6398d42d680e6a410487e8eb'
MATH_REVIEW = 'fa03e55dd19c4712062ffe106972d3b9ce094be7227af52614b2770ff154cdf1'
MODIFIED = {'README.rst', 'audit/corpus/latest.json', 'papers/latest_catalogue.json',
            'papers/catalogue.json', 'scripts/verify_snapshot.py', PUBLICATION}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def old_bytes(root, name):
    return git(root, 'show', BASELINE + ':' + name)


def load(path):
    return json.loads(path.read_text())


def safe(root, name):
    p = PurePosixPath(name)
    need(not p.is_absolute() and p.parts and '..' not in p.parts and str(p) == name,
         'Literal repository-relative path')
    q = root.joinpath(*p.parts)
    need(q.resolve() == q and q.is_file(), 'Regular canonical file: ' + name)
    return q


def pin(root, name):
    p = safe(root, name)
    h = hashlib.sha256()
    with p.open('rb') as stream:
        for chunk in iter(lambda: stream.read(2**20), b''):
            h.update(chunk)
    return dict(path=name, bytes=p.stat().st_size, sha256=h.hexdigest())


def bind(root, row):
    need(pin(root, row['path']) == row, 'Exact published bytes: ' + row['path'])


def corpus_next(old, admission):
    new = copy.deepcopy(old)
    need(old['completion_obligation_original_ids'] == ['F004', 'F009', 'F012', 'L026', 'L046']
         and old['surviving_claim_obligation_original_ids'] == ['L046'], 'Exact previous obligations')
    new['fully_treated_original_ids'] = sorted(old['fully_treated_original_ids'] + ['L046'])
    new['fully_treated_originals'] = 101
    new['source_complete_refutation_original_ids'] = sorted(old['source_complete_refutation_original_ids'] + ['L046'])
    new['source_complete_refutation_originals'] = 9
    new['surviving_claim_obligation_original_ids'] = []
    new['surviving_claim_obligation_originals'] = 0
    new['completion_obligation_original_ids'] = ['F004', 'F009', 'F012', 'L026']
    new['completion_obligation_originals'] = 4
    new['current_source_completion_registration'] = admission
    new['handled_count_meaning'] = (
        'Principal dispositions: 92 corrected recoveries and nine principal refutations. '
        'All nine refuted sources now have complete surviving-source dispositions. '
        'Four originals retain completion obligations.')
    need(len(set(new['fully_treated_original_ids'])) == 101 and
         not set(new['fully_treated_original_ids']) & set(new['completion_obligation_original_ids']) and
         len(set(new['fully_treated_original_ids'] + new['completion_obligation_original_ids'])) == 105,
         'Exact partition of mathematical originals')
    return new


def paper_entry():
    return dict(id='onan_regular_maps/regular_maps', topic='O\'Nan regular maps',
                role='complete_source_treatment', source_contracts=['L046'],
                title='Regular maps for the O\'Nan group: a corrected source synthesis',
                tex='papers/onan_regular_maps/regular_maps.tex',
                pdf='papers/onan_regular_maps/regular_maps.pdf',
                tex_inputs=['papers/onan_regular_maps/exact_table.tex',
                            'papers/onan_regular_maps/source_concordance.tex'],
                compiler='pdflatex', physical_pages=10, admission=ADMISSION,
                measurement_status='not_measured', compression_factor=None,
                status='CURRENT_REVIEWED_COMPLETE_SOURCE_TREATMENT')


def catalogue_next(old, field):
    new = copy.deepcopy(old)
    need(not any(r.get('id') == paper_entry()['id'] for r in new[field]), 'New paper ID')
    new[field].append(paper_entry())
    return new


def verifier_next(old):
    tree = ast.parse(old)
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    lines = old.splitlines(keepends=True)
    replacement = '''def check_onan_source_completion():
    spec = importlib.util.spec_from_file_location('onan_source_completion', ROOT/'scripts/onan_regular_maps/registration.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify(ROOT)

def main():
    current = check_onan_source_completion()
    print(json.dumps(current, sort_keys=True))
    print("PASS: O'Nan source treatment; 101 fully treated originals and 4 remaining.")
    print('Scope: publication integrity and acquired reviews; run the portable checker for a fresh replay.')
'''
    new = ''.join(lines[:main.lineno-1]) + replacement + ''.join(lines[main.end_lineno:])
    before = [ast.dump(n, include_attributes=False) for n in tree.body
              if not isinstance(n, ast.FunctionDef) or n.name != 'main']
    after = [ast.dump(n, include_attributes=False) for n in ast.parse(new).body
             if not isinstance(n, ast.FunctionDef) or n.name not in ('main', 'check_onan_source_completion')]
    need(before == after, 'All predecessor verification functions preserved')
    return new


def changed_paths(root):
    names = set(git(root, 'diff', '--name-only', '-z', BASELINE, '--').decode().split('\0'))
    names |= set(git(root, 'ls-files', '--others', '--exclude-standard', '-z').decode().split('\0'))
    names.discard('')
    return names


def publication_next(root):
    old = json.loads(old_bytes(root, PUBLICATION))
    rows = {r['file']: r for r in old['files']}
    tracked = set(git(root, 'ls-files', '-z').decode().split('\0')) - {'', PUBLICATION}
    need(set(rows) <= tracked, 'No previously tracked artifact removed')
    for name in changed_paths(root) - {PUBLICATION}:
        need(name in tracked, 'Stage every new canonical file: ' + name)
        r = pin(root, name)
        rows[name] = dict(file=name, bytes=r['bytes'], sha256=r['sha256'])
    need(set(rows) == tracked, 'Exact tracked publication inventory')
    return {**old, 'files': [rows[n] for n in sorted(rows)]}


def verify(root):
    root = Path(root).resolve()
    need(git(root, 'merge-base', '--is-ancestor', BASELINE, 'HEAD') == b'', 'Preserved predecessor history')
    reg = load(root/REGISTRATION)
    need(reg['status'] == 'ROOT_ACCEPTED_ONAN_COMPLETE_SOURCE_PUBLICATION' and
         reg['baseline'] == BASELINE, 'Exact root publication registration')
    names = [r['path'] for r in reg['files']]
    need(len(names) == len(set(names)) and REGISTRATION not in names and PUBLICATION not in names,
         'Unique noncyclic registration bindings')
    for row in reg['files']:
        bind(root, row)
    changed = changed_paths(root)
    need(changed == set(names) | {REGISTRATION, PUBLICATION}, 'Only registered changes')
    old_names = set(git(root, 'ls-tree', '-r', '--name-only', BASELINE).decode().splitlines())
    need(changed & old_names == MODIFIED, 'Only six declared predecessor files changed')
    need(not any(n.endswith(('.md', '.pyc', '.olean', '.aux', '.fls', '.out')) for n in changed - old_names),
         'No technical build output in new publication')
    a = load(root/ADMISSION)
    need(a['status'] == 'ROOT_ACCEPTED_L046_COMPLETE_SOURCE_TREATMENT' and a['source_ids'] == ['L046']
         and a['source_completion_credit'] == 1 and a['source_claim_rows'] == 44, 'One complete fixed original')
    for key in ('ordinary_recovery_credit', 'principal_refutation_credit', 'new_original_credit',
                'new_measurements', 'new_question_credit', 'new_Lean_credit'):
        need(a[key] == 0, 'No additional credit: ' + key)
    need(a['compression_factor'] is None and a['whole_source_formalized'] is False,
         'No unearned ratio or formalization')
    need(a['synthesis_sha256'] == SYNTHESIS and a['mathematical_review_sha256'] == MATH_REVIEW,
         'Exact acquired mathematical synthesis')
    need(pin(root, DATA+'manifest.json')['sha256'] == a['manifest_sha256'] and
         pin(root, DATA+'transport.json')['sha256'] == a['transport_sha256'], 'Admitted portable edition')
    for row in load(root/(DATA+'manifest.json'))['exports']:
        bind(root, row)
    for key in ('portable_review', 'portable_report', 'registration_review'):
        bind(root, a[key])
    pr = load(root/a['portable_review']['path'])
    rr = load(root/a['registration_review']['path'])
    need(pr['portable_status'] == 'DISTINCT_ACCEPTED_L046_PORTABLE_PUBLICATION' and
         rr['registration_status'] == 'DISTINCT_ACCEPTED_ONAN_PUBLICATION_REGISTRATION',
         'Separate accepted portable and registration reviews')
    for review, key, name in (
            (rr, 'registration_code', 'scripts/onan_regular_maps/registration.py'),
            (pr, 'portable_code', 'scripts/onan_regular_maps/check.py'),
            (pr, 'manifest', DATA+'manifest.json'),
            (pr, 'portable_report', a['portable_report']['path'])):
        actual = pin(root, name)
        need(all(review[key][k] == actual[k] for k in ('bytes', 'sha256')),
             'Exact reviewed executable or result: ' + key)
    portable = load(root/a['portable_report']['path'])
    need(portable['status'] == 'PASS_L046_PUBLIC_TRANSPORT_AND_SYNTHESIS' and
         portable['manifest_sha256'] == a['manifest_sha256'] and
         portable['transport_sha256'] == a['transport_sha256'] and
         portable['numerical_cells'] == 136 and portable['table_sum'] == 798644 and
         portable['exact_inner_type_count'] == 95 and portable['exact_outer_type_count'] == 97,
         'Same actual passing portable report')
    need(load(root/'audit/corpus/latest.json') == corpus_next(json.loads(old_bytes(root, 'audit/corpus/latest.json')), pin(root, ADMISSION)),
         'Only L046 completion changes corpus')
    need(load(root/'papers/latest_catalogue.json') == catalogue_next(json.loads(old_bytes(root, 'papers/latest_catalogue.json')), 'entries'),
         'Exact reading catalogue addition')
    need(load(root/'papers/catalogue.json') == catalogue_next(json.loads(old_bytes(root, 'papers/catalogue.json')), 'new_editions'),
         'Exact build catalogue addition')
    need((root/'scripts/verify_snapshot.py').read_text() == verifier_next(old_bytes(root, 'scripts/verify_snapshot.py').decode()),
         'Only verifier dispatch changes')
    need(load(root/PUBLICATION) == publication_next(root), 'Exact publication manifest')
    return dict(status='PASS_ONAN_COMPLETE_SOURCE_PUBLICATION', fully_treated=101, outstanding=4,
                ordinary_recoveries=92, principal_refutations=9, measured=53,
                new_source_completion_credit=1, registered_files=len(names),
                fresh_scientific_replay=False, prior_history_preserved=True)


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parents[2]), sort_keys=True))
