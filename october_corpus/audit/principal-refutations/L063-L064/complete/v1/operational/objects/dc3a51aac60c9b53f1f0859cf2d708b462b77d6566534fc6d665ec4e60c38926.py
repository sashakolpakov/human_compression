from pathlib import Path
import hashlib,json,shutil,subprocess
from pypdf import PdfReader
P=Path('/Users/sasha/medusa/research/leemans/geometry/psl2_rank_two'); A=P/'q9_geometry'; D=P/'q9_geometry_independent_review'; N=D/'native'
if D.exists(): raise ValueError('fresh directory required')
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
deps={}
def add(p,r=None):
 p=Path(p).resolve();z=pin(p)
 if r and z!={k:r[k] for k in ['bytes','sha256']}:raise ValueError(str(p))
 if str(p)in deps:return
 deps[str(p)]={'path':str(p),**z}
 if p.name=='manifest.json':
  for x in json.loads(p.read_text()).get('exports',[]):add(p.parent/x['path'],x)
 if p.name=='dependencies.json':
  for x in json.loads(p.read_text()):add(x['path'],x)
add(A/'manifest.json');add(P/'arc_actions_root_adoption/manifest.json');add(Path('/private/tmp/review_q9_oct16.py'))
D.mkdir();N.mkdir();shutil.copyfile(A/'doily.tex',N/'doily.tex')
for i in [1,2]:
 r=subprocess.run(['/opt/homebrew/bin/pdflatex','-recorder','-interaction=nonstopmode','-halt-on-error','doily.tex'],cwd=N,capture_output=True,timeout=30)
 (N/f'pass{i}.stdout').write_bytes(r.stdout);(N/f'pass{i}.stderr').write_bytes(r.stderr)
 if r.returncode:raise ValueError('TeX')
r=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile='+str(N/'page-%02d.png'),str(N/'doily.pdf')],capture_output=True,timeout=30)
(N/'render.stdout').write_bytes(r.stdout);(N/'render.stderr').write_bytes(r.stderr)
if r.returncode:raise ValueError('render')
if [p.extract_text() for p in PdfReader(N/'doily.pdf').pages]!=[p.extract_text()for p in PdfReader(A/'doily.pdf').pages]:raise ValueError('text')
ims=sorted(N.glob('page-*.png'))
if len(ims)!=3 or any(x.read_bytes()!=(A/'native'/x.name).read_bytes() for x in ims):raise ValueError('raster')
r=subprocess.run(['/Users/sasha/.venvs/global/bin/python',str(A/'check_duality.py'),'--out',str(D/'literal.json')],capture_output=True,timeout=10)
(D/'literal.stdout').write_bytes(r.stdout);(D/'literal.stderr').write_bytes(r.stderr)
if r.returncode:raise ValueError('literal')
for line in (N/'doily.fls').read_text().splitlines():
 if line.startswith('INPUT '):
  p=Path(line[6:]);p=p if p.is_absolute() else N/p
  if p.exists() and not p.is_relative_to(N):add(p)
for i in [3,22]:
 for ext in ['pdf','png']:add(P/f'arc_actions_independent_review/source/page-{i:02d}.{ext}')
write(D/'dependencies.json',list(deps.values()));write(D/'replay.json',dict(status='PASS_LITERAL_AND_NATIVE',dependencies=len(deps),pages=3,text_identical=True,rasters_byte_identical=True,literal=json.loads((D/'literal.json').read_text()),whole_source_credit=0,group_order_searches=0))
print((D/'replay.json').read_text())
