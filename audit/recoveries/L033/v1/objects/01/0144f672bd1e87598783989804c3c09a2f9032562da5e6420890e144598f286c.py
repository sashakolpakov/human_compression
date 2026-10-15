import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,ast,shutil,subprocess
from pypdf import PdfReader
W=Path(__file__).resolve().parent;S=W.parent.parent;P=S/'corpus106_L033_spherical_v2';V=S/'corpus106_L033_spherical_v1';O=W/'final02'
def need(b,m):
 if not b:raise ValueError(m)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
need(not O.exists(),'fresh final output');O.mkdir()
need(h(P/'manifest.json')=='3b717862fe5e794f339b21441a11b09206796cc638f1c91837367c9c18b49360','exact final edition')
manifest=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text())
for r in manifest['exports']:
 p=P/r['path'];need(len(p.read_bytes())==r['bytes'] and h(p)==r['sha256'],'exact final export')
for r in deps:
 p=Path(r['path']);need(len(p.read_bytes())==r['bytes'] and h(p)==r['sha256'],'exact final dependency')
same=['weight_orbits.cpp','verify_weights.py','central_matrices.json']+[str(p.relative_to(P))for p in (P/'certificates').glob('*')]
for n in same:need((P/n).read_bytes()==(V/n).read_bytes(),'unchanged acquired finite input')
for n in ['add','neg','mul','identity','product','verify']:
 def get(p):return next(x for x in ast.parse(p.read_text()).body if isinstance(x,ast.FunctionDef) and x.name==n)
 need(ast.dump(get(P/'central_matrices.py'))==ast.dump(get(V/'central_matrices.py')),'same antipode functions')
old=json.loads((W/'fresh01/finite/report.json').read_text());new=json.loads((P/'finite_report.json').read_text())
need(new==dict(old,E6_orbit_size=27,E6_order=51840),'only new finite result fields')
sys.path.insert(0,str(P));from central_matrices import verify_e6
e6=verify_e6();(O/'E6_order.json').write_text(json.dumps(e6,indent=2)+'\n')
need((O/'E6_order.json').read_bytes()==(P/'E6_order.json').read_bytes(),'new E6 exact replay')
# Independent orbit in dual coordinates, with no author function or inverse.
C=[[2*int(i==j)for j in range(6)]for i in range(6)]
for i,j in [(0,1),(0,2),(2,3),(0,4),(4,5)]:C[i][j]=C[j][i]=-1
need(C==e6['cartan'],'literal E6 tree')
initial=tuple(3*int(i==3)for i in range(6));seen={initial};queue=[initial]
for v in queue:
 for i in range(6):
  image=tuple(v[j]-v[i]*C[j][i]for j in range(6))
  if image not in seen:seen.add(image);queue.append(image)
converted={tuple(sum(C[i][j]*z[j]for j in range(6))for i in range(6))for z in e6['orbit']}
need(seen==converted and len(seen)==27,'independent dual orbit exact agreement')
remaining=[0,1,2,4,5];degrees=sorted(sum(C[i][j]==-1 for j in remaining)for i in remaining)
need(degrees==[1,1,1,2,3] and 27*16*120==51840,'literal D5 deletion and order')
N=O/'native';N.mkdir();shutil.copyfile(P/'spherical_quotients.tex',N/'spherical_quotients.tex')
for i in range(2):
 p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','spherical_quotients.tex'],cwd=N,capture_output=True,timeout=60)
 (N/f'build{i}.stdout').write_bytes(p.stdout);(N/f'build{i}.stderr').write_bytes(p.stderr);need(p.returncode==0 and not p.stderr,'final native build')
need(not any(t in (N/'spherical_quotients.log').read_text()for t in ['Overfull','Underfull','Warning']),'clean final native')
expected=[p.extract_text()for p in PdfReader(P/'spherical_quotients.pdf').pages];actual=[p.extract_text()for p in PdfReader(N/'spherical_quotients.pdf').pages]
need(len(actual)==6 and actual==expected,'exact final native text')
p=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','spherical_quotients.pdf'],cwd=N,capture_output=True,timeout=60)
(N/'render.stderr').write_bytes(p.stderr);need(p.returncode==0 and not p.stderr,'final render')
out=dict(status='PASS_FINAL_V2_DELTA_AND_NATIVE',exports=len(manifest['exports']),dependencies=len(deps),unchanged_finite_files=len(same),acquired_full_replay='fresh01/report.json',full_replay_session=30807,E6_order=51840,E6_orbit=27,independent_dual_orbit=27,native_pages=6)
(O/'report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
