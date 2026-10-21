from pathlib import Path
import datetime,hashlib,json,shutil
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L059_principal_distinct'
P=S/'corpus106_L059_principal_v2';V=S/'corpus106_L059_principal_v1'
R=S/'corpus106_L059_principal_independent_review'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):(R/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def pin(p,role):return {'path':str(p.relative_to(S)),'bytes':p.stat().st_size,'sha256':sha(p),'role':role}
need(not R.exists(),'immutable destination already exists')
need(sha(P/'manifest.json')=='7bd69a403767f78a4b4702aa7b110b8eabf6d8d128c9cf4c31141f9b389d21d9','author edition')
closure=json.loads((W/'closure_report.json').read_text());need(closure['status']=='PASS_DISTINCT_CLOSURE','closure')
control=json.loads((W/'method_controls_v3_receipt.json').read_text());need(control['passed'],'controls')
edition=json.loads((W/'edition_audit.json').read_text());need(edition['status']=='PASS_EXACT_METADATA_ONLY_V2','edition')
report=json.loads((W/'replay02/report.json').read_text());need(report['status']=='PASS_PRINCIPAL_CERTIFICATE_INTEGRITY_AND_39_TABLE_CELLS','final replay')
R.mkdir()
text=(W/'review_draft.rst').read_text()
text=text.replace('The complete mathematical and computational recovery is acceptable with the\nstated corrections and retained classification premises. This recommendation\nis conditional only on the final immutable edition acquiring the five actual\ncomparison inputs identified in the execution-closure audit. The first author\nedition remains unchanged. This draft is not the frozen acceptance record.',
'The complete mathematical and computational recovery in author edition v2\nis accepted with the stated corrections and retained classification premises.\nIts manifest SHA256 is 7bd69a403767f78a4b4702aa7b110b8eabf6d8d128c9cf4c31141f9b389d21d9.\nThe first author edition remains unchanged. The only old exported bytes changed\nare dependencies.json and author_report.json; the new edition delta records\nthe acquisition of five actual comparison inputs and five completion tokens.\nAll mathematical text, PDFs, programs, census rows and original runs are unchanged.')
text=text.replace('The final edition must acquire their\nexact bytes; the first edition and the omission report are preserved.', 'Edition v2 acquires their exact\nbytes and five completion tokens; the first edition and omission report are\npreserved. The independent final closure audit passes all 10,406 dependencies,\n1888 actual worker files, 723 nested Read targets, 344 exact automorphism-oracle\npins and six retry-library pins. All 261 renamed CAT/VT3 receipts are checked\nagainst the separately replayed explicit graph isomorphisms.')
(R/'review.rst').write_text(text)
decision={'status':'ACCEPTED_COMPLETE_CORRECTED_L059_PRINCIPAL_RECOVERY','original':'L059','author_manifest_sha256':sha(P/'manifest.json'),'mathematical_acceptance':True,'principal_recovery_recommended':True,'recommended_whole_original_credit_after_root_gate':1,'publication_admission':False,'whole_original_credit':0,'new_question_credit':0,'new_formal_declarations':0,'measurement_credit':0,'contract':'Complete principal faithful-action and finite-family recovery, including 2014 subdivisions, with all eight explicit source qualifications and acquired external catalogue/library premises.','counts':{'graph_inputs':1950,'faithful_markings':4254,'printed_cells':39},'open_questions':'Neither the large-stabilizer classification nor the arXiv cyclic-configuration problem is claimed solved.','reviewer':'/root/publication_recovery','author':'/root/l044_resume','roles':'Distinct full principal review; no authorship of L059 mathematics. Root scope/interface contributions and root distinct reviews of the two bounded components remain disclosed. Reviewer requested only execution-closure metadata acquisition.','native_pages_directly_viewed':list(range(1,11)),'source_physical_pages_directly_viewed':[9,10],'full_census_repeated':False,'owned_live_handles':[]}
write('review.json',decision)
write('report.json',{'status':'PASS_DISTINCT_PRINCIPAL_REVIEW','closure':closure,'finite_control':control,'fresh_principal_replay':report,'edition_delta':edition,'fresh_bounded_primary_inputs':839,'explicit_reuse_isomorphisms':261,'fresh_named_group_and_Mathieu_replay':True,'scope_controls':8,'optimization_controls':2,'damaged_orbit_list_controls':10,'failed_reviewer_drafts':'Two failed GAP harness drafts are retained, not used as evidence; the immutable author programs never changed.','terminal_sessions':[95001,11816,77474,43991,46911,62810,79656,3812,55996,7475]})
write('native_review.json',{'pages':10,'directly_viewed':list(range(1,11)),'source_directly_viewed':[9,10],'all_page_text_identical_to_author':True,'overflow':False,'benign_underfull_warnings':1,'new_builds':2,'new_math_edition':False})
for name in ['audit_closure.py','closure_report.json','edition_audit.json','method_controls_v3.g','method_controls_v3.stdout','method_controls_v3.stderr','method_controls_v3_receipt.json','missing_closure.json']:
 shutil.copy2(W/name,R/name)
deps={}
def add(p,role):
 p=p.resolve();need(p.exists(),'missing '+str(p));q=pin(p,role)
 if str(p) in deps:
  need(deps[str(p)]['sha256']==q['sha256'],'changed pin')
 else:deps[str(p)]=q
for x in json.loads((P/'dependencies.json').read_text()):add(Path(x['path']),'acquired exact principal execution/source dependency')
for package in [P,V]:
 add(package/'manifest.json','immutable author edition')
 for x in json.loads((package/'manifest.json').read_text())['exports']:add(package/x['path'],'complete author export')
for p in W.rglob('*'):
 if p.is_file() and p.name!='review_draft.rst':add(p,'distinct review evidence; diagnostic failures remain historical')
write('dependencies.json',sorted(deps.values(),key=lambda x:x['path']))
exports=[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(R.iterdir()) if p.is_file()]
write('manifest.json',{'status':decision['status'],'exports':exports,'whole_original_credit':0,'new_question_credit':0,'new_formal_declarations':0,'measurements':None})
print(json.dumps({'review_manifest':str(R/'manifest.json'),'sha256':sha(R/'manifest.json'),'exports':len(exports),'bindings':len(deps),'status':decision['status']}))
