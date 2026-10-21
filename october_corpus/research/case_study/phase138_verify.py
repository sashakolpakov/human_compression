#!/usr/bin/env python3
"""Portable read-only binding, derivation-span, complete-cost and rebuild checks.
This verifies documentary continuity, not mathematical validity or Lean proofs.
"""
import argparse,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def file(rec):
 b=(ROOT/rec['path']).read_bytes();require(sha(b)==rec['sha256'],'changed input '+rec['path'])
 for k in ['utf8_bytes','bytes']:
  if k in rec:require(len(b)==rec[k],'changed length '+rec['path'])
 return b

def span(text,b,name):
 a=b['start_codepoint'];z=b['end_codepoint_exclusive'];t=text[a:z]
 require(0<=a<z<=len(text),'bad span '+name);require(sha(t.encode())==b['sha256_utf8'],'changed span '+name)
 if 'utf8_bytes' in b:require(len(t.encode())==b['utf8_bytes'],'span bytes '+name)
 if 'plain_NFC_whitespace_tokens' in b:require(len(unicodedata.normalize('NFC',t).split())==b['plain_NFC_whitespace_tokens'],'span count '+name)
 return t

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--rebuild',action='store_true');ap.add_argument('--primary-check',action='store_true');ap.add_argument('--visual-assets-check',action='store_true');a=ap.parse_args()
 if a.output.exists() or a.output.is_symlink():raise SystemExit('Refusing existing output')
 m=json.loads((ROOT/'phase138_manifest.json').read_text())
 for b in m['files']+m['required_shared_inputs']:file(b)
 l=json.loads((ROOT/'phase138_module_A_v2_ledger.json').read_text());uc=json.loads((ROOT/'phase138_umbrella_v3_contracts.json').read_text());cost=json.loads((ROOT/'phase138_cost_checkpoint.json').read_text());visual=json.loads((ROOT/'phase138_visual_review.json').read_text())
 u=file(uc['manuscript']).decode();app=file(l['application']).decode()
 require(len(l['contract_rows'])==50 and len(set(x['id'] for x in l['contract_rows']))==50,'exact source ledger rows')
 require(l['source_bundle']==['L032','L035','F013','F016','N009','L034'],'source bundle')
 require(len(uc['contracts'])==30,'shared theorem count')
 for x in uc['contracts']:
  t=span(u,x['statement_binding'],x['id']+' statement');span(u,x['complete_proof_binding'],x['id']+' proof')
  require(t==x['statement_exact_markdown'],'statement text '+x['id'])
 for x in l['contract_rows']:
  require(x['proof_locations'],'empty source proof binding')
  for b in x['proof_locations']:span(app,b,x['id'])
 for x in l['auxiliary_records']:
  for b in x['proof_locations']:span(app,b,x['source_reference'])
 old_u=(ROOT/'phase123_umbrella_manuscript_v2.md').read_text();old_c=json.loads((ROOT/'phase123_umbrella_v2_contracts.json').read_text())
 for x in old_c['contracts']:
  for k in ['statement_binding','complete_proof_binding']:
   t=span(old_u,x[k],x['id']);require(u.count(t)==1,'lost old U proof '+x['id'])
 require('every marked generator in every attached group is an involution' in u,'missing corrected involutivity hypothesis')
 require('This is a sufficient condition, not an equivalent reformulation.' in u,'alternative hypothesis scope')
 require('That pairing is erroneous for general s' in app,'missing N009 correction')
 programs=[file(x) for x in l['certificate_artifacts']];code=sum(map(len,programs))
 require(code==56375,'full program cost');require(len(u.encode())+len(app.encode())+code==cost['whole_U_A_four_artifact_bytes']==208861,'complete proof cost')
 require(cost['source_ratio'] is None,'unapproved ratio')
 for b in cost['baselines'].values():require(b['diff']['gross_added_bytes']-b['diff']['gross_removed_bytes']==b['diff']['signed_net_bytes']==cost['whole_U_A_four_artifact_bytes']-b['whole_package_bytes'],'baseline arithmetic')
 require(cost['baselines']['five_source_with_N009_correction']['whole_package_bytes']==196962,'corrected five-source cost')
 require(cost['baselines']['six_source_additive_with_both_corrections']['whole_package_bytes']==214717,'corrected six-source cost')
 for module,folder in [('U','phase138_render_U'),('A','phase138_render_A_v2')]:
  d=json.loads((ROOT/folder/'render_report.json').read_text());text=u if module=='U' else app
  require(d['manuscript']['sha256']==sha(text.encode()),'rendered wrong edition')
  require((ROOT/folder/'source.md').read_text()==text,'rendering omitted source text')
  require(d['pages']==visual[module]['pages'],'page count');require(d['AST_preserved'],'AST preservation')
  require(not any(re.search('Overfull|Missing character|Missing glyph',x,re.I) for x in d['diagnostics']),'unresolved rendering warning')
  file(visual[module]['PDF'])
 primaries=0
 if a.primary_check:
  for x in l['source_versions_and_measurement_boundaries'].values():
   if 'pdf_binding' in x:file(x['pdf_binding']);primaries+=1
   else:
    for b in x['private_primary_bindings']:file(b);primaries+=1
 if a.visual_assets_check:
  for b in visual['authored_pages']+visual['primary_visual_assets']:file(b)
 rebuilt=False
 if a.rebuild:
  with tempfile.TemporaryDirectory(prefix='phase138-verify-') as temp:
   root=Path(temp)
   for script,folder,names in [('phase138_build.py','manuscripts',['phase138_umbrella_v3.md','phase138_module_A_v2.md']),('phase138_checkpoint.py','ledgers',['phase138_umbrella_v3_contracts.json','phase138_module_A_v2_ledger.json','phase138_cost_checkpoint.json'])]:
    result=subprocess.run([sys.executable,'-B','-O',str(ROOT/script),'--output-dir',str(root/folder)],capture_output=True,text=True)
    require(result.returncode==0,'rebuild failed '+script+' '+result.stderr)
    for name in names:require((root/folder/name).read_bytes()==(ROOT/name).read_bytes(),'rebuild differs '+name)
   rebuilt=True
 report={'status':'PASS_documentary_integrity_not_independent_mathematical_admission','manifest_sha256':sha((ROOT/'phase138_manifest.json').read_bytes()),'export_files_checked':len(m['files']),'shared_inputs_checked':len(m['required_shared_inputs']),'source_rows':50,'U_theorems':30,'prior_U_statement_proof_pairs_preserved':28,'complete_U_A_four_artifact_bytes':208861,'source_ratio':None,'U_pages':16,'A_pages':24,'private_primary_files_checked':primaries,'private_visual_hashes_checked':a.visual_assets_check,'exact_builder_and_checkpoint_replay':rebuilt,'fresh_GAP_or_Lean_replay':False}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
