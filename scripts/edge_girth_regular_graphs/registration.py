"""Additive F012 publication registration over the preserved 8e10 predecessor.

Integrity of exact new exports, acquired scoped reviews and inherited Git
identities. This neither reruns mathematical predicates nor hashes the entire
unrelated historical worktree. Missing whole-original gates fail closed.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
import ast
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess

BASELINE = '8e10ebc3a05eef8f6dce3b9f6108afaa918e5f29'
DATA = 'data/edge_girth_regular_graphs/'
PAPER = 'papers/edge_girth_regular_graphs/'
CODE = 'scripts/edge_girth_regular_graphs/registration.py'
ADMISSION = DATA + 'admission.json'
REGISTRATION = DATA + 'registration.json'
MANIFEST = DATA + 'package_manifest.json'
PUBLICATION = 'provenance/publication_manifest.json'
# Exact source-only export declaration; excludes this checker and outer gates.
MANIFEST_SHA = '3202561abab70e974d1153d1504b673c12a25c82120662a9ed34fa2061037486'
BASELINE_RECORDS = {
    PUBLICATION: (10433143, '0187510c67ba1f1d5c806965ecb884a00bb8f76b160fc87eef56b9e7eb77120a'),
    'data/onan_regular_maps/registration.json': (64001, 'eeaabc427b44d6fe3b4b2b333c5b87f3ebcf9ab0b71424b773b1664f836018c3'),
    'data/onan_regular_maps/admission.json': (2146, 'f493bf97c8e3ba7c19e315e943feaf5b32dbf428f3551b7a6c23e66b6ad2fdf9'),
    'scripts/onan_regular_maps/registration.py': (11908, '3b03684925e961cabbeed294e23b73dca72b522af39ec64cecf9cedc9c66c0e9'),
}
INTEGRATION = DATA + 'reviews/binding/integration_root.json'
INTEGRATION_SHA = '728bbff5c5cf4b58631a03089c8ee34f153dabc7026222c8dbc486cb64b5215a'
MODIFIED = {'README.rst', 'docs/REPRODUCING.rst', 'audit/corpus/latest.json',
            'papers/latest_catalogue.json', 'papers/catalogue.json',
            'scripts/verify_snapshot.py', PUBLICATION}
FINAL_REVIEWS = {
    'manuscript': ('manuscript.json', 'DISTINCT_ACCEPTED_F012_WHOLE_MANUSCRIPT'),
    'transport': ('transport.json', 'ROOT_ACCEPTED_F012_SELECTED_PUBLICATION_TRANSPORT'),
    'path_controls': ('path_controls.json', 'ROOT_ACCEPTED_F012_PUBLICATION_PATH_CONTROLS'),
    'render': ('render.json', 'ROOT_ACCEPTED_F012_CURRENT_MANUSCRIPT_RENDER'),
    'registration_review': ('registration_review.json', 'DISTINCT_ACCEPTED_F012_PUBLICATION_REGISTRATION'),
    'selected_checkout': ('selected_checkout.json', 'ROOT_ACCEPTED_F012_SELECTED_CHECKOUT'),
}
TEX = PAPER + 'edge_girth_regular_graphs_with_figures.tex'
PDF = PAPER + 'edge_girth_regular_graphs_with_figures.pdf'
TEX_INPUTS = [PAPER + n + '.tex' for n in (
    'descriptive_figures', 'numeric_tables', 'symmetry_table', 'host_certificate_table',
    'component_concordance', 'component_bibliography')]
COUNTS = dict(components=49, overarching_families=5, principal_claims=16,
              literal_rows=260, written_joins=53)

README_SUFFIX = b"\nF012: complete edge-girth-regular graph source treatment\n-------------------------------------------------------\n\nThe current reviewed F012 manuscript, its exact source concordance and\npackage-relative reproduction instructions are in\n``papers/edge_girth_regular_graphs/``. The additive admission is\n``data/edge_girth_regular_graphs/admission.json``; it retains the source's\nclassification/software premises and unresolved infinity assertions.\nRun ``python3 -E -B scripts/verify_snapshot.py`` for registered publication\nintegrity. Scientific route commands, supported macOS ownership scope and\nselected-checkout qualifications are in the reproduction guide. No whole\nfresh-machine corpus replay or new compression measurement is claimed.\n"
REPRODUCTION_SUFFIX = b"\nF012 package-relative reproduction\n----------------------------------\n\nRead ``papers/edge_girth_regular_graphs/reproduction.rst`` before selecting a\nroute. It gives typed environment generation, complete bounded defaults,\nexact payload authentication and restoration of all 53 written sources.\nThe public registration preserves the full 8e10ebc3 predecessor Git tree and\nglobal manifest; locally sparse unchanged files are retained Git objects,\nnot deletions. Restore a historical path from Git before invoking a checker\nthat needs its working-tree bytes. The registration reports inherited Git\nidentity checks separately from full hashing of all new package exports.\nThe metadata controls and dense-bounds integration do not replace the\nsource's borrowed catalogue premises or amount to an all-route fresh replay.\n"

def need(ok, message):
    if not ok:
        raise ValueError(message)


def git(root, *args):
    return subprocess.check_output(['git', '--no-optional-locks', '-c', 'core.fsmonitor=false',
                                    '-c', 'core.untrackedCache=false', *args], cwd=root)


def relative(name):
    need(isinstance(name, str), 'Literal repository path')
    p = PurePosixPath(name)
    need(not p.is_absolute() and p.parts and '..' not in p.parts and str(p) == name,
         'Canonical repository-relative path')
    return p


def safe(root, name):
    path = root.joinpath(*relative(name).parts)
    for parent in (path.parent, *path.parent.parents):
        need(stat.S_ISDIR(parent.lstat().st_mode) and not parent.is_symlink(), 'Ordinary ancestors')
    need(stat.S_ISREG(path.lstat().st_mode), 'Ordinary published file: ' + name)
    return path


def pin(root, name):
    p = safe(root, name)
    h, size = hashlib.sha256(), 0
    with p.open('rb') as stream:
        for chunk in iter(lambda: stream.read(2**20), b''):
            h.update(chunk)
            size += len(chunk)
    return dict(path=name, bytes=size, sha256=h.hexdigest())


def bind(root, row):
    need(isinstance(row, dict) and set(row) == {'path', 'bytes', 'sha256'}, 'Exact file-pin fields')
    need(pin(root, row['path']) == row, 'Exact registered bytes: ' + row['path'])


def load(root, name):
    p = safe(root, name)
    need(p.stat().st_size <= 16*2**20, 'Bounded registration metadata')
    return json.loads(p.read_bytes())


def old_bytes(root, name):
    relative(name)
    return git(root, 'show', BASELINE + ':' + name)


def predecessor(root):
    need(git(root, 'merge-base', '--is-ancestor', BASELINE, 'HEAD') == b'', 'Preserved predecessor history')
    records = {}
    for name, expected in BASELINE_RECORDS.items():
        raw = old_bytes(root, name)
        need((len(raw), hashlib.sha256(raw).hexdigest()) == expected, 'Exact predecessor record: ' + name)
        records[name] = json.loads(raw) if name.endswith('.json') else raw
    return records


def tree_rows(raw):
    result = {}
    for item in raw.split(b'\0'):
        if not item:
            continue
        header, name = item.split(b'\t', 1)
        mode, kind, oid = header.decode().split(' ')
        name = name.decode('utf-8')
        relative(name)
        need(kind == 'blob' and mode in ('100644', '100755', '120000') and name not in result,
             'Unique predecessor blob, no submodule')
        result[name] = (mode, oid)
    return result


def index_rows(raw):
    result = {}
    for item in raw.split(b'\0'):
        if not item:
            continue
        header, name = item.split(b'\t', 1)
        mode, oid, stage = header.decode().split(' ')
        name = name.decode('utf-8')
        relative(name)
        need(stage == '0' and mode in ('100644', '100755', '120000') and name not in result,
             'Unique resolved index entries')
        result[name] = (mode, oid)
    return result


def tracked_preservation(root, registered):
    before = tree_rows(git(root, 'ls-tree', '-r', '-z', BASELINE))
    current = index_rows(git(root, 'ls-files', '--stage', '-z'))
    need(set(before) <= set(current), 'No predecessor tracked path removed')
    changed = {n for n in current if n not in before or current[n] != before[n]}
    need(changed == registered | {REGISTRATION, PUBLICATION}, 'Only exact staged/committed registered changes')
    need(changed & set(before) == MODIFIED, 'Only seven predecessor navigation/registration paths changed')
    need(not git(root, 'diff-files', '--no-ext-diff', '--name-only', '-z'), 'No unstaged tracked changes')
    need(not git(root, 'ls-files', '--others', '--exclude-standard', '-z'), 'No undeclared untracked publication files')
    flags = {}
    for row in git(root, 'ls-files', '-v', '-z').split(b'\0'):
        if row:
            tag, name = row[:1].decode(), row[2:].decode('utf-8')
            need(row[1:2] == b' ' and name not in flags and tag in ('H', 'S'),
                 'No assume-unchanged or unresolved index flags')
            flags[name] = tag
    need(set(flags) == set(current), 'Exact index flag inventory')
    absent = 0
    for name, identity in before.items():
        if name in MODIFIED:
            continue
        need(current[name] == identity, 'Unchanged predecessor mode/blob identity')
        p = root.joinpath(*relative(name).parts)
        if not os.path.lexists(p):
            need(flags[name] == 'S', 'Only explicitly sparse predecessor paths may be absent')
            absent += 1
        elif flags[name] == 'S':
            raise ValueError('Present skip-worktree predecessor must be restored/unflagged before verification: ' + name)
        elif identity[0] == '120000':
            need(p.is_symlink() and os.fsencode(os.readlink(p)) == old_bytes(root, name),
                 'Exact retained predecessor symbolic link')
        else:
            need(stat.S_ISREG(p.lstat().st_mode), 'Present predecessor remains an ordinary file')
    for name in registered | {REGISTRATION, PUBLICATION}:
        need(current[name][0] == '100644', 'New/modified canonical publication files are ordinary nonexecutables')
        safe(root, name)
    return current, absent


def publication_next(old, registered_rows, registration_pin):
    rows = {r['file']: r for r in old['files']}
    need(len(rows) == len(old['files']), 'Unique predecessor global manifest')
    for r in [*registered_rows, registration_pin]:
        rows[r['path']] = dict(file=r['path'], bytes=r['bytes'], sha256=r['sha256'])
    return {**old, 'files': [rows[n] for n in sorted(rows)]}


def corpus_next(old, admission_pin):
    """Conditional F012 corrected-recovery migration; no gate is created here."""
    need(old['completion_obligation_original_ids'] == ['F004', 'F009', 'F012', 'L026']
         and old['admitted_principal_originals'] == 92 and old['fully_treated_originals'] == 101,
         'Exact predecessor disposition')
    new = copy.deepcopy(old)
    new['status'] = 'CURRENT_PROGRAMME_93_RECOVERED_9_PRINCIPAL_REFUTATIONS_3_PENDING_1_EDITORIAL'
    for field in ('admitted_original_ids', 'handled_mathematical_original_ids', 'fully_treated_original_ids',
                  'measurement_pending_original_ids', 'scientific_unmeasured_original_ids'):
        need('F012' not in old[field], 'No duplicate F012 admission')
        new[field] = sorted(old[field] + ['F012'])
    for field in ('accessible_pending_original_ids', 'completion_obligation_original_ids'):
        need(old[field].count('F012') == 1, 'Exact prior F012 obligation')
        new[field] = [n for n in old[field] if n != 'F012']
    new['admitted_principal_originals'] = 93
    new['accessible_pending_complete_recovery'] = 3
    new['handled_mathematical_originals'] = 102
    new['fully_treated_originals'] = 102
    new['completion_obligation_originals'] = 3
    new['added_admissions'] = old['added_admissions'] + [admission_pin]
    new['current_source_completion_registration'] = admission_pin
    new['handled_count_meaning'] = ('Principal dispositions: 93 corrected recoveries and nine principal refutations. '
        'All nine refuted sources retain complete surviving-source dispositions. Three originals retain completion obligations.')
    need(len(new['fully_treated_original_ids']) == 102 and
         not set(new['fully_treated_original_ids']) & set(new['completion_obligation_original_ids']) and
         len(set(new['fully_treated_original_ids'] + new['completion_obligation_original_ids'])) == 105,
         'Exact preserved 105-original partition')
    return new


def paper_entry(pages):
    need(type(pages) is int and pages > 0, 'Actual rendered physical page count')
    return dict(id='edge_girth_regular_graphs/source_treatment', topic='Edge-girth-regular graphs',
        role='complete_source_treatment', source_contracts=['F012'],
        title='Edge-girth-regular graphs: complete generation, numerical bounds, and the quartic one-hexagon obstruction',
        tex=TEX, pdf=PDF, tex_inputs=TEX_INPUTS, compiler='pdflatex', physical_pages=pages,
        admission=ADMISSION, measurement_status='not_measured', compression_factor=None,
        status='CURRENT_REVIEWED_COMPLETE_SOURCE_TREATMENT')


def catalogue_next(old, field, pages):
    new = copy.deepcopy(old)
    entry = paper_entry(pages)
    need(not any(r.get('id') == entry['id'] for r in old[field]), 'New exact paper ID')
    new[field].append(entry)
    if field == 'entries':
        new['status'] = 'CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_FORTY_CORRECTED_UNMEASURED'
    return new


def verifier_next(old):
    tree = ast.parse(old)
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    lines = old.splitlines(keepends=True)
    replacement = '''def check_f012_source_completion():
    spec = importlib.util.spec_from_file_location('f012_source_completion', ROOT/'scripts/edge_girth_regular_graphs/registration.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify(ROOT)

def main():
    current = check_f012_source_completion()
    print(json.dumps(current, sort_keys=True))
    print('PASS: F012 source treatment; 102 fully treated originals and 3 remaining.')
    print('Scope: exact new exports and acquired reviews; inherited Git identities, not a fresh whole-corpus replay.')
'''
    new = ''.join(lines[:main.lineno-1]) + replacement + ''.join(lines[main.end_lineno:])
    before = [ast.dump(n, include_attributes=False) for n in tree.body
              if not isinstance(n, ast.FunctionDef) or n.name != 'main']
    after = [ast.dump(n, include_attributes=False) for n in ast.parse(new).body
             if not isinstance(n, ast.FunctionDef) or n.name not in ('main', 'check_f012_source_completion')]
    need(before == after, 'All predecessor verifier functions preserved')
    return new


def review(root, admission, key):
    name, status = FINAL_REVIEWS[key]
    row = admission[key]
    need(isinstance(row, dict) and row.get('path') == DATA + 'reviews/publication/' + name,
         'Actual separate ' + key + ' pin required')
    bind(root, row)
    value = load(root, row['path'])
    need(value['status'] == status and value['package_manifest'] == admission['package_manifest'],
         'Actual separate ' + key + ' acceptance and package join')
    return value


def verify(root):
    root = Path(root).absolute()
    need(root.resolve(strict=True) == root and all(not p.is_symlink() for p in (root, *root.parents)),
         'Canonical ordinary checkout root')
    previous = predecessor(root)
    reg = load(root, REGISTRATION)
    need(reg['status'] == 'ROOT_ACCEPTED_F012_COMPLETE_SOURCE_PUBLICATION' and reg['baseline'] == BASELINE,
         'Actual root publication registration required')
    need(reg['predecessor_records'] == {n: dict(path=n, bytes=b, sha256=h) for n,(b,h) in BASELINE_RECORDS.items()},
         'Explicit exact predecessor manifest, registration, admission and code joins')
    rows = reg['files']; names = [r['path'] for r in rows]
    need(len(names) == len(set(names)) and REGISTRATION not in names and PUBLICATION not in names,
         'Unique noncyclic registered files')
    current, absent = tracked_preservation(root, set(names))
    for row in rows:
        bind(root, row)
    package = load(root, MANIFEST)
    need(pin(root, MANIFEST)['sha256'] == MANIFEST_SHA and package['schema'] == 'F012_PUBLIC_PACKAGE_EXPORTS_V1'
         and package['counts'] == COUNTS, 'Exact independently reviewed export declaration and concordance')
    exports = {r['path']:r for r in package['exports']}
    need(len(exports) == len(package['exports']), 'Unique package exports')
    byname = {r['path']:r for r in rows}
    need(all(byname.get(n) == r for n,r in exports.items()), 'All declared payload/source bytes registered')
    expected = set(exports) | {CODE, MANIFEST, ADMISSION, PDF} | (MODIFIED - {PUBLICATION})
    expected |= {DATA + 'reviews/publication/' + n for n,_ in FINAL_REVIEWS.values()}
    need(set(names) == expected, 'No omitted export or undeclared new artifact')
    need(not any(n.endswith(('.pyc','.olean','.aux','.fls','.fdb_latexmk','.o','.dylib','.so'))
                 for n in set(names) - MODIFIED), 'No new compiler sidecars or host binaries')
    a = load(root, ADMISSION)
    need(a['status'] == 'ROOT_ACCEPTED_F012_COMPLETE_SOURCE_TREATMENT' and a['source_ids'] == ['F012']
         and a['principal_disposition'] == 'corrected_recovery' and a['source_completion_credit'] == 1
         and a['ordinary_recovery_credit'] == 1, 'Separate actual whole-original root admission required')
    for key in ('principal_refutation_credit','new_original_credit','new_measurements','new_question_credit','new_Lean_credit'):
        need(a[key] == 0, 'No additional credit: ' + key)
    need(a['compression_factor'] is None and a['whole_source_formalized'] is False
         and a['all_source_conjectures_resolved'] is False and a['counts'] == COUNTS,
         'No unearned measurement, formalization or conjecture claim')
    need(a['package_manifest'] == pin(root, MANIFEST) and a['binding_integration'] == pin(root, INTEGRATION)
         and a['binding_integration']['sha256'] == INTEGRATION_SHA, 'Exact package and acquired scoped integration')
    integration = load(root, INTEGRATION)
    need(integration['status'] == 'ROOT_ACCEPTED_F012_TYPED_PACKAGE_DENSE_BOUNDS_INTEGRATION'
         and integration['scientific_routes_replayed_through_new_interface'] == 1
         and integration['whole_original_credit'] == 0, 'Scoped integration is not the whole-original premise')
    rr = {key:review(root,a,key) for key in FINAL_REVIEWS}
    manuscript = rr['manuscript']; render = rr['render']
    need(manuscript['tex'] == pin(root,TEX) and manuscript['tex_inputs'] == [pin(root,n) for n in TEX_INPUTS]
         and manuscript['concordance'] == package['concordance'] and manuscript['counts'] == COUNTS,
         'Whole written manuscript and exact concordance joins')
    need(render['tex'] == manuscript['tex'] and render['tex_inputs'] == manuscript['tex_inputs']
         and render['pdf'] == pin(root,PDF), 'New PDF belongs to exact current source and all inputs')
    need(rr['registration_review']['code'] == pin(root,CODE)
         and rr['registration_review']['dispatch'] == pin(root,'scripts/verify_snapshot.py'),
         'Separate review of exact current registration and dispatch')
    need(rr['transport']['parts'] == 1182 and rr['transport']['objects'] == 1176
         and rr['transport']['bytes'] == 531189137 and rr['transport']['written_sources'] == 53
         and rr['transport']['scientific_calls'] == 0, 'Complete selected transport and written restoration')
    need(rr['path_controls']['helper'] == exports['scripts/edge_girth_regular_graphs/publication_data.py']
         and rr['path_controls']['all_declared_controls_passed'] is True, 'Actual corrected path-boundary controls')
    need(rr['selected_checkout']['full_corpus_replay'] is False
         and rr['selected_checkout']['private_source_fallback'] is False
         and rr['selected_checkout']['selected_exports_equal'] is True, 'Honest selected checkout scope')
    need(load(root,'audit/corpus/latest.json') == corpus_next(json.loads(old_bytes(root,'audit/corpus/latest.json')),pin(root,ADMISSION)),
         'Only conditionally admitted F012 changes the complete corpus disposition')
    for name, field in [('papers/latest_catalogue.json','entries'),('papers/catalogue.json','new_editions')]:
        need(load(root,name) == catalogue_next(json.loads(old_bytes(root,name)),field,render['physical_pages']),
             'Exact paper catalogue extension')
    need(safe(root,'scripts/verify_snapshot.py').read_text() == verifier_next(old_bytes(root,'scripts/verify_snapshot.py').decode()),
         'Only current verifier dispatch changes')
    need(safe(root,'README.rst').read_bytes() == old_bytes(root,'README.rst') + README_SUFFIX
         and safe(root,'docs/REPRODUCING.rst').read_bytes() == old_bytes(root,'docs/REPRODUCING.rst') + REPRODUCTION_SUFFIX,
         'Only exact additive navigation paragraphs')
    expected_global = publication_next(previous[PUBLICATION],rows,pin(root,REGISTRATION))
    need(load(root,PUBLICATION) == expected_global and {r['file'] for r in expected_global['files']} == set(current)-{PUBLICATION},
         'Every predecessor global manifest row retained, exact current tracked inventory')
    return dict(status='PASS_F012_COMPLETE_SOURCE_PUBLICATION',fully_treated=102,outstanding=3,
        ordinary_recoveries=93,principal_refutations=9,measured=53,registered_files=len(names),
        prior_sparse_absent_files=absent,prior_git_identities_preserved=True,
        prior_whole_worktree_rehashed=False,new_registered_exports_hashed=True,
        fresh_scientific_replay=False,full_fresh_machine_reproduction=False)


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parents[2]),sort_keys=True))
