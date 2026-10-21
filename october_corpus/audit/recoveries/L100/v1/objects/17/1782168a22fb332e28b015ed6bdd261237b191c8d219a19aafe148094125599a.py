import argparse,importlib.util,json,subprocess,sys
from pathlib import Path
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);n=a.parse_args();out=n.out.absolute();assert not out.exists();out.mkdir()
 sp=importlib.util.spec_from_file_location('bounded_palette_runtime',P/'run_palette.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);base,pins=m.preflight()
 q=lambda x:json.dumps(str(x));(out/'driver.g').write_text('CODE_DIR:='+q(P)+';;\nOUTPUT_DIR:='+q(out)+';;\nRead('+q(P/'controls.g')+');;\n')
 r=base.phase([str(base.GAP),'-q','-b',str(out/'driver.g')],out/'graphs',30,False);text=(out/'graphs/stdout').read_text();assert base.clean_phase(r,out/'graphs')and 'graphs=362 positive_isomorphisms=362 coset_models=3'in text
 calls=[]
 for name,cmd in [('literal',[sys.executable,str(P/'literal_oracle.py'),'--input',str(out/'coset_models.json'),'--out',str(out/'literal')]),('interface',[sys.executable,str(P/'interface_controls.py'),'--out',str(out/'interface')])]:
  p=subprocess.run(cmd,capture_output=True,timeout=45);(out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr);assert p.returncode==0 and not p.stderr;calls.append(dict(name=name,returncode=p.returncode))
 report=dict(status='PASS_COMPLETE_BOUNDED_PALETTE_CONTROLS',literal_graphs=362,positive_isomorphisms=362,literal_coset_models=3,calls=calls,target_census_runs=0,L100_postprocessing_runs=0);base.save(out/'report.json',report);print(json.dumps(report))
if __name__=='__main__':main()
