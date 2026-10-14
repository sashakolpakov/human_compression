import sys
if sys.flags.optimize: raise RuntimeError('unoptimized execution required')
from pathlib import Path
import ast, difflib, hashlib, json, os, re, shutil, subprocess
from pypdf import PdfReader
W=Path(__file__).resolve().parent; S=W.parents[1]; P=W/'s11_component_work'; O=W/'s11_author_controls02'
if O.exists(): raise ValueError('fresh controls output required')
O.mkdir(); env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
def need(ok,msg):
 if not ok: raise ValueError(msg)
for row in json.loads((P/'dependencies.json').read_text()):
 b=(S/row['path']).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+row['path'])
# Every positive scientific phase already has a complete terminal receipt.
V=W/'s11_validation_work'
receipt=json.loads((V/'receipt.json').read_text());need(receipt['status']=='PASS_COMPLETE_S11_SUBSETS' and receipt['returncode']==0,'terminal subset phase')
need(hashlib.sha256((V/'validation.stdout').read_bytes()).hexdigest()==receipt['stdout_sha256'],'exact terminal bytes')
need(not (V/'validation.stderr').read_bytes(),'clean terminal stderr')
ids=[];literal=None;counts={str(r):dict(ordered=0,self_dual=0) for r in range(3,11)}
for i in range(1,6):
 D=P/'completed_branches'/f'symmetric11_part{i}';r=json.loads((D/'report.json').read_text());need(r['status']=='COMPLETE_FIXED_BRANCH','terminal enumeration')
 result=json.loads((D/'result.json').read_text());m=re.search(r'INVOLUTIONS_LITERAL\s+(\[.*?\])\s+DIRECT_INITIAL_CHILD',(D/'stdout.log').read_text(),re.S);need(m is not None,'literal header')
 if literal is None:literal=m.group(1)
 else:need(literal==m.group(1),'common literal list')
 ids.extend(row['ids'] for row in result['marks'] if row['order']==39916800)
 for r,c in counts.items():
  for k in c:c[k]+=result['counts'][r][k]
need(('ivs:='+literal+';;\nids:='+json.dumps(ids)+';;\n')==(V/'input.g').read_text(),'literal input interface')
need((V/'validate.g').read_bytes()==(P/'validate.g').read_bytes(),'exact validator used')
cp=subprocess.run([sys.executable,str(P/'canonical.py'),'--input',str(V/'validation.stdout'),'--out',str(O/'canonical_report.json')],env=env,capture_output=True,timeout=20)
(O/'canonical.stdout').write_bytes(cp.stdout);(O/'canonical.stderr').write_bytes(cp.stderr)
need(cp.returncode==0 and not cp.stderr,'literal canonical replay')
actual=json.loads((O/'canonical_report.json').read_text());need(actual==json.loads((P/'expected.json').read_text()),'expected exact literal classes')
for row in actual['rows']:
 c=counts[str(row['rank'])];need(c['ordered']==row['ordered'] and c['self_dual']==row['self_dual'],'independent count agreement')
text=(V/'validation.stdout').read_text()
for name,damaged in [('truncated',text.replace('COMPLETE_S11_VALIDATION','')),('duplicate',text.replace('COMPLETE_S11_VALIDATION',next(x for x in text.splitlines() if x.startswith('SOLUTION|'))+'\nCOMPLETE_S11_VALIDATION'))]:
 src=O/(name+'.txt');src.write_text(damaged);dest=O/(name+'.json')
 cp=subprocess.run([sys.executable,str(P/'canonical.py'),'--input',str(src),'--out',str(dest)],env=env,capture_output=True,timeout=20)
 (O/(name+'.stderr')).write_bytes(cp.stderr);need(cp.returncode!=0 and not dest.exists(),'damaged rejection')
for script in ['check.py','canonical.py']:
 for mode in ['argument','environment']:
  e=env.copy();cmd=[sys.executable]
  if mode=='argument':cmd.append('-O')
  else:e['PYTHONOPTIMIZE']='1'
  target=O/(script+'_'+mode+'_forbidden')
  cp=subprocess.run(cmd+[str(P/script),'--out',str(target)],env=e,capture_output=True,timeout=10)
  (O/(script+'_'+mode+'.stderr')).write_bytes(cp.stderr)
  need(cp.returncode!=0 and b'unoptimized execution required' in cp.stderr and not target.exists(),'optimization guard')
for n in ['check.py','canonical.py']:
 ast.parse((P/n).read_text())
N=P/'native';reader=PdfReader(N/'eleven.pdf');native='\n'.join(p.extract_text() or '' for p in reader.pages)
need(len(reader.pages)==2 and native==(P/'native_expected.txt').read_text(),'native exact text')
need(not any(w in (N/'eleven.log').read_text() for w in ['Overfull','LaTeX Warning']),'native quality')
report=dict(status='PASS_AUTHOR_PHASE_INTEGRATION_S11',dependencies=len(json.loads((P/'dependencies.json').read_text())),complete_branches=5,tuples=len(ids),subset_pairs=actual['subset_pairs'],rows=actual['rows'],damaged_controls=2,optimization_guards=4,native_pages=2,full_wrapper_repeated=False,explanation='All positive scientific phases were already complete; exact input/validator/output identity was checked rather than rerunning the census for freeze.')
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
