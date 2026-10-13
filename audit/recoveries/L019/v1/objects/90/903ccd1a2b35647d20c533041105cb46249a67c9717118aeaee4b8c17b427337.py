from pathlib import Path
import hashlib,json,subprocess,shutil,sys,os
from pypdf import PdfReader
w=Path(__file__).resolve().parent;s=w.parents[1];a=s/'topic_B_L019_anchored_even_v1'
def pin(p):b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(x,m):
 if not x:raise RuntimeError(m)
bindings=[pin(a/'manifest.json')]
for r in json.loads((a/'manifest.json').read_text())['exports']:
 p=a/r['path'];z=pin(p);need(all(z[k]==r[k]for k in ['bytes','sha256']),'export '+r['path']);bindings.append(z)
for r in json.loads((a/'dependencies.json').read_text()):
 p=Path(r['path']);z=pin(p);need(all(z[k]==r[k]for k in ['bytes','sha256']),'dependency '+r['path']);bindings.append(z)
(w/'bindings.json').write_text(json.dumps(bindings,indent=2)+'\n');shutil.copy2(a/'anchored_even.tex',w/'anchored_even.tex');shutil.copy2(a/'build.py',w/'build.py')
r=subprocess.run([sys.executable,str(w/'build.py')],capture_output=True,text=True,timeout=150);(w/'replay.stdout').write_text(r.stdout);(w/'replay.stderr').write_text(r.stderr);need(r.returncode==0 and not r.stderr,'native rebuild')
x=[p.extract_text()for p in PdfReader(a/'anchored_even.pdf').pages];y=[p.extract_text()for p in PdfReader(w/'anchored_even.pdf').pages];need(x==y and len(y)==3,'exact three native pages');warnings=[z for z in(w/'build1.stdout').read_text().splitlines()if any(t in z for t in ['Warning','Overfull','Underfull'])]
for q in bindings:need(pin(Path(q['path']))==q,'changed binding')
(w/'replay_report.json').write_text(json.dumps({'status':'PASS','binding_records':len(bindings),'unique_files':len(set(q['path']for q in bindings)),'native_pages':3,'exact_page_text_match':True,'final_build_warnings':warnings,'mathematical_census_replayed':False,'new_computation_required':False},indent=2)+'\n');print('PASS',len(bindings),'bindings',warnings)
