"""Private science65 wrapper preparation against exact local science64."""
from pathlib import Path
import argparse,ast,copy,difflib,hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent
AUDIT='audit/science65/v1';SCIENCE='audit/recoveries/L096/v1';NATIVE='papers/recoveries/L096/v1'
BASE='e277a8ddcd822e71f0e8ee61e0e9d4ab57508e82'
def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def pin(p,n):return dict(path=n,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main(a):
    need(not(HERE/'manifest.json').exists(),'frozen proposal');repo=a.repo;W=HERE/'wrappers'
    need(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==BASE,'exact local baseline')
    old=load(repo/'audit/corpus/latest.json');need((old['admitted_principal_originals'],old['currently_measured_originals'],old['accessible_pending_complete_recovery'])==(64,53,41),'science64 partition')
    plan=load(HERE/'copy_plan.json');routes={r['study_path']:r for r in plan['files']}
    def logical(n):
        r=routes[n];return dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])
    def pub(n):
        if (W/n).is_file():return pin(W/n,n)
        r=next((r for r in plan['files'] if r['public_path']==n),None)
        return dict(path=n,bytes=r['bytes'],sha256=r['sha256']) if r else pin(repo/n,n)
    history={}
    for n in ['README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py']:
        dest=AUDIT+'/previous/'+n;p=W/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((repo/n).read_bytes());history[n]=pin(p,dest)
    write(W/(AUDIT+'/history_routes.json'),dict(base_commit=BASE,routes=history,scope='Exact local science64 pointers and complete nested history through programme53.'))
    asts={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
    need(len(asts)==155,'155 prior verifier functions')
    protected=['papers/catalogue.json','scripts/build_papers.py','audit/overview/latest.json','audit/overview/v19/admission.json','audit/science64/v1/root_integration.json']
    protected += [str(p.relative_to(repo)) for p in (repo/'audit/overview/v19/packet').rglob('*') if p.is_file()]
    write(HERE/'baseline.json',dict(commit=BASE,origin_main_at_preparation=subprocess.check_output(['git','-C',str(repo),'rev-parse','origin/main'],text=True).strip(),old_nonmain_ASTs=asts,history=history,old_catalogue=old['active_catalogue'],protected_files=[pin(repo/n,n) for n in protected],transport='Baseline is committed locally; remote push failure is not publication success.'))
    inv=load(a.study/'corpus106_L096_recovery/whole_program_inventory.json')
    roles=copy.deepcopy(inv)
    for r in roles['all_occurrences']:r['public_binding']=logical(r['path'])
    roles.update(public_transport=AUDIT+'/publication_plan/copy_plan.json',all_occurrence_roles_preserved=True,disjoint_role_sum_claimed=False,source_software_cost=None,external_proof_cost=None,software_inclusive_factor=None,measurement=None)
    write(W/(AUDIT+'/whole_file_roles.json'),roles)
    native=[]
    for stem,k,role in [('umbrella',11,'complete additional common theory'),('shadow_applications',9,'complete corrected application'),('named_geometries',7,'complete source-profile and naming companion')]:
        p=a.study/'corpus106_L096_recovery'/(stem+'.tex');t=p.read_text()
        inputs=[]
        def recurse(path):
            for x in re.findall(r'\\input\{([^{}]+)\}',path.read_text()):
                n=x if x.endswith('.tex') else x+'.tex';q=path.parent/n
                rel=str(q.relative_to(p.parent));dest=NATIVE+'/'+rel
                if dest not in inputs:inputs.append(dest);recurse(q)
        recurse(p)
        native.append(dict(id='L096_'+stem,title=re.search(r'\\title\{([^{}]+)\}',t).group(1),tex=NATIVE+'/'+stem+'.tex',pdf=NATIVE+'/'+stem+'.pdf',tex_inputs=inputs,compiler='pdflatex',physical_pages=k,role=role,source_ids=['L096'],topic='D: shadow intersections',comparison_topic_created=False,measured=False,compression_factor=None,externaldocument_dependency=None))
    note='Complete corrected principal L096 recovery: all73 main/count dispositions,57 printed numerical comparisons and232 positive named occurrences. The entire11-page common,9-page application and7-page naming companion are required, plus the whole existing6-page TopicD common. All229 source-profile occurrences agree on every compatible class; the three J1 historical4.1 ordinals are unverified metadata, replaced mathematically by the complete explicit profile classification. M12/J3 count corrections and the HS archive-pointer correction remain explicit. Global historical classification/identification premises and external/source software costs remain retained, not newly proved or zero. Literal source/table-name equivalence is not claimed. Current root acceptance supersedes frozen author pending labels without changing bytes.'
    ad=dict(status='ROOT_ACCEPTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE65_GATE',source_id='L096',source_ids=['L096'],source_author_role='Pascale Jacobs and Dimitri Leemans; focal-group-authored source.',principal_originals_added=1,measured=False,measurement_status='pending',compression_factor=None,software_inclusive_factor=None,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,theorem_sets_equivalent=False,
            author_manifest=logical('corpus106_L096_recovery/manifest.json'),distinct_root_review_manifest=logical('corpus106_L096_complete_root_review/manifest.json'),root_scientific_acceptance=logical('corpus106_L096_complete_root_review/manifest.json'),
            source_map=logical('corpus106_L096_recovery/source_map.json'),dependency_boundary=logical('corpus106_L096_recovery/dependencies.json'),source_ledger=logical('corpus106_L096_recovery/source_ledger.json'),program_roles=pub(AUDIT+'/whole_file_roles.json'),whole_scientific_manuscripts=[pub(d['pdf']) for d in native],physical_pages=[11,9,7],old_whole_common=pub('papers/topic-d/v2/umbrella.pdf'),old_whole_common_pages=6,source_pages=16,source_routes=73,named_occurrences=232,profile_confirmed_occurrences=229,historical_ordinals_unverified=3,comparison_topic_created=False,current_measurements_changed=False,publication_gate=AUDIT+'/root_integration.json',public_mapping=AUDIT+'/publication_plan/copy_plan.json',scope_note=note,
            roles='Enumeration_volume authored the new naming proof, bounded discriminators and assembly, and this operational publication mapping; prior volume/J2/M22 review roles remain disclosed. Root distinctly accepted the current complete corrected contract and reused earlier independent component acceptances. No self-adjudication is claimed.',frozen_status_overlay='Later root complete review governs current acceptance; all historical author/reviewer statuses remain immutable.')
    ap=SCIENCE+'/admission.json';write(W/ap,ad);admission=pub(ap);rp=AUDIT+'/new_original_registration.json'
    write(W/rp,dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_REGISTRATION_PROPOSAL',source_ids=['L096'],admissions=[admission],principal_originals_added=1,measurement_originals_added=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,comparison_topics_added=0,compression_factor=None,previous_registration=old['current_science_registration']))
    unmeasured=sorted(old['measurement_pending_original_ids']+['L096']);cat=copy.deepcopy(load(repo/old['active_catalogue']['path']))
    cat.update(status='CURRENT_ACCESSIBLE106_65_CORRECTED_RECOVERIES_53_MEASURED',admitted_principal_originals=65,currently_measured_originals=53,measurement_pending_original_ids=unmeasured,accessible_pending_complete_recovery=40,review_revision='Only L096 becomes an accepted complete corrected principal recovery;105 other records unchanged.',new_proof_credit=1,new_question_credit=0,previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=65,measured=53,measurement_pending=12,pending=40,editorial=1))
    row=next(r for r in cat['entries'] if r['original_id']=='L096');previous=copy.deepcopy(row['current_principal_recovery'])
    row['current_principal_recovery']=dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING',latest_admission_references=[admission],principal_contract_admitted=True,measured=False,compression_factor=None,whole_source_formalized=False,theorem_sets_equivalent=False,new_question_credit=0,scope=note,historical_admission_evidence=previous)
    row['next_obligation']='Any later measurement acquires the complete old TopicD common plus all11+9+7 current pages and the complete required file/data boundary. Source executable Magma listings require symmetric treatment. Three J1 historical ordinal identities remain unverified metadata; no factor or literal source equivalence is asserted.'
    cp='audit/corpus/accessible106/updates/corrected-unmeasured65-catalogue.json';write(W/cp,cat)
    c=copy.deepcopy(old);c.update(status='CURRENT_PROGRAMME_65_CORRECTED_RECOVERIES_53_MEASURED_40_PENDING_1_EDITORIAL',admitted_principal_originals=65,accessible_pending_complete_recovery=40,admitted_original_ids=sorted(old['admitted_original_ids']+['L096']),accessible_pending_original_ids=[i for i in old['accessible_pending_original_ids'] if i!='L096'],measurement_pending_original_ids=unmeasured,scientific_unmeasured_original_ids=unmeasured,previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pub(cp),current_science_registration=pub(rp));c['added_admissions'].append(pub(rp));c.pop('snapshot',None)
    sp='audit/corpus/updates/accessible106-corrected-unmeasured65.json';write(W/sp,c);c['snapshot']=pub(sp);write(W/'audit/corpus/latest.json',c)
    for r in native:r['admission']=admission
    sc=load(repo/'papers/catalogue_corrected_unmeasured.json');sc['entries'].extend(native);sc['original_ids'].append('L096');sc['root_publication_gate']=AUDIT+'/root_integration.json'
    sc['acquired_dependencies'].append(dict(id='L096_existing_whole_TopicD_common',source_ids=['L096'],tex='papers/topic-d/v2/umbrella.tex',pdf='papers/topic-d/v2/umbrella.pdf',physical_pages=6,scope='Whole existing TopicD common retained as paid dependency; no new measurement or overlap discount.',binding=pub('papers/topic-d/v2/umbrella.pdf')))
    write(W/'papers/catalogue_corrected_unmeasured.json',sc)
    papers=load(repo/'papers/latest_catalogue.json');papers['status']='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_TWELVE_CORRECTED_UNMEASURED';papers['active_source_catalogue']=pub(cp);papers['corrected_unmeasured_scientific_catalogue']=pub('papers/catalogue_corrected_unmeasured.json');write(W/'papers/latest_catalogue.json',papers)
    write(HERE/'native_catalogue.json',dict(new_documents=native,complete_scientific_pages=27,additional_old_common_pages=6,compiler='pdflatex',all_whole_papers_paid=True))
    oldlist='N014, L024, L102, F011, F008, L039, L013, L011, L025, L122 and L015';newlist='N014, L024, L102, F011, F008, L039, L013, L011, L025, L122, L015 and L096'
    t=(repo/'README.rst').read_text().replace('**64 accessible originals','**65 accessible originals').replace('53 are measured and eleven ('+oldlist+')','53 are measured and twelve ('+newlist+')').replace('41 await mathematical recovery;','40 await mathematical recovery;')
    insert='The `L096 guide <'+NATIVE+'/PUBLICATION.rst>`_ gives the complete eleven-page\nshadow common paper, nine-page application and seven-page naming companion.\nThe whole existing six-page Topic D common remains acquired. All 73 source\ndispositions and 232 named occurrences are adjudicated under the corrected\ncontract: 229 have source-profile proofs; the three J1 ordinal correspondences\nremain historical metadata, with the complete mathematical classes stated\nexplicitly. Full required software/data and retained classifications remain\nvisible. No measurement or new question claim is added.\n\nAll twelve source editions, complete proof packets and distinct reviews are recorded'
    need('All eleven source editions, complete proof packets and distinct reviews are recorded' in t,'reader insertion')
    t=t.replace('All eleven source editions, complete proof packets and distinct reviews are recorded',insert).replace('None of these eleven recoveries','None of these twelve recoveries').replace('audit/science64/v1/new_original_registration.json',rp);write(W/'README.rst',t)
    t=(repo/'audit/completion.rst').read_text().replace('**64 reviewed corrected principal recoveries**','**65 reviewed corrected principal recoveries**').replace('53 are measured and eleven ('+oldlist+') are unmeasured. There are 41 originals','53 are measured and twelve ('+newlist+') are unmeasured. There are 40 originals').replace(oldlist+' have separate scientific admissions',newlist+' have separate scientific admissions').replace('science64/v1/new_original_registration.json','science65/v1/new_original_registration.json')
    t=t.replace('The `current overview','L096 retains all 27 current native pages and the complete six-page existing\nTopic D common. Its 73 dispositions, 57 numerical comparisons and 232 positive\noccurrences preserve corrected counts, source-profile proofs and three expressly\nunverified historical J1 ordinals. The full mathematical profile classification\nis complete. Software, external classifications and their limits stay explicit;\nthere is no new length factor.\n\nThe `current overview',1);write(W/'audit/completion.rst',t)
    t=(repo/'audit/protocol.tex').read_text().replace('106=64\\ \\text{reviewed corrected recoveries}+41','106=65\\ \\text{reviewed corrected recoveries}+40').replace('Of the 64 corrected recoveries','Of the 65 corrected recoveries').replace(oldlist+' are scientifically accepted but unmeasured',newlist+' are scientifically accepted but unmeasured')
    t=t.replace('The accepted overview v19','L096 retains its complete eleven-page shadow common paper, nine-page\napplication and seven-page naming companion, together with the entire existing\nsix-page Topic D common. Its corrected contract preserves all 73 source\ndispositions and 232 named occurrences. Source profiles settle 229; three\nhistorical $J_1$ ordinals remain unverified metadata while the full mathematical\nprofile classification is given. Complete required programs, data, checkpoints\nand retained classification inputs remain visible. No factor follows.\n\nThe accepted overview v19',1);write(W/'audit/protocol.tex',t)
    write(HERE/'registration_proposal.json',dict(status='PRIVATE_PROPOSAL_ROOT_INTEGRATION_REQUIRED',base_commit=BASE,new_originals=['L096'],counts=dict(active=106,corrected_recoveries=65,measured=53,unmeasured=12,mathematical_pending=40,editorial=1,archived=55,comparison_topics=19),corpus_pointer=pub('audit/corpus/latest.json'),active_catalogue=pub(cp),snapshot=pub(sp),papers_pointer=pub('papers/latest_catalogue.json'),new_registration=pub(rp),admission=admission,unchanged_measurement_overview='audit/overview/v19/admission.json',new_factors=0,root_integration_route=AUDIT+'/root_integration.json'))
    diff=''
    for n in ['README.rst','audit/completion.rst','audit/protocol.tex','papers/latest_catalogue.json']:diff+=''.join(difflib.unified_diff((repo/n).read_text().splitlines(True),(W/n).read_text().splitlines(True),fromfile='old/'+n,tofile='proposed/'+n))
    write(HERE/'documentation.diff',diff)
    print('prepared',len(plan['files']),'logical files;',len(asts),'old functions')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);main(p.parse_args())
