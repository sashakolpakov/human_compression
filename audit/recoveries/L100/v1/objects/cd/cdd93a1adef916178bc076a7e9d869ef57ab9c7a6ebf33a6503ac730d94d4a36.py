"""Only changed initialization: three tiny complete orbit checks and exact delta."""
import argparse,importlib.util,json,os,subprocess,sys
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;G34=P.parent;OLD=G34/'incremental_fusion_interface_v1'
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);ns=a.parse_args();out=ns.out.absolute();assert not out.exists();out.mkdir(parents=True)
 old=(OLD/'incremental.g').read_text();new=(P/'incremental.g').read_text();assert old[old.index(' Read(row[2]);'):]==new[new.index(' Read(row[2]);'):]
 for name in ['run_incremental.py','controls.py','tiny_controls.g']:assert(OLD/name).read_bytes()==(P/name).read_bytes()
 sp=importlib.util.spec_from_file_location('incremental_accepted_input',P/'run_incremental.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);base,pins,row=m.preflight()
 suffix='RunIncrementalFusion(G,reps,L100PartialFusion,L100FullAutData,NEW_ROW,OUTPUT_DIR);;\n';assert new.endswith(suffix);(out/'function_only.g').write_text(new[:-len(suffix)])
 # Exact previous tiny caller, changing only the literal function and output locations.
 source=G34/'incremental_controls01/tiny.g';text=source.read_text().replace(str(G34/'incremental_controls01'),str(out)).replace(str(G34/'incremental_fusion_work/tiny_controls.g'),str(P/'tiny_controls.g'))
 for i in [1,2,3]:(out/f'case{i}').mkdir()
 (out/'tiny.g').write_text(text);r=base.phase([str(base.GAP),'-q','-b',str(out/'tiny.g')],out/'tiny',20,False);stdout=(out/'tiny/stdout').read_text();assert base.clean_phase(r,out/'tiny')and stdout.count('PASS_TINY_INCREMENT counts=')==3 and 'PASS_ALL_INCREMENTAL_TINY_CONTROLS'in stdout
 guards=[]
 for mode in ['argument','environment']:
  dest=out/('DENIED_'+mode);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
  if mode=='environment':env['PYTHONOPTIMIZE']='1'
  cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/'focused_controls.py'),'--out',str(dest)];q=subprocess.run(cmd,env=env,capture_output=True,timeout=5);assert q.returncode!=0 and not dest.exists()and b'optimized execution forbidden'in q.stderr;guards.append(mode)
 report=dict(status='PASS_INCREMENTAL_V2_INITIALIZER_CONTROLS',unchanged_classification_tail=True,unchanged_python_caller=True,tiny_complete_orbit_models=3,guards=guards,execution=r,input_pins=len(pins),target_census_runs=0,L100_postprocessing_runs=0)
 base.save(out/'report.json',report);print(json.dumps(dict(status=report['status'],models=3,guards=2)))
if __name__=='__main__':main()
