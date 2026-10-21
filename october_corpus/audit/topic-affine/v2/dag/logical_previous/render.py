#!/usr/bin/env python3
"""Render the authored logical reader in a fresh directory; never edit its packet."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
from pypdf import PdfReader
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args()
    if a.out.exists() or a.out.is_symlink():raise ValueError('fresh render output')
    a.out.mkdir(parents=True);src=Path(__file__).resolve().parent/'reader.tex';shutil.copy2(src,a.out/src.name)
    for i in range(2):
        r=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,text=True,capture_output=True)
        (a.out/f'pass{i+1}.log').write_text(r.stdout+r.stderr)
        if r.returncode:raise RuntimeError('XeLaTeX failed')
    log=(a.out/'reader.log').read_text();diagnostics=[x for x in log.splitlines() if re.search(r'Overfull|Underfull|Missing character|LaTeX Warning|Package .* Warning|^!',x)]
    if diagnostics:raise RuntimeError(json.dumps(diagnostics))
    pdf=a.out/'reader.pdf';reader=PdfReader(pdf);texts=[p.extract_text() or '' for p in reader.pages]
    for t in texts:
        if '\ufffd' in t or any(0xE000<=ord(c)<=0xF8FF for c in t):raise RuntimeError('unmapped output glyph')
    report=dict(status='PASS_RENDER_AND_GLYPH_DIAGNOSTICS',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),pages=len(texts),page_text_sha256=[hashlib.sha256(t.encode()).hexdigest() for t in texts],diagnostics=diagnostics)
    (a.out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
