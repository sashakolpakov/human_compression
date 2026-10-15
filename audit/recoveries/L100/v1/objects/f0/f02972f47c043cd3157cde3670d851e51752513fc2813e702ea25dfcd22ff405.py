import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,time

S=Path('/Users/sasha/medusa/research/leemans');P=S/'corpus106_L100_rank_two_v1';Q=S/'geometry/psl3_4'
AUTHOR='2a53441260ce172d195ae028e433d21d9b4af75fcd74209ae1fd7a40c12ea114'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def pin(p):
 b=p.read_bytes();return {'path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def exact(p,r):need(all(pin(p)[k]==r[k]for k in ['bytes','sha256']),'input pin '+str(p))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();out=a.out.resolve();need(not out.exists()and out.parent.exists(),'fresh output')
 need(pin(P/'manifest.json')['sha256']==AUTHOR,'exact author')
 for r in load(P/'manifest.json')['exports']:exact(P/r['path'],r)
 deps=load(P/'dependencies.json')
 for r in deps:exact(Path(r['path']),r)
 lib=load(S/'reboot_20261013/L091_work/retained_library_inputs.json')
 for r in lib['files']:exact(Path(r['path']),r)
 for name,marker in [('run01','PASS_PRIMITIVE_RANK_TWO'),('witnesses01','PASS_EXPLICIT_WITNESSES 24'),('oracle02','PASS_COSET_ORACLE 60 PAIRS 3098 NEIGHBOUR_PAIRS 24 WITNESSES')]:
  r=load(Q/(name+'.json'));need(r['returncode']==0 and not(Q/(name+'.stderr')).read_bytes()and marker in(Q/(name+'.stdout')).read_text(),'acquired clean scientific terminal')
 out.mkdir();calls=[]
 def run(name,cmd,cap=60,cwd=None,env=None):
  t=time.monotonic();error=None
  try:
   p=subprocess.run(cmd,cwd=cwd,env=env,timeout=cap,capture_output=True);rc,so,se=p.returncode,p.stdout,p.stderr
  except subprocess.TimeoutExpired as e:rc,so,se=None,e.stdout or b'',e.stderr or b'';error='DEADLINE'
  except OSError as e:rc,so,se=None,b'',str(e).encode();error='LAUNCH_FAILED'
  (out/(name+'.stdout')).write_bytes(so);(out/(name+'.stderr')).write_bytes(se)
  calls.append({'name':name,'command':cmd,'returncode':rc,'cap':cap,'seconds':time.monotonic()-t,'error':error,'stdout':pin(out/(name+'.stdout')),'stderr':pin(out/(name+'.stderr'))});(out/'calls.json').write_text(json.dumps(calls,indent=2)+'\n')
  return rc,so.decode(errors='replace'),se.decode(errors='replace')
 rc,so,se=run('fresh_oracle',['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(Q/'coset_oracle_v2.g')]);need(rc==0 and not se and 'PASS_COSET_ORACLE 60 PAIRS 3098 NEIGHBOUR_PAIRS 24 WITNESSES'in so,'fresh bounded saved-candidate oracle')
 oracle=(Q/'coset_oracle_v2.g').read_text();need(oracle.count('RunOracle();')==1,'exact final call')
 changes=[('wrong_order','PSL34RankTwo.pairs[1].orders[1]:=1;','Actual groups mismatch'),('wrong_common_count','PSL34RankTwo.pairs[1].common_counts[1]:=999;','Common neighbour multiset'),('wrong_IP2','PSL34RankTwo.pairs[1].IP2:=not PSL34RankTwo.pairs[1].IP2;','All pairs incidence'),('wrong_local2T','PSL34RankTwo.pairs[1].local_two_transitive[1]:=not PSL34RankTwo.pairs[1].local_two_transitive[1];','Local 2T flag'),('duplicate_witness','PSL34Witnesses[2].source_pair:=PSL34Witnesses[1].source_pair;','Witness coverage'),('trivial_homomorphism','PSL34Witnesses[1].generator_images:=List(PSL34RankTwo.group_generators,g->());','Not an automorphism'),('wrong_type_swap','for w in PSL34Witnesses do if PSL34RankTwo.pairs[w.source_pair].orders[1]<>PSL34RankTwo.pairs[w.source_pair].orders[2] then w.type_permutation:=w.type_permutation*(1,2);break;fi;od;','Simultaneous images')]
 for name,delta,marker in changes:
  f=out/(name+'.g');f.write_text(oracle.replace('RunOracle();',delta+'\nRunOracle();'))
  rc,so,se=run(name,['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(f)])
  need(rc not in [None,0]and marker in so+se and 'PASS_COSET_ORACLE'not in so,'specific damaged-data rejection '+name)
 for mode in ['argument','environment']:
  ge=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');ge.pop('PYTHONOPTIMIZE',None)
  if mode=='environment':ge['PYTHONOPTIMIZE']='1'
  dest=out/('forbidden_'+mode)
  rc,so,se=run(mode,[sys.executable]+(['-O']if mode=='argument'else[])+[str(Path(__file__).resolve()),'--out',str(dest)],10,env=ge)
  need(rc not in [0,None]and 'normal Python required'in so+se and not dest.exists(),'pre-output optimization guard')
 native=out/'native';native.mkdir();shutil.copy2(Q/'primitive_residues.tex',native/'primitive_residues.tex')
 for n in [1,2]:
  rc,so,se=run('native'+str(n),['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','primitive_residues.tex'],cwd=native);need(rc==0 and not se,'clean native build')
 log=(native/'primitive_residues.log').read_text();need(not any(x in log for x in ['Warning','Overfull','Underfull']),'clean final log')
 from pypdf import PdfReader
 a=PdfReader(Q/'primitive_residues.pdf');b=PdfReader(native/'primitive_residues.pdf')
 need(len(a.pages)==len(b.pages)==2,'two complete pages')
 at='\f'.join(p.extract_text()for p in a.pages);bt='\f'.join(p.extract_text()for p in b.pages);need(at==bt,'exact native text')
 (out/'author.txt').write_text(at);(out/'review.txt').write_text(bt)
 rc,so,se=run('render',['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r120','-sOutputFile='+str(out/'page-%02d.png'),str(native/'primitive_residues.pdf')]);need(rc==0 and not se and len(list(out.glob('page-*.png')))==2,'fresh native pages')
 report={'status':'PASS_L100_DISTINCT_BOUNDED_REPLAY','author_manifest':pin(P/'manifest.json'),'direct_dependencies':len(deps),'library_files':len(lib['files']),'fresh_saved_candidate_oracle':True,'negative_controls':[x[0]for x in changes],'optimization_guards':2,'native_pages':2,'new_subgroup_enumerations':0}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
