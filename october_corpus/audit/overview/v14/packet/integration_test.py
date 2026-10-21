#!/usr/bin/env python3
"""Check additive guard proposal without public writes or fabricated acceptance."""
from pathlib import Path
import argparse,ast,json
from build import HERE,read,need,sha
from check import nonmain

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 old=(a.public_root/'scripts/verify_snapshot.py').read_text();prior=nonmain(old);base=read('bindings.json')['baseline_non_main_functions'];need(len(base)==110 and all(prior.get(k)==v for k,v in base.items()),'110 prior functions')
 snippet=(HERE/'proposed/verifier_additions.py').read_text();need(old.count('\ndef main():')==1,'one main');merged=old.replace('\ndef main():','\n'+snippet+'\n\ndef main():',1);after=nonmain(merged);need(all(after.get(k)==v for k,v in prior.items()),'every current root function preserved');need(set(after)-set(prior)=={'check_unified_faithfulness_overview'},'one new function');compile(merged,'private_v14_merge','exec');compile((HERE/'proposed/check_unified_faithfulness_overview.py').read_text(),'private_v14_standalone','exec')
 bad=[]
 def reject(name,fn):
  try:fn()
  except ValueError:bad.append(name);return
  raise ValueError('missed control '+name)
 q=dict(after);q[next(iter(base))]='0'*64;reject('changed old function',lambda:need(all(q.get(k)==v for k,v in base.items()),'old change'))
 q=dict(after);q['unsolicited_function']='0'*64;reject('extra new function',lambda:need(set(q)-set(prior)=={'check_unified_faithfulness_overview'},'extra function'))
 p=read('proposed/latest.template.json');need(p['reader']['sha256']==sha((HERE/'reader.pdf').read_bytes()),'reader binding');prog=read('programme_binding.json');need(p['counts_source']==next(r for r in prog['public_artifacts']if r['path']==prog['snapshot']),'counts source');need(p['admission']['sha256']is None,'root admission unresolved');reject('premature acceptance',lambda:need(p['admission']['sha256']is not None,'missing root acceptance'))
 r=dict(status='PASS_PRIVATE_ADDITIVE_GUARD_PROPOSAL',baseline_non_main_functions=110,current_root_non_main_functions_preserved=len(prior),new_functions=['check_unified_faithfulness_overview'],controls=bad,public_files_written=False,current_pointer_exact_except_root_admission=True,full_snapshot_run=False)
 (a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
