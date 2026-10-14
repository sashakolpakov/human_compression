from pathlib import Path
import json,hashlib,shutil,subprocess
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L027_odd_four_work'
A=S/'corpus106_L027_odd_four_v1';B=S/'corpus106_L027_odd_four_v2'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
if B.exists():raise SystemExit('immutable successor exists')
shutil.copytree(A,B)
t=(B/'odd_four.tex').read_text();t=t.replace('Let $F$ have odd characteristic $p$.','Let $F$ be a finite field of odd characteristic $p$.')
t=t.replace('\\section*{Classification and source qualifications}','\\enlargethispage{2\\baselineskip}\n\\section*{Classification and source qualifications}')
(B/'odd_four.tex').write_text(t)
N=W/'native_v2';N.mkdir()
shutil.copy2(B/'odd_four.tex',N/'odd_four.tex')
for i in (1,2):
 r=subprocess.run(['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','odd_four.tex'],cwd=N,capture_output=True)
 (N/f'latex{i}.stdout').write_bytes(r.stdout);(N/f'latex{i}.stderr').write_bytes(r.stderr)
 if r.returncode:raise SystemExit('native failed')
log=(N/'odd_four.log').read_text()
if any(x in log for x in ['Warning','Overfull','Underfull']):raise SystemExit('native warning')
shutil.copy2(N/'odd_four.pdf',B/'odd_four.pdf')
from pypdf import PdfReader
pages=len(PdfReader(B/'odd_four.pdf').pages)
sc=json.loads((B/'scope.json').read_text());sc['native_pages']=pages;sc['edition']='v2 explicitly states finite field and fits final paragraph';write(B/'scope.json',sc)
deps=json.loads((B/'dependencies.json').read_text());deps.extend(pin(p) for p in [A/'manifest.json',A/'odd_four.tex',A/'scope.json',W/'frozen_check01/report.json']);write(B/'dependencies.json',deps)
write(B/'edition_delta.json',dict(predecessor=pin(A/'manifest.json'),mathematical_change='Explicit finite-field standing hypothesis, already required by the fixed source and all invoked classifications.',layout_change='Enlarge page3 by two baselines to retain final paragraph on the same page.',unchanged_scientific_files=[pin(B/x) for x in ['finite.g','literal.py','finite_expected.json','literal_expected.json','check.py']],prior_full_replay=pin(W/'frozen_check01/report.json'),native_pages=pages))
shutil.copy2(W/'prepare_v2.py',B/'prepare_v2.py')
(B/'development.rst').write_text((B/'development.rst').read_text()+'\nV2 retains all v1 bytes. Full frozen v1 replay54572 passed; final inspection\nmade the finite-field hypothesis explicit and repaired a two-line last-page\nspill. No scientific program or expected output changed.\n')
exports=[]
for p in sorted(B.rglob('*')):
 if p.is_file() and p.name!='manifest.json':
  z=pin(p);z['path']=str(p.relative_to(B));exports.append(z)
write(B/'manifest.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',exports=exports))
subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','odd_four.pdf'],cwd=N,check=True)
print(json.dumps(dict(manifest=pin(B/'manifest.json'),pages=pages,exports=len(exports),deps=len(deps))))
