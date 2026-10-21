from pathlib import Path
import re
S=Path('/Users/sasha/medusa/research/leemans');R=S.parents[1]/'math_compression';T=S/'reboot_20261013/L038_publication_work/stage01'
s=(R/'scripts/check_science72.py').read_text().replace('L071','L038').replace('science72','science73').replace('SCIENCE72','SCIENCE73')
a=s.index('def semantics(');b=s.index('\n\ndef verify(',a)
s=s[:a]+'''def semantics(current, old, admission, scope):
    need(set(current['admitted_original_ids']) == set(old['admitted_original_ids']) | {'L038'}, 'only L038 added')
    need(len(current['admitted_original_ids']) == current['admitted_principal_originals'] == 73, '73 unique recoveries')
    need(set(current['accessible_pending_original_ids']) == set(old['accessible_pending_original_ids']) - {'L038'} and len(current['accessible_pending_original_ids']) == current['accessible_pending_complete_recovery'] == 31, 'only L038 removed from pending')
    need(set(current['handled_mathematical_original_ids']) == set(old['handled_mathematical_original_ids']) | {'L038'} and len(current['handled_mathematical_original_ids']) == current['handled_mathematical_originals'] == 74, '74 handled originals')
    for key in ('measurement_pending_original_ids','scientific_unmeasured_original_ids'):
        need(set(current[key]) == set(old[key]) | {'L038'} and len(current[key]) == 20, 'twenty unmeasured originals')
    for key in ('active_original_ids','archived_original_ids','measured_original_ids','added_measurements','current_topic_replacements','editorial_original_ids','refuted_principal_originals','refuted_principal_original_ids','principal_refutation_admissions','all_mathematical_originals_handled'):
        need(current[key] == old[key], 'unchanged scope, refutation or measurement: '+key)
    need(current['currently_measured_originals']==53 and current['originals']==106 and current['editorial_originals']==1, 'fixed corpus')
    need(admission['source_ids']==['L038'] and admission['principal_originals_added']==1 and admission['whole_original_credit']==0, 'one proposed recovery; final credit requires root gate')
    need(admission['literal_principal_theorem_recovered'] and admission['complete_principal_existence_recovered'] and not admission['all_original_assertions_claimed'], 'principal and auxiliary scopes distinct')
    need(set(admission['component_acceptance'])=={'low_rank','signed_ends','principal'} and all(set(c)=={'author','distinct_review','root_adoption'}for c in admission['component_acceptance'].values()), 'complete review chains')
    need(len(scope['routes'])==14 and len({r['source_claim']for r in scope['routes']})==14, 'fourteen source routes')
    need(admission['finite_subset_pairs']==3200 and admission['physical_pages']==17 and len(admission['retained_inputs'])==5, 'complete stated evidence')
    need(admission['compression_factor'] is admission['software_inclusive_factor'] is None and admission['new_question_credit']==admission['new_Lean_declarations']==admission['new_measurements']==0 and not admission['whole_source_formalized'] and not admission['measured'], 'no new factor or formal claim')
''' +s[b:]
s=s.replace("    for row in ad['complete_acquired_proofs'].values():\n        bind(root,row)\n", "    for key in ['scope_addendum','source_routes','portable_report','portable_checker','portable_review']:\n        bind(root,ad[key])\n    for row in load(root,ad['portable_review']['path'])['bindings'].values():\n        bind(root,row)\n")
s=s.replace("t['logical_files'] == 1057", "t['logical_files'] == 713").replace('len(unique) == 688','len(unique) == 485')
a=s.index("    need(replay['status']");b=s.index("    previous = load(",a)
s=s[:a]+'''    need(replay['status']=='PASS_PUBLIC_L038_RESTORATION_AND_FINITE_PREMISES' and replay['transport_sha256']==ad['portable_transport']['sha256'] and not replay['private_proof_fallback'] and not replay['source_content_reread'] and replay['subset_pairs']==3200 and [c['component']for c in replay['checks']]==['low_rank','signed_ends','principal'], 'complete portable finite replay')
''' +s[b:]
s=s.replace("native['entries'][:-5]", "native['entries'][:-3]").replace("native['entries'][-5:]", "native['entries'][-3:]").replace('== [2,2,2,3,2]', '== [7,7,3]').replace('five complete application documents','three complete application documents')
s=s.replace("('literal equivalence',lambda c,a,s:a.update(literal_theorem_sets_equivalent=True))", "('auxiliary overclaim',lambda c,a,s:a.update(all_original_assertions_claimed=True))").replace("['Co3'].pop('distinct_review')", "['signed_ends'].pop('distinct_review')")
s=s.replace("        for row in gate['bindings']:\n            bind(root,row)", "        for row in gate['bindings']:\n            bind(root,row)\n        need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_L038_REGISTRATION','distinct registration review')")
s=s.replace('corrected_recoveries=72,measured=53,unmeasured=19,mathematical_pending=33,','corrected_recoveries=73,refuted=1,handled=74,measured=53,unmeasured=20,mathematical_pending=31,')
(T/'scripts/check_science73.py').write_text(s)
s=(R/'scripts/check_F003_history.py').read_text().replace("AUD='audit/principal-refutations/F003/v1'", "AUD='audit/science73/v1'").replace("module.check_previous_science72()", "module.check_previous_F003_disposition()").replace("science72=module.check_science72()", "science72=module.check_F003_disposition()").replace("['mathematical_pending']!=33", "['mathematical_pending']!=32").replace('PASS_EXACT_HISTORICAL_SCIENCE72','PASS_EXACT_HISTORICAL_F003_DISPOSITION')
(T/'scripts/check_science73_history.py').write_text(s)
print('Prepared two science73 guards; previous verifier functions remain unchanged.')
