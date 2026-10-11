#!/usr/bin/env python3
"""Bounded read-only G publication integration review; no science replay."""
import argparse,ast,copy,hashlib,importlib.util,json,pathlib,re,subprocess
BASE='b731b4cd6dc5aa04010f89ef0634cee7793e4631'
HERE=pathlib.Path(__file__).resolve().parent
ADM='audit/topic-g/v2/admission.json';SCOPE='papers/topic-g/v2/scope.json'
PRIVATE={'current_edition':'topic_G_current_edition','original_author':'topic_G_volume','notation_delta':'topic_G_notation_delta','program_formal_review':'topic_G_program_formal_independent_review','steiner_review':'topic_G_steiner_independent_review','root_adoption':'topic_G_root_adoption','assembly_replay':'topic_G_current_edition_replay'}
def need(b,s):
 if not b:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(r,p):return json.loads((r/p).read_text())
def funcs(s):return {n.name:n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
def dump(n):return ast.dump(n,include_attributes=False)
def calls(n):return [x.func.id for x in ast.walk(n) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id.startswith('check_')]
def audit(root,study):
 bounds=load(HERE,'bindings.json')
 for r in bounds['public']:
  b=(root/r['path']).read_bytes();need(sha(b)==r['sha256'] and len(b)==r['bytes'],'candidate binding '+r['path'])
 oldtext=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=root,text=True);newtext=(root/'scripts/verify_snapshot.py').read_text();old,new=funcs(oldtext),funcs(newtext)
 prior=[k for k in old if k!='main'];need(all(dump(old[k])==dump(new[k]) for k in prior),'previous checker AST changed')
 need(set(new)-set(old)=={'check_topic_g_proofs'},'unexpected checker added');need([x for x in calls(new['main']) if x!='check_topic_g_proofs']==calls(old['main']) and calls(new['main']).count('check_topic_g_proofs')==1,'old checker order changed')
 spec=importlib.util.spec_from_file_location('GPublication',root/'scripts/verify_snapshot.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.ROOT=root
 need(m.check_topic_g_proofs()==(79,40),'G check');need(m.check_catalogue()==(10,37),'catalogue check')
 admission=load(root,ADM);copies=[];allfiles=[]
 for p in admission['packets']:
  public=root/p['path'];private=study/PRIVATE[p['role']] if study else None;man=load(public,'manifest.json');need(len(man['exports'])==p['exports'] and sha((public/'manifest.json').read_bytes())==p['manifest_sha256'],'packet manifest')
  for r in man['exports']:
   b=(public/r['path']).read_bytes();need(sha(b)==r['sha256'] and len(b)==r['bytes'],'public export binding')
  for path in [r['path'] for r in man['exports']]+['manifest.json']:
   if private:need((public/path).read_bytes()==(private/path).read_bytes(),'private/public frozen equality '+path)
   allfiles.append(str(pathlib.Path(p['path'])/path))
  copies.append(dict(role=p['role'],exports=len(man['exports']),manifest_additional=True,private_equality=bool(private)))
 need(len(allfiles)==len(set(allfiles))==288,'frozen copy total')
 oldcat=json.loads(subprocess.check_output(['git','show',BASE+':papers/catalogue.json'],cwd=root,text=True));cat=load(root,'papers/catalogue.json')
 need(cat['papers']==oldcat['papers'] and cat['new_editions'][:-3]==oldcat['new_editions'],'old catalogue entries')
 need({k:v for k,v in cat['current_topic_editions'].items() if k!='G'}==oldcat['current_topic_editions'],'old current edition routes')
 entries=cat['new_editions'][-3:]
 for row,name,role,app,pages,source in zip(entries,['umbrella','triangle-geometries','steiner-geometries'],['umbrella','application','application'],['U_G','G1','G2'],[12,8,22],[[],['L009'],['L092']]):
  need(row['id']=='topic-g/v2/'+name and row['tex']=='papers/topic-g/v2/'+name+'.tex' and row['pdf']=='papers/topic-g/v2/'+name+'.pdf' and row['role']==role and row['application_id']==app and row['physical_pages']==pages and row['source_contracts']==source,'exact current paper identity')
  need(all(p in set(allfiles) for p in [row['tex'],row['pdf']]+row['tex_inputs']),'all TeX dependencies explicitly copied')
 # Only read links in the new reader passage; prior unrelated links are not this review.
 links=[]
 for file in ['papers/topic-g/v2/PUBLICATION.rst','audit/completion.rst','README.rst']:
  text=(root/file).read_text()
  if file=='README.rst':text=text.split('Flag relations and incidence residues\n',1)[1].split('Papers and verification\n',1)[0]
  for target in re.findall(r'<([^>]+)>`_',text):
   if '://' in target:continue
   path=((root/file).parent/target.split('#')[0]).resolve();need(path.is_relative_to(root.resolve()) and path.exists(),'reader link '+target);links.append(dict(document=file,target=target))
 changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=root,text=True).splitlines();gpaths=[p for p in changed if '/topic-g/v2/' in p]
 need(not any(pathlib.Path(p).suffix in ['.md','.olean','.png','.jpg'] or '/sources/' in p for p in gpaths),'unintended private or build export')
 original=m.load;controls=[]
 def reject(name,path,fn):
  obj=original(path);fn(obj);m.load=lambda p:copy.deepcopy(obj) if p==path else original(p)
  try:m.check_topic_g_proofs()
  except (ValueError,KeyError,IndexError) as e:controls.append(dict(name=name,rejected=True,reason=str(e)))
  else:raise ValueError('semantic mutation accepted: '+name)
  finally:m.load=original
 for key,val in [('status','PENDING'),('source_rows',80),('proof_or_context_spans',33),('scientific_pages',41),('common_pages',11),('whole_program_pages',19),('complete_programs',12),('required_mathematical_programs',3),('witness_or_certificate_programs',0),('validation_programs',8),('separate_operational_files',1),('formal_modules',7),('reused_lean_declarations',41),('new_lean_declarations',40),('end_to_end_source_formalization',True),('project_total_preserved',28),('canonical_complete_contract_count_at_this_admission',25),('remaining_contracts_for_canonical_topic_editions',[]),('compression_ratio',2),('retained_classification_full_cost',0),('source_graphics_cost',0),('new_question_credit',1),('new_principal_credit',1),('source_corrections_and_exclusions_preserved',False),('whole_common_charged_once_within_topic',False),('cross_topic_discount',True)]:
  reject('admission '+key,ADM,lambda d,k=key,v=val:d.__setitem__(k,v))
 for id,status in [('L092.Pasini.names','recovered'),('L092.T10','reproved'),('L009.question.gonality3','solved'),('L092.Conj1','new solution')]:
  reject('source disposition '+id,SCOPE,lambda d,id=id,status=status:next(r for r in d['rows'] if r['id']==id).__setitem__('status',status))
 reject('notation changed to additive quotient','audit/topic-g/v2/notation_delta/delta.json',lambda d:d.__setitem__('new_literal',r'\(\mathbb F_{16}/\mathbb F_4\)'))
 reject('original file dropped from assembly','papers/topic-g/v2/assembly.json',lambda d:d['mapping'].pop())
 reject('root review pending','audit/topic-g/v2/root_adoption/review.json',lambda d:d.__setitem__('status','PENDING'))
 reject('Steiner review pending','audit/topic-g/v2/steiner_review/review.json',lambda d:d.__setitem__('status','PENDING'))
 reject('whole finite file omitted','papers/topic-g/v2/program_inventory.json',lambda d:d['programs'].pop())
 reject('wrong formal axiom','audit/topic-g/v2/program_formal_review/audit.json',lambda d:d['formal_declarations'][0]['axioms'].append('sorryAx'))
 reject('failed actual program replay','audit/topic-g/v2/program_formal_review/replay/report.json',lambda d:d['program_replays'][0].__setitem__('returncode',1))
 reject('catalogue dependency dropped','papers/catalogue.json',lambda d:next(r for r in d['new_editions'] if r['id']=='topic-g/v2/umbrella')['tex_inputs'].pop())
 reject('program appendix render mismatch','audit/topic-g/v2/assembly_replay/render.json',lambda d:d['documents'][-1].__setitem__('same_text_as_bound',False))
 whitespace=load(HERE,'whitespace_exceptions.json')
 for r in whitespace['frozen_exceptions']:need(sha((root/r['path']).read_bytes())==r['sha256'],'whitespace exception changed')
 p=subprocess.run(['git','diff',BASE,'--check','--','.']+[':(exclude)'+r['path'] for r in whitespace['frozen_exceptions']],cwd=root,text=True,capture_output=True);need(p.returncode==0,'unbound whitespace '+p.stdout)
 return dict(status='PASS_BOUNDED_PUBLICATION_REVIEW',baseline=BASE,admission_sha256=sha((root/ADM).read_bytes()),admission_artifacts=len(admission['artifacts']),frozen_copies=len(allfiles),packets=copies,old_nonmain_functions_unchanged=len(prior),old_checker_order_preserved=True,new_checker=[79,40],catalogue=[10,37],prior_catalogue_preserved=True,public_links=links,no_primary_or_build_exports=True,semantic_controls=controls,whitespace_exceptions=whitespace,scope='Integration only; prior accepted mathematics, source, finite and formal reviews reused. No new scientific replay, result or ratio.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repository',type=pathlib.Path,required=True);p.add_argument('--study',type=pathlib.Path);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');r=audit(a.repository,a.study);a.out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','frozen_copies','old_nonmain_functions_unchanged']}));print('controls',len(r['semantic_controls']))
