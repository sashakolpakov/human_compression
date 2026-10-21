from pathlib import Path
import hashlib,json,subprocess,shutil
S=Path('/Users/sasha/medusa/research/leemans');D=S/'reboot_20261013/L091_rank_two_distinct';A=S/'corpus106_L091_rank_two_v1';Q=S/'reboot_20261013/L091_work';O=D/'final_author01';O.mkdir(exist_ok=False)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(p,r):
 if p.stat().st_size!=r['bytes']or h(p)!=r['sha256']:raise ValueError(str(p))
if h(A/'manifest.json')!='cd5d88b1948e753830dad6e5b19714fdc7531c0b826b27d936901380776b8e12':raise ValueError('Author manifest')
m=json.loads((A/'manifest.json').read_text())
for r in m['exports']:ck(A/r['path'],r)
deps=json.loads((A/'dependencies.json').read_text())
for r in deps:ck(Path(r['path']),r)
lib=json.loads((Q/'retained_library_inputs.json').read_text())
for r in lib['files']:ck(Path(r['path']),r)
old=json.loads((D/'working_report.json').read_text())
for r in old['inputs']:
 p=S/r['path']if r['namespace']=='study'else Path(r['path']);ck(p,r)
N=O/'native';N.mkdir();shutil.copyfile(Q/'rank_two.tex',N/'rank_two.tex')
for i in [1,2]:
 r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','rank_two.tex'],cwd=N,capture_output=True,timeout=45)
 (O/f'build{i}.stdout').write_bytes(r.stdout);(O/f'build{i}.stderr').write_bytes(r.stderr)
 if r.returncode or r.stderr:raise ValueError('Native failed')
for p,name in [(Q/'rank_two.pdf','author'),(N/'rank_two.pdf','review')]:
 r=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(p),str(O/(name+'.txt'))],capture_output=True,timeout=30)
 if r.returncode or r.stderr:raise ValueError('Text extraction')
if (O/'author.txt').read_bytes()!=(O/'review.txt').read_bytes():raise ValueError('Native text differs')
r=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(O/'page-%02d.png'),str(N/'rank_two.pdf')],capture_output=True,timeout=30)
if r.returncode or r.stderr:raise ValueError('Raster failure')
report=dict(status='PASS_EXACT_FINAL_AUTHOR_AND_NATIVE',author_manifest_sha256=h(A/'manifest.json'),author_exports=len(m['exports']),author_dependencies=len(deps),library_inventory_files=len(lib['files']),working_math_inputs_identical=True,native_text_identical=True,native_pages=len(list(O.glob('page-*.png'))),no_geometry_census_repeated=True)
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
