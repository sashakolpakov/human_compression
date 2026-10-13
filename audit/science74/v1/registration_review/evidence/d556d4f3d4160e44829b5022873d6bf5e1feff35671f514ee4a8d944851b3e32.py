from pathlib import Path
import ast
S=Path('/Users/sasha/medusa/research/leemans');R=S.parents[1]/'math_compression';T=S/'reboot_20261013/F006_publication_work/stage01'
s=(R/'scripts/check_science73.py').read_text().replace('L038','F006').replace('science73','science74').replace('SCIENCE73','SCIENCE74')
s=s.replace('== 73','== 74').replace('73 unique','74 unique').replace('== 31','== 30').replace('== 74, \'74 handled','== 75, \'75 handled').replace('== 20','== 21').replace('twenty unmeasured','twenty-one unmeasured')
s=s.replace("need(admission['literal_principal_theorem_recovered'] and admission['complete_principal_existence_recovered'] and not admission['all_original_assertions_claimed'], 'principal and auxiliary scopes distinct')", "need(not admission['literal_principal_theorem_recovered'] and admission['complete_principal_contract_recovered'] and not admission['all_original_assertions_claimed'], 'corrected principal scope')\n    need(admission['corrected_literal_cases']==['I2(m), m=2 modulo4','H3','E7'] and admission['strict_warning_receipts_preserved'], 'exact disconnected corrections and warning boundary')")
s=s.replace("{'low_rank','signed_ends','principal'}", "{'complete'}").replace("len(scope['routes'])==14 and len({r['source_claim']for r in scope['routes']})==14, 'fourteen source routes'", "len(scope['rows'])==24 and len({r['id']for r in scope['rows']})==24, 'twenty-four source routes'")
s=s.replace("admission['finite_subset_pairs']==3200 and admission['physical_pages']==17", "admission['finite_subset_pairs']==14050496 and admission['physical_pages']==21 and admission['exceptional_ordered_tuples']==32603 and admission['printed_source_cells']==42")
s=s.replace("['scope_addendum','source_routes','portable_report','portable_checker','portable_review']", "['dependency_locator_correction','source_routes','portable_report','portable_checker','portable_review']")
s=s.replace("    for entry in ad['new_native_manuscripts']:", "    for row in ad['complete_acquired_proofs'].values():\n        bind(root,row)\n    for entry in ad['new_native_manuscripts']:")
s=s.replace("t['logical_files'] == 713 and len(t['packets']) == 21", "t['logical_files'] == 476 and len(t['packets']) == 8").replace('len(unique) == 485','len(unique) == 412')
a=s.index("    need(replay['status']");b=s.index('    previous = load(',a)
s=s[:a]+'''    need(replay['status']=='PASS_PUBLIC_F006_RESTORATION_AND_RECEIPTS' and replay['transport_sha256']==ad['portable_transport']['sha256'] and not replay['private_proof_fallback'] and not replay['source_content_reread'] and replay['original_warning_receipts_unchanged'] and replay['author_evidence']['exceptional_ordered_tuples']==32603 and replay['author_evidence']['printed_cells']==42 and len(replay['warning_controls'])==13, 'complete portable evidence replay')
''' +s[b:]
s=s.replace("native['entries'][:-3]", "native['entries'][:-9]").replace("native['entries'][-3:]", "native['entries'][-9:]").replace('== [7,7,3]', '== [2,3,3,3,2,2,1,3,2]').replace('three complete application documents','nine complete immediate proof documents')
s=s.replace("s['routes'].pop()", "s['rows'].pop()").replace("['signed_ends'].pop('distinct_review')", "['complete'].pop('distinct_review')")
s=s.replace('corrected_recoveries=73,refuted=1,handled=74,measured=53,unmeasured=20,mathematical_pending=31','corrected_recoveries=74,refuted=1,handled=75,measured=53,unmeasured=21,mathematical_pending=30')
ast.parse(s);(T/'scripts').mkdir(exist_ok=True);(T/'scripts/check_science74.py').write_text(s)
s=(R/'scripts/check_science73_history.py').read_text().replace("AUD='audit/science73/v1'", "AUD='audit/science74/v1'").replace('module.check_previous_F003_disposition()', 'module.check_previous_science73()').replace('module.check_F003_disposition()', 'module.check_science73()').replace("['corrected_recoveries']!=72", "['corrected_recoveries']!=73").replace("['mathematical_pending']!=32", "['mathematical_pending']!=31").replace('PASS_EXACT_HISTORICAL_F003_DISPOSITION','PASS_EXACT_HISTORICAL_SCIENCE73')
ast.parse(s);(T/'scripts/check_science74_history.py').write_text(s)
print('F006 publication guards prepared.')
