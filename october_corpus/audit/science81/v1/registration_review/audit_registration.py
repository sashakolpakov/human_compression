"""Independent, public-only L120 registration audit; never executes a census."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Optimized Python is not supported')
sys.dont_write_bytecode = True
import argparse
import ast
import copy
import hashlib
import json
import subprocess
from pathlib import Path

BASE = 'de9e7c4c7058c800820be91c091a200d2ece9c86'
AUD = 'audit/science81/v1'
REC = 'audit/recoveries/L120/v1'

def require(ok, why):
    if not ok:
        raise ValueError(why)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def read(root, path):
    return json.loads((root / path).read_text())

def git_bytes(root, path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=root)

def partition(before, after):
    require(len(before['entries']) == len(after['entries']) == 106, '106 catalogue records')
    a = {r['original_id']: r for r in before['entries']}
    b = {r['original_id']: r for r in after['entries']}
    require(len(a) == len(b) == 106 and a.keys() == b.keys(), 'Unique identical original IDs')
    require([k for k in a if a[k] != b[k]] == ['L120'], 'Only the L120 record may change')
    for k in a['L120']:
        if k not in {'current_principal_recovery', 'next_obligation'}:
            require(a['L120'][k] == b['L120'][k], 'Preserved source/historical L120 field ' + k)
    return a, b

def measured(old, current):
    ids = old['measured_original_ids']
    require(len(ids) == len(set(ids)) == 53, '53 distinct measured IDs')
    require(current['measured_original_ids'] == ids, 'Exact measured ID order and membership')
    for k in ['currently_measured_originals', 'added_measurements', 'superseded_measurement_admissions']:
        require(current[k] == old[k], 'Unchanged measurement field ' + k)
    return ids

def functions(text):
    tree = ast.parse(text)
    return {n.name: ast.dump(n, include_attributes=False) for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

def main_interface(old, current):
    replacements = [
        ('    science80_history = check_previous_science80()\n',
         "    science81_history = check_previous_science81()\n    science80_history = science81_history['previous']\n"),
        ('    science72 = check_science80()\n', '    science72 = check_science81()\n'),
        ("    print('PASS: exact science79 history preserved; L042 explicit classification adds one original.')\n",
         "    print('PASS: exact science80 history preserved; L120 attributed survey recovery adds one original.')\n")
    ]
    expected = old
    for before, after in replacements:
        require(expected.count(before) == 1, 'Unambiguous predecessor main call')
        expected = expected.replace(before, after)
    require(functions(expected)['main'] == functions(current)['main'], 'Only the three exact main edits')

def audit(root, bindings, git_baseline=True):
    require(bindings['baseline_commit'] == BASE, 'Exact scientific predecessor')
    for row in bindings['files']:
        p = (root / row['path']).resolve()
        require(p.is_relative_to(root) and p.is_file(), 'Safe existing candidate path')
        raw = p.read_bytes()
        require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'Changed candidate ' + row['path'])
    h = read(root, AUD + '/history_routes.json')
    require(h['baseline_commit'] == BASE and len(h['routes']) == 8, 'Eight historical routes')
    old_bytes = {}
    for name, row in h['routes'].items():
        retained = (root / row['path']).read_bytes()
        require(digest(retained) == row['sha256'] and len(retained) == row['bytes'], 'Historical pin')
        if git_baseline:
            require(retained == git_bytes(root, name), 'Historical bytes differ from actual git predecessor ' + name)
        old_bytes[name] = retained
    old = json.loads(old_bytes['audit/corpus/latest.json'])
    current = read(root, 'audit/corpus/latest.json')
    cat = read(root, current['active_catalogue']['path'])
    oldcat = read(root, old['active_catalogue']['path'])
    if git_baseline:
        require((root / old['active_catalogue']['path']).read_bytes() == git_bytes(root, old['active_catalogue']['path']), 'Actual predecessor catalogue bytes')
    a, b = partition(oldcat, cat)
    ids = measured(old, current)
    require(all(a[k] == b[k] for k in ids), 'All measured original records unchanged')
    require(set(current['admitted_original_ids']) == set(old['admitted_original_ids']) | {'L120'}, 'One recovery added')
    require(set(current['accessible_pending_original_ids']) == set(old['accessible_pending_original_ids']) - {'L120'}, 'One pending original removed')
    require((old['admitted_principal_originals'], current['admitted_principal_originals'], current['handled_mathematical_originals'], current['accessible_pending_complete_recovery']) == (80, 81, 82, 23), 'Exact 80 to 81 increment')
    require({'L045', 'L046', 'F009', 'F012'} <= set(current['accessible_pending_original_ids']), 'Unfinished originals remain pending')
    # Every existing measured paper route is retained byte for byte as JSON data.
    papers = read(root, 'papers/latest_catalogue.json')
    oldpapers = json.loads(old_bytes['papers/latest_catalogue.json'])
    require(papers['entries'] == oldpapers['entries'] and papers['original_ids'] == oldpapers['original_ids'], 'Measured manuscript catalogue unchanged')
    vf_old = old_bytes['scripts/verify_snapshot.py'].decode()
    vf_new = (root / 'scripts/verify_snapshot.py').read_text()
    fs_old, fs_new = functions(vf_old), functions(vf_new)
    preserved = {k: v for k, v in fs_old.items() if k != 'main'}
    require(len(preserved) == 189 and all(fs_new.get(k) == v for k, v in preserved.items()), '189 old verifier functions unchanged')
    require(set(fs_new) - set(fs_old) == {'check_previous_science81', 'check_science81'}, 'Exactly two added functions')
    main_interface(vf_old, vf_new)
    admission = read(root, REC + '/admission.json')
    scope = read(root, REC + '/scope_routes.json')
    require((admission['counts']['acquired_or_corrected_assertions'], admission['counts']['retained_assertions'], admission['counts']['project_cells'], admission['counts']['retained_cells']) == (25, 7, 212, 9), 'No promotion of retained results')
    require(len(admission['intermediate_corrections']) == 8 and scope['retained_assertions'] == admission['retained_assertions'], 'All corrections and retained clauses explicit')
    require(not admission['all_original_assertions_claimed'] and not admission['measured'] and admission['whole_original_credit'] == 0, 'Pre-gate scope unchanged')
    require(admission['new_question_credit'] == admission['new_Lean_declarations'] == admission['new_measurements'] == 0, 'No extra phase credit')
    require(set(admission['component_acceptance']['complete']) == {'author', 'distinct_root_review'}, 'No invented independent adoption')
    parameters = read(root, AUD + '/registration_parameters.json')
    require(parameters['operational_manifest'] == 'ddd8bbfe7427d7f8e5b8c9117102e3648dbe3769c09665608a206a9fe98ee69a', 'Exact separately accepted transport')
    # Independent controls exercise ID comparisons rather than the production zip.
    controls = []
    for label, damage, check in [
        ('duplicate catalogue ID', lambda x: x['entries'].__setitem__(1, copy.deepcopy(x['entries'][0])), lambda x: partition(oldcat, x)),
        ('another original changed', lambda x: x['entries'][0].update(title='damaged'), lambda x: partition(oldcat, x)),
        ('L120 source changed', lambda x: next(r for r in x['entries'] if r['original_id'] == 'L120').update(title='damaged'), lambda x: partition(oldcat, x))
    ]:
        damaged = copy.deepcopy(cat); damage(damaged)
        try: check(damaged)
        except ValueError: controls.append(label)
        else: raise ValueError('Independent damage accepted ' + label)
    damaged = copy.deepcopy(current); damaged['measured_original_ids'][0] = 'L120'
    try: measured(old, damaged)
    except ValueError: controls.append('measured ID substituted')
    else: raise ValueError('Changed measured set accepted')
    try: main_interface(vf_old, vf_new.replace('    active_pending = science72', '    active_pending = science73'))
    except ValueError: controls.append('unrelated main edit')
    else: raise ValueError('Unrelated main edit accepted')
    return dict(status='PASS_INDEPENDENT_L120_REGISTRATION', exact_candidate_files=len(bindings['files']),
        baseline_commit=BASE, git_predecessor_compared=git_baseline, historical_pointers=8,
        catalogue_records=106, changed_original_ids=['L120'], measured_originals_unchanged=53,
        preserved_verifier_functions=189, exact_main_edits=3, independent_damaged_controls=controls,
        counts=dict(recoveries=81, refutations=1, handled=82, pending=23, measured=53, unmeasured=28),
        full_history_repeated=False, mathematical_census_repeated=False, public_writes=False)

def main():
    p = argparse.ArgumentParser(); p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--without-git-baseline', action='store_true', help='For exported repositories: preserve hashes but do not claim a fresh git-object comparison')
    args = p.parse_args(); root = args.repo.resolve()
    bindings = json.loads((Path(__file__).parent / 'candidate_bindings.json').read_text())
    report = audit(root, bindings, not args.without_git_baseline)
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
