import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,copy
def read(p):return json.loads(p.read_text())
def need(v,m):
    if not v:raise ValueError(m)
EXCLUDED={'Table3.3434.1','Table3.3534.1','Table3.3535.1','Table3.3535.2'}
MIN=[('3334',7680,168,1920,None),('3335',7200,2520,7200,None),('3434',9216,168,1152,None),('3534',2160,1080,None,2160),('3535',3840,1920,None,3840),('353',8160,660,8160,None),('435',7680,1920,3840,None),('535',8160,3420,7200,None),('5333',7680,960,3840,None)]
def validate(L,N,M,B,C):
    rows=L['rows'];need(len(rows)==109 and len({r['id']for r in rows})==109,'exact109unique source clauses')
    D={r['id']:r for r in rows};need(L['legacy_rows']==83 and L['additional_table2_rows']==21 and L['additional_scope_rows']==5,'stable83+21+5')
    need(L['source']=='L033'and L['source_sha256']=='f6f3e9eefc06bbaec9da34dae97497e89551b5269033a72bc52ec1c9c5b9ab28','fixed source')
    need(not any('PENDING'in r['status']for r in rows),'no unresolved source routing')
    need(all(1<=r['manuscript_section']<=7 for r in rows),'actual manuscript sections')
    need(len(C)==12 and all(k in C for r in rows for k in r['component_keys']),'complete component interfaces')
    need(D['E2.5']['component_keys']==['cubic']and D['E2.5']['status']=='ACQUIRED_COMPLETE_PROOF','actual infinite cubic proof')
    need(D['P2.2']['status']==D['C.reducible']['status']=='PROVED_ELEMENTARY_SYNTHESIS_JOIN','two written elementary joins')
    need(D['T5.1']['source_label']=='Corollary 5.1','literal numbering')
    need(D['T4.1']['status']=='RETAINED_CLASSIFICATION'and D['T2.4']['status']=='RETAINED_CLASSICAL_INPUT','retained substantive classification')
    need(D['C.affine_future']['status']=='NOT_A_PROVED_SOURCE_RESULT'and D['C.rank5_search']['status']=='NOT_A_NEGATIVE_EXISTENCE_RESULT','future/inconclusive boundary')
    need(len([r for r in rows if r['id'].startswith('Table2.')])==21 and D['Table2.affine.A1']['source_domain']=='rank2','diagram boundary')
    need(D['C.affine_rank2_boundary']['status']=='EXPLICIT_BOUNDARY','rank>=3 existence boundary')
    need(len(N)==22 and len({r['source_id']for r in N})==22,'22literal named certificates')
    named={r['source_id']for r in N};printed={r['id']for r in rows if r['id'].startswith('Table3.')}
    need(len(printed)==26 and named.isdisjoint(EXCLUDED)and printed==named|EXCLUDED,'entire printed table partition')
    for r in N:
        q=D[r['source_id']];need(q['status']=='ACQUIRED_POSITIVE_NAMED_MARKING','positive disposition')
        a=q['actual_certificate'];need(all(a[k]==r[k]for k in ['type','order','selected_node','local_orders','printed_group']),'actual marking/name join')
    need({r['id']for r in rows if r['status']=='ACQUIRED_EXCLUDED_PRINTED_ROW'}==EXCLUDED,'exact4exclusions')
    need([(r['type'],r['bound'],r['broad'],r['universal'],r['universal_exclusion'])for r in M]==MIN,'all9corrected minima')
    for r in M:
        q=D['Minimum.'+r['type']];need((q['complete_bound'],q['broad_minimum'],q['universal_minimum'],q['universal_lower_bound_exclusive'])==(r['bound'],r['broad'],r['universal'],r['universal_exclusion']),'source minimum join')
    need(len(L['retained_inputs'])==8 and len(L['corrections'])==7,'retained inputs/corrections explicit')
    need([r['source_reference']for r in B]==list(range(1,30))and all(r['roles']and r['literal_extracted_text']for r in B),'all29 source citations')
    need(not L['principal_refutation']and not L['public_admission']and all(L[k]==0 for k in ['new_measurements','new_Lean','new_question_credit']),'author scope and no credit mutation')
    return True
def controls(args):
    validate(*args);out=[]
    changes=[('missing clause',lambda a:a[0]['rows'].pop()),('duplicate clause',lambda a:a[0]['rows'].__setitem__(1,copy.deepcopy(a[0]['rows'][0]))),('source change',lambda a:a[0].__setitem__('source_sha256','0'*64)),('unreviewed cubic',lambda a:next(r for r in a[0]['rows']if r['id']=='E2.5').__setitem__('component_keys',[])),('lost local condition',lambda a:a[2][3].__setitem__('universal',2160)),('invented universal minimum',lambda a:a[2][4].__setitem__('universal',9720)),('unlabelled count substitution',lambda a:a[1].pop()),('wrong named mark',lambda a:a[1][0].__setitem__('selected_node',9)),('wrong local order',lambda a:a[1][0]['local_orders'].__setitem__(0,12)),('wrong abstract name',lambda a:a[1][0].__setitem__('printed_group','A5')),('lost citation',lambda a:a[3].pop()),('removed retained theorem',lambda a:next(r for r in a[0]['rows']if r['id']=='T4.1').__setitem__('status','PROVED')),('future theorem promoted',lambda a:next(r for r in a[0]['rows']if r['id']=='C.affine_future').__setitem__('status','PROVED')),('rank5 negative invented',lambda a:next(r for r in a[0]['rows']if r['id']=='C.rank5_search').__setitem__('status','NONEXISTENT')),('missing premise',lambda a:a[0]['retained_inputs'].pop()),('new measurement',lambda a:a[0].__setitem__('new_measurements',1)),('premature public gate',lambda a:a[0].__setitem__('public_admission',True)),('wrong source table partition',lambda a:a[1][0].__setitem__('source_id','Table3.3535.1'))]
    for label,f in changes:
        a=copy.deepcopy(args);f(a)
        try:validate(*a)
        except(ValueError,KeyError):out.append(label)
        else:raise ValueError('damage accepted '+label)
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--join',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(a.out.is_absolute()and not a.out.exists(),'fresh output')
    args=[read(a.join/n)for n in ['claim_register.json','named_rows.json','minima.json','bibliography_routes.json','components.json']];bad=controls(args);a.out.mkdir();r=dict(status='PASS_L033_LITERAL_SOURCE_CONTRACT',rows=109,damage_controls=len(bad),damages=bad,target_censuses=0);(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
