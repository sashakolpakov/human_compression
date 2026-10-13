import json,hashlib,subprocess,shutil,os,sys
from pathlib import Path
from pypdf import PdfReader
if sys.flags.optimize:raise RuntimeError('optimization forbidden')
S=Path('/Users/sasha/medusa/research/leemans');A=S/'topic_B_L044_contracted_forests_v1';W=S/'reboot_20261013/L044_contracted_forests_distinct';pins={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,h):
 if sha(p)!=h:raise RuntimeError(str(p))
 pins[str(p)]=h
check(A/'manifest.json','00c9d6d1de398d83d4811f21ff23a04446d911ab3646008cf0401daada646c6d')
exp=json.loads((A/'manifest.json').read_text())['exports'];deps=json.loads((A/'dependencies.json').read_text())['bindings']
for e in exp:check(A/e['path'],e['sha256'])
for e in deps:check(S/e['path'],e['sha256'])
N=W/'native01';N.mkdir();shutil.copy2(A/'contracted_forests.tex',N/'contracted_forests.tex');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
for i in [1,2]:
 p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','contracted_forests.tex'],cwd=N,capture_output=True,env=env,timeout=60);(N/f'pass{i}.stdout').write_bytes(p.stdout);(N/f'pass{i}.stderr').write_bytes(p.stderr)
 if p.returncode or p.stderr:raise RuntimeError('native failure')
t=[p.extract_text() for p in PdfReader(N/'contracted_forests.pdf').pages];u=[p.extract_text() for p in PdfReader(A/'contracted_forests.pdf').pages]
if t!=u or len(t)!=3:raise RuntimeError('page mismatch')
warnings=[l for l in (N/'contracted_forests.log').read_text().splitlines() if 'Overfull' in l or 'LaTeX Warning' in l]
if warnings:raise RuntimeError(str(warnings))
subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(N/'page-%d.png'),str(N/'contracted_forests.pdf')],check=True,timeout=60)
for p,h in list(pins.items()):check(Path(p),h)
(W/'input_pins.json').write_text(json.dumps(pins,indent=2)+'\n');r={'status':'PASS_ELEMENTARY_GRAPH_COMPONENT_REPLAY','exports':len(exp),'bindings':len(deps),'native_pages':3,'native_text_equal':True,'warnings':warnings,'all_inputs_unchanged':True,'whole_original_credit':0};(W/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
