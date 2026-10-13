import json,hashlib,subprocess,shutil,os,sys
from pathlib import Path
from pypdf import PdfReader
if sys.flags.optimize:raise RuntimeError('optimization forbidden')
S=Path('/Users/sasha/medusa/research/leemans');A=S/'topic_B_L044_binary_preserving_neighbours_v1';W=S/'reboot_20261013/L044_binary_preserving_neighbours_distinct';pins={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,h):
 if sha(p)!=h:raise RuntimeError(str(p))
 pins[str(p)]=h
check(A/'manifest.json','5aec551be52b7b29a3fa65d36e346321db1633d4cda1d1b8d0966f06ea05d850')
exp=json.loads((A/'manifest.json').read_text())['exports'];deps=json.loads((A/'dependencies.json').read_text())['bindings'];acquired=0
for e in exp:check(A/e['path'],e['sha256'])
for e in deps:
 p=S/e['path'];check(p,e['sha256'])
 if p.name=='manifest.json':
  for q in json.loads(p.read_text()).get('exports',[]):
   target=p.parent/q['path']
   if not target.exists():
    if p!=S/'topic_B_L047_candidate_v2/retained/common/manifest.json':raise RuntimeError('unrecognized missing export '+str(target))
    check(S/'topic_B_unified/manifest.json','21aeba398dfda4766d3ff441032672ddde2efdac14fef8f67258c971dd827965')
    target=S/'topic_B_unified'/q['path']
   check(target,q['sha256']);acquired+=1
N=W/'native01';N.mkdir();shutil.copy2(A/'binary_preserving_neighbours.tex',N/'binary_preserving_neighbours.tex');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
for i in [1,2]:
 p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','binary_preserving_neighbours.tex'],cwd=N,capture_output=True,env=env,timeout=60);(N/f'pass{i}.stdout').write_bytes(p.stdout);(N/f'pass{i}.stderr').write_bytes(p.stderr)
 if p.returncode or p.stderr:raise RuntimeError('native failure')
t=[p.extract_text() for p in PdfReader(N/'binary_preserving_neighbours.pdf').pages];u=[p.extract_text() for p in PdfReader(A/'binary_preserving_neighbours.pdf').pages]
if t!=u or len(t)!=5:raise RuntimeError('page mismatch')
warnings=[l for l in (N/'binary_preserving_neighbours.log').read_text().splitlines() if 'Overfull' in l or 'LaTeX Warning' in l]
if warnings:raise RuntimeError(str(warnings))
subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(N/'page-%d.png'),str(N/'binary_preserving_neighbours.pdf')],check=True,timeout=60)
for p,h in list(pins.items()):check(Path(p),h)
(W/'input_pins.json').write_text(json.dumps(pins,indent=2)+'\n');r={'status':'PASS_BINARY_PRESERVING_NEIGHBOURS_COMPONENT_REPLAY','exports':len(exp),'bindings':len(deps),'acquired_export_occurrences':acquired,'unique_inputs':len(pins),'native_pages':5,'native_text_equal':True,'warnings':warnings,'all_inputs_unchanged':True,'whole_original_credit':0};(W/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
