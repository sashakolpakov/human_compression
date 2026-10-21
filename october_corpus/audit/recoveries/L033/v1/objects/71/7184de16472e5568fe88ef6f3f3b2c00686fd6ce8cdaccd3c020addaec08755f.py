import sys
if sys.flags.optimize: raise SystemExit('optimized execution unsupported')
import pathlib,json,hashlib,shutil,subprocess,datetime
S=pathlib.Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L033_method_distinct';A=S/'corpus106_L033_coxeter_lins_methods_v1';F=S/'corpus106_L033_coxeter_lins_methods_independent_review'
def pin(p):
 b=p.read_bytes();return {'path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(ok,msg):
 if not ok:raise ValueError(msg)
need(pin(A/'manifest.json')['sha256']=='4458a61aa5a7fa472ebe56195bcebb12755b72495ce81748971854b7945c38d1','author pin')
records=[]
def acquire(p):
 r=pin(p);records.append(r);return r
for packet in [A,S/'corpus106_L033_hyperbolic_core_v1',S/'corpus106_L033_hyperbolic_core_independent_review']:
 acquire(packet/'manifest.json');m=json.loads((packet/'manifest.json').read_text())
 for row in m['exports']:
  r=acquire(packet/row['path']);need(r['sha256']==row['sha256'] and r['bytes']==row['bytes'],'export changed')
for row in json.loads((A/'dependencies.json').read_text()):
 p=(S if row['namespace']=='study' else pathlib.Path('/'))/row['path'];r=acquire(p);need(r['sha256']==row['sha256']and r['bytes']==row['bytes'],'dependency changed')
for pdf in [A/'method.pdf',W/'fresh01/native/method.pdf']:
 r=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=txtwrite','-sOutputFile=-',str(pdf)],capture_output=True,check=True);need(not r.stderr,'gs stderr')
 (W/('frozen_native.txt' if pdf.parent==A else 'fresh_native.txt')).write_bytes(r.stdout)
need((W/'frozen_native.txt').read_bytes()==(W/'fresh_native.txt').read_bytes(),'native text')
r=json.loads((W/'fresh01/report.json').read_text());i=json.loads((W/'independent02/report.json').read_text());need(r['status']==i['status']=='PASS','reports')
review={'status':'ACCEPTED_L033_COXETER_LINS_METHODS','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author':'publication_recovery','reviewer':'f003_resume','author_manifest':pin(A/'manifest.json'),'prior_reviewer_contribution':'Retained LINS documentation/table-boundary read only; no new method proof or code authorship.','full_proof_code_and_primary_interfaces_read':True,'native_pages_directly_viewed':2,'native_text_identity':True,'fresh_replay':pin(W/'fresh01/report.json'),'fresh_session':57335,'independent_seed_control':pin(W/'independent02/report.json'),'independent_session':58840,'literal_surjections':sum(x['literal_surjections']for x in i['cases']),'inner_orbits':sum(x['inner_orbits']for x in i['cases']),'acquired_record_occurrences':len(records),'acquired_unique_files':len({x['path']for x in records}),'target_census_credit':0,'whole_original_credit':0,'new_question_credit':0,'new_lean_credit':0,'new_measurement_credit':0,'owned_review_processes':[]}
(W/'review.json').write_text(json.dumps(review,indent=2)+'\n');(W/'dependencies.json').write_text(json.dumps(records,indent=2)+'\n');need(not F.exists(),'immutable destination exists');F.mkdir()
for name in ['review.rst','review.json','dependencies.json','independent_seed.py','independent_seed_v2.py','reviewer_control_correction.rst','frozen_native.txt','fresh_native.txt','freeze.py']:
 shutil.copy2(W/name,F/name)
for name in ['fresh01','independent01','independent02']:shutil.copytree(W/name,F/name)
exports=[]
for p in sorted(F.rglob('*')):
 if p.is_file():r=pin(p);r['path']=str(p.relative_to(F));exports.append(r)
(F/'manifest.json').write_text(json.dumps({'status':review['status'],'author_manifest':review['author_manifest'],'exports':exports,'target_census_credit':0,'whole_original_credit':0},indent=2)+'\n');print(json.dumps(pin(F/'manifest.json')));print(json.dumps(review))
