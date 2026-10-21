#!/usr/bin/env python3
"""Bounded independent review of root's publication wiring, not D's authored mathematics."""
import argparse,ast,copy,hashlib,importlib.util,json,re,shutil,subprocess,tempfile
from pathlib import Path

def need(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();r=a.public_root.resolve();s=a.study_root.resolve();need(not a.out.exists(),'fresh report')
 verifier=r/'scripts/verify_snapshot.py';text=verifier.read_text();prior=subprocess.check_output(['git','show','3bfbd6f:scripts/verify_snapshot.py'],cwd=r).decode()
 def funcs(x):return {n.name:n for n in ast.parse(x).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
 old,new=funcs(prior),funcs(text);unchanged=[]
 for name,fn in old.items():
  if name=='main':continue
  need(ast.dump(fn,include_attributes=False)==ast.dump(new[name],include_attributes=False),'prior verifier changed '+name);unchanged.append(name)
 need(set(new)-set(old)=={'check_topic_d_proofs'},'only new verifier function')
 mainbody=[];removed=[]
 for n in new['main'].body:
  if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='check_topic_d_proofs':removed.append('new-call')
  elif isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='print' and 'Topic D preserves' in ast.unparse(n):removed.append('new-print')
  else:mainbody.append(n)
 m=copy.deepcopy(new['main']);m.body=mainbody;need(ast.dump(m,include_attributes=False)==ast.dump(old['main'],include_attributes=False) and removed==['new-call','new-print'],'main only adds D call and summary')
 spec=importlib.util.spec_from_file_location('snapshot_d_integration',verifier);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 need(mod.check_topic_d_proofs()==(37,10),'new public verifier passes')
 admission=json.loads((r/'audit/topic-d/v2/admission.json').read_text());need(sha((r/'audit/topic-d/v2/admission.json').read_bytes())=='65bcfb731a5cab716c6703964fba6e10bb318a2cab91b62107358ac7884ff1ae','exact admission under review')
 mappings=[('topic_D_volume','papers/topic-d/v2',61),('topic_D_volume_independent_review','audit/topic-d/v2/independent_review',18),('topic_D_root_adoption','audit/topic-d/v2/root_adoption',3)]
 copied=[]
 for private,public,count in mappings:
  if not (s/private).exists():
   candidates=[p.parent for p in s.glob('*/manifest.json') if sha(p.read_bytes())==sha((r/public/'manifest.json').read_bytes())];need(len(candidates)==1,'find exact root adoption directory');source=candidates[0]
  else:source=s/private
  need((source/'manifest.json').read_bytes()==(r/public/'manifest.json').read_bytes(),'manifest identical '+public);manifest=json.loads((source/'manifest.json').read_text());need(len(manifest['exports'])==count,'export inventory '+public)
  for x in manifest['exports']:need((source/x['path']).read_bytes()==(r/public/x['path']).read_bytes(),'exact relocated bytes '+public+'/'+x['path'])
  copied.append(dict(private=str(source),public=public,exports=count,byte_identical=True))
 need(len(admission['artifacts'])==90,'ninety admitted artifacts')
 for x in admission['artifacts']:
  b=(r/x['path']).read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'complete admission hash '+x['path'])
 # Inventory local RST links in changed/new public readers; no network or primary acquisition.
 docs=['README.rst','audit/completion.rst','papers/topic-d/v2/PUBLICATION.rst','audit/topic-d/v2/root_adoption/README.rst']
 links=[]
 for f in docs:
  t=(r/f).read_text()
  for raw in re.findall(r'<([^>]+)>`_',t,re.S):
   link=''.join(raw.split())
   if re.match(r'^[a-zA-Z]+:',link) or link.startswith('#'):continue
   target=(r/f).parent/link.split('#')[0];need(target.exists(),'reader link '+f+' -> '+link);links.append(dict(document=f,target=link))
 # Actual byte mutations in an isolated copy exercise the immutable packet binding.
 controls=[]
 with tempfile.TemporaryDirectory(prefix='topic_D_publication_control_') as td:
  root=Path(td);paths={x['path'] for x in admission['artifacts']}|{'audit/topic-d/v2/admission.json','papers/catalogue.json'}
  for p in paths:
   dest=root/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(r/p,dest)
  mod.ROOT=root
  for label,path in [('scientific_bytes','papers/topic-d/v2/sections/02-support.tex'),('required_program_bytes','papers/topic-d/v2/programs/phase5_j2_search.g'),('independent_review_bytes','audit/topic-d/v2/independent_review/review.json')]:
   p=root/path;b=p.read_bytes();p.write_bytes(b+b'\n')
   try:mod.check_topic_d_proofs()
   except (ValueError,KeyError) as exc:controls.append(dict(name=label,mode='isolated file mutation',rejected=True,reason=str(exc)))
   else:raise ValueError('accepted altered bytes '+label)
   p.write_bytes(b)
 mod.ROOT=r;original_load=mod.load
 # In-memory metadata mutations bypass no mathematics; they isolate the new semantic guards.
 for label in ['omit_clause','inflate_formal_scope','invent_factor','erase_L104_exclusion','omit_tex_input']:
  overrides={};ad=copy.deepcopy(admission);sc=original_load('papers/topic-d/v2/scope.json');cat=original_load('papers/catalogue.json')
  if label=='omit_clause':sc['contracts'].pop();overrides['papers/topic-d/v2/scope.json']=sc
  elif label=='inflate_formal_scope':ad['fresh_lean_declarations']=28;ad['later_support_formal_packet_included']=True
  elif label=='invent_factor':ad['compression_ratio']=2.0
  elif label=='erase_L104_exclusion':
   oldstatus=sc['contracts'][-1]['current_status'];sc['contracts'][-1]['current_status']='full_principal';ad['row_status_counts'][oldstatus]-=1;ad['row_status_counts']['full_principal']+=1;overrides['papers/topic-d/v2/scope.json']=sc
  else:
   entry=next(x for x in cat['new_editions'] if x['id']=='topic-d/v2/umbrella');entry['tex_inputs'].pop();next(x for x in ad['catalogue_entries'] if x['id']=='topic-d/v2/umbrella')['tex_inputs'].pop();overrides['papers/catalogue.json']=cat
  overrides['audit/topic-d/v2/admission.json']=ad
  mod.load=lambda path:copy.deepcopy(overrides[path]) if path in overrides else original_load(path)
  try:mod.check_topic_d_proofs()
  except (ValueError,KeyError) as exc:controls.append(dict(name=label,mode='metadata guard isolation; original file bindings left intact',rejected=True,reason=str(exc)))
  else:raise ValueError('accepted metadata corruption '+label)
  finally:mod.load=original_load
 files=['scripts/verify_snapshot.py','README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/work_queue.json','papers/catalogue.json','papers/topic-d/v2/PUBLICATION.rst','audit/topic-d/v2/admission.json','audit/topic-d/v2/root_integration.json']
 report=dict(status='PASS_BOUNDED_PUBLICATION_INTEGRATION',baseline_commit='3bfbd6f1b54baf5f4674ba243011cc552b6eca81',unchanged_non_main_functions=unchanged,new_main_statements=removed,public_verifier_result=[37,10],exact_packet_copies=copied,admission_artifacts=90,checked_local_links=links,controls=controls,bound_artifacts=[dict(path=p,bytes=(r/p).stat().st_size,sha256=sha((r/p).read_bytes())) for p in files],scope='Review of root-created copying, catalogue, metadata, documentation and verifier wiring. This reviewer authored D mathematics; this is not a second independent mathematical review. The independent mathematical acceptance is e5069edb.',new_source_credit=0,new_question_credit=0,compression_ratio=None)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status=report['status'],prior_functions=len(unchanged),copies=[x['exports'] for x in copied],links=len(links),controls=len(controls))))
if __name__=='__main__':main()
