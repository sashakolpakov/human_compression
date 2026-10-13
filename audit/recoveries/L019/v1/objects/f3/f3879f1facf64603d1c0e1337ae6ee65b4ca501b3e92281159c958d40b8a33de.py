import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from pathlib import Path
import argparse,json,hashlib,shutil,subprocess,os,time

def need(c,m):
 if not c:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args();P=Path(__file__).resolve().parent;O=a.out.resolve();need(not O.exists(),'fresh output');O.mkdir(parents=True)
 if(P/'manifest.json').exists():
  for r in json.loads((P/'manifest.json').read_text())['exports']:need(pin(P/r['path'])=={k:r[k]for k in['bytes','sha256']},'frozen export')
 for n in ['enumerate_anchors.py','gap_control.g','positive_controls.py','seven_anchors.tex']:shutil.copy2(P/n,O/n)
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
 def run(name,cmd,cap):
  t=time.monotonic();r=subprocess.run(cmd,cwd=O,capture_output=True,text=True,env=env,timeout=cap);(O/(name+'.stdout')).write_text(r.stdout);(O/(name+'.stderr')).write_text(r.stderr);(O/(name+'_receipt.json')).write_text(json.dumps({'returncode':r.returncode,'seconds':time.monotonic()-t,'cap':cap},indent=2)+'\n');need(r.returncode==0 and not r.stderr,'fresh '+name);return r.stdout
 run('python',[sys.executable,'enumerate_anchors.py'],45);r=json.loads((O/'enumeration01.json').read_text());need(r['counts']=={'involutions':231,'left':50,'middle':25,'right':50,'commuting_end_pairs':200,'distinct_triples':5000,'transitive_triples':0,'paired_transitive_triples':0}and not r['survivors'],'complete literal result')
 raw=run('gap',['/opt/homebrew/bin/gap','-q','-b','gap_control.g'],45);need(raw.count('COMPLETE_S7_ANCHOR_CONTROL')==1 and 'EXACT_S7_ANCHORS 231 50 25 50 200 5000 0'in raw,'independent group result')
 raw=run('positives',[sys.executable,'positive_controls.py'],10);need(json.loads(raw)['status']=='PASS_NONVACUOUS_BOUNDARY_CONTROLS','positive controls')
 for mode in['argument','environment']:
  ee=env.copy();cmd=[sys.executable]
  if mode=='argument':cmd+=['-O']
  else:ee['PYTHONOPTIMIZE']='1'
  x=subprocess.run(cmd+[str(P/'check.py')],capture_output=True,text=True,env=ee,timeout=5);need(x.returncode!=0 and 'normal Python required'in x.stderr,'optimization guard');(O/(mode+'_guard.stderr')).write_text(x.stderr)
 if a.render:
  for i in[1,2]:run('native'+str(i),['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','seven_anchors.tex'],30)
  need('Overfull'not in(O/'seven_anchors.log').read_text()and'LaTeX Warning:'not in(O/'seven_anchors.log').read_text(),'native layout')
 report={'status':'PASS_S7_ENDPOINT_ANCHORS','involutions':231,'triples':5000,'transitive':0,'positive_controls':3,'optimization_guards':2,'self_contained_written_proof':True,'whole_original_credit':0};(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
