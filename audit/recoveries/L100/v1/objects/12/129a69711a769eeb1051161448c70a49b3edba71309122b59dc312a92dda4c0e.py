"""Bounded fusion/caller controls, no L100 fusion or census."""
import argparse, copy, importlib.util, json, subprocess, sys, time
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('caller',HERE/'run_partial_fusion.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ns=ap.parse_args();out=ns.out.absolute();out.mkdir(parents=True,exist_ok=False)
 base,pins,rows,inv=m.preflight();tests=[]
 for folder,sha,completed,status in m.RECEIPTS:
  d=json.loads((m.G34/folder/'receipt.json').read_text());m.receipt_shape(d,completed,status)
  mutations=[lambda x:x.update(status='ACTIVE_TARGET'),lambda x:x.update(completed_anchors=x['completed_anchors']+[x['completed_anchors'][0]]),lambda x:x.update(audited_returned_rows=[]),lambda x:x['audit'].update(returncode=1),lambda x:x.update(target_census=False)]
  for i,f in enumerate(mutations):
   z=copy.deepcopy(d);f(z)
   try:m.receipt_shape(z,completed,status)
   except (ValueError,KeyError):tests.append([folder,i,'REJECTED'])
   else:raise AssertionError('damage accepted')
 before=m.pin(m.G34/'exhaustion_target03_anchor2/receipt.json');bad=dict(before,sha256='0'*64)
 try:base.verify(bad)
 except ValueError:tests.append(['changed_receipt','REJECTED'])
 else:raise AssertionError('changed pin accepted')
 # Exercise the exact actual CLI but stop before any GAP postprocessing.
 command=[sys.executable,str(HERE/'run_partial_fusion.py'),'--out',str(out/'prepared'),'--prepare-only']
 cp=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
 (out/'prepare.stdout').write_bytes(cp.stdout);(out/'prepare.stderr').write_bytes(cp.stderr)
 if cp.returncode or cp.stderr:raise RuntimeError('preparation failed')
 (out/'tiny.g').write_text('SizeScreen([100000,24]);;\n'+''.join('Read('+json.dumps(str(HERE/n))+');;\n' for n in ['legacy_fusion_functions.g','fusion_witness.g','witness_controls.g'])+'QUIT_GAP(0);\n')
 rr=base.phase([str(base.GAP),'-q','-b',str(out/'tiny.g')],out/'tiny',45,False)
 stdout=(out/'tiny/stdout').read_text()
 if not base.clean_phase(rr,out/'tiny') or 'PASS_FUSION_WITNESSES tests=' not in stdout:raise RuntimeError('tiny control failed')
 guards=[]
 for name in ['run_partial_fusion.py','controls.py']:
  dest=out/(name+'_optimized')
  for envkind in ['argument','environment']:
   cmd=[sys.executable]+(['-O'] if envkind=='argument' else [])+[str(HERE/name),'--out',str(dest)]
   import os
   env=dict(os.environ)
   if envkind=='environment':env['PYTHONOPTIMIZE']='1'
   q=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,timeout=5)
   if q.returncode==0 or dest.exists() or b'optimized execution forbidden' not in q.stderr:raise AssertionError('optimization guard')
   guards.append(dict(file=name,kind=envkind,returncode=q.returncode,stderr=q.stderr.decode()))
 report=dict(status='PASS_PARTIAL_FUSION_CALLER_CONTROLS',actual_preparation_anchors=len(rows),inputs_rehashed=len(pins),damaged_controls=tests,optimization_guards=guards,tiny_receipt=rr,tiny_stdout=stdout,target_runs=0,target_postprocessing_runs=0,complete_automorphism_computation_on_L100=False)
 base.save(out/'report.json',report);print(json.dumps(dict(status=report['status'],damage=len(tests),guards=len(guards),tiny=stdout.strip())))
if __name__=='__main__':main()
