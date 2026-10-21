#!/usr/bin/env python3
"""Read-only publication review, not an independent re-audit of authored costs."""
import argparse,ast,copy,hashlib,importlib.util,json,re,shutil,subprocess,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
BASE='87143e24c6fcc588ab339a9c3b01dd6cc3808486'
ADMISSION='12390b837bee5757913ca707d784424d87ea8124506970de149b4e1666324c2b'
B='audit/topic-c/v2/dag/'
PACKETS={
 'logical_previous':('topic_C_logical_dag','99ee813a34bc203cc21f7d7e5645ab8583c2660f8b3bd765c1bcbce6cf375a49'),
 'logical':('topic_C_logical_dag_v2','214e8c47cedb21897a590387cb25557189e600b3356b828f20f722293d84bdf3'),
 'logical_review':('topic_C_logical_dag_independent_review','f1376df93d5a10c5e1b0783d0d70fa6d775c4ca182aaa7799f999e88406312d8'),
 'costs_previous':('topic_C_dag_costs','d78d618ed35ffb31d260ded85d27627f8db43a435a5fe4cd02822dd510beb718'),
 'costs':('topic_C_dag_costs_v2','74cebf42fad7330804bfb95a85bf44eae729e62fb4c311b4ad7c32364e6202d8'),
 'independent_review':('topic_C_dag_costs_independent_review','4e4adbb96f01f7d9ccbc0c238533f2c652905a6a5a6eb9d3891b4fb3b2ea115d'),
 'root_adoption':('topic_C_dag_root_adoption','58770ac2fbc3ce3a5e184e293c32aaf85f422e5549f6d4178a75625045b7405f')}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def ast_dump(n):return ast.dump(n,include_attributes=False)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output report');root=a.public_root.resolve();study=a.study_root.resolve()
 admission=read(root/B/'admission.json');need(sha((root/B/'admission.json').read_bytes())==ADMISSION,'exact core admission')
 need(admission['packet_manifests']=={k:r[1] for k,r in PACKETS.items()},'all seven pinned packets')
 copies=[]
 for folder,(private,pin) in PACKETS.items():
  p,q=root/B/folder,study/private
  need((p/'manifest.json').read_bytes()==(q/'manifest.json').read_bytes() and sha((p/'manifest.json').read_bytes())==pin,'unchanged pinned manifest')
  m=read(p/'manifest.json')
  for row in m['exports']:
   n=Path(row['path']);need(not n.is_absolute() and '..' not in n.parts,'safe frozen export')
   data=(p/n).read_bytes();need(data==(q/n).read_bytes() and len(data)==row['bytes'] and sha(data)==row['sha256'],'unchanged frozen bytes '+str(n))
  copies.append(dict(folder=folder,private=private,exports=len(m['exports']),manifest_sha256=pin,identical=True))
 need(sum(r['exports'] for r in copies)==133,'complete frozen copy count')
 for row in admission['artifacts']:
  n=Path(row['path']);need(not n.is_absolute() and '..' not in n.parts,'safe admission path')
  b=(root/n).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'bound admission artifact')
 verifier=root/'scripts/verify_snapshot.py';spec=importlib.util.spec_from_file_location('C_publication_snapshot',verifier);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 need(v.check_topic_c_dag()==(270,85),'positive public C dependency check')
 old=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=root,text=True)
 funcs=lambda text:{n.name:n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
 oldf,newf=funcs(old),funcs(verifier.read_text());need(set(newf)-set(oldf)=={'check_topic_c_dag'} and set(oldf)<=set(newf),'only new C DAG checker added')
 prior=[n for n in oldf if n!='main'];need(len(prior)==27 and all(ast_dump(oldf[n])==ast_dump(newf[n]) for n in prior),'all 27 older non-main ASTs preserved')
 original_statements={ast_dump(n) for n in oldf['main'].body};newmain=copy.deepcopy(newf['main']);extra=[n for n in newmain.body if ast_dump(n) not in original_statements]
 need(len(extra)==2 and any('check_topic_c_dag' in ast_dump(n) for n in extra) and any('c_closures' in ast_dump(n) for n in extra),'only new checker call and status line')
 newmain.body=[n for n in newmain.body if ast_dump(n) in original_statements];need(ast_dump(newmain)==ast_dump(oldf['main']),'all prior main statements/order preserved')
 unchanged=['papers/catalogue.json','audit/intake.json','audit/source_registry.json','audit/completion.json',
  'scripts/build_papers.py','research/case_study/formal/lakefile.lean','audit/topic-c/v2/admission.json',
  'audit/topic-c/v2/measurement/admission.json','audit/topic-c/v2/measurement/packet/results.json']
 for n in unchanged:need((root/n).read_bytes()==subprocess.check_output(['git','show',BASE+':'+n],cwd=root),'unchanged underlying publication '+n)
 view=read(root/B/'costs/view_data.json');locators=[]
 for node in view['nodes']:
  for l in node.get('current_public_locators',[]):
   p=Path(l['path']);need(not p.is_absolute() and '..' not in p.parts,'safe public proof path')
   text=(root/p).read_text();passage=text[l['start_codepoint']:l['end_codepoint_exclusive']]
   need(sha(passage.encode())==l['sha256_utf8'],'exact current proof passage');locators.append(l)
 for key,d in view['documents'].items():
  if d.get('path'):need((root/d['path']).is_file(),'public document link')
 js=(root/B/'costs/explorer.js').read_text();need('href="../../../../../${' in js,'correct five-level public explorer routing')
 links=[];docs=['README.rst','audit/completion.rst',B+'README.rst']
 for n in docs:
  for raw in re.findall(r'<([^>]+)>`_',(root/n).read_text(),re.S):
   url=''.join(raw.split())
   if re.match(r'^[a-zA-Z]+:',url) or url.startswith('#'):continue
   need(((root/n).parent/url.split('#')[0]).exists(),'working local reader link '+n+' -> '+url);links.append(dict(document=n,target=url))
 need(view['measurement']['complete_common_and_programs_prepaid_for_conditional_factors'] is True and view['measurement']['all_four_applications_charged'] is True,'complete conditional boundary')
 need(view['measurement']['common_theory_discount_for_other_topics'] is False,'no cross-topic free umbrella')
 build=read(root/B/'publication_replay/protocol_build.json')['papers']
 need(len(build)==1 and build[0]['diagnostics']==[] and build[0]['status']=='compiled' and
      build[0]['tex_sha256']==sha((root/'audit/protocol.tex').read_bytes()) and
      build[0]['pdf_sha256']==sha((root/'audit/protocol.pdf').read_bytes()),'exact clean protocol compilation')
 rootrecord=read(root/B/'root_integration.json');need(rootrecord['fresh_checker_return']==[270,85] and rootrecord['copied_frozen_exports']==133 and rootrecord['fresh_public_DOM_views']==180 and rootrecord['protocol_build_diagnostics']==[],'bounded root replay record')
 controls=[]
 with tempfile.TemporaryDirectory(prefix='c-dag-integration-') as t:
  temp=Path(t)
  for n in {r['path'] for r in admission['artifacts']}|{B+'admission.json'}:
   out=temp/n;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/n,out)
  v.ROOT=temp
  for name,n in [('viewer_bytes',B+'costs/explorer.html'),('logical_review_bytes',B+'logical_review/review.json'),('frozen_partition_bytes',B+'costs/partition.json')]:
   p=temp/n;b=p.read_bytes();p.write_bytes(b+b'\n')
   try:v.check_topic_c_dag()
   except (ValueError,KeyError) as e:controls.append(dict(name=name,mode='temporary copied file mutation',rejected=True,reason=str(e)))
   else:raise ValueError('accepted corrupt artifact '+name)
   p.write_bytes(b)
 v.ROOT=root;actual=v.load
 summary_fields=['source_contracts','source_rows','logical_nodes','exclusive_owners','output_closures','primary_written_denominator','primary_program_inclusive_denominator','primary_raw_program_alternative_denominator']
 cases=['summary:'+k for k in summary_fields]+['deny_review','wrong_review_edition','invent_missing_cost','new_credit','claim_browser','omit_owned_character','owner_overlap','omit_prerequisite','omit_application_context','invent_historical_curve','change_conditional_cost','wrong_public_locator']
 for name in cases:
  overrides={};ad=copy.deepcopy(admission)
  def edit(n):
   if n not in overrides:overrides[n]=actual(n)
   return overrides[n]
  if name.startswith('summary:'):ad[name.split(':',1)[1]]=-1
  elif name=='deny_review':ad['independent_cost_and_reader_review_accepted']=False
  elif name=='wrong_review_edition':edit(B+'independent_review/review.json')['accepted_author_manifest']['sha256']='0'*64
  elif name=='invent_missing_cost':ad['L108_original_pdf_cost']=0
  elif name=='new_credit':ad['new_source_credit']=1
  elif name=='claim_browser':ad['real_browser_layout_test']=True
  elif name=='omit_owned_character':
   w=edit(B+'costs/weights.json');next(iter(w['owner_costs'].values()))['calibrated_selected']['NFC']['characters_without_whitespace']-=1
  elif name=='owner_overlap':
   p=edit(B+'costs/partition.json');next(iter(p['documents'].values()))['variants']['calibrated_selected']['spans'][1]['start']-=1
  elif name=='omit_prerequisite':
   w=edit(B+'costs/weights.json');next(r for r in w['source_contract_closures'] if r['replacement']['logical_nodes'])['replacement']['logical_nodes'].pop()
  elif name=='omit_application_context':edit(B+'costs/acquisition.json')['stages'][-1]['complete_local_owner_ids'].pop()
  elif name=='invent_historical_curve':edit(B+'costs/acquisition.json')['historical_complete_numeric_curve']=[]
  elif name=='change_conditional_cost':edit(B+'costs/view_data.json')['measurement']['complete_common_and_programs_prepaid_for_conditional_factors']=False
  elif name=='wrong_public_locator':next(n for n in edit(B+'costs/view_data.json')['nodes'] if n.get('current_public_locators'))['current_public_locators'][0]['start_codepoint']+=1
  overrides[B+'admission.json']=ad;v.load=lambda p:copy.deepcopy(overrides[p]) if p in overrides else actual(p)
  try:v.check_topic_c_dag()
  except (ValueError,KeyError,IndexError) as e:controls.append(dict(name=name,mode='in-memory semantic guard isolation',rejected=True,reason=str(e)))
  else:controls.append(dict(name=name,rejected=False))
  finally:v.load=actual
 need(all(r['rejected'] for r in controls),'all corruptions rejected '+repr([r for r in controls if not r['rejected']]))
 added=subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=ACMR',BASE,'--','*.md'],cwd=root,text=True);need(not added.strip(),'no working Markdown published')
 whitespace=subprocess.run(['git','diff','--cached','--check',BASE],cwd=root,text=True,capture_output=True)
 warnings=re.findall(r'^([^:\n]+):\d+: trailing whitespace\.$',whitespace.stdout,re.M)
 allowed={B+folder+'/'+name for folder in ['costs','costs_previous'] for name in ['acquisition.svg','default_graph.svg','owner_costs.csv']}
 need(set(warnings)==allowed,'only exact frozen matplotlib SVG/CSV whitespace exceptions')
 exception_rows=[dict(path=p,occurrences=warnings.count(p),sha256=sha((root/p).read_bytes()),
   reason='Preserved byte-exact generated SVG formatting or CSV CRLF; not rewritten after freeze.') for p in sorted(allowed)]
 files=['scripts/verify_snapshot.py','README.rst','audit/completion.rst','audit/work_queue.json','audit/protocol.tex','audit/protocol.pdf',B+'admission.json',B+'README.rst',B+'root_integration.json',B+'publication_replay/viewer.json',B+'publication_replay/protocol_build.json']
 report=dict(status='PASS_BOUNDED_C_DAG_PUBLICATION_INTEGRATION',baseline_commit=BASE,admission_sha256=ADMISSION,copies=copies,
  frozen_exports=133,admission_artifacts=len(admission['artifacts']),positive_checker=[270,85],old_non_main_functions_preserved=27,
  prior_main_order_preserved=True,underlying_catalogue_registry_proofs_and_counts_preserved=unchanged,
  exact_public_proof_locators=len(locators),unique_public_proof_paths=sorted({l['path'] for l in locators}),links_checked=links,
  controls=controls,frozen_generated_whitespace_exceptions=exception_rows,bound_public_files=[dict(path=n,bytes=(root/n).stat().st_size,sha256=sha((root/n).read_bytes())) for n in files],
  conflict_disclosure='Reviewer authored the cost/reader packet. This reviews root publication integration only; independent ownership/reader acceptance is reused from enumeration_volume, and the already frozen logical review is reused.',
  primary_extraction_math_GAP_Lean_or_full_cost_review_repeated=False,new_source_credit=0,new_question_credit=0,new_formal_credit=0,
  combined_factor=None,node_ratio=None,public_files_modified_by_reviewer=False)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(status=report['status'],copies=133,controls=len(controls),proof_locators=len(locators),checker=[270,85])))
if __name__=='__main__':main()
