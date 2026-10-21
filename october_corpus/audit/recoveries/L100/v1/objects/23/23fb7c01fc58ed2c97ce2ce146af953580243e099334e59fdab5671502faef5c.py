"""Execute the actual new caller on a tiny closed C2^2 family, no L100 computation."""
import argparse, importlib.util, json, sys
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('caller',HERE/'run_partial_fusion.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);ns=a.parse_args();out=ns.out.absolute();out.mkdir(parents=True,exist_ok=False);base,pins=m.get_base()
 done=out/'b1_done.g';done.write_text('borelResult:=rec(id:=1,order:=1,levels:=[3,3,0],geometries:=[[Group((1,2)),Group((3,4))],[Group((1,2)),Group((1,2)(3,4))],[Group((3,4)),Group((1,2)(3,4))]]);\n')
 q=lambda x:json.dumps(str(x))
 driver=out/'driver.g';driver.write_text('SizeScreen([100000,24]);;\nG:=Group((1,2),(3,4));;reps:=[TrivialSubgroup(G)];;borelResult:=rec();;\nINPUT_ROWS:=[[1,'+q(done)+',[3,3,0],[2,2,2]]];;OUTPUT_DIR:='+q(out)+';;\n'+''.join('Read('+q(HERE/n)+');;\n' for n in ['legacy_fusion_functions.g','fusion_witness.g','fusion_driver.g'])+'if L100ControlSentinel=false then Error("unreachable");fi;\n')
 # The final literal readback checks the serialized artifacts, not an internal counter.
 t=driver.read_text().replace('if L100ControlSentinel=false then Error("unreachable");fi;\n','Read('+q(out/'result.g')+');;Read('+q(out/'automorphisms.g')+');;\nif L100PartialFusion.counts<>[[2,3,1]] or Length(L100PartialFusion.members)<>3 or L100FullAutData.automorphism_order<>6 then Error("tiny caller output mismatch");fi;\nPrint("PASS_TINY_ACTUAL_CALLER_SERIALIZATION\\n");QUIT_GAP(0);\n');driver.write_text(t)
 r=base.phase([str(base.GAP),'-q','-b',str(driver)],out/'execution',15,False)
 stdout=(out/'execution/stdout').read_text();assert base.clean_phase(r,out/'execution') and 'PASS_TINY_ACTUAL_CALLER_SERIALIZATION' in stdout
 report=dict(status='PASS_TINY_ACTUAL_FUSION_CALLER',execution=r,stdout=stdout,source_files=[m.pin(HERE/n) for n in ['fusion_driver.g','fusion_witness.g','legacy_fusion_functions.g']],target_census_runs=0,L100_postprocessing_runs=0)
 base.save(out/'report.json',report);print(json.dumps(dict(status=report['status'],stdout=stdout.strip())))
if __name__=='__main__':main()
