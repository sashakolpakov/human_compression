"""Join acquired complete applications without rerunning their scientific calculations."""
from pathlib import Path
import argparse,copy,json
P=Path(__file__).resolve().parent;A=P.parent

def need(b,m):
    if not b:raise ValueError(m)
def read(p):return json.loads(Path(p).read_text())
FOLDERS=dict(alt10='alternating_ten_structural_v1',alt11='alternating_eleven_structural_v2',m23='mathieu_twenty_three_structural_v1',sp45='symplectic_four_five_structural_v1',sp47='symplectic_four_seven_structural_v1',sp62='symplectic_six_two_structural_v1',sym10='symmetric_ten_structural_v1')
EXPECTED=dict(alt10=(1814400,430),alt11=(19958400,788),m23=(10200960,204),sp45=(4680000,307),sp47=(138297600,603),sp62=(1451520,1369),sym10=(3628800,1593))

def join(scope,large,small,review,source_rows,claims):
    need(review==dict(status='SUPPORTS_NARROW_ARTICLE_MAIN_RESULTS_SYNTHESIS_WITH_EXPLICIT_LIMITS',requires_all36_current_large_tables_from_article_alone=False,article_main_results_criterion_supported=True,complete_historical_or_current_atlas_recovered=False,sporadic_large_examples_acquired=['M23'],remaining_companion_claims_preserved=True,whole_original_credit=0,count_changes=0,target_runs=0),'exact independently reviewed source contract')
    expected=dict(simple_socles=56,almost_simple_classes=127,old_tables=80,new_tables=47,new_rows=2468,new_edges=6248,total_small_structural_rows=10694)
    need(all(type(small.get(k))is int and small[k]==v for k,v in expected.items()),'acquired complete small-domain totals')
    ts=small['targets'];need(len(ts)==47 and len({t['table']for t in ts})==47,'47 distinct extra tables')
    need(sum(t['rows']for t in ts)==2468 and sum(t['edges']for t in ts)==6248,'exact extra rows and edges')
    for t in ts:
        need(type(t['order'])is int and t['order']<=10**6,'article bound on group order')
        need([r['row']for r in t['structural_rows']]==list(range(2,t['rows']+1)),'all extra proper structural rows')
    need(len(large)==7 and {t['table']for t in large}==set(EXPECTED),'exact seven larger applications')
    for t in large:
        n=t['table'];order,count=EXPECTED[n]
        need(t['order']==order and t['source_rows']==count and t['structural_rows_accepted']==count and t['structural_rows_pending']==0,'complete exact larger table')
        need(t['numeric']['status']=='ACCEPTED_COMPLETE_CURRENT_NUMERICS','accepted numerical prerequisite')
        need('ACCEPTED'in read(Path(t['structural_review']['path']))['status'],'actual distinct table review')
        rows=source_rows[n]
        need([(r['table'],r['row'])for r in rows]==[(n,i)for i in range(1,count+1)],'complete exact native source-row domain')
        if n=='alt11':
            need(t['structural_printed_labels_recovered']==787 and t['structural_printed_labels_refuted_and_corrected']==1 and t['structural_correction']['row']==186,'A11 correction retained')
            need(rows[185]['tree']==['split',['nonsplit',['C',2],['A',5]],['C',2]],'printed left-associated A11 tree retained')
    counts=dict(small_groups=127,small_rows=10694,new_small_tables=47,new_small_rows=2468,large_groups=7,large_rows=5294,total_groups=134,total_rows=15988,current_companion_complete_tables=87,current_companion_structural_rows=13520,source_labels_refuted_and_corrected=1)
    need(all(type(scope.get(k))is int and scope[k]==v for k,v in counts.items()),'exact aggregate counts and scalar types')
    need(sum(t['source_rows']for t in large)==5294 and 10694+5294==15988 and 8226+5294==13520,'disjoint source and additional application totals')
    need(scope['article_order_bound']=='|G| <= 1000000','article uses G order')
    need(scope['large_sporadic_examples']==['M23'],'only one acquired larger sporadic example')
    for k in ['companion_socle_bound_established','historical_aggregate_reconstruction','historical_byte_identity','all_current_companion_tables_recovered','plural_large_sporadic_collection_recovered']:
        need(scope[k]is False,'unpaid companion and historical boundary')
    need(type(scope['whole_original_credit'])is int and scope['whole_original_credit']==0,'no self-issued whole credit')
    need(len(claims['clauses'])==21 and [c['id']for c in claims['clauses']]==[f'C{i:02}'for i in range(1,22)],'all original source clauses retained')
    need(claims['clauses'][17]['disposition']=='PROVED_BY_STRONGER_COMPLETE_CLASSIFIED_DOMAIN'and claims['clauses'][18]['disposition']=='QUANTIFIED_MATHEMATICAL_COVERAGE_RECONSTRUCTED_HISTORICAL_OUTPUTS_ATTRIBUTED','quantified reconstruction and historical attribution distinct')
    return counts

def run():
    scope=read(P/'scope.json');large=read(P/'large_applications.json');small=read(A/'small_order_domain_v1/target_join01.json');review=read(A/'article_main_results_scope_distinct_review/review.json');claims=read(P/'claim_register.json');sources={n:read(A/f/'native_assertions.json')['rows']for n,f in FOLDERS.items()}
    counts=join(scope,large,small,review,sources,claims);damages=[]
    def reject(name,ss=scope,ll=large,sm=small,rr=review,sr=sources,cc=claims):
        try:join(ss,ll,sm,rr,sr,cc)
        except (ValueError,KeyError,TypeError):damages.append(name)
        else:raise ValueError('damage accepted: '+name)
    ll=copy.deepcopy(large);ll.pop();reject('omitted_larger_application',ll=ll)
    ll=copy.deepcopy(large);ll[1]['structural_printed_labels_refuted_and_corrected']=0;reject('erased_A11_correction',ll=ll)
    sr=copy.deepcopy(sources);sr['alt11'][185]['tree']=['C',240];reject('replaced_printed_A11_AST',sr=sr)
    sr=copy.deepcopy(sources);sr['sp62'].pop();reject('omitted_source_row',sr=sr)
    sm=copy.deepcopy(small);sm['targets'][0]['structural_rows'].pop();reject('omitted_extra_structural_row',sm=sm)
    sm=copy.deepcopy(small);sm['targets'][-1]=copy.deepcopy(sm['targets'][0]);reject('duplicated_extra_table',sm=sm)
    rr=copy.deepcopy(review);rr['requires_all36_current_large_tables_from_article_alone']=True;reject('changed_source_contract',rr=rr)
    for k in ['companion_socle_bound_established','historical_aggregate_reconstruction','historical_byte_identity','all_current_companion_tables_recovered','plural_large_sporadic_collection_recovered','whole_original_credit']:
        ss=copy.deepcopy(scope);ss[k]=True;reject('invented_'+k,ss=ss)
    ss=copy.deepcopy(scope);ss['large_sporadic_examples']=['M23','ON'];reject('unpaid_sporadic_example',ss=ss)
    cc=copy.deepcopy(claims);cc['clauses'].pop();reject('removed_source_clause',cc=cc)
    return dict(status='PASS',**counts,source_clauses=21,damages=damages,whole_original_credit=0,new_censuses=0,prior_scientific_campaigns_replayed=0)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh audit output');r=run();a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
