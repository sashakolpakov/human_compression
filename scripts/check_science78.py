"""Verify the additive L059 recovery without weakening historical checks."""
from pathlib import Path
import argparse, ast, copy, hashlib, json, sys
if sys.flags.optimize:
    raise RuntimeError('Optimized Python is not supported')
AUD='audit/science78/v1'
REC='audit/recoveries/L059/v1'
DIGEST='67996de3c2d9bca084a7436bd10c1d46312bed1f3e14ea559d4471498a788885'
def need(ok, message):
    if not ok: raise ValueError(message)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(root, name): return json.loads((root/name).read_text())
def bind(root, row):
    path=root/row['path']
    need(not Path(row['path']).is_absolute() and path.resolve().is_relative_to(root.resolve()),'Unsafe public binding')
    need(path.is_file() and sha(path)==row.get('stored_sha256',row['sha256']),'Changed public binding: '+row['path'])
    need(path.stat().st_size==row.get('stored_bytes',row.get('bytes',path.stat().st_size)),'Changed binding size')
def unique(actual, expected, label):
    need(len(actual)==len(set(actual)) and set(actual)==set(expected),label)
def semantics(c, old, a, scope):
    for key, number in [('admitted_original_ids',78),('handled_mathematical_original_ids',79),('measurement_pending_original_ids',25),('scientific_unmeasured_original_ids',25)]:
        unique(c[key],old[key]+['L059'],'Only L059 added: '+key)
        need(len(c[key])==number,'Exact count: '+key)
    unique(c['accessible_pending_original_ids'],set(old['accessible_pending_original_ids'])-{'L059'},'Only L059 removed from pending')
    need(c['admitted_principal_originals']==78 and c['handled_mathematical_originals']==79 and c['accessible_pending_complete_recovery']==26,'Exact current partition')
    mutable={'status','admitted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery','previous_snapshot','active_catalogue','current_science_registration','admitted_original_ids','handled_mathematical_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids','accessible_pending_original_ids','added_admissions','snapshot'}
    need(set(c)==set(old),'Same corpus schema')
    for key in set(old)-mutable: need(c[key]==old[key],'Unrelated corpus property changed: '+key)
    need(c['added_admissions'][:-1]==old['added_admissions'] and c['added_admissions'][-1]['path']==REC+'/admission.json','Single new admission')
    need('L046' in c['accessible_pending_original_ids'] and 'F012' in c['accessible_pending_original_ids'],'Bounded components not whole recoveries')
    need(a['source_ids']==['L059'] and a['principal_originals_added']==1 and a['whole_original_credit']==0,'Only final root gate grants credit')
    need(a['complete_principal_contract_recovered'] and a['corrected_principal_recovery'] and not a['all_original_assertions_claimed'],'Corrected principal contract only')
    need(a['compression_factor'] is a['software_inclusive_factor'] is None and a['new_question_credit']==a['new_Lean_declarations']==a['new_measurements']==0 and not a['whole_source_formalized'] and not a['measured'],'No new measurement, conjecture or formalization')
    need(set(a['component_acceptance'])=={'complete'} and set(a['component_acceptance']['complete'])=={'author','distinct','root_adoption'},'Complete acceptance chain')
    need(set(a['complete_acquired_proofs'])=={'historical_quartic','subdivision_actions'},'Both acquired proof components')
    need(len(a['intermediate_corrections'])==8 and scope['documentary_qualifications']==a['intermediate_corrections'],'All eight source qualifications')
    need(scope['original']=='L059' and len(scope['routes'])==11 and len({r['id'] for r in scope['routes']})==11 and scope['complete_closure'],'Eleven principal source routes')
    need(a['counts']==scope['counts']==dict(graphs=1950,faithful_markings=4254,printed_table_cells=39,symmetric_cubic=[714,1082],semisymmetric_cubic=[43,102],subdivisions=[796,1427],quartic_corrected_scope=[397,1643]),'Every census family and table cell')
    need(a['open_questions']==scope['open_questions'] and a['open_questions']['new_question_credit']==0 and 'unclaimed' in a['open_questions']['final_problem'] and 'unclaimed' in a['open_questions']['arxiv_only'],'Both recorded questions unclaimed')
    need(a['immediate_manuscripts']==3 and a['physical_pages']==15 and a['logical_files']==10573 and a['restored_mathematical_and_audit_files']==10554 and a['source_assets_hash_only']==19 and a['acquired_packets']==9 and not a['private_runtime_fallback'],'Exact proof and documentary boundary')
    need(a['document_inventory_not_measurement']=='The fifteen immediate manuscript pages are entry points to the complete acquired proof and validation closure, not a compression denominator.','Document pages not a denominator')
def verify(root, require_root=True):
    root=Path(root).resolve();history=load(root,AUD+'/history_routes.json')['routes']
    for row in history.values(): bind(root,row)
    old=load(root,history['audit/corpus/latest.json']['path']);c=load(root,'audit/corpus/latest.json');a=load(root,REC+'/admission.json');scope=load(root,REC+'/scope_routes.json');semantics(c,old,a,scope)
    for key in ['active_catalogue','snapshot','current_science_registration']: bind(root,c[key])
    need(load(root,c['snapshot']['path'])=={k:v for k,v in c.items() if k!='snapshot'},'Exact snapshot')
    cat=load(root,c['active_catalogue']['path']);oldcat=load(root,old['active_catalogue']['path']);need(len(cat['entries'])==len(oldcat['entries'])==106,'Fixed original catalogue')
    for before,after in zip(oldcat['entries'],cat['entries']):
        if before['original_id']!='L059': need(before==after,'Another original entry changed')
        else:
            need(set(before)==set(after),'Original schema preserved')
            for key in set(before)-{'current_principal_recovery','next_obligation'}: need(before[key]==after[key],'Historical source data changed')
            x=after['current_principal_recovery'];need(x['historical_admission_evidence']==before['current_principal_recovery'] and x['principal_contract_admitted'] and x['complete_principal_contract_recovered'] and x['corrected_principal_recovery'] and not x['all_original_assertions_claimed'] and not x['measured'],'L059 admission and historical evidence')
            need(x['source_qualifications']==a['intermediate_corrections'] and x['open_questions']==a['open_questions'] and x['counts']==a['counts'],'Catalogue qualifications and scope')
    need(cat['current_recovery_counts']==dict(active=106,admitted=78,refuted=1,handled=79,measured=53,measurement_pending=25,pending=26,editorial=1),'Catalogue current partition')
    reg=load(root,c['current_science_registration']['path']);need(reg['source_ids']==['L059'] and reg['previous_registration']==old['current_science_registration'] and reg['principal_originals_added']==1 and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==reg['comparison_topics_added']==0 and reg['compression_factor'] is None and not reg['whole_source_formalized'],'One-original registration without other credit')
    need(len(reg['admissions'])==1 and reg['admissions'][0]['path']==REC+'/admission.json','Exact admission');bind(root,reg['admissions'][0])
    for row in a['component_acceptance']['complete'].values(): bind(root,row)
    for chain in a['complete_acquired_proofs'].values():
        need(set(chain)=={'author','review'},'Reviewed acquired component')
        for row in chain.values(): bind(root,row)
    for key in ['source_map','scope_routes','portable_report','portable_checker','portable_replay','portable_transport']: bind(root,a[key])
    for item in a['new_native_manuscripts']: bind(root,item['tex']);bind(root,item['pdf'])
    transport=load(root,a['portable_transport']['path']);need(sha(root/a['portable_transport']['path'])==DIGEST and transport['logical_files']==10573 and len(transport['packets'])==9,'Exact transport')
    public={r['public_path']:r for r in transport['files'] if 'public_path' in r};need(len(public)==8574 and len(transport['files'])==10573 and sum('public_path' not in r for r in transport['files'])==19 and not transport['private_mathematical_proof_fallback'],'All public proofs; fixed documentary omissions')
    for path,row in public.items(): bind(root,dict(row,path=path))
    replay=load(root,a['portable_report']['path']);need(replay['status']=='PASS_PUBLIC_L059_COMPLETE_CLOSURE' and replay['transport_sha256']==DIGEST and replay['logical_files']==10573 and replay['restored_files']==10554 and replay['unique_decoded_payloads']==8574 and replay['packets']==9 and replay['exports']==118 and replay['exact_metadata_pins']==43321 and replay['documentary_hash_only']==19,'Complete replay scope')
    need(replay['graphs']==1950 and replay['faithful_markings']==4254 and replay['printed_cells']==39 and replay['numeric_inputs']==839 and replay['explicit_reuse_isomorphisms']==261 and replay['method_control_graphs']==5 and not replay['private_runtime_fallback'] and not replay['full_census_repeated'] and len(replay['malformed_controls'])==8,'Exact bounded numerical replay')
    need([r['pages']for r in replay['native']]==[10,3,2] and all(r['text_identical']for r in replay['native']),'Complete native manuscript rebuilds')
    previous=load(root,history['papers/catalogue_corrected_unmeasured.json']['path']);native=load(root,'papers/catalogue_corrected_unmeasured.json');need(native['entries'][:-3]==previous['entries'] and native['original_ids']==previous['original_ids']+['L059'] and native['existing_comparison_topic_count']==19 and native['new_measurements']==0 and native['acquired_dependencies']==previous['acquired_dependencies'],'Old manuscripts and measurements unchanged')
    need([r['physical_pages']for r in native['entries'][-3:]]==[10,3,2],'Three full entry manuscripts')
    for actual,expected in zip(native['entries'][-3:],a['new_native_manuscripts']): need(actual['id']==expected['id'] and actual['tex']==expected['tex']['path'] and actual['pdf']==expected['pdf']['path'] and not actual['measured'] and actual['compression_factor'] is None,'Exact native route')
    paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,history['papers/latest_catalogue.json']['path']);need(set(paper)==set(oldpaper),'Paper schema preserved')
    for key in set(oldpaper)-{'active_source_catalogue','corrected_unmeasured_scientific_catalogue'}: need(paper[key]==oldpaper[key],'Unrelated paper route changed')
    need(paper['active_source_catalogue']==c['active_catalogue'],'Paper source routing');bind(root,paper['corrected_unmeasured_scientific_catalogue'])
    oldtree=ast.parse((root/history['scripts/verify_snapshot.py']['path']).read_text());newtree=ast.parse((root/'scripts/verify_snapshot.py').read_text())
    def functions(tree): return {n.name:ast.dump(n,include_attributes=False)for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
    oldf,newf=functions(oldtree),functions(newtree);need(all(newf.get(k)==v for k,v in oldf.items()),'Old verifier functions changed');added={'check_previous_science78','check_science78'};need(set(newf)-set(oldf)==added,'Exactly two new verifier functions')
    def remaining(tree,exclude): return [ast.dump(n,include_attributes=False)for n in tree.body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in exclude)]
    need(remaining(oldtree,{'main'})==remaining(newtree,{'main'}|added),'Other top-level verifier nodes preserved')
    controls=[]
    mutations=[('duplicate original',lambda c,a,s:c['admitted_original_ids'].append('L059')),('remove another pending',lambda c,a,s:c['accessible_pending_original_ids'].remove('F012')),('invent factor',lambda c,a,s:a.update(compression_factor=2)),('unrestricted overclaim',lambda c,a,s:a.update(all_original_assertions_claimed=True)),('lose correction',lambda c,a,s:a['intermediate_corrections'].pop()),('omit source route',lambda c,a,s:s['routes'].pop()),('omit acquired proof',lambda c,a,s:a['complete_acquired_proofs'].pop('historical_quartic')),('omit distinct review',lambda c,a,s:a['component_acceptance']['complete'].pop('distinct')),('invent question',lambda c,a,s:a.update(new_question_credit=1)),('change census',lambda c,a,s:a['counts'].update(graphs=1949)),('extra omission',lambda c,a,s:a.update(source_assets_hash_only=20)),('wrapper length only',lambda c,a,s:a.update(document_inventory_not_measurement='15 pages'))]
    for label,fn in mutations:
        cc,aa,ss=copy.deepcopy((c,a,scope));fn(cc,aa,ss)
        try: semantics(cc,old,aa,ss)
        except (ValueError,KeyError): controls.append(label)
        else: raise ValueError('Invalid registration accepted: '+label)
    operational=load(root,AUD+'/operational_review.json');need(operational['status']=='ACCEPTED_L059_PUBLIC_TRANSPORT' and operational['logical_files_rehashed']==10554 and operational['distinct_payloads']==8574 and operational['whole_original_credit']==0,'Distinct operational review')
    for row in load(root,AUD+'/operational_review/mapping.json')['bindings'].values(): bind(root,row)
    if require_root:
        gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_SCIENCE78_PUBLICATION' and gate['source_ids']==['L059'] and gate['whole_original_credit']==1 and gate['new_question_credit']==gate['new_Lean_declarations']==gate['new_measurements']==0 and gate['compression_factor'] is None,'Final root gate')
        for row in gate['bindings']: bind(root,row)
        need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_L059_REGISTRATION','Distinct registration review')
    return dict(status='PASS_SCIENCE78_PUBLICATION',counts=dict(active=106,corrected_recoveries=78,refuted=1,handled=79,measured=53,unmeasured=25,mathematical_pending=26,editorial=1,archived=55,comparison_topics=19),source_ids=['L059'],old_verifier_functions_preserved=len(oldf),public_payloads={'L059':8574},controls=controls)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--preflight',action='store_true');args=parser.parse_args();print(json.dumps(verify(args.repo,require_root=not args.preflight)))
