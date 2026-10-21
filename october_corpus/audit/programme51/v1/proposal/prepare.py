#!/usr/bin/env python3
"""Prepare private immutable-byte routes and proposed metadata; never write a checkout."""
from pathlib import Path
from copy import deepcopy
import argparse, ast, hashlib, json, re, subprocess

HERE = Path(__file__).resolve().parent
SCI = 'papers/topic-a/extensions/locally-toroidal/v1'
AUD = 'audit/topic-a/extensions/locally-toroidal/v1'
NUM = 'audit/topic-a/v4/measurement'
ED = 'audit/corpus/editorial/L022/v1'

def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_text())
def need(ok, message):
    if not ok: raise ValueError(message)
def write(name, value):
    p = HERE / name; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
def binding(p, root):
    b = p.read_bytes()
    return dict(path=str(p.relative_to(root)), bytes=len(b), sha256=sha(b))

def prepare(study, repo):
    need(study.resolve() != repo.resolve(), 'distinct private and public roots')
    need(not (HERE/'manifest.json').exists(), 'preserve final frozen proposal')
    base = subprocess.check_output(['git','rev-parse','HEAD'], cwd=repo, text=True).strip()
    corpus = load(repo/'audit/corpus/latest.json')
    cat = load(repo/'papers/catalogue.json')
    latest = load(repo/'papers/latest_catalogue.json')
    need(corpus['currently_measured_originals']==50, 'fixed programme50 baseline')
    need(len(corpus['active_original_ids'])==106, '106 active originals')
    paths = ['papers/catalogue.json','papers/latest_catalogue.json','papers/topic-a/latest.json',
             'audit/corpus/latest.json','README.rst','audit/completion.rst',
             'audit/topic-a/v3/proposed_catalogue_rows.json','scripts/build_papers.py',
             'scripts/verify_snapshot.py',corpus['active_catalogue']['path'],
             'audit/overview/v16/packet/results.json','audit/overview/latest.json',
             'audit/overview/README.rst','audit/protocol.tex','audit/protocol.pdf']
    for name in paths:
        if (repo/name).exists():
            p=HERE/'baseline'/name;p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes((repo/name).read_bytes())
    functions={n.name:sha(ast.dump(n,include_attributes=False).encode())
               for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body
               if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
    write('baseline.json',dict(commit=base,files=[binding(repo/p,repo)for p in paths if(repo/p).exists()],
                              prior_nonmain_verifier_ASTs=functions,public_writes=False))
    packets=[
      ('science','topic_A_L121_application',SCI,'a9acb0e60065cdef16f63fee0328200357347c29a22175beafb1dc5b87981f1e'),
      ('scientific_review','topic_A_L121_application_independent_review',AUD+'/scientific_review','8b7f18eadcc6fdf032bca0cf298208a8e2cab8e979aadc1d17cb9317d7e1f215'),
      ('scientific_adoption','topic_A_L121_application_root_adoption',AUD+'/root_adoption','38901fc13359b1124ee2bbb005b7ac445aca47163ef16dcf62db5bc26f5c04f6'),
      ('numbers','topic_A_L121_measurement_results',NUM+'/packet','0f071b3d9098d48bfdadd8273239c4459ab35c549e2ddae59f6a9c622fa9a90e'),
      ('editorial_author','L022_editorial_disposition',ED+'/author','f5f8f9b6d9f247e264c2107b516a7bcb9d6c78f017c7081a85ff72f114f1322e'),
      ('editorial_review','L022_editorial_independent_review',ED+'/independent_review','0c6ff364496afc73ee36b63db1bba1ea81e840416d1977959c76860bd86b008b'),
      ('editorial_adoption','L022_editorial_root_adoption',ED+'/root_adoption','63fd7715402444d0ec49b102ac574dd789f6d6cebe852659a9cced0d3a738de7')]
    numerical_acceptance=HERE/'numerical_acceptance.json'
    if numerical_acceptance.exists():
        for p in load(numerical_acceptance)['packets']:
            packets.append((p['role'],p['study_directory'],p['public_directory'],p['manifest_sha256']))
    routes=[]; inventory=[]
    for role, directory, dest, expected in packets:
        folder=study/directory; m=folder/'manifest.json';need(sha(m.read_bytes())==expected,'exact '+role)
        mm=load(m); rows=mm['exports']+[binding(m,folder)]
        for e in rows:
            b=(folder/e['path']).read_bytes()
            need(len(b)==e['bytes']and sha(b)==e['sha256'],'export '+e['path'])
            routes.append(dict(role=role,study_path=directory+'/'+e['path'],public_path=dest+'/'+e['path'],bytes=e['bytes'],sha256=e['sha256']))
        inventory.append(dict(role=role,study_directory=directory,public_directory=dest,manifest_sha256=expected,exports=len(mm['exports'])))
    need(len({x['public_path']for x in routes})==len(routes),'unique routes')
    write('copy_plan.json',dict(status='PRIVATE_PROPOSED_EXACT_COPY_ROUTES',packets=inventory,files=routes,
                               primary_source_assets_copied=False,public_write_author='root',
                               numerical_root_adoption_pending=not numerical_acceptance.exists()))
    frozen=load(repo/'audit/topic-a/v3/proposed_catalogue_rows.json')
    oldrows=[deepcopy(r)for r in frozen['entries']if r['role']in['umbrella','application']]
    need(len(oldrows)==9,'all9 existing science entries')
    for row in oldrows:
        row['compiler']='xelatex'
        row['status']='ROOT_ADMITTED_CURRENT_EDITION'
        row['build_registration_note']='Exact existing scientific bytes; canonical registration was missing despite accepted current v3 routes.'
    scope=load(study/'topic_A_L121_application/scope.json')
    main=(study/'topic_A_L121_application/application.tex').read_text()
    title=re.search(r'\\title\{([^{}]*)\}',main).group(1)
    inputs=[SCI+'/'+x['path']for x in load(study/'topic_A_L121_application/manifest.json')['exports']
            if x['path'].startswith('sections/')and x['path'].endswith('.tex')]
    raw=[dict(x,public_path=SCI+'/'+x['path'])for x in scope['required_whole_files']]
    top=binding(study/'topic_A_L121_application/check.py',study/'topic_A_L121_application')
    raw.append(dict(top,role='operational_validation_runner',public_path=SCI+'/check.py'))
    need(len(raw)==15,'new complete15 raw file roles')
    app=dict(id='topic-a/extensions/locally-toroidal/v1/application',topic='A',application_id='A9',
             title=title,title_origin='Literal unchanged accepted TeX title',role='application',source_contracts=['L121'],
             tex=SCI+'/application.tex',pdf=SCI+'/application.pdf',tex_inputs=inputs,compiler='pdflatex',
             physical_pages=11,admission=AUD+'/admission.json',review_record=AUD+'/scientific_review/review.json',
             measurement_admission='audit/topic-a/v4/admission.json',
             status=('PROPOSED_REGISTRATION_OF_ACCEPTED_SCIENCE_AND_NUMBERS'if numerical_acceptance.exists()
                     else'PROPOSED_REGISTRATION_OF_ACCEPTED_SCIENCE_PENDING_NUMERICAL_ADOPTION'),
             required_program_inputs=[r['public_path']for r in raw if r['role']=='required_program'],
             required_data_inputs=[r['public_path']for r in raw if r['role']=='required_data'],
             operational_driver_inputs=[r['public_path']for r in raw if r['role']=='operational_validation_runner'],
             partial_formal_inputs=[r['public_path']for r in raw if r['role']=='partial_formal'],
             full_Lean=False,source_software_cost=None,common_pdf='papers/topic-a/v3/umbrella.pdf')
    allrows=oldrows+[app]
    need([len(app[k])for k in ['required_program_inputs','required_data_inputs','operational_driver_inputs','partial_formal_inputs']]==[8,1,4,2],'8+1+4+2 inventory')
    write('catalogue_additions.json',dict(entries=allrows,old_frozen_rows=binding(repo/'audit/topic-a/v3/proposed_catalogue_rows.json',repo),
                                         old_bytes_unchanged=True,historical_rows_retained=True,
                                         excluded_from_canonical_import='Three old code appendices require file-copy support beyond the canonical TeX-only builder. They remain published, separately routed and explicitly incomplete for the enlarged required closure.'))
    write('raw_roles.json',dict(new_L121_files=raw,required_programs=8,required_data=1,operational=4,
                              partial_formal_files=2,declarations=6,source_software_cost=None,
                              entire_topic_files=45,entire_topic_required_files=20,
                              old_printed_appendices_only_old11files=True,complete_enlarged_printed_cost=None))
    cc=deepcopy(cat);ids={r['id']for r in cc['papers']+cc.get('new_editions',[])}
    for r in allrows:
        need(r['id']not in ids,'do not override a canonical existing row');cc['new_editions'].append(r);ids.add(r['id'])
    cc['current_topic_editions']['A']=[r['id']for r in allrows]
    write('proposed/papers/catalogue.json',cc)
    write('source_contract.json',dict(original_id='L121',source=scope['source'],source_publicly_copied=False,
          application=app,source_map=SCI+'/source_map.json',dispositions=27,retained_premises=scope['retained_classical_premises'],
          interfaces=scope['interfaces'],formal_scope=scope['formal_scope'],
          source_corrections='Exact source_map.json dispositions; cubic subgroup/full toroid distinction, finite presentation and unrestricted minimum-degree qualifications retained.',
          new_question_credit=0,proof_review_repeated=False))
    old_pending=set(corpus['accessible_pending_original_ids']);need({'L121','L022'}<=old_pending,'only two pending dispositions')
    updated=deepcopy(corpus)
    updated.update(status='PROPOSED_PROGRAMME_51_MEASURED_54_PENDING_1_EDITORIAL',admitted_principal_originals=51,
                   currently_measured_originals=51,accessible_pending_complete_recovery=54,
                   accessible_pending_original_ids=sorted(old_pending-{'L121','L022'}),
                   editorial_original_ids=['L022'],editorial_originals=1,editorial_factor=None,
                   all_original_proofs_recovered=False,all_conjectures_resolved=False)
    for k in ['admitted_original_ids','measured_original_ids']:updated[k]=sorted(corpus[k]+['L121'])
    updated['proposal_only']=True
    updated['future_snapshot_path']='audit/corpus/updates/accessible106-l121-measured-editorial.json'
    updated['pending_root_bindings']=[AUD+'/admission.json','audit/topic-a/v4/admission.json',ED+'/admission.json']
    write('proposed/audit/corpus/next.json',updated)
    active=load(repo/corpus['active_catalogue']['path']);active2=deepcopy(active)
    for r in active2['entries']:
        if r['original_id']=='L121':
            r['current_principal_recovery']=dict(status='PROPOSED_ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT',
              source_dispositions=27,application=app['pdf'],common='papers/topic-a/v3/umbrella.pdf',
              latest_admission_references=[AUD+'/admission.json','audit/topic-a/v4/admission.json'],
              scope='All corrected principal source dispositions with exact retained inputs; not new question or full-formal credit.')
            r['next_obligation']='No new recovery obligation in this accepted principal contract; preserve explicit retained inputs and unresolved broader questions.'
        if r['original_id']=='L022':
            d=load(study/'L022_editorial_disposition/disposition.json')
            r['current_principal_recovery']=dict(status='EDITORIAL_NO_PRINCIPAL_MATHEMATICAL_RESULT',
              latest_admission_references=[ED+'/admission.json'],count_as_measured_mathematical_recovery=False,
              factor=None,accessible_original_retained=True)
            r['principal_results_to_recover'].update(summary=d['scope_note'],scope_status='COMPLETE_EDITORIAL_READING_ACCEPTED',
                                                   principal_mathematical_results=[],replacement_manuscript_required=False)
            r['next_obligation']='Retain as one accessible editorial original; no theorem recovery, factor or measured-original credit applies.'
    active2.update(status='PROPOSED_ACCESSIBLE106_CATALOGUE_WITH_EDITORIAL_DISPOSITION',admitted_principal_originals=51,
                   accessible_pending_complete_recovery=54,editorial_originals=1,
                   current_recovery_counts=dict(active=106,admitted=51,pending=54,editorial=1))
    write('proposed/audit/corpus/active_catalogue.json',active2)
    pl=deepcopy(latest)
    for r in pl['entries']:
        if r.get('id')in {x['id']for x in oldrows}:
            r['measurement_admission']='audit/topic-a/v4/admission.json'
    pl['entries'].append(app);pl['original_ids']=sorted(set(pl['original_ids'])|{'L121'})
    pl['new_principal_originals']=latest['new_principal_originals']+1
    pl['unified_A_current_edition'].update(source_ids=load(study/'topic_A_L121_measurement_results/results.json')['source_ids'],
               current_applications=pl['unified_A_current_edition']['current_applications']+[app['pdf']],
               future_admission='audit/topic-a/v4/admission.json',prior_admission=pl['unified_A_current_edition']['admission'])
    pl['unified_A_current_edition'].pop('admission')
    pl['editorial_dispositions']=[dict(original_id='L022',admission=ED+'/admission.json',measured=False,factor=None,active=True)]
    pl['status']='PROPOSED_CURRENT_MANUSCRIPT_CATALOGUE_51_PLUS_EDITORIAL'
    write('proposed/papers/latest_catalogue.json',pl)
    reuse=[]
    for r in oldrows:
        for f in [r['tex'],r['pdf']]+r['tex_inputs']:
            if f not in {x['path']for x in reuse}:reuse.append(binding(repo/f,repo))
    write('reused_science.json',dict(files=reuse,common_pages=23,application_pages=45,scientific_PDFs=9,
                                    public_copy_requested=False,source_cost_reused=True))
    write('topic_pointer_proposal.json',dict(status='PROPOSED_NINE_ORIGINAL_A_AFTER_NUMERICAL_ADOPTION',
         source_ids=load(study/'topic_A_L121_measurement_results/results.json')['source_ids'],
         admission='audit/topic-a/v4/admission.json',reader=NUM+'/packet/reader.pdf',measurement=NUM+'/packet/results.json',
         common='papers/topic-a/v3/umbrella.pdf',applications=[r['pdf']for r in allrows if r['role']=='application'],
         catalogue_entries=allrows,old_science_bytes_reused=True,old_measurement_preserved=True,
         software_inclusive_factor=None,complete_enlarged_printed_program_factor=None))
    write('overview17_plan.json',dict(status='SEPARATE_PENDING_OVERVIEW_TASK',baseline='audit/overview/v16',
          target='audit/overview/v17',topics=19,measured_originals=51,mathematical_pending_originals=54,
          editorial_originals=1,active_originals=106,archived_originals=55,
          changes=['Replace only A whole-topic comparison with accepted nine-original value.',
                   'Retain eight prior A conditional records exactly; append L121 conditional.',
                   'Retain every non-A topic and conditional value exactly.',
                   'Register L022 editorial with factor null and no measured credit.'],
          no_pooled_factor=True,source_software_unknown=True,numerical_adoption_required=True))
    write('state.json',dict(status='PRIVATE_PROVISIONAL_PUBLICATION_PREPARATION',base_commit=base,
           exact_copy_files=len(routes),existing_science_files_reused=len(reuse),canonical_science_builds=10,
           numerical_root_adoption_pending=not numerical_acceptance.exists(),public_writes=False,
           no_GAP_Lean_or_primary_replay=True))
    return load(HERE/'state.json')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True)
    a=ap.parse_args();print(json.dumps(prepare(a.study_root,a.repo)))
