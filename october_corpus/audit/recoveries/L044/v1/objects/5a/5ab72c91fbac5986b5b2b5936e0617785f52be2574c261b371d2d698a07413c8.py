import json,hashlib,subprocess,shutil,os,sys
from pathlib import Path
from pypdf import PdfReader
if sys.flags.optimize:raise RuntimeError('optimization forbidden')
S=Path('/Users/sasha/medusa/research/leemans');R=Path('/Users/sasha/medusa/math_compression');A=S/'topic_B_L044_pair_blocks_completion_v1';W=S/'reboot_20261013/L044_pair_blocks_completion_distinct';roots={'private_study':S,'public_repository':R};pins={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,h):
 if sha(p)!=h:raise RuntimeError(str(p))
 pins[str(p)]=h
check(A/'manifest.json','1599e1f800207f726767cd4f5973caa5988df215b9796e44d9fcf91bdf69eb70')
exp=json.loads((A/'manifest.json').read_text())['exports'];deps=json.loads((A/'dependencies.json').read_text())['bindings'];acquired=0
for e in exp:check(A/e['path'],e['sha256'])
for e in deps:
 p=roots[e.get('root','private_study')]/e['path'];check(p,e['sha256'])
 if p.name=='manifest.json':
  for q in json.loads(p.read_text()).get('exports',[]):check(p.parent/q['path'],q['sha256']);acquired+=1
N=W/'native01';N.mkdir();shutil.copy2(A/'pair_blocks_completion.tex',N/'pair_blocks_completion.tex');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
for i in [1,2]:
 p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','pair_blocks_completion.tex'],cwd=N,capture_output=True,env=env,timeout=60);(N/f'pass{i}.stdout').write_bytes(p.stdout);(N/f'pass{i}.stderr').write_bytes(p.stderr)
 if p.returncode or p.stderr:raise RuntimeError('native failure')
t=[p.extract_text() for p in PdfReader(N/'pair_blocks_completion.pdf').pages];u=[p.extract_text() for p in PdfReader(A/'pair_blocks_completion.pdf').pages]
if t!=u or len(t)!=1:raise RuntimeError('page mismatch')
warnings=[l for l in (N/'pair_blocks_completion.log').read_text().splitlines() if 'Overfull' in l or 'LaTeX Warning' in l]
if warnings:raise RuntimeError(str(warnings))
subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(N/'page-%d.png'),str(N/'pair_blocks_completion.pdf')],check=True,timeout=60)
for p,h in list(pins.items()):check(Path(p),h)
(W/'input_pins.json').write_text(json.dumps(pins,indent=2)+'\n');r={'status':'PASS_BOUNDED_ASSEMBLY_REPLAY','exports':len(exp),'bindings':len(deps),'acquired_export_occurrences':acquired,'native_pages':1,'native_text_equal':True,'warnings':warnings,'all_inputs_unchanged':True,'whole_original_credit':0};(W/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
