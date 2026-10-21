#!/usr/bin/env python3
"""Integrity and full-charge check for the typed-Helly/L034 author candidate."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(x,m):
 if not x:raise RuntimeError(m)
def check(z):
 p=R/z['path'];require(p.is_file(),'Missing '+z['path']);require(sha(p)==z['sha256'],'Changed '+z['path'])
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--primary-check',action='store_true');a=p.parse_args()
 require(not a.output.exists(),'Refusing existing output')
 m=json.loads((R/'phase130_manifest.json').read_text())
 for z in m['exports']+m['required_shared_bindings']:check(z)
 q=json.loads((R/'phase130_intake.json').read_text());s=(R/'phase130_typed_helly_L034.md').read_text()
 for z in q['proof_sections']:
  t=s[z['start_codepoint']:z['end_codepoint_exclusive']];require(hashlib.sha256(t.encode()).hexdigest()==z['sha256_utf8'],'Proof span')
 if a.primary_check:
  for z in q['private_primary_bindings']:check(z)
 require(q['source_principal_contract']['status']=='corrected_complete_principal_construction_candidate','Contract scope')
 require(len(q['source_principal_contract']['clauses'])==6,'Six theorem clauses')
 require(q['conjecture_3_3_solved'] is False and q['full_Lean_formalization'] is False and q['ratio'] is None,'Scope flags')
 base=json.loads((R/'phase117_two_group_application_checkpoint04.json').read_text())['complete_U_plus_A_raw_bytes']
 require(base==190995,'Prior full U+A cost changed')
 require(q['complete_charged_raw_bytes']==base+len(s.encode())==206349,'Complete added proof cost')
 result=dict(status='PASS_author_integrity_not_independent_mathematical_review',manifest_sha256=sha(R/'phase130_manifest.json'),
  new_body_bytes=len(s.encode()),complete_U_A_extension_raw_bytes=base+len(s.encode()),source_principal_clauses=6,
  primary_bytes_checked=a.primary_check,ratio=None,conjecture_solved=False,new_computation_required_for_parameter_proof=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
