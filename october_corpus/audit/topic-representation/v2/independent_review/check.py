#!/usr/bin/env python3
"""Bounded review-evidence verifier; this does not prove the written mathematics."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import local_cases

HERE = Path(__file__).resolve().parent
AUTHOR_SHA = 'e16d351e45b3b706757b8d16ba1f8e8e30974d387d5f60a3f9ea9fa8c7a44f7c'
SOURCE_SHA = 'a8ff604a96a57ab8baf20aaa808a90308c01237ab0607a1062207fcb49f736e7'
ORDER = ['Theorem3.1','Theorem4.1','Theorem4.2','TheoremA','Example5.1','Example5.2']
STANDARD = {'propext','Classical.choice','Quot.sound'}


def need(b, reason):
    if not b:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify(root, row):
    name=Path(row['path'])
    need(not name.is_absolute() and '..' not in name.parts, 'relative binding path')
    p=root/name
    need(p.is_file() and not p.is_symlink(), 'regular bound file: '+str(name))
    data=p.read_bytes()
    need(len(data)==row['bytes'] and digest(data)==row['sha256'], 'binding: '+str(name))


def semantics(review, scope, proof, formal, fresh, compiled):
    need(review['status']=='ACCEPTED_COMPLETE_WRITTEN_CONTRACT_WITH_SCOPED_FORMAL_EVIDENCE', 'acceptance status')
    need(review['author_manifest_sha256']==AUTHOR_SHA and review['source_sha256']==SOURCE_SHA, 'exact edition')
    need(scope['source_ids']==['F010'] and scope['source']['primary']['sha256']==SOURCE_SHA, 'source identity')
    need(scope['inherited_source_block_order']==ORDER, 'complete inherited order')
    need([r['id'] for r in scope['contracts']]==['F010.'+x for x in ORDER], 'six exact source blocks')
    need(proof['source_blocks']==scope['contracts'], 'independent six-row disposition')
    need({p['id'] for p in proof['proof_spans']}==set(scope['proof_spans']), 'all thirteen spans reviewed')
    for p in proof['proof_spans']:
        need(all(p[k]==v for k,v in scope['proof_spans'][p['id']].items()), 'exact proof context')
        need(len(p['independent_reasoning'])>150, 'substantive reading note')
    h=scope['precise_hypotheses']
    need(h['normal_subgroup_required'] is True and h['finite'] is True and h['rank_two_universal_claim'] is False, 'normal finite pair, not rank-two generalization')
    need(h['main_nontrivial_rank']=='[G:H]+3' and h['trivial_rank']==1 and h['connected_main_construction'] is True, 'actual rank and connectedness')
    need(h['arbitrary_input_cleaning_need_not_be_connected'] is True, 'components preserved, not invented connectedness')
    need(review['qualifications']==scope['source_qualifications'] and len(review['qualifications'])==3, 'three retained qualifications')
    need(any('(D12,S3)' in x for x in review['qualifications']), 'completed hexagon kernel')
    need(review['preserved_exclusions']==scope['exclusions'], 'source scope exclusions')
    need(review['new_source_credit']==scope['new_source_credit']==0 and review['new_question_credit']==scope['new_question_credit']==0 and review['compression_ratio'] is None, 'no new credit or ratio')
    need(review['coverage']=={'source_pages':13,'inherited_source_blocks':6,'written_spans':13,'whole_author_exports':46,'scientific_pages':10,'full_validation_appendix_pages':4,'whole_validation_programs':2,'required_finite_proof_programs':0,'archival_drivers':2,'new_generic_formal_declarations':8,'reused_local_formal_declarations':4,'end_to_end_source_Lean':False}, 'exact review scope')
    need('phase188' in review['review_roles']['inherited_contribution'] and 'phase193' in review['review_roles']['distinct_prior_acceptance'], 'inherited role disclosure')
    need(scope['validation_boundary']['uniform_written_proof_depends_on_finite_results'] is False, 'bounded computations not uniform proof')
    need([x['role'] for x in scope['program_inventory']]==['bounded_validation','bounded_validation','historical_operational_driver','historical_operational_driver'], 'whole program/driver roles')
    need(all(x['universal_proof_premise'] is False for x in scope['program_inventory']), 'no test-to-proof promotion')
    need(scope['cost_boundary']['prior_own_proof_bank_as_unpriced_logical_premise'] is False, 'no hidden old manuscript')
    need(formal['statement_map']==scope['formal_statement_map'], 'actual statement map')
    declarations=[x for m in formal['modules'] for x in m['declarations']]
    reports=[a for m in compiled['modules'] for a in m['axioms']]
    need([x['name'] for x in reports]==declarations and len(reports)==12, 'all twelve actual reports')
    need(all(set(x['axioms']) <= STANDARD for x in reports), 'standard axioms only')
    need(len(formal['new_generic_statement_review'])==8 and len(formal['not_formalized'])==6, 'generic/local formal boundary')
    need(formal['not_formalized']==compiled['not_formalized'], 'remaining written work')
    need(compiled['status']=='PASS' and '4.32.2' in compiled['lean_version'], 'fresh pinned Lean')
    need({x['name']:x['revision'] for x in compiled['dependencies']}['mathlib']=='905b95818eb32af7874a58b427f50c1711a5e96c', 'Mathlib revision')
    need(len(compiled['countermodels'])==4, 'all four hypothesis controls')
    need(fresh['status']=='PASS' and fresh['manifest_sha256']==AUTHOR_SHA, 'exact fresh runner')
    need(len(fresh['controls'])==11 and all(x['rejected'] for x in fresh['controls']), 'scope mutation controls')
    need(fresh['bounded_validation']['universal_proof'] is False and len(fresh['bounded_validation']['controls'])==3 and all(x['rejected'] for x in fresh['bounded_validation']['controls']), 'actual program mutations')
    need(fresh['formal']=={'reports':12,'generic_new':8,'local_reused':4,'countermodels':4,'end_to_end_source':False}, 'formal runner summary')
    need([(x['document'],x['pages']) for x in fresh['render']]==[('umbrella',5),('finite-normal-pairs',5),('program-appendix',4)], 'all fourteen own pages')
    need(all(x['per_page_text_identical'] and x['diagnostics']==[] for x in fresh['render']), 'clean text-identical render')


def audit(author, study=None, public=None):
    manifest=read(HERE/'manifest.json')
    for row in manifest['exports']: verify(HERE,row)
    bindings=read(HERE/'bindings.json')
    verify(author,bindings['author_manifest'])
    need(bindings['author_manifest']['sha256']==AUTHOR_SHA, 'frozen author')
    am=read(author/'manifest.json')
    need(bindings['author_exports']==am['exports'] and len(am['exports'])==46, 'complete exact author export set')
    for row in bindings['author_exports']: verify(author,row)
    for row in bindings['review_evidence']: verify(HERE,row)
    scope=read(author/'scope.json')
    for key,span in scope['proof_spans'].items():
        text=(author/span['path']).read_text();a=span['start_codepoint'];b=span['end_codepoint_exclusive']
        need(0<=a<b<=len(text) and digest(text[a:b].encode())==span['sha256_utf8'], 'exact span '+key)
    review=read(HERE/'review.json');proof=read(HERE/'proof_reading.json');formal=read(HERE/'formal_review.json')
    fresh=read(HERE/'fresh_replay/report.json');compiled=read(HERE/'fresh_replay/formal/report.json')
    semantics(review,scope,proof,formal,fresh,compiled)
    need(compiled['modules'][0]['source']['sha256']==formal['modules'][0]['sha256'] and compiled['modules'][1]['source']['sha256']==formal['modules'][1]['sha256'], 'fresh compiled source hashes')
    for item in compiled['modules']:
        name=item['source']['file'].removesuffix('.lean')
        log=(HERE/'fresh_replay/formal/logs'/(name+'.txt')).read_bytes()
        need(digest(log)==item['log_sha256'],'actual axiom stdout')
    external=[]
    if study:
        verify(study,bindings['primary']);verify(study,bindings['primary_text_reading_witness'])
        external+=['primary PDF','reading text']
    for row in bindings['prior_inputs']:
        base=study if row['namespace']=='study' else public
        if base:verify(base,row);external.append(row['path'])
    if public:
        prior=read(public/'research/case_study/phase193_F010_overlay.json')
        need(prior['status']=='ROOT_ADMITTED_COMPLETE_WRITTEN_PRINCIPAL_THEOREM_CONTRACT' and prior['id']=='F010' and prior['normal_subgroup_required'] is True, 'distinct prior root acceptance')
    local=local_cases.run();need(local==read(HERE/'local_cases.json'),'independent local finite checks')
    mutations=[('normality',1,lambda x:x['precise_hypotheses'].__setitem__('normal_subgroup_required',False)),
      ('rank-two promotion',1,lambda x:x['precise_hypotheses'].__setitem__('rank_two_universal_claim',True)),
      ('missing source row',1,lambda x:x['contracts'].pop()),
      ('sample-to-proof promotion',1,lambda x:x['validation_boundary'].__setitem__('uniform_written_proof_depends_on_finite_results',True)),
      ('full Lean promotion',0,lambda x:x['coverage'].__setitem__('end_to_end_source_Lean',True)),
      ('new question credit',0,lambda x:x.__setitem__('new_question_credit',1)),
      ('erase inherited role',0,lambda x:x['review_roles'].__setitem__('inherited_contribution','none')),
      ('nonstandard axiom',5,lambda x:x['modules'][0]['axioms'][0]['axioms'].append('sorryAx')),
      ('failed semantic mutation',4,lambda x:x['bounded_validation']['controls'][0].__setitem__('rejected',False)),
      ('incomplete render',4,lambda x:x['render'].pop())]
    controls=[]
    for name,index,change in mutations:
        args=copy.deepcopy([review,scope,proof,formal,fresh,compiled]);change(args[index])
        try:semantics(*args)
        except (ValueError,KeyError,IndexError) as error:controls.append({'name':name,'rejected':True,'reason':str(error)})
        else:raise ValueError('accepted corruption '+name)
    return {'status':'PASS','author_manifest_sha256':AUTHOR_SHA,'author_exports':46,'source_blocks':6,'proof_spans':13,'formal_reports':12,'rendered_pages':14,'external_bindings_checked':external,'review_metadata_controls':controls,'independent_small_cases':local,'written_proof_automatically_verified':False,'new_source_credit':0,'new_question_credit':0,'ratio':None}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--author-root',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--public-root',type=Path);p.add_argument('--out',type=Path);a=p.parse_args()
    result=audit(a.author_root,a.study_root,a.public_root);text=json.dumps(result,indent=2)+'\n'
    if a.out:
        need(not a.out.exists(),'fresh review report required');a.out.write_text(text)
    else:print(text,end='')
