"""Prepare reviewable L114 completion metadata; never writes public files."""
from pathlib import Path
import copy
import difflib
import hashlib
import json
import shutil
import subprocess
import sys

if not __debug__:
    raise SystemExit('ordinary Python required')
P = Path(__file__).resolve().parent
F = P.parent
R = Path('/Users/sasha/medusa/math_compression')
STAGE = P / 'stage02'
AUD = 'audit/principal-refutations/L114/complete/v1'
PAPER = 'papers/corrections/L114/v1'
C = P / 'registration_candidate02'


def load(path):
    return json.loads(path.read_text())


def pin(path, base=None):
    data = path.read_bytes()
    return dict(path=str(path.relative_to(base) if base else path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def need(ok, message):
    if not ok:
        raise ValueError(message)


def write(relative, value):
    target = C / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2) + '\n')
    return target


def public_pin(relative):
    return pin(C / 'proposed' / relative, C / 'proposed')


def main():
    need(len(sys.argv) == 1 and not C.exists(), 'fresh no-argument registration preparation')
    need(shutil.disk_usage(P).free >= 4 * 2**30 + 25 * 2**20, '4GiB reserve')
    baseline = subprocess.check_output(['git', '-C', str(R), 'rev-parse', 'HEAD'], text=True).strip()
    need(baseline == '027092205a0a89890326ea53d6ae0aba5509c23f', 'expected L054 predecessor')
    need(not subprocess.check_output(['git', '-C', str(R), 'status', '--porcelain']).strip(), 'clean predecessor')
    op = F / 'publication_operational_root_review'
    root = pin(op / 'manifest.json')
    need(root['sha256'] == '3647336df21368fd20d46be3f464ae7bfa7e746ed84dd7fbee448d66d5d0a067', 'exact portable acceptance')
    need(load(op / 'manifest.json')['status'] == 'ACCEPTED_L114_PORTABLE_COMPLETE_SOURCE_TREATMENT', 'accepted portable status')
    old = load(R / 'audit/corpus/latest.json')
    need([old[k] for k in ['admitted_principal_originals', 'refuted_principal_originals',
                         'handled_mathematical_originals', 'currently_measured_originals',
                         'surviving_claim_obligation_originals', 'completion_obligation_originals']]
         == [92, 9, 101, 53, 6, 10], 'exact predecessor counts')
    C.mkdir()
    # Carry the operational acceptance and all exact inputs with stage-file reuse.
    operational_rows = load(op / 'dependencies.json')
    operational_rows += [dict(r, path=str(op / r['path'])) for r in load(op / 'manifest.json')['exports']]
    operational_rows.append(root)
    mathematical_record = pin(F / 'source_synthesis_root_review/manifest.json')
    need(mathematical_record in operational_rows, 'portable review binds mathematical acceptance')
    need(mathematical_record == load(STAGE / AUD / 'transport.json')['root_acceptance'],
         'same mathematical acceptance in reviewed transport and operational review')
    # The exact stage already carries this content; retain a small readable copy
    # for the admission as well, without inventing another acceptance boundary.
    operational_rows.append(mathematical_record)
    stage_records = load(STAGE / AUD / 'manifest.json')['exports'] + [pin(STAGE / AUD / 'manifest.json', STAGE)]
    stage_by_hash = {r['sha256']: r for r in stage_records}
    premises = load(STAGE / AUD / 'transport.json')['premises']
    premise_by_hash = {r['sha256']: r for r in premises}
    need(len(premises) == len(premise_by_hash) == 263, 'exact accepted documentary/environment boundary')
    logical_premise_occurrences = {(r['original_path'], r['sha256'], r['bytes']) for r in load(STAGE / AUD / 'transport.json')['logical_files'] if r['sha256'] in premise_by_hash}
    objects = {}
    routes = []
    for row in operational_rows:
        source = Path(row['path'])
        need(pin(source) == row, 'unchanged operational input')
        if row['sha256'] in premise_by_hash:
            premise = premise_by_hash[row['sha256']]
            need((row['path'], row['sha256'], row['bytes']) in logical_premise_occurrences, 'exact accepted premise occurrence')
            routes.append(dict(original=row, premise=premise))
            continue
        if row['sha256'] in stage_by_hash:
            target = stage_by_hash[row['sha256']]
        else:
            name = AUD + '/operational/objects/' + row['sha256'] + ('.bin' if source.suffix.lower() == '.md' else source.suffix)
            target = dict(row, path=name)
            if name not in objects:
                dest = C / 'proposed' / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, dest)
                objects[name] = target
        routes.append(dict(original=row, public=target))
    mapping = dict(status='EXACT_L114_PORTABLE_REVIEW_TRANSPORT', original_manifest=root,
                   original_status=load(op / 'manifest.json')['status'], routes=routes, premises=premises,
                   additional_readable_scientific_acceptance=mathematical_record)
    write('proposed/' + AUD + '/operational/mapping.json', mapping)
    original_to_public = {r['original']['path']: r['public'] for r in routes if 'public' in r}
    science = pin(F / 'source_synthesis_root_review/manifest.json')
    need(science['path'] in original_to_public, 'operational closure includes mathematical acceptance')
    claims = load(F / 'source_synthesis/claims.json')
    manuscripts = []
    for ident, stem, title, count in [('L114-completion', 'completion', 'Rank-three Suzuki geometries: results, corrections and realizations', 5), ('L114-realizations', 'realizations', 'Realizations and obstructions for the displayed patterns', 5), ('L114-principal', 'proofs/principal', 'Compatible tori and a missing Suzuki geometry', 4), ('L114-preliminary', 'proofs/preliminary', 'Preliminary statements and their precise scope', 3), ('L114-prime_degree', 'proofs/prime_degree', 'A rank obstruction in prime-degree Suzuki groups', 3), ('L114-restrictions', 'proofs/restrictions', 'Maximal intersections in Suzuki torus normalizers', 5), ('L114-patterns', 'proofs/patterns', 'The necessary patterns when the split torus has prime order', 6), ('L114-markings', 'proofs/markings', 'Panels of eight retained Suzuki markings', 2), ('L114-nonthin8', 'proofs/nonthin8', 'An algebraic local action does not force thinness', 3), ('L114-nonthin32', 'proofs/nonthin32', 'A second failure of the thinness assertion', 2), ('L114-local_rank', 'proofs/local_rank', 'Scalar subspaces and unbounded algebraic local rank', 3), ('L114-common_preliminaries', 'proofs/common_preliminaries', 'Maximal subgroups and elementary reductions for Suzuki geometries', 5), ('L114-normalizer_families', 'proofs/normalizer_families', 'Normalizer fibres in rank-two Suzuki geometries', 8), ('L114-subfield_families', 'proofs/subfield_families', 'Subfield parabolics and the corrected Suzuki classification', 6), ('L114-scalar_subspaces', 'proofs/scalar_subspaces', 'Scalar subspaces in rank-two Suzuki geometries', 4), ('L114-standard_subfields', 'proofs/standard_subfields', 'A missing boundary in the Suzuki subfield construction', 3)]:
        manuscripts.append(dict(id=ident, title=title, physical_pages=count,
            tex=pin(STAGE / PAPER / (stem + '.tex'), STAGE), pdf=pin(STAGE / PAPER / (stem + '.pdf'), STAGE),
            tex_inputs=[], compiler='pdflatex', existing_principal_manuscript_reused=(stem == 'proofs/principal')))
    admission = dict(status='REVIEWED_L114_SOURCE_COMPLETION_REQUIRING_ROOT_PUBLICATION_GATE', source_ids=['L114'],
        disposition_kind='principal_refutation_with_complete_surviving_source_disposition',
        source_identity=claims['source_pdf'], source_edition=claims['source_edition'],
        principal_refutation_admission=pin(R / 'corrections/suzuki-subfields/v1/L114/admission.json', R),
        mathematical_acceptance=original_to_public[science['path']],
        portable_acceptance=original_to_public[root['path']], operational_mapping=public_pin(AUD + '/operational/mapping.json'),
        stage_manifest=pin(STAGE / AUD / 'manifest.json', STAGE), transport=pin(STAGE / AUD / 'transport.json', STAGE),
        portable_checker=pin(STAGE / AUD / 'portable_check.py', STAGE),
        source_claim_ledger=pin(STAGE / PAPER / 'claims.json', STAGE), source_claim_rows=61,
        complete_volume=dict(tex=pin(STAGE / PAPER / 'complete.tex', STAGE), pdf=pin(STAGE / PAPER / 'complete.pdf', STAGE),
                             physical_pages=68, introduction_pages=1, mathematical_pages=67),
        manuscripts=manuscripts, uncertified_extensions=claims['uncertified_extensions'],
        ordinary_recovery_credit=0, principal_refutation_credit=0, new_original_credit=0,
        proposed_source_completion_credit=1, new_measurements=0, new_question_credit=0, new_Lean_credit=0,
        whole_source_formalized=False, compression_factor=None, source_retrieval_performed=False,
        public_gate=AUD + '/root_integration.json')
    write('proposed/' + AUD + '/admission.json', admission)
    ap = public_pin(AUD + '/admission.json')
    updated = copy.deepcopy(old)
    updated.update(surviving_claim_obligation_original_ids=[x for x in old['surviving_claim_obligation_original_ids'] if x != 'L114'],
                   surviving_claim_obligation_originals=5,
                   completion_obligation_original_ids=[x for x in old['completion_obligation_original_ids'] if x != 'L114'],
                   completion_obligation_originals=9, source_complete_refutation_original_ids=sorted(old['source_complete_refutation_original_ids'] + ['L114']),
                   source_complete_refutation_originals=4, fully_treated_original_ids=sorted(old['fully_treated_original_ids'] + ['L114']),
                   fully_treated_originals=96,
                   handled_count_meaning='Principal dispositions only: 92 corrected recoveries and nine principal refutations. F003, L029, L036 and L114 have complete surviving-source dispositions; five other refutations retain surviving-claim obligations.')
    delta = {k: v for k, v in updated.items() if old.get(k) != v}
    write('machine_delta.json', delta)
    registration = dict(status='REVIEWED_L114_SOURCE_COMPLETION_REQUIRING_ROOT_GATES', source_ids=['L114'], admission=ap,
        predecessor_commit=baseline, previous_principal_disposition=old['current_principal_disposition_registration'],
        previous_science_registration=old['current_science_registration'],
        previous_source_completion_registration=old['current_source_completion_registration'], ordinary_recoveries_added=0,
        principal_refutations_added=0, principal_dispositions_added=0, fully_treated_originals_added=1,
        surviving_claim_obligations_closed=['L114'], new_measurements=0, new_question_credit=0, new_Lean_credit=0,
        compression_factor=None, public_gate=AUD + '/root_integration.json')
    write('proposed/' + AUD + '/source_completion_registration.json', registration)
    rp = public_pin(AUD + '/source_completion_registration.json')
    catalogue = load(R / old['active_catalogue']['path'])
    before_entry = copy.deepcopy(next(e for e in catalogue['entries'] if e['original_id'] == 'L114'))
    entry = next(e for e in catalogue['entries'] if e['original_id'] == 'L114')
    entry['current_source_completion'] = dict(status='REVIEWED_COMPLETE_SOURCE_DISPOSITION_AFTER_PRINCIPAL_REFUTATION',
        admission=ap, principal_refutation_preserved=True, ordinary_recovery_credit=0, source_claim_rows=61,
        source_contract='Fixed twenty-one-page edition, Note di Matematica 19(1) (1999), 43--63: the accepted principal refutation is reused; all 61 source claim rows receive explicit treatment, including surviving restrictions, individual realizations, two thinness counterexamples and the unbounded algebraic local-rank family, with attributed classical premises.',
        qualification='This is a complete disposition of the fixed source assertions, not a corrected exhaustive classification of all Suzuki incidence geometries. The frozen volume makes only its stated algebraic higher-rank conclusion. Independent classical premises and the original principal-refutation status remain explicit.',
        whole_source_formalized=False, measured=False, compression_factor=None)
    entry['next_obligation'] = 'No surviving mathematical source-disposition obligation remains for the fixed twenty-one-page article. Preserve the prior principal refutation, explicit source corrections, surviving positive theorems, individual realization results and classical premises. A complete corrected classification is not claimed. No ordinary recovery, new principal refutation or measurement is assigned.'
    catalogue.update(previous_catalogue=old['active_catalogue'], review_revision='L114 receives complete treatment of its surviving source claims after its already registered principal refutation. Ordinary recoveries, principal dispositions and measurements do not change.',
                     source_complete_refutation_original_ids=updated['source_complete_refutation_original_ids'], source_complete_refutation_originals=4,
                     fully_treated_original_ids=updated['fully_treated_original_ids'], fully_treated_originals=96)
    catalogue['current_recovery_counts'].update(surviving_claim_obligations=5, completion_obligations=9,
                                              fully_treated=96, completed_refutation_sources=4)
    catname = 'audit/corpus/accessible106/updates/completion-L114-catalogue.json'
    write('proposed/' + catname, catalogue)
    updated.pop('snapshot')
    updated.update(previous_snapshot=dict(pin(R / 'audit/corpus/latest.json', R), path=AUD + '/previous/audit/corpus/latest.json'),
                   active_catalogue=public_pin(catname), current_source_completion_registration=rp)
    snapname = 'audit/corpus/updates/accessible106-completion-L114.json'
    write('proposed/' + snapname, updated)
    updated['snapshot'] = public_pin(snapname)
    write('proposed/audit/corpus/latest.json', updated)
    native = load(R / 'papers/catalogue_principal_refutations.json')
    target = next(e for e in native['entries'] if e['source_ids'] == ['L114'])
    target['source_completion'] = dict(admission=ap, complete_volume=admission['complete_volume'],
        additional_manuscripts=[m for m in manuscripts if not m['existing_principal_manuscript_reused']],
        principal_manuscript_counted_again=False, measured=False, compression_factor=None)
    native.update(source_complete_original_ids=updated['source_complete_refutation_original_ids'], source_completion_credit=4)
    write('proposed/papers/catalogue_principal_refutations.json', native)
    paper = load(R / 'papers/latest_catalogue.json')
    paper.update(active_source_catalogue=public_pin(catname), principal_refutation_catalogue=public_pin('papers/catalogue_principal_refutations.json'))
    write('proposed/papers/latest_catalogue.json', paper)
    paragraph = 'F003, L029 and L036 now have complete reviewed treatments of their surviving\nsource claims. Thus 95 originals are fully treated: 92 ordinary recoveries\nand three complete source treatments after principal refutations. Six other\nrefuted originals and four without a principal disposition retain completion\nobligations: 10 originals remain. There are 101 principal dispositions and\n92 ordinary recoveries; the stopping condition is unchanged.'
    replacement = 'F003, L029, L036 and L114 now have complete reviewed treatments of their\nsurviving source claims. Thus 96 originals are fully treated: 92 ordinary\nrecoveries and four complete source treatments after principal refutations.\nFive other refuted originals and four without a principal disposition retain\ncompletion obligations: 9 originals remain. There are 101 principal\ndispositions and 92 ordinary recoveries; the stopping condition is unchanged.'
    note = 'The `complete L114 volume <{prefix}papers/corrections/L114/v1/complete.pdf>`_\ntreats all 61 claim rows in the fixed twenty-one-page article on rank-three\nSuzuki geometries. It proves the surviving restriction theorems, gives the\nrealization or obstruction for each displayed pattern, and preserves the\npreviously accepted principal counterexample. Two finite examples disprove\nthe thinness assertions, and a general scalar-subspace construction disproves\nthe stated bound on algebraic local rank. The 68-page reading volume includes\nthe exact common theory and component proofs, with classical premises and\nsource corrections attributed. It does not claim a complete corrected\nclassification or a compression factor. This closes one source obligation\nwithout adding an ordinary recovery, principal refutation, question or Lean\ncredit.\n\n'
    changes = []
    for name, prefix in [('README.rst', ''), ('audit/completion.rst', '../')]:
        before = (R / name).read_text()
        need(before.count(paragraph) == 1, 'exact narrative completion anchor')
        after = before.replace(paragraph, replacement)
        anchor = 'The `complete L036 volume'
        need(after.count(anchor) == 1, 'exact L114 insertion anchor')
        after = after.replace(anchor, note.format(prefix=prefix) + anchor)
        dest = C / 'proposed' / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(after)
        changes.append(dict(path=name, before=pin(R / name, R), after=public_pin(name)))
        (C / (name.replace('/', '_') + '.diff')).write_text(''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='before/' + name, tofile='after/' + name)))
    name = 'audit/protocol.tex'
    before = (R / name).read_text()
    old_scope = 'statement is handled separately from a recovery. F003, L029 and L036 now\nhave complete reviewed treatments of their surviving source claims. Thus 95\noriginals are fully treated: 92 ordinary recoveries and three complete source\ntreatments after principal refutations. Six other refuted sources and\nfour without a principal disposition retain obligations, so 10 originals\nstill require completion. There are 101 principal dispositions and 92\nordinary recoveries; the stopping condition is unchanged.'
    new_scope = 'statement is handled separately from a recovery. F003, L029, L036 and L114 now\nhave complete reviewed treatments of their surviving source claims. Thus 96\noriginals are fully treated: 92 ordinary recoveries and four complete source\ntreatments after principal refutations. Five other refuted sources and\nfour without a principal disposition retain obligations, so 9 originals\nstill require completion. There are 101 principal dispositions and 92\nordinary recoveries; the stopping condition is unchanged.'
    need(before.count(old_scope) == 1, 'exact protocol scope')
    after = before.replace(old_scope, new_scope)
    anchor = "L036's complete source treatment supplies a common double-coset parameter"
    need(after.count(anchor) == 1, 'exact protocol insertion anchor')
    text = "L114's complete source treatment accounts for all 61 claim rows in its fixed\n21-page edition. It proves the surviving restrictions, supplies the individual\nrealizations and obstructions, and retains the accepted principal correction.\nFinite examples in $\\operatorname{Sz}(8)$ and $\\operatorname{Sz}(32)$ refute\nthinness under the source's algebraic local condition. A scalar-subspace\nconstruction gives unbounded algebraic local rank. The 68-page volume retains\nall common theory and component proofs with explicit classical premises.\nIt does not assert an exhaustive corrected classification or a compression\nfactor. This closes one source obligation without a new ordinary recovery,\nprincipal refutation, question or Lean credit.\n\n"
    after = after.replace(anchor, text + anchor)
    dest = C / 'proposed' / name
    dest.write_text(after)
    changes.append(dict(path=name, before=pin(R / name, R), after=public_pin(name)))
    (C / 'audit_protocol.tex.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='before/' + name, tofile='after/' + name)))
    write('narrative_changes.json', changes)
    write('source_entry_delta.json', dict(original_id='L114', before=before_entry,
        added_current_source_completion=entry['current_source_completion'], next_obligation=entry['next_obligation'],
        principal_disposition_unchanged=True, all_other_originals_unchanged=True))
    write('baseline.json', dict(commit=baseline, current_corpus=pin(R / 'audit/corpus/latest.json', R),
          active_catalogue=old['active_catalogue'], preserved_measured_ids=old['measured_original_ids'],
          preserved_recovery_ids=old['admitted_original_ids'], preserved_refutation_ids=old['refuted_principal_original_ids'],
          history_paths=['README.rst', 'audit/completion.rst', 'audit/protocol.tex', 'audit/protocol.pdf',
                         'audit/corpus/latest.json', 'papers/latest_catalogue.json', 'papers/catalogue_principal_refutations.json',
                         'scripts/verify_snapshot.py']))
    write('proposal.json', dict(status='PRIVATE_L114_SOURCE_COMPLETION_REGISTRATION_PROPOSAL',
        baseline=baseline, source_ids=['L114'], stage=pin(STAGE / AUD / 'manifest.json'),
        mathematical_acceptance=science, operational_acceptance=root,
        admission=ap, source_completion_registration=rp, machine_delta=delta,
        public_files_written=False, root_final_gate_required=AUD + '/root_integration.json',
        proposed_paths=[str(p.relative_to(C / 'proposed')) for p in sorted((C / 'proposed').rglob('*')) if p.is_file()],
        installation_and_snapshot_checker='To be supplied after review of this exact semantic and narrative proposal.'))
    print(json.dumps(dict(status='PREPARED_L114_REGISTRATION_CANDIDATE', proposal=pin(C / 'proposal.json'),
                         fully_treated=96, remaining=9, ordinary_recovery_delta=0, public_mutations=0)))


if __name__ == '__main__':
    main()
