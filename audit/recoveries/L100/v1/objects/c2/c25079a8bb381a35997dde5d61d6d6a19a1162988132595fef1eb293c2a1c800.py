"""Tiny incremental equivalence and exact receipt guards, no L100 fusion."""
import argparse,copy,importlib.util,json,os,subprocess,sys
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('incr',HERE/'run_incremental.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);ns=a.parse_args();out=ns.out.absolute();out.mkdir(parents=True,exist_ok=False)
 base,pins,row=m.preflight();old=json.loads((m.OUTOLD/'receipt.json').read_text());new=json.loads((m.NEW/'receipt.json').read_text());damages=[]
 for i in range(8):
  x,y=copy.deepcopy(old),copy.deepcopy(new)
  if i==0:x['status']='PARTIAL_POSTPROCESSING_DEADLINE'
  elif i==1:x['anchors'].append(1)
  elif i==2:x['execution']['returncode']=1
  elif i==3:y['completed_anchors']=[]
  elif i==4:y['requested_anchors']=[2]
  elif i==5:y['audit']['returncode']=1
  elif i==6:y['audited_returned_rows'][0][1][-1]=1
  else:y['reported_completed_rows']=[]
  try:m.receipt_shapes(x,y)
  except ValueError:damages.append(i)
  else:raise AssertionError('damaged receipt accepted')
 cmd=[sys.executable,str(HERE/'run_incremental.py'),'--out',str(out/'prepared'),'--prepare-only'];p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20);(out/'prepare.stdout').write_bytes(p.stdout);(out/'prepare.stderr').write_bytes(p.stderr);assert p.returncode==0 and not p.stderr
 q=lambda p:json.dumps(str(p))
 code=(HERE/'incremental.g').read_text();suffix='RunIncrementalFusion(G,reps,L100PartialFusion,L100FullAutData,NEW_ROW,OUTPUT_DIR);;\n';assert code.endswith(suffix)
 (out/'function_only.g').write_text(code[:-len(suffix)])
 for i in range(1,4):(out/f'case{i}').mkdir()
 lines=['SizeScreen([100000,24]);;','borelResult:=rec();;L100CompleteAutFusion:=rec();;',
 'Read('+q(m.OLD/'legacy_fusion_functions.g')+');;','Read('+q(m.OLD/'fusion_witness.g')+');;',
 'Read('+q(out/'function_only.g')+');;','Read('+q(HERE/'tiny_controls.g')+');;',
 'g:=Group((1,2),(3,4));;a:=Group((1,2));;b:=Group((3,4));;c:=Group((1,2)(3,4));;',
 'MakeTinyIncrement(g,[a,b],[[a,c],[b,c]],[[2,3,1]],'+q(out/'case1')+');;',
 'g:=SymmetricGroup(3);;a:=Group((1,2));;b:=Group((1,2,3));;c:=Group((2,3));;',
 'MakeTinyIncrement(g,[a,b],[[a,c],[c,b]],[[2,3,2]],'+q(out/'case2')+');;',
 'g:=Group((1,2,3),(4,5),(6,7));;a:=Group((1,2,3));;b:=Group((4,5));;c:=Group((6,7));;',
 'MakeTinyIncrement(g,[ClosureGroup(b,a),ClosureGroup(b,c)],[[a,b,c]],[[2,1,1],[3,1,1]],'+q(out/'case3')+');;',
 'Print("PASS_ALL_INCREMENTAL_TINY_CONTROLS\\n");QUIT_GAP(0);']
 (out/'tiny.g').write_text('\n'.join(lines)+'\n');rr=base.phase([str(base.GAP),'-q','-b',str(out/'tiny.g')],out/'tiny',20,False);text=(out/'tiny/stdout').read_text();assert base.clean_phase(rr,out/'tiny') and 'PASS_ALL_INCREMENTAL_TINY_CONTROLS'in text
 guards=[]
 for name in ['run_incremental.py','controls.py']:
  for mode in ['argument','environment']:
   dest=out/(name+'_'+mode);cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(HERE/name),'--out',str(dest)];env=dict(os.environ)
   if mode=='environment':env['PYTHONOPTIMIZE']='1'
   r=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5);assert r.returncode!=0 and not dest.exists()and b'optimized execution forbidden'in r.stderr;guards.append([name,mode,r.returncode])
 report=dict(status='PASS_INCREMENTAL_FUSION_CONTROLS_NO_L100_POSTPROCESSING',prior_damages=damages,guards=guards,tiny=rr,tiny_stdout=text,input_pins=len(pins),L100_postprocessing_runs=0,target_census_runs=0)
 base.save(out/'report.json',report);print(json.dumps(dict(status=report['status'],damages=len(damages),guards=len(guards),tiny=text.strip())))
if __name__=='__main__':main()
