#!/usr/bin/env python3
"""Bounded exact-delta check; mathematical acceptance belongs to the reviewer."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
PIN='681c011dddc78fd82852d5b19bfbcdde67cac86d4ced6aedae8005b2c6d39db3'
def need(b,s):
 if not b: raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def rec(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def load(n):return json.loads((R/n).read_text())
def audit():
 need(sha((R/'previous_manifest.json').read_bytes())==PIN,'predecessor pin')
 old=load('previous_manifest.json');delta=load('precision_delta.json');oldrows={x['path']:x for x in old['exports']}
 need(delta['previous_manifest_sha256']==PIN,'delta pin')
 changed=[]
 for n,row in oldrows.items():
  if rec(R/n)!={k:row[k] for k in ['bytes','sha256']}:changed.append(n)
 need(set(changed)==set(delta['permitted_modified_predecessor_exports']),'unexpected changed predecessor export')
 for n in ['primitive_branch.tex','source_map.json']:
  need(rec(R/'previous'/n)=={k:oldrows[n][k] for k in ['bytes','sha256']},'old fragment binding')
 a=(R/'previous/primitive_branch.tex').read_text();b=(R/'primitive_branch.tex').read_text()
 need(a.count(delta['old_fragment'])==1 and b==a.replace(delta['old_fragment'],delta['new_fragment']),'literal precision replacement')
 sm0=load('previous/source_map.json');sm1=load('source_map.json')
 need(sm0['rows']==sm1['rows'],'source dispositions changed')
 q0=sm0.pop('proof_contexts');q1=sm1.pop('proof_contexts');need(sm0==sm1,'source map metadata changed')
 need([q['id'] for q in q0 if q!=next(x for x in q1 if x['id']==q['id'])]==['PR.1','PR.2'],'unexpected proof span delta')
 for q in q1:
  t=(R/q['file']).read_text();z=t[q['start_codepoint']:q['end_codepoint_exclusive']]
  need(sha(z.encode())==q['sha256_utf8'],'proof span hash')
 need(load('scope.json')['source_rows']==58 and load('scope.json')['new_Lean_declarations']==0,'scope')
 return {'status':'PASS_EXACT_PRECISION_DELTA','previous_exports':len(oldrows),'unchanged_exports':len(oldrows)-len(changed),'changed_exports':changed,'source_dispositions_identical':58,'changed_proof_contexts':['PR.1','PR.2'],'mathematical_programs_changed':0,'finite_results_changed':False,'new_credits':0}
if __name__=='__main__':print(json.dumps(audit(),indent=2))
