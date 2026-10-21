#!/usr/bin/env python3
"""Independent metadata/set/binding checks; no mathematical or numerical re-adjudication."""
import argparse,copy,csv,hashlib,io,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent

def require(x, why):
    if not x: raise ValueError(why)
def load(p): return json.loads(p.read_text())
def bound(root,row):
    p=pathlib.PurePosixPath(row['path']);require(not p.is_absolute() and '..' not in p.parts,'unsafe path')
    b=(root/p).read_bytes();require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+str(p));return b

def semantic(c,a,old,inv,latest,single,rows):
    E={x['original_id']:x for x in c['entries']};A={x['original_id']:x for x in a['entries']};I={x['original_id']:x for x in inv['entries']}
    require(len(E)==len(c['entries'])==106,'106 unique active entries')
    require(len(A)==len(a['entries'])==55,'55 unique archive entries')
    old_access={i for i,e in I.items() if e['source_access']['accessible']}|{'L084','L100'}
    require(len(I)==161 and len(old_access)==106 and set(E)==old_access,'exact previous accessible source set')
    require(set(A)==set(I)-old_access and not(set(A)&set(E)),'exact archived complement')
    require(set(old['admitted_original_ids'])=={i for i,e in E.items() if e['current_principal_recovery']['status']=='ADMITTED_AND_MEASURED'},'42 unchanged admitted IDs')
    require(set(old['accessible_pending_original_ids'])=={i for i,e in E.items() if e['current_principal_recovery']['status']=='PENDING_COMPLETE_RECOVERY'},'64 unchanged pending IDs')
    require(c['active_originals']==106 and c['admitted_principal_originals']==42 and c['accessible_pending_complete_recovery']==64 and c['archived_unavailable_originals']==55,'catalogue counts')
    require(c['source_retrieval_in_scope'] is False and a['retrieval_scheduled'] is False,'retrieval stopped')
    require(c['new_proof_credit']==c['new_question_credit']==0,'no science credit')
    require(all(e['active'] is True and e['original_count']==1 and e['source_access']['accessible'] is True and e['source_access']['pending_retrieval'] is False for e in E.values()),'active per-entry scope')
    require(all(e['active'] is False and e['retrieval_scheduled'] is False and e['historical_access']==I[i]['source_access'] for i,e in A.items()),'archive/history preserved')
    require(all(e['title']==I[i]['title'] and e['authors']==I[i]['authors'] for i,e in E.items()),'fixed original identities')
    require(set(latest['active_original_ids'])==set(E) and set(latest['archived_original_ids'])==set(A),'latest scope IDs')
    require(latest['originals']==106 and latest['historical_originals']==161 and latest['accessible_originals']==106 and latest['archived_unavailable_originals']==55 and latest['admitted_principal_originals']==42 and latest['accessible_pending_complete_recovery']==64,'latest counts')
    require(latest['source_retrieval_in_scope'] is False and latest['pending_source_retrieval']==0 and latest['retrieval_original_ids']==[] and latest['all_historical_originals_remain_active'] is False,'latest retrieval and historical distinction')
    for k in ['admitted_original_ids','accessible_pending_original_ids','measured_original_ids','added_measurements','superseded_measurement_admissions','added_admissions','currently_measured_originals','measurement_pending_original_ids','all_conjectures_resolved','all_original_proofs_recovered']:
        require(latest[k]==old[k],'preserved '+k)
    require(latest['all_conjectures_resolved'] is False and latest['all_original_proofs_recovered'] is False,'no blanket recovery')
    require(len(rows)==106 and {r['original_id']for r in rows}==set(E),'complete CSV')
    for r in rows:
        e=E[r['original_id']];require(r['title']==e['title'] and r['principal_recovery_status']==e['current_principal_recovery']['status'] and r['accessible']==r['active']=='True','CSV row')
    new=set(old['admitted_original_ids'])-set(old['historical_admitted_ids']);require(len(new)==15,'15 postbaseline original contracts')
    for i in new:
        e=E[i];p=e['principal_results_to_recover'];q=e['current_principal_recovery']
        require(p['scope_status']=='ADMITTED_CORRECTED_PRINCIPAL_CONTRACT' and p['current_contract_admissions']==q['latest_admission_references'] and p['current_application_routes']==q['current_application_routes'] and len(p['current_application_routes'])>0 and len(p['current_contract_admissions'])>0,'current contract routes '+i)
        require('historical_principal_targets' in e,'old target retained '+i)
    sources={i:{q['sha256'] for q in E[i]['source_access']['usable_representations']}for i in ['L084','L100','L040','N005']}
    for i,h in [('L084','63789bad8fa35c53feee35275bf1f85dd52a54df905c768dd5257240b7f7ddb6'),('L100','3bd275e4bd344dea8a75fd2c4aeafd69cbe2ca975b3b58933dc7fe4105c5e11e'),('L100','13f207232f40ca0e00674b9e9de02a91e98226b325ddd428320c661e6131ff84'),('L040','1945f07fb2a0395c9a033b5fc1aeb7f5f40cfcd8b2598d43679cf60eb24de9bb'),('N005','9ac31adc29a5cc66a4b412e0adae7fb47152568db89d1207ee2c34f134ee1427')]:require(h in sources[i],'current source '+i)
    require(E['L084']['source_access']['availability_evidence_category']=='verified_complete_published_erratum','L084 accessible edition')
    require(E['L100']['source_access']['availability_evidence_category']=='verified_complete_institutional_preprint' and E['L100']['principal_results_to_recover']['status']=='ACCESSIBLE_AWAITING_COMPLETE_RECOVERY','L100 access without recovery')
    require(E['L100']['principal_results_to_recover']['principal_targets'][0]['outputs']=={'rank2':7,'rank3':7,'rank4':11,'rank5':4,'rank6':0},'L100 complete pending targets')
    require('2003 journal edition is not claimed identical' in E['L100']['next_obligation'],'L100 edition limitation')
    require(any(r['tex']=='papers/topic-b/v3/high-rank-symmetric-markings.tex' for r in E['L040']['current_principal_recovery']['current_application_routes']),'current unified B5 route')
    for i in ['L040','L030','N001','N003','N008']:
        require('papers/topic-b/latest.json' in json.dumps(E[i]['current_principal_recovery']),'current B pointer '+i)
    require(single['excluded_originals']==[] and single['measured_singleton_topics']==10 and len(single['entries'])==10,'no singleton exclusions')
    require(all(e['exclusion_applied'] is False and len(e['source_ids'])==1 and set(e['source_ids'])<=set(old['measured_original_ids']) for e in single['entries']),'singleton scope')
    return {'active':106,'archive':55,'admitted_and_measured':42,'pending':64,'new_contract_routes':15,'singletons_retained':10}

def audit(public,study=None):
    pins=load(HERE/'bindings.json');verified=0
    for q in pins['public']:
        bound(public,q);verified+=1
    c=load(public/'audit/corpus/accessible106/catalogue.json');a=load(public/'audit/corpus/accessible106/archived_unavailable.json');old=load(public/'audit/corpus/updates/mixes-measured.json');inv=load(public/'audit/corpus/v1/packet/inventory.json');latest=load(public/'audit/corpus/latest.json');single=load(public/'audit/corpus/accessible106/singleton_topics.json');rows=list(csv.DictReader(io.StringIO((public/'audit/corpus/accessible106/catalogue.csv').read_text())))
    args=[c,a,old,inv,latest,single,rows];counts=semantic(*args)
    admission=load(public/'audit/corpus/accessible106/admission.json')
    for q in admission['artifacts']+[admission['previous_snapshot']]:bound(public,q)
    require(admission['active_originals']==106 and admission['archived_originals']==55 and admission['source_retrieval_in_scope'] is False and all(admission[k]==0 for k in ['principal_credit_added','question_credit_added','measurement_factor_changes','singletons_excluded']),'scope-only admission')
    for q in old['added_admissions']+old['added_measurements']+old['access_additions']+old['superseded_measurement_admissions']:bound(public,q)
    require(load(public/latest['snapshot']['path'])=={k:v for k,v in latest.items()if k!='snapshot'},'latest exact snapshot')
    for k in ['snapshot','active_catalogue','scope_admission','scope_archive']:bound(public,latest[k])
    source_rows=[];route_rows=[];source_verified=0
    for e in c['entries']:
        i=e['original_id']
        for q in e['source_access']['usable_representations']:
            source_rows.append({'original_id':i,**{k:q[k]for k in ['namespace','path','sha256','bytes']}})
            if study:
                if q['namespace']=='study': bound(study,q)
                elif q['namespace']=='private_access_packet':
                    packet={'L084':'corpus161_access_supplement_v3','L100':'corpus161_access_supplement_v4'}[i];bound(study/packet,q)
                else: raise ValueError('unhandled source namespace')
                source_verified+=1
        cr=e['current_principal_recovery']
        for q in cr.get('latest_admission_references',[]):bound(public,q)
        for q in cr.get('current_application_routes',[]):
            for k in ['tex','pdf','admission']:require((public/q[k]).is_file(),'current route exists')
            route_rows.append({'original_id':i,**q})
        if cr['status']=='ADMITTED_AND_MEASURED' and not cr.get('latest_admission_references'):
            evidence=cr['historical_admission_evidence'];require(evidence['principal_contract_admitted'] is True,'baseline27 admission')
            canonical=[q for q in evidence['evidence'] if q.get('role')=='current canonical proof/contract admission'];require(bool(canonical),'baseline proof record')
            for q in canonical:bound(public,q)
    tests=[]
    def reject(name,fn):
        trial=copy.deepcopy(args);fn(trial)
        try:semantic(*trial)
        except (ValueError,KeyError,IndexError):tests.append(name);return
        raise ValueError('mutation accepted: '+name)
    def entry(v,i):return next(e for e in v[0]['entries']if e['original_id']==i)
    reject('drop_active_original',lambda v:v[0]['entries'].pop())
    reject('duplicate_original',lambda v:v[0]['entries'].append(copy.deepcopy(v[0]['entries'][0])))
    reject('restore_archived_original',lambda v:v[0]['entries'].__setitem__(0,copy.deepcopy(v[3]['entries'][0])))
    reject('lost_archived_identity',lambda v:v[1]['entries'].pop())
    reject('renew_retrieval',lambda v:v[4].__setitem__('source_retrieval_in_scope',True))
    reject('premature_L007_credit',lambda v:entry(v,'L007')['current_principal_recovery'].__setitem__('status','ADMITTED_AND_MEASURED'))
    reject('lost_measurement',lambda v:v[4]['measured_original_ids'].pop())
    reject('changed_measurement_reference',lambda v:v[4]['added_measurements'][0].__setitem__('sha256','0'*64))
    reject('omitted_singular_admission',lambda v:entry(v,'F015')['current_principal_recovery'].__setitem__('latest_admission_references',[]))
    reject('stale_L084_availability',lambda v:entry(v,'L084')['source_access'].__setitem__('availability_evidence_category','prior_failed_fulltext_search'))
    reject('lost_L100_source',lambda v:entry(v,'L100')['source_access'].__setitem__('usable_representations',[]))
    reject('weakened_L100_target',lambda v:entry(v,'L100')['principal_results_to_recover']['principal_targets'][0]['outputs'].__setitem__('rank5',0))
    reject('stale_L040_source',lambda v:entry(v,'L040')['source_access']['usable_representations'].pop())
    reject('stale_N005_source',lambda v:entry(v,'N005')['source_access']['usable_representations'].pop())
    reject('singleton_exclusion',lambda v:v[5]['entries'][0].__setitem__('exclusion_applied',True))
    reject('new_science_credit',lambda v:v[0].__setitem__('new_proof_credit',1))
    reject('false_all_recovered',lambda v:v[4].__setitem__('all_original_proofs_recovered',True))
    reject('CSV_inconsistent',lambda v:v[6][0].__setitem__('principal_recovery_status','ADMITTED_AND_MEASURED'))
    require(load(public/'audit/corpus/accessible106/catalogue.json')['entries']==c['entries'],'no mutation of inputs')
    return {'status':'PASS','counts':counts,'public_bindings_verified':verified,'listed_source_representations':len(source_rows),'actual_source_byte_bindings_verified':source_verified,'current_application_routes_verified':len(route_rows),'semantic_controls_rejected':tests,'scope':'Metadata, exact ID sets, current source/proof routes and unchanged measurement references; no new mathematical, font or arithmetic adjudication.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--public-root',type=pathlib.Path,required=True);p.add_argument('--study-root',type=pathlib.Path);p.add_argument('--out',type=pathlib.Path,required=True);v=p.parse_args();report=audit(v.public_root,v.study_root);v.out.parent.mkdir(parents=True,exist_ok=True);v.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
