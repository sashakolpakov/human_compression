"""Verify the administrative F012/L046 catalogue layer over a fixed public tree.

Inherited scientific publications are authenticated by their retained Git
identities and acquired reviews, not by a new mathematical or whole-corpus
replay.  Only the declared administrative delta is freshly byte-checked.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import time

BASELINE = 'de0864a7bde3c992239427d3c838fe0fe8ea370d'
DIRECTORY = 'audit/corpus/accessible106/updates/'
PREVIOUS = DIRECTORY + 'completion-L063-L064-catalogue.json'
CATALOGUE = DIRECTORY + 'completion-F012-L046-catalogue.json'
EXPLANATION = DIRECTORY + 'completion-F012-L046.rst'
REGISTRATION = DIRECTORY + 'completion-F012-L046-publication.json'
GUIDE = DIRECTORY + 'completion-F012-L046-publication.rst'
CODE = 'scripts/catalogue_completion_registration.py'
DISPATCH = 'scripts/verify_snapshot.py'
CORPUS = 'audit/corpus/latest.json'
PAPERS = 'papers/latest_catalogue.json'
F012 = 'data/edge_girth_regular_graphs/admission.json'
L046 = 'data/onan_regular_maps/admission.json'
OLD_REGISTRATION = 'data/edge_girth_regular_graphs/registration.json'
OLD_CODE = 'scripts/edge_girth_regular_graphs/registration.py'
PUBLICATION = 'provenance/publication_manifest.json'
OLD_REVIEW = 'data/edge_girth_regular_graphs/reviews/publication/registration_review.json'
OLD_CHECKOUT = 'data/edge_girth_regular_graphs/reviews/publication/selected_checkout.json'
FILES = {CATALOGUE, EXPLANATION, CODE, GUIDE, DISPATCH, CORPUS, PAPERS}
OLD_MAIN = """def main():
    current = check_f012_source_completion()
    print(json.dumps(current, sort_keys=True))
    print('PASS: F012 source treatment; 102 fully treated originals and 3 remaining.')
    print('Scope: exact new exports and acquired reviews; inherited Git identities, not a fresh whole-corpus replay.')
"""
NEW_MAIN = """def main():
    spec = importlib.util.spec_from_file_location('catalogue_completion_registration',
        ROOT/'scripts/catalogue_completion_registration.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    current = module.verify(ROOT, require_tracked=True)
    print(json.dumps(current, sort_keys=True))
    print('PASS: administrative catalogue correction; 102 fully treated originals and 3 remaining.')
    print('Scope: exact catalogue layer and inherited reviewed Git identities; no fresh scientific or whole-corpus replay.')
"""


def need(condition, message):
    if not condition:
        raise ValueError(message)


def relative(name):
    need(isinstance(name, str), 'String relative path required')
    p = PurePosixPath(name)
    need(not p.is_absolute() and str(p) == name and '..' not in p.parts,
         'Canonical repository-relative path required')
    return name


def pin_bytes(name, data):
    return dict(path=relative(name), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def read(root, name, cap=4 * 1024 * 1024):
    path = root / relative(name)
    need(path.is_file() and not path.is_symlink(), 'Ordinary file required: ' + name)
    before = path.stat()
    need(before.st_size <= cap, 'Administrative input cap: ' + name)
    with path.open('rb') as f:
        data = f.read(cap + 1)
    after = path.stat()
    fields = ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    need(len(data) == before.st_size and len(data) <= cap and
         all(getattr(before, k) == getattr(after, k) for k in fields),
         'Stable complete administrative input required: ' + name)
    return data


def git(root, *args):
    q = subprocess.run(['git', '--no-optional-locks', '-c', 'core.fsmonitor=false',
        '-c', 'core.untrackedCache=false', *args], cwd=root,
        capture_output=True, timeout=60)
    need(q.returncode == 0, 'Required retained Git history unavailable: ' + ' '.join(args))
    need(len(q.stdout) <= 32 * 1024 * 1024, 'Bounded Git metadata response required')
    return q.stdout


def old(root, name, cap=4 * 1024 * 1024):
    b = git(root, 'show', BASELINE + ':' + relative(name))
    need(len(b) <= cap, 'Bounded retained administrative record required: ' + name)
    return b


def successor(base, fpin, lpin, fadmission, ladmission, previous_pin):
    """The exact two-row correction; all other source annotations survive."""
    new = copy.deepcopy(base)
    rows = {r['original_id']: r for r in new['entries']}
    need(len(rows) == len(new['entries']) == 106, 'Exact active 106-original domain')
    fr = rows['F012']; c = fr['current_principal_recovery']
    need(c['status'] == 'PENDING_COMPLETE_RECOVERY', 'Exact previous F012 status')
    c.update(status='CORRECTED_PRINCIPAL_RECOVERY_ACCEPTED_MEASUREMENT_PENDING',
        disposition_kind='ordinary_recovery', principal_contract_admitted=True,
        complete_principal_contract_recovered=True, original_fully_handled=True,
        all_original_assertions_claimed=False, whole_source_formalized=False,
        measured=False, compression_factor=None, latest_admission_references=[fpin],
        source_qualifications=fadmission['qualification'])
    fr['next_obligation'] = ('Complete reviewed source treatment accepted; measurement remains pending. '
        'Preserve the borrowed classification/software premises and unresolved infinity assertions. '
        'No complete Lean formalization or all-conjecture resolution is claimed.')
    lr = rows['L046']; c = lr['current_principal_recovery']
    need(c['status'] == 'CLOSED_BY_REVIEWED_PRINCIPAL_REFUTATION', 'Preserved L046 refutation')
    need(lpin not in c['latest_admission_references'], 'No repeated completion admission')
    c['latest_admission_references'].append(lpin)
    c['original_fully_handled'] = True
    c['source_qualifications'] = ('The earlier principal refutation is preserved. The complete reviewed '
        'treatment now disposes of all 44 fixed source clauses under its explicit classical group, '
        'character and subgroup premises. Type counts are not global numbers of reflexible markings. '
        'The portable composition and arithmetic checks do not repeat every historical group census; '
        'no ordinary recovery, new principal refutation, measurement or whole-source formalization is added.')
    lr['current_source_completion'] = dict(
        status='REVIEWED_COMPLETE_SOURCE_DISPOSITION_AFTER_PRINCIPAL_REFUTATION',
        admission=lpin, principal_refutation_preserved=True, ordinary_recovery_credit=0,
        source_claim_rows=ladmission['source_claim_rows'], source_contract=ladmission['scope'],
        qualification=' '.join(ladmission['limits']), whole_source_formalized=False,
        measured=False, compression_factor=None)
    lr['next_obligation'] = ('No surviving mathematical source-disposition obligation remains for this fixed '
        'original. Preserve the principal refutation and the complete treatment with its explicit classical '
        'premises, source conventions and replay limits. No ordinary recovery, new principal refutation '
        'or compression measurement is assigned.')
    new.update(status='CURRENT_ACCESSIBLE106_93_RECOVERED_9_PRINCIPAL_REFUTATIONS_3_PENDING',
        admitted_principal_originals=93, accessible_pending_complete_recovery=3,
        handled_mathematical_originals=102, source_complete_refutation_originals=9,
        fully_treated_originals=102, previous_catalogue=previous_pin,
        review_revision='Synchronize F012 and L046 with their already-public reviewed complete-source admissions. '
        'F012 is an ordinary corrected recovery awaiting measurement; L046 completes the surviving claims '
        'after its existing principal refutation. This catalogue correction adds no new proof, principal '
        'refutation, measurement, question or Lean credit.')
    new['current_recovery_counts'].update(admitted=93, handled=102, measurement_pending=40,
        pending=3, surviving_claim_obligations=0, completion_obligations=3,
        fully_treated=102, completed_refutation_sources=9)
    for key, additions in [('measurement_pending_original_ids', ['F012']),
        ('handled_mathematical_original_ids', ['F012']),
        ('source_complete_refutation_original_ids', ['L046']),
        ('fully_treated_original_ids', ['F012', 'L046'])]:
        new[key] = sorted(set(new[key]).union(additions))
    return new


def verify(root, require_tracked=False):
    started = time.monotonic()
    root = Path(root).absolute()
    need(root.resolve(strict=True) == root, 'Canonical checkout root required')
    git(root, 'merge-base', '--is-ancestor', BASELINE, 'HEAD')
    registration = json.loads(read(root, REGISTRATION))
    need(registration['schema'] == 'CATALOGUE_COMPLETION_PUBLICATION_LAYER_V1' and
         registration['baseline'] == BASELINE, 'Exact administrative predecessor')
    rows = registration['files']; byname = {r['path']: r for r in rows}
    need(len(rows) == len(byname) and set(byname) == FILES, 'Exact noncyclic seven-file layer')
    for name, row in byname.items():
        need(row == pin_bytes(name, read(root, name)), 'Changed declared administrative export: ' + name)
    inherited = registration['inherited_records']
    expected_inherited = {F012, L046, OLD_REGISTRATION, OLD_CODE, OLD_REVIEW, OLD_CHECKOUT, PREVIOUS}
    need({r['path'] for r in inherited} == expected_inherited and len(inherited) == len(expected_inherited),
         'Complete exact inherited admission/review/code roles')
    inherited_sparse_absent = []
    for row in inherited:
        name = row['path']; b = old(root, name)
        need(row == pin_bytes(name, b), 'Retained acquired authority changed: ' + name)
        if (root / name).exists():
            need(read(root, name) == b, 'Changed materialized acquired authority: ' + name)
        else:
            inherited_sparse_absent.append(name)
    # The large historical global manifest is opaque administrative provenance.
    # Its exact Git object is retained; it is not decoded or promoted to a new manifest.
    m = registration['inherited_publication_manifest']
    need(m == dict(path=PUBLICATION,
         git_blob=git(root, 'rev-parse', BASELINE + ':' + PUBLICATION).decode().strip(),
         bytes=int(git(root, 'cat-file', '-s', BASELINE + ':' + PUBLICATION))),
         'Exact historical global manifest Git identity')
    f = json.loads(read(root, F012)); l = json.loads(read(root, L046))
    need(f['status'] == 'ROOT_ACCEPTED_F012_COMPLETE_SOURCE_TREATMENT' and
         f['ordinary_recovery_credit'] == f['source_completion_credit'] == 1,
         'Existing reviewed F012 complete recovery')
    need(l['status'] == 'ROOT_ACCEPTED_L046_COMPLETE_SOURCE_TREATMENT' and
         l['ordinary_recovery_credit'] == 0 and l['source_completion_credit'] == 1 and
         l['source_claim_rows'] == 44, 'Existing reviewed L046 source completion')
    for a in (f, l):
        need(a['principal_refutation_credit'] == a['new_measurements'] == a['new_original_credit'] ==
             a['new_question_credit'] == a['new_Lean_credit'] == 0 and
             a['whole_source_formalized'] is False and a['compression_factor'] is None,
             'No new measurement, refutation, formalization or question credit')
    fp = pin_bytes(F012, read(root, F012)); lp = pin_bytes(L046, read(root, L046))
    before = old(root, PREVIOUS); actual = json.loads(read(root, CATALOGUE))
    need(actual == successor(json.loads(before), fp, lp, f, l, pin_bytes(PREVIOUS, before)),
         'Exact two-row catalogue successor; no silent other-original change')
    pending = sorted(r['original_id'] for r in actual['entries']
        if r['current_principal_recovery']['status'] == 'PENDING_COMPLETE_RECOVERY')
    need(pending == ['F004', 'F009', 'L026'] and len(actual['fully_treated_original_ids']) == 102 and
         len(actual['measurement_pending_original_ids']) == 40 and
         set(actual['source_complete_refutation_original_ids']) == set(actual['refuted_principal_original_ids']),
         'Exact 102/105 partition with unchanged nine refutations and 53 measurements')
    cp = byname[CATALOGUE]
    for name, key in [(CORPUS, 'active_catalogue'), (PAPERS, 'active_source_catalogue')]:
        previous = json.loads(old(root, name)); previous[key] = cp
        need(json.loads(read(root, name)) == previous, 'Only the exact current catalogue pin changes: ' + name)
    prior_dispatch = old(root, DISPATCH).decode()
    need(prior_dispatch.count(OLD_MAIN) == 1 and read(root, DISPATCH).decode() ==
         prior_dispatch.replace(OLD_MAIN, NEW_MAIN, 1), 'Exact dispatcher-only Source inverse')
    review = json.loads(old(root, OLD_REVIEW))
    need(review['status'] == 'DISTINCT_ACCEPTED_F012_PUBLICATION_REGISTRATION' and
         review['code'] == pin_bytes(OLD_CODE, old(root, OLD_CODE)) and
         review['dispatch'] == pin_bytes(DISPATCH, old(root, DISPATCH)),
         'Old review stays bound to its old code and dispatcher, never retargeted')
    checkout = json.loads(old(root, OLD_CHECKOUT))
    need(checkout['status'] == 'ROOT_ACCEPTED_F012_SELECTED_CHECKOUT' and
         checkout['full_corpus_replay'] is False and checkout['private_source_fallback'] is False and
         checkout['selected_exports_equal'] is True,
         'Inherited selected-checkout scope remains qualified')
    baseline_names = set(git(root, 'ls-tree', '-r', '--name-only', '-z', BASELINE).decode().rstrip('\0').split('\0'))
    tracked = set(git(root, 'ls-files', '-z').decode().rstrip('\0').split('\0'))
    allowed = FILES | {REGISTRATION}
    changed = set(filter(None, git(root, 'diff', '--no-ext-diff', '--no-renames',
        '--name-only', BASELINE, '--').decode().splitlines()))
    need(not changed - allowed and not baseline_names - tracked and not tracked - baseline_names - allowed,
         'Every inherited tracked identity retained except the exact administrative layer')
    pending_tracking = sorted(allowed - tracked)
    need(not require_tracked or not pending_tracking, 'Stage all declared administrative files before final check')
    need(time.monotonic() - started < 120, 'Administrative metadata time limit')
    return dict(status='PASS_CANDIDATE_CATALOGUE_PUBLICATION_LAYER' if pending_tracking else
        'PASS_CATALOGUE_PUBLICATION_LAYER', baseline=BASELINE,
        inherited_publication='retained Git identities and acquired scoped reviews',
        fully_treated=102, mathematical_originals=105, ordinary_recoveries=93,
        principal_refutations=9, measured=53, measurement_pending=40, pending=pending,
        fresh_administrative_exports=len(rows), pending_tracking=pending_tracking,
        inherited_sparse_absent=inherited_sparse_absent,
        fresh_scientific_replay=False, fresh_whole_corpus_replay=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--require-tracked', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.root, args.require_tracked), sort_keys=True))
