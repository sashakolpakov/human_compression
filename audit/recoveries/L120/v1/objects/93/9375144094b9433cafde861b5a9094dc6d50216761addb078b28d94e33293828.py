"""Complete positive replay, with optional full unchanged enumeration replay."""
import sys
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
import argparse,gzip,hashlib,importlib.util,json,math,os,re,shutil,subprocess,time
from pathlib import Path

def need(b,s):
 if not b:raise ValueError(s)
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def digest(p):
 h=hashlib.sha256();size=0
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);size+=len(b)
 return dict(bytes=size,sha256=h.hexdigest())
def checkpin(p,x):need(digest(p)=={k:x[k]for k in ['bytes','sha256']},'exact bytes '+str(p))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--replay-enumeration',action='store_true');a=ap.parse_args()
 P=Path(__file__).resolve().parent;S=a.study.resolve();O=a.out.resolve();need(not O.exists(),'fresh output required')
 deps=json.loads((P/'dependencies.json').read_text())
 for x in deps:checkpin(S/x['path'],x)
 exports=[]
 if(P/'manifest.json').exists():
  exports=json.loads((P/'manifest.json').read_text())['exports']
  for x in exports:checkpin(P/x['path'],x)
 rows=json.loads((P/'roster.json').read_text());need([(x['key'],x['kind'],x['degree'],x['rank_limit'],[b['spec']['branch']for b in x['branches']])for x in rows]==[('s12','symmetric',12,7,list(range(1,7))),('s13','symmetric',13,7,list(range(1,7))),('s14','symmetric',14,8,list(range(1,8))),('a15','even',15,7,[2,4,6])],'exact complete four-row roster')
 method=S/'corpus106_L120_finite_method_v1';spec=importlib.util.spec_from_file_location('acquired_run_pool',method/'run_pool.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 O.mkdir(parents=True);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
 def run(name,cmd,cap,directory):
  started=time.monotonic()
  with(directory/(name+'.stdout')).open('wb')as so,(directory/(name+'.stderr')).open('wb')as se:
   try:cp=subprocess.run(list(map(str,cmd)),env=env,stdout=so,stderr=se,timeout=cap,cwd=directory)
   except subprocess.TimeoutExpired:
    save(directory/(name+'_receipt.json'),dict(status='TIMEOUT_NO_CERTIFICATE',command=list(map(str,cmd)),cap=cap));raise
  record=dict(returncode=cp.returncode,seconds=time.monotonic()-started,command=list(map(str,cmd)),stdout=digest(directory/(name+'.stdout')),stderr=digest(directory/(name+'.stderr')))
  save(directory/(name+'_receipt.json'),record);need(cp.returncode==0 and record['stderr']['bytes']==0,'clean terminal '+name)
  return(directory/(name+'.stdout')).read_text()
 answers=[];phase_records=[]
 for row in rows:
  key,kind,n,limit=[row[k]for k in ['key','kind','degree','rank_limit']];Q=P/key;D=O/key;D.mkdir();B=D/'branches';B.mkdir();order=math.factorial(n)//(2 if kind=='even' else 1);ids=[];literal=None;counts={str(r):dict(ordered=0,self_dual=0)for r in range(3,limit+1)}
  for b in row['branches']:
   original=Q/'branches'/b['name'];dest=B/b['name'];dest.mkdir();receipt=json.loads((original/'report.json').read_text());need(receipt['status']=='COMPLETE_FIXED_BRANCH'and receipt['returncode']==0 and receipt['spec']==b['spec'],'full retained execution')
   need(b['spec']==dict(kind=kind,degree=n,rank_limit=limit,branch=b['spec']['branch'],engine_entry='pool'),'unchanged complete engine scope')
   checkpin(method/'run_pool.py',receipt['runner']);checkpin(method/f'enumerate_{kind}_pool.g',receipt['engine']);checkpin(original/'driver.g',receipt['driver']);checkpin(original/'stderr.log',receipt['stderr']);need(receipt['stderr']['bytes']==0,'no original GAP errors')
   with gzip.open(original/'stdout.log.gz','rb')as src,(dest/'stdout.log').open('wb')as out:shutil.copyfileobj(src,out)
   checkpin(dest/'stdout.log',receipt['stdout']);need(receipt['stdout']==b['original_stdout'],'original transcript identity')
   result=mod.parse(dest/'stdout.log',n,kind,limit);need(result==json.loads((original/'result.json').read_text()),'full acquired parse');checkpin(original/'result.json',receipt['result'])
   if a.replay_enumeration:
    fresh=mod.execute(b['spec'],D/('fresh_'+b['name']),b['cap_seconds']);need(fresh['status']=='COMPLETE_FIXED_BRANCH','fresh complete enumeration');need(json.loads((D/('fresh_'+b['name'])/'result.json').read_text())==result,'exact fresh enumeration output')
   text=(dest/'stdout.log').read_text();m=re.search(r'INVOLUTIONS_LITERAL\s+(\[.*?\])\s+DIRECT_INITIAL_CHILD',text,re.S);need(m is not None,'exact literal universe boundary');li=re.sub(r'\s+','',m[1])
   if literal is None:literal=li
   else:need(literal==li,'common literal universe across branches')
   ids.extend(x['ids']for x in result['marks']if x['order']==order)
   for r in counts:
    for c in counts[r]:counts[r][c]+=result['counts'][r][c]
   # Lossless source remains frozen; remove only the temporary decompression.
   (dest/'stdout.log').unlink()
  need(len(ids)==len(set(map(tuple,ids))),'distinct source tuples')
  (D/'input.g').write_text(f'degree:={n};;rankLimit:={limit};;kind:="{kind}";;\nivs:='+literal+';;\nids:='+json.dumps(ids)+';;\n')
  (D/'driver.g').write_text('intervalFile:='+json.dumps(str(S/'corpus106_L120_interval_validator_v1/intervals.g'))+';;\ninputFile:='+json.dumps(str(D/'input.g'))+';;\nRead('+json.dumps(str(P/'validate.g'))+');\n')
  run('validation',['/opt/homebrew/bin/gap','-q','-T',D/'driver.g'],600,D)
  run('canonical',[sys.executable,P/'canonical.py','--degree',n,'--rank-limit',limit,'--input',D/'validation.stdout','--out',D/'canonical_report.json'],180,D)
  actual=json.loads((D/'canonical_report.json').read_text());expected=json.loads((Q/'expected.json').read_text())
  for k in ['degree','rank_limit','tuples','interval_checks','rows','reversal_maps']:need(actual[k]==expected[k],'exact positive/fusion phase '+k)
  for x in actual['rows']:
   c=counts[str(x['rank'])];need(c['ordered']==x['ordered']and c['self_dual']==x['self_dual'],'independent census/positive fusion agreement')
  source_positive=gzip.decompress((Q/'author_positive/validation.stdout.gz').read_bytes());original=json.loads((Q/'author_positive/validation_receipt.json').read_text());need(hashlib.sha256(source_positive).hexdigest()==original['stdout']['sha256'],'original positive phase')
  marker='COMPLETE_ALTERNATING_INTERVAL_VALIDATION'if kind=='even'else'COMPLETE_SYMMETRIC_INTERVAL_VALIDATION'
  normalized=source_positive.decode().replace(marker,'COMPLETE_FINITE_INTERVAL_VALIDATION');need(normalized==(D/'validation.stdout').read_text(),'exact literal positive phase except explicit common marker')
  phase_records.append(dict(key=key,tuples=actual['tuples'],interval_checks=actual['interval_checks'],branches=len(row['branches'])));answers.append(dict(key=key,rows=actual['rows']))
  print(json.dumps(dict(status='PASS_COMPLETE_ROW',**phase_records[-1])),flush=True)
 negatives=[]
 for row in rows:
  D=O/row['key'];n=row['degree'];limit=row['rank_limit'];lines=(D/'validation.stdout').read_text().splitlines();first=next(x for x in lines if x.startswith('SOLUTION|'));r=len(json.loads(first.split('|',1)[1]));checks=(r-1)*(r-2)
  tests={'truncated':'\n'.join(lines[:-1])+'\n','duplicate':'\n'.join([first,first,f'DEGREE|{n}',f'RANK_LIMIT|{limit}','VALIDATED_TUPLES|2',f'INTERVAL_CHECKS|{checks}','COMPLETE_FINITE_INTERVAL_VALIDATION'])+'\n'}
  for name,t in tests.items():
   src=D/(name+'.txt');src.write_text(t);out=D/(name+'.json');cp=subprocess.run([sys.executable,str(P/'canonical.py'),'--degree',str(n),'--rank-limit',str(limit),'--input',str(src),'--out',str(out)],env=env,capture_output=True,timeout=15);(D/(name+'.stderr')).write_bytes(cp.stderr);need(cp.returncode!=0 and not out.exists(),'damaged positive rejected');negatives.append(dict(row=row['key'],case=name,rejected=True))
 save(O/'negative_controls.json',negatives)
 guards=[]
 for script in ['check.py','canonical.py']:
  for mode in ['argument','environment']:
   e=env.copy();cmd=[sys.executable]
   if mode=='argument':cmd.append('-O')
   else:e['PYTHONOPTIMIZE']='1'
   dest=O/(script+'_'+mode+'_forbidden');cp=subprocess.run(cmd+[str(P/script),'--out',str(dest)],env=e,capture_output=True,timeout=10);need(cp.returncode!=0 and b'unoptimized execution required'in cp.stderr and not dest.exists(),'optimization rejection');(O/(script+'_'+mode+'.stderr')).write_bytes(cp.stderr);guards.append(dict(script=script,mode=mode,rejected=True))
 save(O/'optimization_controls.json',guards);pages=None
 if a.render:
  N=O/'native';N.mkdir();shutil.copy2(P/'rows.tex',N/'rows.tex')
  for i in range(2):run('native'+str(i),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','rows.tex'],45,N)
  from pypdf import PdfReader
  pdf=PdfReader(N/'rows.pdf');pages=len(pdf.pages);text='\n'.join(p.extract_text()or''for p in pdf.pages);(N/'text.txt').write_text(text);log=(N/'rows.log').read_text();need('Overfull'not in log and 'LaTeX Warning'not in log,'native layout/references')
  if(P/'native_expected.txt').exists():need(text==(P/'native_expected.txt').read_text(),'exact native text')
  run('raster',['/opt/homebrew/bin/gs','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=page-%02d.png','rows.pdf'],45,N)
 report=dict(status='PASS_FOUR_COMPLETE_FINITE_ROWS',mode='FRESH_ENUMERATION_AND_ALL_POSITIVE_CHECKS'if a.replay_enumeration else'RETAINED_COMPLETE_ENUMERATION_AND_FRESH_ALL_POSITIVE_CHECKS',exports=len(exports),dependencies=len(deps),complete_branches=22,rows=answers,phases=phase_records,tuples=sum(x['tuples']for x in phase_records),interval_checks=sum(x['interval_checks']for x in phase_records),damaged_controls=len(negatives),optimization_guards=len(guards),native_pages=pages,new_numeric_cells=21,whole_original_credit=0)
 save(O/'report.json',report);print(json.dumps(report))
if __name__=='__main__':main()
