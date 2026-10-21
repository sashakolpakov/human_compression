#!/usr/bin/env python3
"""Read-only Module B integrity, source-anchor and accounting replay.

This verifies documentary bindings, not the mathematical truth of the proofs.
No private source is needed unless --primary-check is expressly supplied.
"""
import argparse,hashlib,json,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def require(test,msg):
 if not test:raise RuntimeError(msg)
def check_file(rec):
 p=ROOT/rec['path'];b=p.read_bytes()
 require(sha(b)==rec['sha256'],'changed input: '+rec['path'])
 if 'bytes' in rec:require(len(b)==rec['bytes'],'changed length: '+rec['path'])
 return b
def check_span(text,rec,name):
 a=rec['start_codepoint'];b=rec['end_codepoint_exclusive'];s=text[a:b]
 require(0<=a<b<=len(text),'invalid span: '+name)
 require(sha(s.encode())==rec['sha256_utf8'],'changed span: '+name)
 if 'bytes' in rec:require(len(s.encode())==rec['bytes'],'span bytes: '+name)
 if 'NFC_whitespace_tokens' in rec:require(len(unicodedata.normalize('NFC',s).split())==rec['NFC_whitespace_tokens'],'span count: '+name)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--primary-check',action='store_true');ap.add_argument('--visual-assets-check',action='store_true');a=ap.parse_args()
 if a.output.exists():raise SystemExit('Refusing existing output')
 m=json.loads((ROOT/'phase132_module_B_manifest.json').read_text())
 for x in m['files']+m['required_shared_inputs']:check_file(x)
 d=json.loads((ROOT/'phase132_module_B_checkpoint03.json').read_text());s=check_file(d['manuscript']).decode();ub=check_file(d['umbrella'])
 require(len(d['targets'])==30,'contract row count')
 require(len(d['nodes'])==22,'proof node count')
 for k,x in d['nodes'].items():
  check_span(s,x['span'],k)
  for dep in x['direct_dependencies']:
   require(dep in d['nodes'] or dep in d['umbrella_used_contracts'] or dep.startswith('retained:'),'unresolved declared dependency: '+dep)
 for x in d['targets']:
  require(x['application_nodes'],'empty source adapter')
  for k in x['application_nodes']:require(k in d['nodes'],'unbound adapter '+k)
 us=ub.decode()
 for k,x in d['umbrella_used_contracts'].items():
  check_span(us,x['statement_binding'],k+' statement');check_span(us,x['complete_proof_binding'],k+' proof')
 c=d['cost'];require(c['application_raw_utf8_bytes']==len(s.encode()),'application accounting')
 require(c['application_raw_NFC_whitespace_tokens']==len(unicodedata.normalize('NFC',s).split()),'application token count')
 require(c['whole_umbrella_raw_utf8_bytes']==len(ub),'umbrella accounting')
 require(c['complete_conservative_U_plus_B_raw_bytes']==len(s.encode())+len(ub),'complete accounting')
 require(c['required_external_proof_programs']==[] and c['complete_source_ratio'] is None,'scope changed')
 primary=0
 if a.primary_check:
  intake=json.loads((ROOT/'phase132_module_B_intake.json').read_text())
  for x in intake['source_files']:check_file(x)
  for x in d['targets']:
   text=(ROOT/x['source_file']).read_text();check_span(text,x['source_span'],x['paper']+':'+x['adapter']);primary+=1
  for x in d['source_complexity_inventory']:
   text=check_file(x['text_file']).decode();check_span(text,x['body_span'],x['source_id']+' inventory')
 v=json.loads((ROOT/'phase132_module_B_visual_review.json').read_text())
 if a.visual_assets_check:
  for x in v['authored_pages']:check_file(x)
  for x in v['primary_visual_assets']:check_file(x)
 report={'status':'PASS_documentary_replay_not_mathematical_admission','manifest_sha256':sha((ROOT/'phase132_module_B_manifest.json').read_bytes()),'export_files_checked':len(m['files']),'shared_inputs_checked':len(m['required_shared_inputs']),'source_anchors_checked':primary,'proof_nodes_checked':len(d['nodes']),'source_rows':len(d['targets']),'application_bytes':len(s.encode()),'complete_U_plus_B_bytes':len(s.encode())+len(ub),'authored_pages':v['page_count'],'visual_assets_hash_checked':a.visual_assets_check,'source_ratio':None,'complete_Lean_claim':False}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
