import sys
if sys.flags.optimize: raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,hashlib,json,os,re,shutil,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent
GATES={
 'corpus106_L033_hyperbolic_core_v1':('75d6ef6c76971792a0c26952c460c3f550458cfdb2d7620704f092502712844f','AUTHOR_FROZEN_PARTIAL_COMPONENT'),
 'corpus106_L033_hyperbolic_core_independent_review':('d6098307aa2b10f046275ce9150f04e7afdc02cfab073cb194166e735f0fa333','ACCEPTED_L033_HYPERBOLIC_CORE'),
 'corpus106_L033_hyperbolic_core_root_adoption':('1bf7aed4508bf9f5bdfdb3edb29e4cae830e5a4ef434c9015ecff0776d3761ce','ROOT_ADOPTED_DISTINCTLY_REVIEWED_EIGHT_DIAGRAM_CORE')}
EXPECTED=[('3334',1,8,1920),('3334',2,9,2688),('3334',3,11,3840),('3334',4,12,7680),('3334',5,13,7680),('3335',1,5,7200),('3434',2,24,1152),('3434',3,27,1440),('3434',4,36,4320),('3434',5,38,5376),('3434',6,40,6048),('3434',7,45,9216),('353',1,5,8160),('435',1,14,3840),('435',2,12,3840),('435',3,15,7680),('435',4,16,7680),('535',1,5,7200),('535',2,6,8160),('5333',1,14,3840),('5333',2,19,3840),('5333',3,20,7680)]
UNIVERSAL={'3334':[24,48,48,24],'3335':[24,120,120,24],'3434':[48]*4,'353':[120,12,12,120],'435':[120,20,16,48],'535':[120,20,20,120],'5333':[8,24,120,120]}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def pin(p):
 b=p.read_bytes();return dict(path=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text())
def exact(p,row):
 a=pin(p);need(all(a[k]==row[k]for k in ['bytes','sha256']),'exact input '+str(p))
def dep_path(study,row):
 p=Path(row['path']);ns=row.get('namespace')
 if p.is_absolute():return p
 need('..'not in p.parts,'safe dependency path')
 if ns=='absolute':return Path('/')/p
 need(ns=='study','explicit study namespace');return study/p
def packet(folder,expected=None):
 manifest=folder/'manifest.json'
 if expected:need(pin(manifest)['sha256']==expected[0],'exact acquired manifest')
 m=load(manifest)
 if expected:need(m['status']==expected[1],'exact acquired status')
 seen=set()
 for r in m['exports']:
  p=Path(r['path']);need(not p.is_absolute()and '..'not in p.parts and str(p)not in seen,'unique relative export');seen.add(str(p));exact(folder/p,r)
 return m
def join(rows,selected,core):
 keys=[(r['type'],r['printed_row_within_type'],r['selected_node'],r['order'])for r in rows]
 need(keys==EXPECTED,'exact twenty-two printed row join')
 by={(r['type'],r['node']):r for r in core};got={(r['type'],r['node']):r for r in selected}
 need(len(got)==len(selected)==22,'distinct selected marked tuples')
 fields=['type','node','order','degree','local_orders','permutations']
 for r in rows:
  key=(r['type'],r['selected_node']);z=by[key]
  need(got[key]=={k:z[k]for k in fields},'literal tuple equality with accepted core')
  need(z['order']==r['order']and z['local_orders']==r['local_orders']==UNIVERSAL[r['type']],'actual universal local orders')
  need(r['source_id']==f"Table3.{r['type']}.{r['printed_row_within_type']}",'literal source row ID')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--render',action='store_true');a=ap.parse_args();study=a.study.resolve();out=a.out.resolve()
 need(not out.exists()and out.parent.is_dir(),'fresh output with existing parent')
 own=packet(P)
 for name,gate in GATES.items():packet(study/name,gate)
 deps=load(P/'dependencies.json')
 for r in deps:exact(dep_path(study,r),r)
 core=study/'corpus106_L033_hyperbolic_core_v1';rows=load(P/'source_map.json')['rows'];selected=load(P/'selected_tuples.json');positives=load(core/'positives.json');join(rows,selected,positives)
 out.mkdir();calls=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
 def run(name,cmd,cap,extraenv=None,cwd=None):
  before=time.monotonic();error=None
  try:
   p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=cap,cwd=cwd,env=extraenv or env);code,so,se=p.returncode,p.stdout,p.stderr
  except subprocess.TimeoutExpired as e:code,so,se=None,e.stdout or b'',e.stderr or b'';error='DEADLINE'
  except OSError as e:code,so,se=None,b'',str(e).encode();error='LAUNCH_FAILED'
  (out/(name+'.stdout')).write_bytes(so);(out/(name+'.stderr')).write_bytes(se)
  calls.append(dict(name=name,command=cmd,cap_seconds=cap,returncode=code,error=error,seconds=time.monotonic()-before,stdout=pin(out/(name+'.stdout')),stderr=pin(out/(name+'.stderr'))));(out/'calls.json').write_text(json.dumps(calls,indent=2)+'\n')
  return code,so.decode(errors='replace'),se.decode(errors='replace')
 prefix='hyperbolic_records:=[];;named_direct_records:=[];;named_series_records:=[];;named_dot_record:=rec();;linear_bridge:=rec();;\n'
 markers=['COMPLETE_NAMED_VERIFICATION 22','direct model exact isomorphism','actual split kernel','split outer involution','central nonsplit obstruction','linear bridge isomorphism']
 for bad in range(6):
  driver=out/f'case{bad}.g';driver.write_text(prefix+'if GAPInfo.Version<>"4.15.1" then Error("GAP version");fi;\nRead('+json.dumps(str(P/'verify.g'))+');;\nVerifyNamed('+json.dumps(str(core))+','+json.dumps(str(P))+','+str(bad)+');;\nQUIT;\n')
  rc,so,se=run(f'case{bad}',['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(driver)],60)
  if bad==0:need(rc==0 and not se and markers[0]in so and 'Syntax warning'not in so and 'Error'not in so,'clean complete positive certificate')
  else:need(rc not in [None,0]and markers[bad]in so+se and markers[0]not in so,'specific damaged certificate rejection')
 damages=[]
 for kind in ['wrong_order','duplicate_row','changed_literal_tuple']:
  rs=copy.deepcopy(rows);ss=copy.deepcopy(selected)
  if kind=='wrong_order':rs[0]['order']+=1
  elif kind=='duplicate_row':rs[-1]=copy.deepcopy(rs[0])
  else:ss[0]['permutations'][0]=list(range(1,ss[0]['degree']+1))
  try:join(rs,ss,positives)
  except (ValueError,KeyError):damages.append(kind)
  else:raise ValueError('damaged source join accepted')
 guards=[]
 for mode in ['argument','environment']:
  dest=out/('rejected_'+mode);ge=dict(env)
  if mode=='environment':ge['PYTHONOPTIMIZE']='1'
  rc,so,se=run(mode,[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/'check.py'),'--study',str(study),'--out',str(dest)],10,ge)
  need(rc not in [None,0]and 'normal Python required'in so+se and not dest.exists(),'pre-output optimization rejection');guards.append(mode)
 pages=None
 if a.render:
  native=out/'native';native.mkdir();shutil.copy2(P/'names.tex',native/'names.tex')
  for n in [1,2]:
   rc,so,se=run(f'native{n}',['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','names.tex'],60,cwd=native);need(rc==0 and not se,'clean native build')
  log=(native/'names.log').read_text();need(not re.search('Warning|Overfull|Underfull',log),'native log clean')
  rc,so,se=run('native_text',['/opt/homebrew/bin/pdftotext',str(native/'names.pdf'),str(native/'names.txt')],20);need(rc==0 and not se,'native text extraction');pages=(native/'names.txt').read_text().count('\f');need(pages==3,'three complete manuscript pages')
  if (P/'names.pdf').exists():
   rc,so,se=run('reference_text',['/opt/homebrew/bin/pdftotext',str(P/'names.pdf'),str(out/'reference.txt')],20);need(rc==0 and (out/'reference.txt').read_bytes()==(native/'names.txt').read_bytes(),'reference native text identity')
  rc,so,se=run('native_render',['/opt/homebrew/bin/pdftoppm','-r','110','-png',str(native/'names.pdf'),str(native/'page')],30);need(rc==0 and not se and len(list(native.glob('page-*.png')))==3,'three native views')
 report=dict(status='PASS_L033_TWENTY_TWO_GROUP_CERTIFICATES',exports=len(own['exports']),dependencies=len(deps),source_rows=22,positive_certificates=22,damaged_certificates=5,damaged_source_joins=damages,optimization_guards=guards,all_selected_universal_local_orders=True,native_pages=pages,LINS_runs=0,target_searches=0,ninth_diagram_claimed=False,whole_original_credit=0,new_question_credit=0,new_measurements=0)
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
