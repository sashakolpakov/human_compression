"""Acquire the reviewed predecessor and freeze its single displayed correction."""
from pathlib import Path
import hashlib,json,difflib,sys
from pypdf import PdfReader
W=Path(__file__).resolve().parent;Z=W.parent
def need(x,m):
 if not x:raise ValueError(m)
def pin(p):
 p=Path(p).absolute();return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def main():
 need(not(W/'manifest.json').exists(),'fresh corrected edition');rows={}
 def include(q):
  need(pin(q['path'])==q,'exact acquired binding');need(q['path']not in rows or rows[q['path']]==q,'consistent repeated binding');rows[q['path']]=q
 for name,sha in [('subfield_families','079b3780782be50940868cd477e19685fd347fe641594edf4903121af0717b82'),('subfield_families_distinct_review','127eb4e28f25d870947fdaf5633432e4198408056da4fd933c94d3437513085f')]:
  P=Z/name;q=pin(P/'manifest.json');need(q['sha256']==sha,'exact predecessor edition');include(q)
  for e in json.loads((P/'manifest.json').read_text())['exports']:
   q=pin(P/e['path']);need((q['bytes'],q['sha256'])==(e['bytes'],e['sha256']),'unchanged predecessor export');include(q)
  bindings='dependencies.json' if name=='subfield_families' else 'final_bindings.json'
  for q in json.loads((P/bindings).read_text()):include(q)
 old=(Z/'subfield_families/subfields.tex').read_text();new=(W/'subfields.tex').read_text()
 a=r'\Sz(2^e)&\Sz(2^{ep})&';b=r'\Sz(2^e)&\Sz(2^{er})&'
 need(old.count(a)==1 and new==old.replace(a,b),'exact single displayed exponent correction')
 delta=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='frozen/subfields.tex',tofile='corrected/subfields.tex'))
 need((W/'subfields.diff').read_text()==delta,'exact recorded delta')
 need(len(PdfReader(W/'native01/subfields.pdf').pages)==6,'unchanged six-page extent')
 log=(W/'native01/subfields.log').read_text();need('undefined'not in log.lower()and'Overfull'not in log,'complete native build')
 for p in [Path(sys.executable),Path('/opt/homebrew/bin/pdflatex').resolve(),Path('/opt/homebrew/bin/gs').resolve()]:include(pin(p))
 (W/'native01/subfields.tex').write_bytes((W/'subfields.tex').read_bytes())
 (W/'dependencies.json').write_text(json.dumps(list(rows.values()),indent=2)+'\n')
 exports=[]
 for p in sorted(W.rglob('*')):
  if p.is_file():q=pin(p);exports.append(dict(path=str(p.relative_to(W)),bytes=q['bytes'],sha256=q['sha256']))
 (W/'manifest.json').write_text(json.dumps(dict(status='AUTHOR_CORRECTED_L115_SUBFIELD_CLASSIFICATION_AWAITING_DISTINCT_DELTA_REVIEW',exports=exports,proof_pages=6,mathematical_delta='Theorem3 table4 second simple-subfield subgroup exponent ep becomes er; proof unchanged.',whole_original_credit=0,new_conjecture_credit=0,Lean_certificate=False),indent=2)+'\n')
 print(json.dumps(dict(manifest=pin(W/'manifest.json'),exports=len(exports),dependencies=len(rows))))
if __name__=='__main__':main()
