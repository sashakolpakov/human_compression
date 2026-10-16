from pathlib import Path
import hashlib,json,resource,subprocess,sys,time
S=Path('/Users/sasha/medusa/research/leemans');P=S/'geometry/suzuki_subgroups/preliminaries';W=P.parent/'preliminaries_distinct_run01';assert not W.exists();W.mkdir()
def pin(p):
 p=Path(p).absolute();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
m=json.loads((P/'manifest.json').read_text());assert pin(P/'manifest.json')['sha256']=='f8234485599a4af33c4e01b32c2a31e42105498fa9c18b04a8878c7ad47e53b4'
rows={str(P/'manifest.json'):pin(P/'manifest.json')}
for q in m['exports']:
 p=P/q['path'];got=pin(p);assert (got['bytes'],got['sha256'])==(q['bytes'],q['sha256']);rows[str(p)]=got
for q in json.loads((P/'dependencies.json').read_text()):assert pin(q['path'])==q;rows[q['path']]=q
(P/'native03/preliminaries.tex').read_bytes()==(P/'preliminaries.tex').read_bytes()
checks=[]
def limit():resource.setrlimit(resource.RLIMIT_FSIZE,(8*2**20,8*2**20))
for name,cmd,cap in [('arithmetic',[sys.executable,'-B',str(P/'check_arithmetic.py')],30),('groups',['/opt/homebrew/bin/gap','-q','-b','-T','-m','64m','-K','512m',str(P/'controls.g')],60)]:
 start=time.monotonic()
 with(W/(name+'.stdout')).open('wb')as so,(W/(name+'.stderr')).open('wb')as se:
  try:r=subprocess.run(cmd,stdin=subprocess.DEVNULL,stdout=so,stderr=se,timeout=cap,preexec_fn=limit);code=r.returncode;timeout=False
  except subprocess.TimeoutExpired:code=None;timeout=True
 outcome=dict(name=name,command=cmd,cap_seconds=cap,returncode=code,timeout=timeout,seconds=time.monotonic()-start,stdout=pin(W/(name+'.stdout')),stderr=pin(W/(name+'.stderr')));checks.append(outcome);(W/'processes.json').write_text(json.dumps(checks,indent=2)+'\n')
 assert code==0 and not timeout and not(W/(name+'.stderr')).read_bytes()
 if name=='arithmetic':z=json.loads((W/(name+'.stdout')).read_text());assert z['status']=='PASS_L115_ARITHMETIC_CONTROLS'and z['odd_exponents']==50 and z['subfield_parameters']==240
 else:assert 'PASS_L115_PRELIMINARY_CONTROLS CYCLIC_ACTIONS 34' in (W/(name+'.stdout')).read_text()
for q in rows.values():assert pin(q['path'])==q
report=dict(status='PASS_FRESH_PRELIMINARY_CONTROLS',author_manifest=pin(P/'manifest.json'),unchanged_dependencies=len(rows),processes=checks,source_credit=0,whole_original_credit=0,mathematical_review='pending separate written proof/source review')
(W/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
