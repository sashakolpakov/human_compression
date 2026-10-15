"""Exact page concatenation, with an explicit source-page inventory."""
from pathlib import Path
import json,hashlib
from pypdf import PdfReader,PdfWriter
W=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def build(out,principal,components):
    if out.exists():raise ValueError('fresh reading volume')
    writer=PdfWriter();index=[];start=1
    paths=[('principal',principal)]+[(k,Path(c['proof_pdf']['path']))for k,c in components.items()]
    for name,p in paths:
        reader=PdfReader(p);writer.append(reader,outline_item=name,import_outline=False,excluded_fields=['/Annots']);n=len(reader.pages)
        index.append(dict(component=name,first_page=start,pages=n,input=pin(p)));start+=n
    writer.write(out);r=PdfReader(out);expected=[page.extract_text()for _,p in paths for page in PdfReader(p).pages]
    if [page.extract_text()for page in r.pages]!=expected:raise ValueError('exact concatenated pages')
    streams=[page.get_contents().get_data()for _,p in paths for page in PdfReader(p).pages]
    if [page.get_contents().get_data()for page in r.pages]!=streams:raise ValueError('exact original page content streams')
    return dict(status='EXACT_COMPLETE_PROOF_VOLUME',pages=start-1,manuscripts=len(index),entries=index,output=pin(out),annotation_policy='Original component PDFs are unchanged. This combined reading copy omits annotations and old outlines, and supplies one component bookmark per manuscript. Every page text and decoded content stream equals the source.')
if __name__=='__main__':
    r=build(W/'complete_proofs.pdf',W/'native03/principal.pdf',json.loads((W/'join03/components.json').read_text()));(W/'volume.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'pages':r['pages'],'manuscripts':r['manuscripts']}))
