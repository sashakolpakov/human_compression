#!/usr/bin/env python3
"""Independent bounded integration review. Reuses accepted science and arithmetic."""
import argparse,ast,copy,hashlib,importlib.util,json,re,subprocess,tempfile,sys,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE='dc9d521b16f6399934416f09caba14f50d4a48b8'
M='audit/topic-f/v2/measurement/'
ADM=M+'admission.json'
PRIVATE={'inputs':'topic_F_measurement_inputs','input_review':'topic_F_measurement_input_review','input_adoption':'topic_F_measurement_input_root_adoption','packet':'topic_F_measurement_numerical','arithmetic_review':'topic_F_measurement_numerical_review','root_adoption':'topic_F_measurement_numerical_root_adoption'}
def need(x,msg):
 if not x:raise ValueError(msg)
def sha(x):return hashlib.sha256(x).hexdigest()
def load(root,path):return json.loads((root/path).read_text())
def functions(text):return {x.name:x for x in ast.parse(text).body if isinstance(x,ast.FunctionDef)}
def astsame(x,y):return ast.dump(x,include_attributes=False)==ast.dump(y,include_attributes=False)
def calls(f):return [n.func.id for n in ast.walk(f) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id.startswith('check_')]
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def publication_additions(root, study, binding):
 """Validate only the separately adopted publication review and root report.

 The root acceptance anchors the independent manifest. The repository-wide
 manifest anchors the acceptance itself; there is no circular self-hash.
 """
 folder=root/M/'publication_review'
 acceptance=root/M/'publication_acceptance.json'
 report=root/M/'publication_root_replay.json'
 if not folder.exists() and not acceptance.exists() and not report.exists():
  return set(), {'state':'candidate_before_review_publication','validated_paths':[]}
 need(folder.is_dir() and not folder.is_symlink(),'published review directory')
 manifest=load(folder,'manifest.json')
 need(manifest['status']=='INDEPENDENT_PUBLICATION_REVIEW_FROZEN_ACCEPTED' and
      manifest['packet']=='topic_F_measurement_publication_review_v2' and
      manifest['candidate_bindings_sha256']==sha((HERE/'bindings.json').read_bytes()) and
      manifest['admission_sha256']==sha((root/ADM).read_bytes()),'published review scope')
 expected_names={'README.rst','bindings.json','check.py','replay.json','review.json','portability_controls.json'}
 need({r['path'] for r in manifest['exports']}==expected_names and len(manifest['exports'])==len(expected_names),'exact independent review export set')
 allowed={M+'publication_review/manifest.json'}
 for row in manifest['exports']:
  name=Path(row['path']);need(not name.is_absolute() and '..' not in name.parts,'relative independent export')
  file=folder/name;need(file.is_file() and not file.is_symlink(),'regular independent export')
  data=file.read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'changed independent export '+row['path'])
  allowed.add(M+'publication_review/'+row['path'])
 need((folder/'bindings.json').read_bytes()==(HERE/'bindings.json').read_bytes(),'review binds this exact candidate')
 need((folder/'check.py').read_bytes()==Path(__file__).read_bytes(),'published checker is this reviewed checker')
 if study:
  private=study/'topic_F_measurement_publication_review_v2'
  for name in expected_names|{'manifest.json'}:
   need((private/name).read_bytes()==(folder/name).read_bytes(),'private/public review equality '+name)
 if not acceptance.exists() and not report.exists():
  return allowed, {'state':'review_copied_before_root_adoption','validated_paths':sorted(allowed)}
 need(acceptance.is_file() and not acceptance.is_symlink() and report.is_file() and not report.is_symlink(),'root acceptance and replay must both exist')
 a=load(root,M+'publication_acceptance.json')
 keys={'status','independent_manifest_sha256','independent_review_sha256','candidate_bindings_sha256',
       'admission_sha256','fresh_root_replay','controls_rejected','author_and_reviewer_roles_preserved',
       'no_primary_export','new_source_credit','new_question_credit','new_formal_credit'}
 need(set(a)==keys,'exact root publication-acceptance schema')
 need(a['status']=='ROOT_ACCEPTED_INDEPENDENT_TOPIC_F_MEASUREMENT_PUBLICATION' and
      a['independent_manifest_sha256']==sha((folder/'manifest.json').read_bytes()) and
      a['independent_review_sha256']==sha((folder/'review.json').read_bytes()) and
      a['candidate_bindings_sha256']==sha((folder/'bindings.json').read_bytes()) and
      a['admission_sha256']==sha((root/ADM).read_bytes()),'root acceptance anchors exact review and candidate')
 need(a['author_and_reviewer_roles_preserved'] is True and a['no_primary_export'] is True and
      a['new_source_credit']==a['new_question_credit']==a['new_formal_credit']==0,'root publication scope')
 rb=a['fresh_root_replay'];need(set(rb)=={'path','bytes','sha256'} and rb['path']==M+'publication_root_replay.json','exact root replay path')
 raw=report.read_bytes();need(len(raw)==rb['bytes'] and sha(raw)==rb['sha256'],'bound root replay bytes')
 rr=json.loads(raw)
 need(rr['status']=='PASS_BOUNDED_PUBLICATION_INTEGRATION' and rr['base_commit']==BASE and
      rr['candidate_files']==62 and rr['admission_sha256']==a['admission_sha256'] and
      rr['prior_nonmain_functions_unchanged']==32 and rr['prior_guard_dispatch_preserved'] is True and
      rr['new_guard_result']==[120,120] and rr['frozen_exports_plus_manifests']==50 and
      rr['public_input_routes']==15 and rr['separately_supplied_primary']==1 and
      len(rr['semantic_controls'])==a['controls_rejected']==34 and
      all(c['rejected'] is True for c in rr['semantic_controls']) and
      rr['science_replayed'] is False and rr['input_extraction_repeated'] is False and
      rr['new_source_credit']==rr['new_question_credit']==rr['new_formal_credit']==0,'actual fresh root replay semantics')
 allowed|={M+'publication_acceptance.json',M+'publication_root_replay.json'}
 return allowed, {'state':'root_accepted_public_review','validated_paths':sorted(allowed),'root_replay_sha256':rb['sha256']}

def publication_controls(root):
 """Private filesystem fixtures exercise each postpublication acceptance gate."""
 result=[]
 with tempfile.TemporaryDirectory(prefix='F-review-publication-fixture-') as temp:
  fixture=Path(temp);(fixture/M).mkdir(parents=True)
  (fixture/ADM).write_bytes((root/ADM).read_bytes())
  binding=load(HERE,'bindings.json')
  allowed,state=publication_additions(fixture,None,binding)
  need(not allowed and state['state']=='candidate_before_review_publication','candidate stage')
  result.append({'name':'prepublication candidate needs no own review files','passed':True})
  folder=fixture/M/'publication_review';folder.mkdir()
  man=load(HERE,'manifest.json')
  for name in [r['path'] for r in man['exports']]+['manifest.json']:
   shutil.copyfile(HERE/name,folder/name)
  allowed,state=publication_additions(fixture,None,binding)
  need(len(allowed)==7 and state['state']=='review_copied_before_root_adoption','copied review stage')
  result.append({'name':'exact copied review allowed before adoption','passed':True})
  report=load(HERE,'replay.json')
  rp=fixture/M/'publication_root_replay.json'
  rp.write_text(json.dumps(report,indent=2)+'\n')
  ap=fixture/M/'publication_acceptance.json'
  acceptance={'status':'ROOT_ACCEPTED_INDEPENDENT_TOPIC_F_MEASUREMENT_PUBLICATION',
   'independent_manifest_sha256':sha((folder/'manifest.json').read_bytes()),
   'independent_review_sha256':sha((folder/'review.json').read_bytes()),
   'candidate_bindings_sha256':sha((folder/'bindings.json').read_bytes()),
   'admission_sha256':sha((fixture/ADM).read_bytes()),
   'fresh_root_replay':{'path':M+'publication_root_replay.json','bytes':rp.stat().st_size,'sha256':sha(rp.read_bytes())},
   'controls_rejected':34,'author_and_reviewer_roles_preserved':True,'no_primary_export':True,
   'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0}
  ap.write_text(json.dumps(acceptance,indent=2)+'\n')
  allowed,state=publication_additions(fixture,None,binding)
  need(len(allowed)==9 and state['state']=='root_accepted_public_review','postpublication exact paths')
  result.append({'name':'fully bound public review and acceptance allowed','passed':True})
  def corrupt(name,path,change):
   before=path.read_bytes();d=json.loads(before);change(d);path.write_text(json.dumps(d,indent=2)+'\n')
   try:publication_additions(fixture,None,binding)
   except (ValueError,KeyError,IndexError) as error:result.append({'name':name,'rejected':True,'reason':str(error)})
   else:raise ValueError('postpublication corruption accepted '+name)
   finally:path.write_bytes(before)
  corrupt('wrong independent review hash',ap,lambda d:d.__setitem__('independent_review_sha256','0'*64))
  corrupt('extra acceptance field grants unrelated path',ap,lambda d:d.__setitem__('allow_directory','audit/'))
  corrupt('replay path traversal',ap,lambda d:d['fresh_root_replay'].__setitem__('path','../outside'))
  corrupt('question credit in adoption',ap,lambda d:d.__setitem__('new_question_credit',1))
  corrupt('unbound independent export',folder/'manifest.json',lambda d:d['exports'].append({'path':'extra.json','bytes':0,'sha256':'0'*64}))
  original=rp.read_bytes();original_acceptance=ap.read_bytes()
  bad=json.loads(original);bad['semantic_controls'][0]['rejected']=False
  rp.write_text(json.dumps(bad,indent=2)+'\n')
  relink=copy.deepcopy(acceptance);relink['fresh_root_replay'].update(bytes=rp.stat().st_size,sha256=sha(rp.read_bytes()))
  ap.write_text(json.dumps(relink,indent=2)+'\n')
  try:publication_additions(fixture,None,binding)
  except ValueError as error:result.append({'name':'failed replay even with consistent new hash','rejected':True,'reason':str(error)})
  else:raise ValueError('failed root report accepted')
  finally:rp.write_bytes(original);ap.write_bytes(original_acceptance)
  original=ap.read_bytes();ap.unlink()
  try:publication_additions(fixture,None,binding)
  except ValueError as error:result.append({'name':'orphan root replay without acceptance','rejected':True,'reason':str(error)})
  else:raise ValueError('unadopted root replay allowed')
  finally:ap.write_bytes(original)
  need(M+'unrelated.json' not in allowed and 'unrelated.json' not in allowed,'no broad-prefix exception')
  result.append({'name':'unrelated paths remain outside exact allowed set','passed':True})
 return result

def audit(root,study):
 binding=load(HERE,'bindings.json')
 for row in binding['bindings']:
  b=(root/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'candidate binding '+row['path'])
 oldtext=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=root,text=True)
 newtext=(root/'scripts/verify_snapshot.py').read_text();old,new=functions(oldtext),functions(newtext)
 need(all(astsame(f,new[k]) for k,f in old.items() if k!='main'),'old checker function changed')
 need(set(new)-set(old)=={'check_topic_f_measurement'},'only one new guard')
 need([x for x in calls(new['main']) if x!='check_topic_f_measurement']==calls(old['main']) and calls(new['main']).count('check_topic_f_measurement')==1,'old dispatch order')
 v=module(root/'scripts/verify_snapshot.py','TopicFPublicationGuard');v.ROOT=root
 need(v.check_topic_f_measurement()==(120,120),'new public guard')
 admission=load(root,ADM);copies=[]
 for folder,pin in admission['packet_manifests'].items():
  dest=root/M/folder;m=load(dest,'manifest.json');need(sha((dest/'manifest.json').read_bytes())==pin,'admitted archive pin')
  for row in m['exports']:
   b=(dest/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'archive export')
  if study:
   source=study/PRIVATE[folder]
   for path in [x['path'] for x in m['exports']]+['manifest.json']:
    need((source/path).read_bytes()==(dest/path).read_bytes(),'frozen private/public equality '+folder+'/'+path)
  copies.append({'folder':folder,'exports':len(m['exports']),'manifest_sha256':pin,'private_equality':bool(study)})
 mapping=load(root,M+'input_adoption/public_mapping.json')['routes'];inputs=load(root,M+'inputs/manifest.json')['immutable_inputs']
 need([{k:r[k] for k in ['path','bytes','sha256']} for r in mapping]==inputs,'complete immutable mapping')
 for row in mapping:
  if row['public_path']:
   b=(root/row['public_path']).read_bytes();need(sha(b)==row['sha256'] and len(b)==row['bytes'],'public scientific route')
 need(len(mapping)==16 and sum(r['public_path'] is not None for r in mapping)==15,'exact 15 public + 1 source routes')
 for path in ['papers/catalogue.json','audit/source_registry.json','audit/intake.json']:
  # Some longstanding registry lives elsewhere: only listed existing tracked paths are compared.
  p=root/path
  if p.exists():
   oldb=subprocess.check_output(['git','show',BASE+':'+path],cwd=root);need(p.read_bytes()==oldb,'unrelated scientific registry/catalogue changed '+path)
 links=[]
 for path in [M+'README.rst','README.rst','audit/completion.rst']:
  text=(root/path).read_text()
  if path=='README.rst':text=text.split('Odd kernels and cyclotomic polyhedra\n',1)[1].split('Flag relations and incidence residues\n',1)[0]
  for target in re.findall(r'<([^>]+)>`_',text):
   if '://' in target:continue
   p=((root/path).parent/target.split('#')[0]).resolve();need(p.is_relative_to(root.resolve()) and p.exists(),'reader link '+target);links.append({'document':path,'target':target})
  for target in re.findall(r'^\.\. image::\s*(\S+)',text,re.M):
   need(((root/path).parent/target).is_file(),'image link');links.append({'document':path,'target':target})
 original=v.load;controls=[]
 def reject(name,path,change):
  d=original(path);change(d);v.load=lambda x:copy.deepcopy(d) if x==path else original(x)
  try:v.check_topic_f_measurement()
  except (ValueError,KeyError,IndexError) as error:controls.append({'name':name,'rejected':True,'reason':str(error)})
  else:raise ValueError('semantic corruption accepted: '+name)
  finally:v.load=original
 for key,value in [('status','PENDING'),('source_ids',['L012']),('source_records',24),('principal_contracts',2),('project_total_preserved',28),('policy_coordinates',29),('pdf_metric_cells',119),('raw_metric_cells',0),('exact_fractions',119),('combined_fractions',91),('conditional_fractions',29),('required_uniform_proof_programs',3),('complete_validation_programs',2),('separate_drivers',0),('separate_formal_files',0),('scoped_Lean_declarations',6),('paired_dependency_audit_complete',True),('source_specific_formalization',True),('new_source_credit',1),('new_question_credit',1),('new_formal_credit',1)]:
  reject('admission '+key,ADM,lambda d,k=key,x=value:d.__setitem__(k,x))
 reject('unknown retained input changed to zero',ADM,lambda d:d['unknown_external_costs'].__setitem__('retained_CP_fulltext',0))
 reject('program-inclusive total substituted as written',ADM,lambda d:d['primary']['comparisons'].__setitem__('written',d['primary']['comparisons']['including_printed_validation']))
 reject('unaccepted arithmetic review',M+'arithmetic_review/review.json',lambda d:d.__setitem__('status','PENDING'))
 reject('unaccepted input adoption',M+'input_adoption/review.json',lambda d:d.__setitem__('status','PENDING'))
 reject('wrong input packet',M+'packet/measurement.json',lambda d:d['input_manifests'].__setitem__('inputs','0'*64))
 reject('omitted raw program',M+'input_adoption/public_mapping.json',lambda d:d['routes'].pop(4))
 reject('primary published',M+'input_adoption/public_mapping.json',lambda d:d.__setitem__('no_primary_export',False))
 reject('failed root arithmetic control',M+'root_adoption/fresh_arithmetic.json',lambda d:d['controls'][0].__setitem__('rejected',False))
 adapter=module(root/M/'replay_inputs.py','FInputPublicationAdapter');need(adapter.ROOT==root,'adapter repository depth')
 for text in ['../outside','/absolute/path','safe/../../outside']:
  try:adapter.relative(text)
  except ValueError:controls.append({'name':'adapter rejects '+text,'rejected':True})
  else:raise ValueError('unsafe adapter path')
 # Check the public adapter actually pins every executable review source before execution.
 for folder in ['inputs','input_adoption','input_review']:
  adapter.check_packet(folder,admission['packet_manifests'][folder])
 with tempfile.TemporaryDirectory(prefix='F-public-adapter-review-') as tmp:
  tmp=Path(tmp);base=tmp/'measurement';base.mkdir()
  for folder in ['inputs','input_adoption','input_review']:shutil.copytree(root/M/folder,base/folder)
  saved_here=adapter.HERE;adapter.HERE=base
  try:
   target=base/'input_review/recount.py';target.write_bytes(target.read_bytes()+b'\n# review corruption\n')
   try:adapter.check_packet('input_review',admission['packet_manifests']['input_review'])
   except ValueError:controls.append({'name':'tampered executable review script','rejected':True})
   else:raise ValueError('changed executable accepted')
   saved_argv=sys.argv[:]
   try:
    sys.argv=['replay_inputs.py','--source-pdf',str(tmp/'not-read.pdf'),'--out',str(tmp/'not-created')]
    try:adapter.main()
    except ValueError as e:
     need('recount.py' in str(e),'adapter failed for wrong reason')
     need(not (tmp/'not-created').exists(),'adapter wrote before executable integrity check')
     controls.append({'name':'standalone adapter rejects changed reviewer before any execution','rejected':True,'reason':str(e)})
    else:raise ValueError('main bypassed executable review pin')
   finally:sys.argv=saved_argv
  finally:adapter.HERE=saved_here
 # Exact changed-file boundary: no source manuscript, primary, Lean build or Markdown is added.
 changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=root,text=True).splitlines()
 additions, publication_state=publication_additions(root,study,binding)
 need(set(changed)<=set(r['path'] for r in binding['bindings'])|{'provenance/publication_manifest.json'}|additions,'unexpected public edits')
 need(not any('/sources/' in p or p.endswith(('.md','.olean','.png','.jpg')) for p in changed),'private/build export')
 svg=M+'packet/complete_costs.svg';exceptions=[]
 data=(root/svg).read_bytes();lines=data.decode().splitlines();trailing=[i+1 for i,x in enumerate(lines) if x.endswith((' ','\t'))]
 exceptions.append({'path':svg,'sha256':sha(data),'trailing_space_lines':trailing,'reason':'Exact frozen matplotlib SVG; preserved byte-for-byte.'})
 r=subprocess.run(['git','diff',BASE,'--check','--','.',':(exclude)'+svg],cwd=root,text=True,capture_output=True)
 need(r.returncode==0,'unbound whitespace '+r.stdout)
 publication_tests=publication_controls(root)
 need(publication_tests==load(HERE,'portability_controls.json')['controls'],'frozen portability fixtures')
 return {'status':'PASS_BOUNDED_PUBLICATION_INTEGRATION','base_commit':BASE,'candidate_files':len(binding['bindings']),'admission_sha256':sha((root/ADM).read_bytes()),'admission_artifacts':len(admission['artifacts']),'packet_copies':copies,'frozen_exports_plus_manifests':sum(x['exports']+1 for x in copies),'prior_nonmain_functions_unchanged':len(old)-1,'prior_guard_dispatch_preserved':True,'new_guard_result':[120,120],'public_input_routes':15,'separately_supplied_primary':1,'reader_links':links,'semantic_controls':controls,'whitespace_exceptions':exceptions,'publication_review_additions':publication_state,'publication_validation_controls':publication_tests,'science_replayed':False,'input_extraction_repeated':False,'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--study',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh report path');x=audit(a.repository,a.study);a.out.write_text(json.dumps(x,indent=2)+'\n');print(json.dumps({k:x[k] for k in ['status','candidate_files','prior_nonmain_functions_unchanged']}));print('controls',len(x['semantic_controls']))
