"""Check the separate F003 principal-refutation transition and publication."""
from pathlib import Path
import argparse
import ast
import copy
import hashlib
import json

AUD='audit/principal-refutations/F003/v1'
BASE='corrections/suzuki-rank/v1'
WRAPPER='abdef1dcb1de90f4047cf52b812590d29a3ec1056511af201c5f6ab3f3fcdad2'
REVIEW='7af3efbad1e8bde17d52c440c83e91eee1276d539b595c593a7cf6e5b1a09bbc'

def need(ok,message):
    if not ok:
        raise ValueError(message)

def load(root,name):
    return json.loads((root/name).read_text())

def bind(root,row):
    name=Path(row['path']);p=root/name
    need(not name.is_absolute() and '..' not in name.parts and
         p.resolve().is_relative_to(root.resolve()),'binding escapes public repository')
    data=p.read_bytes()
    need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],
         'binding changed: '+str(name))

def semantics(current,old,admission):
    changes={'status','accessible_pending_complete_recovery','accessible_pending_original_ids',
             'previous_snapshot','active_catalogue','current_scope','snapshot'}
    for key in set(old)-changes:
        need(current[key]==old[key],'unrelated current field changed: '+key)
    additions={'refuted_principal_originals','refuted_principal_original_ids',
               'handled_mathematical_originals','handled_mathematical_original_ids',
               'all_mathematical_originals_handled','principal_refutation_admissions',
               'current_principal_disposition_registration'}
    need(set(current)-set(old)==additions,'exact new disposition fields')
    recovered=current['admitted_original_ids'];refuted=current['refuted_principal_original_ids']
    pending=current['accessible_pending_original_ids'];editorial=current['editorial_original_ids']
    for ids in (recovered,refuted,pending,editorial):
        need(len(ids)==len(set(ids)),'duplicate original')
    need(recovered==old['admitted_original_ids'] and len(recovered)==72,'recoveries unchanged')
    need(refuted==['F003'] and current['refuted_principal_originals']==1,'one exact refutation')
    need(pending==[x for x in old['accessible_pending_original_ids'] if x!='F003'] and
         len(pending)==current['accessible_pending_complete_recovery']==32,'only F003 leaves pending')
    sets=[set(x) for x in (recovered,refuted,pending,editorial)]
    need(all(not a&b for i,a in enumerate(sets) for b in sets[i+1:]),'disjoint original dispositions')
    need(set.union(*sets)==set(current['active_original_ids']) and
         sum(map(len,sets))==current['originals']==106,'exhaustive 106-original partition')
    need(current['handled_mathematical_original_ids']==sorted(recovered+refuted) and
         current['handled_mathematical_originals']==73 and 72+1+32==105,'73 handled mathematical originals')
    need(not current['all_mathematical_originals_handled'] and not current['all_original_proofs_recovered']
         and not current['all_conjectures_resolved'],'incomplete programme remains explicit')
    need(admission['source_ids']==['F003'] and admission['disposition_kind']=='principal_statement_refuted',
         'separate refutation classification')
    need(admission['source_edition']=='arXiv:2010.04080v1, 8 October 2020' and
         admission['target']=='Theorem 1.1','exact fixed-edition target')
    need(admission['accepted_counterexample']==dict(group='Sz(32768)',rank=4,type=[31,31,25]),
         'exact counterexample')
    need(admission['principal_refutation_credit']==1,'one refuted principal statement')
    for key in ('ordinary_recovery_credit','measurement_credit','new_question_credit','new_Lean_credit'):
        need(admission[key]==0,'unearned credit: '+key)
    for key in ('whole_source_formalized','root_is_distinct_reviewer','later_edition_claim',
                'historical_priority_claim','absence_of_errata_claim','journal_fulltext_claim'):
        need(admission[key] is False,'unsupported scope: '+key)
    need(admission['compression_factor'] is admission['software_inclusive_factor'] is None,
         'refutation has no compression factor')

def verify(root,require_root=True):
    root=Path(root).resolve()
    routes=load(root,AUD+'/history_routes.json')['routes']
    need(set(routes)=={'README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf',
                      'audit/corpus/latest.json','papers/latest_catalogue.json','scripts/verify_snapshot.py'},
         'seven archived mutable paths')
    for row in routes.values():bind(root,row)
    old=load(root,routes['audit/corpus/latest.json']['path'])
    current=load(root,'audit/corpus/latest.json');admission=load(root,BASE+'/admission.json')
    semantics(current,old,admission)
    for key in ('active_catalogue','snapshot','current_science_registration','current_principal_disposition_registration'):
        bind(root,current[key])
    need(current['previous_snapshot']==routes['audit/corpus/latest.json'],'exact predecessor')
    need(load(root,current['snapshot']['path'])=={k:v for k,v in current.items() if k!='snapshot'},
         'exact immutable current snapshot')
    cat=load(root,current['active_catalogue']['path']);oldcat=load(root,old['active_catalogue']['path'])
    changed_cat={'entries','status','accessible_pending_complete_recovery','review_revision','new_proof_credit',
                 'previous_catalogue','current_recovery_counts'}
    for key in set(oldcat)-changed_cat:
        need(cat[key]==oldcat[key],'unrelated catalogue metadata changed: '+key)
    need(len(cat['entries'])==len(oldcat['entries'])==106,'fixed catalogue size')
    proposal=load(root,BASE+'/catalogue_disposition_proposal.json')
    for before,after in zip(oldcat['entries'],cat['entries']):
        if before['original_id']!='F003':
            need(before==after,'another original changed')
        else:
            expected=copy.deepcopy(before);expected.update(proposal['proposed_row'])
            need(after==expected,'exact reviewed F003 row')
            need(after['current_principal_recovery']['historical_admission_evidence']==before['current_principal_recovery'],
                 'complete old F003 record retained')
    need(cat['current_recovery_counts']==dict(active=106,admitted=72,refuted=1,handled=73,
         measured=53,measurement_pending=19,pending=32,editorial=1),'catalogue count agreement')
    need(cat['refuted_principal_original_ids']==['F003'] and cat['handled_mathematical_original_ids']==
         current['handled_mathematical_original_ids'],'catalogue handled sets')
    need(cat['refuted_principal_originals']==1 and cat['handled_mathematical_originals']==73 and
         cat['new_proof_credit']==0 and cat['new_principal_refutation_credit']==1,
         'catalogue credit remains separate')
    reg=load(root,current['current_principal_disposition_registration']['path'])
    need(reg['source_ids']==['F003'] and reg['principal_refutations_added']==1 and
         reg['ordinary_recoveries_added']==reg['new_measurements']==reg['new_question_credit']==reg['new_Lean_credit']==0,
         'registration credit boundary')
    need(reg['mathematical_originals_handled_added']==1 and reg['compression_factor'] is None,
         'one terminal refutation without a factor')
    need(reg['previous_science_registration']==old['current_science_registration'] and
         reg['previous_corpus']==routes['audit/corpus/latest.json'],'unchanged prior science registration')
    bind(root,reg['admission'])
    need(current['principal_refutation_admissions']==[current['current_principal_disposition_registration']],
         'one registered refutation')
    for key in ('source','scientific_author','distinct_mathematical_review','distinct_v2_addendum',
                'root_scientific_adoption','portable_wrapper','distinct_portable_review'):
        bind(root,admission[key])
    need(admission['portable_wrapper']['sha256']==WRAPPER and
         admission['distinct_portable_review']['sha256']==REVIEW,'reviewed frozen wrapper')
    for directory in (BASE,AUD+'/portable_review'):
        for row in load(root,directory+'/manifest.json')['exports']:
            bind(root,dict(row,path=directory+'/'+row['path']))
    need(len(load(root,BASE+'/manifest.json')['exports'])==115,'all115 exact wrapper exports')
    for row in load(root,BASE+'/transport.json')['files']:
        if row['transport']=='EXISTING_PUBLIC':
            bind(root,dict(row,path=row['public_path']))
    manuscript=admission['complete_manuscript']
    bind(root,manuscript['tex']);bind(root,manuscript['pdf'])
    need(manuscript['physical_pages']==5,'complete five-page written proof')
    replay=load(root,AUD+'/reports/portable.json')
    need(replay['status']=='PASS_PUBLIC_CORRECTION_REPLAY' and replay['independent_GAP'] and
         replay['face_orders']==[32537600,32537600] and replay['source_equation13_residual']==28331 and
         replay['logical_bindings']==116 and replay['complete_packets']==7 and
         replay['v2_nonprimary_bindings']==39 and not replay['private_mathematical_proof_fallback'] and
         not replay['private_source_files_read'] and not replay['catalogue_modified'],
         'completed public Python and independent GAP replay')
    papers=load(root,'papers/latest_catalogue.json')
    oldpapers=load(root,routes['papers/latest_catalogue.json']['path'])
    for key in set(oldpapers)-{'status','active_source_catalogue'}:
        need(papers[key]==oldpapers[key],'old paper catalogue changed')
    need(set(papers)-set(oldpapers)=={'principal_refutation_catalogue'},'one separate paper catalogue')
    need(papers['active_source_catalogue']==current['active_catalogue'],'paper source catalogue')
    bind(root,papers['corrected_unmeasured_scientific_catalogue'])
    bind(root,papers['principal_refutation_catalogue'])
    native=load(root,papers['principal_refutation_catalogue']['path'])
    need(native['original_ids']==['F003'] and len(native['entries'])==1 and
         native['ordinary_recovery_credit']==native['new_measurements']==native['new_question_credit']==0,
         'separate native refutation catalogue')
    entry=native['entries'][0]
    need(entry['role']=='principal_statement_refutation' and not entry['measured'] and
         entry['compression_factor'] is None and entry['source_ids']==['F003'] and entry['physical_pages']==5,
         'native correction scope')
    oldtree=ast.parse((root/routes['scripts/verify_snapshot.py']['path']).read_text())
    newtree=ast.parse((root/'scripts/verify_snapshot.py').read_text())
    additions={'check_previous_F003_disposition','check_F003_disposition'}
    def nodes(tree,excluded):
        return [ast.dump(n,include_attributes=False) for n in tree.body
                if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in excluded)]
    need(nodes(oldtree,{'main'})==nodes(newtree,{'main'}|additions),
         'all old verifier functions and other top-level nodes preserved')
    newnames={n.name for n in newtree.body if isinstance(n,ast.FunctionDef)}
    oldnames={n.name for n in oldtree.body if isinstance(n,ast.FunctionDef)}
    need(newnames-oldnames==additions,'only two verifier functions added')
    controls=[]
    cases=[('duplicate refutation',lambda c,a:c['refuted_principal_original_ids'].append('F003')),
           ('false recovery',lambda c,a:c['admitted_original_ids'].append('F003')),
           ('pending overlap',lambda c,a:c['accessible_pending_original_ids'].append('F003')),
           ('extra removal',lambda c,a:c['accessible_pending_original_ids'].pop()),
           ('changed measurement',lambda c,a:c['measured_original_ids'].pop()),
           ('unearned completion',lambda c,a:c.update(all_mathematical_originals_handled=True)),
           ('wrong source',lambda c,a:a.update(source_edition='journal text')),
           ('ordinary credit',lambda c,a:a.update(ordinary_recovery_credit=1)),
           ('question credit',lambda c,a:a.update(new_question_credit=1)),
           ('formal credit',lambda c,a:a.update(whole_source_formalized=True)),
           ('factor',lambda c,a:a.update(compression_factor=2)),
           ('self review',lambda c,a:a.update(root_is_distinct_reviewer=True))]
    for label,edit in cases:
        c,a=copy.deepcopy((current,admission));edit(c,a)
        try:semantics(c,old,a)
        except (ValueError,KeyError):controls.append(label)
        else:raise ValueError('invalid disposition accepted: '+label)
    if require_root:
        gate=load(root,AUD+'/root_integration.json')
        need(gate['status']=='ROOT_ACCEPTED_F003_PRINCIPAL_REFUTATION_PUBLICATION' and
             gate['source_ids']==['F003'] and gate['principal_refutation_credit']==1 and
             gate['ordinary_recovery_credit']==0,'final root acceptance')
        for row in gate['bindings']:bind(root,row)
        review=load(root,AUD+'/registration_review/review.json')
        need(review['status']=='ACCEPTED_SEPARATE_F003_REGISTRATION','distinct transition acceptance')
    return dict(status='PASS_SEPARATE_F003_PRINCIPAL_REFUTATION',source_ids=['F003'],
        counts=dict(active=106,corrected_recoveries=72,refuted=1,handled=73,
                    measured=53,unmeasured=19,mathematical_pending=32,editorial=1,archived=55),
        controls=controls,old_verifier_functions_preserved=len(oldnames)-1)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--preflight',action='store_true');a=parser.parse_args()
    print(json.dumps(verify(a.repo,require_root=not a.preflight)))
