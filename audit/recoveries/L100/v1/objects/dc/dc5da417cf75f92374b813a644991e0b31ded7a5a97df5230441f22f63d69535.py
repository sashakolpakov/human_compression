"""Actual tiny caller + input guards; no L100 palette postprocessing."""
import argparse,copy,importlib.util,json,os,subprocess,sys
from pathlib import Path
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('palette_call',P/'run_palette.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);ns=a.parse_args();out=ns.out.absolute();assert not out.exists();out.mkdir();base,pins=m.preflight();m.prepare(out/'actual_prepared')
 old=json.loads((m.TARGET/'receipt.json').read_text());damages=[]
 for i in range(6):
  d=copy.deepcopy(old)
  if i==0:d['status']='PARTIAL_POSTPROCESSING_DEADLINE'
  elif i==1:d['old_anchors'].append(1)
  elif i==2:d['new_anchor']=[2]
  elif i==3:d['execution']['returncode']=1
  elif i==4:d['total_input_members']=144
  else:d['new_member_count']=41
  try:m.shape(d)
  except ValueError:damages.append(i)
  else:raise ValueError('damaged input boundary accepted')
 q=lambda p:json.dumps(str(p));target=out/'tiny';target.mkdir();code=(P/'driver_body.g').read_text();suffix='RunLiteralPaletteCatalogue(G,L100CompleteAutFusion,OUTPUT_DIR);;\nQUIT_GAP(0);\n';assert code.endswith(suffix);(out/'function_only.g').write_text(code[:-len(suffix)])
 lines=['LoadPackage("grape");;LoadPackage("json");;SizeScreen([100000,24]);;',
 'Read('+q(P/'cosets.g')+');;','Read('+q(P/'palette.g')+');;','Read('+q(out/'function_only.g')+');;',
 'G:=Group((1,2),(3,4));;a:=Group((1,2));;b:=Group((3,4));;c:=Group((1,2)(3,4));;',
 'data:=rec(group_generators:=GeneratorsOfGroup(G),representatives:=[rec(borel_id:=1,source_index:=1,parabolics:=[a,b]),rec(borel_id:=1,source_index:=2,parabolics:=[a,c]),rec(borel_id:=1,source_index:=3,parabolics:=[b,c])]);;',
 'RunLiteralPaletteCatalogue(G,data,'+q(target)+');;','Print("PASS_ACTUAL_TINY_PALETTE_CALLER\\n");QUIT_GAP(0);']
 (out/'tiny.g').write_text('\n'.join(lines)+'\n');r=base.phase([str(base.GAP),'-q','-b',str(out/'tiny.g')],out/'process',20,False);text=(out/'process/stdout').read_text();assert base.clean_phase(r,out/'process')and 'PASS_ACTUAL_TINY_PALETTE_CALLER'in text
 result=json.loads((target/'result.json').read_text());assert result['counts']==[[2,3,1]]and result['classes']==[1]and result['completed']==[1,2,3]and all(r['correlations_order']==8 and r['typed_order']==4 for r in result['records'])
 guards=[]
 for name in ['run_palette.py','interface_controls.py']:
  for mode in ['argument','environment']:
   denied=out/('DENIED_'+name+'_'+mode);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
   if mode=='environment':env['PYTHONOPTIMIZE']='1'
   cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/name),'--out',str(denied)];p=subprocess.run(cmd,env=env,capture_output=True,timeout=5);assert p.returncode!=0 and b'normal Python required'in p.stderr and not denied.exists();guards.append([name,mode])
 report=dict(status='PASS_LITERAL_PALETTE_INTERFACE_CONTROLS',tiny_models=3,tiny_classes=1,input_damages=damages,guards=guards,input_pins=len(pins),target_census_runs=0,L100_postprocessing_runs=0);base.save(out/'report.json',report);print(json.dumps(report))
if __name__=='__main__':main()
