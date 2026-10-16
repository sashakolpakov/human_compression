#!/usr/bin/env python3
"""Public replay of the reviewed fixed-edition counterexample and its acceptance chain."""
import argparse,copy,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent
AUTHOR='225b0b354870d9f89669de3e4eb4d0458b6468c0ba78e0feffccd62163a4ee93'
REVIEW='dc264adb17bee3736757fa44e7150380a16fea5aee0ecd40063537db661ee250'
ADDENDUM='91933165146a3071d356ad79d6c34584f1005766c96d136b060fb510f388f428'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inside(root,name):
 p=PurePosixPath(name);need(not p.is_absolute()and'..'not in p.parts,'unsafe public route');q=(root/p).resolve();need(q.is_relative_to(root.resolve()),'public route escapes root');return q
def pin(p,row):need(p.is_file()and p.stat().st_size==row['bytes']and sha(p)==row['sha256'],'missing or changed '+str(p))
def semantics(s,ad):
 need(s['original_id']=='F003'and s['source_edition']=='arXiv:2010.04080v1, 8 October 2020'and s['target']=='Theorem 1.1, physical page 1','source scope')
 need(s['counterexample']==dict(group='Sz(32768)',rank=4,type=[31,31,25],face_groups=['Sz(32)','Sz(32)'],face_intersection_order=31),'construction scope')
 need(s['open_conjecture_credit']==0 and s['compression_factor']is None and not s['whole_source_formalized'],'source overclaim')
 need(ad['classification']=='PRINCIPAL_STATEMENT_REFUTATION_SEPARATE_FROM_COMPRESSION_OF_VALID_RESULTS','refutation classification')
 for key in ['new_original_credit','new_question_credit','new_Lean_credit']:need(ad[key]==0,'credit '+key)
 for key in ['later_edition_claim','historical_priority_claim','absence_of_errata_claim','journal_fulltext_claim','root_is_distinct_reviewer','whole_source_formalized','current_catalogue_mutated']:need(ad[key]is False,'overclaim '+key)
 need(ad['compression_factor']is ad['software_inclusive_factor']is None,'no compression factor')
def main(a):
 need(__debug__,'optimized Python is not permitted')
 repo=a.repo.resolve();a.out=a.out.resolve();need(not a.out.is_relative_to(HERE),'output must be outside frozen correction')
 a.out.mkdir(parents=True,exist_ok=False)
 if(HERE/'manifest.json').is_file():
  for row in load(HERE/'manifest.json')['exports']:pin(inside(HERE,row['path']),row)
 t=load(HERE/'transport.json');base=PurePosixPath(t['base_public_path']);mapping={}
 documentary=[]
 for r in t['files']:
  logical=r['logical_path'];need(logical not in mapping,'duplicate logical binding')
  if r['transport']=='PRIMARY_SOURCE_HASH_ONLY':
   need(logical.startswith('sources/')or any('/'+part+'/'in '/'+logical for part in ['LMO','Spiga','coordinates']),'undisclosed omitted proof')
   documentary.append(r);mapping[logical]=None;continue
  need(r['transport']in ['EXACT_PUBLIC_COPY','EXISTING_PUBLIC'],'transport kind')
  public=PurePosixPath(r['public_path'])
  p=inside(HERE,str(public.relative_to(base)))if r['transport']=='EXACT_PUBLIC_COPY'else inside(repo,r['public_path'])
  pin(p,r);mapping[logical]=p
 need(len(t['files'])==116 and len(documentary)==11 and len(t['complete_packets'])==7,'complete public transport boundary')
 exports=0
 for packet in t['complete_packets']:
  directory=inside(HERE,str(PurePosixPath(packet['public_directory']).relative_to(base)))
  need(sha(directory/'manifest.json')==packet['manifest_sha256'],'frozen manifest')
  m=load(directory/'manifest.json');need(len(m['exports'])==packet['exports'],'full export count')
  for row in m['exports']:pin(inside(directory,row['path']),row);exports+=1
 # Direct construction bindings are checked publicly, except the declared primary materials.
 deps=load(HERE/'proof/dependencies.json')['bindings'];bound=0;primary=0
 for r in deps:
  need(r['path']in mapping,'missing direct proof/review route')
  p=mapping[r['path']]
  if p is None:primary+=1
  else:pin(p,r);bound+=1
 need(len(deps)==45 and primary==6,'exact v2 dependency boundary')
 need(sha(HERE/'proof/manifest.json')==AUTHOR and sha(HERE/'independent_review/manifest.json')==REVIEW and sha(HERE/'v2_addendum/manifest.json')==ADDENDUM,'accepted editions')
 root=load(HERE/'root_adoption/adoption.json')
 need(root['author_manifest']['sha256']==AUTHOR and root['distinct_full_review']['sha256']==REVIEW and root['distinct_v2_addendum']['sha256']==ADDENDUM,'root adoption chain')
 need(root['status']=='ROOT_ADOPTS_DISTINCT_EXPLICIT_COUNTEREXAMPLE'and root['classification']=='PRINCIPAL_STATEMENT_REFUTATION_SEPARATE_FROM_COMPRESSION_OF_VALID_RESULTS','root scientific scope')
 src=load(HERE/'source_statement.json');ad=load(HERE/'admission_proposal.json');semantics(src,ad)
 controls=[]
 for key,value in [('new_original_credit',1),('new_question_credit',1),('new_Lean_credit',1),('later_edition_claim',True),('historical_priority_claim',True),('absence_of_errata_claim',True),('journal_fulltext_claim',True),('root_is_distinct_reviewer',True),('whole_source_formalized',True),('compression_factor',1.0),('classification','RECOVERED_TRUE_THEOREM')]:
  bad=copy.deepcopy(ad);bad[key]=value
  try:semantics(src,bad)
  except ValueError:controls.append(key)
  else:raise ValueError('accepted negative control '+key)
 old=HERE/'history/author-v1';new=HERE/'proof'
 atex=(old/'rank4_counterexample.tex').read_text();btex=(new/'rank4_counterexample.tex').read_text()
 need(atex.count(r'arXiv:1706.05697v1 (2017), \S2.')==1,'exact old bibliography locator')
 need(btex==atex.replace(r'arXiv:1706.05697v1 (2017), \S2.',r'arXiv:1706.05697v1 (2017), \S1.'),'only reviewed manuscript delta')
 for name in ['check.py','check_arithmetic.py','expected_arithmetic.json','program_inventory.json']:need((old/name).read_bytes()==(new/name).read_bytes(),'arithmetic changed after review')
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 command=[sys.executable,'-B',str(new/'check.py'),'--out',str(a.out/'author')]
 if a.render:command.append('--render')
 result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,text=True,timeout=120)
 (a.out/'author.stdout').write_text(result.stdout);(a.out/'author.stderr').write_text(result.stderr)
 need(result.returncode==0 and not result.stderr,'exact author replay')
 ar=load(a.out/'author/report.json');need(ar['status']=='PASS'and ar['rotation_orders']==dict(a=31,b=31,c=25,ab=2,bc=2,abc=2)and ar['source_equation13_residual']==28331,'exact arithmetic result')
 gap=a.gap or shutil.which('gap');need(gap is not None,'GAP executable required for independent reconstruction')
 code=HERE/'independent_review/independent.g';before=sha(code)
 result=subprocess.run([str(gap),'-q','-b',str(code)],cwd=a.out,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,timeout=120)
 (a.out/'independent_gap.stdout').write_bytes(result.stdout);(a.out/'independent_gap.stderr').write_bytes(result.stderr)
 need(result.returncode==0 and not result.stderr and sha(code)==before,'independent GAP execution')
 expected=(HERE/'independent_review/independent_gap_stdout.log').read_text().split();need(result.stdout.decode().split()==expected,'independent GAP output')
 need(result.stdout.decode().count('COMPLETE_INDEPENDENT_GAP_RECONSTRUCTION')==1,'independent completion marker')
 report=dict(status='PASS_PUBLIC_CORRECTION_REPLAY',classification=ad['classification'],source_edition=src['source_edition'],logical_bindings=len(mapping),complete_packets=7,complete_packet_exports=exports,primary_hash_only=len(documentary),v2_nonprimary_bindings=bound,scope_controls=controls,author_replay=ar,independent_GAP=True,face_orders=[32537600,32537600],source_equation13_residual=28331,private_source_files_read=False,private_mathematical_proof_fallback=False,discovery_search_repeated=False,whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,compression_factor=None,catalogue_modified=False)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=HERE.parents[2]);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--gap',type=Path);ap.add_argument('--render',action='store_true');main(ap.parse_args())
