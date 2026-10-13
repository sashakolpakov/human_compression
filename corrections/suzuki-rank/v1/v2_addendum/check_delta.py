from pathlib import Path
import json,hashlib,subprocess,shutil
from pypdf import PdfReader
S=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent
a=S/'corpus106_F003_rank4_counterexample_v1';b=S/'corpus106_F003_rank4_counterexample_v2'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(b/'manifest.json')=='225b0b354870d9f89669de3e4eb4d0458b6468c0ba78e0feffccd62163a4ee93'
for e in json.loads((b/'manifest.json').read_text())['exports']:
 p=b/e['path'];assert p.stat().st_size==e['bytes'] and h(p)==e['sha256']
for e in json.loads((b/'dependencies.json').read_text())['bindings']:
 p=S/e['path'];assert p.stat().st_size==e['bytes'] and h(p)==e['sha256']
assert (b/'rank4_counterexample.tex').read_text()==(a/'rank4_counterexample.tex').read_text().replace(r'arXiv:1706.05697v1 (2017), \S2.',r'arXiv:1706.05697v1 (2017), \S1.')
for f in ['check.py','check_arithmetic.py','expected_arithmetic.json','program_inventory.json']: assert (a/f).read_bytes()==(b/f).read_bytes()
pa=PdfReader(a/'rank4_counterexample.pdf').pages;pb=PdfReader(b/'rank4_counterexample.pdf').pages
assert len(pa)==len(pb)==5
assert all(pa[i].extract_text()==pb[i].extract_text() for i in range(4))
assert pa[4].extract_text().replace('(2017),§2.','(2017),§1.')==pb[4].extract_text()
shutil.copy2(b/'rank4_counterexample.tex',W)
r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','rank4_counterexample.tex'],cwd=W,capture_output=True);(W/'build.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0
pn=PdfReader(W/'rank4_counterexample.pdf').pages;assert all(pn[i].extract_text()==pb[i].extract_text() for i in range(5))
r=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-dFirstPage=5','-dLastPage=5','-sOutputFile='+str(W/'page05.png'),str(W/'rank4_counterexample.pdf')],capture_output=True);assert r.returncode==0
report={'status':'PASS','author_manifest_sha256':h(b/'manifest.json'),'exports':13,'bindings':45,'only_manuscript_delta':'Recognition bibliography section 2 to section 1','unchanged_programs':['check.py','check_arithmetic.py','expected_arithmetic.json','program_inventory.json'],'unchanged_page_texts':[1,2,3,4],'page5_only_citation_delta':True,'fresh_native_pages':5,'fresh_native_all_page_texts_match':True,'mathematical_computations_repeated':False}
(W/'delta_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
