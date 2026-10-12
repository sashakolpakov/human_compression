#!/usr/bin/env python3
"""Exact bounded review bindings; no author imports or mathematical computations."""
import argparse,hashlib,json
from pathlib import Path

def need(b,m):
 if not b: raise ValueError(m)
def bind(p):
 b=p.read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();here=Path(__file__).resolve().parent
 spec=json.loads((here/'bindings.json').read_text()); n=0
 for x in spec['study_inputs']:
  need(bind(a.study_root/x['path'])=={k:x[k] for k in ('bytes','sha256')},'input '+x['path']);n+=1
 packet=a.study_root/spec['author_directory'];m=json.loads((packet/'manifest.json').read_text())
 for x in m['exports']:
  need(bind(packet/x['path'])=={k:x[k] for k in ('bytes','sha256')},'author export '+x['path']);n+=1
 sc=json.loads((packet/'scope.json').read_text());need(sc['new_original_credit']==0 and sc['new_conjecture_credit']==0 and sc['ratio']is None,'bounded scope')
 need(len(m['exports'])==5,'five frozen author exports')
 need((a.study_root/'sources/phase27_halving_current_arxiv.pdf').read_bytes()==(a.study_root/'sources/halving_hypertopes2025.pdf').read_bytes(),'source alias')
 need(bind(packet/'manifest.json')['sha256']=='57d0eeff3347c782e485606111822581c8bb5ff4254f592c919b5aa1e3faa1d9','exact author freeze')
 if (here/'manifest.json').exists():
  for x in json.loads((here/'manifest.json').read_text())['exports']:
   need(bind(here/x['path'])=={k:x[k] for k in ('bytes','sha256')},'review export '+x['path'])
 r={'status':'PASS','exact_input_bindings':n,'author_exports':5,'source_alias_exact':True,'math_check_basis':'complete written review, not automated theorem proving','new_mathematical_computations':0,'new_Lean_runs':0,'whole_source_acceptance':False}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
