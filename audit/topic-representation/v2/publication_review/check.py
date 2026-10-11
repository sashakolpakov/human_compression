#!/usr/bin/env python3
"""Independent review of root integration, not of this reviewer's own science."""
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.util,json,re,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
CANDIDATE='17d390b48df202033308c93167218de266418662e23bbbb90910ed69c7828055'
BASE='580d6d06851206c06c5b55313ffc0f9040cf4a8f'
P='papers/topic-representation/v2/'
A='audit/topic-representation/v2/'
MAPPINGS=[(P,'topic_Representation_volume',46),(A+'independent_review/','topic_Representation_independent_review',25),(A+'review_role_delta/','topic_Representation_review_role_delta',2),(A+'root_adoption/','topic_Representation_root_adoption',5)]
def need(ok,why):
 if not ok:raise ValueError('REPRESENTATION_PUBLICATION_REJECT: '+why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output directory');a.out.mkdir(parents=True)
 root=a.public_root;need(sha(HERE/'candidate.json')==CANDIDATE,'immutable candidate boundary');cand=read(HERE/'candidate.json');need(cand['base_commit']==BASE and len(cand['public_files'])==cand['file_count']==93,'exact candidate')
 expected={r['path'] for r in cand['public_files']}
 for row in cand['public_files']:
  f=root/row['path'];need(f.is_file() and f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'exact candidate file '+row['path'])
 changes=set(subprocess.check_output(['git','diff','--name-only',BASE],cwd=root,text=True).splitlines())
 changes.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=root,text=True).splitlines())
 allowed=expected|{'provenance/publication_manifest.json',A+'publication_acceptance.json',A+'publication_replay/independent_integration.json'}
 pubreview=root/A/'publication_review';privreview=a.study_root/'topic_Representation_publication_review'
 if (pubreview/'manifest.json').exists():
  need((pubreview/'manifest.json').read_bytes()==(privreview/'manifest.json').read_bytes(),'exact declared review manifest');allowed.add(A+'publication_review/manifest.json')
  for row in read(pubreview/'manifest.json')['exports']:
   path=Path(row['path']);need(not path.is_absolute() and '..' not in path.parts,'safe review export')
   f=pubreview/path;need(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'] and f.read_bytes()==(privreview/path).read_bytes(),'exact declared review export');allowed.add(A+'publication_review/'+row['path'])
 need(not(changes-allowed),'unexpected mutation beyond candidate and exact review/root rollup: '+str(sorted(changes-allowed)))
 copied=[]
 for public,private,count in MAPPINGS:
  x=root/public;y=a.study_root/private
  need((x/'manifest.json').read_bytes()==(y/'manifest.json').read_bytes(),'exact manifest '+private);m=read(y/'manifest.json');need(len(m['exports'])==count,'exact export count')
  for row in m['exports']:
   f=x/row['path'];need(f.read_bytes()==(y/row['path']).read_bytes() and sha(f)==row['sha256'] and f.stat().st_size==row['bytes'],'exact scientific/review copy '+row['path'])
  copied.append(dict(public=public,private=private,exports=count,manifest_sha256=sha(x/'manifest.json')))
 old=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=root,text=True);new=(root/'scripts/verify_snapshot.py').read_text()
 def functions(t):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(t).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
 before,after=functions(old),functions(new);prior=set(before)-{'main'}
 need(len(prior)==33 and all(before[k]==after[k] for k in prior),'all 33 earlier non-main verifier ASTs unchanged');need(set(after)-set(before)=={'check_representation_proofs'},'one new declared guard')
 docs=['README.rst','audit/completion.rst',P+'PUBLICATION.rst',P+'README.rst',A+'independent_review/README.rst',A+'root_adoption/README.rst'];links=[]
 for name in docs:
  doc=root/name
  for target in re.findall(r'<([^<>]+)>`_',doc.read_text()):
   if '://' in target or target.startswith('#'):continue
   need((doc.parent/target.split('#')[0]).exists(),'relative link '+name+' -> '+target);links.append(dict(document=name,target=target))
 # Exact candidate allowlist forbids extra primary texts/images; only own PDFs occur here.
 allowed_pdfs={P+'umbrella.pdf',P+'finite-normal-pairs.pdf',P+'program-appendix.pdf','audit/protocol.pdf'}
 for name in expected:
  need(not name.endswith(('.md','.png','.jpg','.jpeg','.olean')),'unexpected raster/cache/Markdown')
  if name.endswith('.pdf'):need(name in allowed_pdfs,'primary PDF export')
 spec=importlib.util.spec_from_file_location('representation_integrated_verifier',root/'scripts/verify_snapshot.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);need(v.check_representation_proofs()==(6,12),'new standard guard result')
 original=v.load;controls=[]
 cases=[
 ('rank_two_overclaim',P+'scope.json',lambda x:x['precise_hypotheses'].update(rank_two_universal_claim=True)),
 ('drop_normality',P+'scope.json',lambda x:x['precise_hypotheses'].update(normal_subgroup_required=False)),
 ('cleaning_connectedness_overclaim',P+'scope.json',lambda x:x['precise_hypotheses'].update(arbitrary_input_cleaning_need_not_be_connected=False)),
 ('hexagon_uncorrected',P+'scope.json',lambda x:next(r for r in x['contracts'] if r['id']=='F010.Example5.1').update(status='literal_source_verified')),
 ('omit_source_qualification',P+'scope.json',lambda x:x['source_qualifications'].pop()),
 ('rename_original_authors',P+'scope.json',lambda x:x['source'].update(authors=['Wrong author'])),
 ('whole_program_omitted',P+'scope.json',lambda x:x['program_inventory'].pop(0)),
 ('finite_model_as_uniform_premise',P+'scope.json',lambda x:x['program_inventory'][0].update(universal_proof_premise=True)),
 ('wrong_role_delta',A+'review_role_delta/correction.json',lambda x:x.update(new='root')),
 ('double_formal_count',A+'admission.json',lambda x:x.update(new_lean_declarations=12)),
 ('claim_full_formalization',A+'admission.json',lambda x:x.update(end_to_end_source_formalization=True)),
 ('custom_axiom',A+'independent_review/fresh_replay/formal/report.json',lambda x:x['modules'][0]['axioms'][0]['axioms'].append('unprovedAxiom')),
 ('incomplete_catalogue_inputs','papers/catalogue.json',lambda x:next(r for r in x['new_editions'] if r['id']=='topic-representation/v2/umbrella')['tex_inputs'].pop()),
 ('invent_ratio',A+'admission.json',lambda x:x.update(compression_ratio=2)),
 ('new_question_credit',A+'admission.json',lambda x:x.update(new_question_credit=1)),
 ('new_source_credit',A+'admission.json',lambda x:x.update(new_source_credit=1))]
 for name,path,change in cases:
  bad=copy.deepcopy(original(path));change(bad);v.load=lambda p,path=path,bad=bad:copy.deepcopy(bad) if p==path else original(p)
  try:v.check_representation_proofs()
  except (ValueError,KeyError) as exc:controls.append(dict(name=name,rejected=True,reason=str(exc),method='Parsed-object semantic mutation; no public file edited.'))
  else:raise RuntimeError('Accepted false semantic mutation '+name)
  finally:v.load=original
 with tempfile.TemporaryDirectory(prefix='repr-integrity-') as d:
  f=Path(d)/'proof.lean';f.write_text('example : True := True.intro\n');row=dict(path=f.name,bytes=f.stat().st_size,sha256=sha(f));f.write_text('axiom bad : False\n');vr=v.ROOT;v.ROOT=Path(d)
  try:v.check_bindings([row])
  except ValueError as exc:controls.append(dict(name='changed_bound_proof',rejected=True,reason=str(exc),method='Temporary file only.'))
  else:raise RuntimeError('Changed proof accepted')
  finally:v.ROOT=vr
 # Fresh public command exercises binding/staging without repeating mathematics.
 cmd=[sys.executable,'-B','-O',str(root/P/'check.py'),'--out',str(a.out/'portable_bindings')]
 proc=subprocess.run(cmd,text=True,capture_output=True);(a.out/'portable.stdout').write_text(proc.stdout);(a.out/'portable.stderr').write_text(proc.stderr);need(proc.returncode==0,'portable public binding command')
 portable=read(a.out/'portable_bindings/report.json');need(portable['status']=='PASS' and portable['source_blocks']==6 and portable['proof_spans']==13,'portable complete source bindings')
 report=dict(status='ACCEPTED_BOUNDED_ROOT_PUBLICATION_INTEGRATION',candidate_sha256=CANDIDATE,baseline_commit=BASE,candidate_files_checked=93,prior_nonmain_verifier_ASTs_unchanged=33,new_guard_result=[6,12],exact_copies=copied,total_copied_exports=78,relative_links_checked=len(links),semantic_controls=controls,portable_public_binding_replay=portable,unexpected_changes=[],allowed_post_review_additions={'review':'Only byte-exact paths declared by its own frozen manifest; no prefix exclusion','root_acceptance':A+'publication_acceptance.json','root_replay':A+'publication_replay/independent_integration.json','standard_manifest':'provenance/publication_manifest.json'},reviewer_role='enumeration_volume authored the scientific edition; this review independently audits root-authored publication integration only, not its own mathematics.',scientific_acceptance_retained_from='enumeration_review 5ff68feb with exact role delta8577769f; root adoptioncbf96238',new_GAP_or_Lean_run=False,mathematical_proofs_reaccepted=False,public_files_modified=False,new_source_credit=0,new_question_credit=0,compression_ratio=None)
 (a.out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','candidate_files_checked','prior_nonmain_verifier_ASTs_unchanged','new_guard_result','total_copied_exports','relative_links_checked']}))
if __name__=='__main__':main()
