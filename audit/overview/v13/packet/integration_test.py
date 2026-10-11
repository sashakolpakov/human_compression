#!/usr/bin/env python3
"""Bounded additive guard test; no public writes or fabricated admission."""
from pathlib import Path
import argparse,ast,json
from build import HERE,read,need,sha
from check import nonmain

def main():
 a=argparse.ArgumentParser();a.add_argument('--public-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args();need(not args.out.exists(),'fresh output');args.out.mkdir(parents=True)
 old=(args.public_root/'scripts/verify_snapshot.py').read_text();baseline=read('bindings.json')['integration_existing_non_main_functions'];need(all(nonmain(old).get(k)==v for k,v in baseline.items())and len(baseline)==108,'108 current functions unchanged')
 snippet=(HERE/'proposed/verifier_additions.py').read_text();need(old.count('\ndef main():')==1,'one main');merged=old.replace('\ndef main():','\n'+snippet+'\n\ndef main():',1);after=nonmain(merged)
 need(all(after.get(k)==v for k,v in baseline.items()),'108 preserved on additive integration');need(set(after)-set(nonmain(old))=={'check_projective_covers_overview'},'one new guard only');compile(merged,'private_guard_merge','exec');compile((HERE/'proposed/check_projective_covers_overview.py').read_text(),'private_standalone_guard','exec')
 controls=[]
 def reject(name,fn):
  try:fn()
  except ValueError:controls.append(name);return
  raise ValueError('missed '+name)
 corrupt=dict(after);key=next(iter(baseline));corrupt[key]='0'*64;reject('changed old function',lambda:need(all(corrupt.get(k)==v for k,v in baseline.items()),'old function changed'))
 corrupt=dict(after);corrupt['second_new_function']='0'*64;reject('extra unsolicited function',lambda:need(set(corrupt)-set(nonmain(old))=={'check_projective_covers_overview'},'extra function'))
 pointer=read('proposed/latest.template.json');need(pointer['reader']['sha256']==sha((HERE/'reader.pdf').read_bytes()),'reader binding');need(pointer['counts_source']==next(x for x in read('programme_binding.json')['public_artifacts']if x['path']==read('programme_binding.json')['snapshot']),'current snapshot binding');need(pointer['admission']['sha256']is None,'root admission deliberately unresolved')
 reject('claim publication before root admission',lambda:need(pointer['admission']['sha256']is not None,'root admission missing'))
 report=dict(status='PASS',prior_nonmain_functions_preserved=108,new_functions=['check_projective_covers_overview'],standalone_guard_compiles=True,current_pointer_exact_except_root_admission=True,controls=controls,public_files_written=False,full_snapshot_run=False,scope='Root historical overlay retained; root creates and tests its distinct overview admission before publication.')
 (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
