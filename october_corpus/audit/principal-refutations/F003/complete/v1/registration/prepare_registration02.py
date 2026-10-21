"""Prepare reviewable F003 completion metadata; never writes public files."""
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
STAGE = P / 'stage01'
AUD = 'audit/principal-refutations/F003/complete/v1'
PAPER = 'papers/corrections/F003/v1'
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
    need(baseline == '8993ad2c' or baseline.startswith('8993ad2c'), 'expected L029 predecessor')
    need(not subprocess.check_output(['git', '-C', str(R), 'status', '--porcelain']).strip(), 'clean predecessor')
    op = F / 'portable_completion_root_review'
    root = pin(op / 'manifest.json')
    need(root['sha256'] == 'c7e196475a11be6243ef7863253336e8c6fa5d03e6c0d1e36316a89c5fa55386', 'exact portable acceptance')
    need(load(op / 'manifest.json')['status'] == 'ACCEPTED_F003_PORTABLE_COMPLETE_SOURCE_TREATMENT', 'accepted portable status')
    old = load(R / 'audit/corpus/latest.json')
    need([old[k] for k in ['admitted_principal_originals', 'refuted_principal_originals',
                         'handled_mathematical_originals', 'currently_measured_originals',
                         'surviving_claim_obligation_originals', 'completion_obligation_originals']]
         == [91, 9, 100, 53, 8, 13], 'exact predecessor counts')
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
    need(len(premises) == len(premise_by_hash) == 6, 'exact accepted six-premise boundary')
    objects = {}
    routes = []
    for row in operational_rows:
        source = Path(row['path'])
        need(pin(source) == row, 'unchanged operational input')
        if row['sha256'] in premise_by_hash:
            premise = premise_by_hash[row['sha256']]
            need(row['bytes'] == premise['bytes'] and row['path'] == premise['exact_locator'], 'canonical documentary premise')
            routes.append(dict(original=row, documentary_premise=premise))
            continue
        if row['sha256'] in stage_by_hash:
            target = stage_by_hash[row['sha256']]
        else:
            name = AUD + '/operational/objects/' + row['sha256'] + source.suffix
            target = dict(row, path=name)
            if name not in objects:
                dest = C / 'proposed' / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, dest)
                objects[name] = target
        routes.append(dict(original=row, public=target))
    mapping = dict(status='EXACT_F003_PORTABLE_REVIEW_TRANSPORT', original_manifest=root,
                   original_status=load(op / 'manifest.json')['status'], routes=routes, documentary_premises=premises,
                   additional_readable_scientific_acceptance=mathematical_record)
    write('proposed/' + AUD + '/operational/mapping.json', mapping)
    original_to_public = {r['original']['path']: r['public'] for r in routes if 'public' in r}
    science = pin(F / 'source_synthesis_root_review/manifest.json')
    need(science['path'] in original_to_public, 'operational closure includes mathematical acceptance')
    claims = load(F / 'source_synthesis_v1/claims.json')
    manuscripts = []
    for ident, stem, title, count in [
        ('F003-symmetric', 'symmetric', 'Symmetric matrices in the Suzuki group and the scope of a rank argument', 6),
        ('F003-principal-reused', 'proofs/principal', 'A chiral 4-polytope with automorphism group Sz(32768)', 5),
    ]:
        manuscripts.append(dict(id=ident, title=title, physical_pages=count,
            tex=pin(STAGE / PAPER / (stem + '.tex'), STAGE), pdf=pin(STAGE / PAPER / (stem + '.pdf'), STAGE),
            tex_inputs=[], compiler='pdflatex', existing_principal_manuscript_reused=(count == 5)))
    admission = dict(status='REVIEWED_F003_SOURCE_COMPLETION_REQUIRING_ROOT_PUBLICATION_GATE', source_ids=['F003'],
        disposition_kind='principal_refutation_with_complete_surviving_source_disposition',
        source_identity=claims['source_pdf'], source_edition=claims['source_edition'],
        principal_refutation_admission=pin(R / 'corrections/suzuki-rank/v1/admission.json', R),
        mathematical_acceptance=original_to_public[science['path']],
        portable_acceptance=original_to_public[root['path']], operational_mapping=public_pin(AUD + '/operational/mapping.json'),
        stage_manifest=pin(STAGE / AUD / 'manifest.json', STAGE), transport=pin(STAGE / AUD / 'transport.json', STAGE),
        portable_checker=pin(STAGE / AUD / 'portable_check.py', STAGE),
        source_claim_ledger=pin(STAGE / PAPER / 'claims.json', STAGE), source_claim_rows=19,
        complete_volume=dict(tex=pin(STAGE / PAPER / 'complete.tex', STAGE), pdf=pin(STAGE / PAPER / 'complete.pdf', STAGE),
                             physical_pages=12, introduction_pages=1, mathematical_pages=11),
        manuscripts=manuscripts, uncertified_extensions=claims['uncertified_extensions'],
        ordinary_recovery_credit=0, principal_refutation_credit=0, new_original_credit=0,
        proposed_source_completion_credit=1, new_measurements=0, new_question_credit=0, new_Lean_credit=0,
        whole_source_formalized=False, compression_factor=None, source_retrieval_performed=False,
        public_gate=AUD + '/root_integration.json')
    write('proposed/' + AUD + '/admission.json', admission)
    ap = public_pin(AUD + '/admission.json')
    updated = copy.deepcopy(old)
    updated.update(surviving_claim_obligation_original_ids=[x for x in old['surviving_claim_obligation_original_ids'] if x != 'F003'],
                   surviving_claim_obligation_originals=7,
                   completion_obligation_original_ids=[x for x in old['completion_obligation_original_ids'] if x != 'F003'],
                   completion_obligation_originals=12, source_complete_refutation_original_ids=sorted(old['source_complete_refutation_original_ids'] + ['F003']),
                   source_complete_refutation_originals=2, fully_treated_original_ids=sorted(old['fully_treated_original_ids'] + ['F003']),
                   fully_treated_originals=93,
                   handled_count_meaning='Principal dispositions only: 91 corrected recoveries and nine principal refutations. F003 and L029 have complete surviving-source dispositions; seven other refutations retain surviving-claim obligations.')
    delta = {k: v for k, v in updated.items() if old.get(k) != v}
    write('machine_delta.json', delta)
    registration = dict(status='REVIEWED_F003_SOURCE_COMPLETION_REQUIRING_ROOT_GATES', source_ids=['F003'], admission=ap,
        predecessor_commit=baseline, previous_principal_disposition=old['current_principal_disposition_registration'],
        previous_science_registration=old['current_science_registration'],
        previous_source_completion_registration=old['current_source_completion_registration'], ordinary_recoveries_added=0,
        principal_refutations_added=0, principal_dispositions_added=0, fully_treated_originals_added=1,
        surviving_claim_obligations_closed=['F003'], new_measurements=0, new_question_credit=0, new_Lean_credit=0,
        compression_factor=None, public_gate=AUD + '/root_integration.json')
    write('proposed/' + AUD + '/source_completion_registration.json', registration)
    rp = public_pin(AUD + '/source_completion_registration.json')
    catalogue = load(R / old['active_catalogue']['path'])
    before_entry = copy.deepcopy(next(e for e in catalogue['entries'] if e['original_id'] == 'F003'))
    entry = next(e for e in catalogue['entries'] if e['original_id'] == 'F003')
    entry['current_source_completion'] = dict(status='REVIEWED_COMPLETE_SOURCE_DISPOSITION_AFTER_PRINCIPAL_REFUTATION',
        admission=ap, principal_refutation_preserved=True, ordinary_recovery_credit=0, source_claim_rows=19,
        source_contract='Fixed arXiv:2010.04080v1, 8 October 2020: the principal refutation is reused; the valid matrix equations and all six conditional cases are proved, the defect and source typos corrected, and cited premises attributed.',
        qualification='This treats only the specified four-page source; it does not classify all chiral Suzuki polytopes or claim a result about later editions.',
        whole_source_formalized=False, measured=False, compression_factor=None)
    entry['next_obligation'] = 'No surviving source-disposition obligation remains for the fixed four-page v1. Preserve the separate principal refutation, explicit structural premises, corrected full matrix criterion, and conditional stronger-system classification. No ordinary recovery or new measurement is assigned.'
    catalogue.update(previous_catalogue=old['active_catalogue'], review_revision='F003 receives complete treatment of its surviving source claims after its already registered principal refutation. Ordinary recoveries, principal dispositions and measurements do not change.',
                     source_complete_refutation_original_ids=updated['source_complete_refutation_original_ids'], source_complete_refutation_originals=2,
                     fully_treated_original_ids=updated['fully_treated_original_ids'], fully_treated_originals=93)
    catalogue['current_recovery_counts'].update(surviving_claim_obligations=7, completion_obligations=12,
                                              fully_treated=93, completed_refutation_sources=2)
    catname = 'audit/corpus/accessible106/updates/completion-F003-catalogue.json'
    write('proposed/' + catname, catalogue)
    updated.pop('snapshot')
    updated.update(previous_snapshot=dict(pin(R / 'audit/corpus/latest.json', R), path=AUD + '/previous/audit/corpus/latest.json'),
                   active_catalogue=public_pin(catname), current_source_completion_registration=rp)
    snapname = 'audit/corpus/updates/accessible106-completion-F003.json'
    write('proposed/' + snapname, updated)
    updated['snapshot'] = public_pin(snapname)
    write('proposed/audit/corpus/latest.json', updated)
    native = load(R / 'papers/catalogue_principal_refutations.json')
    target = next(e for e in native['entries'] if e['source_ids'] == ['F003'])
    target['source_completion'] = dict(admission=ap, complete_volume=admission['complete_volume'],
        additional_manuscripts=[m for m in manuscripts if not m['existing_principal_manuscript_reused']],
        principal_manuscript_counted_again=False, measured=False, compression_factor=None)
    native.update(source_complete_original_ids=updated['source_complete_refutation_original_ids'], source_completion_credit=2)
    write('proposed/papers/catalogue_principal_refutations.json', native)
    paper = load(R / 'papers/latest_catalogue.json')
    paper.update(active_source_catalogue=public_pin(catname), principal_refutation_catalogue=public_pin('papers/catalogue_principal_refutations.json'))
    write('proposed/papers/latest_catalogue.json', paper)
    paragraph = ('L029 now also has a complete reviewed treatment of its surviving source claims.\n'
                 'Thus 92 originals are fully treated: 91 ordinary recoveries and one complete\n'
                 'source treatment after a principal refutation. Eight other refuted originals\n'
                 'and five without a principal disposition retain completion obligations: 13\n'
                 'originals remain. The principal-disposition count stays 100, the ordinary\n'
                 'recovery count stays 91, and the stopping condition is unchanged.')
    replacement = ('F003 and L029 now have complete reviewed treatments of their surviving source\n'
                   'claims. Thus 93 originals are fully treated: 91 ordinary recoveries and two\n'
                   'complete source treatments after principal refutations. Seven other refuted\n'
                   'originals and five without a principal disposition retain completion\n'
                   'obligations: 12 originals remain. The principal-disposition count stays 100,\n'
                   'the ordinary recovery count stays 91, and the stopping condition is unchanged.')
    note = ('The `complete F003 volume <{prefix}papers/corrections/F003/v1/complete.pdf>`_\n'
            'treats all 19 source rows in the fixed four-page preprint. Six supplement\n'
            'pages prove the corrected criterion for symmetric Suzuki matrices and\n'
            'retain all six source algebra cases and the final generation argument\n'
            'under their exact hypotheses. The accepted five-page rank-four\n'
            'counterexample follows unchanged. This closes the surviving source\n'
            'obligation without adding a recovery, refutation, measurement or Lean credit.\n\n')
    changes = []
    for name, prefix in [('README.rst', ''), ('audit/completion.rst', '../')]:
        before = (R / name).read_text()
        need(before.count(paragraph) == 1, 'exact narrative completion anchor')
        after = before.replace(paragraph, replacement)
        anchor = 'The `complete L029 volume'
        need(after.count(anchor) == 1, 'exact F003 insertion anchor')
        after = after.replace(anchor, note.format(prefix=prefix) + anchor)
        dest = C / 'proposed' / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(after)
        changes.append(dict(path=name, before=pin(R / name, R), after=public_pin(name)))
        (C / (name.replace('/', '_') + '.diff')).write_text(''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='before/' + name, tofile='after/' + name)))
    name = 'audit/protocol.tex'
    before = (R / name).read_text()
    old_scope = ('statement is handled separately from a recovery. L029 now has a complete\n'
                 'reviewed treatment of its surviving source claims. Thus 92 originals are\n'
                 'fully treated: 91 ordinary recoveries and one source treatment after a\n'
                 'principal refutation. Eight other refuted sources and five without a\n'
                 'principal disposition retain obligations, so 13 originals still require\n'
                 'completion. The 100 principal dispositions and 91 ordinary recoveries\n'
                 'remain unchanged.')
    new_scope = ('statement is handled separately from a recovery. F003 and L029 now have\n'
                 'complete reviewed treatments of their surviving source claims. Thus 93\n'
                 'originals are fully treated: 91 ordinary recoveries and two complete source\n'
                 'treatments after principal refutations. Seven other refuted sources and\n'
                 'five without a principal disposition retain obligations, so 12 originals\n'
                 'still require completion. The 100 principal dispositions and 91 ordinary\n'
                 'recoveries remain unchanged.')
    need(before.count(old_scope) == 1, 'exact protocol scope')
    after = before.replace(old_scope, new_scope)
    anchor = "L029's complete source treatment supplies seven synthesis"
    need(after.count(anchor) == 1, 'exact protocol insertion anchor')
    text = ("F003's complete source treatment supplies six supplement pages and the\n"
            'unchanged five-page accepted rank-four counterexample, with one cover in\n'
            'the 12-page reading volume. Its 19 source rows separate the corrected\n'
            'matrix criterion, the six valid cases for the stronger system, the\n'
            'conditional generation argument, the principal refutation and cited\n'
            'premises. The fixed edition is arXiv:2010.04080v1 of 8 October 2020.\n'
            'No additional recovery, refutation, measurement, question or Lean credit\n'
            'is added.\n\n')
    after = after.replace(anchor, text + anchor)
    dest = C / 'proposed' / name
    dest.write_text(after)
    changes.append(dict(path=name, before=pin(R / name, R), after=public_pin(name)))
    (C / 'audit_protocol.tex.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='before/' + name, tofile='after/' + name)))
    write('narrative_changes.json', changes)
    write('source_entry_delta.json', dict(original_id='F003', before=before_entry,
        added_current_source_completion=entry['current_source_completion'], next_obligation=entry['next_obligation'],
        principal_disposition_unchanged=True, all_other_originals_unchanged=True))
    write('baseline.json', dict(commit=baseline, current_corpus=pin(R / 'audit/corpus/latest.json', R),
          active_catalogue=old['active_catalogue'], preserved_measured_ids=old['measured_original_ids'],
          preserved_recovery_ids=old['admitted_original_ids'], preserved_refutation_ids=old['refuted_principal_original_ids'],
          history_paths=['README.rst', 'audit/completion.rst', 'audit/protocol.tex', 'audit/protocol.pdf',
                         'audit/corpus/latest.json', 'papers/latest_catalogue.json', 'papers/catalogue_principal_refutations.json',
                         'scripts/verify_snapshot.py']))
    write('proposal.json', dict(status='PRIVATE_F003_SOURCE_COMPLETION_REGISTRATION_PROPOSAL',
        baseline=baseline, source_ids=['F003'], stage=pin(STAGE / AUD / 'manifest.json'),
        mathematical_acceptance=science, operational_acceptance=root,
        admission=ap, source_completion_registration=rp, machine_delta=delta,
        public_files_written=False, root_final_gate_required=AUD + '/root_integration.json',
        proposed_paths=[str(p.relative_to(C / 'proposed')) for p in sorted((C / 'proposed').rglob('*')) if p.is_file()],
        installation_and_snapshot_checker='To be supplied after review of this exact semantic and narrative proposal.'))
    print(json.dumps(dict(status='PREPARED_F003_REGISTRATION_CANDIDATE', proposal=pin(C / 'proposal.json'),
                         fully_treated=93, remaining=12, ordinary_recovery_delta=0, public_mutations=0)))


if __name__ == '__main__':
    main()
