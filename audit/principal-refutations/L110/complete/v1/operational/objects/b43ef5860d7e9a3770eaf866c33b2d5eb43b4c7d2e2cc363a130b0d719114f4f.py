import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,subprocess,importlib.util
from pypdf import PdfReader
SI=Path('/Users/sasha/medusa/research/leemans/geometry/suzuki_incidence');H=SI/'higher_split_family';R=Path(__file__).resolve().parent
EXPECTED='e805024a62d9f6fdbab2707f9b0e67777fb74c99f2ce24a19f633bd62f12b007'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p,row):need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Exact file '+str(p))
need(sha(H/'manifest.json')==EXPECTED,'Exact frozen author packet')
m=json.loads((H/'manifest.json').read_text());deps=json.loads((H/'dependencies.json').read_text())
for row in m['exports']:bind(H/row['path'],row)
for row in deps:bind(Path(row['path']),row)
out=R/'fresh02';need(not out.exists(),'Fresh replay output');out.mkdir()
spec=importlib.util.spec_from_file_location('author_arithmetic_controls',H/'arithmetic_controls.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
actual=json.loads(json.dumps(c.run()));need(actual==json.loads((H/'arithmetic_controls.json').read_text()),'Eight exact finite controls match')
(out/'arithmetic_controls.json').write_text(json.dumps(actual,indent=2)+'\n')
commands=[]
for k in [1,2]:
    cmd=['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(out),str(H/'split_families.tex')];commands.append(cmd)
    r=subprocess.run(cmd,cwd=H,capture_output=True);(out/f'latex{k}.stdout').write_bytes(r.stdout);(out/f'latex{k}.stderr').write_bytes(r.stderr);r.check_returncode()
need('Overfull' not in (out/'split_families.log').read_text(),'Clean native layout')
a=PdfReader(H/'split_families.pdf');b=PdfReader(out/'split_families.pdf');need(len(a.pages)==len(b.pages)==3,'Exactly three pages')
need([p.extract_text() for p in a.pages]==[p.extract_text() for p in b.pages],'Exact mathematical text')
cmd=['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(out/'page-%02d.png'),str(out/'split_families.pdf')];commands.append(cmd);subprocess.run(cmd,check=True,capture_output=True)
for k in range(1,4):need(sha(H/f'page-{k:02d}.png')==sha(out/f'page-{k:02d}.png'),'Exact native raster')
for row in m['exports']:bind(H/row['path'],row)
for row in deps:bind(Path(row['path']),row)
report=dict(status='PASS_DISTINCT_L110_SPLIT_FAMILY_REPLAY',author_manifest=EXPECTED,dependencies=len(deps),exports=len(m['exports']),native_pages=3,arithmetic_controls=len(actual['rows']),general_proof_by_computation=False,commands=commands)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
