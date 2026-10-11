#!/usr/bin/env python3
"""Compile complete Topic G TeX twice; compare text and whole code inclusion."""
import argparse,hashlib,json,re,subprocess,unicodedata
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
NAMES=['umbrella','triangle-geometries','steiner-geometries','programs']
def need(p,s):
    if not p:raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(t):return ''.join(c for c in unicodedata.normalize('NFKC',t) if not c.isspace())
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();out=a.out.resolve();need(not out.exists(),'fresh output required');out.mkdir(parents=True)
    rows=[]
    for name in NAMES:
        for i in range(2):
            r=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory',str(out),name+'.tex'],cwd=ROOT,capture_output=True,text=True,timeout=180)
            (out/(name+'.run'+str(i)+'.log')).write_text(r.stdout+r.stderr);need(r.returncode==0,'compile '+name)
        log=(out/(name+'.log')).read_text();need(not re.search(r'Missing character:|Overfull \\hbox|LaTeX Warning:|Package .* Warning:',log),'render diagnostics '+name)
        text=[p.extract_text() or '' for p in PdfReader(out/(name+'.pdf')).pages]
        need(not any(any(ord(c)<32 and c not in '\n\r\t' for c in t) for t in text),'control glyph '+name)
        eq=None
        if (ROOT/(name+'.pdf')).exists():
            eq=text==[p.extract_text() or '' for p in PdfReader(ROOT/(name+'.pdf')).pages];need(eq,'current PDF text differs '+name)
        rows.append(dict(document=name,pages=len(text),pdf_sha256=sha(out/(name+'.pdf')),tex_sha256=sha(ROOT/(name+'.tex')),text_sha256=hashlib.sha256(json.dumps(text,ensure_ascii=False).encode()).hexdigest(),same_text_as_bound=eq,diagnostics=[]))
    # Whole code, including comments, must remain in the printed appendix.
    pieces=[]
    for page in PdfReader(out/'programs.pdf').pages:
        def visitor(t,cm,tm,font,size):
            if tm[4]*cm[1]+tm[5]*cm[3]+cm[5]>55:pieces.append(t)
        page.extract_text(visitor_text=visitor)
    text=norm(''.join(pieces));inc=[]
    for r in json.loads((ROOT/'program_inventory.json').read_text())['programs']:
        need(norm((ROOT/r['path']).read_text()) in text,'code omission '+r['path']);inc.append(r['path'])
    report=dict(status='PASS',documents=rows,complete_code_files=inc,extraction_rule='Whole NFKC nonspace program substring after excluding page-number band below55pt. No code character substitutions.',visual_inspection='Separate author review; this script checks diagnostics/text only.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',documents=len(rows),pages=[r['pages'] for r in rows],whole_code=len(inc))))
if __name__=='__main__':main()
