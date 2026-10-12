"""Science65 publication guard; accepted science is reused, not re-adjudicated."""
from pathlib import Path,PurePosixPath
import argparse,ast,copy,hashlib,json,re
HERE=Path(__file__).resolve().parent;AUDIT='audit/science65/v1';SCIENCE='audit/recoveries/L096/v1';NATIVE='papers/recoveries/L096/v1'
def need(x,m):
    if not x:raise ValueError('SCIENCE65: '+m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(root,r):
    p=PurePosixPath(r['path']);need(not p.is_absolute() and '..' not in p.parts,'safe path')
    f=root/p;need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'binding '+r['path'])
def semantics(c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,review,source):
    need(tuple(c[k] for k in ['originals','admitted_principal_originals','currently_measured_originals','accessible_pending_complete_recovery','editorial_originals','archived_unavailable_originals'])==(106,65,53,40,1,55),'partition')
    need(len(c['admitted_original_ids'])==len(set(c['admitted_original_ids']))==65 and set(c['admitted_original_ids'])==set(old['admitted_original_ids'])|{'L096'},'only L096 added')
    need(len(c['accessible_pending_original_ids'])==40 and set(c['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'L096'},'pending subtraction')
    need(c['measurement_pending_original_ids']==c['scientific_unmeasured_original_ids']==sorted(old['measurement_pending_original_ids']+['L096']) and len(c['measurement_pending_original_ids'])==12,'12 unmeasured')
    for k in ['measured_original_ids','added_measurements','current_topic_replacements','historical_admitted_ids','active_original_ids','archived_original_ids','editorial_original_ids','editorial_factor','source_retrieval_in_scope','all_original_proofs_recovered','all_conjectures_resolved']:
        need(c[k]==old[k],'unchanged '+k)
    parts=[set(c['admitted_original_ids']),set(c['accessible_pending_original_ids']),set(c['editorial_original_ids'])]
    need(sum(map(len,parts))==106 and set.union(*parts)==set(c['active_original_ids']),'complete disjoint active partition')
    need(c['added_admissions']==old['added_admissions']+[c['current_science_registration']],'one science registration')
    before={r['original_id']:r for r in oldcat['entries']};after={r['original_id']:r for r in cat['entries']}
    need(len(after)==len(cat['entries'])==106 and before.keys()==after.keys(),'same original roster')
    need(all(before[k]==after[k] for k in before if k!='L096'),'all105 other records exact')
    for k in before['L096']:
        if k not in ['current_principal_recovery','next_obligation']:need(before['L096'][k]==after['L096'][k],'L096 source/history '+k)
    r=after['L096']['current_principal_recovery'];need(r['historical_admission_evidence']==before['L096']['current_principal_recovery'] and r['principal_contract_admitted'] and not r['measured'] and r['compression_factor'] is None,'corrected unmeasured record')
    need(ad['source_ids']==['L096'] and ad['principal_originals_added']==1 and ad['source_author_role'].startswith('Pascale Jacobs and Dimitri Leemans;'),'one original and exact source authors')
    need(ad['physical_pages']==[11,9,7] and ad['old_whole_common_pages']==6 and len(ad['whole_scientific_manuscripts'])==3,'complete manuscripts including old common')
    need(ad['source_pages']==16 and ad['source_routes']==73 and ad['named_occurrences']==232 and ad['profile_confirmed_occurrences']==229 and ad['historical_ordinals_unverified']==3,'corrected source contract')
    need(not ad['measured'] and not ad['comparison_topic_created'] and not ad['current_measurements_changed'] and ad['compression_factor'] is ad['software_inclusive_factor'] is None,'no new measure/topic')
    need(ad['new_question_credit']==ad['new_Lean_declarations']==0 and not ad['whole_source_formalized'] and not ad['theorem_sets_equivalent'],'scope limits')
    need(roles['occurrence_count']==len(roles['all_occurrences'])==881 and roles['unique_content_count']==len(roles['unique_contents'])==824,'complete whole role inventory')
    need(roles['role_categories_disjoint'] is False and roles['disjoint_role_sum_claimed'] is False and roles['all_occurrence_roles_preserved'],'overlapping roles explicit')
    need(roles['source_software_cost'] is roles['external_proof_cost'] is roles['software_inclusive_factor'] is roles['measurement'] is None,'unknown costs remain null')
    need(review['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY' and review['source_ids']==['L096'] and review['reviewer']=='root' and review['author']=='enumeration_volume','distinct complete root science')
    need(review['author_manifest_sha256']==ad['author_manifest']['sha256'] and review['native_pages']==[11,9,7] and review['historical_ordinal_correspondences_unverified']==3 and not review['literal_source_equivalence'],'accepted exact edition/limits')
    need(len(source['main_and_count_clauses'])==73 and len(source['historical_label_claims'])==232 and source['mathematical_principal_obligations_unresolved']==[] and not source['literal_original_replacement_equivalence'],'all corrected source routes')
    claims=source['historical_label_claims'];need(sum(r['status']=='CONFIRMED_ON_EVERY_COMPATIBLE_CLASS' for r in claims)==229,'all229 profile claims')
    unverified=[r for r in claims if r['status']=='ORDINAL_UNVERIFIED_CORRECTED_PROFILE_CLASSIFICATION'];need(len(unverified)==3 and all(r['group']=='J1' and r['label']=='4.1' and not r['candidate_decisions'] for r in unverified),'three unassigned historical ordinals')
    for k in oldpapers:
        if k not in ['status','active_source_catalogue','corrected_unmeasured_scientific_catalogue']:need(papers[k]==oldpapers[k],'old measured catalogue '+k)
    need(papers['status']=='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_TWELVE_CORRECTED_UNMEASURED','paper status')
    need(sc['entries'][:-3]==oldsc['entries'] and sc['acquired_dependencies'][:-1]==oldsc['acquired_dependencies'],'prior native papers exact')
    need(sc['original_ids']==oldsc['original_ids']+['L096'] and sc['existing_comparison_topic_count']==19 and sc['new_measurements']==0,'unchanged comparison topics')
    need([r['physical_pages'] for r in sc['entries'][-3:]]==[11,9,7] and all(r['source_ids']==['L096'] and r['compiler']=='pdflatex' and not r['measured'] for r in sc['entries'][-3:]),'three complete native papers')
    need(sc['acquired_dependencies'][-1]['physical_pages']==6 and sc['acquired_dependencies'][-1]['pdf']=='papers/topic-d/v2/umbrella.pdf','old whole common acquired')
def controls(args):
    ans=[]
    def reject(n,f):
        a=copy.deepcopy(args);f(a)
        try:semantics(*a)
        except (ValueError,KeyError,IndexError):ans.append(n);return
        raise ValueError('control accepted '+n)
    reject('count science as measured',lambda a:a[0].__setitem__('currently_measured_originals',65))
    reject('duplicate new original',lambda a:a[0]['admitted_original_ids'].append('L096'))
    reject('remove another target',lambda a:a[0]['accessible_pending_original_ids'].pop())
    reject('change old measurement',lambda a:a[0]['added_measurements'].append({}))
    reject('change another original',lambda a:a[2]['entries'][0].__setitem__('title','changed'))
    reject('wrong source author',lambda a:a[8].__setitem__('source_author_role','Philippe Jacobs'))
    reject('omit old common',lambda a:a[8].__setitem__('old_whole_common_pages',0))
    reject('shorten companion',lambda a:a[8].__setitem__('physical_pages',[11,9,3]))
    reject('invent factor',lambda a:a[8].__setitem__('compression_factor',1))
    reject('claim literal names',lambda a:a[8].__setitem__('theorem_sets_equivalent',True))
    reject('claim formalization',lambda a:a[8].__setitem__('whole_source_formalized',True))
    reject('hide required whole file',lambda a:a[9]['all_occurrences'].pop())
    reject('role sums disjoint',lambda a:a[9].__setitem__('role_categories_disjoint',True))
    reject('unknown source code zero',lambda a:a[9].__setitem__('source_software_cost',0))
    reject('self-review substituted',lambda a:a[10].__setitem__('reviewer','enumeration_volume'))
    reject('wrong accepted edition',lambda a:a[10].__setitem__('author_manifest_sha256','0'*64))
    reject('drop main clause',lambda a:a[11]['main_and_count_clauses'].pop())
    reject('drop named occurrence',lambda a:a[11]['historical_label_claims'].pop())
    reject('assign historical ordinal',lambda a:next(r for r in a[11]['historical_label_claims'] if r['group']=='J1').__setitem__('candidate_decisions',[{}]))
    reject('old paper omitted',lambda a:a[6]['entries'].pop(0))
    reject('new comparison topic',lambda a:a[6].__setitem__('existing_comparison_topic_count',20))
    reject('retrieval reopened',lambda a:a[0].__setitem__('source_retrieval_in_scope',True))
    return ans
def root_gate(g,required):
    need(g['status']=='ROOT_ACCEPTED_SCIENCE65_PUBLICATION' and g['source_ids']==['L096'] and g['measurements_added']==g['new_question_credit']==0,'root-only publication gate')
    paths=[r['path'] for r in g['bindings']];need(len(paths)==len(set(paths)) and required<=set(paths),'all exact root bindings')
def verify(root,require_root=False):
    root=Path(root).resolve();base=load(HERE/'baseline.json');plan=load(HERE/'copy_plan.json')
    if (HERE/'manifest.json').exists():
        for r in load(HERE/'manifest.json')['exports']:bind(HERE,r)
    wrappers=load(HERE/'wrapper_routes.json')['files']
    for r in wrappers+base['protected_files']+plan['public_dependencies']:bind(root,r)
    routes={r['study_path']:r for r in plan['files']};need(len(routes)==len(plan['files'])==1346,'all logical files')
    checked=set()
    for r in plan['files']:
        n=r['public_path'];need(not n.endswith('.md') and not any(p in PurePosixPath(n).parts for p in ['sources','private_source','private_auxiliary','fonts','rasters']),'no primary assets or public Markdown')
        if n not in checked:bind(root,dict(path=n,bytes=r['bytes'],sha256=r['sha256']));checked.add(n)
    need(len(checked)==plan['unique_public_files']==1230 and len(plan['packets'])==28,'whole dependency transport')
    for p in plan['packets']:
        bind(root,p['manifest']);m=load(root/p['manifest']['path']);need(len(m['exports'])==p['exports'],'whole frozen packet')
        for r in m['exports']:
            n=str(PurePosixPath(p['study_manifest']).parent/r['path']);need(n in routes and all(routes[n][k]==r[k] for k in ['bytes','sha256']),'exact manifest logical export')
    history=load(root/AUDIT/'history_routes.json')['routes'];need(history==base['history'],'exact history overlay')
    for r in history.values():bind(root,r)
    old=load(root/history['audit/corpus/latest.json']['path']);c=load(root/'audit/corpus/latest.json')
    for k in ['active_catalogue','snapshot','current_science_registration']:bind(root,c[k])
    need(load(root/c['snapshot']['path'])=={k:v for k,v in c.items() if k!='snapshot'},'current immutable snapshot')
    bind(root,base['old_catalogue']);cat=load(root/c['active_catalogue']['path']);oldcat=load(root/base['old_catalogue']['path'])
    papers=load(root/'papers/latest_catalogue.json');oldpapers=load(root/history['papers/latest_catalogue.json']['path'])
    need(papers['active_source_catalogue']==c['active_catalogue'],'catalogue agreement');bind(root,papers['corrected_unmeasured_scientific_catalogue'])
    sc=load(root/papers['corrected_unmeasured_scientific_catalogue']['path']);oldsc=load(root/history['papers/catalogue_corrected_unmeasured.json']['path'])
    reg=load(root/c['current_science_registration']['path']);need(reg['source_ids']==['L096'] and reg['previous_registration']==old['current_science_registration'] and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==0,'one science-only registration')
    need(len(reg['admissions'])==1,'one admission');bind(root,reg['admissions'][0]);ad=load(root/reg['admissions'][0]['path'])
    for k in ['author_manifest','distinct_root_review_manifest','root_scientific_acceptance','source_map','dependency_boundary','source_ledger','program_roles','old_whole_common']:bind(root,ad[k])
    need(ad['author_manifest']['sha256']==plan['current_pins']['corpus106_L096_recovery'] and ad['distinct_root_review_manifest']['sha256']==plan['current_pins']['corpus106_L096_complete_root_review'],'accepted current pins')
    roles=load(root/ad['program_roles']['path']);review=load(root/SCIENCE/'root_review/review.json');source=load(root/ad['source_map']['path'])
    oldroles=load(root/SCIENCE/'author/whole_program_inventory.json')
    need([{k:v for k,v in r.items() if k!='public_binding'} for r in roles['all_occurrences']]==oldroles['all_occurrences'],'all exact original occurrence roles')
    for r in roles['all_occurrences']:
        need(r['public_binding']==dict(path=routes[r['path']]['public_path'],bytes=r['bytes'],sha256=r['sha256']),'whole occurrence public route');bind(root,r['public_binding'])
    args=[c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,review,source];semantics(*args);tests=controls(args)
    from pypdf import PdfReader
    for r in sc['entries'][-3:]:
        need(re.search(r'\\title\{([^{}]+)\}',(root/r['tex']).read_text()).group(1)==r['title'],'literal title')
        need(len(PdfReader(root/r['pdf']).pages)==r['physical_pages'] and r['admission']==reg['admissions'][0],'whole native PDF/admission')
    actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse((root/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
    need(len(base['old_nonmain_ASTs'])==155 and all(actual.get(k)==v for k,v in base['old_nonmain_ASTs'].items()),'155 exact prior verifier functions')
    t=(root/'README.rst').read_text();p=(root/'audit/protocol.tex').read_text()
    for x in ['65 accessible originals','53 are measured and twelve','40 await mathematical recovery','L096 guide','three J1 ordinal','Conjecture 1.1 remains unanswered']:need(x in t,'current reader '+x)
    need('106=65' in p and 'recoveries}+40' in p and 'Of the 65 corrected recoveries, 53' in p,'current protocol partition')
    links=0
    for n in ['README.rst','audit/completion.rst',NATIVE+'/PUBLICATION.rst']:
        for target in re.findall(r'<([^<>\n]+)>`_', (root/n).read_text()):
            if re.match(r'\w+://',target):continue
            need((root/PurePosixPath(n).parent/target).exists(),'local link '+target);links+=1
    required={r['path'] for r in wrappers}|{r['public_path'] for r in plan['files'] if r['public_path'].startswith(NATIVE+'/')}|{AUDIT+'/publication_plan/manifest.json','scripts/verify_snapshot.py'}
    if require_root:
        gate=load(root/AUDIT/'root_integration.json');root_gate(gate,required)
        for r in gate['bindings']:bind(root,r)
    return dict(status='PASS_SCIENCE65_PUBLICATION_ROUTES',publication_status='ROOT_ACCEPTED' if require_root else 'ROOT_PUBLICATION_NOT_ADJUDICATED',counts=dict(active=106,corrected_recoveries=65,measured=53,unmeasured=12,mathematical_pending=40,editorial=1,archived=55,comparison_topics=19),logical_payload_routes=1346,complete_frozen_packets=28,unique_public_files=1230,other_originals_preserved=105,old_verifier_functions_preserved=155,new_native_pages=[11,9,7],old_whole_common_pages=6,new_factors=0,checked_links=links,controls=tests,required_root_gate_paths=sorted(required),old_censuses_or_Lean_repeated=False)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path);p.add_argument('--require-root',action='store_true');a=p.parse_args();r=verify(a.repo,a.require_root)
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r))
