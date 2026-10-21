"""Prepare reviewable L029 completion metadata; never writes public files."""
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
AUD = 'audit/principal-refutations/L029/complete/v1'
PAPER = 'papers/corrections/L029/v1'
C = P / 'registration_candidate03'


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
    need(baseline == '8926312d' or baseline.startswith('8926312d'), 'expected L091 predecessor')
    need(not subprocess.check_output(['git', '-C', str(R), 'status', '--porcelain']).strip(), 'clean predecessor')
    op = F / 'portable_completion_root_review'
    root = pin(op / 'manifest.json')
    need(root['sha256'] == 'ac73264839094bda01919dfd60226ff0506157f829b41e8f008a345eb93825d4', 'exact portable acceptance')
    need(load(op / 'manifest.json')['status'] == 'ACCEPTED_L029_PORTABLE_SOURCE_COMPLETION', 'accepted portable status')
    old = load(R / 'audit/corpus/latest.json')
    need([old[k] for k in ['admitted_principal_originals', 'refuted_principal_originals',
                         'handled_mathematical_originals', 'currently_measured_originals',
                         'surviving_claim_obligation_originals', 'completion_obligation_originals']]
         == [91, 9, 100, 53, 9, 14], 'exact predecessor counts')
    C.mkdir()
    # Carry the operational acceptance and all exact inputs with stage-file reuse.
    operational_rows = load(op / 'dependencies.json')
    operational_rows += [dict(r, path=str(op / r['path'])) for r in load(op / 'manifest.json')['exports']]
    operational_rows.append(root)
    mathematical_record = load(op / 'review.json')['mathematical_acceptance']
    need(mathematical_record == load(STAGE / AUD / 'transport.json')['root_acceptance'],
         'same mathematical acceptance in reviewed transport and operational review')
    # The exact stage already carries this content; retain a small readable copy
    # for the admission as well, without inventing another acceptance boundary.
    operational_rows.append(mathematical_record)
    stage_records = load(STAGE / AUD / 'manifest.json')['exports'] + [pin(STAGE / AUD / 'manifest.json', STAGE)]
    stage_by_hash = {r['sha256']: r for r in stage_records}
    objects = {}
    routes = []
    for row in operational_rows:
        source = Path(row['path'])
        need(pin(source) == row, 'unchanged operational input')
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
    mapping = dict(status='EXACT_L029_PORTABLE_REVIEW_TRANSPORT', original_manifest=root,
                   original_status=load(op / 'manifest.json')['status'], routes=routes,
                   additional_readable_scientific_acceptance=mathematical_record)
    write('proposed/' + AUD + '/operational/mapping.json', mapping)
    original_to_public = {r['original']['path']: r['public'] for r in routes}
    science = pin(F / 'source_synthesis_root_review/manifest.json')
    need(science['path'] in original_to_public, 'operational closure includes mathematical acceptance')
    claims = load(F / 'source_synthesis_v1/claims.json')
    manuscripts = []
    for ident, stem, title, count in [
        ('L029-residues', 'residues', 'Coset residues and chamber orbits', 7),
        ('L029-principal-reused', 'proofs/principal', 'A chiral coset geometry with disconnected residues', 5),
        ('L029-panels', 'proofs/panels', 'Panels in the coset construction for a C+-group', 3),
        ('L029-chirality', 'proofs/chirality', 'Chirality without firmness', 2),
    ]:
        manuscripts.append(dict(id=ident, title=title, physical_pages=count,
            tex=pin(STAGE / PAPER / (stem + '.tex'), STAGE), pdf=pin(STAGE / PAPER / (stem + '.pdf'), STAGE),
            tex_inputs=[], compiler='pdflatex', existing_principal_manuscript_reused=(count == 5)))
    admission = dict(status='REVIEWED_L029_SOURCE_COMPLETION_REQUIRING_ROOT_PUBLICATION_GATE', source_ids=['L029'],
        disposition_kind='principal_refutation_with_complete_surviving_source_disposition',
        source_identity=claims['source_pdf'], source_edition=claims['source_edition'],
        principal_refutation_admission=pin(R / 'corrections/chiral-residues/v1/admission.json', R),
        mathematical_acceptance=original_to_public[science['path']],
        portable_acceptance=original_to_public[root['path']], operational_mapping=public_pin(AUD + '/operational/mapping.json'),
        stage_manifest=pin(STAGE / AUD / 'manifest.json', STAGE), transport=pin(STAGE / AUD / 'transport.json', STAGE),
        portable_checker=pin(STAGE / AUD / 'portable_check.py', STAGE),
        source_claim_ledger=pin(STAGE / PAPER / 'claims.json', STAGE), source_claim_rows=19,
        complete_volume=dict(tex=pin(STAGE / PAPER / 'complete.tex', STAGE), pdf=pin(STAGE / PAPER / 'complete.pdf', STAGE),
                             physical_pages=18, introduction_pages=1, mathematical_pages=17),
        manuscripts=manuscripts, general_higher_rank_firmness='UNPROVED_CORRECTED_VARIANT',
        ordinary_recovery_credit=0, principal_refutation_credit=0, new_original_credit=0,
        proposed_source_completion_credit=1, new_measurements=0, new_question_credit=0, new_Lean_credit=0,
        whole_source_formalized=False, compression_factor=None, source_retrieval_performed=False,
        public_gate=AUD + '/root_integration.json')
    write('proposed/' + AUD + '/admission.json', admission)
    ap = public_pin(AUD + '/admission.json')
    updated = copy.deepcopy(old)
    updated.update(surviving_claim_obligation_original_ids=[x for x in old['surviving_claim_obligation_original_ids'] if x != 'L029'],
                   surviving_claim_obligation_originals=8,
                   completion_obligation_original_ids=[x for x in old['completion_obligation_original_ids'] if x != 'L029'],
                   completion_obligation_originals=13, source_complete_refutation_original_ids=['L029'],
                   source_complete_refutation_originals=1, fully_treated_original_ids=sorted(old['admitted_original_ids'] + ['L029']),
                   fully_treated_originals=92,
                   handled_count_meaning='Principal dispositions only: 91 corrected recoveries and nine principal refutations. L029 also has a complete surviving-source disposition; eight other refutations retain surviving-claim obligations.')
    delta = {k: v for k, v in updated.items() if old.get(k) != v}
    write('machine_delta.json', delta)
    registration = dict(status='REVIEWED_L029_SOURCE_COMPLETION_REQUIRING_ROOT_GATES', source_ids=['L029'], admission=ap,
        predecessor_commit=baseline, previous_principal_disposition=old['current_principal_disposition_registration'],
        previous_science_registration=old['current_science_registration'], ordinary_recoveries_added=0,
        principal_refutations_added=0, principal_dispositions_added=0, fully_treated_originals_added=1,
        surviving_claim_obligations_closed=['L029'], new_measurements=0, new_question_credit=0, new_Lean_credit=0,
        compression_factor=None, public_gate=AUD + '/root_integration.json')
    write('proposed/' + AUD + '/source_completion_registration.json', registration)
    rp = public_pin(AUD + '/source_completion_registration.json')
    catalogue = load(R / old['active_catalogue']['path'])
    before_entry = copy.deepcopy(next(e for e in catalogue['entries'] if e['original_id'] == 'L029'))
    entry = next(e for e in catalogue['entries'] if e['original_id'] == 'L029')
    entry['current_source_completion'] = dict(status='REVIEWED_COMPLETE_SOURCE_DISPOSITION_AFTER_PRINCIPAL_REFUTATION',
        admission=ap, principal_refutation_preserved=True, ordinary_recovery_credit=0, source_claim_rows=19,
        source_contract='Final 2021 journal edition: valid source arguments proved, false literal assertions given counterexamples, expressly borrowed results attributed.',
        qualification='General rank-at-least-four C+ firmness without extra action hypotheses remains an unproved corrected variant.',
        whole_source_formalized=False, measured=False, compression_factor=None)
    entry['next_obligation'] = 'No surviving source-disposition obligation remains for the fixed journal edition. Preserve the separate principal refutation, borrowed inputs, rank and firmness qualifications, and unproved corrected higher-rank variant. No ordinary recovery or new measurement is assigned.'
    catalogue.update(previous_catalogue=old['active_catalogue'], review_revision='L029 receives complete treatment of its surviving source claims after its already registered principal refutation. Ordinary recoveries, principal dispositions and measurements do not change.',
                     source_complete_refutation_original_ids=['L029'], source_complete_refutation_originals=1,
                     fully_treated_original_ids=updated['fully_treated_original_ids'], fully_treated_originals=92)
    catalogue['current_recovery_counts'].update(surviving_claim_obligations=8, completion_obligations=13,
                                              fully_treated=92, completed_refutation_sources=1)
    catname = 'audit/corpus/accessible106/updates/completion-L029-catalogue.json'
    write('proposed/' + catname, catalogue)
    updated.pop('snapshot')
    updated.update(previous_snapshot=dict(pin(R / 'audit/corpus/latest.json', R), path=AUD + '/previous/audit/corpus/latest.json'),
                   active_catalogue=public_pin(catname), current_source_completion_registration=rp)
    snapname = 'audit/corpus/updates/accessible106-completion-L029.json'
    write('proposed/' + snapname, updated)
    updated['snapshot'] = public_pin(snapname)
    write('proposed/audit/corpus/latest.json', updated)
    native = load(R / 'papers/catalogue_principal_refutations.json')
    target = next(e for e in native['entries'] if e['source_ids'] == ['L029'])
    target['source_completion'] = dict(admission=ap, complete_volume=admission['complete_volume'],
        additional_manuscripts=[m for m in manuscripts if not m['existing_principal_manuscript_reused']],
        principal_manuscript_counted_again=False, measured=False, compression_factor=None)
    native.update(source_complete_original_ids=['L029'], source_completion_credit=1)
    write('proposed/papers/catalogue_principal_refutations.json', native)
    paper = load(R / 'papers/latest_catalogue.json')
    paper.update(active_source_catalogue=public_pin(catname), principal_refutation_catalogue=public_pin('papers/catalogue_principal_refutations.json'))
    write('proposed/papers/latest_catalogue.json', paper)
    paragraph = ('The nine principal refutations do not close their other source claims.\n'
                 'Their surviving-claim obligations remain open alongside the five originals\n'
                 'without a principal disposition: fourteen originals retain completion work.\n'
                 'The stopping condition requires those obligations to be settled; the count of\n'
                 '100 principal dispositions is not a count of 100 completely recovered sources.')
    replacement = ('L029 now also has a complete reviewed treatment of its surviving source claims.\n'
                   'Thus 92 originals are fully treated: 91 ordinary recoveries and one complete\n'
                   'source treatment after a principal refutation. Eight other refuted originals\n'
                   'and five without a principal disposition retain completion obligations: 13\n'
                   'originals remain. The principal-disposition count stays 100, the ordinary\n'
                   'recovery count stays 91, and the stopping condition is unchanged.')
    note = ('The `complete L029 volume <{prefix}papers/corrections/L029/v1/complete.pdf>`_\n'
            'now treats all 19 source claims. Seven synthesis pages prove the valid\n'
            'coset, residue and chamber component arguments; the accepted five-page\n'
            'principal counterexample and three- and two-page auxiliary proofs follow\n'
            'unchanged. The rank-three result is recovered, while the omitted firmness\n'
            'and rank restrictions are corrected separately. General C-plus firmness\n'
            'in rank at least four remains an unproved corrected variant. Completing\n'
            'this source leaves the ordinary recovery and principal refutation counts\n'
            'unchanged, and adds no measurement, question or Lean credit.\n\n')
    changes = []
    for name, prefix in [('README.rst', ''), ('audit/completion.rst', '../')]:
        before = (R / name).read_text()
        need(before.count(paragraph) == 1, 'exact narrative completion anchor')
        after = before.replace(paragraph, replacement)
        anchor = 'The `Suzuki geometry corrections'
        need(after.count(anchor) == 1, 'exact L029 insertion anchor')
        after = after.replace(anchor, note.format(prefix=prefix) + anchor)
        dest = C / 'proposed' / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(after)
        changes.append(dict(path=name, before=pin(R / name, R), after=public_pin(name)))
        (C / (name.replace('/', '_') + '.diff')).write_text(''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='before/' + name, tofile='after/' + name)))
    name = 'audit/protocol.tex'
    before = (R / name).read_text()
    old_scope = ('statement is handled separately from a recovery. The nine refuted originals\n'
                 'retain surviving-claim obligations; together with the five pending originals,\n'
                 'fourteen originals still require completion work. The count of 100 principal\n'
                 'dispositions does not assert complete recovery of 100 sources.')
    new_scope = ('statement is handled separately from a recovery. L029 now has a complete\n'
                 'reviewed treatment of its surviving source claims. Thus 92 originals are\n'
                 'fully treated: 91 ordinary recoveries and one source treatment after a\n'
                 'principal refutation. Eight other refuted sources and five without a\n'
                 'principal disposition retain obligations, so 13 originals still require\n'
                 'completion. The 100 principal dispositions and 91 ordinary recoveries\n'
                 'remain unchanged.')
    need(before.count(old_scope) == 1, 'exact protocol scope')
    after = before.replace(old_scope, new_scope)
    anchor = 'The Suzuki geometry corrections'
    # Insert beside the principal discussion using the next source paragraph.
    if anchor not in after:
        anchor = 'L110'
    at = after.find(anchor, after.find('F003 has'))
    need(at >= 0, 'protocol L029 neighbourhood')
    # Use a paragraph boundary, avoiding splitting a sentence or macro.
    at = after.rfind('\n\n', 0, at) + 2
    text = ("L029's complete source treatment supplies seven synthesis\n"
            'pages and the unchanged five-, three- and two-page accepted proofs,\n'
            'with one introduction page in the 18-page reading volume. The 19 source\n'
            'rows distinguish valid recovered arguments, the principal refutation,\n'
            'auxiliary corrections and borrowed background. General firmness in rank\n'
            'at least four remains an unproved corrected variant. The ordinary recovery\n'
            'and principal refutation counts remain unchanged; no measurement, question\n'
            'or Lean credit is added.\n\n')
    after = after[:at] + text + after[at:]
    dest = C / 'proposed' / name
    dest.write_text(after)
    changes.append(dict(path=name, before=pin(R / name, R), after=public_pin(name)))
    (C / 'audit_protocol.tex.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='before/' + name, tofile='after/' + name)))
    write('narrative_changes.json', changes)
    write('source_entry_delta.json', dict(original_id='L029', before=before_entry,
        added_current_source_completion=entry['current_source_completion'], next_obligation=entry['next_obligation'],
        principal_disposition_unchanged=True, all_other_originals_unchanged=True))
    write('baseline.json', dict(commit=baseline, current_corpus=pin(R / 'audit/corpus/latest.json', R),
          active_catalogue=old['active_catalogue'], preserved_measured_ids=old['measured_original_ids'],
          preserved_recovery_ids=old['admitted_original_ids'], preserved_refutation_ids=old['refuted_principal_original_ids'],
          history_paths=['README.rst', 'audit/completion.rst', 'audit/protocol.tex', 'audit/protocol.pdf',
                         'audit/corpus/latest.json', 'papers/latest_catalogue.json', 'papers/catalogue_principal_refutations.json',
                         'scripts/verify_snapshot.py']))
    write('proposal.json', dict(status='PRIVATE_L029_SOURCE_COMPLETION_REGISTRATION_PROPOSAL',
        baseline=baseline, source_ids=['L029'], stage=pin(STAGE / AUD / 'manifest.json'),
        mathematical_acceptance=science, operational_acceptance=root,
        admission=ap, source_completion_registration=rp, machine_delta=delta,
        public_files_written=False, root_final_gate_required=AUD + '/root_integration.json',
        proposed_paths=[str(p.relative_to(C / 'proposed')) for p in sorted((C / 'proposed').rglob('*')) if p.is_file()],
        installation_and_snapshot_checker='To be supplied after review of this exact semantic and narrative proposal.'))
    print(json.dumps(dict(status='PREPARED_L029_REGISTRATION_CANDIDATE', proposal=pin(C / 'proposal.json'),
                         fully_treated=92, remaining=13, ordinary_recovery_delta=0, public_mutations=0)))


if __name__ == '__main__':
    main()
