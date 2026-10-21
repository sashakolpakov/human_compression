import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from pathlib import Path
import argparse,json,hashlib,shutil,subprocess,os,time,copy

def need(c,m):
 if not c:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
EXPECTED=[[75,75,120,0],[11,11,0,0],[19,19,0,0],[11,11,0,0],[19,75,48,0],[11,19,8,0],[11,75,80,0],[75,19,48,0],[19,11,8,0],[19,19,16,4],[75,11,80,0]]
def validate(r):
 need(r['status']=='COMPLETE_ELEVEN_ENDPOINT_MODELS' and len(r['models'])==11,'endpoint coverage')
 need([[x[k]for k in['middle_left','middle_right','transitive','paired']]for x in r['rows']]==EXPECTED,'exact rows')
 need(sum(x['pairs']for x in r['rows'])==11507 and sum(x['transitive']for x in r['rows'])==408,'complete pair counts')
 need(len(r['survivors'])==r['survivor_count']==4 and r['all_survivors_path'],'exact survivors')
 for s in r['survivors']:
  f=s['path_map'];need(f is not None and sorted(f)==list(range(9))and f[0]==0 and f[8]==8,'anchored bijection')
  need(all(f[p[x]]==q[f[x]]for p,q in zip(s['marks'],r['target'])for x in range(9)),'literal labelled conjugacy')
  need(all(len(es)>=2 for es in s['eligible']),'all colours eligible')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();P=Path(__file__).resolve().parent;O=a.out.resolve();need(not O.exists(),'fresh output');O.mkdir(parents=True)
 if(P/'manifest.json').exists():
  for r in json.loads((P/'manifest.json').read_text())['exports']:need(pin(P/r['path'])=={k:r[k]for k in['bytes','sha256']},'frozen export')
 for n in ['enumerate_boundary.py','endpoint_control.py','gap_control.g','models.g','degree9.tex']:shutil.copy2(P/n,O/n)
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
 def run(name,cmd,cap):
  t=time.monotonic();r=subprocess.run(cmd,cwd=O,capture_output=True,text=True,env=env,timeout=cap);(O/(name+'.stdout')).write_text(r.stdout);(O/(name+'.stderr')).write_text(r.stderr);(O/(name+'_receipt.json')).write_text(json.dumps({'returncode':r.returncode,'seconds':time.monotonic()-t,'cap':cap},indent=2)+'\n');need(r.returncode==0 and not r.stderr,'fresh '+name);return r.stdout
 run('python',[sys.executable,'enumerate_boundary.py'],45);r=json.loads((O/'enumeration01.json').read_text());validate(r)
 # The static GAP input is checked literally against the fresh Python result.
 expected='rawModels:='+json.dumps([[list(map(lambda x:x+1,m[k]))for k in['a','d']]for m in r['models']])+';;\nrawExpected:='+json.dumps([[[x+1 for x in p]for p in s['marks']]for s in r['survivors']])+';;\nrawTarget:='+json.dumps([[x+1 for x in p]for p in r['target']])+';;\n'
 need((O/'models.g').read_text()==expected,'literal independent input')
 raw=run('gap',['/opt/homebrew/bin/gap','-q','-b','gap_control.g'],45);need(raw.count('COMPLETE_DEGREE9_BOUNDARY_CONTROL')==1 and 'ACTUAL_GROUP_ORDER 181440 SUBSET_PAIRS 256'in raw,'actual group and IP')
 raw=run('endpoints',[sys.executable,'endpoint_control.py'],10);need(json.loads(raw)=={'status':'PASS_LITERAL_ENDPOINT_AND_MAP_CONTROL','left':76,'right':76,'commuting_pairs':196,'canonical_types':11,'conjugacy_checks':4},'independent endpoint coverage')
 for i in range(5):
  bad=copy.deepcopy(r)
  if i==0:bad['models'].pop()
  elif i==1:bad['rows'][0]['transitive']+=1
  elif i==2:bad['survivors'].pop()
  elif i==3:bad['survivors'][0]['path_map'][0]=8
  else:bad['survivors'][0]['eligible'][0]=[]
  try:validate(bad)
  except RuntimeError:pass
  else:raise RuntimeError('damaged control survived')
 for mode in['argument','environment']:
  ee=env.copy();cmd=[sys.executable]
  if mode=='argument':cmd+=['-O']
  else:ee['PYTHONOPTIMIZE']='1'
  x=subprocess.run(cmd+[str(P/'check.py')],capture_output=True,text=True,env=ee,timeout=5);need(x.returncode!=0 and 'normal Python required'in x.stderr,'optimization guard');(O/(mode+'_guard.stderr')).write_text(x.stderr)
 if a.render:
  for i in[1,2]:run('native'+str(i),['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','degree9.tex'],30)
  need('Overfull'not in(O/'degree9.log').read_text()and'LaTeX Warning:'not in(O/'degree9.log').read_text(),'native layout')
 report={'status':'PASS_DEGREE9_ENDPOINT_BOUNDARY','endpoint_types':11,'middle_pairs':11507,'transitive':408,'survivors':4,'independent_endpoint_pairs':196,'actual_group':'Alt9','subset_pairs':256,'anchored_tail_centralizer':'< (2,3) >','damaged_controls':5,'optimization_guards':2,'whole_original_credit':0};(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
