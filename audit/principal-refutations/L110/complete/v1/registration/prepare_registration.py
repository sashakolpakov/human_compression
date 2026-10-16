"""Prepare reviewable L110 completion metadata; never writes public files."""
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
AUD = 'audit/principal-refutations/L110/complete/v1'
PAPER = 'papers/corrections/L110/v1'
C = P / 'registration_candidate01'


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
    need(baseline == '70bc355bc5dff1ea86b1b42ac836bfa3136bd71a', 'expected L114 predecessor')
    need(not subprocess.check_output(['git', '-C', str(R), 'status', '--porcelain']).strip(), 'clean predecessor')
    op = F / 'higher_publication_operational_root_review'
    root = pin(op / 'manifest.json')
    need(root['sha256'] == '9f552eea93133033c1810752bb6d1a4e014b737d31b318549d01731da03f8794', 'exact portable acceptance')
    need(load(op / 'manifest.json')['status'] == 'ACCEPTED_L110_PORTABLE_COMPLETE_SOURCE_TREATMENT', 'accepted portable status')
    old = load(R / 'audit/corpus/latest.json')
    need([old[k] for k in ['admitted_principal_originals', 'refuted_principal_originals',
                         'handled_mathematical_originals', 'currently_measured_originals',
                         'surviving_claim_obligation_originals', 'completion_obligation_originals']]
         == [92, 9, 101, 53, 5, 9], 'exact predecessor counts')
    C.mkdir()
    # Carry the operational acceptance and all exact inputs with stage-file reuse.
    operational_rows = load(op / 'dependencies.json')
    operational_rows += [dict(r, path=str(op / r['path'])) for r in load(op / 'manifest.json')['exports']]
    operational_rows.append(root)
    mathematical_record = pin(F / 'higher_source_root_review/manifest.json')
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
    need(len(premises) == len(premise_by_hash) == 273, 'exact accepted documentary/environment boundary')
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
    mapping = dict(status='EXACT_L110_PORTABLE_REVIEW_TRANSPORT', original_manifest=root,
                   original_status=load(op / 'manifest.json')['status'], routes=routes, premises=premises,
                   additional_readable_scientific_acceptance=mathematical_record)
    write('proposed/' + AUD + '/operational/mapping.json', mapping)
    original_to_public = {r['original']['path']: r['public'] for r in routes if 'public' in r}
    science = pin(F / 'higher_source_root_review/manifest.json')
    need(science['path'] in original_to_public, 'operational closure includes mathematical acceptance')
    claims = load(F / 'higher_source_synthesis02/claims.json')
    manuscripts = []
    for ident, stem, title, count in [('L110-completion', 'completion', 'Subfield descent and the higher-rank Suzuki constructions', 5), ('L110-principal_boundary', 'proofs/principal_boundary', 'A missing boundary in the Suzuki subfield construction', 3), ('L110-prime_extensions', 'proofs/prime_extensions', 'Prime subfield residues do not extend to rank four', 4), ('L110-higher_obstructions', 'proofs/higher_obstructions', 'Obstructions to five prescribed Suzuki constructions', 3), ('L110-split_families', 'proofs/split_families', 'Scalar fields and split torus families', 3), ('L110-split_necessity', 'proofs/split_necessity', 'Extensions of the split affine residues', 4), ('L110-torus_necessity', 'proofs/torus_necessity', 'Extensions of residues containing subfield groups and tori', 5), ('L110-descent', 'proofs/descent', 'Field descent and compatible tori', 7), ('L110-torus_families', 'proofs/torus_families', 'Subfield and torus geometries', 4), ('L110-pure_mixed', 'proofs/pure_mixed', 'Pure subfield geometries and a scalar obstruction', 5), ('L110-diagrams', 'proofs/diagrams', 'Diagrams of the surviving prescribed families', 2), ('L110-local_geometry', 'proofs/local_geometry', 'Scalar subspaces and flag transitivity', 2), ('L110-preliminary', 'proofs/preliminary', 'Preliminary statements and their precise scope', 3), ('L110-prime_degree', 'proofs/prime_degree', 'A rank obstruction in prime-degree Suzuki groups', 3), ('L110-restrictions', 'proofs/restrictions', 'Maximal intersections in Suzuki torus normalizers', 5), ('L110-patterns', 'proofs/patterns', 'The necessary patterns when the split torus has prime order', 6), ('L110-realizations', 'proofs/realizations', 'Realizations and obstructions for the displayed patterns', 5), ('L110-principal', 'proofs/principal', 'Compatible tori and a missing Suzuki geometry', 4), ('L110-nonthin8', 'proofs/nonthin8', 'An algebraic local action does not force thinness', 3), ('L110-nonthin32', 'proofs/nonthin32', 'A second failure of the thinness assertion', 2), ('L110-local_rank', 'proofs/local_rank', 'Scalar subspaces and unbounded algebraic local rank', 3), ('L110-scalar_subspaces', 'proofs/scalar_subspaces', 'Scalar subspaces in rank-two Suzuki geometries', 4), ('L110-common_preliminaries', 'proofs/common_preliminaries', 'Maximal subgroups and elementary reductions for Suzuki geometries', 5), ('L110-normalizer_families', 'proofs/normalizer_families', 'Normalizer fibres in rank-two Suzuki geometries', 8), ('L110-subfield_families', 'proofs/subfield_families', 'Subfield parabolics and the corrected Suzuki classification', 6)]:
        manuscripts.append(dict(id=ident, title=title, physical_pages=count,
            tex=pin(STAGE / PAPER / (stem + '.tex'), STAGE), pdf=pin(STAGE / PAPER / (stem + '.pdf'), STAGE),
            tex_inputs=[], compiler='pdflatex', existing_principal_manuscript_reused=(stem == 'proofs/principal_boundary')))
    admission = dict(status='REVIEWED_L110_SOURCE_COMPLETION_REQUIRING_ROOT_PUBLICATION_GATE', source_ids=['L110'],
        disposition_kind='principal_refutation_with_complete_surviving_source_disposition',
        source_identity=claims['source_pdf'], source_edition=claims['source_edition'],
        principal_refutation_admission=pin(R / 'corrections/suzuki-subfields/v1/L110/admission.json', R),
        mathematical_acceptance=original_to_public[science['path']],
        portable_acceptance=original_to_public[root['path']], operational_mapping=public_pin(AUD + '/operational/mapping.json'),
        stage_manifest=pin(STAGE / AUD / 'manifest.json', STAGE), transport=pin(STAGE / AUD / 'transport.json', STAGE),
        portable_checker=pin(STAGE / AUD / 'portable_check.py', STAGE),
        source_claim_ledger=pin(STAGE / PAPER / 'claims.json', STAGE), source_claim_rows=63,
        complete_volume=dict(tex=pin(STAGE / PAPER / 'complete.tex', STAGE), pdf=pin(STAGE / PAPER / 'complete.pdf', STAGE),
                             physical_pages=105, introduction_pages=1, mathematical_pages=104),
        manuscripts=manuscripts, uncertified_extensions=claims['uncertified_extensions'],
        ordinary_recovery_credit=0, principal_refutation_credit=0, new_original_credit=0,
        proposed_source_completion_credit=1, new_measurements=0, new_question_credit=0, new_Lean_credit=0,
        whole_source_formalized=False, compression_factor=None, source_retrieval_performed=False,
        public_gate=AUD + '/root_integration.json')
    write('proposed/' + AUD + '/admission.json', admission)
    ap = public_pin(AUD + '/admission.json')
    updated = copy.deepcopy(old)
    updated.update(surviving_claim_obligation_original_ids=[x for x in old['surviving_claim_obligation_original_ids'] if x != 'L110'],
                   surviving_claim_obligation_originals=4,
                   completion_obligation_original_ids=[x for x in old['completion_obligation_original_ids'] if x != 'L110'],
                   completion_obligation_originals=8, source_complete_refutation_original_ids=sorted(old['source_complete_refutation_original_ids'] + ['L110']),
                   source_complete_refutation_originals=5, fully_treated_original_ids=sorted(old['fully_treated_original_ids'] + ['L110']),
                   fully_treated_originals=97,
                   handled_count_meaning='Principal dispositions only: 92 corrected recoveries and nine principal refutations. F003, L029, L036, L110 and L114 have complete surviving-source dispositions; four other refutations retain surviving-claim obligations.')
    delta = {k: v for k, v in updated.items() if old.get(k) != v}
    write('machine_delta.json', delta)
    registration = dict(status='REVIEWED_L110_SOURCE_COMPLETION_REQUIRING_ROOT_GATES', source_ids=['L110'], admission=ap,
        predecessor_commit=baseline, previous_principal_disposition=old['current_principal_disposition_registration'],
        previous_science_registration=old['current_science_registration'],
        previous_source_completion_registration=old['current_source_completion_registration'], ordinary_recoveries_added=0,
        principal_refutations_added=0, principal_dispositions_added=0, fully_treated_originals_added=1,
        surviving_claim_obligations_closed=['L110'], new_measurements=0, new_question_credit=0, new_Lean_credit=0,
        compression_factor=None, public_gate=AUD + '/root_integration.json')
    write('proposed/' + AUD + '/source_completion_registration.json', registration)
    rp = public_pin(AUD + '/source_completion_registration.json')
    catalogue = load(R / old['active_catalogue']['path'])
    before_entry = copy.deepcopy(next(e for e in catalogue['entries'] if e['original_id'] == 'L110'))
    entry = next(e for e in catalogue['entries'] if e['original_id'] == 'L110')
    entry['current_source_completion'] = dict(status='REVIEWED_COMPLETE_SOURCE_DISPOSITION_AFTER_PRINCIPAL_REFUTATION',
        admission=ap, principal_refutation_preserved=True, ordinary_recovery_credit=0, source_claim_rows=63,
        source_contract='Fixed twenty-page edition, Note di Matematica 20(1) (2000/2001), 1--20: all 63 source claim rows receive explicit treatment. The principal boundary counterexample is retained. General proofs settle the prime-residue nonextension claims, all five conditional rank-four extension necessities and the asserted higher constructions, with literal and intended statements distinguished.',
        qualification='This completely disposes of the fixed source assertions, not a corrected exhaustive classification of arbitrary subgroup positions. The source excludes Sz(2) from Suzuki type. Classical premises, conditional diagrams and the unproved stronger variants are explicit. The separate scalar-coordinate family is proved flag-transitive, thick, residually connected and locally two-transitive in arbitrary rank.',
        whole_source_formalized=False, measured=False, compression_factor=None)
    entry['next_obligation'] = 'No surviving mathematical source-disposition obligation remains for the fixed twenty-page article. Retain the principal refutation, exact residue hypotheses, source conventions, corrected constructions and classical premises. No complete corrected classification, ordinary recovery, new principal refutation or measurement is assigned.'
    catalogue.update(previous_catalogue=old['active_catalogue'], review_revision='L110 receives complete treatment of its surviving source claims after its already registered principal refutation. Ordinary recoveries, principal dispositions and measurements do not change.',
                     source_complete_refutation_original_ids=updated['source_complete_refutation_original_ids'], source_complete_refutation_originals=5,
                     fully_treated_original_ids=updated['fully_treated_original_ids'], fully_treated_originals=97)
    catalogue['current_recovery_counts'].update(surviving_claim_obligations=4, completion_obligations=8,
                                              fully_treated=97, completed_refutation_sources=5)
    catname = 'audit/corpus/accessible106/updates/completion-L110-catalogue.json'
    write('proposed/' + catname, catalogue)
    updated.pop('snapshot')
    updated.update(previous_snapshot=dict(pin(R / 'audit/corpus/latest.json', R), path=AUD + '/previous/audit/corpus/latest.json'),
                   active_catalogue=public_pin(catname), current_source_completion_registration=rp)
    snapname = 'audit/corpus/updates/accessible106-completion-L110.json'
    write('proposed/' + snapname, updated)
    updated['snapshot'] = public_pin(snapname)
    write('proposed/audit/corpus/latest.json', updated)
    native = load(R / 'papers/catalogue_principal_refutations.json')
    target = next(e for e in native['entries'] if e['source_ids'] == ['L110'])
    target['source_completion'] = dict(admission=ap, complete_volume=admission['complete_volume'],
        additional_manuscripts=[m for m in manuscripts if not m['existing_principal_manuscript_reused']],
        principal_manuscript_counted_again=False, measured=False, compression_factor=None)
    native.update(source_complete_original_ids=updated['source_complete_refutation_original_ids'], source_completion_credit=5)
    write('proposed/papers/catalogue_principal_refutations.json', native)
    paper = load(R / 'papers/latest_catalogue.json')
    paper.update(active_source_catalogue=public_pin(catname), principal_refutation_catalogue=public_pin('papers/catalogue_principal_refutations.json'))
    write('proposed/papers/latest_catalogue.json', paper)
    paragraph = 'F003, L029, L036 and L114 now have complete reviewed treatments of their\nsurviving source claims. Thus 96 originals are fully treated: 92 ordinary\nrecoveries and four complete source treatments after principal refutations.\nFive other refuted originals and four without a principal disposition retain\ncompletion obligations: 9 originals remain. There are 101 principal\ndispositions and 92 ordinary recoveries; the stopping condition is unchanged.'
    replacement = 'F003, L029, L036, L110 and L114 now have complete reviewed treatments of\ntheir surviving source claims. Thus 97 originals are fully treated: 92\nordinary recoveries and five complete source treatments after principal\nrefutations. Four other refuted originals and four without a principal\ndisposition retain completion obligations: 8 originals remain. There are\n101 principal dispositions and 92 ordinary recoveries; the stopping condition\nis unchanged.'
    note = 'The `complete L110 volume <{prefix}papers/corrections/L110/v1/complete.pdf>`_\ntreats all 63 claim rows in the fixed twenty-page article on Suzuki\npregeometries. It retains the principal boundary counterexample and proves\nthe surviving prime-residue and conditional extension assertions, with the\nsource conventions and corrected constructions stated precisely. A separate\nscalar-coordinate construction gives thick, connected, flag-transitive and\nlocally two-transitive geometries in arbitrary rank. The 105-page reading\nvolume contains the exact common theory and component proofs. Classical\npremises and stronger unproved variants remain explicit; no complete corrected\nclassification or compression factor is claimed. This closes one source\nobligation without adding an ordinary recovery, principal refutation,\nquestion or Lean credit.\n\n'
    changes = []
    for name, prefix in [('README.rst', ''), ('audit/completion.rst', '../')]:
        before = (R / name).read_text()
        need(before.count(paragraph) == 1, 'exact narrative completion anchor')
        after = before.replace(paragraph, replacement)
        anchor = 'The `complete L114 volume'
        need(after.count(anchor) == 1, 'exact L110 insertion anchor')
        after = after.replace(anchor, note.format(prefix=prefix) + anchor)
        dest = C / 'proposed' / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(after)
        changes.append(dict(path=name, before=pin(R / name, R), after=public_pin(name)))
        (C / (name.replace('/', '_') + '.diff')).write_text(''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='before/' + name, tofile='after/' + name)))
    name = 'audit/protocol.tex'
    before = (R / name).read_text()
    old_scope = 'statement is handled separately from a recovery. F003, L029, L036 and L114 now\nhave complete reviewed treatments of their surviving source claims. Thus 96\noriginals are fully treated: 92 ordinary recoveries and four complete source\ntreatments after principal refutations. Five other refuted sources and\nfour without a principal disposition retain obligations, so 9 originals\nstill require completion. There are 101 principal dispositions and 92\nordinary recoveries; the stopping condition is unchanged.'
    new_scope = 'statement is handled separately from a recovery. F003, L029, L036, L110 and\nL114 now have complete reviewed treatments of their surviving source claims.\nThus 97 originals are fully treated: 92 ordinary recoveries and five complete\nsource treatments after principal refutations. Four other refuted sources\nand four without a principal disposition retain obligations, so 8 originals\nstill require completion. There are 101 principal dispositions and 92\nordinary recoveries; the stopping condition is unchanged.'
    need(before.count(old_scope) == 1, 'exact protocol scope')
    after = before.replace(old_scope, new_scope)
    anchor = "L114's complete source treatment accounts for all 61 claim rows"
    need(after.count(anchor) == 1, 'exact protocol insertion anchor')
    text = "L110's complete source treatment accounts for all 63 claim rows in its fixed\n20-page edition. It retains the accepted principal boundary counterexample,\nproves the prime-residue obstructions and all five conditional rank-four\nextension necessities, and treats the corrected higher constructions. The\nsource's simple-Suzuki convention and the exact residue hypotheses remain\nexplicit. A separate scalar-coordinate family consists of thick, residually\nconnected, flag-transitive and locally two-transitive geometries in arbitrary\nrank. The 105-page volume retains all common theory and component proofs;\nclassical premises and stronger unproved variants are stated. It claims no\ncomplete corrected classification or compression factor. One source obligation\ncloses without new recovery, principal refutation, question or Lean credit.\n\n"
    after = after.replace(anchor, text + anchor)
    dest = C / 'proposed' / name
    dest.write_text(after)
    changes.append(dict(path=name, before=pin(R / name, R), after=public_pin(name)))
    (C / 'audit_protocol.tex.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='before/' + name, tofile='after/' + name)))
    write('narrative_changes.json', changes)
    write('source_entry_delta.json', dict(original_id='L110', before=before_entry,
        added_current_source_completion=entry['current_source_completion'], next_obligation=entry['next_obligation'],
        principal_disposition_unchanged=True, all_other_originals_unchanged=True))
    write('baseline.json', dict(commit=baseline, current_corpus=pin(R / 'audit/corpus/latest.json', R),
          active_catalogue=old['active_catalogue'], preserved_measured_ids=old['measured_original_ids'],
          preserved_recovery_ids=old['admitted_original_ids'], preserved_refutation_ids=old['refuted_principal_original_ids'],
          history_paths=['README.rst', 'audit/completion.rst', 'audit/protocol.tex', 'audit/protocol.pdf',
                         'audit/corpus/latest.json', 'papers/latest_catalogue.json', 'papers/catalogue_principal_refutations.json',
                         'scripts/verify_snapshot.py']))
    write('proposal.json', dict(status='PRIVATE_L110_SOURCE_COMPLETION_REGISTRATION_PROPOSAL',
        baseline=baseline, source_ids=['L110'], stage=pin(STAGE / AUD / 'manifest.json'),
        mathematical_acceptance=science, operational_acceptance=root,
        admission=ap, source_completion_registration=rp, machine_delta=delta,
        public_files_written=False, root_final_gate_required=AUD + '/root_integration.json',
        proposed_paths=[str(p.relative_to(C / 'proposed')) for p in sorted((C / 'proposed').rglob('*')) if p.is_file()],
        installation_and_snapshot_checker='To be supplied after review of this exact semantic and narrative proposal.'))
    print(json.dumps(dict(status='PREPARED_L110_REGISTRATION_CANDIDATE', proposal=pin(C / 'proposal.json'),
                         fully_treated=97, remaining=8, ordinary_recovery_delta=0, public_mutations=0)))


if __name__ == '__main__':
    main()
