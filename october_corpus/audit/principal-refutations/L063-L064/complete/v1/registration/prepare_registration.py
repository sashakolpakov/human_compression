"""Prepare reviewable L063_L064 completion metadata; never writes public files."""
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
AUD = 'audit/principal-refutations/L063-L064/complete/v1'
PAPER = 'papers/corrections/psl2_rank_two/v1'
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
    need(baseline == '1664d087bf3c1132110a1560d47e13830fd1710b', 'expected L115 predecessor')
    need(not subprocess.check_output(['git', '-C', str(R), 'status', '--porcelain']).strip(), 'clean predecessor')
    op = F / 'publication_operational_root_review'
    root = pin(op / 'manifest.json')
    need(root['sha256'] == load(P / 'registration_inputs.json')['portable_acceptance']['sha256'], 'exact portable acceptance')
    need(load(op / 'manifest.json')['status'] == 'ACCEPTED_L063_L064_PORTABLE_COMPLETE_SOURCE_TREATMENT', 'accepted portable status')
    old = load(R / 'audit/corpus/latest.json')
    need([old[k] for k in ['admitted_principal_originals', 'refuted_principal_originals',
                         'handled_mathematical_originals', 'currently_measured_originals',
                         'surviving_claim_obligation_originals', 'completion_obligation_originals']]
         == [92, 9, 101, 53, 3, 7], 'exact predecessor counts')
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
    need(len(premises) == len(premise_by_hash) == 232, 'exact accepted documentary/environment boundary')
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
    mapping = dict(status='EXACT_L063_L064_PORTABLE_REVIEW_TRANSPORT', original_manifest=root,
                   original_status=load(op / 'manifest.json')['status'], routes=routes, premises=premises,
                   additional_readable_scientific_acceptance=mathematical_record)
    write('proposed/' + AUD + '/operational/mapping.json', mapping)
    original_to_public = {r['original']['path']: r['public'] for r in routes if 'public' in r}
    science = pin(F / 'source_synthesis_root_review/manifest.json')
    need(science['path'] in original_to_public, 'operational closure includes mathematical acceptance')
    A = F / 'source_synthesis'
    ledgers = {sid: load(A / (sid + '_claims.json')) for sid in ['L063','L064']}
    manuscripts = []
    for part in load(A / 'parts.json'):
        stem = str(Path(part['path']).with_suffix(''))
        manuscripts.append(dict(id='psl2-rank-two-'+Path(stem).name, title=part['title'], physical_pages=part['pages'],
            tex=pin(STAGE/PAPER/(stem+'.tex'),STAGE),pdf=pin(STAGE/PAPER/(stem+'.pdf'),STAGE),
            tex_inputs=[],compiler='pdflatex',existing_principal_manuscript_reused=(stem=='proofs/omitted_affine')))
    volume=dict(tex=pin(STAGE/PAPER/'complete.tex',STAGE),pdf=pin(STAGE/PAPER/'complete.pdf',STAGE),
                physical_pages=52,introduction_pages=1,mathematical_pages=51)
    admissions={}
    for sid,claims in ledgers.items():
        admission=dict(status='REVIEWED_'+sid+'_SOURCE_COMPLETION_REQUIRING_ROOT_PUBLICATION_GATE',source_ids=[sid],
            disposition_kind='principal_refutation_with_complete_surviving_source_disposition',
            source_identity=pin(F.parents[1]/'sources'/('catalogue_'+sid+'.pdf')),
            source_edition=('Published 24-page article' if sid=='L063' else 'Fixed 21-page appendix, Lemma 12 through Proposition 30'),
            principal_refutation_admission=pin(R/('audit/principal-refutations/'+sid+'/v1/admission.json'),R),
            mathematical_acceptance=original_to_public[science['path']],portable_acceptance=original_to_public[root['path']],
            operational_mapping=public_pin(AUD+'/operational/mapping.json'),stage_manifest=pin(STAGE/AUD/'manifest.json',STAGE),
            transport=pin(STAGE/AUD/'transport.json',STAGE),portable_checker=pin(STAGE/AUD/'portable_check.py',STAGE),
            source_claim_ledger=pin(STAGE/PAPER/(sid+'_claims.json'),STAGE),source_claim_rows=len(claims['claims']),
            complete_volume=volume,manuscripts=manuscripts,shared_manuscript_source_ids=['L063','L064'],
            shared_manuscript_counted_once=True,uncertified_extensions=claims['uncertified_extensions'],
            ordinary_recovery_credit=0,principal_refutation_credit=0,new_original_credit=0,proposed_source_completion_credit=1,
            new_measurements=0,new_question_credit=0,new_Lean_credit=0,whole_source_formalized=False,compression_factor=None,
            source_retrieval_performed=False,public_gate=AUD+'/root_integration.json')
        write('proposed/'+AUD+'/'+sid+'/admission.json',admission)
        admissions[sid]=public_pin(AUD+'/'+sid+'/admission.json')
    updated=copy.deepcopy(old)
    updated.update(surviving_claim_obligation_original_ids=['L046'],surviving_claim_obligation_originals=1,
        completion_obligation_original_ids=[x for x in old['completion_obligation_original_ids'] if x not in ledgers],
        completion_obligation_originals=5,source_complete_refutation_original_ids=sorted(old['source_complete_refutation_original_ids']+list(ledgers)),
        source_complete_refutation_originals=8,fully_treated_original_ids=sorted(old['fully_treated_original_ids']+list(ledgers)),fully_treated_originals=100,
        handled_count_meaning='Principal dispositions only: 92 corrected recoveries and nine principal refutations. F003, L029, L036, L063, L064, L110, L114 and L115 have complete surviving-source dispositions; L046 retains a surviving-claim obligation.')
    delta={k:v for k,v in updated.items() if old.get(k)!=v};write('machine_delta.json',delta)
    registration=dict(status='REVIEWED_L063_L064_SOURCE_COMPLETION_REQUIRING_ROOT_GATES',source_ids=list(ledgers),admissions=admissions,
        shared_readable_home=PAPER,shared_manuscript_counted_once=True,predecessor_commit=baseline,
        previous_principal_disposition=old['current_principal_disposition_registration'],previous_science_registration=old['current_science_registration'],
        previous_source_completion_registration=old['current_source_completion_registration'],ordinary_recoveries_added=0,
        principal_refutations_added=0,principal_dispositions_added=0,fully_treated_originals_added=2,
        surviving_claim_obligations_closed=list(ledgers),new_measurements=0,new_question_credit=0,new_Lean_credit=0,
        compression_factor=None,public_gate=AUD+'/root_integration.json')
    write('proposed/'+AUD+'/source_completion_registration.json',registration);rp=public_pin(AUD+'/source_completion_registration.json')
    catalogue=load(R/old['active_catalogue']['path']);entry_deltas=[]
    for sid in ledgers:
        entry=next(e for e in catalogue['entries'] if e['original_id']==sid);before_entry=copy.deepcopy(entry)
        contract=('Fixed 24-page published original: all 122 claim rows receive explicit dispositions, including every row of Tables 1–6, nine Table 9 crossreferences, the local arc values and all stated full graph groups.' if sid=='L063' else 'Fixed 21-page appendix: all 28 claim rows receive explicit dispositions, from Lemma 12 through Proposition 30. Its actual Lemma 21 is separated from the false Proposition 22 restriction; advertised but absent content is not invented.')
        entry['current_source_completion']=dict(status='REVIEWED_COMPLETE_SOURCE_DISPOSITION_AFTER_PRINCIPAL_REFUTATION',admission=admissions[sid],
            principal_refutation_preserved=True,ordinary_recovery_credit=0,source_claim_rows=len(ledgers[sid]['claims']),source_contract=contract,
            qualification='The two originals retain separate claim ledgers and share one exact manuscript collection. The accepted affine omission remains a principal refutation. Corrected formulas, empty parameter branches, auxiliary errors and classical premises are explicit; source-isomorphism counts are distinguished from full graph automorphism groups.',
            whole_source_formalized=False,measured=False,compression_factor=None)
        entry['next_obligation']='No surviving mathematical source-disposition obligation remains for this fixed original. Preserve its principal refutation, source conventions, corrected formulas, explicit classical premises and edition qualifications. No ordinary recovery, new principal refutation or compression measurement is assigned.'
        entry_deltas.append(dict(original_id=sid,before=before_entry,added_current_source_completion=entry['current_source_completion'],next_obligation=entry['next_obligation'],principal_disposition_unchanged=True))
    catalogue.update(previous_catalogue=old['active_catalogue'],review_revision='L063 and L064 receive separate complete source dispositions after their existing principal refutations, using one shared proof collection. Ordinary recoveries, principal dispositions and measurements do not change.',
        source_complete_refutation_original_ids=updated['source_complete_refutation_original_ids'],source_complete_refutation_originals=8,
        fully_treated_original_ids=updated['fully_treated_original_ids'],fully_treated_originals=100)
    catalogue['current_recovery_counts'].update(surviving_claim_obligations=1,completion_obligations=5,fully_treated=100,completed_refutation_sources=8)
    catname='audit/corpus/accessible106/updates/completion-L063-L064-catalogue.json';write('proposed/'+catname,catalogue)
    updated.pop('snapshot');updated.update(previous_snapshot=dict(pin(R/'audit/corpus/latest.json',R),path=AUD+'/previous/audit/corpus/latest.json'),
        active_catalogue=public_pin(catname),current_source_completion_registration=rp)
    snapname='audit/corpus/updates/accessible106-completion-L063-L064.json';write('proposed/'+snapname,updated)
    updated['snapshot']=public_pin(snapname);write('proposed/audit/corpus/latest.json',updated)
    native=load(R/'papers/catalogue_principal_refutations.json');target=next(e for e in native['entries'] if e['source_ids']==['L063','L064'])
    target['source_completion']=dict(admissions=admissions,complete_volume=volume,
        additional_manuscripts=[m for m in manuscripts if not m['existing_principal_manuscript_reused']],
        shared_manuscript_source_ids=['L063','L064'],shared_manuscript_counted_once=True,principal_manuscript_counted_again=False,measured=False,compression_factor=None)
    native.update(source_complete_original_ids=updated['source_complete_refutation_original_ids'],source_completion_credit=8)
    write('proposed/papers/catalogue_principal_refutations.json',native)
    paper=load(R/'papers/latest_catalogue.json');paper.update(active_source_catalogue=public_pin(catname),principal_refutation_catalogue=public_pin('papers/catalogue_principal_refutations.json'))
    write('proposed/papers/latest_catalogue.json',paper)
    before_scope='F003, L029, L036, L110, L114 and L115 now have complete reviewed treatments\nof their surviving source claims. Thus 98 originals are fully treated:\n92 ordinary recoveries and six complete source treatments after principal\nrefutations. Three other refuted originals and four without a principal\ndisposition retain completion obligations: 7 originals remain. There are\n101 principal dispositions and 92 ordinary recoveries; the stopping\ncondition is unchanged.'
    after_scope='F003, L029, L036, L063, L064, L110, L114 and L115 now have complete reviewed\ntreatments of their surviving source claims. Thus 100 originals are fully\ntreated: 92 ordinary recoveries and eight complete source treatments after\nprincipal refutations. L046 and four originals without a principal disposition\nretain completion obligations: 5 originals remain. There are 101 principal\ndispositions and 92 ordinary recoveries; the stopping condition is unchanged.'
    note='The `shared L063 and L064 volume <{prefix}papers/corrections/psl2_rank_two/v1/complete.pdf>`_\ncontains one 52-page collection and separate ledgers for 122 claims in the\npublished article and 28 in its fixed appendix. It retains the accepted\naffine omission and gives complete counts from scalar spaces and normalizers,\nall 44 printed local arc values, and proofs of the stated full graph groups\nwith four corrected groups. Unordered counts, empty parameter branches and\npreliminary or appendix errors have separate dispositions. Ten accepted\nproofs are reused exactly; the common theory, classical premises and new\nsource joins remain explicit. This completes two originals without duplicating\nthe shared manuscript or adding a recovery, principal refutation, question,\nLean claim or compression measurement.\n\n'
    changes=[]
    for name,prefix in [('README.rst',''),('audit/completion.rst','../')]:
        before=(R/name).read_text();need(before.count(before_scope)==1,'exact narrative completion anchor')
        after=before.replace(before_scope,after_scope);anchor='The `complete L110 volume';need(after.count(anchor)==1,'exact insertion anchor')
        after=after.replace(anchor,note.format(prefix=prefix)+anchor)
        historical='Lemma 21. Retained classical inputs and all unpaid results remain explicit.'
        need(after.count(historical)==1,'exact earlier principal scope')
        after=after.replace(historical,'Lemma 21. That earlier correction concerned the principal omission. The\ncomplete joint treatment above now disposes of the remaining assertions in\nboth fixed sources, with classical premises explicit.')
        dest=C/'proposed'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(after)
        changes.append(dict(path=name,before=pin(R/name,R),after=public_pin(name)))
        (C/(name.replace('/','_')+'.diff')).write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before/'+name,tofile='after/'+name)))
    name='audit/protocol.tex';before=(R/name).read_text();old_scope=before_scope.replace('stopping\ncondition','stopping condition')
    need(before.count(old_scope)==1,'exact protocol scope');after=before.replace(old_scope,after_scope)
    anchor="L110's complete source treatment accounts for all 63 claim rows";need(after.count(anchor)==1,'exact protocol insertion anchor')
    text="The complete L063 and L064 treatment uses one shared 52-page collection,\nwith separate ledgers for 122 claims in the published article and 28 in its\nfixed appendix. It retains the accepted affine omission, proves complete\ncounts through scalar spaces and normalizers, supplies all 44 printed local\narc values, and proves the stated full graph groups with four corrections.\nUnordered counts, empty parameter branches, preliminary errors and appendix\ntranscription errors receive separate dispositions. Ten accepted proofs are\nimported unchanged; the common theory and classical premises are explicit.\nTwo source obligations close with one shared manuscript, without new ordinary\nrecovery, principal refutation, question, Lean or compression credit.\n\n"
    after=after.replace(anchor,text+anchor)
    historical='None of these refutations is an ordinary recovery or a claim that all valid\nsource assertions have been recovered.'
    need(after.count(historical)==1,'exact historical principal scope')
    after=after.replace(historical,'Those earlier principal corrections alone did not settle every valid source\nassertion. The complete L036 and joint L063/L064 treatments above now close\ntheir surviving source obligations; L046 remains outstanding.')
    dest=C/'proposed'/name;dest.write_text(after);changes.append(dict(path=name,before=pin(R/name,R),after=public_pin(name)))
    (C/'audit_protocol.tex.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before/'+name,tofile='after/'+name)))
    write('narrative_changes.json',changes);write('source_entry_delta.json',dict(original_ids=list(ledgers),entries=entry_deltas,all_other_originals_unchanged=True))
    write('baseline.json',dict(commit=baseline,current_corpus=pin(R/'audit/corpus/latest.json',R),active_catalogue=old['active_catalogue'],preserved_measured_ids=old['measured_original_ids'],preserved_recovery_ids=old['admitted_original_ids'],preserved_refutation_ids=old['refuted_principal_original_ids'],history_paths=['README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_principal_refutations.json','scripts/verify_snapshot.py']))
    write('proposal.json',dict(status='PRIVATE_L063_L064_SOURCE_COMPLETION_REGISTRATION_PROPOSAL',baseline=baseline,source_ids=list(ledgers),stage=pin(STAGE/AUD/'manifest.json'),mathematical_acceptance=science,operational_acceptance=root,admissions=admissions,source_completion_registration=rp,machine_delta=delta,public_files_written=False,root_final_gate_required=AUD+'/root_integration.json',proposed_paths=[str(p.relative_to(C/'proposed')) for p in sorted((C/'proposed').rglob('*')) if p.is_file()],installation_and_snapshot_checker='Concrete wrapper follows the exact semantic and narrative review.'))
    print(json.dumps(dict(status='PREPARED_L063_L064_REGISTRATION_CANDIDATE',proposal=pin(C/'proposal.json'),fully_treated=100,remaining=5,ordinary_recovery_delta=0,public_mutations=0)))

if __name__=='__main__':main()
