#!/usr/bin/env python3
"""Bounded publication integration checks; accepted mathematics/counts are reused."""
import argparse, ast, copy, hashlib, importlib.util, json, re, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
M='audit/topic-representation/v2/measurement/'
PRIVATE={'inputs':'topic_Representation_measurement_inputs','input_review':'topic_Representation_measurement_input_review','input_adoption':'topic_Representation_measurement_input_root_adoption','packet':'topic_Representation_measurement_results','arithmetic_review':'topic_Representation_measurement_independent_review','root_adoption':'topic_Representation_measurement_root_adoption'}
PINS={
 'inputs':'122820fac69c94d484444a88b4318fa7ae1a588770c4378737af7d457a037af1',
 'input_review':'d9b130046c95f625946762a4414fc294d2366e5bed3803aae783bb43967b69f3',
 'input_adoption':'c6cd89907ac02b7384fb887e93e3d4f941dcab2f963cc9156341cbeb5b2a24c5',
 'packet':'8a0c2a30ac88b0d703b5082ce8a2426d8da82f27dea94558f0005a5b29d76c03',
 'arithmetic_review':'20c787b813181a6775337c6e64d356f14bc739baf5abdc62240967f16d508d70',
 'root_adoption':'cd29438dea67ad8258b1905a5f568a7f3f228b9c57e39d1cc232758fac06d1a0'}
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def read(root,path):return json.loads((root/path).read_text())
def relative(path):
 p=Path(path);need(not p.is_absolute() and '..' not in p.parts,'unsafe path');return p
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def funcs(text):return {f.name:f for f in ast.parse(text).body if isinstance(f,ast.FunctionDef)}
def calls(f):return [n.func.id for n in ast.walk(f) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id.startswith('check_')]
def archive_copies(root,study):
 records=[]
 for folder,pin in PINS.items():
  base=root/M/folder;raw=(base/'manifest.json').read_bytes();need(sha(raw)==pin,'packet pin '+folder);mf=json.loads(raw)
  for row in mf['exports']:
   path=relative(row['path']);need(path.suffix!='.md','working Markdown exported');b=(base/path).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'frozen export '+str(path))
  if study:
   private=study/PRIVATE[folder]
   for path in [x['path'] for x in mf['exports']]+['manifest.json']:need((private/path).read_bytes()==(base/path).read_bytes(),'private/public equality '+folder+'/'+path)
  records.append(dict(folder=folder,exports=len(mf['exports']),manifest_sha256=pin,private_equality=bool(study)))
 need(sum(r['exports']+1 for r in records)==66,'complete copied packet closure')
 return records

def mapping_check(root):
 policy=read(root,M+'inputs/policy.json');spec=read(root,M+'inputs/replacement_input_spec.json')
 prefixes={'topic_Representation_volume/':'papers/topic-representation/v2/','topic_Representation_independent_review/':'audit/topic-representation/v2/independent_review/','topic_Representation_review_role_delta/':'audit/topic-representation/v2/review_role_delta/','topic_Representation_root_adoption/':'audit/topic-representation/v2/root_adoption/'}
 rows=list(policy['replacement_roster'].values())
 for k in ['complete_validation_programs','complete_operational_drivers','complete_formal_files']: rows+=spec[k]
 rows += [policy[k] for k in ['author','independent_review','role_delta','root_adoption','accepted_scope']]
 rows += [spec['appendix_tex']]
 formal=root/'papers/topic-representation/v2/formal/scope.json'
 rows += [dict(path='topic_Representation_volume/formal/scope.json',bytes=formal.stat().st_size,sha256=sha(formal.read_bytes()))]
 expected=[]
 for row in rows:
  paths=[new+row['path'][len(old):] for old,new in prefixes.items() if row['path'].startswith(old)]
  need(len(paths)==1,'unique public route')
  expected.append(dict(private_path=row['path'],public_path=paths[0],bytes=row['bytes'],sha256=row['sha256']))
 for key,row in policy['source_roster'].items(): expected.append(dict(private_path=row['path'],public_path=None,source_id=key,bytes=row['bytes'],sha256=row['sha256']))
 actual=read(root,M+'recount_mapping.json')
 need(actual['routes']==expected and actual['primary_exported'] is False,'exact complete recount mapping')
 need(len(expected)==len({r['private_path'] for r in expected})==17,'unique17 inputs')
 for row in expected:
  if row['public_path'] is not None:
   b=(root/relative(row['public_path'])).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'public science input '+row['public_path'])
 need(sum(r['public_path'] is not None for r in expected)==16,'sixteen public inputs')
 return expected

def old_checks(root,base):
 oldtext=subprocess.check_output(['git','show',base+':scripts/verify_snapshot.py'],cwd=root,text=True)
 newtext=(root/'scripts/verify_snapshot.py').read_text();old,new=funcs(oldtext),funcs(newtext)
 need(all(ast.dump(f,include_attributes=False)==ast.dump(new[k],include_attributes=False) for k,f in old.items() if k!='main'),'old checker function changed')
 need(set(new)-set(old)=={'check_representation_measurement'},'exactly one new check')
 need([x for x in calls(new['main']) if x!='check_representation_measurement']==calls(old['main']) and calls(new['main']).count('check_representation_measurement')==1,'prior check dispatch order')
 return len(old)-1

# Exact candidate checks below remain replayable before and after publication.
# Later review/adoption files are allowed only after their exact bindings validate.

EXPORTS={'README.rst','check.py','bindings.json','review.json','replay.json','visual_review.json','whitespace.json'}

def later_publication(root,study):
 folder=root/M/'publication_review';ap=root/M/'root_publication_acceptance.json';rp=root/M/'root_publication_replay.json'
 if not folder.exists() and not ap.exists() and not rp.exists():return set(),{'state':'candidate_before_review_publication'}
 need(folder.is_dir() and not folder.is_symlink(),'exact public review folder')
 mf=read(folder,'manifest.json')
 need(mf['status']=='INDEPENDENT_PUBLICATION_REVIEW_FROZEN_ACCEPTED' and mf['candidate_sha256']==sha((HERE/'bindings.json').read_bytes()),'published independent review scope')
 need(len(mf['exports'])==len(EXPORTS) and {e['path'] for e in mf['exports']}==EXPORTS,'exact independent export names')
 allowed={M+'publication_review/manifest.json'}
 for row in mf['exports']:
  name=relative(row['path']);f=folder/name;need(f.is_file() and not f.is_symlink(),'regular review file');b=f.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'review export binding')
  need(b==(HERE/name).read_bytes(),'public review matches exact current reviewer file '+str(name))
  if study:need(b==(study/'topic_Representation_measurement_publication_review'/name).read_bytes(),'private/public review copy')
  allowed.add(M+'publication_review/'+str(name))
 need((folder/'manifest.json').read_bytes()==(HERE/'manifest.json').read_bytes(),'exact independent manifest copy')
 if not ap.exists() and not rp.exists():return allowed,{'state':'review_copied_before_root_adoption'}
 need(ap.is_file() and not ap.is_symlink() and rp.is_file() and not rp.is_symlink(),'paired acceptance and replay')
 a=read(root,M+'root_publication_acceptance.json')
 keys={'status','independent_manifest_sha256','independent_review_sha256','candidate_bindings_sha256','admission_sha256','fresh_root_replay','controls_rejected','author_and_reviewer_roles_preserved','no_primary_export','source_extraction_repeated','GAP_or_Lean_replayed','new_source_credit','new_question_credit','new_formal_credit'}
 need(set(a)==keys,'exact publication acceptance schema')
 need(a['status']=='ROOT_ACCEPTED_REPRESENTATION_MEASUREMENT_PUBLICATION_INTEGRATION' and a['independent_manifest_sha256']==sha((folder/'manifest.json').read_bytes()) and a['independent_review_sha256']==sha((folder/'review.json').read_bytes()) and a['candidate_bindings_sha256']==sha((HERE/'bindings.json').read_bytes()) and a['admission_sha256']==sha((root/M/'admission.json').read_bytes()),'publication acceptance anchors')
 need(a['author_and_reviewer_roles_preserved'] is True and a['no_primary_export'] is True and a['source_extraction_repeated'] is False and a['GAP_or_Lean_replayed'] is False and a['new_source_credit']==a['new_question_credit']==a['new_formal_credit']==0,'publication scope')
 rb=a['fresh_root_replay'];need(set(rb)=={'path','bytes','sha256'} and rb['path']=='root_publication_replay.json','exact root replay path')
 b=rp.read_bytes();need(len(b)==rb['bytes'] and sha(b)==rb['sha256'],'root replay binding');rr=json.loads(b)
 need(rr['status']=='PASS_BOUNDED_REPRESENTATION_PUBLICATION_INTEGRATION' and rr['candidate_sha256']==sha((HERE/'bindings.json').read_bytes()) and rr['candidate_files']==78 and rr['new_guard_result']==[120,120] and rr['prior_nonmain_functions_unchanged']==37 and rr['frozen_exports_plus_manifests']==66 and rr['public_input_routes']==16 and rr['separately_supplied_primary']==1 and rr['source_extraction_repeated'] is False and rr['GAP_or_Lean_replayed'] is False and rr['new_source_credit']==rr['new_question_credit']==rr['new_formal_credit']==0 and rr['admission_sha256']==a['admission_sha256'] and len(rr['semantic_controls'])==a['controls_rejected']==47 and {x['name'] for x in rr['semantic_controls']}=={x['name'] for x in read(HERE,'replay.json')['semantic_controls']} and all(x['rejected'] is True for x in rr['semantic_controls']),'root replay actual success')
 allowed|={M+'root_publication_acceptance.json',M+'root_publication_replay.json'}
 return allowed,{'state':'root_accepted_public_review','root_replay_sha256':rb['sha256']}

def publication_fixtures(root):
 import tempfile,shutil
 if not (HERE/'manifest.json').exists():return {'status':'DEFERRED_UNTIL_REVIEW_FREEZE','controls':[]}
 controls=[]
 with tempfile.TemporaryDirectory(prefix='R-review-publication-') as temp:
  fixture=Path(temp);(fixture/M).mkdir(parents=True);shutil.copyfile(root/M/'admission.json',fixture/M/'admission.json')
  need(later_publication(fixture,None)[0]==set(),'prepublication clean');controls.append({'name':'candidate before review copy','passed':True})
  folder=fixture/M/'publication_review';folder.mkdir()
  for name in EXPORTS|{'manifest.json'}:shutil.copyfile(HERE/name,folder/name)
  allowed,info=later_publication(fixture,None);need(len(allowed)==8 and info['state']=='review_copied_before_root_adoption','copied exact review');controls.append({'name':'copied exact review before acceptance','passed':True})
  rp=fixture/M/'root_publication_replay.json';rp.write_bytes((HERE/'replay.json').read_bytes());ap=fixture/M/'root_publication_acceptance.json'
  a={'status':'ROOT_ACCEPTED_REPRESENTATION_MEASUREMENT_PUBLICATION_INTEGRATION','independent_manifest_sha256':sha((folder/'manifest.json').read_bytes()),'independent_review_sha256':sha((folder/'review.json').read_bytes()),'candidate_bindings_sha256':sha((HERE/'bindings.json').read_bytes()),'admission_sha256':sha((fixture/M/'admission.json').read_bytes()),'fresh_root_replay':{'path':'root_publication_replay.json','bytes':rp.stat().st_size,'sha256':sha(rp.read_bytes())},'controls_rejected':len(read(HERE,'replay.json')['semantic_controls']),'author_and_reviewer_roles_preserved':True,'no_primary_export':True,'source_extraction_repeated':False,'GAP_or_Lean_replayed':False,'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0}
  ap.write_text(json.dumps(a)+'\n');allowed,info=later_publication(fixture,None);need(len(allowed)==10 and info['state']=='root_accepted_public_review','postpublication replay');controls.append({'name':'fully bound publication accepted','passed':True})
  def reject(name,path,change):
   before=path.read_bytes();d=json.loads(before);change(d);path.write_text(json.dumps(d)+'\n')
   try:later_publication(fixture,None)
   except (ValueError,KeyError):controls.append({'name':name,'rejected':True})
   else:raise ValueError('publication corruption accepted '+name)
   finally:path.write_bytes(before)
  reject('wrong reviewer manifest',ap,lambda x:x.update(independent_manifest_sha256='0'*64))
  reject('accept unrelated prefix',ap,lambda x:x.update(extra_allowed_directory='audit/'))
  reject('invent question credit',ap,lambda x:x.update(new_question_credit=1))
  reject('traversing root replay path',ap,lambda x:x['fresh_root_replay'].update(path='../outside'))
  reject('add unbound review export',folder/'manifest.json',lambda x:x['exports'].append({'path':'unrelated.txt','bytes':0,'sha256':'0'*64}))
  b=rp.read_bytes();ab=ap.read_bytes();bad=json.loads(b);bad['semantic_controls'][0]['rejected']=False;rp.write_text(json.dumps(bad)+'\n');a2=copy.deepcopy(a);a2['fresh_root_replay'].update(bytes=rp.stat().st_size,sha256=sha(rp.read_bytes()));ap.write_text(json.dumps(a2)+'\n')
  try:later_publication(fixture,None)
  except ValueError:controls.append({'name':'failed root replay even with consistent hash','rejected':True})
  else:raise ValueError('failed root replay admitted')
  finally:rp.write_bytes(b);ap.write_bytes(ab)
  need(M+'publication_review/unrelated.txt' not in allowed,'no broad publication directory exemption');controls.append({'name':'unrelated public files excluded','passed':True})
 return {'status':'PASS_EXACT_POSTPUBLICATION_FIXTURES','controls':controls}

def adapter_fixtures(root):
 import tempfile,shutil,sys
 adapter=module(root/M/'replay_inputs.py','RepresentationAdapterReview');need(adapter.ROOT==root,'adapter checkout depth')
 controls=[]
 for bad in ['../outside','/absolute/path','safe/../../outside']:
  try:adapter.relative(bad)
  except ValueError:controls.append({'name':'adapter rejects '+bad,'rejected':True})
  else:raise ValueError('unsafe adapter mapping')
 # Exercise rejection before any subprocess can execute. No source PDF is read.
 with tempfile.TemporaryDirectory(prefix='R-adapter-preflight-') as temp:
  tmp=Path(temp).resolve();here=tmp/'checkout/audit/topic-representation/v2/measurement';here.mkdir(parents=True)
  for folder in adapter.PINS:shutil.copytree(root/M/folder,here/folder)
  shutil.copyfile(root/M/'recount_mapping.json',here/'recount_mapping.json')
  oldhere,oldroot,oldargv,oldrun=adapter.HERE,adapter.ROOT,sys.argv,adapter.subprocess.run
  adapter.HERE=here;adapter.ROOT=tmp/'checkout'
  def noexec(*a,**k):raise RuntimeError('subprocess unexpectedly reached')
  adapter.subprocess.run=noexec
  def attempt(name,edit,undo,out=None):
   edit();sys.argv=['replay_inputs.py','--source-pdf',str(tmp/'deliberately_absent.pdf'),'--out',str(out or tmp/name.replace(' ','_'))]
   try:adapter.main()
   except ValueError as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
   else:raise ValueError('adapter corruption accepted '+name)
   finally:undo()
  try:
   for folder in adapter.PINS:
    path=here/folder/'manifest.json';before=path.read_bytes()
    attempt('adapter rejects changed '+folder+' pin',lambda p=path:p.write_text('{}\n'),lambda p=path,b=before:p.write_bytes(b))
   path=here/'input_review/check.py';before=path.read_bytes()
   attempt('adapter rejects changed executable review',lambda:path.write_bytes(before+b'\n# changed\n'),lambda:path.write_bytes(before))
   attempt('adapter rejects output inside checkout',lambda:None,lambda:None,out=tmp/'checkout/fresh-output')
   existing=tmp/'existing';existing.mkdir();attempt('adapter rejects existing output',lambda:None,lambda:None,out=existing)
   dangling=tmp/'dangling';dangling.symlink_to(tmp/'absent-target');attempt('adapter rejects dangling output',lambda:None,lambda:None,out=dangling)
  finally:adapter.HERE=oldhere;adapter.ROOT=oldroot;sys.argv=oldargv;adapter.subprocess.run=oldrun
 return controls

def audit(root,study):
 binding=read(HERE,'bindings.json');base=binding['base_commit']
 for row in binding['files']:
  b=(root/relative(row['path'])).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'candidate file '+row['path'])
 unchanged=old_checks(root,base);need(unchanged==37,'37 previous checker functions')
 copies=archive_copies(root,study);routes=mapping_check(root)
 v=module(root/'scripts/verify_snapshot.py','RepresentationPublicGuard');v.ROOT=root
 need(v.check_representation_measurement()==(120,120),'new public guard')
 links=[]
 for file in [M+'README.rst','README.rst','audit/completion.rst']:
  text=(root/file).read_text()
  if file=='README.rst':text=text.split('Recognizable extensions and finite normal pairs\n',1)[1].split('Chamber fibers, reflections and regular covers\n',1)[0]
  for target in re.findall(r'<([^>]+)>`_',text):
   if '://' in target:continue
   path=((root/file).parent/target.split('#')[0]).resolve();need(path.is_relative_to(root.resolve()) and path.exists(),'reader link '+target);links.append(dict(document=file,target=target))
  for target in re.findall(r'^\.\. image::\s*(\S+)',text,re.M):need(((root/file).parent/target).is_file(),'image link');links.append(dict(document=file,target=target))
 # A bounded guard call, not a rerun of primary/font/scientific computation.
 original=v.load;controls=[]
 def reject(name,path,change):
  data=copy.deepcopy(original(path));change(data);v.load=lambda x:copy.deepcopy(data) if x==path else original(x)
  try:v.check_representation_measurement()
  except (ValueError,KeyError,IndexError) as e:controls.append(dict(name=name,rejected=True,reason=str(e)))
  else:raise ValueError('semantic corruption accepted '+name)
  finally:v.load=original
 for key,value in [('status','PENDING'),('source_ids',['L092']),('source_blocks',5),('proof_contexts',12),('principal_contracts',2),('project_total_preserved',28),('pdf_metric_cells',119),('raw_metric_cells',0),('policy_coordinates',29),('combined_fractions',89),('conditional_fractions',29),('all_exact_fractions',119),('complete_validation_programs',1),('uniform_finite_proof_premises',2),('separate_drivers',0),('separate_formal_files',1),('scoped_Lean_declarations',13),('generic_declarations',12),('reused_local_declarations',0),('paired_dependency_audit_complete',True),('source_specific_formalization',True),('new_source_credit',1),('new_question_credit',1),('new_formal_credit',1)]:
  reject('admission '+key,M+'admission.json',lambda d,k=key,x=value:d.__setitem__(k,x))
 reject('unknown external cost replaced by zero',M+'admission.json',lambda d:d['unknown_external_costs'].__setitem__('retained_external_proofs',0))
 reject('printed-inclusive cost mislabeled written',M+'admission.json',lambda d:d['primary']['comparisons'].__setitem__('written_papers',d['primary']['comparisons']['including_printed_validation']))
 reject('UTF8 reversal hidden',M+'admission.json',lambda d:d['UTF8_reversal'].__setitem__('decimal','1.100000000000'))
 for file in ['input_review/review.json','input_adoption/review.json','arithmetic_review/review.json','root_adoption/review.json']:
  reject('unaccepted '+file,M+file,lambda d:d.update(status='PENDING'))
 reject('wrong numerical input pin',M+'packet/input_bindings.json',lambda d:d['accepted_manifest_sha256'].__setitem__('inputs','0'*64))
 reject('lost source qualification',M+'inputs/source_contract_boundary.json',lambda d:d.__setitem__('source_qualifications',[]))
 reject('failed root arithmetic control',M+'root_adoption/fresh_independent_replay.json',lambda d:d['controls'][0].__setitem__('rejected',False))
 reject('failed root chart control',M+'root_adoption/fresh_independent_replay.json',lambda d:d['presentation_controls'][0].__setitem__('rejected',False))
 reject('omitted scientific input',M+'recount_mapping.json',lambda d:d['routes'].pop(2))
 reject('primary material exported',M+'recount_mapping.json',lambda d:d.update(primary_exported=True))
 controls+=adapter_fixtures(root)
 # Read-only immutability comparison for science/registry and exact publication scope.
 changed=set(subprocess.check_output(['git','diff','--name-only',base],cwd=root,text=True).splitlines())
 allowed,state=later_publication(root,study)
 expected={r['path'] for r in binding['files']}|{'provenance/publication_manifest.json'}|allowed
 need(changed<=expected,'unreviewed changed public paths: '+repr(sorted(changed-expected)))
 for prefix in ['papers/','research/case_study/']:
  need(not any(x.startswith(prefix) for x in changed),'scientific bytes changed')
 for file in ['audit/source_registry.json','audit/intake.json','papers/catalogue.json']:
  if (root/file).exists():need((root/file).read_bytes()==subprocess.check_output(['git','show',base+':'+file],cwd=root),'registry/catalogue changed')
 adm=read(root,M+'admission.json');rp=read(root,M+'publication_replay/root_checks.json');ar=read(root,M+'publication_replay/input_adapter.json')
 need(rp['status']=='PASS_PUBLIC_REPRESENTATION_MEASUREMENT_REPLAYS' and rp['original_scientific_files_changed'] is False and rp['new_guard_result']==[120,120] and rp['prior_nonmain_guards_preserved']==37,'root publication replay')
 for key in ['input_adapter','arithmetic']:
  row=rp[key];need(sha((root/M/'publication_replay'/row['report']).read_bytes())==row['sha256'],'bound root public replay '+key)
 need(ar['status']=='PASS_PUBLIC_REPRESENTATION_INPUT_ADAPTER' and ar['public_files']==16 and ar['separately_supplied_originals']==1 and ar['pdf_metric_cells']==120 and ar['raw_metric_cells']==60 and ar['independent_controls']==30 and ar['primary_copies_removed'] is True and ar['primary_material_exported'] is False and ar['matches_archived_recount_except_elapsed_time'] is True,'root source replay scope')
 return dict(status='PASS_BOUNDED_REPRESENTATION_PUBLICATION_INTEGRATION',base_commit=base,candidate_sha256=sha((HERE/'bindings.json').read_bytes()),candidate_files=len(binding['files']),admission_sha256=sha((root/M/'admission.json').read_bytes()),prior_nonmain_functions_unchanged=unchanged,prior_dispatch_order_preserved=True,new_guard_result=[120,120],frozen_exports_plus_manifests=66,archives=copies,public_input_routes=16,separately_supplied_primary=1,links=links,semantic_controls=controls,postpublication=state,source_extraction_repeated=False,GAP_or_Lean_replayed=False,numerical_and_scientific_acceptances_reused=True,new_source_credit=0,new_question_credit=0,new_formal_credit=0)

def main():
 p=argparse.ArgumentParser();p.add_argument('--public-root',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output required')
 report=audit(a.public_root.resolve(),a.study_root.resolve() if a.study_root else None);report['publication_fixtures']=publication_fixtures(a.public_root.resolve());a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['archives','links','semantic_controls','publication_fixtures']}));print('Rejected semantic controls:',len(report['semantic_controls']))
if __name__=='__main__':main()
